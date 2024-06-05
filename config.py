from dataclasses import dataclass


@dataclass
class Config:
    DB_PATH: str = "data/ABBREV.csv"
    CUSTOM_DB_PATH: str = "data/custom_foods.csv"
    EXTRA_INFO_PATH: str = "data/extra_info.csv"
    SOLVER_NAME: str = "SCIP_MIXED_INTEGER_PROGRAMMING"  # 'GLOP'
    INFINITY: int = 999999
    N_DECISION_VARS_PER_FOOD: int = 4
