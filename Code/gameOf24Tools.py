nextStepTools = [
    {
        "type": "function",
        "function": {
            "name": "game24Step",
            "description": "One step of game of 24. number_x and number_y can be any of the input numbers.",
            "parameters": {
                "type": "object", #what other types are there? Should this be changed?
                "properties": {
                    "inputNumbers": {
                        "type": "array",
                        "items": { "type": "integer" },
                        "description": "All the input numbers including those used and those not used."
                    },
                    "numberX": {
                        "type": "integer",
                        "description": "One of the given numbers."
                    },
                    "operator": {
                        "type": "string",
                        "description": "The operator used for this step's equation (possible operators: +, -, *, /)."
                    },
                    "numberY": {
                        "type": "integer",
                        "description": "Another of the given numbers."
                    },
                    "numberZ": {
                        "type": "integer",
                        "description": "The result of number_x operator number_y."
                    },
                    "remainingNumbers": {
                        "type": "array",
                        "items": { "type": "integer" },
                        "description": "inputNumbers - [numberX and numberY]" #TODO: if number_z matches a remaining number, that number won't be in the array which is obviously not intended (ex. [4, 9, 10, 13] -> 4+9=13 -> [10])
                    }
                },
                "required": [
                    "inputNumbers", "numberX", "operator", "numberY", "numberZ", "remainingNumbers"
                ],
                "additionalProperties": False #required due to 'strict: True' I believe, but what does this do exactly?
            },
            "strict": True
        }
    }
]

evaluationTools = [
    {
        "type": "function",
        "function": {
            "name": "evaluateStep",
            "description": "Evaluate how likely a game of 24 step is to lead to a valid solution.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stepPotential": {
                        "type": "integer",
                        "description": "Based on how likely a step is to lead to a valid solution to the game of 24, choose 2 for 'sure', 1 for 'maybe', or 0 for 'impossible'."
                    }
                },
                "required": [
                    "stepPotential"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
