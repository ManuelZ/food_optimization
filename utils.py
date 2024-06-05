from collections import defaultdict


def print_variables(solver, variables):
    """ """
    print("Number of variables:", solver.NumVariables())
    print("Variables:\n")
    for v in variables.keys():
        print(f"  - {v.capitalize()}")
    print()


def print_constraints(solver, constraints):
    """ """
    print("Number of constraints =", solver.NumConstraints())
    print("Constraints: \n")
    for constraint_name, (min_nut, max_nut) in constraints.items():
        print(f"  {min_nut:4} < {constraint_name:<15} < {max_nut:6}")


def print_solution(sorted_solution, constraints, data):
    """ """

    totals = defaultdict(int)
    for food_name, food_var in sorted_solution:

        for k in constraints.keys():
            totals[k] += food_var * data[food_name][k]

        if data[food_name]["is_discrete"]:
            print(f"{food_var:>5.0f} unit of {food_name:<40}")
        else:
            print(f"{food_var*100:5.0f} gr of {food_name:<40}")
