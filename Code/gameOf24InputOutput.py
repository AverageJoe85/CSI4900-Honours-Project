from openai import OpenAI
import json
import apiKey

model = "gpt-4o-mini"
print("Using OpenAI with model: " + model + "\n")
client = OpenAI(api_key=apiKey.apiKey)


system_message = {
    "role": "system",
    "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24."
}

initial_numbers = [10, 48, 2, 4]

completion = client.chat.completions.create(
    model=model,
    messages= [
        {"role": "system",
    "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24."},
        {"role": "user", "content": f"Solve the game of 24 for these numbers: {initial_numbers}"}],
)


response = completion.choices[0].message.content
print(response)
