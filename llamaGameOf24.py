from openai import OpenAI
from apiKey import apiKey
import json

client = OpenAI(
    api_key=apiKey
)

tools = [{
    "type": "function",
    "function": {
        "name": "game_24_step",
        "description": "One step of game of 24.",
        "parameters": {
            "type": "object", #what other types are there? Should this be changed?
            "properties": {
                "number_x": {
                    "type": "integer",
                    "description": "One of the given numbers."
                },
                "operator": {
                    "type": "string",
                    "description": "The operator used for this step's equation (possible operators: +, -, *, /)."
                },
                "number_y": {
                    "type": "integer",
                    "description": "Another of the given numbers."
                },
                "number_z": {
                    "type": "integer",
                    "description": "The result of number_x operator number_y."
                },
                "remaining_numbers": {
                    "type": "array",
                    "items": { "type": "integer" },
                    "description": "Unused numbers."
                }
            },
            "required": [
                "number_x", "operator", "number_y", "number_z", "remaining_numbers"
            ],
            "additionalProperties": False #required due to strict: True I believe, but what does this do exactly?
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o-mini", #https://platform.openai.com/docs/pricing
    messages=[
        {
            "role": "system",
            "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24. Therefore there will be exactly 3 steps to the game of 24."
        },
        {
            "role": "user",
            "content": "Provide a potential first step of the game of 24 with these numbers: (4 9 10 13)."
        }
    ],
    tools = tools #required
)

# ===========TODO=============
# Function
def game24(number_x, operator, number_y, number_z, remaining_numbers):
    pass


# Passing the output to a function
tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

#result = game24(args["number_x"], args["operator"], args["number_y"], args["number_z"], args["remaining_numbers"])

print(completion.choices[0].message.tool_calls[0])
