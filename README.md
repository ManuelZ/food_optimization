# My customized or-tools solution for the Stigler diet problem.

Linear optimization problem to find a subset of foods that meet desired ranges for calories, proteins, fats, carbohydrates, and micronutrients, while minimizing the glycemic load.

## Usage

To run the script:

```
python main.py
```

## Requirements

Depends on or-tools and Pandas.

## Output:

```
Number of variables: 49
Variables:

  - Cheese,cottage,lowfat,1% milkfat
  - Egg,whl,ckd,hard-boiled
  - Egg,whl,ckd,scrmbld
  - Chicken,broilers or fryers,breast,meat only,ckd,rstd
  - Cereals,oats,reg & quick,not fort,dry
  - Apples,raw,with skin
  - Avocados,raw,all comm var
  - Bananas,raw
  - Kiwifruit,grn,raw
  - Tangerines,(mandarin oranges),raw
  - Prickly pears,raw
  - Watermelon,raw
  - Beans,snap,grn,ckd,bld,drnd,wo/salt
  - Carrots,raw
  - Onions,raw
  - Peas,grn,ckd,bld,drnd,wo/salt
  - Potatoes,bkd,skn,wo/salt
  - Sweet potato,ckd,bld,wo/ skn
  - Tomatoes,red,ripe,raw,year rnd average
  - Peppers,swt,red,ckd,bld,drnd,wo/salt
  - Spinach,ckd,bld,drnd,w/salt
  - Mushrooms,white,microwaved
  - Chia seeds,dried
  - Pumpkin&squash sd krnls,rstd,wo/salt
  - Cashew nuts,dry rstd,wo/salt
  - Almonds,dry rstd,w/salt
  - Tuna,lt,cnd in oil,drnd sol
  - Beans,baked,home prepared
  - Chickpeas ,mature seeds,ckd,bld,wo/salt
  - Lentils,mature seeds,ckd,bld,wo/salt
  - Peas,split,mature seeds,ckd,bld,wo/salt
  - Peanuts,all types,dry-roasted,w/salt
  - Amaranth grain,ckd
  - Rice,brown,medium-grain,ckd
  - Quinoa,ckd
  - Pasta,ckd,enr,w/ added salt
  - Beef,loin,tenderloin rst,bnless,l & f,0" fat,choic,ckd,rstd
  - Beef,ground,90% ln meat / 10% fat,raw
  - Tarwi
  - Optimum nutrition, gold standard, 100% whey, cookies & cream
  - Salt
  - Sunvit calcium citrate (1 tablet)
  - Vitamin e (1 pill)
  - Pan bimbo integral "vital"
  - Maca gelatinizada
  - Nutrex, isofit whey isolate, cookies & cream
  - Vitamin c (1/4 pill)
  - Vitamin d (1 pill)
  - Isopure protein powder, zero carb, creamy vanilla

Number of constraints = 30
Constraints:

  3000 < Energ_Kcal      <   3100
   152 < Protein_(g)     <    160
   358 < available_carbs_(g) <    400
    76 < Lipid_Tot_(g)   <     86
   1.2 < Thiamin_(mg)    < 999999
   1.3 < Riboflavin_(mg) < 999999
    16 < Niacin_(mg)     <     35
     5 < Panto_Acid_mg)  < 999999
   1.3 < Vit_B6_(mg)     <    100
   2.4 < Vit_B12_(µg)    < 999999
   400 < Folate_Tot_(µg) <   1000
  3000 < Vit_A_IU        <  10000
    90 < Vit_C_(mg)      <   2000
   600 < Vit_D_IU        <   4000
    15 < Vit_E_(mg)      <   1000
   120 < Vit_K_(µg)      < 999999
  1000 < Calcium_(mg)    <   2500
   0.9 < Copper_mg)      <     10
     8 < Iron_(mg)       <     45
   420 < Magnesium_(mg)  < 999999
   2.3 < Manganese_(mg)  <     11
   700 < Phosphorus_(mg) <   4000
  3400 < Potassium_(mg)  < 999999
    55 < Selenium_(µg)   <    400
  1500 < Sodium_(mg)     <   2300
    11 < Zinc_(mg)       <     40
    38 < Fiber_TD_(g)    <     80
     0 < Cholestrl_(mg)  <    300
     0 < FA_Sat_(g)      <     12
     0 < Sugar_Tot_(g)   <    100

Optimal solution found.
Objective value: 170.41

  350 gr of QUINOA,CKD
  300 gr of TANGERINES,(MANDARIN ORANGES),RAW
  263 gr of PRICKLY PEARS,RAW
  214 gr of BANANAS,RAW
  214 gr of PASTA,CKD,ENR,W/ ADDED SALT
  150 gr of CHICKPEAS ,MATURE SEEDS,CKD,BLD,WO/SALT
  150 gr of PEAS,SPLIT,MATURE SEEDS,CKD,BLD,WO/SALT
  120 gr of ONIONS,RAW
  100 gr of TUNA,LT,CND IN OIL,DRND SOL
    1 unit of Sunvit Calcium Citrate (1 tablet)
    1 unit of Vitamin E (1 pill)
    1 unit of Vitamin C (1/4 pill)
    1 unit of Vitamin D (1 pill)
   80 gr of CEREALS,OATS,REG & QUICK,NOT FORT,DRY
   44 gr of LENTILS,MATURE SEEDS,CKD,BLD,WO/SALT
   44 gr of PEANUTS,ALL TYPES,DRY-ROASTED,W/SALT
   41 gr of Optimum Nutrition, Gold Standard, 100% Whey, Cookies & Cream
   39 gr of CARROTS,RAW
   27 gr of CASHEW NUTS,DRY RSTD,WO/SALT
   20 gr of ALMONDS,DRY RSTD,W/SALT
   15 gr of Maca Gelatinizada
    9 gr of SPINACH,CKD,BLD,DRND,W/SALT
    2 gr of Isopure Protein Powder, Zero Carb, Creamy Vanilla
    1 gr of Salt
```
