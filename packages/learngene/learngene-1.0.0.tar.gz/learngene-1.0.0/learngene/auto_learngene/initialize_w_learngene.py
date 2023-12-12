import argparse
import logging
import time
import datetime
import sys
sys.path.append('../')
import copy
import numpy as np
import os
import shutil
import random
import warnings
import xlwt
# import dill as pickle

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, ConcatDataset
from torch.autograd import Variable
#from check_dataset import check_dataset
#from check_model import check_model
from utils.utils import AverageMeter, accuracy, set_logging_config
from learngene.data_all.dataloader.dataloader import get_inheritable_auto
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import scipy
from scipy.stats import t
from extract_learngene import auto_extract


CIFAR100_TRAIN_MEAN = (0.5070751592371323, 0.48654887331495095, 0.4409178433670343)
CIFAR100_TRAIN_STD = (0.2673342858792401, 0.2564384629170883, 0.27615047132568404)

record_time = str((datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d_%H:%M:%S'))

RESULT_PATH_VAL = ''


def save_checkpoint(states, is_best, output_dir, filename='checkpoint.pth'):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
        print('making dir: %s'%output_dir)
        
    torch.save(states, os.path.join(output_dir, filename))
    
    if is_best and 'state_dict' in states:
        torch.save(states['state_dict'], os.path.join(output_dir, 'model_best.pth'))
        
def auto_initialize(data_name, path, model_c, batchSize = 64, epochs = 100, lr = 0.0005, weight_decay = 0.0005, num_imgs_per_class = 20, num_classes = 5,
                    momentum = 0.9, no_cuda = 'False', seed = 1, arch = 'dino_small_patch16', num_works = 10, experiment = 'logs/less_sensitive', ):

    inherit_path = path

    log_file = data_name + '_' + model_c + '_' + str(batchSize) + '_' + str(epochs) \
               + '_' + str(num_classes) + 'way' + str(num_imgs_per_class) + 'shot_' + 'meta-learning' \
               + '_lr_' + str(lr) + 'decay_' + str(weight_decay) + '.txt'

    set_logging_config(experiment, log_file)
    cuda = not no_cuda and torch.cuda.is_available()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    torch.manual_seed(seed)
    if cuda:
        torch.cuda.manual_seed(seed)

    lr_ = lr

    logger = logging.getLogger('auto_initialize')
    logger.info(' '.join(os.sys.argv))

    #print("Data loading...")
    #loaders = check_dataset(args)
    
    print("Model constructing...")

    if model_c == 'vgg':
        from utils.models.vgg_cifar import vgg_compression_meta_learngene
        layer_1, layer_2, layer_3, layer_4 = auto_extract(model_c, arch)

        individual_model = vgg_compression_meta_learngene(layer_1, layer_2, layer_3, layer_4, num_classes = num_classes)
    
    elif model_c == 'resnet':
        from utils.models.resnet_ilsvrc import resnet18
        from utils.models.res12 import resnet12, ResNet_meta_learngene

        layer_1, layer_2, layer_3, layer_4 = auto_extract(model_c, arch)
        individual_model = ResNet_meta_learngene(layer_1, layer_2, layer_3, layer_4, num_classes = num_classes)

            
        
    elif model_c == 'swin':
        from utils.models.model_transformer import swin_tiny_patch4_window7_224, swin_small_patch4_window7_224, SwinTransformer_with_learngene
        #print(collective_model)
        #exit()

        layers_0, layers_2, layers_3 = auto_extract(model_c, arch)

        individual_model = SwinTransformer_with_learngene(num_classes=5, inherited_layers_0 = layers_0, inherited_layers_2 = layers_2, inherited_layers_3 = layers_3)

        
    elif model_c == 'vit-dino':
        from utils.models import get_model
        from utils.models.vision_transformer import vitsmall_with_learngene
        collective_model = get_model(arch=arch)
        patch_embed = collective_model.patch_embed
        cls_token = collective_model.cls_token
        pos_embed = collective_model.pos_embed
        pos_drop = collective_model.pos_drop
        #print(cls_token)
        #print(pos_embed)
        layers_0, layers_2 = auto_extract(model_c, arch)

        individual_model = vitsmall_with_learngene(num_classes=5, inherited_layers_0 = layers_0, inherited_layers_2 = layers_2, patch_embed=patch_embed, cls_token=cls_token, pos_embed=pos_embed, pos_drop=pos_drop)

        
        
    #print(individual_model)    
    model_v = copy.deepcopy(individual_model)
    del individual_model

    individual_model = model_v
    # individual_model = individual_model.cuda()
    
    '''conv2_params = list(map(id, individual_model.layer4[0].conv2.parameters()))
    bn2_params = list(map(id, individual_model.layer4[0].bn2.parameters()))
    conv3_params = list(map(id, individual_model.layer4[0].conv3.parameters()))
    bn3_params = list(map(id, individual_model.layer4[0].bn3.parameters()))
    base_params = filter(lambda p: id(p) not in conv2_params + bn2_params + conv3_params + bn3_params, individual_model.parameters())'''
    
    
    optimizer = optim.SGD(individual_model.parameters(), lr=lr, momentum=momentum,  weight_decay=weight_decay)
    #print(optimizer)
    #exit()
    
    print("Data loading...")
    trainloader_inheritable, testloader_inheritable = get_inheritable_auto(data_name, num_works, batchSize, num_imgs_per_cate=num_imgs_per_class, path=inherit_path)

    #print(args.num_imgs_per_class)
    #print(args.lr)
    #print(args.weight_decay)
    #exit()
    
    def mean_confidence_interval(data, confidence=0.95):
        a = 1.0 * np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * t._ppf((1+confidence)/2., n-1)
        return m, h
    
    def validate(model, loader):
        #acc = []
        acc = AverageMeter()                      
        model.eval()                              
        #count = random.randint(0,30)
        for i, (x, y) in enumerate(loader):
            #print(y)
            #exit()
            #if i != count:
            #    continue
            x, y = x.to(device), y.to(device)
            if model_c == 'vgg':
                y_pred = model(x)
            elif model_c == 'resnet':
                y_pred, [f1, f2, f3, f4] = model(x)
            elif model_c == 'swin':
                y_pred = model(x)
            elif model_c == 'vit-dino':
                y_pred = model(x)
            #query_ys_pred = clf.predict(y_pred.cpu().detach().numpy())
            #acc.append(metrics.accuracy_score(y.cpu().numpy(), query_ys_pred))
            acc.update(accuracy(y_pred.data, y, topk=(1,))[0].item(), x.size(0))
            
        return acc.avg            
        #return mean_confidence_interval(acc)

    def objective(data, model):   
        x, y = data[0].to(device), data[1].to(device)
        if model_c == 'vgg':
            y_pred = model(x)
        elif model_c == 'resnet':
            y_pred, [f1, f2, f3, f4] = model(x)
        elif model_c == 'swin':
            y_pred = model(x)
        elif model_c == 'vit-dino':
            y_pred = model(x)
        #clf.fit(y_pred.data.cpu().numpy(), y.cpu().numpy()) 
        
        state['accuracy'] = accuracy(y_pred.data, y, topk=(1,))[0].item()
        loss = F.cross_entropy(y_pred, y)
        state['loss'] = loss.item()
        return loss
    
    acc_all = []
    for task in range(num_works):
        
        '''optimizer = torch.optim.SGD([
            {'params': base_params},
            {'params': individual_model.layer4[0].conv2.parameters(), 'lr': args.lr / 100},
            {'params': individual_model.layer4[0].bn2.parameters(), 'lr': args.lr / 100},
            {'params': individual_model.layer4[0].conv3.parameters(), 'lr': args.lr / 100},
            {'params': individual_model.layer4[0].bn3.parameters(), 'lr': args.lr / 100}
            ], lr=args.lr, momentum=args.momentum,  weight_decay=args.weight_decay)'''
        
        print("Individual Task {} begins !".format(task))
        state = {
            'model': individual_model.state_dict(),
            'optimizer': optimizer.state_dict(),
            'best': 0.0
        }
        logger.info(optimizer)
        print(optimizer)
        '''clf = LogisticRegression(penalty='l2',
                                         random_state=0,
                                         C=1.0,
                                         solver='lbfgs',
                                         max_iter=1000,
                                         multi_class='multinomial')'''
        
        
        for epoch in range(epochs):
            state['epoch'] = epoch
            state['iter'] = 0
            trainloader = trainloader_inheritable[task](epoch)
            testloader = testloader_inheritable[task](epoch)

            for i, data in enumerate(trainloader):
                optimizer.zero_grad()
                objective(data, individual_model).backward() 
                optimizer.step(None)

                if i%10 == 0:
                    print( '[Epoch {:3d}] [Iter {:3d}] [Loss {:.4f}] [Acc {:.4f}] '.format(
                        state['epoch'], state['iter'],
                        state['loss'], state['accuracy']) )


                logger.info('[Epoch {:3d}] [Iter {:3d}] [Loss {:.4f}] [Acc {:.4f}] '.format(
                    state['epoch'], state['iter'],
                    state['loss'], state['accuracy']))
                state['iter'] += 1

            acc = validate(individual_model, testloader)

            if state['best'] < acc:
                state['best'] = acc

            #if state['epoch'] % 10 == 0:
            #    torch.save(state, os.path.join(opt.experiment, 'ckpt-{}.pth'.format(state['epoch']+1)))
            if epoch % 10 == 0:
                logger.info('[Epoch {}] [test {:.4f}] [best {:.4f}]'.format(epoch, acc, state['best']) )
                print( '[Epoch {}] [test {:.4f}] [best {:.4f}]'.format(epoch, acc, state['best'] ) )

        #logger.info('[Epoch {}] [test {:.4f}] [best {:.4f}]'.format(epoch, acc, state['best']) )
        #print( '[Epoch {}] [test {:.4f}] [best {:.4f}]'.format(epoch, acc, state['best'] ) )
        del individual_model
        individual_model = model_v
        individual_model = individual_model.cuda()
        
        print("Individual Task {0} finished !".format(task))
        acc_all.append(state['best'])
    
    mean_acc, std_acc = mean_confidence_interval(acc_all) 
    logger.info('[All test accuracy {}] [mean test accuracy {:.4f}] [std test accuracy {:.4f}]'.format(acc_all, mean_acc, std_acc ) )
    print( '[All test accuracy {}] [mean test accuracy {:.4f}] [std test accuracy {:.4f}]'.format(acc_all, mean_acc, std_acc )  )
    
    #logger.info('[All test accuracy {}] [mean test accuracy {:.4f}] [std test accuracy {:.4f}]'.format(acc_all, np.array(acc_all).mean(), np.array(acc_all).std() ) )
    #print( '[All test accuracy {}] [mean test accuracy {:.4f}] [std test accuracy {:.4f}]'.format(acc_all, np.array(acc_all).mean(), np.array(acc_all).std() )  )

auto_initialize('cifar100', "../data_all/datasets/exp_data/data_cifar100/2023-12-12_21_52_12/inheritabledataset", 'vgg')
