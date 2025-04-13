import gameOf24ToT
import examples

solves = 0
fails = 0

for numbers in examples.examples:
    gameOf24ToT.numbers = numbers
    if gameOf24ToT.run():
        solves += 1
        print("Solves +1")
    else:
        fails += 1
        print("Fails +1")

solvePercent = solves / (solves + fails)
print(f"\nSolve Percentage = {(solvePercent * 100):.2f}%")
