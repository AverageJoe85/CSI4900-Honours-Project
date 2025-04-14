import gameOf24ToT
import examples

def run(start,end):
    solves = 0
    fails = 0
    for numbers in examples.examples[start-1:end-1]:
        gameOf24ToT.numbers = numbers
        if gameOf24ToT.run():
            solves += 1
            print("Solves +1")
        else:
            fails += 1
            print("Fails +1")
    solvePercent = solves / (solves + fails)
    print(f"\nSolve Percentage = {(solvePercent * 100):.2f}%\n")

##run(901,911)
run(911,921)
##run(921,931)
##run(931,941)
##run(941,951)
##run(951,961)
##run(961,971)
##run(971,981)
##run(981,991)
##run(991,1001)
