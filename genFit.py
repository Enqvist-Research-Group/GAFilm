#!/usr/bin/python
# genFit.py
# Code for building gafchromic film dose-darkness calibration curve
# (C) Brice Turner, 2023

import argparse
import importlib.util
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import tifffile as tiff
import time

# BEGIN: IMPORT DATA #########################################################
desc = f'Command line interface for {os.path.basename(__file__)}.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-id', '--INPUTDIR', dest='inputdir', required=True,
                    help='Input directory name. REQUIRED.\n'
                        'Usage: -i/--INPUT <./local/path/to/dir>')
parser.add_argument('-rf', '--REFFILM', dest='refile', required=True,
                    help='Reference film file. REQUIRED. \n'
                         'Usage: -r/--REF <./local/path/to/filename>.tif')

args = parser.parse_args()

# Get the file path and the file name without the extension
infile_path = os.path.abspath(os.path.normpath(args.inputdir))
# Make sure the input file exists
if not os.path.isdir(infile_path):
    raise FileNotFoundError(f"Dir '{args.inputdir}' not found")

refile_path = os.path.abspath(os.path.normpath(args.refile))
refile_name = os.path.splitext(os.path.basename(args.refile))[0]
# Make sure the input file exists
if not os.path.isfile(refile_path):
    raise FileNotFoundError(f"File '{args.refile}' not found")
# END:   IMPORT DATA #########################################################



# BEGIN: MAKE DATAFRAME OF IMAGE V. transparency #############################
transparency_avg_tot = []
for file in os.listdir(infile_path):
    file_path = os.path.join(infile_path, file)
    img_my = tiff.imread(file_path)
    transparency_avg_film = np.mean(img_my)
    transparency_avg_tot.append(transparency_avg_film)
    print(file)
print(transparency_avg_tot)

img_ref = tiff.imread(refile_path)
transparency_avg_ref = np.mean(img_my)
print(refile_name)
print(transparency_avg_ref)
# END:   MAKE DATAFRAME OF IMAGE V. transparency #############################



# BEGIN: CREATE CURVE ########################################################
# x = transparency_avg_tot['transparency_avg']
# y = transparency_avg_tot['dose (Gy)']

# I_0 = 53184.541394 # hardcoded ./reference_HD/230506_reference_HD_shiny.tif
I_0  = transparency_avg_ref 

x = [50,
     100,
     100,
     200,
     200]

y = [48245.67397/I_0,
    38092.03514/I_0,
    51019.6743/I_0,
    27027.30594/I_0,
    40113.27465/I_0]

x_shands = [50, 100, 200]
y_shands = [48245.67397/I_0,
            38092.03514/I_0,
            27027.30594/I_0]

x_Co = [100,200]
y_Co = [51019.674296/I_0,
        40113.27465/I_0]


curve_order = 1 # order (polynomial) of curve
coeffs = np.polyfit(x,y,curve_order)
print(coeffs)
p = np.poly1d(coeffs)
# formula = f"{p[0]:.2f}x^5 + {p[1]:.2f}x^4 + {p[2]:.2f}x^3 + {p[3]:.2f}x^2 + {p[4]:.2f}x + {p[5]:.2f}"


plt.plot(x_shands, y_shands, drawstyle = 'steps-post', label = 'shands calibrated')
plt.plot(x_Co, y_Co, drawstyle = 'steps-post', label = 'Co-60 calibrated')
plt.plot(x, p(x), linestyle = 'dashed', label = 'best fit' ) # , drawstyle = 'default')
plt.legend()
plt.xlabel('Dose (Gy)')
plt.ylabel('Transparency ratio (arb. unit)')

timestr = time.strftime('%Y%m%d_%H%M%S')
filename = f'plot_{timestr}.png'
dir_output = os.path.join(os.getcwd(), 'outputs_genFit')
if not os.path.exists(dir_output):
    os.makedirs(dir_output)
fp_plot = os.path.join(dir_output, filename)
fig = plt.gcf()
fig.savefig(fp_plot, dpi=600)

filename_best_fit = f'best_fit_constants_{timestr}.txt'
fp_best_fit = os.path.join(dir_output, filename_best_fit)
with open(fp_best_fit, "w") as f:
    f.write(str(coeffs))

plt.show()
# END:   CREATE CURVE ########################################################

