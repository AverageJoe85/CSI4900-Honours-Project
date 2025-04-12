###IMPORTS###
from openai import OpenAI
import json
import time
import apiKey
import gameOf24Tools  # Includes nextStepTools and evaluationTools


###FUNCTIONS###
# Function to generate possible next steps given the current numbers and conversation history
def generate_steps(remaining_numbers, message_history):
    steps = [] # store generated steps
    seen_steps = set() # track unique steps to prevent duplicates
    attempts = 0
    max_attempts = 5  # limit to avoid excessive API calls and excessive execution time
    
    while len(steps) < 3: # generate up to 3 unique steps
        completion = client.chat.completions.create(
            model=model,
            messages=message_history + [{"role": "user", "content": f"Input: {remaining_numbers}. Possible next step:"}],
            tools=gameOf24Tools.nextStepTools,
            tool_choice="required"
        )

        assistant_msg = completion.choices[0].message
        for tool_call in assistant_msg.tool_calls:
            step = json.loads(tool_call.function.arguments)

            if not all(k in step for k in ["numberX", "numberY", "operator"]):
                attempts += 1
                continue
        
            # make sure that numbers used in the step exist in the remaining numbers
            if step["numberX"] not in remaining_numbers or step["numberY"] not in remaining_numbers:
                attempts += 1
                continue # skip invalid steps
            
            # create a unique signature to avoid duplicate steps
            step_signature = f"{step['numberX']} {step['operator']} {step['numberY']}"
            if step_signature in seen_steps:
                attempts += 1
                continue # skip already generated steps
            
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
                attempts += 1
                continue 
            
            step["numberZ"] = result # store result
            
            # Simulate tool response for evaluation
            tool_response = {
                "role": "tool",
                "content": json.dumps({"numberZ": result}),
                "tool_call_id": tool_call.id
            }
            step_history = message_history + [assistant_msg, tool_response] # update history
            steps.append({"step": step, "history": step_history})
            #seen_steps.add(step_signature) # mark step as seen
            attempts += 1
    
    return steps

# Function to evaluate the potential of a step leading to 24
def evaluate_step(step, path, remaining):
    eval_history = [
        system_message,
        {"role": "user", "content": f"Given the path so far: {path}, and remaining numbers: {remaining}, evaluate this step: {step['numberX']} {step['operator']} {step['numberY']} = {step['numberZ']}. How likely can it lead to 24? Consider if the result is too big or too small to reach 24 with the remaining numbers."}
    ]
    completion = client.chat.completions.create(
        model=model,
        messages=eval_history,
        tools=gameOf24Tools.evaluationTools,
        tool_choice="required"
    )
    assistant_msg = completion.choices[0].message
    tool_call = assistant_msg.tool_calls[0]
    score = json.loads(tool_call.function.arguments)["stepPotential"] # extract evaluation scoree
    
    tool_response = {
        "role": "tool",
        "content": json.dumps({"stepPotential": score}),
        "tool_call_id": tool_call.id
    }
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
def build_tree(initial_numbers):
    tree = []
    current_level = [{"remaining": initial_numbers, "history": [system_message], "path": []}]
    b = 5  # Keep top 5 branches per level
    
    for level in range(3): # three levels to reah a single number
        candidates = []
        expected_remaining_count = 4 - (level + 1)
        
        # Generate all possible steps for the current level
        for branch in current_level:
            if len(branch["remaining"]) <= 1:
                candidates.append({
                    "branch": branch,
                    "score": branch.get("score", 0),
                    "proximity": 0  # default for branches already at 1 number
                })
                continue
            
            steps = generate_steps(branch["remaining"], branch["history"])
            for step_data in steps:
                step = step_data["step"]
                remaining = calculate_remaining_numbers(branch["remaining"], step)
                if len(remaining) != expected_remaining_count:
                    continue
                
                new_path = branch["path"] + [f"{step['numberX']} {step['operator']} {step['numberY']} = {step['numberZ']}"]
                score = evaluate_step(step, new_path, remaining)
                
                if score == 0:  # get rid of impossible steps
                    continue
                
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
        
        print(f"\nLevel {level + 1}:")
        for branch in current_level:
            print(f"Path: {branch['path']}, Remaining: {branch['remaining']}, Score: {branch['score']}")
    
    return tree



###MAIN###
model = "gpt-4o-mini"
print("Using OpenAI with model: " + model + "\n")
client = OpenAI(api_key=apiKey.apiKey)

startTime = time.time()

system_message = {
    "role": "system",
    "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24."
}
# Run the tree
initial_numbers = [17, 4, 1, 2]
initial_numbers = [10, 48, 2, 4]
print(f"Starting with numbers: {initial_numbers}")
tree = build_tree(initial_numbers)

print("\nFinal Results:")
for branch in tree[-1]:
    final_num = branch["remaining"][0] if branch["remaining"] else None
    print(f"Path: {branch['path']}, Final Number: {final_num}, Score: {branch['score']}")
    if final_num == 24:
        print("Solution found")

endTime = time.time()
print("\nExecution Time: " + str(endTime - startTime) + " seconds, or " + str((endTime - startTime) / 60) + " minutes")
