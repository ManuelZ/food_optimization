from dataclasses import dataclass

INFINITY = 999999


@dataclass(frozen=True)
class Config:
    DB_PATH: str = "data/ABBREV.csv"
    CUSTOM_DB_PATH: str = "data/custom_foods.csv"
    EXTRA_INFO_PATH: str = "data/extra_info.csv"
    SOLVER_NAME: str = "SCIP_MIXED_INTEGER_PROGRAMMING"  # 'GLOP'


CONSTRAINTS = {
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
