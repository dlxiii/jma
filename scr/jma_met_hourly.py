### Python 3.5 script for JMA hourly meteorological csv data
###   except wind, cloud cover & rainfall downloaded from web
###   for checking missing data
###   USAGE: $ python jma_met_hourly.py [sample]
###   Input: sample.csv  Output: sample_r.csv
###   coded on April 7, 2016, by Jun Sasaki (jsasaki@k.u-tokyo.ac.jp)
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import sys
import os

### Read csv input file
fname = "../atm_pressure_sealevel2015" # extension should be "csv"
argvs = sys.argv  # gets command line arguments
if len(argvs) > 1:  # command line argument exists
  fname = argvs[1]  # 1st arguement
if not os.path.isfile(fname + ".csv"):  # check whether the csv data exists
  sys.exit("ERROR: No input file.")
names = ["Year", "Month", "Day", "Hour", "value", "code", "homo"] # homo:均質番号
df = pd.read_csv(fname + ".csv", skiprows=5, header=None, names=names)

### check data quality
code = set(df["code"].unique())
if code == {8}: # 8: normal, 1: missing, others: unusual
  print("All data are normal.")
elif code == {1,8}:
  print("There are missing values.")
else:
  print("ERROR: Data are unusual and check them. code = ", code)

### check missing value and replace it with previous or next value
value = [] # value
for n in range(len(df)):
  if df["code"][n] > 1: # data exists
    value.append(df["value"][n])
  else: # missing
    print("Missing data at n = ", n)
    if n > 0:
      value.append(value[-1])  # set as the previous one
      print("Successfully treated as the previous value at n=", n)
    else: # n=0
      if df["code"][n+1] > 1: # data exists for n=1
        value.append(df["value"][n+1])
        print("Successfully treated as the next value at n=", n)
      else:
        sys.exit("ERROR: Cannot treat because value at both n=0 & n=1 are missing.")
df["value"] = value

if df["value"].count() == len(df):
  print("### Congratulations! There are no missing data. ###")
else:
  sys.exit("### ERROR: There must be missing data. Check them! ###")
### output to csv
df.to_csv(fname + "_r.csv", index=None)
