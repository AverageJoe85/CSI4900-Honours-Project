from openai import OpenAI
from apiKey import apiKey

client = OpenAI(
    api_key=apiKey
)

tools = [{
    "type": "function",
    "function": {
        "name": "game_24_step",
        "description": "One step of game of 24. Each step consists of one equation (ex. a+b=c), and the remaining numbers (ex. c, d, e).",
        "parameters": {
            "type": "object", #what other types are there? Should this be changed?
            "properties": {
                "number_x": {
                    "type": "integer",
                    "description": "One of the given numbers."
                },
                "operator": {
                    "type": "string",
                    "description": "The operator used for this step's equation."
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
            "additionalProperties": False #required, but what does this do?
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o-mini",
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

print(completion.choices[0].message.tool_calls)
