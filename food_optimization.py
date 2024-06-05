"""The Stigler diet problem.

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""

# Standard Library imports
from collections import defaultdict

# External imports
from ortools.linear_solver import pywraplp
import pandas as pd

# Local imports
from utils import print_variables, print_constraints
from utils import print_solution
from config import Config
from config import CONSTRAINTS


FoodType = dict[str, float]


config = Config()



def create_data() -> dict[str, FoodType]:
    """ """

    # Load food tables
    df = pd.read_csv(config.DB_PATH, dtype={"NDB_No": str})
    df_custom = pd.read_csv(config.CUSTOM_DB_PATH, dtype={"NDB_No": str})
    extra_info_df = pd.read_csv(config.EXTRA_INFO_PATH, dtype={"NDB_No": str})

    # Filter data of interest from main table
    rows_of_interest = extra_info_df["NDB_No"].to_list()
    df = df[df["NDB_No"].isin(rows_of_interest)]

    # Concatenate main table with custom table
    df = pd.concat([df, df_custom], axis=0)

    # Calculate available carbohydrates
    df["available_carbs_(g)"] = df["Carbohydrt_(g)"] - df["Fiber_TD_(g)"]

    # Add Glycemic Index data
    df = pd.merge(
        df,
        extra_info_df[
            ["NDB_No", "GI", "is_discrete", "min_amount_gr", "max_amount_gr"]
        ],
        on="NDB_No",
        how="left",
    )

    # Calculate Glycemic Load
    df["GL"] = (df["GI"] * df["available_carbs_(g)"]) / 100

    df.fillna(0, inplace=True)

    columns_to_drop = ["Shrt_Desc", "NDB_No", "GmWt_Desc1", "GmWt_Desc2"]
    data = {
        row["Shrt_Desc"]: row.drop(columns_to_drop).to_dict()
        for _, row in df.iterrows()
    }

    return data


def create_variables(solver, data):
    """ """

    variables = {}

    for food_name, food_data in data.items():

        # Create integer variables, used for pills
        if food_data["is_discrete"]:
            variables[food_name] = solver.IntVar(0, 1, food_name)

        # Create float variables
        else:
            min_val = data[food_name]["min_amount_gr"] / 100
            max_val = data[food_name]["max_amount_gr"] / 100
            variables[food_name] = solver.NumVar(min_val, max_val, food_name)

    return variables


def create_constraints(solver, variables, data: dict[str, FoodType], nutrients):
    """ """

    for nutrient_name, (min_val, max_val) in nutrients.items():

        nutrient_constraint = solver.Constraint(min_val, max_val)

        # Set the coefficient of the variable on the constraint.
        # e.g. 2.50 gr of prot per 100 gr of potatoes * gr_potatoes
        #       ^                                             ^
        # nutrients_per_food_unit                         food_var
        for food_name, food_nutrients in data.items():
            food_var = variables[food_name]  # units of food to use
            nutrients_per_food_unit = food_nutrients[nutrient_name]
            nutrient_constraint.SetCoefficient(food_var, nutrients_per_food_unit)


def create_objective(solver, variables, data):
    """ """

    objective = solver.Objective()
    objective.SetMinimization()

    for food_name, food_var in variables.items():
        # Glycemic index
        coefficient = data[food_name]["GL"]
        objective.SetCoefficient(food_var, coefficient)

    return objective


def solve(solver, data: dict[str, FoodType], nutrients):
    """ """

    variables = create_variables(solver, data)
    create_constraints(solver, variables, data, nutrients)
    create_objective(solver, variables, data)

    parameters = pywraplp.MPSolverParameters()
    status = solver.Solve(parameters)

    return status, solver, variables


def get_solution(variables):

    solution = []
    for food_name, food_var in variables.items():
        food_var_value = food_var.solution_value()
        if food_var_value > 0:
            solution.append((food_name, food_var.solution_value()))

    solution.sort(key=lambda x: x[1], reverse=True)

    return solution


def main():
    """ """

    data = create_data()
    solver = pywraplp.Solver.CreateSolver(config.SOLVER_NAME)
    status, solver, variables = solve(solver, data, CONSTRAINTS)

    print_variables(solver, variables)
    print_constraints(solver, CONSTRAINTS)

    if status != solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if status == solver.FEASIBLE:
            print("A feasible solution was found.")
        else:
            print("The solver could not solve the problem.")
            print("Trying to identify the problematic restriction...")

            keys = list(CONSTRAINTS.keys())
            while status != solver.OPTIMAL:
                key = keys.pop()
                if key in CONSTRAINTS:
                    del CONSTRAINTS[key]
                    status, solver, variables = solve(solver, data, CONSTRAINTS)
                if len(CONSTRAINTS.keys()) == 0:
                    raise Exception("Unexpected error, go into the code.")

            print(
                "Optimal solution found after removing constraint '{CONSTRAINTS[key][0]} < {key} < {CONSTRAINTS[key][1]}'"
            )
            exit(0)

    elif status == pywraplp.Solver.OPTIMAL:
        solver.VerifySolution(tolerance=1e-6, log_errors=True)
        print("\nOptimal solution found.")
        print(f"Objective value: {solver.Objective().Value():.2f}\n")

        solution = get_solution(variables)
        print_solution(solution, CONSTRAINTS, data)


if __name__ == "__main__":
    main()
