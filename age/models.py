"""
DCGAN code taken from:
https://github.com/sdhnshu/pytorch-model-zoo/blob/master/dcgan/model.py
Because they had a fairly well written, simple version available.
"""
import torch.nn as nn
from torch.nn.functional import leaky_relu, tanh
from torchvision.models import VGG as TorchVGG

from utility import seed_all


batch_norm = False


def transpose_convolution(c_in, c_out, k_size, stride=2, pad=1, bn=batch_norm):
    layers = [nn.ConvTranspose2d(c_in, c_out, k_size, stride, pad)]
    if bn:
        layers.append(nn.BatchNorm2d(c_out))
    return nn.Sequential(*layers)


def convolution(c_in, c_out, k_size, stride=2, pad=1, bn=batch_norm):
    layers = [nn.Conv2d(c_in, c_out, k_size, stride, pad)]
    if bn:
        layers.append(nn.BatchNorm2d(c_out))
    return nn.Sequential(*layers)


class Generator(nn.Module):
    def __init__(self, z_dim=256, image_size=128, conv_dim=64):
        seed_all(0)
        super().__init__()
        self.fc = transpose_convolution(z_dim, conv_dim * 8, int(image_size / 16), 1, 0, bn=False)
        self.layer1 = transpose_convolution(conv_dim * 8, conv_dim * 4, 4)
        self.layer2 = transpose_convolution(conv_dim * 4, conv_dim * 2, 4)
        self.layer3 = transpose_convolution(conv_dim * 2, conv_dim, 4)
        self.layer4 = transpose_convolution(conv_dim, 3, 4, bn=False)
        self.input_size = z_dim

    def forward(self, z):
        z = z.view(z.size(0), z.size(1), 1, 1)
        out = self.fc(z)                            # (?, 512, 4, 4)
        out = leaky_relu(self.layer1(out), 0.05)    # (?, 256, 8, 8)
        out = leaky_relu(self.layer2(out), 0.05)    # (?, 128, 16, 16)
        out = leaky_relu(self.layer3(out), 0.05)    # (?, 64, 32, 32)
        out = tanh(self.layer4(out))                # (?, 3, 64, 64)
        return out


class Discriminator(nn.Module):
    def __init__(self, image_size=128, conv_dim=64):
        seed_all(0)
        super().__init__()
        self.layer1 = convolution(3, conv_dim, 4, bn=False)
        self.layer2 = convolution(conv_dim, conv_dim * 2, 4)
        self.layer3 = convolution(conv_dim * 2, conv_dim * 4, 4)
        self.layer4 = convolution(conv_dim * 4, conv_dim * 8, 4)
        self.layer5 = convolution(conv_dim * 8, 1, int(image_size / 16), 1, 0, False)
        self.feature_layer = None

    def forward(self, x):
        out = leaky_relu(self.layer1(x), 0.05)    # (?, 64, 32, 32)
        out = leaky_relu(self.layer2(out), 0.05)  # (?, 128, 16, 16)
        out = leaky_relu(self.layer3(out), 0.05)  # (?, 256, 8, 8)
        out = leaky_relu(self.layer4(out), 0.05)  # (?, 512, 4, 4)
        self.feature_layer = out.view(out.size(0), -1)
        out = self.layer5(out).view(-1)
        return out