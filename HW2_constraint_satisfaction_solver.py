from constraint import *

def sum_constraint_1(s, i, n, c, e, j, u, l, a, r):
        if (s*10000 + i*1000 + n*100 + c*10 + e) + (j*100000 + u*10000 + l*1000 + i*100 + u*10 + s) == (c*100000 + a*10000 + e*1000 + s*100 + a*10 + r):
            return True

def sum_constraint_2(c, h, e, k, t, i, r, s):
        if (c*10000 + h*1000 + e*100 + c*10 + k) + (t*100 + h*10 + e) == (t*10000 + i*1000 + r*100 + e*10 + s):
            return True

def sum_constraint_3(d, o, y, u, f, e, l, c, k):
        if (d*10 + o) + (y*100 + o*10 + u) + (f*1000 + e*100 + e*10 + l) == (l*10000 + u*1000 + c*100 + k*10 + y):
            return True

def puzzle_1():
    # SINCE + JULIUS = CAESAR
    problem = Problem()
    problem.addVariables("SJC", range(1, 10))
    problem.addVariables("INEULAR", range(10))


    problem.addConstraint(sum_constraint_1, "SINCEJULAR")
    problem.addConstraint(AllDifferentConstraint())

    solutions = problem.getSolutions()

    print("Number of solutions found: {}\n".format(len(solutions)))

    for s in solutions:
        print("S = {}, I = {}, N = {}, C = {}, E = {}, J = {}, U = {}, L = {}, A = {}, R = {}"
            .format(s['S'], s['I'], s['N'], s['C'], s['E'], s['J'], s['U'], s['L'], s['A'], s['R']))

def puzzle_2():
    # CHECK + THE = TIRES
    problem = Problem()
    problem.addVariables("CT", range(1, 10))
    problem.addVariables("HEKIRS", range(10))


    problem.addConstraint(sum_constraint_2, "CHEKTIRS")
    problem.addConstraint(AllDifferentConstraint())

    solutions = problem.getSolutions()
    
    print("Number of solutions found: {}\n".format(len(solutions)))

    for s in solutions:
        print("C = {}, H = {}, E = {}, K = {}, T = {}, I = {}, R = {}, S = {}"
            .format(s['C'], s['H'], s['E'], s['K'], s['T'], s['I'], s['R'], s['S']))

def puzzle_3():
    # DO + YOU + FEEL = LUCKY
    problem = Problem()
    problem.addVariables("DYFL", range(1, 10))
    problem.addVariables("OUECK", range(10))


    problem.addConstraint(sum_constraint_3, "DOYUFELCK")
    problem.addConstraint(AllDifferentConstraint())

    solutions = problem.getSolutions()
    
    print("Number of solutions found: {}\n".format(len(solutions)))

    for s in solutions:
        print("D = {}, O = {}, Y = {}, U = {}, F = {}, E = {}, L = {}, C = {}, K = {}"
            .format(s['D'], s['O'], s['Y'], s['U'], s['F'], s['E'], s['L'], s['C'], s['K']))

def main():
    # SINCE + JULIUS = CAESAR
    puzzle_1()
    
    # CHECK + THE = TIRES
    puzzle_2()

    # DO + YOU + FEEL = LUCKY
    puzzle_3()


if __name__ == "__main__":
    main()