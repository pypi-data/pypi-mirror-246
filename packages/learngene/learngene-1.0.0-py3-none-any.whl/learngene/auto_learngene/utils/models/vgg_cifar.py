"""vgg in pytorch
[1] Karen Simonyan, Andrew Zisserman
    Very Deep Convolutional Networks for Large-Scale Image Recognition.
    https://arxiv.org/abs/1409.1556v6
"""
'''VGG11/13/16/19 in Pytorch.'''

import torch
import torch.nn as nn

cfg = {
    'A' : [64,     'M', 128,      'M', 256, 256,           'M', 512, 512,           'M', 512, 512,           'M'],
    'B' : [64, 64, 'M', 128, 128, 'M', 256, 256,           'M', 512, 512,           'M', 512, 512,           'M'],
    'D' : [64, 64, 'M', 128, 128, 'M', 256, 256, 256,      'M', 512, 512, 512,      'M', 512, 512, 512,      'M'],
    'E' : [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M']
}

class VGG(nn.Module):

    def __init__(self, features, num_classes=100):
        super().__init__()
        self.features = features

        self.classifier = nn.Sequential(
            nn.Linear(512, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, num_classes)
        )

    def forward(self, x):
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            #print(x.shape)
            x = layer(x)
        x = x.view(x.size()[0], -1)
        x = self.classifier(x)
        return x, feat 

    def extract_feature_cnn(self, x):
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            x = layer(x)
        #x = x.view(x.size()[0], -1)
        #x = self.classifier(x)
        return  [feat[-2]], x  #return last second 
        #return  feat, x

    def extract_feature(self, x):
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            x = layer(x)
        return  feat, x  
    
    def forward_with_features(self, x):
        return self.forward(x)
    
    def get_layers_64(self):  # For Vgg9  # layer_0
        return self.features[0:3] # including maxpooling
    
    def get_layers_128(self): # layer_1 
        return self.features[7:10] 
    
    def get_layers_256(self):  # layer_2 
        return self.features[14:20] 
    
    def get_layers_512_0(self):  # layer_3: from Conv2d(256,512) to Conv2d(512,512)
        return self.features[24:30] 
        
    def get_layers_512_1(self):  # layer_4: from Two Conv2d(512,512) to MaxPool
        return self.features[37:44] 
    
    def get_layers_512_3(self):  
        return self.features[37:40] 
    
    def get_layers_512_4(self):  
        return self.features[40:43] 

def make_layers(cfg, batch_norm=False):
    layers = []

    input_channel = 3
    for l in cfg:
        if l == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            continue

        layers += [nn.Conv2d(input_channel, l, kernel_size=3, padding=1)]

        if batch_norm:
            layers += [nn.BatchNorm2d(l)]

        layers += [nn.ReLU(inplace=True)]
        input_channel = l

    return nn.Sequential(*layers)


def vgg11_bn():
    return VGG(make_layers(cfg['A'], batch_norm=True))

def vgg13_bn():
    return VGG(make_layers(cfg['B'], batch_norm=True))

def vgg16_bn():
    return VGG(make_layers(cfg['D'], batch_norm=True))

def vgg19_bn():
    return VGG(make_layers(cfg['E'], batch_norm=True))

def vgg16_bn_cifar64():
    """
    VGG 16-layer model (configuration "D") with batch normalization   
    """
    return VGG(make_layers(cfg['D'], batch_norm=True), num_classes=64)

def vgg16_bn_cifar64_with_num_classes(num_class=64):
    """
    VGG 16-layer model (configuration "D") with batch normalization   
    """
    return VGG(make_layers(cfg['D'], batch_norm=True), num_classes=num_class)

cfg_target = {
    'Z' : [],
    'A' : [64, 'M', 128, 'M', 256],
    'B' : [512, 512, 'M'],
    'C': [256, 'M', 512, 512, 'M'],
    'D': [64, 'M', 128, 'M', 256, 256, 'M'],
    'E': [512, 512, 'M'],
    'F': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M']
}

# lightweight individual model
class vgg_compression_meta_learngene(nn.Module):
    
    def __init__(self, layer_1, layer_2, layer_3, layer_4, num_classes=100):
        
        super().__init__()
    
        #[64, 'M', 128, 'M', 256, 'M', 512, 512, 'M', 512, 512, 'M']
        self.features = make_layers_compression(cfg_target['Z'], batch_norm=True)
        for layer in layer_1:
            self.features.append(layer)
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))
        for layer in layer_2:
            self.features.append(layer)
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))
        for layer in layer_3:
            self.features.append(layer)
        self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))
        layer_512 = make_layers_compression(cfg_target['E'], batch_norm=True, input_channel = 256)
        for layer in layer_512:
            self.features.append(layer)
        for layer in layer_4:
            self.features.append(layer)

        self.classifier = nn.ModuleList([
            nn.Linear(512, 1024),
            nn.ReLU(True),
            nn.Linear(1024, 1024),
            nn.ReLU(True),
            nn.Linear(1024, num_classes),
        ])

        
    def forward(self, x):
        for layer in self.features:
            x = layer(x) 
        x = x.view(x.size()[0], -1)
        for layer in self.classifier:
            x = layer(x)
        return x

    def forward_output_features(self, x):
        for layer in self.features:
            x = layer(x) 
        x = x.view(x.size()[0], -1)
        return x 

    def extract_feature_cnn(self, x):
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            x = layer(x)
        #x = x.view(x.size()[0], -1)
        #for layer in self.classifier:
        #    x = layer(x)
        return  [feat[-2]], x #return last second
        #return  feat, x

    def extract_feature(self, x):
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            x = layer(x)
        x = x.view(x.size()[0], -1)
        for layer in self.classifier:
            x = layer(x)
        return  feat, x  

class vgg_compression_cross_learngene(nn.Module):
    
    def __init__(self, layer_1, layer_2, layer_3, layer_4, num_classes=100, method='meta-learngene', fc_inputs=512):
        
        super().__init__()
    
        if method == 'meta-learngene':
            self.features = make_layers_compression(cfg_target['Z'], batch_norm=True)
            for layer in layer_1:
                self.features.append(layer)
            self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))
            for layer in layer_2:
                self.features.append(layer)
            self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))
            for layer in layer_3:
                self.features.append(layer)
            self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))    
            layer_512 = make_layers_compression(cfg_target['E'], batch_norm=True, input_channel = 256)
            for layer in layer_512:
                self.features.append(layer)
            for layer in layer_4:
                self.features.append(layer)
        elif method == 'orig-learngene':
            self.features = make_layers_compression(cfg_target['D'], batch_norm=True)
            for layer in layer_3:
                self.features.append(layer)
            self.features.append(nn.MaxPool2d(kernel_size=2, stride=2))
            for layer in layer_4:
                self.features.append(layer)  
        else:
            self.features = make_layers_compression(cfg_target['F'], batch_norm=True)

        self.classifier = nn.ModuleList([
            nn.Linear(fc_inputs, 1024),
            nn.ReLU(True),
            nn.Linear(1024, 1024),
            nn.ReLU(True),
            nn.Linear(1024, num_classes),
        ])

        
    def forward(self, x):
        for layer in self.features:
            x = layer(x) 
        x = x.view(x.size()[0], -1)
        for layer in self.classifier:
            x = layer(x)
        return x    
    

def make_layers_compression(cfg, batch_norm, input_channel = 3):

    layers = nn.ModuleList([])
    
    for l in cfg:
        
        if l == 'M':
            layers.append(nn.MaxPool2d(kernel_size=2, stride=2))
            continue
        
        layers.append(nn.Conv2d(input_channel, l, kernel_size=3, padding=1))
        if batch_norm:
            layers.append(nn.BatchNorm2d(l))
        layers.append(nn.ReLU(inplace=True))
        
        input_channel = l

    return layers 