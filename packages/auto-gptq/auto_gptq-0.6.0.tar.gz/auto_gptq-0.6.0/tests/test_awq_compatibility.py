import torch
import torch.nn as nn
from auto_gptq.utils.import_utils import dynamically_import_QuantLinear
import copy
import unittest
from awq.quantize.qmodule import WQLinear, calculate_zeros_width

def awq_from_linear(linear, w_bit, group_size, scales=None, zeros=None):
    awq_linear = WQLinear(w_bit, group_size, linear.in_features, linear.out_features, linear.bias is not None, linear.weight.device)
    
    # need scales and zeros info for real quantization
    assert scales is not None and zeros is not None  
    scale_zeros = zeros * scales

    pack_num = 32 // awq_linear.w_bit
    print("from_linear scales", scales.shape)
    assert linear.in_features % group_size == 0

    # awq_linear.scales = scales.clone().half()
    awq_linear.scales = scales
    if linear.bias is not None:
        awq_linear.bias = linear.bias.clone().half()
    
    intweight = []
    for idx in range(awq_linear.in_features):
        intweight.append(torch.round((linear.weight.data[:, idx] + scale_zeros[:, idx // group_size]) / awq_linear.scales[:, idx // group_size]).to(torch.int)[:, None])
    intweight = torch.cat(intweight, dim=1)
    # intweight = intweight.t().contiguous()
    intweight = intweight.to(dtype=torch.int32)
    qweight = torch.zeros((intweight.shape[0], intweight.shape[1] // 32 * awq_linear.w_bit), dtype=torch.int32, device=intweight.device)           
        
    for col in range(intweight.shape[1] // pack_num):
        if awq_linear.w_bit == 4:
            # order_map = [0, 2, 4, 6, 1, 3, 5, 7]
            order_map = [0, 1, 2, 3, 4, 5, 6, 7]
        else:
            raise NotImplementedError("Only 4-bit are supported for now.")
        for i in range(pack_num):
            qweight_col = intweight[:, col * pack_num + order_map[i]]
            qweight[:, col] |= qweight_col << (i * awq_linear.w_bit)
    awq_linear.qweight = qweight

    print("zeros here", zeros.shape)
    zeros = zeros.to(dtype=torch.int32)
    qzeros = torch.zeros(
        (zeros.shape[0], calculate_zeros_width(linear.in_features, group_size)),
        dtype=torch.int32,
        device=zeros.device,
    )

    print("qzeros", qzeros.shape)
    
    for col in range((zeros.shape[1] + pack_num - 1) // pack_num):
        if awq_linear.w_bit == 4:
            # order_map = [0, 2, 4, 6, 1, 3, 5, 7]
            order_map = [0, 1, 2, 3, 4, 5, 6, 7]
        else:
            raise NotImplementedError("Only 4-bit are supported for now.")
        for i in range(pack_num):
            if col * pack_num + order_map[i] >= zeros.shape[1]:
                continue
            qzero_col = zeros[:, col * pack_num + order_map[i]]
            qzeros[:, col] |= qzero_col << (i * awq_linear.w_bit)
    awq_linear.qzeros = qzeros
    return awq_linear


class TestAwqCompatibility(unittest.TestCase):
    def test_unpack(self):

        group_size = 128
        bits = 4

        m = 1
        k = 11008
        n = 4096
        device = torch.device("cuda:0")

        linear_class = dynamically_import_QuantLinear(use_triton=False, desc_act=False, group_size=group_size, bits=bits, disable_exllama=True, disable_exllamav2=True)

        gptq_linear = linear_class(
            bits=bits,
            group_size=group_size,
            infeatures=k,
            outfeatures=n,
            bias=False,
        )

        gptq_linear.qweight = torch.randint(-2**30, 2**30, size=gptq_linear.qweight.shape, dtype=torch.int32)
        gptq_linear.scales = gptq_linear.scales + 0.002

        gptq_linear = gptq_linear.eval()
        gptq_linear = gptq_linear.to(device)

        m = 1
        inp = torch.rand(1, m, k, dtype=torch.float16).to(device)

        with torch.no_grad():
            res_gptq = gptq_linear(inp)

        unpacked_weight, unpacked_zeros = gptq_linear.unpack()
        unpacked_zeros = unpacked_zeros.to("cpu")

        unpacked_linear = nn.Linear(k, n, bias=False)
        self.assertTrue(unpacked_linear.weight.shape == unpacked_weight.t().shape)

        # AWQ respects the order (out_features, in_features), contrarily to all the other GPTQ implementations, hence the following transposes for weight, scale, qzeros.
        unpacked_linear.weight = torch.nn.Parameter(unpacked_weight.t().contiguous())

        unpacked_linear = unpacked_linear.to("cpu")
        gptq_linear = gptq_linear.to("cpu")

        gptq_linear_new = linear_class(
            bits=bits,
            group_size=group_size,
            infeatures=k,
            outfeatures=n,
            bias=False,
        )

        # pack is transposing back the scales and qzeros, giving (in_feature, out_features)
        gptq_linear_new.pack(unpacked_linear, gptq_linear.scales.t(), unpacked_zeros.t(), g_idx=None)

        self.assertTrue(torch.equal(gptq_linear.qweight, gptq_linear_new.qweight))
        self.assertTrue(torch.equal(gptq_linear.scales, gptq_linear_new.scales))
        self.assertTrue(torch.equal(gptq_linear.qzeros, gptq_linear_new.qzeros))



    """
    # from_linear is NOT transposing back the scales and qzeros, giving (out_features, in_feature)
    #awq_linear = awq_from_linear(unpacked_linear, w_bit=bits, group_size=group_size, scales=gptq_linear.scales.t().contiguous(), zeros=unpacked_zeros.t().contiguous())

    awq_linear = WQLinear.from_linear_gptq(unpacked_linear.weight.to("cpu"), w_bit=4, group_size=128, scales=gptq_linear.scales.to("cpu"), zeros=unpacked_zeros.to("cpu"))

    gptq_linear = gptq_linear.to(device)
    awq_linear = awq_linear.to(device)

    print("gptq_linear qweight", gptq_linear.qweight.shape)
    print("gptq_linear scales", gptq_linear.scales.shape)
    print("gptq_linear qzeros", gptq_linear.qzeros.shape)
    print("awq_linear qweight", awq_linear.qweight.shape)
    print("awq_linear scales", awq_linear.scales.shape)
    print("awq_linear qzeros", awq_linear.qzeros.shape)

    #for m in [1, 3, 15]:
    with torch.no_grad():
        res_awq = awq_linear(inp)

    self.assertTrue(res_awq.shape == res_gptq.shape)
    torch.set_printoptions(threshold=10000)

    #print("res_awq - res_gptq", res_awq - res_gptq)
    relative_diff = (res_awq - res_gptq).abs() / (res_gptq.abs() + 1e-15)
    print("relative_diff", relative_diff)
    self.assertTrue(torch.all(relative_diff < 1e-2))
    """