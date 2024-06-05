"""The Stigler diet problem.

A description of the problem can be found here:
https://en.wikipedia.org/wiki/Stigler_diet.
"""

# Standard Library imports
from collections import defaultdict
from copy import copy

# External imports
from ortools.linear_solver import pywraplp
import pandas as pd


FoodType = dict[str, float]


class FoodOptimization:

    def __init__(
        self,
        solver,
        constraints,
        db_path,
        custom_db_path,
        extra_info_path,
    ):
        self.solver = solver
        self.constraints = copy(constraints)
        self.db_path = db_path
        self.custom_db_path = custom_db_path
        self.extra_info_path = extra_info_path

    def create_data(
        self,
    ) -> dict[str, FoodType]:
        """ """

        # Load food tables
        df = pd.read_csv(self.db_path, dtype={"NDB_No": str})
        df_custom = pd.read_csv(self.custom_db_path, dtype={"NDB_No": str})
        extra_info_df = pd.read_csv(self.extra_info_path, dtype={"NDB_No": str})

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
        self.data = {
            row["Shrt_Desc"]: row.drop(columns_to_drop).to_dict()
            for _, row in df.iterrows()
        }

    def create_variables(self):
        """ """

        self.variables = {}

        for food_name, food_data in self.data.items():

            # Create integer variables, used for pills
            if food_data["is_discrete"]:
                self.variables[food_name] = self.solver.IntVar(0, 1, food_name)

            # Create float variables
            else:
                min_val = self.data[food_name]["min_amount_gr"] / 100
                max_val = self.data[food_name]["max_amount_gr"] / 100
                self.variables[food_name] = self.solver.NumVar(
                    min_val, max_val, food_name
                )

    def create_constraints(
        self,
    ):
        """ """

        for nutrient_name, (min_val, max_val) in self.constraints.items():

            nutrient_constraint = self.solver.Constraint(min_val, max_val)

            # Set the coefficient of the variable on the constraint.
            # e.g. 2.50 gr of prot per 100 gr of potatoes * gr_potatoes
            #       ^                                             ^
            # nutrients_per_food_unit                         food_var
            for food_name, food_nutrients in self.data.items():
                food_var = self.variables[food_name]  # units of food to use
                nutrients_per_food_unit = food_nutrients[nutrient_name]
                nutrient_constraint.SetCoefficient(food_var, nutrients_per_food_unit)

    def create_objective(self):
        """ """

        objective = self.solver.Objective()
        objective.SetMinimization()

        for food_name, food_var in self.variables.items():

            # Glycemic index
            coefficient = self.data[food_name]["GL"]
            objective.SetCoefficient(food_var, coefficient)

        return objective

    def solve(self):
        """ """

        self.create_variables()
        self.create_constraints()
        self.create_objective()

        parameters = pywraplp.MPSolverParameters()
        status = self.solver.Solve(parameters)

        return status

    def get_solution(self):
        """ """

        solution = []
        for food_name, food_var in self.variables.items():
            food_var_value = food_var.solution_value()
            if food_var_value > 0:
                solution.append((food_name, food_var.solution_value()))

        solution.sort(key=lambda x: x[1], reverse=True)

        return solution
