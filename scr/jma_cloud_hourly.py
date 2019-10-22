### Python 3.5 script for JMA hourly cloud cover csv data downloaded from web
###   for reformatting and checking missing data
###   cloud cover varies from 0 to 10
###   0+ => 0.2  10- => 9.8 (assumption)
###   USAGE: $ python jma_cloud_hourly.py [sample]
###   Input: sample.csv  Output: sample_r.csv
###   coded on April 7, 2016, by Jun Sasaki (jsasaki@k.u-tokyo.ac.jp)
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import sys
import os

### Read csv input file
fname = "../cloud_cover_Tokyo2015" # extension should be "csv"
argvs = sys.argv  # gets command line arguments
if len(argvs) > 1:  # command line argument exists
  fname = argvs[1]  # 1st arguement
if not os.path.isfile(fname + ".csv"):  # check whether the csv data exists
  sys.exit("ERROR: No input file.")
names = ["Year", "Month", "Day", "Hour", "value", "code", "homo"] # homo:均質番号
df = pd.read_csv(fname + ".csv", skiprows=5, header=None, names=names)

### check missing value and replace it
value = [] # value
nval = [n for n in range(len(df)) if df["code"][n] > 2] # list of index of existing data
for n in range(nval[0]):  # special treatmet at the head of data
  value.append(df["value"][nval[0]])

for i in range(len(nval)-1):  # treatment except at the beginning and the last
  for n in range(nval[i], nval[i+1]):
    value.append(df["value"][nval[i]])

for n in range(nval[-1], len(df)):  # special treatment at the last of data
    value.append(df["value"][nval[-1]])

### replace "10-" and "0+" with some float values
for n in range(len(df)):
  if value[n] == "10-":
    value[n] = 9.8        ### assumed
  elif value[n] == "0+":
    value[n] = 0.2        ### assumed

df["value"] = np.array(value)

if df["value"].count() == len(df):
  print("### Congratulations! There are no missing data. ###")
else:
  sys.exit("### ERROR: There must be missing data. Check them! ###")
### output to csv
df.to_csv(fname + "_r.csv", index=None)
