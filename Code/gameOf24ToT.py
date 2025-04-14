###IMPORTS###
from openai import OpenAI
import json
import time
import apiKey
import gameOf24Tools  # Includes nextStepTools and evaluationTools
client = OpenAI(api_key=apiKey.apiKey)
system_message = {
    "role": "system",
    "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24."
}


###FUNCTIONS###
# Function to generate possible next steps given the current numbers and conversation history
def generate_steps(remaining_numbers, message_history):
    steps = [] #Return value, stores all generated steps
    failed_attempts = 0
    max_failed_attempts = 5  #limit to avoid excessive API calls and excessive execution time
    
    while len(steps) < a and failed_attempts < max_failed_attempts: #ideally generate at least 'a' unique steps
        # Completion is just LLM's response
        completion = client.chat.completions.create(
            model=model, #model chosen previously
            # Attach current node's message history to new query asking for potential next steps so LLM has greater context
            messages=message_history + [{"role": "user", "content": f"Input: {remaining_numbers}. Possible next step:"}],
            tools=gameOf24Tools.nextStepTools, #use tool defined in other file for generating formatted next steps
            tool_choice="required" #require the use of the tool so response is formatted
        )

        assistant_msg = completion.choices[0].message #Retrieves actual message portion of LLM response, which includes both human readable responses and tool calls 
        for tool_call in assistant_msg.tool_calls: #Iterates over every tool call
            step = json.loads(tool_call.function.arguments) #Formats current tool call

            # Confirms all parts of a step are included in current step
            if not all(k in step for k in ["numberX", "numberY", "operator"]):
                failed_attempts += 1
                continue
        
            # make sure that numbers used in the step exist in the remaining numbers
            if step["numberX"] not in remaining_numbers or step["numberY"] not in remaining_numbers:
                failed_attempts += 1
                continue # skip invalid steps
            
            # calculate result of the operation
            if step["operator"] == "+":
                result = step["numberX"] + step["numberY"]
            elif step["operator"] == "-":
                result = step["numberX"] - step["numberY"]
            elif step["operator"] == "*":
                result = step["numberX"] * step["numberY"]
            elif step["operator"] == "/":
                result = step["numberX"] / step["numberY"] if step["numberY"] != 0 else float("inf")
            else:
                failed_attempts += 1
                continue 
            
            step["numberZ"] = result # store result
            
            # Simulate tool response for evaluation
            tool_response = {
                "role": "tool",
                "content": json.dumps({"numberZ": result}),
                "tool_call_id": tool_call.id
            }
            step_history = message_history + [step] # update history
            steps.append({"step": step, "history": step_history})
    
    return steps

# Function to evaluate the potential of a step leading to 24
def evaluate_step(step, path, remaining):
    eval_history = [
        system_message,
        {"role": "user", "content": f"Given the steps so far: {path}, and remaining numbers: {remaining}, evaluate how likey this step will reach 24: {step['numberX']} {step['operator']} {step['numberY']} = {step['numberZ']}. Consider if the result is too big or too small to reach 24 with the remaining numbers."}
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=eval_history,
        tools=gameOf24Tools.evaluationTools,
        tool_choice="required"
    )
    tool_call = completion.choices[0].message.tool_calls[0]
    score = json.loads(tool_call.function.arguments)["stepPotential"] # extract evaluation score
    return score

# Function to update the list of remaining numbers after a step
def calculate_remaining_numbers(remaining_numbers, step):
    current_nums = remaining_numbers.copy()
    used_nums = [step["numberX"], step["numberY"]]
    for num in used_nums:
        if num in current_nums:
            current_nums.remove(num)
    current_nums.append(step["numberZ"])
    return current_nums

# Function to build the solution tree
def build_tree(initial_numbers, b, system_message):
    tree = [] #return value (saves top 'b' nodes of each step level
    # Initializes current_level with 4 given numbers, the message history (for LLM's ability to read its
    #previous replies in branch), and an empty path array. At level 0, there's only one node (the root node)
    #which has the initial 4 numbers, a message history with just the system message, and an empty path (since
    #there are no ndoes before it in the tree). Current level is repalced at each level of nodes.
    current_level = [{"remaining": initial_numbers, "history": [system_message], "path": []}]

    # 3 steps are always required to reach a final result (level 1, 2, and 3),
    #but step 3 doesn't require a call to evaluate_step
    # STEP 1 AND 2
    for level in range(2):
        candidates = [] #Filled with all potential next steps, then later trimmed to the 'b' top potential steps
        expected_remaining_count = 4 - (level + 1) #For pruning a node if a it lost remaining numbers somewhere
        
        # Generate all possible steps for the current level
        for branch in current_level:
            if len(branch["remaining"]) <= 1:
                candidates.append({
                    "branch": branch,
                    "score": branch.get("score", 0),
                    "proximity": 0  # default for branches already at 1 number
                })
                continue
            
            # Takes current node (branch) and generates potential next steps
            steps = generate_steps(branch["remaining"], branch["history"])
            for step_data in steps:
                step = step_data["step"]
                remaining = calculate_remaining_numbers(branch["remaining"], step)
                if len(remaining) != expected_remaining_count:
                    continue
                
                new_path = branch["path"] + [f"{step['numberX']} {step['operator']} {step['numberY']} = {step['numberZ']}"]
                score = evaluate_step(step, new_path, remaining)
                
                # calculate proximity to 24 as a tiebreaker
                proximity = abs(step["numberZ"] - 24)
                
                candidates.append({
                    "branch": {
                        "remaining": remaining,
                        "history": [
                            system_message,
                            {"role": "user", "content": f"Previous steps: {new_path}"}
                        ],
                        "path": new_path,
                        "score": score
                    },
                    "score": score,
                    "proximity": proximity
                })
        
        # Sort candidates by score (descending) and proximity (ascending) for ties
        candidates.sort(key=lambda x: (-x["score"], x["proximity"]))
        # Keep top b=5 branches
        next_level = [candidate["branch"] for candidate in candidates[:b]]
        
        current_level = next_level
        tree.append(current_level)

        if __name__ == "__main__":
            print(f"\nLevel {level + 1} Top {b} Steps:")
            for branch in current_level:
                print(f"Path: {branch['path']}, Remaining: {branch['remaining']}, Score: {branch['score']}")

    # STEP 3
    candidates = [] #Filled with all potential next steps, then later trimmed to the 'b' top potential steps
    expected_remaining_count = 1 #For pruning a node if a it lost remaining numbers somewhere
    
    # Generate all possible steps for the current level
    for branch in current_level:
        if len(branch["remaining"]) <= 1:
            candidates.append({
                "branch": branch,
                "score": branch.get("score", 0),
                "proximity": 0  # default for branches already at 1 number
            })
            continue
        
        # Takes current node (branch) and generates potential next steps
        steps = generate_steps(branch["remaining"], branch["history"])
        for step_data in steps:
            step = step_data["step"]
            remaining = calculate_remaining_numbers(branch["remaining"], step)
            if len(remaining) != expected_remaining_count:
                continue
            
            new_path = branch["path"] + [f"{step['numberX']} {step['operator']} {step['numberY']} = {step['numberZ']}"]
            
            # calculate proximity to 24 as a tiebreaker
            proximity = abs(step["numberZ"] - 24)
            
            candidates.append({
                "branch": {
                    "remaining": remaining,
                    "history": [
                        system_message,
                        {"role": "user", "content": f"Previous steps: {new_path}"}
                    ],
                    "path": new_path,
                    "score": score
                },
                "score": score,
                "proximity": proximity
            })
    
    # Keep all branches
    current_level = [candidate["branch"] for candidate in candidates]
    tree.append(current_level)
    if __name__ == "__main__":
        print(f"\nLevel 3 Finished Generating Steps")
    
    return tree

def run():
    startTime = time.time() #DEBUG for run time
    if __name__ == "__main__":
        print("Using OpenAI with model: " + model + "\n") #Prints which model was chosen
    
    # Run the tree
    print(f"Numbers: {numbers}") #Prints which 4 numbers were chosen
    tree = build_tree(numbers, b, system_message) #Creates a tree of thought

    if __name__ == "__main__":
        # Prints all final steps (and the paths they took) and tags them as "Solution Found" if they reached 24
        print("\nFinal Results:")
    for branch in tree[-1]:
        final_num = branch["remaining"][0] if branch["remaining"] else None #confirms that the branch didn't glitch and actually has a final result
        # If a branch reached 24, ToT was successful, and the program can stop
        if final_num == 24:
            print("SOLVED")
            print(f"Path: {branch['path']}")
            endTime = time.time() #DEBUG for run time
            print("Execution Time: " + str((endTime - startTime) / 60) + " minutes\n")
            return 1
    print("NO SOLUTION FOUND")
    endTime = time.time() #DEBUG for run time
    print("Execution Time: " + str((endTime - startTime) / 60) + " minutes")
    return 0



###PARAMETERS###
model = "gpt-4o-mini" #LLM model to use (https://platform.openai.com/docs/pricing)
a = 5 #Least number of potential next steps to generate at each tree node
b = 5  #Number of best potential next steps to keep per step
numbers = [10, 48, 2, 4] #The four numbers used in the game of 24



# This only executes if this file is run directly.
#If this file is imported then you must run gameOf24Optimized.run()
if __name__ == "__main__":
    run() #Initiates program

