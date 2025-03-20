from openai import OpenAI
import json
import time
# create apiKey.py in Code folder(either variable can be set as blank string if needed):
#apiKey="LA-..."
#apiKeyOpenAI="sk-proj-..."
import apiKey
import gameOf24Tools #includes nextStepTools and 

model = "gpt-4o-mini" #https://platform.openai.com/docs/pricing, we'll eventually use gpt-4o or gpt-4 to be more comparable to paper
print("Using OpenAI with model: " + model + "\n")
client = OpenAI(api_key=apiKey.apiKeyOpenAI)

# Used for knowing how long you'll have to wait on subsequent runs
startTime = time.time()

inputNumbers = [4, 9, 10, 13]

potentialNextSteps = []
nextStepEvaluations = []
promisingSteps = []
numPotentialSteps = 0


#TODO: I think we want to store each potential step with its message history.
#This is so the LLM has the context of what it's done so far. We need to append the potential step
#to its personal message history, then append our question of "How likely can this produce a valid solution?".
#We then append that and ask it for 10 more potential next steps. <-So maybe we should also put
#the below loop into a function to be called whenever we need the next level of steps.
while numPotentialSteps < 10:
    completion = client.chat.completions.create(
        model = model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24. The user will tell you the input numbers and you will give a potential next step."
            },
            {
                "role": "user",
                "content": f"Input: {inputNumbers}. Possible next steps:"
            }
        ],
        tools = gameOf24Tools.nextStepTools, #required
        tool_choice= "required",
    )
    toolCalls = completion.choices[0].message.tool_calls
    if toolCalls:
        for toolCall in toolCalls:
            numPotentialSteps += 1 #weird, I forgot Python doesn't support int++
            args = json.loads(toolCall.function.arguments)
            potentialNextSteps.append(args)
            print(args)
    print(numPotentialSteps)




### Parsing output
##toolCalls = completion.choices[0].message.tool_calls
##print(f"Number of tool calls: {str(len(toolCalls))}\n") #number of tool calls should be 1 for efficiency
##
##args = json.loads(toolCalls[0].function.arguments)
##print("input_numbers: " + str(args["input_numbers"]))
##print("number_x: " + str(args["number_x"]))
##print("operator: " + str(args["operator"]))
##print("number_y: " + str(args["number_y"]))
##print("=")
##print("number_z: " + str(args["number_z"]))
##print("remaining_numbers: " + str(args["remaining_numbers"]))



# DEBUGGING
# How long did it take to run this program:
endTime = time.time()
print("\nExecution Time: " + str(endTime - startTime) + " seconds, or " + str((endTime-startTime)/60) + " minutes")

### See all tool calls (and entire completion)
##open("debugOutput.txt", "w").write(json.dumps(completion.model_dump(),indent=4))
