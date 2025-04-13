import gameOf24ToT

gameOf24ToT.numbers = [1, 1, 4, 6]


solves = 0
fails = 0
if gameOf24ToT.run():
    solves += 1
    print("Solves +1")
else:
    fails += 1
    print("Fails +1")

solvePercent = solves / (solves + fails)
print(f"\nSolve Percentage = {(solvePercent * 100).2f}%")
