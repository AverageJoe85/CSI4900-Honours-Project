import gameOf24Optimized

gameOf24Optimized.numbers = [1, 1, 4, 6]


solves = 0
fails = 0
if gameOf24Optimized.run():
    solves += 1
    print("Solves +1")
else:
    fails += 1
    print("Fails +1")

solvePercent = solves / (solves + fails)
print(f"Solve Percentage = %{solvePercent * 100}")
