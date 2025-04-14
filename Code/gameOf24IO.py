from openai import OpenAI
import json
import apiKey
import gameOf24Tools
client = OpenAI(api_key=apiKey.apiKey)

def equation(a, op, b):
    return {
        '+': a + b,
        '-': a - b,
        '*': a * b,
        '/': a / b
    }.get(op, "Invalid operator")

def run():
    if __name__ == "__main__":
        print("Using OpenAI with model: " + model + "\n")
    print(f"Numbers: {numbers}")
    
    completion = client.chat.completions.create(
        model=model,
        messages= [
            {"role": "system", "content": "You are an expert in solving game of 24 steps. The game of 24 works like this: You are given four numbers and must make the number 24 from them. You can add or subtract or multiply or divide using all four numbers but use each number only once. At step 1 there are 4 numbers initially which will turn into 3 numbers, step 2 will turn those 3 into 2, and finally step 3 will turn those 2 numbers into 1, which should be 24."},
            {"role": "user", "content": f"Solve the game of 24 for these numbers: {numbers}"}],
        tools=gameOf24Tools.inputOutputTools,
        tool_choice="required"
    )
    
    tool_call = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
    if not all(k in tool_call for k in ["firstEquationFirstNumber", "firstEquationSecondNumber", "firstEquationOperator", "secondEquationFirstNumber", "secondEquationSecondNumber", "secondEquationOperator", "thirdEquationFirstNumber", "thirdEquationSecondNumber", "thirdEquationOperator"]):
        print("NO SOLUTION FOUND")
        return 0
    
    if __name__ == "__main__":
        print(tool_call)
    availableNumbers = numbers

    # First Step
    if tool_call["firstEquationFirstNumber"] not in availableNumbers or tool_call["firstEquationSecondNumber"] not in availableNumbers:
        print("NO SOLUTION FOUND")
        return 0
    if tool_call["firstEquationFirstNumber"] == tool_call["firstEquationSecondNumber"] and availableNumbers.count(tool_call["firstEquationFirstNumber"]) < 2:
        print("NO SOLUTION FOUND")
        return 0
    result = equation(tool_call["firstEquationFirstNumber"], tool_call["firstEquationOperator"], tool_call["firstEquationSecondNumber"])
    if result == "Invalid operator":
        print("NO SOLUTION FOUND")
        return 0
    availableNumbers.append(result)
    availableNumbers.remove(tool_call["firstEquationFirstNumber"])
    availableNumbers.remove(tool_call["firstEquationSecondNumber"])

    # Second Step
    if tool_call["secondEquationFirstNumber"] not in availableNumbers or tool_call["secondEquationSecondNumber"] not in availableNumbers:
        print("NO SOLUTION FOUND")
        return 0
    if tool_call["secondEquationFirstNumber"] == tool_call["secondEquationSecondNumber"] and availableNumbers.count(tool_call["secondEquationFirstNumber"]) < 2:
        print("NO SOLUTION FOUND")
        return 0
    result = equation(tool_call["secondEquationFirstNumber"], tool_call["secondEquationOperator"], tool_call["secondEquationSecondNumber"])
    if result == "Invalid operator":
        print("NO SOLUTION FOUND")
        return 0
    availableNumbers.append(result)
    availableNumbers.remove(tool_call["secondEquationFirstNumber"])
    availableNumbers.remove(tool_call["secondEquationSecondNumber"])

    # Third Step
    if tool_call["thirdEquationFirstNumber"] not in availableNumbers or tool_call["thirdEquationSecondNumber"] not in availableNumbers:
        print("NO SOLUTION FOUND")
        return 0
    if tool_call["thirdEquationFirstNumber"] == tool_call["thirdEquationSecondNumber"] and availableNumbers.count(tool_call["thirdEquationFirstNumber"]) < 2:
        print("NO SOLUTION FOUND")
        return 0
    result = equation(tool_call["thirdEquationFirstNumber"], tool_call["thirdEquationOperator"], tool_call["thirdEquationSecondNumber"])
    if result == "Invalid operator":
        print("NO SOLUTION FOUND")
        return 0
    availableNumbers.append(result)
    availableNumbers.remove(tool_call["thirdEquationFirstNumber"])
    availableNumbers.remove(tool_call["thirdEquationSecondNumber"])

    if availableNumbers[0] != 24:
        print("NO SOLUTION FOUND")
        return 0

    print("SOLVED")
    return 1


numbers = [10, 48, 2, 4]
model = "gpt-4o-mini"
if __name__ == "__main__":
    run()

