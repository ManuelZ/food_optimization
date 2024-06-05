# External imports
from ortools.linear_solver import pywraplp

# Local imports
from utils import print_variables, print_constraints
from utils import print_solution

from config import CONSTRAINTS
from food_optimization import FoodOptimization
from config import Config

config = Config()


def main():
    """ """

    solver = pywraplp.Solver.CreateSolver(config.SOLVER_NAME)
    optim = FoodOptimization(
        solver,
        constraints=CONSTRAINTS,
        db_path=config.DB_PATH,
        custom_db_path=config.CUSTOM_DB_PATH,
        extra_info_path=config.EXTRA_INFO_PATH,
    )

    status = optim.solve()

    print_variables(solver, optim.variables)
    print_constraints(solver, optim.constraints)

    if status != solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if status == solver.FEASIBLE:
            print("A feasible solution was found.")
        else:
            print("The solver could not solve the problem.")
            print("Trying to identify the problematic restriction...")

            keys = list(optim.constraints.keys())
            while status != solver.OPTIMAL:
                key = keys.pop()
                if key in optim.constraints:
                    del optim.constraints[key]
                    status = optim.solve()
                if len(optim.constraints.keys()) == 0:
                    raise Exception("Unexpected error, go into the code.")

            print(
                "Optimal solution found after removing constraint '{optim.constraints[key][0]} < {key} < {optim.constraints[key][1]}'"
            )
            exit(0)

    elif status == pywraplp.Solver.OPTIMAL:
        solver.VerifySolution(tolerance=1e-6, log_errors=True)
        print("\nOptimal solution found.")
        print(f"Objective value: {solver.Objective().Value():.2f}\n")

        solution = optim.get_solution()
        print_solution(solution, optim.constraints, optim.data)


if __name__ == "__main__":
    main()
