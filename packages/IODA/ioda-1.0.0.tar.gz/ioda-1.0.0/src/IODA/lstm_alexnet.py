from typing import Optional, Tuple

import torch
import torch.nn as nn
import torchvision

from IODA.loss import FocalLoss


class FeatureAlexNet(nn.Module):
    def __init__(self, num_classes=4096, transfer_learning: bool = True):
        super(FeatureAlexNet, self).__init__()
        self.alexnet = torchvision.models.alexnet(
            weights=torchvision.models.AlexNet_Weights.IMAGENET1K_V1
        )
        self.sig = nn.Sigmoid()
        if transfer_learning:
            for param in self.alexnet.parameters():
                param.requires_grad = False
        self.alexnet.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(self.alexnet.classifier[1].in_features, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.alexnet.features(x)
        x = x.view(x.size(0), -1)
        x = self.alexnet.classifier(x)

        return self.sig(x)


class LSTMAlexNet(nn.Module):
    def __init__(self, num_classes, lstm_size=512, transfer_learning: bool = True):
        super(LSTMAlexNet, self).__init__()
        self.featureNet = FeatureAlexNet(
            num_classes=4096, transfer_learning=transfer_learning
        )

        self.lstm_size = lstm_size
        self.lstm = nn.LSTM(4096, self.lstm_size, batch_first=True)
        self.classifier = nn.Linear(lstm_size, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Stateless LSTM
        x = self.featureNet.forward(x)
        x = x.view(1, x.size(0), -1)
        x, _ = self.lstm(x)
        x = x.view(x.size(1), -1)
        x = self.classifier(x)

        return x


def initialize(
    batch_size: int,
    num_classes: int,
    weights: Optional[torch.Tensor] = None,
    transfer_learning: bool = True,
) -> Tuple[torch.nn.Module, torch.optim.Optimizer, torch.nn.Module, Tuple[int, int]]:
    """
    Returns an instance of an LSTMAlexNet with optimizer, loss function
    and expected image size.
    """
    model = LSTMAlexNet(
        num_classes=num_classes,
        lstm_size=batch_size,
        transfer_learning=transfer_learning,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.5e-4)
    loss_fn = FocalLoss(alphas=weights, gamma=2.0, reduction="mean")

    IMAGE_SIZE = (224, 224)

    return model, optimizer, loss_fn, IMAGE_SIZE
