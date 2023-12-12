import torch

def auto_extract(model, arch):
    if model == 'vgg':
        from utils.models.vgg_cifar import vgg16_bn_cifar64
        collective_model = vgg16_bn_cifar64()
        collective_model.load_state_dict(
            torch.load('./checkpoint/vgg16/Monday_06_November_2023_16h_34m_05s/vgg16-2-best.pth'))

        layer_1 = collective_model.get_layers_64()
        layer_2 = collective_model.get_layers_128()
        layer_3 = collective_model.get_layers_256()
        layer_4 = collective_model.get_layers_512_1()

        return layer_1, layer_2, layer_3, layer_4

    elif model == 'resnet':
        from utils.models.resnet_ilsvrc import resnet18
        from utils.models.res12 import resnet12
        collective_model = resnet18(num_classes=64)
        # collective_model.load_state_dict(torch.load('./checkpoint/resnet18/Wednesday_06_April_2022_00h_40m_16s/resnet18-120-regular.pth'))
        collective_model.load_state_dict(
            torch.load('./checkpoint/resnet18/Monday_29_August_2022_15h_16m_37s/resnet18-180-regular.pth'))

        layer_1 = collective_model.get_layers_64()
        layer_2 = []
        layer_3 = []  # collective_model.get_layers_256()
        layer_4 = collective_model.get_layers_512()
        return layer_1, layer_2, layer_3, layer_4

    elif model == 'swin':
        from utils.models.model_transformer import swin_tiny_patch4_window7_224, swin_small_patch4_window7_224, \
            SwinTransformer_with_learngene
        collective_model = swin_small_patch4_window7_224(num_classes=64)
        collective_model.load_state_dict(
            torch.load('./checkpoint/swin-s/Sunday_28_August_2022_14h_36m_41s/swin-s-180-regular.pth'))

        # print(collective_model)
        # exit()

        layers_0 = []
        layers_2 = collective_model.get_layers_num_2_last6blocks()
        layers_3 = collective_model.get_layers_num_3()

        return layers_0, layers_2, layers_3

    elif model == 'vit-dino':
        from utils.models import get_model
        from utils.models.vision_transformer import vitsmall_with_learngene
        collective_model = get_model(arch=arch)
        patch_embed = collective_model.patch_embed
        cls_token = collective_model.cls_token
        pos_embed = collective_model.pos_embed
        pos_drop = collective_model.pos_drop
        # print(cls_token)
        # print(pos_embed)


        layers_0 = collective_model.get_layers_num_0()
        layers_2 = collective_model.get_layers_num_2()

    return layers_0, layers_2