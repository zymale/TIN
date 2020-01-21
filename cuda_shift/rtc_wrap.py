# Code for "Temporal Interlacing Network"
# Hao Shao, Shengju Qian, Yu Liu
# shaoh19@mails.tsinghua.edu.cn, sjqian@cse.cuhk.edu.hk, yuliu@ee.cuhk.edu.hk

import torch
from torch.autograd import Function

from _ext import rtc as _backend

class ShiftFeatureFunc(Function):
    def __init__(self):
        super(ShiftFeatureFunc, self).__init__()

    def forward(self, data, shift):
        if not data.is_cuda or not shift.is_cuda:
            raise NotImplementedError

        if data.requires_grad:
            self.save_for_backward(shift)

        out = torch.zeros_like(data)
        _backend.shift_featuremap_cuda_forward(data, shift, out)
        return out

    def backward(self, grad_output):
        if not grad_output.is_cuda:
            raise NotImplementedError
        shift = self.saved_tensors[0]
        data_grad_input = grad_output.new(*grad_output.size()).zero_()
        shift_grad_input = shift.new(*shift.size()).zero_()
        _backend.shift_featuremap_cuda_backward(grad_output, shift, data_grad_input)
        return data_grad_input, shift_grad_input
