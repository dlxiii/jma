### Python 3.5 script for formatting JMA hourly wind csv data downloaded from web
###   and checking missing data
###   e.g., 北北西 => 22.5 (deg)
###   USAGE: $ python jma_wind_hourly.py [sample]
###   Input: sample.csv  Output: sample_r.csv
###   coded on April 7, 2016, by Jun Sasaki (jsasaki@k.u-tokyo.ac.jp)
### !!!!CAUTION: csv file encoding should be UTF-8 !!!!
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import sys
import os

### Read csv input file
fname = "../wind_Chiba2015"  # extension should be "csv"
argvs = sys.argv  # gets command line arguments
if len(argvs) > 1:  # command line argument exists
  fname = argvs[1]  # 1st arguement
if not os.path.isfile(fname + ".csv"): # check whether the csv data exists
  sys.exit("ERROR: No input file.")
wd = {"北": 0.0, "北北東": 22.5, "北東": 45.0, "東北東": 67.5, "東": 90.0,\
                   "東南東": 112.5, "南東": 135.0, "南南東": 157.5, "南": 180.0,\
                   "南南西": 202.5, "南西": 225.0, "西南西": 247.5, "西": 270.0,\
                   "西北西": 292.5, "北西": 315.0, "北北西": 337.5}
names = ["Year", "Month", "Day", "Hour", "wind_spd", "code_spd", "wind_dir", \
         "code_wd", "homo"]
df = pd.read_csv(fname + ".csv", skiprows=6, header=None, names=names)

### check data quality
code = set(df["code_spd"].unique())
if code == {8}: # 8: normal, 1: missing, others: unusual
  print("All data are normal.")
elif code == {1,8}:
  print("There are missing values.")
else:
  print("ERROR: Data are unusual and check them. code = ", code)

wind_dir = [] # wind direction in degree
wind_spd = [] # wind speed in m/s
for n in range(len(df)):
  if df["code_spd"][n] > 1: # data exists
    wind_spd.append(df["wind_spd"][n])
    key = df["wind_dir"][n]  # "東南東" etc.
    if key in wd:   # check whether key exists in dictionary wd
      wind_dir.append(wd[key])
    elif key == "静穏":
      if n > 0:
        wind_dir.append(wind_dir[-1])  # set as the previous one
      else: # n=0
        print("Warning: n = 0 and set as North.")
        wind_dir.append(0.0)  # temporalily set as North
  else: # missing
    print("Missing data at n = ", n)
    if n > 0:
      wind_spd.append(wind_spd[-1])  # set as the previous one
      wind_dir.append(wind_dir[-1])  # set as the previous one
      print("Successfully treated as the previous value at n=", n)
    else: # n=0
      if df["code_spd"][n+1] > 1: # data exists for n=1
        wind_spd.append(df["wind_spd"][n+1])
        key = df["wind_dir"][n+1]  # "東南東" etc.
        if key in wd:   # check whether key exists in dictionary wd
          wind_dir.append(wd[key])
        elif key == "静穏":
          wind_dir.append(0.0)  # temporalily set as North
        print("Successfully treated as North at n=", n)
      else:
        sys.exit("ERROR: Cannot treat because values at n=0 & n=1 are missing.")
df["wind_spd"] = wind_spd
df["wind_dir"] = wind_dir
if df["wind_spd"].count() == len(df) & df["wind_dir"].count() == len(df):
  print("### Congratulations! There are no missing data. ###")
else:
  sys.exit("### ERROR: There must be missing data. Check them! ###")
### output to csv
df.to_csv(fname + "_r.csv", index=None)
