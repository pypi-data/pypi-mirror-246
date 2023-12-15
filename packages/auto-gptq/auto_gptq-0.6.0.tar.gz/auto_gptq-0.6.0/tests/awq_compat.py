import torch
import torch.nn as nn
from auto_gptq.utils.import_utils import dynamically_import_QuantLinear
import copy

from awq.quantize.qmodule import WQLinear

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

from safetensors import safe_open

tensors = {}
with safe_open("/fsx/felix/vicuna_7b_gptq/model.safetensors", framework="pt", device=0) as f:
    #for k in ["model.layers.0.mlp.down_proj.qweight", "model.layers.0.mlp.down_proj.qzeros", "model.layers.0.mlp.down_proj.scales"]:
    scales = f.get_tensor("model.layers.0.mlp.down_proj.scales").to(torch.float16)
    qweight = f.get_tensor("model.layers.0.mlp.down_proj.qweight")
    qzeros = f.get_tensor("model.layers.0.mlp.down_proj.qzeros")

gptq_linear.qweight = qweight
gptq_linear.qzeros = qzeros
gptq_linear.scales = scales

gptq_linear = gptq_linear.eval()
gptq_linear = gptq_linear.to(device)

inp = torch.rand(1, m, k, dtype=torch.float16).to(device)

with torch.no_grad():
    res_gptq = gptq_linear(inp)

unpacked_weight, unpacked_zeros = gptq_linear.unpack()
unpacked_zeros = unpacked_zeros.to("cpu")

unpacked_linear = nn.Linear(k, n, bias=False)
assert unpacked_linear.weight.shape == unpacked_weight.t().shape
unpacked_linear.weight = torch.nn.Parameter(unpacked_weight.t().contiguous())

gptq_linear = gptq_linear.to("cpu")
unpacked_linear = unpacked_linear.to("cpu")

#unpacked_zeros += 1

print("gptq_linear.scales", gptq_linear.scales.dtype)
awq_linear = WQLinear.from_linear_gptq(unpacked_linear.weight.to("cpu"), w_bit=bits, group_size=128, scales=gptq_linear.scales.to("cpu"), zeros=unpacked_zeros.to("cpu"))
awq_linear = awq_linear.to("cuda")

print("inp", inp.dtype)
print("awq_linear scales", scales.dtype)

with torch.no_grad():
    res_awq = awq_linear(inp)

assert res_awq.shape == res_gptq.shape
torch.set_printoptions(threshold=10000)
#print(res_awq - res_gptq)
print("Relative diff", ((res_awq - res_gptq).abs()) / (res_gptq.abs() + 1e-15))