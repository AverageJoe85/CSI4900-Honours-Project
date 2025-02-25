from openai import OpenAI
from apiKey import apiKey
client = OpenAI(
    api_key=apiKey,
    base_url="https://api.llama-api.com" #required
)

tools = [{
    "type": "function",
    "function": {
        "name": "game_24_step",
        "description": "One step of game of 24 in a specific format. Each step consists of one equation (ex. a+b=c), and the remaining numbers (ex. c, d, e).",
        "parameters": {
            "type": "object", #what other types are there? Should this be changed?
            "properties": {
                "first_number": {
                    "type": "integer",
                    "description": "First number in the step's equation."
                },
                "operator": {
                    "type": "string",
                    "description": "The operator used in the step's equation."
                },
                "second_number": {
                    "type": "integer",
                    "description": "Second number in the step's equation."
                },
                "remaining_numbers": {
                    "type": "array",
                    "items": { "type": "integer" },
                    "description": "The numbers left to be used, including the result of this step's equation."
                }
            },
            "required": [
                "first_number", "operator", "second_number", "remaining_numbers"
            ],
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="llama3.1-8b", #some models break with the "strict": true parameter, this model seems fine (for now)
    messages=[
        {
            "role": "system",
            "content": "You are an expert in solving game of 24 steps."
        },
        {
            "role": "user",
            "content": "Provide a potential first step of the game of 24 with these numbers: (4 9 10 13)."
        }
    ],
    tools = tools #required
)

print(completion.choices[0].message.tool_calls)
