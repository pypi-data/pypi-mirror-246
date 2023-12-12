import os
import argparse
import logging

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
from utils.models import vgg_ilsvrc as ivgg

#from check_dataset import check_dataset
from utils.utils import AverageMeter, accuracy, set_logging_config
from utils.meta_optimizers import MetaSGD
import numpy as np
from utils.conf import settings

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"

torch.backends.cudnn.benchmark = True

## python3.6 train_learngene.py --dataset cifar100 --datasplit cifar100 --dataroot /data/ --experiment logs/cifar100_source_vgg16/ --source-path logs --source-model vgg16_bn --source-domain cifar --target-model vgg9_bn --pairs 0-0,0-1,0-2,0-3,0-4,1-0,1-1,1-2,1-3,1-4,2-0,2-1,2-2,2-3,2-4,3-0,3-1,3-2,3-3,3-4,4-0,4-1,4-2,4-3,4-4 --batchSize 128

def check_model(model_c, num_classes):
    if model_c.startswith('resnet'):
        '''
        if opt.dataset in ['cub200', 'indoor', 'stanford40', 'flowers102', 'dog', 'tinyimagenet']:
            ResNet = resnet_ilsvrc.__dict__[opt.model]
            model = ResNet(num_classes=opt.num_classes)
        else:
            ResNet = cresnet.__dict__[opt.model]
            model = ResNet(num_classes=opt.num_classes)'''
        from utils.models.res12 import resnet12
        model = resnet12(num_classes=num_classes)
        return model

    elif model_c.startswith('vgg'):
        VGG = ivgg.__dict__[model_c]
        model = VGG(num_classes=num_classes)
        return model

    elif model_c.startswith('vit'):
        from utils.models.vision_transformer_wfeature import vit_small_6
        model = vit_small_6(num_classes=num_classes)
        return model

    else:
        raise Exception('Unknown model')

def _get_num_features(model):
    if model.startswith('resnet'):
        n = int(model[6:])
        if n in [18, 34, 50, 101, 152]:
            return [64, 64, 128, 256, 512]
        elif n == 12:
            return [64, 128, 256, 512]
            
    elif model.startswith('vgg'):
        n = int(model[3:].split('_')[0])
        if n == 9:
            return [64, 128, 256, 512, 512]
        elif n == 16:
            return [64, 128, 256, 512, 512]

    elif model.startswith('vit'):
        n = int(model[3:])
        if n == 6:
            #return [384, 384, 384]
            return [196, 196, 196]
        if n == 12:
            #return [384, 384, 384, 384, 384, 384]
            return [196, 196, 196, 196, 196, 196]

    raise NotImplementedError


class FeatureMatching(nn.ModuleList):
    def __init__(self, source_model, target_model, pairs):
        super(FeatureMatching, self).__init__()
        self.src_list = _get_num_features(source_model)
        self.tgt_list = _get_num_features(target_model)
        self.pairs = pairs

        if self.opt.source_domain == 'ImageNet-vit': 
            for src_idx, tgt_idx in pairs:
                #self.append(nn.Linear(self.tgt_list[tgt_idx], self.src_list[src_idx]))
                self.append(nn.Identity())
        else:
            for src_idx, tgt_idx in pairs:
                self.append(nn.Conv2d(self.tgt_list[tgt_idx], self.src_list[src_idx], 1))
        

    def forward(self, source_features, target_features,
                 loss_weight):  # weight=w_c^{m,n}, loss_weight=\lambda^{m,n} [15,128]

        matching_loss = 0.0
        #a = np.array(loss_weight)
        #for i in range(15):
        #    print( a[i].sum()/128.0 )

        for i, (src_idx, tgt_idx) in enumerate(self.pairs):
            sw = source_features[src_idx].size(2)
            tw = target_features[tgt_idx].size(2)
            if sw == tw:
                diff = source_features[src_idx] - self[i](target_features[tgt_idx])
            else:
                diff = F.interpolate(  
                    source_features[src_idx],
                    scale_factor=tw / sw,
                    mode='bilinear'
                ) - self[i](target_features[tgt_idx])#Down/up samples the input to either the given size or the given scale_factor

            if self.opt.source_domain == 'ImageNet-vit':
                diff = torch.abs(diff).mean(2)
            else:
                diff = diff.pow(2).mean(3).mean(2)
                

            if loss_weight is None:
                diff = diff.mean(1).mean(0)#.mul(beta[i])
            else:
                # temperature = 0.5 # add
                # loss_weight[i] = F.softmax(loss_weight[i]/temperature, dim=1) # add
                diff = (diff.mean(1)*(loss_weight[i].squeeze())).mean(0)#.mul(beta[i])
            
            #if self.opt.source_domain == 'ImageNet-vit': 
            #    diff = F.relu6(diff)
                
            #print(diff)
            '''
            if loss_weight is None and weight is None:
                diff = diff.mean(1).mean(0).mul(beta[i])
            elif loss_weight is None:
                diff = diff.mul(weight[i]).sum(1).mean(0).mul(beta[i])
            elif weight is None:
                diff = (diff.sum(1)*(loss_weight[i].squeeze())).mean(0).mul(beta[i])
            else:
                diff = (diff.mul(weight[i]).sum(1)*(loss_weight[i].squeeze())).mean(0).mul(beta[i])'''
            
            matching_loss = matching_loss + diff

        return matching_loss

class LossWeightNetwork(nn.ModuleList):
    def __init__(self, source_model, pairs, weight_type='relu', init=None):
        super(LossWeightNetwork, self).__init__()
        n = _get_num_features(source_model) # see Line-21
        if weight_type == 'const':
            self.weights = nn.Parameter(torch.zeros(len(pairs)))
        else:
            for i, _ in pairs:
                #if self.opt.source_domain == 'ImageNet-vit': 
                #    l = nn.Linear(196, 1)
                #else:
                l = nn.Linear(n[i], 1)
                if init is not None:
                    nn.init.constant_(l.bias, init)
                self.append(l)
        self.pairs = pairs  # 提前给定的pairs
        self.weight_type = weight_type

    def forward(self, source_features):
        outputs = []
        if self.weight_type == 'const':
            for w in F.softplus(self.weights.mul(10)):
                outputs.append(w.view(1, 1))
        else:
            for i, (idx, _) in enumerate(self.pairs): #每个pairs都有相应的fc网络
                if self.opt.source_domain == 'ImageNet-vit':  
                    f = source_features[idx]  #[batch, num_patch, token]
                    f = F.avg_pool1d(f, f.size(2)).view(-1, f.size(1)) #保留[batch, channel]
                else:
                    f = source_features[idx]  # [batch, channel, h, w] h=w
                    f = F.avg_pool2d(f, f.size(2)).view(-1, f.size(1)) #保留[batch, channel]
                if self.weight_type == 'relu':
                    outputs.append(F.relu(self[i](f)))
                elif self.weight_type == 'relu-avg':
                    outputs.append(F.relu(self[i](f.div(f.size(1)))))
                elif self.weight_type == 'relu6':
                    outputs.append(F.relu6(self[i](f)))
        return outputs
    
    def printf(self):
        for i, layer in enumerate(self):
            print("{0}-layer:{1}".format(i, layer))


def auto_train(source_domain, source_model_c, source_path_c, model_c, target_model_c, nesterov, num_classes, batchSize = 64, epochs = 100, T = 5,
               lam = 1.0, loss_weight = True, loss_weight_type = 'relu6', loss_weight_init = 1.0, optimizer = 'adam', lr = 0.1, meta_lr = 1e4,
               wd = 0.0001, meta_wd = 1e-4, momentum = 0.9, schedule = 'True', pairs_c = '4-4,4-3,4-2,4-1,3-4,3-3,3-2,3-1,2-4,2-3,2-2,2-1,1-4,1-3,1-2,1-1',
               experiment = 'logs'):

    # default settings
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    os.makedirs(experiment)
    set_logging_config(experiment, 'log.txt')
    logger = logging.getLogger('auto_train')
    logger.info(' '.join(os.sys.argv))

    if source_domain == 'ImageNet-vit':
        T = 2
        lam = 0.1
        
        
    # load source model
    if source_domain == 'cifar':
        #from models import resnet_ilsvrc
        from utils.models.vgg_cifar import vgg16_bn_cifar64, vgg_compression_meta_learngene
        source_model = vgg16_bn_cifar64()
        source_model.load_state_dict(torch.load('./checkpoint/vgg16/Monday_06_November_2023_16h_34m_05s/vgg16-2-best.pth'))
        source_model = torch.nn.DataParallel(source_model)
        source_model = source_model.to(device)
        num_classes = 16
        
    elif source_domain == 'MiniImageNet':
        from utils.models.resnet_ilsvrc import resnet18
        source_model = resnet18(num_classes=64)
        source_model.load_state_dict(torch.load('./checkpoint/resnet18/Monday_29_August_2022_15h_16m_37s/resnet18-180-regular.pth'))
        source_model = torch.nn.DataParallel(source_model)
        source_model = source_model.to(device)
        num_classes = 16
    
    elif source_domain == 'ImageNet-vit':
        from utils.models import vision_transformer_wfeature as vit
        source_model = vit.__dict__['vit_small'](patch_size=16, num_classes=0)
        source_model.load_state_dict(torch.load('./models/checkpoint/dino_deitsmall16_pretrain.pth'), strict=True)
        source_model = torch.nn.DataParallel(source_model)
        source_model = source_model.to(device)
        num_classes = 16

    elif source_domain == 'TinyImageNet':
        model_c = source_model_c
        weights = []
        source_gen_params = []
        source_path = os.path.join(
            source_path_c, '{}-{}'.format(source_domain, source_model_c),
            '0',
            'model_best.pth.tar'
        )
        ckpt = torch.load(source_path)
        num_classes = ckpt['num_classes']
        source_model = check_model(model_c, num_classes)
        #source_model=nn.DataParallel(source_model,device_ids=[0,1])
        source_model.load_state_dict(ckpt['state_dict'], strict=False)
        source_model = torch.nn.DataParallel(source_model)
        source_model = source_model.to(device)
        
    pairs = []
    for pair in pairs_c.split(','):
        pairs.append((int(pair.split('-')[0]),
                      int(pair.split('-')[1])))
    
    if loss_weight:
        lwnet = LossWeightNetwork(source_model_c, pairs, loss_weight_type, loss_weight_init)
        lwnet = torch.nn.DataParallel(lwnet)
        lwnet = lwnet.to(device)
        weight_params = list(lwnet.parameters())

    #if opt.loss_weight:
    #    ckpt = torch.load(opt.lwnet_path)
    #    lwnet.load_state_dict(ckpt['lw'])

    if optimizer == 'sgd':
        source_optimizer = optim.SGD(weight_params, lr=meta_lr, weight_decay=meta_wd, momentum=momentum, nesterov=nesterov)
    else:
        source_optimizer = optim.Adam(weight_params, lr=meta_lr, weight_decay=meta_wd)

    # load dataloaders
    #loaders = check_dataset(opt)
    if source_domain == 'cifar':
        transform_learngene = transforms.Compose([
            #transforms.ToPILImage(),
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor(),
            transforms.Normalize(settings.CIFAR100_TRAIN_MEAN, settings.CIFAR100_TRAIN_STD)
        ])
        cifar16_training = datasets.ImageFolder('./cifar100-open/open-world',
                                                transform=transform_learngene)                
        loaders = DataLoader(
            cifar16_training, shuffle=True, num_workers=4, batch_size=batchSize)
        print("Use Cifar:")
    elif source_domain == 'MiniImageNet' or source_domain == 'ImageNet-vit':
        mean_pix  = [0.485, 0.456, 0.406]
        std_pix   = [0.229, 0.224, 0.225]
        transform_train = transforms.Compose([
                        transforms.Resize(224),
                        transforms.RandomCrop(224),
                        transforms.RandomHorizontalFlip(),
                        lambda x: np.asarray(x),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=mean_pix, std=std_pix)
                    ])
        MiniImageNet16_training = datasets.ImageFolder('/root/data2/datasets/MiniImageNet/val',
                                                transform=transform_train)                
        loaders = DataLoader(
            MiniImageNet16_training, shuffle=True, num_workers=4, batch_size=batchSize)
        print("Use MiniImageNet:")


    # load target model
    model_c = target_model_c
    target_model = check_model(model_c, num_classes)
    target_model = torch.nn.DataParallel(target_model)
    target_model = target_model.to(device)
    target_branch = FeatureMatching(source_model_c,
                                    target_model_c,
                                    pairs)
    target_branch = torch.nn.DataParallel(target_branch)
    target_branch = target_branch.to(device)
    target_params = list(target_model.parameters()) + list(target_branch.parameters())
    if meta_lr == 0:
        target_optimizer = optim.SGD(target_params, lr=lr, momentum=momentum, weight_decay=wd)
    else:
        target_optimizer = MetaSGD(target_params,
                                   [target_model, target_branch],
                                   lr=lr,
                                   momentum=momentum,
                                   weight_decay=wd, rollback=True, cpu=T>2)

    state = {
        'target_model': target_model.state_dict(),
        'target_branch': target_branch.state_dict(),
        'target_optimizer': target_optimizer.state_dict(),
        'best': (0.0, 0.0)
    }

    scheduler = optim.lr_scheduler.CosineAnnealingLR(target_optimizer, epochs)

    def validate(model, loader):
        acc = AverageMeter()
        model.eval()
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            y_pred, _ = model(x)
            acc.update(accuracy(y_pred.data, y, topk=(1,))[0].item(), x.size(0))
        return acc.avg

    '''def inner_objective(data, matching_only=False):
        x, y = data[0].to(device), data[1].to(device)
        y_pred, target_features = target_model.forward(x)

        with torch.no_grad():
            s_pred, source_features = source_model.forward(x)
        
        #print(len(source_features))


        weights = wnet(source_features)
        state['loss_weights'] = ''
        if opt.loss_weight:
            loss_weights = lwnet(source_features)
            state['loss_weights'] = ' '.join(['{:.2f}'.format(lw.mean().item()) for lw in loss_weights])
        else:
            loss_weights = None
            
        # 删除beta
        beta = [opt.beta] * lenwnet

        matching_loss = target_branch(source_features,
                                      target_features,
                                      weights, beta, loss_weights)

        state['accuracy'] = accuracy(y_pred.data, y, topk=(1,))[0].item()

        if matching_only:
            return matching_loss

        loss = F.cross_entropy(y_pred, y)
        state['loss'] = loss.item()
        print(loss)
        print(matching_loss)
        return loss + matching_loss ''' # total loss
        #return matching_loss 
        
    def inner_objective(data, meta_data, matching_only=False):
        x, y = data[0].to(device), data[1].to(device)
        meta_x, meta_y = meta_data[0].to(device), meta_data[1].to(device)
        
        #print("target model on x")
        y_pred, _a = target_model.forward(x)
        
        #print("target model on meta_x")
        _b, target_features = target_model.forward(meta_x)

        with torch.no_grad():
            #print("source model on meta_x")
            s_pred, source_features = source_model.forward(meta_x)
        
        #print(len(source_features))
        state['loss_weights'] = ''
        if loss_weight:
            loss_weights = lwnet(source_features)
            state['loss_weights'] = ' '.join(['{:.2f}'.format(lw.mean().item()) for lw in loss_weights])
        else:
            loss_weights = None

        matching_loss = target_branch(source_features,
                                      target_features,
                                      loss_weights)

        state['accuracy'] = accuracy(y_pred.data, y, topk=(1,))[0].item()

        if matching_only:
            return matching_loss

        loss = F.cross_entropy(y_pred, y)
        state['loss'] = loss.item()
        print(loss)
        print(matching_loss)
        return loss + lam*matching_loss

    def outer_objective(data):
        x, y = data[0].to(device), data[1].to(device)
        y_pred, _ = target_model(x)
        state['accuracy'] = accuracy(y_pred.data, y, topk=(1,))[0].item()
        loss = F.cross_entropy(y_pred, y)
        state['loss'] = loss.item()
        return loss

    # source generator training
    state['iter'] = 0
    
    ############################################## adding meta data
    for i, data in enumerate(loaders):
        meta_data = data
        break
    
    
    for epoch in range(epochs):
        if schedule:
            scheduler.step()

        state['epoch'] = epoch
        
        # layers = source_model.get_layers_19_20()
        #compose target model
        '''
        target_model = vgg_compression_ONE(layers, 2048, num_class = 100)
        model_v = copy.deepcopy(target_model)
        del target_model
        target_model = model_v
        #model_vgg.printf()
        target_model = target_model.cuda()'''
        
        target_model.train()
        source_model.eval()
        for i, data in enumerate(loaders):
            if i == 0:
                continue
            target_optimizer.zero_grad()
            inner_objective(data, meta_data).mean().backward()  # only return matching_loss
            target_optimizer.step(None)

            logger.info('[Epoch {:3d}] [Iter {:3d}] [Loss {:.4f}] [Acc {:.4f}] [LW {}]'.format(
                state['epoch'], state['iter'],
                state['loss'], state['accuracy'], state['loss_weights']))
            state['iter'] += 1
            
            for _ in range(T): # inner_objective = loss_meta, update parameter w
                target_optimizer.zero_grad() 
                target_optimizer.step(inner_objective, data, meta_data, True) # 等于loss = inner_objective(data, True) 然后loss.sum().backward()
                # return loss + matching_loss
            
            target_optimizer.zero_grad() # outer_objective = loss_cross_entropy, update parameter w
            target_optimizer.step(outer_objective, data)

            target_optimizer.zero_grad()
            source_optimizer.zero_grad()
            outer_objective(data).mean().backward()
            target_optimizer.meta_backward()
            source_optimizer.step()     # update meta-parameter \phi
            
            #print('ok')
            #exit()
        
        
        '''acc = (validate(target_model, loaders[1]), validate(target_model, loaders[2]))

        if state['best'][0] < acc[0]:
            state['best'] = acc'''

        if state['epoch'] % 10 == 0:
            torch.save(state, os.path.join(experiment, 'ckpt-{}.pth'.format(state['epoch']+1)))

        #logger.info('[Epoch {}] [val {:.4f}] [test {:.4f}] [best {:.4f}]'.format(epoch, acc[0], acc[1], state['best'][1]))
