import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

def scatter(data, x, y, hue=None, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis", xlim=None, ylim=None, remove_outliers=False, threshold = 3):
    """
    Create a scatter plot.

    Parameters:
    - x (str or array-like): The data for the x-axis.
    - y (str or array-like): The data for the y-axis.
    - data (DataFrame, optional): The DataFrame containing the data. Default is None.
    - hue (str, optional): Names of grouping variables in data.
    - title (str, optional): The title of the plot. Default is "Scatter Plot".
    - xlabel (str, optional): The label for the x-axis. Default is "X-axis".
    - ylabel (str, optional): The label for the y-axis. Default is "Y-axis".
    - xlim (tuple, optional): The limits for the x-axis. Default is None.
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - remove_outliers (bool, optional): Whether to remove outliers. Default is False.
    - threshold (float, optional): The threshold for outlier removal. Default is 3.
    """
    
    if remove_outliers:
        
        clean_data=data.copy()
        clean_data[x],clean_data[y]=remove_outliers_from_scatter(clean_data[x],clean_data[y], threshold)
        sns.scatterplot( x=x, y=y, data=clean_data, hue=hue)
        
    else:
        sns.scatterplot( x=x, y=y, data=data, hue=hue)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.show()


def box(data, x, y, labels=None, title="Box Plot", xlabel="Categories", ylabel="Values", ylim=None, log=False):
    """
    Create a box plot.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x,y (str): Names of variables in data.
    - labels (list, optional): The labels for each box. Default is None.
    - title (str, optional): The title of the plot. Default is "Box Plot".
    - xlabel (str, optional): The label for the x-axis. Default is "Categories".
    - ylabel (str, optional): The label for the y-axis. Default is "Values".
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - log (bool): if True, set y to log(y).
    """

    if log:
                 
        log_data=data.copy() 
        log_data[y]=np.log(log_data[y])
        sns.boxplot(data=log_data, x=x, y=y, palette = "tab10")
  
    else: 
        sns.boxplot(data=data, x=x, y=y, palette = "tab10")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=90)
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(ylim)
    plt.show()
    
def violin(data, x, y, labels=None, title="Violin Plot", xlabel="Categories", ylabel="Values", ylim=None, log=False):
    
    """
    Create a violin plot.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x,y (str): Names of variables in data.
    - labels (list, optional): The labels for each box. Default is None.
    - title (str, optional): The title of the plot. Default is "Violin Plot".
    - xlabel (str, optional): The label for the x-axis. Default is "Categories".
    - ylabel (str, optional): The label for the y-axis. Default is "Values".
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - log (bool): if True, set y to log(y).
    """

    if log:
                 
        log_data=data.copy() 
        log_data[y]=np.log(log_data[y])
        sns.violinplot(data=log_data, x=x, y=y, palette = "tab10")
  
    else: 
        sns.violinplot(data=data, x=x, y=y, palette = "tab10")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=90)
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(ylim)
    plt.show()

def line(data, x, y, hue=None, title="Line Plot with Error Bars", xlabel="X-axis", ylabel="Y-axis", remove_outliers=False,threshold = 3, xlim=None, ylim=None):
    """
    Create a line plot with error bars.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x,y (str): Names of variables in data.
    - hue (str, optional): Names of grouping variables in data.
    - title (str, optional): The title of the plot. Default is "Line Plot with Error Bars".
    - xlabel (str, optional): The label for the x-axis. Default is "X-axis".
    - ylabel (str, optional): The label for the y-axis. Default is "Y-axis".
    - error_bars (bool, optional): Whether to include error bars. Default is True.
    - remove_outliers (bool, optional): Whether to remove outliers. Default is False.
    - threshold (float, optional): The threshold for outlier removal. Default is 3.
    - xlim (tuple, optional): The limits for the x-axis. Default is None.
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    """
    if remove_outliers:
        clean_data=data.copy()
        clean_data[x],clean_data[y]=remove_outliers_from_scatter(clean_data[x],clean_data[y], threshold)
        ax = sns.lineplot(data=clean_data, x=x, y=y, hue=hue)
        
    else:
        
        ax = sns.lineplot(data=data, x=x, y=y, hue=hue)
        
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(ylim)
    if xlim:
        plt.xlim(xlim)
    plt.legend()
    plt.show()

    return ax

def histogram(x, data=None, bins='auto', xscale='linear', yscale='linear', title="Histogram",
              xlabel="Values", ylabel="Frequency", xlim=None, ylim=None, remove_outliers=False, threshold=3):
    """
    Create a line plot with error bars.

    Parameters:
    - x (array-like): The data for the x-axis.
    - y (array-like): The data for the y-axis.
    - title (str, optional): The title of the plot. Default is "Line Plot with Error Bars".
    - xlabel (str, optional): The label for the x-axis. Default is "X-axis".
    - ylabel (str, optional): The label for the y-axis. Default is "Y-axis".
    - error_bars (bool, optional): Whether to include error bars. Default is True.
    """

    if data is not None:
        if remove_outliers:
            x = remove_outliers_from_histogram(data[x], threshold)
        else:
            x = data[x]
    else:
        if remove_outliers:
            x = remove_outliers_from_histogram(x, threshold)

    sns.histplot(x, bins=bins, kde=False)
    plt.title(title)
    plt.xscale(xscale)
    plt.yscale(yscale)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.show()

def pie_chart(data, labels, title="Pie Chart",startangle = 0,pctdistance=0.85):
    """
    Create a pie chart.

    Parameters:
    - data (array-like): The data for the pie chart.
    - labels (list): The labels for each wedge.
    - title (str, optional): The title of the plot. Default is "Pie Chart".
    - startangle (float, optional): The starting angle of the pie chart. Default is 0.
    - pctdistance (float, optional): The distance from the center to label the percentages. Default is 0.85.
    """
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=startangle,pctdistance=pctdistance)
    plt.title(title)
    plt.show()

def pair_grid_w_p_values(data, filename):
    """
    Create a PairGrid with scatter plots in the upper triangle, histograms in the diagonal,
    and display p-values for Pearson correlation in the lower triangle.

    Parameters:
    - data (DataFrame): The DataFrame containing the data for the PairGrid.
    - filename (str): Name of the file for the plot
    """
    # Create a PairGrid and map p-values
    g = sns.PairGrid(data)
    g.map_upper(sns.scatterplot)
    g.map_lower(display_pvalue)
    g.map_diag(sns.histplot, color = "green")

    for ax in g.axes.flat:
        ax.xaxis.label.set_size(16)
        ax.yaxis.label.set_size(16)


    # Add a title
    g.fig.suptitle("Scatter Plot Matrix for Music Features", y=1.02)

    # Show the plot
    plt.show()
    
    plt.savefig(filename)

def display_pvalue(x, y, **kwargs):
    """
    Display the p-value for the Pearson correlation between two variables on a scatter plot.

    Parameters:
    - x (array-like): The data for the x-axis.
    - y (array-like): The data for the y-axis.
    - **kwargs: Additional keyword arguments (used by seaborn's mapping functions).
    """
    ax = plt.gca()
    
    # Calculate p-value
    pearson_corr, p_value = pearsonr(x, y)
    corr_str = f"Corr = {pearson_corr:.2f}"
    p_value_str = f"p = {p_value:.4f}"
    
    # Add p-value and correlation coeff to the plot 
    text = f"{corr_str}\n{p_value_str}"
    ax.text(0.5, 0.5, text, transform=ax.transAxes, ha='center', va='center', fontsize=16, color='red')


def remove_outliers_from_scatter(x, y, threshold):
    """
    Remove outliers from scatter plot data.

    Parameters:
    - x (array-like): The data for the x-axis.
    - y (array-like): The data for the y-axis.
    - threshold (float): The threshold for outlier removal.

    Returns:
    - Tuple of arrays: (x, y) with outliers removed corresponding to z-score threshold.
    """
    z_scores = np.abs((x - np.mean(x)) / np.std(x))
    mask_x = z_scores < threshold

    z_scores = np.abs((y - np.mean(y)) / np.std(y))
    mask_y = z_scores < threshold

    combined_mask = np.logical_and(mask_x, mask_y)

    return x[combined_mask], y[combined_mask]

def remove_outliers_from_histogram(data, threshold):
    """
    Remove outliers from histogram data.

    Parameters:
    - data (array-like): The data for the histogram.
    - threshold (float): The threshold for outlier removal.

    Returns:
    - Array: Data with outliers removed, according to z-score threshold.
    """
    z_scores = np.abs((data - np.mean(data)) / np.std(data))
    mask = z_scores < threshold
    
    return data[mask]