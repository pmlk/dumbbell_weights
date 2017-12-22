# Dumbbell Weights

This program helps you figure out which configurations of weights you can use with your dumbbells.

## Usage
Execute `python3 main.py inventory` to save a `.json`-file that stores information about the available weights you own.

Execute `python3 main.py config` to get a list of total weight configurations available with your set of weights.

## Example
```
python3 main.py config

possible total weights:
*  2.0 kg
   4.0 kg
*  4.5 kg
   6.0 kg
   6.5 kg
*  7.0 kg
*  8.0 kg
  [...]
  24.0 kg
choose total weight:
```

An asterix indicates that this weight can be configured at least twice.

After choosing your weight you will be able to select a total weight again until there are no more weights to choose from. 
Once there are no more weights to choose from you will be presented with the configurations for each dumbbell. 
You can also enter any non-number to stop the selection process.

```
selected weights:
[24.0, 18.0, 13.5, 4.0, 4.5]

weight combos:
 4.5 kg: [1.25]
 4.0 kg: [1.0]
13.5 kg: [2.5, 2.0, 1.25]
18.0 kg: [3.0, 2.5, 2.5]
24.0 kg: [5.0, 3.0, 3.0]
```

## Assumptions
* each empty dumbbell weighs 2 kg
* there are an infinite number of empty dumbbells
