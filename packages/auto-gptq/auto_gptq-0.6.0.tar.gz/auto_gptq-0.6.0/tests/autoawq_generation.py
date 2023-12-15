from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer, TextStreamer

quant_path = "/fsx/felix/llama_7b_awq_gemm"

# Load model
model = AutoAWQForCausalLM.from_quantized(quant_path, fuse_layers=False)
tokenizer = AutoTokenizer.from_pretrained(quant_path)

prompt = "I am in Paris and I am going to see the"

tokens = tokenizer(prompt, return_tensors='pt').input_ids.cuda()

# Generate output
generation_output = model.generate(
    tokens,
    num_beams=1,
    min_new_tokens=30,
    max_new_tokens=30,
)

print(tokenizer.decode(generation_output[0]))