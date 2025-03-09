from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Encode input text
input_text = "Solve: 2 + 2 = "
input_ids = tokenizer.encode(input_text, return_tensors="pt")

tokenizer.pad_token = tokenizer.eos_token

# Generate text
output = model.generate(
    input_ids, 
    attention_mask=torch.ones_like(input_ids),
    max_length=50,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    do_sample=True,
    temperature=0.5,
    top_k=50,
    repetition_penalty=1.5
)

# Decode and print result
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
