# train.py
#!/usr/bin/env	python3

import os
import sys
import argparse
import time
from datetime import datetime
from multiprocessing import freeze_support
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets

from torch.utils.data import DataLoader
# from torch.utils.tensorboard import SummaryWriter

from utils.conf import settings
from utils.utils import get_training_dataloader, get_test_dataloader, WarmUpLR, \
    most_recent_folder, most_recent_weights, last_epoch, best_acc_weights



def get_network(net_c):
    """ return given network
    """

    if net_c == 'vgg16':
        from utils.models.vgg_cifar import vgg16_bn_cifar64
        net = vgg16_bn_cifar64()
        
    elif net_c == 'resnet12':
        from utils.models.res12 import resnet12
        net = resnet12(num_classes=64)
    
    elif net_c == 'resnet18':
        from utils.models.resnet_ilsvrc import resnet18
        net = resnet18(num_classes=64)
        
    elif net_c == 'swin-s':
        from utils.models.model_transformer import swin_small_patch4_window7_224
        net = swin_small_patch4_window7_224(num_classes=64)
        


    else:
        print('the network name you have entered is not supported yet')
        sys.exit()

    # if args.gpu: #use_gpu
    #     net = net.cuda()
    
    #print(net)
    #exit()
    return net

def train(training_loader, optimizer, loss_function, epoch, net_c, net, batch_size, warm, warmup_scheduler):

    start = time.time()
    net.train()
    for batch_index, (images, labels) in enumerate(training_loader):

        # if args.gpu:
        #     labels = labels.cuda()
        #     images = images.cuda()

        optimizer.zero_grad()
        if net_c == 'swin-s':
            outputs = net(images)
        else:
            outputs, [r1, f2, f3, f4, f5] = net(images)
        loss = loss_function(outputs, labels)
        loss.backward()
        optimizer.step()

        n_iter = (epoch - 1) * len(training_loader) + batch_index + 1

        last_layer = list(net.children())[-1]
        '''for name, para in last_layer.named_parameters():
            if 'weight' in name:
                writer.add_scalar('LastLayerGradients/grad_norm2_weights', para.grad.norm(), n_iter)
            if 'bias' in name:
                writer.add_scalar('LastLayerGradients/grad_norm2_bias', para.grad.norm(), n_iter)'''

        print('Training Epoch: {epoch} [{trained_samples}/{total_samples}]\tLoss: {:0.4f}\tLR: {:0.6f}'.format(
            loss.item(),
            optimizer.param_groups[0]['lr'],
            epoch=epoch,
            trained_samples=batch_index * batch_size + len(images),
            total_samples=len(training_loader.dataset)
        ))

        #update training loss for each iteration
        #writer.add_scalar('Train/loss', loss.item(), n_iter)

        if epoch <= warm:
            warmup_scheduler.step()

    for name, param in net.named_parameters():
        layer, attr = os.path.splitext(name)
        attr = attr[1:]
        #writer.add_histogram("{}/{}".format(layer, attr), param, epoch)

    finish = time.time()

    print('epoch {} training time consumed: {:.2f}s'.format(epoch, finish - start))

cifar100_test_loader = get_test_dataloader(settings.CIFAR100_TEST_MEAN, settings.CIFAR100_TEST_STD, num_workers = 0)

@torch.no_grad()
def eval_training(loss_function, net, gpu, epoch=0, tb=True):

    start = time.time()
    net.eval()

    test_loss = 0.0 # cost function error
    correct = 0.0

    for (images, labels) in cifar100_test_loader:

        if gpu:
            images = images.cuda()
            labels = labels.cuda()

        outputs = net(images)
        loss = loss_function(outputs, labels)

        test_loss += loss.item()
        _, preds = outputs.max(1)
        correct += preds.eq(labels).sum()

    finish = time.time()
    if gpu:
        print('GPU INFO.....')
        print(torch.cuda.memory_summary(), end='')
    print('Evaluating Network.....')
    print('Test set: Epoch: {}, Average loss: {:.4f}, Accuracy: {:.4f}, Time consumed:{:.2f}s'.format(
        epoch,
        test_loss / len(cifar100_test_loader.dataset),
        correct.float() / len(cifar100_test_loader.dataset),
        finish - start
    ))
    print()

    #add informations to tensorboard
    if tb:
        writer.add_scalar('Test/Average loss', test_loss / len(cifar100_test_loader.dataset), epoch)
        writer.add_scalar('Test/Accuracy', correct.float() / len(cifar100_test_loader.dataset), epoch)

    return correct.float() / len(cifar100_test_loader.dataset)


def auto_pretrain_collective(net_c, data_name, gpu = True, batch_size = 128, warm =1, lr = 0.1, resume = False):


    net = get_network(net_c)

    #data preprocessing:
    if data_name == 'cifar100':
        transform_train = transforms.Compose([
            #transforms.ToPILImage(),
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor(),
            transforms.Normalize(settings.CIFAR100_TRAIN_MEAN, settings.CIFAR100_TRAIN_STD)
        ])
        cifar64_training = datasets.ImageFolder(r'D:\stu_res\reconstruct\YuanMou\learngene\datasets\cifar100-open\base',
                                                transform=transform_train)                
        training_loader = DataLoader(
            cifar64_training, shuffle=True, num_workers=0, batch_size=batch_size)
    elif data_name == 'MiniImageNet':
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
        MiniImageNet64_training = datasets.ImageFolder('/root/data/datasets/MiniImageNet/train',
                                                transform=transform_train)                
        training_loader = DataLoader(
            MiniImageNet64_training, shuffle=True, num_workers=4, batch_size=batch_size)
        

    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=lr, momentum=0.9, weight_decay=5e-4)
    train_scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=settings.MILESTONES, gamma=0.2) #learning rate decay
    iter_per_epoch = len(training_loader)
    warmup_scheduler = WarmUpLR(optimizer, iter_per_epoch * warm)

    if resume:
        recent_folder = most_recent_folder(os.path.join(settings.CHECKPOINT_PATH, net_c), fmt=settings.DATE_FORMAT)
        if not recent_folder:
            raise Exception('no recent folder were found')

        checkpoint_path = os.path.join(settings.CHECKPOINT_PATH, net_c, recent_folder)

    else:
        checkpoint_path = os.path.join(settings.CHECKPOINT_PATH, net_c, settings.TIME_NOW)

    #use tensorboard
    if not os.path.exists(settings.LOG_DIR):
        os.mkdir(settings.LOG_DIR)

    #since tensorboard can't overwrite old values
    #so the only way is to create a new tensorboard log
    #writer = SummaryWriter(log_dir=os.path.join(settings.LOG_DIR, args.net, settings.TIME_NOW))
    input_tensor = torch.Tensor(1, 3, 32, 32)
    
    
    # if args.gpu:
    #     input_tensor = input_tensor.cuda()
    #writer.add_graph(net, input_tensor)

    #create checkpoint folder to save model
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)
    checkpoint_path = os.path.join(checkpoint_path, '{net}-{epoch}-{type}.pth')
    
    

    best_acc = 0.0
    if resume:
        best_weights = best_acc_weights(os.path.join(settings.CHECKPOINT_PATH, net_c, recent_folder))
        if best_weights:
            weights_path = os.path.join(settings.CHECKPOINT_PATH, net_c, recent_folder, best_weights)
            print('found best acc weights file:{}'.format(weights_path))
            print('load best training file to test acc...')
            net.load_state_dict(torch.load(weights_path))
            best_acc = eval_training(loss_function, net, gpu, tb=False)
            print('best acc is {:0.2f}'.format(best_acc))

        recent_weights_file = most_recent_weights(os.path.join(settings.CHECKPOINT_PATH, net_c, recent_folder))
        if not recent_weights_file:
            raise Exception('no recent weights file were found')
        weights_path = os.path.join(settings.CHECKPOINT_PATH, net_c, recent_folder, recent_weights_file)
        print('loading weights file {} to resume training.....'.format(weights_path))
        net.load_state_dict(torch.load(weights_path))

        resume_epoch = last_epoch(os.path.join(settings.CHECKPOINT_PATH, net_c, recent_folder))


    for epoch in range(1, settings.EPOCH + 1):
        if epoch > warm:
            train_scheduler.step(epoch)

        if resume:
            if epoch <= resume_epoch:
                continue

        train(training_loader, optimizer, loss_function, epoch, net_c, net, batch_size, warm, warmup_scheduler)
        acc = eval_training(epoch)

        #start to save best performance model after learning rate decay to 0.01
        if epoch > settings.MILESTONES[1] and best_acc < acc:
            weights_path = checkpoint_path.format(net=net_c, epoch=epoch, type='best')
            print('saving weights file to {}'.format(weights_path))
            torch.save(net.state_dict(), weights_path)
            best_acc = acc

        if not epoch % settings.SAVE_EPOCH:
            weights_path = checkpoint_path.format(net=net_c, epoch=epoch, type='regular')
            print('saving weights file to {}'.format(weights_path))
            torch.save(net.state_dict(), weights_path)

    #writer.close()
freeze_support()
auto_pretrain_collective('vgg16', 'cifar100')