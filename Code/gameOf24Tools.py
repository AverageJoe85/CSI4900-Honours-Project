nextStepTools = [
    {
        "type": "function",
        "function": {
            "name": "game24Step",
            "description": "One step of game of 24. Randomly pick numberX, operator, and numberY.",
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
                        "description": "One of the inputNumbers."
                    },
                    "operator": {
                        "type": "string",
                        "description": "The operator used for this step's equation (possible operators: +, -, *, /)."
                    },
                    "numberY": {
                        "type": "integer",
                        "description": "Another of the inputNumbers."
                    },
                    "numberZ": {
                        "type": "integer",
                        "description": "The result of number_x operator number_y."
                    } #remainingNumbers removed because it was insanely inconsistent. This technically breaks what the paper did but I don't think it matters much in this case.
                },
                "required": [
                    "inputNumbers", "numberX", "operator", "numberY", "numberZ"
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
                        "description": "Based on how likely a step is to lead to a valid solution to the game of 24, choose 2 for 'sure', 1 for 'maybe', or 0 for 'unlikely'."
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

inputOutputTools = [
    {
        "type": "function",
        "function": {
            "name": "solve",
            "description": "Give a series of equations using each of the 4 input numbers only once. Subsequent equations can use the result of previous equations, but only once.",
            "parameters": {
                "type": "object",
                "properties": {
                    "firstEquationFirstNumber": {
                        "type": "integer",
                        "description": "First number of first equation"
                    },
                    "firstEquationOperator": {
                        "type": "string",
                        "description": "Operator of first equation. Can be +, -, *, or /."
                    },
                    "firstEquationSecondNumber": {
                        "type": "integer",
                        "description": "Second number of first equation"
                    },
                    "secondEquationFirstNumber": {
                        "type": "integer",
                        "description": "First number of second equation"
                    },
                    "secondEquationOperator": {
                        "type": "string",
                        "description": "Operator of second equation. Can be +, -, *, or /."
                    },
                    "secondEquationSecondNumber": {
                        "type": "integer",
                        "description": "Second number of second equation"
                    },
                    "thirdEquationFirstNumber": {
                        "type": "integer",
                        "description": "First number of third equation"
                    },
                    "thirdEquationOperator": {
                        "type": "string",
                        "description": "Operator of third equation. Can be +, -, *, or /."
                    },
                    "thirdEquationSecondNumber": {
                        "type": "integer",
                        "description": "Second number of third equation"
                    },
                },
                "required": [
                    "firstEquationFirstNumber", "firstEquationOperator", "firstEquationSecondNumber",
                    "secondEquationFirstNumber", "secondEquationOperator", "secondEquationSecondNumber",
                    "thirdEquationFirstNumber", "thirdEquationOperator", "thirdEquationSecondNumber"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
