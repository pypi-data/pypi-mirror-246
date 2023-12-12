'''
Modified from https://github.com/pytorch/vision/blob/master/torchvision/models/vgg.py
'''
import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F
import math


__all__ = [
    'VGG', 'vgg11', 'vgg11_bn', 'vgg13', 'vgg13_bn', 'vgg16', 'vgg16_bn',
    'vgg19_bn', 'vgg19', 'vgg9_bn'
]


## For models pre-trained on ImageNet
model_urls = {
    'vgg11': 'https://download.pytorch.org/models/vgg11-bbd30ac9.pth',
    'vgg13': 'https://download.pytorch.org/models/vgg13-c768596a.pth',
    'vgg16': 'https://download.pytorch.org/models/vgg16-397923af.pth',
    'vgg19': 'https://download.pytorch.org/models/vgg19-dcbb9e9d.pth',
    'vgg11_bn': 'https://download.pytorch.org/models/vgg11_bn-6002323d.pth',
    'vgg13_bn': 'https://download.pytorch.org/models/vgg13_bn-abd245e5.pth',
    'vgg16_bn': 'https://download.pytorch.org/models/vgg16_bn-6c64b313.pth',
    'vgg19_bn': 'https://download.pytorch.org/models/vgg19_bn-c79401a0.pth',
}


class VGG(nn.Module):

    def __init__(self, features, num_classes=1000, init_weights=True, dropout: float = 0.5):
        super(VGG, self).__init__()
        self.features = features
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(p=dropout),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(p=dropout),
            nn.Linear(4096, num_classes),
        )
        if init_weights:
            for m in self.modules():
                if isinstance(m, nn.Conv2d):
                    nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
                    if m.bias is not None:
                        nn.init.constant_(m.bias, 0)
                elif isinstance(m, nn.BatchNorm2d):
                    nn.init.constant_(m.weight, 1)
                    nn.init.constant_(m.bias, 0)
                elif isinstance(m, nn.Linear):
                    nn.init.normal_(m.weight, 0, 0.01)
                    nn.init.constant_(m.bias, 0)

    def forward(self, x):  # The feat of VGG divides according to the Maxpooling position
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            #print(x.shape)
            x = layer(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x, feat
    
    def forward_with_features(self, x):
        return self.forward(x)
    '''
    def get_layers_64(self):  # For Vgg9  # layer_0
        return self.features[3:7] # including maxpooling
    
    def get_layers_128(self): # layer_1 
        return self.features[10:14] 
    
    def get_layers_256(self):  # layer_2 
        return self.features[20:24] 
    
    def get_layers_512_0(self):  # layer_3: from Conv2d(256,512) to Conv2d(512,512)
        return self.features[24:30] 
        
    def get_layers_512_1(self):  # layer_4: from Two Conv2d(512,512) to MaxPool
        return self.features[37:44] '''
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

        
# The customized model from https://arxiv.org/abs/1803.00443
class VGG_small(nn.Module):

    def __init__(self, features, num_classes=1000, init_weights=True, lwf=False, num_source_cls=200, no_ft=False):
        super(VGG_small, self).__init__()
        self.features = features

        self.num_classes = num_classes
        if isinstance(num_classes, list):
            fcs = []
            for i in range(len(num_classes)):
                fcs.append(nn.Linear(512, num_classes[i]))
            self.classifier = nn.ModuleList(fcs)
        else:
            self.classifier = nn.Linear(512, num_classes)

        #self.classifier = nn.Linear(512, num_classes)
        self.lwf = lwf
        if self.lwf:
            self.lwf_lyr = nn.Linear(512, num_source_cls)

        self.no_ft = no_ft
        if self.no_ft:
            self.outputs_branch = nn.ModuleList(
                                    [nn.Linear(64, num_classes),
                                    nn.Linear(128, num_classes),
                                    nn.Linear(256, num_classes)])

        self.alphas = nn.ParameterList([nn.Parameter(torch.rand(3, 1, 1, 1)*0.1),
                nn.Parameter(torch.rand(3, 1, 1, 1)*0.1),
                nn.Parameter(torch.rand(3, 1, 1, 1)*0.1)])

        self.new_classifier = nn.Linear(512, num_classes)
        self.new_bn = nn.ModuleList()
        for layer in self.features:
            if isinstance(layer, nn.BatchNorm2d):
                self.new_bn.append(nn.BatchNorm2d(layer.num_features))

        self.w1 = nn.Linear(64, 16)
        self.w2 = nn.Linear(128, 32)
        self.w3 = nn.Linear(256, 64)
        self.w = nn.ModuleList([self.w1, self.w2, self.w3])
        if init_weights:
            self._initialize_weights()

    def forward(self, x, idx=-1):
        feat = []
        for layer in self.features:
            if isinstance(layer, nn.MaxPool2d):
                feat.append(x)
            x = layer(x)
        x = F.avg_pool2d(x, x.size(3))
        x = x.view(x.size(0), -1)

        if self.lwf:
            old_out = self.lwf_lyr(x)

        if isinstance(self.num_classes, list):
            x = self.classifier[idx](x)
        else:
            x = self.classifier(x)

        
        if self.lwf:
            return x, feat, old_out
        else:
            return x, feat

    def forward_with_features(self, x):
        return self.forward(x)

    def forward_with_combine_features(self, x, fs, metanet):
        return self.combine_forward(x, fs, metanet, 0)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


def make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


cfg = {
    'A': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'B': [64, 64, 'M', 128, 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
    'D': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M'],
    'E': [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M'],
}

cfg_small = {
    'A': [64, 'M', 128, 'M', 512, 'M'],
    'B': [64, 'M', 128, 'M', 256, 256, 'M', 512, 512, 'M', 512, 512, 'M'],
}


def vgg4(**kwargs):
    """
    VGG 4-layer model (configuration_small "A")
    """
    model = VGG_small(make_layers(cfg_small['A']), **kwargs)
    return model


def vgg4_bn(**kwargs):
    """
    VGG 4-layer model (configuration_small "A") with batch normalization
    """
    model = VGG_small(make_layers(cfg_small['A'], batch_norm=True), **kwargs)
    return model


def vgg9(**kwargs):
    """
    VGG 9-layer model (configuration_small "B")
    """
    model = VGG_small(make_layers(cfg_small['B']), **kwargs)
    return model


def vgg9_bn(**kwargs):
    """
    VGG 9-layer model (configuration_small "B") with batch normalization
    """
    model = VGG_small(make_layers(cfg_small['B'], batch_norm=True), **kwargs)
    return model



def vgg11(**kwargs):
    """
    VGG 11-layer model (configuration "A")
    """
    model = VGG(make_layers(cfg['A']), **kwargs)
    return model


def vgg11_bn(**kwargs):
    """
    VGG 11-layer model (configuration "A") with batch normalization
    """
    model = VGG(make_layers(cfg['A'], batch_norm=True), **kwargs)
    return model


def vgg13(**kwargs):
    """
    VGG 13-layer model (configuration "B")
    """
    model = VGG(make_layers(cfg['B']), **kwargs)
    return model


def vgg13_bn(**kwargs):
    """
    VGG 13-layer model (configuration "B") with batch normalization
    """
    model = VGG(make_layers(cfg['B'], batch_norm=True), **kwargs)
    return model


def vgg16(**kwargs):
    """
    VGG 16-layer model (configuration "D")
    """
    model = VGG(make_layers(cfg['D']), **kwargs)
    return model


def vgg16_bn(pretrained=False, **kwargs):
    """
    VGG 16-layer model (configuration "D") with batch normalization
    Args:
        pretrained (bool): If True, returns a model pre-trained on ImageNet
    """
    model = VGG(make_layers(cfg['D'], batch_norm=True), **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['vgg16_bn']))
    return model


def vgg19(**kwargs):
    """
    VGG 19-layer model (configuration "E")
    """
    model = VGG(make_layers(cfg['E']), **kwargs)
    return model


def vgg19_bn(**kwargs):
    """
    VGG 19-layer model (configuration 'E') with batch normalization
    """
    model = VGG(make_layers(cfg['E'], batch_norm=True), **kwargs)
    return model

cfg_target = {
    'A' : [64, 'M', 128, 'M', 256],
    'B' : [512, 512, 'M'],
    'C': [256, 'M', 512, 512, 'M'],
    'D': [64, 'M', 128, 'M', 256, 256, 'M']
}

# lightweight individual model
class vgg_compression_meta_learngene(nn.Module):
    
    def __init__(self, layer_2, layer_4, num_classes=100):
        
        super().__init__()
        
        self.features = make_layers_compression(cfg_target['A'], batch_norm=True)
        
        if len(layer_2) == 0:
            layer_3 = make_layers_compression(cfg_target['C'], batch_norm=True, input_channel = 256)
            for layer in layer_3:
                self.features.append(layer)
            
        else:
            for layer in layer_2:
                self.features.append(layer)

            layer_3 = make_layers_compression(cfg_target['B'], batch_norm=True, input_channel = 256)

            for layer in layer_3:
                self.features.append(layer)
        
        if len(layer_4) == 0:
            layer_4 = make_layers_compression(cfg_target['B'], batch_norm=True, input_channel = 512)
            for layer in layer_4:
                self.features.append(layer)
        else:    
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


if __name__ == "__main__":
    pass
#    x = torch.Tensor(5,3,32,32)
#    net = vgg4_bn()
#    y, feat = net(x)
#    
#    print (y.size())
#    print()
#    for i in range(len(feat)):
#        print (feat[i].size())


