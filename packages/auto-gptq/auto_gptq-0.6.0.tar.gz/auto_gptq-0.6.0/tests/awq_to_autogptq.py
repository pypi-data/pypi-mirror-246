import torch

from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

#device = "cuda:0"
device = "cuda:0"

model_q = AutoGPTQForCausalLM.from_quantized("/fsx/felix/llama_7b_awq_gemm", device=device, use_triton=False, inject_fused_attention=False, inject_fused_mlp=False, disable_exllama=True, disable_exllamav2=True, torch_dtype=torch.float32)
tokenizer = AutoTokenizer.from_pretrained("/fsx/felix/llama_7b_awq_gemm")

prompt = "I am in Paris and I am going to see the"
device = torch.device(device)

inp = tokenizer(prompt, return_tensors="pt").to(device)

res = model_q.model.generate(**inp, num_beams=1, min_new_tokens=10, max_new_tokens=10)

print("predicted:", tokenizer.decode(res[0]))
