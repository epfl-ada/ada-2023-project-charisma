import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def scatter(x, y, data=None, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis", xlim=None, ylim=None, remove_outliers=False, threshold = 3):
    if remove_outliers:
        if data is not None:
            x,y = remove_outliers_from_scatter(data[x], data[y],threshold)
        else:
            x, y = remove_outliers_from_scatter(x, y,threshold)
    sns.scatterplot(x=x, y=y, data=data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.show()

def box(data, labels=None, title="Box Plot", xlabel="Categories", ylabel="Values", ylim=None):
    sns.boxplot(data=data)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(ylim)
    plt.show()

def line(x, y, title="Line Plot with Error Bars", xlabel="X-axis", ylabel="Y-axis", error_bars=True):
    ax = sns.lineplot(x, y, label='Data with Error Bars')
    if error_bars:
        ax.errorbar(x, y, yerr=error_bars, fmt='o', capsize=5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def histogram(data, bins = 'auto', title="Histogram", xlabel="Values", ylabel="Frequency", xlim=None, ylim=None, remove_outliers = False, threshold = 3):
    if remove_outliers:
        data = remove_outliers_from_histogram(data, threshold)
    sns.histplot(data, bins, kde=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.show()

def remove_outliers_from_scatter(x, y, threshold):
    z_scores = np.abs((x - np.mean(x)) / np.std(x))
    mask_x = z_scores < threshold

    z_scores = np.abs((y - np.mean(y)) / np.std(y))
    mask_y = z_scores < threshold

    combined_mask = np.logical_and(mask_x, mask_y)
    return x[combined_mask], y[combined_mask]

def remove_outliers_from_histogram(data, threshold):
    z_scores = np.abs((data - np.mean(data)) / np.std(data))
    mask = z_scores < threshold
    return data[mask]
