import os

import torch
import torch.nn as nn
import copy

from qllm.quant.quant_linear_awq import WQLinear_GEMM
from qllm.quant.quant_linear import QuantLinear

torch.set_printoptions(threshold=10000)

group_size = 128
bits = 4

m = 8
k = 11008
n = 4096
device = torch.device("cuda:0")

awq_linear = WQLinear_GEMM(w_bit=bits, group_size=group_size, in_features=k, out_features=n, bias=False)

from auto_gptq.nn_modules.qlinear.qlinear_cuda_old import QuantLinear as QuantLinearAutoGPTQ

from safetensors import safe_open

tensors = {}
with safe_open("/fsx/felix/llama_7b_awq_gemm/model.safetensors", framework="pt", device=0) as f:
    scales = f.get_tensor("model.layers.0.mlp.down_proj.scales").to(torch.float16)
    qweight = f.get_tensor("model.layers.0.mlp.down_proj.qweight")
    qzeros = f.get_tensor("model.layers.0.mlp.down_proj.qzeros")


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

awq_linear = awq_linear.to("cuda")
awq_linear.qweight = qweight.to("cuda")
awq_linear.qzeros = qzeros.to("cuda")
awq_linear.scales = scales.to("cuda")

awq_linear = awq_linear.eval()

inp = torch.rand(1, m, k, dtype=torch.float16).to(device)

with torch.no_grad():
    res_awq_original = awq_linear(inp).to(torch.float32)

# NOTE: Somehow we need this on here to have good results.
#os.environ['load_from_autogptq'] = "0"

f16_weight, scales_unpack, zeros_unpack = awq_linear.unpack()

linear_unpacked = nn.Linear(k, n, bias=False).to("cuda").to(torch.float16)
linear_unpacked.weight = torch.nn.Parameter(f16_weight)

linear_unpacked = linear_unpacked.to("cpu")
scales_unpack = scales_unpack.to("cpu")
zeros_unpack = zeros_unpack.to("cpu")

torch.save(zeros_unpack, f"qllm_unpacked_qzeros.bin")

qllm_linear = QuantLinear(bits, groupsize=group_size, infeatures=k, outfeatures=n, bias=False)
qllm_linear.pack(linear_unpacked, scales_unpack.T, zeros_unpack.T, g_idx=None)

# NOTE: Somehow we need this off here have good results.
#os.environ['load_from_autogptq'] = "1"

qllm_linear = qllm_linear.to("cuda")

with torch.no_grad():
    res_qllm = qllm_linear(inp).to(torch.float32)

reldiff_qllm = (res_awq_original - res_qllm).abs() / (res_awq_original.abs() + 1e-15)

#print("Reldiff awq/gptq (qllm)", reldiff_qllm)
print("p90 reldiff awq/gptq", torch.quantile(reldiff_qllm, 0.9))
print("Median reldiff awq/gptq (qllm)", reldiff_qllm.median())
print("Mean reldiff awq/gptq (qllm)", reldiff_qllm.mean())
print("numel reldiff > 0.02:", torch.sum(reldiff_qllm > 5e-2).item(), f"out of total={res_awq_original.numel()}")
print("numel reldiff > 0.1:", reldiff_qllm[reldiff_qllm > 0.1].numel(), f"out of total={res_awq_original.numel()}")
print("numel reldiff > 0.5:", reldiff_qllm[reldiff_qllm > 0.5].numel(), f"out of total={res_awq_original.numel()}")

torch.save(qllm_linear.qweight, "qllm_qweight.bin")
torch.save(qllm_linear.scales, "qllm_scales.bin")
torch.save(qllm_linear.qzeros, "qllm_qzeros.bin")

autogptq_qlinear = QuantLinearAutoGPTQ(
    bits,
    group_size,
    infeatures=k,
    outfeatures=n,
    bias=False,
)

with safe_open("/fsx/felix/llama_7b_awq_gemm/autogptq_model.safetensors", framework="pt", device=0) as f:
    autogptq_qweight = f.get_tensor("model.layers.0.mlp.down_proj.qweight")
    autogptq_scales = f.get_tensor("model.layers.0.mlp.down_proj.scales")
    autogptq_qzeros = f.get_tensor("model.layers.0.mlp.down_proj.qzeros")

autogptq_qlinear.qweight = autogptq_qweight.to("cuda")
autogptq_qlinear.qzeros = autogptq_qzeros.to("cuda")
autogptq_qlinear.scales = autogptq_scales.to("cuda").to(torch.float16)

with torch.no_grad():
    res_autogptq = autogptq_qlinear(inp).to(torch.float32)

reldiff_autogptq = (res_awq_original - res_autogptq).abs() / (res_awq_original.abs() + 1e-15)
print("------ autogptq comparison")
print("p90 reldiff awq/autogptq", torch.quantile(reldiff_autogptq, 0.9))
print("Median reldiff awq/autogptq", reldiff_autogptq.median())
print("Mean reldiff awq/autogptq", reldiff_autogptq.mean())
print("numel reldiff > 0.02:", torch.sum(reldiff_autogptq > 5e-2).item(), f"out of total={res_awq_original.numel()}")
print("numel reldiff > 0.1:", reldiff_autogptq[reldiff_autogptq > 0.1].numel(), f"out of total={res_awq_original.numel()}")
print("numel reldiff > 0.5:", reldiff_autogptq[reldiff_autogptq > 0.5].numel(), f"out of total={res_awq_original.numel()}")
