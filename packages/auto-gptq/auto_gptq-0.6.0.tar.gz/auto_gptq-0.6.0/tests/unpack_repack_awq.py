import os
import copy

def reverse_reorder_int_tensor(int_tensor, pack_mode: str, bits: int):
    if pack_mode != "GEMM":
        return int_tensor
    else:
        int_tensor = int_tensor.T.contiguous()
        compress_ratio = (32 // bits)
        assert int_tensor.shape[-1] % compress_ratio == 0
        if bits == 4:
            order_map = [0, 2, 4, 6, 1, 3, 5, 7]
        else:
            raise NotImplementedError("Only 4-bit are supported for now.")
        order_tensor = torch.tensor(
            order_map, dtype=torch.int32, device=int_tensor.device).reshape(1, -1)
        order_tensor = order_tensor.repeat(
            int_tensor.shape[1]//compress_ratio, 1)
        order_tensor = order_tensor + torch.arange(0, int_tensor.shape[1],
                                                    compress_ratio, dtype=torch.int32, device=int_tensor.device).reshape(-1, 1)
        order_tensor = order_tensor.reshape(-1)

        reverse_order_tensor = torch.arange(order_tensor.shape[0]).cuda()[order_tensor]
        reverse_order_tensor = reverse_order_tensor[order_tensor]
        int_tensor = int_tensor[:, reverse_order_tensor]
        return int_tensor

def dequant_weight(intweight, zeros, scales, g_idx):
    scales = scales.cuda()
    zeros = zeros.t().contiguous()
    scale_zeros = zeros * scales
    g_idx = g_idx.long().cuda()

    scale_mat = scales[g_idx]
    scale_zeros_mat = scale_zeros[g_idx].half()
    qdq_weight_T = intweight.T*scale_mat-scale_zeros_mat.half()

    return qdq_weight_T.T.cpu()


def unpack(qlinear, pack_mode: str):
    print("qlinear.qzeros device", qlinear.qzeros.device)
    qzeros = qlinear.qzeros.cuda()
    qweight = qlinear.qweight.cuda()
    bits = qlinear.w_bit

    if "GEMM" in pack_mode:
        qweight = qweight.T.contiguous()

    load_from_autogptq = int(os.environ.get('load_from_autogptq', "0"))
    load_from_autogptq = 1

    if bits in [2, 4, 8]:
        wf = torch.tensor(list(range(0, 32, bits)), dtype=torch.int32, device=qzeros.device).unsqueeze(0)
        zeros = torch.bitwise_right_shift(torch.unsqueeze(qzeros, 2), wf.unsqueeze(0)).to(
            torch.int16 if bits == 8 else torch.int8)
        torch.bitwise_and(zeros, (2 ** bits) - 1, out=zeros)

        zeros = zeros + load_from_autogptq
        zeros = zeros.reshape(-1, 1, zeros.shape[1] * zeros.shape[2])

        weight = torch.bitwise_right_shift(torch.unsqueeze(
            qweight, 1), wf.unsqueeze(-1)).to(torch.int16 if bits == 8 else torch.int8)
        torch.bitwise_and(weight, (2 ** bits) - 1, out=weight)
        weight = weight.reshape(-1, qlinear.group_size, weight.shape[2])

        weight = weight.view(-1, weight.shape[-1])
        zeros = zeros.view(-1, zeros.shape[-1])
    else:
        weight = torch.zeros((qlinear.in_features, qweight.shape[1]), dtype=torch.int8, device=qweight.device)
        general_unpack_on_row(qweight, weight, bits)
        zeros = torch.zeros((qlinear.in_features//qlinear.group_size,
                            qweight.shape[1]), dtype=torch.int8, device=qweight.device)
        zeros = zeros.T
        general_unpack_on_row(qzeros.T, zeros, bits)
        zeros = zeros.T
        zeros = zeros + load_from_autogptq

    if "GEMM" in pack_mode:
        zeros = zeros.T.contiguous()
    zeros = reverse_reorder_int_tensor(zeros, pack_mode="GEMM", bits=bits)
    weight = reverse_reorder_int_tensor(weight, pack_mode="GEMM", bits=bits)

    g_idx = torch.tensor([i // qlinear.group_size for i in range(qlinear.in_features)], dtype=torch.int32)
    fp16_weight = dequant_weight(weight.T, zeros.T, qlinear.scales, g_idx).cuda()
    # weight = (scales * (weight - zeros))
    # weight = weight.reshape(weight.shape[0] * weight.shape[1], weight.shape[2])
    return fp16_weight, qlinear.scales.T, zeros.T


import torch
import torch.nn as nn
from auto_gptq.utils.import_utils import dynamically_import_QuantLinear
import copy
torch.set_printoptions(threshold=10000)

#from awq.quantize.qmodule import WQLinear

from awq.modules.linear import WQLinear_GEMM

group_size = 128
bits = 4

m = 1
k = 11008
n = 4096
device = torch.device("cuda:0")

awq_linear = WQLinear_GEMM(w_bit=bits, group_size=group_size, in_features=k, out_features=n, bias=False, dev="cuda")

from safetensors import safe_open

tensors = {}
with safe_open("/fsx/felix/llama_7b_awq_gemm/model.safetensors", framework="pt", device=0) as f:
    #for k in ["model.layers.0.mlp.down_proj.qweight", "model.layers.0.mlp.down_proj.qzeros", "model.layers.0.mlp.down_proj.scales"]:
    scales = f.get_tensor("model.layers.0.mlp.down_proj.scales").to(torch.float16)
    qweight = f.get_tensor("model.layers.0.mlp.down_proj.qweight")
    qzeros = f.get_tensor("model.layers.0.mlp.down_proj.qzeros")
# scales = torch.load("/fsx/felix/vicuna_7b_awq_gemv/down_proj_scales.pt").to(torch.float16)
# qweight = torch.load("/fsx/felix/vicuna_7b_awq_gemv/down_proj_qweight.pt")
# qzeros = torch.load("/fsx/felix/vicuna_7b_awq_gemv/down_proj_qzeros.pt")


print("awq_linear.qweight.dtype", awq_linear.qweight.dtype)
print("qweight.dtype", qweight.dtype)
print("awq_linear.qweight.shape", awq_linear.qweight.shape)
print("qweight.shape", qweight.shape)
assert awq_linear.qweight.shape == qweight.shape
assert awq_linear.qzeros.shape == qzeros.shape
assert awq_linear.scales.shape == scales.shape
assert awq_linear.qweight.dtype == qweight.dtype
assert awq_linear.qzeros.dtype == qzeros.dtype
assert awq_linear.scales.dtype == scales.dtype

awq_linear.qweight = qweight.to("cuda")
awq_linear.qzeros = qzeros.to("cuda")
awq_linear.scales = scales.to("cuda")

awq_linear = awq_linear.eval()

inp = torch.rand(1, m, k, dtype=torch.float16).to(device)

with torch.no_grad():
    res_awq_original = awq_linear(inp).to(torch.float32)

f16_weight, scales_unpack, zeros_unpack = unpack(awq_linear, pack_mode="GEMM")

linear_unpacked = nn.Linear(k, n, bias=False).to("cuda").to(torch.float16)
linear_unpacked.weight = torch.nn.Parameter(f16_weight)

linear_class = dynamically_import_QuantLinear(use_triton=False, desc_act=False, group_size=group_size, bits=bits, disable_exllama=True, disable_exllamav2=True)
gptq_linear = linear_class(
    bits=bits,
    group_size=group_size,
    infeatures=k,
    outfeatures=n,
    bias=False,
)

linear_unpacked = linear_unpacked.to("cpu")
scales_unpack = scales_unpack.to("cpu")
zeros_unpack = zeros_unpack.to("cpu")

gptq_linear.pack(copy.deepcopy(linear_unpacked), copy.deepcopy(scales_unpack), copy.deepcopy(zeros_unpack), g_idx=None)

gptq_linear = gptq_linear.to("cuda")
gptq_linear = gptq_linear.eval()

#gptq_linear.handle_qzeros_for_autogptq()

with torch.no_grad():
    res_gptq = gptq_linear(inp).to(torch.float32)

# print("res_awq_original", res_awq_original)
# print("res_gptq", res_gptq)

# print("Reldiff", (res_awq_original - res_gptq).abs() / (res_awq_original.abs() + 1e-15))

print("------ autogptq")

reldiff_autogptq = (res_awq_original - res_gptq).abs() / (res_awq_original.abs() + 1e-15)
print("Reldiff", reldiff_autogptq)
print("p90 reldiff awq/gptq", torch.quantile(reldiff_autogptq, 0.9))
print("Median reldiff awq/gptq", reldiff_autogptq.median())
print("Mean reldiff awq/gptq", reldiff_autogptq.mean())
print("reldiff > 5e-2 awq/gptq", torch.sum(reldiff_autogptq > 5e-2).item(), f"total = {res_awq_original.numel()}")

print("reldiff_autogptq > 0.1 where:", torch.argwhere(reldiff_autogptq > 0.1))
print("reldiff_autogptq > 0.1:", reldiff_autogptq[reldiff_autogptq > 0.1])

qllm_repacked_qweight = torch.load("/fsx/felix/QLLM/down_proj_qweight_gptq_repacked.pt")
qllm_repacked_qzeros = torch.load("/fsx/felix/QLLM/down_proj_qzeros_gptq_repacked.pt")
qllm_repacked_scales = torch.load("/fsx/felix/QLLM/down_proj_scales_gptq_repacked.pt")

assert qllm_repacked_qweight.dtype == gptq_linear.qweight.dtype
assert qllm_repacked_qzeros.dtype == gptq_linear.qzeros.dtype
assert qllm_repacked_scales.dtype == gptq_linear.scales.dtype
assert qllm_repacked_qweight.shape == gptq_linear.qweight.shape
assert qllm_repacked_qzeros.shape == gptq_linear.qzeros.shape
assert qllm_repacked_scales.shape == gptq_linear.scales.shape

print("Mean reldiff qweight", ((qllm_repacked_qweight - gptq_linear.qweight).abs() / (qllm_repacked_qweight.abs() + 1e-15)).mean())
print("Mean reldiff qzeros", ((qllm_repacked_qzeros - gptq_linear.qzeros).abs() / (qllm_repacked_qzeros.abs() + 1e-15)).mean())
print("Mean reldiff scales", ((qllm_repacked_scales - gptq_linear.scales).abs() / (qllm_repacked_scales.abs() + 1e-15)).mean())

print("------- qllm")

from qllm.quant.quant_linear import QuantLinear

qllm_linear = QuantLinear(bits, groupsize=group_size, infeatures=k, outfeatures=n, bias=False)
qllm_linear.pack(linear_unpacked, scales_unpack, zeros_unpack, g_idx=None)

qllm_linear = qllm_linear.to("cuda")
qllm_linear = copy.deepcopy(qllm_linear)


with torch.no_grad():
    res_qllm = qllm_linear(inp).to(torch.float32)

reldiff_qllm = (res_awq_original - res_qllm).abs() / (res_awq_original.abs() + 1e-15)

print("Reldiff awq/gptq (qllm)", reldiff_qllm)
print("p90 reldiff awq/gptq", torch.quantile(reldiff_qllm, 0.9))
print("Median reldiff awq/gptq (qllm)", reldiff_qllm.median())
print("Mean reldiff awq/gptq (qllm)", reldiff_qllm.mean())
print("reldiff > 5e-2 awq/gptq (qllm)", torch.sum(reldiff_qllm > 5e-2).item(), f"total = {res_awq_original.numel()}")

print("reldiff_qllm > 0.1 where:", torch.argwhere(reldiff_qllm > 0.1))
print("reldiff_qllm > 0.1:", reldiff_qllm[reldiff_qllm > 0.1])


#awq_linear.qweight = qweight.to("cuda")
#awq_linear.qzeros = qzeros.to("cuda")
#awq_linear.scales = scales.to("cuda")

"""
assert torch.equal(qllm_repacked_qweight, gptq_linear.qweight)
assert torch.equal(qllm_repacked_qzeros, gptq_linear.qzeros)
assert torch.equal(qllm_repacked_scales, gptq_linear.scales)


assert torch.allclose(res_awq_original, res_gptq)
"""