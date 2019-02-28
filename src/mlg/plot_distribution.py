#! /usr/bin/python3
"""This is a script to plot WER."""

import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import sys
import csv
import os


# Make the graphs a bit prettier
# pd.set_option('display.mpl_style', 'default')
plt.rcParams['figure.figsize'] = (15, 5)
plt.rcParams['font.family'] = 'sans-serif'
grid_linestyle = "--"
grid_linewidth = 0.5
markerstyle = "+"
markersize = 6


def plot_wer(noises, wer):
    """Plot the WER of a single max_iter/code."""
    plt.show()


names = ["bch_n", "bch_info_bits", "bch_fk", "bch_h", "num_sim", "max_iter",
         "num_err", "noise_db", "sigma", "result", "needed_iter"]

if os.path.isfile("hard_mod_raw.csv"):
    hard_df = pd.read_csv("hard_mod_raw.csv", delimiter=" ")
else:
    hard_df = pd.read_csv(glob("*hard_raw.csv")[0],
                          delimiter=" ",
                          header=None,
                          names=names)
    hard_df["needed_iter"].replace(-1, hard_df.max_iter, inplace=True)
    hard_df.to_csv("hard_mod_raw.csv", sep=' ', quotechar='|', index=False)

if os.path.isfile("soft_mod_raw.csv"):
    soft_df = pd.read_csv("soft_mod_raw.csv", delimiter=" ")
else:
    soft_df = pd.read_csv(glob("*soft_raw.csv")[0],
                          delimiter=" ",
                          header=None,
                          names=names)
    soft_df["needed_iter"].replace(-1, soft_df.max_iter, inplace=True)
    soft_df.to_csv("soft_mod_raw.csv", sep=' ', quotechar='|', index=False)

hard_max = hard_df.loc[hard_df.result == 'correct']['num_err'].max()
soft_max = soft_df.loc[soft_df.result == 'correct']['num_err'].max()
print(hard_max)
print(soft_max)

# plt.figure()
# plt.title("Error density over all possible decoding results.")
# hard_df.groupby('result')["num_err"].hist(
#     density=True, histtype="step", linewidth=2)
# plt.xlabel('Number of Errors')
# plt.ylabel('Density')
# plt.legend(("DV", "correct", "wrong"))
# plt.grid(True, which='both',
#          linestyle=grid_linestyle, linewidth=grid_linewidth)

plt.figure()
plt.title("Distribution of reconstruction results over w(e) - Hard")
histo_df = pd.DataFrame(columns=['error_bin', 'result', 'num_err'])
# hard_df.groupby('result')["num_err"].hist(histtype="step", linewidth=2)
for errors in range(hard_df["num_err"].max() + 1):
    num_DV = hard_df.loc[hard_df.result == "DV"].loc[hard_df.num_err == errors].count()["num_err"] / hard_df.count()["num_err"]
    num_correct = hard_df.loc[hard_df.result == "correct"].loc[hard_df.num_err == errors].count()["num_err"] / hard_df.count()["num_err"]
    num_wrong = hard_df.loc[hard_df.result == "wrong"].loc[hard_df.num_err == errors].count()["num_err"] / hard_df.count()["num_err"]
    histo_df = histo_df.append(
        pd.DataFrame({'error_bin': [errors],
                      'result': ["DV"],
                      'num_err': [num_DV]}), ignore_index=True)
    histo_df = histo_df.append(
        pd.DataFrame({'error_bin': [errors],
                      'result': ["correct"],
                      'num_err': [num_correct]}), ignore_index=True)
    histo_df = histo_df.append(
        pd.DataFrame({'error_bin': [errors],
                      'result': ["wrong"],
                      'num_err': [num_wrong]}), ignore_index=True)
histo_df.set_index('error_bin', inplace=True)
histo_df.groupby('result')['num_err'].plot()
plt.xlabel('w(e)')
plt.ylabel('Distribution of Reconstruction results')
plt.legend(("Decoding Failure", "correct", "wrong"))
plt.grid(True, which='both',
         linestyle=grid_linestyle, linewidth=grid_linewidth)

plt.figure()
plt.title("Distribution of reconstruction results over w(e) - Soft")
histo_df = pd.DataFrame(columns=['error_bin', 'result', 'num_err'])
for errors in range(soft_df["num_err"].max() + 1):
    num_DV = soft_df.loc[soft_df.result == "DV"].loc[soft_df.num_err == errors].count()["num_err"] / soft_df.count()["num_err"]
    num_correct = soft_df.loc[soft_df.result == "correct"].loc[soft_df.num_err == errors].count()["num_err"] / soft_df.count()["num_err"]
    num_wrong = soft_df.loc[soft_df.result == "wrong"].loc[soft_df.num_err == errors].count()["num_err"] / soft_df.count()["num_err"]
    histo_df = histo_df.append(
        pd.DataFrame({'error_bin': [errors],
                      'result': ["DV"],
                      'num_err': [num_DV]}), ignore_index=True)
    histo_df = histo_df.append(
        pd.DataFrame({'error_bin': [errors],
                      'result': ["correct"],
                      'num_err': [num_correct]}), ignore_index=True)
    histo_df = histo_df.append(
        pd.DataFrame({'error_bin': [errors],
                      'result': ["wrong"],
                      'num_err': [num_wrong]}), ignore_index=True)
histo_df.set_index('error_bin', inplace=True)
histo_df.groupby('result')['num_err'].plot()
plt.xlabel('w(e)')
plt.ylabel('Distribution of Reconstruction results')
plt.legend(("Decoding Failure", "correct", "wrong"))
plt.grid(True, which='both',
         linestyle=grid_linestyle, linewidth=grid_linewidth)

plt.show()
