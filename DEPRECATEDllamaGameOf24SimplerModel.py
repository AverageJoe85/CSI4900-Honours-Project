from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()  # Set model to evaluation mode

# Generate a response
prompt = """<|system|>You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24. Therefore there will be exactly 3 steps to the game of 24.
<|user|>What is a potential first step in the game of 24? Give your answer in the form of numA operator numB = result
<|assistant|>"""
inputs = tokenizer(prompt, return_tensors="pt").to(device)

outputs = model.generate(**inputs, max_new_tokens=1000, do_sample=True, temperature=0.7)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)
