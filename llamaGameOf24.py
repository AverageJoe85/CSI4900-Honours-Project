from openai import OpenAI
from apiKey import apiKey, apiKeyOpenAI #create apiKey.py which has apiKey set as your LlamaAPI key and apiKeyOpenAI set as your OpenAI key (set to empty string if doesn't exist)
import json
import time

# 0 = OpenAI, 1 = LlamaAPI
useLlamaAPI = 0

startTime = time.time()

if useLlamaAPI:
    model = "llama3.1-70b" #llama3.1-70b
    print("Using LlamaAPI with model: " + model + "\n")
    client = OpenAI(
        api_key=apiKey,
        base_url="https://api.llama-api.com"
    )
else:
    model = "gpt-4o-mini"
    print("Using OpenAI with model: " + model + "\n")
    client = OpenAI(
        api_key=apiKeyOpenAI
    )


tools = [
    {
        "type": "function",
        "function": {
            "name": "game_24_step",
            "description": "One step of game of 24. number_x and number_y can be any of the input numbers.",
            "parameters": {
                "type": "object", #what other types are there? Should this be changed?
                "properties": {
                    "input_numbers": {
                        "type": "array",
                        "items": { "type": "integer" },
                        "description": "All the input numbers including those used and those not used."
                    },
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
                        "description": "input_numbers - [number_x and number_y]"
                    }
                },
                "required": [
                    "input_numbers", "number_x", "operator", "number_y", "number_z", "remaining_numbers"
                ],
                "additionalProperties": False #required due to 'strict: True' I believe, but what does this do exactly?
            },
            "strict": True
        }
    }
]

completion = client.chat.completions.create(
    model = model, #https://platform.openai.com/docs/pricing
    messages=[
        {
            "role": "system",
            "content": "You must call exactly one tool function per response. You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24. Therefore there will be exactly 3 steps to the game of 24."
        },
        {
            "role": "user",
            "content": "Provide a potential first step of the game of 24 with these numbers: (4 9 10 13)."
        }
    ],
    tools = tools, #required
    tool_choice= "required"
)

if not completion.choices[0].message.tool_calls:    
    print("No tools were called, I bet Llama is behind this.")
    endTime = time.time()
    print("\nExecution Time: " + str(endTime - startTime) + " seconds")
    exit()



# ===========TODO=============
# Function
def game24(number_x, operator, number_y, number_z, remaining_numbers):
    pass


print("Number of tool calls: " + str(len(completion.choices[0].message.tool_calls)) + "\n") #number of tool calls should be 1 for efficiency
print(completion.choices[0].message.tool_calls[0])

# Passing the output to a function
tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)
result = game24(args["number_x"], args["operator"], args["number_y"], args["number_z"], args["remaining_numbers"])

endTime = time.time()
print("\nExecution Time: " + str(endTime - startTime) + " seconds")
