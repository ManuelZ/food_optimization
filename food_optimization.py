"""The Stigler diet problem.

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""

from ortools.linear_solver import pywraplp
import pandas as pd
from collections import defaultdict

DB_PATH = "ABBREV.csv"
CUSTOM_DB_PATH = "custom_foods.csv"
EXTRA_INFO_PATH = "extra_info.csv"
INFINITY = 999999

nutrients = {
    # Macro-nutrients
    "Energ_Kcal": [3000, 3100],
    "Protein_(g)": [152, 160],
    "available_carbs_(g)": [358, 400],  # Custom: total carbs minus fiber
    "Lipid_Tot_(g)": [76, 86],
    # Vitamins
    "Thiamin_(mg)": [1.2, INFINITY],  # vit B1
    "Riboflavin_(mg)": [1.3, INFINITY],  # vit B2
    "Niacin_(mg)": [16, 35],  # vit B3
    "Panto_Acid_mg)": [5, INFINITY],  # vit B5
    "Vit_B6_(mg)": [1.3, 100],  # vit b6
    "Vit_B12_(µg)": [2.4, INFINITY],
    "Folate_Tot_(µg)": [400, 1000],
    "Vit_A_IU": [
        3000,
        10000,
    ],  # UL: https://www.hsph.harvard.edu/nutritionsource/vitamin-a/
    "Vit_C_(mg)": [90, 2000],
    "Vit_D_IU": [600, 4000],
    "Vit_E_(mg)": [15, 1000],
    "Vit_K_(µg)": [120, INFINITY],
    # Minerals
    "Calcium_(mg)": [1000, 2500],
    "Copper_mg)": [0.9, 10],
    "Iron_(mg)": [8, 45],
    "Magnesium_(mg)": [420, INFINITY],
    "Manganese_(mg)": [2.3, 11],
    "Phosphorus_(mg)": [700, 4000],
    "Potassium_(mg)": [3400, INFINITY],
    "Selenium_(µg)": [55, 400],
    "Sodium_(mg)": [1500, 2300],
    "Zinc_(mg)": [11, 40],
    # Extras
    "Fiber_TD_(g)": [38, 80],  # custom UL
    "Cholestrl_(mg)": [0, 300],
    "FA_Sat_(g)": [0, 12],
    "Sugar_Tot_(g)": [0, 100],
}


def create_data():
    """ """

    df = pd.read_csv(DB_PATH, dtype={"NDB_No": str})
    df_custom = pd.read_csv(CUSTOM_DB_PATH, dtype={"NDB_No": str})
    extra_info_df = pd.read_csv(EXTRA_INFO_PATH, dtype={"NDB_No": str})

    # Filter raw data
    rows_of_interest = extra_info_df["NDB_No"].to_list()
    df = df[df["NDB_No"].isin(rows_of_interest)]

    df = pd.concat([df, df_custom], axis=0)

    # Calculate "available_carbohydrate" column
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

    data = {
        row["Shrt_Desc"]: row.drop("Shrt_Desc").to_dict() for _, row in df.iterrows()
    }

    return data


def create_variables(solver, data, log=True):
    """ """

    # Create binary decision variables, https://or.stackexchange.com/a/7553
    decision_variables = defaultdict(dict)

    variables = {}
    for food_name, food_data in data.items():

        # Set Integer variables
        if food_data["is_discrete"]:
            variables[food_name] = solver.IntVar(0.0, 1, food_name)

        # Set float variables
        else:
            min_val = data[food_name]["min_amount_gr"] / 100
            max_val = data[food_name]["max_amount_gr"] / 100
            variables[food_name] = solver.NumVar(min_val, max_val, food_name)

        # Create binary decision variables, https://or.stackexchange.com/a/7553
        GROUPS = range(4)
        for group in GROUPS:
            var_name = f"{food_name}_g_{group}"
            decision_variables[food_name][group] = solver.IntVar(0, 1, var_name)

    if log:
        print("Number of variables:", solver.NumVariables())
        print("Variables (one unit represents 100 gr of food):\n")
        for v in variables.keys():
            print(f"  - {v.capitalize()}")
        print()

    return variables, decision_variables


def set_constraints(solver, variables, data, nutrients, log=True):
    """ """

    for nutrient_name, (nutrient_min, nutrient_max) in nutrients.items():

        nutrient_constraint = solver.Constraint(nutrient_min, nutrient_max)

        for item_name, item_nutrients in data.items():
            nutrients_in_one_food = item_nutrients[nutrient_name]
            food_var_qty = variables[item_name]
            # In this loop, the constraint will receive a new variable and coefficient
            # e.g. 0.83 [gr prot per 100 gr papa] * num_100_gr_papas
            nutrient_constraint.SetCoefficient(food_var_qty, nutrients_in_one_food)

    if log:
        print("Number of constraints =", solver.NumConstraints())
        print("Constraints: \n")
        for constraint_name, (min_nut, max_nut) in nutrients.items():
            print(f"  {min_nut:4} < {constraint_name:<15} < {max_nut:6}")


def create_objective(solver, variables, data):
    """ """

    objective = solver.Objective()

    for food_name, food_var in variables.items():
        # Glycemic index
        coefficient = data[food_name]["GL"]
        objective.SetCoefficient(food_var, coefficient)

    return objective


def solve(data, nutrients, log=True):
    """ """

    if not solver:
        return

    # Create binary decision variables, https://or.stackexchange.com/a/7553
    variables, decision_variables = create_variables(solver, data, log)
    for food_name, food_group_variables in decision_variables.items():
        group_constraint = solver.Constraint(0, 1)
        for group, group_var in food_group_variables.items():
            group_constraint.SetCoefficient(group_var, 1)

    set_constraints(solver, variables, data, nutrients, log)

    objective = create_objective(solver, variables, data)
    objective.SetMinimization()

    parameters = pywraplp.MPSolverParameters()
    status = solver.Solve(parameters)

    return status, solver, variables, decision_variables


def main():

    data = create_data()
    status, solver, variables, decision_variables = solve(data, nutrients)

    if status != solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if status == solver.FEASIBLE:
            print("A potentially suboptimal solution was found.")
        else:
            print("The solver could not solve the problem.")
            print("Trying to identify the problematic restriction")
            keys = list(nutrients.keys())
            while status != solver.OPTIMAL:
                key = keys.pop()
                if key in nutrients:
                    del nutrients[key]
                    status, solver, variables = solve(data, nutrients, log=False)
                if len(nutrients.keys()) == 0:
                    print("CHECK THIS ERROR")
                    exit(1)
            print("SOLUTION FOUND after removing constraint ", key)
            exit(0)

    elif status == pywraplp.Solver.OPTIMAL:
        solver.VerifySolution(tolerance=1e-6, log_errors=True)
        print("\nOptimal solution found.")
        print(f"Objective value: {solver.Objective().Value():.2f}\n")

        totals = defaultdict(int)

        sorted_solution = [
            (food_name, food_var.solution_value())
            for food_name, food_var in variables.items()
        ]
        sorted_solution.sort(key=lambda x: x[1], reverse=True)

        for food_name, food_amount in sorted_solution:
            if food_amount > 0:

                for k in nutrients:
                    totals[k] += food_amount * data[food_name][k]

                # Print variables
                if data[food_name]["is_discrete"]:
                    print(f"{food_amount:>6.0f} unit of {food_name:<40}")
                else:
                    if food_amount * 100 < 5:
                        continue
                    print(f"{food_amount*100:8.0f} gr of {food_name:<40}")

        selected_foods = [
            (food_name, food_var.solution_value())
            for food_name, food_var in variables.items()
            if food_var.solution_value() > 0
        ]


if __name__ == "__main__":
    main()
