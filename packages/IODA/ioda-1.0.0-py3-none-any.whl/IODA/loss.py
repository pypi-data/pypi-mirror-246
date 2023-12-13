import torch


class DICELoss(torch.nn.Module):
    def __init__(self):
        super(DICELoss, self).__init__()

    def forward(self, input, target):
        smooth = 1.0

        y_onehot = torch.FloatTensor(input.shape[0], input.shape[1]).to(
            input.get_device()
        )
        y_onehot.zero_()
        y_onehot.scatter_(1, target.view(-1, 1), 1)

        iflat = torch.nn.functional.softmax(input, None, _stacklevel=5).view(-1)
        tflat = y_onehot.view(-1)
        intersection = (iflat * tflat).sum()

        return 1 - (
            (2.0 * intersection + smooth) / (iflat.sum() + tflat.sum() + smooth)
        )


class FocalLoss(torch.nn.CrossEntropyLoss):
    """Focal loss for classification tasks on imbalanced datasets

    Arguments:
        alpha (float): Weighting factor :math:`\alpha \in [0, 1]`.
        gamma (float): Focusing parameter :math:`\gamma >= 0`.
        reduction (Optional[str]): Specifies the reduction to apply to the
         output: ‘none’ | ‘mean’ | ‘sum’. ‘none’: no reduction will be applied,
         ‘mean’: the sum of the output will be divided by the number of elements
         in the output, ‘sum’: the output will be summed. Default: ‘none’."""

    def __init__(self, alphas=None, gamma=2.0, reduction="none"):
        super().__init__(weight=alphas, ignore_index=-1, reduction="none")
        self.reduction = reduction
        self.gamma = gamma

    def forward(self, input_, target):
        cross_entropy = super().forward(input_, target)
        # Temporarily mask out ignore index to '0' for valid gather-indices input.
        # This won't contribute final loss as the cross_entropy contribution
        # for these would be zero.
        target = target * (target != self.ignore_index).long()
        input_prob = torch.gather(
            torch.nn.functional.softmax(input_, 1), 1, target.unsqueeze(1)
        )
        loss = torch.pow(1 - input_prob, self.gamma) * cross_entropy
        return (
            torch.mean(loss)
            if self.reduction == "mean"
            else torch.sum(loss)
            if self.reduction == "sum"
            else loss
        )
