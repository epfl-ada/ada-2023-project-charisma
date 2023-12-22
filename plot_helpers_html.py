import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
import plotly.express as px
from slugify import slugify
import pandas as pd
import os
import mplcursors
import mpld3

def scatter_html(data, x, y, hue=None, title="Scatter Plot", xlabel="X-axis", ylabel="Y-axis", xlim=None, ylim=None, remove_outliers=False, threshold=3, filename=None):
    """
    Create a scatter plot using Plotly Express.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x (str or array-like): The data for the x-axis.
    - y (str or array-like): The data for the y-axis.
    - hue (str, optional): Names of grouping variables in data.
    - title (str, optional): The title of the plot. Default is "Scatter Plot".
    - xlabel (str, optional): The label for the x-axis. Default is "X-axis".
    - ylabel (str, optional): The label for the y-axis. Default is "Y-axis".
    - xlim (tuple, optional): The limits for the x-axis. Default is None.
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - remove_outliers (bool, optional): Whether to remove outliers. Default is False.
    - threshold (float, optional): The threshold for outlier removal. Default is 3.
    - filename (str, optional): The name of the HTML file to save the plot. Default is "scatter_plot.html".
    """
    if remove_outliers:
        clean_data = data.copy()
        clean_data[x], clean_data[y] = remove_outliers_from_scatter(clean_data[x], clean_data[y], threshold)
        fig = px.scatter(clean_data, x=x, y=y, color=hue, title=title)
    else:
        fig = px.scatter(data, x=x, y=y, color=hue, title=title)

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        title_text=title
    )

    if xlim:
        fig.update_xaxes(range=xlim)

    if ylim:
        fig.update_yaxes(range=ylim)

    if filename is None:
        # If filename is not provided, use the title as the default filename
        filename = slugify(title) + ".html"

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename)

    # Save the plot as an HTML file
    fig.write_html(full_filename)

    #fig.show()


def box_html(data, x, y, labels=None, title="Box Plot", xlabel="Categories", ylabel="Values", ylim=None, log=False, filename=None):
    """
    Create a box plot using Plotly Express.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x,y (str): Names of variables in data.
    - labels (list, optional): The labels for each box. Default is None.
    - title (str, optional): The title of the plot. Default is "Box Plot".
    - xlabel (str, optional): The label for the x-axis. Default is "Categories".
    - ylabel (str, optional): The label for the y-axis. Default is "Values".
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - log (bool): if True, set y to log(y).
    - filename (str, optional): The name of the HTML file to save the plot. Default is "box_plot.html".
    """
    if log:
        data[y] = np.log(data[y])

    fig = px.box(data, x=x, y=y, color=labels, title=title)

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        title_text=title,
        xaxis=dict(tickangle=20)
    )

    if ylim:
        fig.update_yaxes(range=ylim)

    if filename is None:
        # If filename is not provided, use the title as the default filename
        filename = slugify(title) + ".html"

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename)

    # Save the plot as an HTML file
    fig.write_html(full_filename)

    #fig.show()


def violin_html(data, x, y, labels=None, title="Violin Plot", xlabel="Categories", ylabel="Values", ylim=None, log=False, filename=None):
    """
    Create a violin plot using Plotly Express.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x,y (str): Names of variables in data.
    - labels (list, optional): The labels for each box. Default is None.
    - title (str, optional): The title of the plot. Default is "Violin Plot".
    - xlabel (str, optional): The label for the x-axis. Default is "Categories".
    - ylabel (str, optional): The label for the y-axis. Default is "Values".
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - log (bool): if True, set y to log(y).
    - filename (str, optional): The name of the HTML file to save the plot. Default is "violin_plot.html".
    """
    if log:
        data[y] = np.log(data[y])

    fig = px.violin(data, x=x, y=y, color=labels, title=title, box=True, points="all")

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        title_text=title,
        xaxis=dict(tickangle=90)
    )

    if ylim:
        fig.update_yaxes(range=ylim)

    if filename is None:
        # If filename is not provided, use the title as the default filename
        filename = slugify(title) + ".html"

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename)

    # Save the plot as an HTML file
    fig.write_html(full_filename)

    #fig.show()


def line_html(data, x, y, hue=None, title="Line Plot with Error Bars", xlabel="X-axis", ylabel="Y-axis", remove_outliers=False, threshold=3, xlim=None, ylim=None, filename=None):
    """
    Create a line plot with error bars.

    Parameters:
    - data (DataFrame): The DataFrame containing the data.
    - x, y (str): Names of variables in data.
    - hue (str, optional): Names of grouping variables in data.
    - title (str, optional): The title of the plot. Default is "Line Plot with Error Bars".
    - xlabel (str, optional): The label for the x-axis. Default is "X-axis".
    - ylabel (str, optional): The label for the y-axis. Default is "Y-axis".
    - remove_outliers (bool, optional): Whether to remove outliers. Default is False.
    - threshold (float, optional): The threshold for outlier removal. Default is 3.
    - xlim (tuple, optional): The limits for the x-axis. Default is None.
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - filename (str, optional): The name of the HTML file to save the plot. Default is "line_plot.html".
    """
    if remove_outliers:
        clean_data = data.copy()
        clean_data[x], clean_data[y] = remove_outliers_from_scatter(clean_data[x], clean_data[y], threshold)

    # Create a new figure for each plot
    fig, ax = plt.subplots()

    sns.lineplot(data=clean_data if remove_outliers else data, x=x, y=y, hue=hue, ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if ylim:
        ax.set_ylim(ylim)
    if xlim:
        ax.set_xlim(xlim)

    ax.legend()

    if filename is None:
        # If filename is not provided, use the title as the default filename
        filename = slugify(title) + ".html"

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename) if filename else "images/line_plot.html"

    # Add interactivity using mplcursors
    mplcursors.cursor(hover=True)

    # Save the plot as an HTML file using mpld3
    mpld3.save_html(fig, full_filename)

    return ax


def histogram_html(x, data=None, bins='auto', xscale='linear', yscale='linear', title="Histogram",
              xlabel="Values", ylabel="Frequency", xlim=None, ylim=None, remove_outliers=False, threshold=3, filename=None):
    """
    Create a histogram using Plotly Express.

    Parameters:
    - x (array-like): The data for the x-axis.
    - data (DataFrame, optional): The DataFrame containing the data. Default is None.
    - bins (int, sequence, or str, optional): Specification for the number of bins. Default is 'auto'.
    - xscale (str, optional): The scale of the x-axis. Default is 'linear'.
    - yscale (str, optional): The scale of the y-axis. Default is 'linear'.
    - title (str, optional): The title of the plot. Default is "Histogram".
    - xlabel (str, optional): The label for the x-axis. Default is "Values".
    - ylabel (str, optional): The label for the y-axis. Default is "Frequency".
    - xlim (tuple, optional): The limits for the x-axis. Default is None.
    - ylim (tuple, optional): The limits for the y-axis. Default is None.
    - remove_outliers (bool, optional): Whether to remove outliers. Default is False.
    - threshold (float, optional): The threshold for outlier removal. Default is 3.
    - filename (str, optional): The name of the HTML file to save the plot. Default is "histogram_plot.html".
    """
    if data is not None:
        if remove_outliers:
            x = remove_outliers_from_histogram(data[x], threshold)
        else:
            x = data[x]
    else:
        if remove_outliers:
            x = remove_outliers_from_histogram(x, threshold)

    if bins == 'auto': fig = px.histogram(x)
    else: fig = px.histogram(x, nbins=bins)

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        title_text=title,
        xaxis_type=xscale,
        yaxis_type=yscale
    )

    if xlim:
        fig.update_xaxes(range=xlim)

    if ylim:
        fig.update_yaxes(range=ylim)

    if filename is None:
        # If filename is not provided, use the title as the default filename
        filename = slugify(title) + ".html"

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename)

    # Save the plot as an HTML file
    fig.write_html(full_filename)

    #fig.show()


def pie_chart_html(data, labels, title="Pie Chart", filename=None):
    """
    Create a pie chart using Plotly Express.

    Parameters:
    - data (array-like): The data for the pie chart.
    - labels (list): The labels for each wedge.
    - title (str, optional): The title of the plot. Default is "Pie Chart".
    - filename (str, optional): The name of the HTML file to save the plot. Default is "pie_chart.html".
    """
    fig = px.pie(names=labels, values=data, title=title, hole=0.3, labels=labels)

    if filename is None:
        # If filename is not provided, use the title as the default filename
        filename = slugify(title) + ".html"

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename)

    # Save the plot as an HTML file
    fig.write_html(full_filename)

    #fig.show()

def pair_grid_w_p_values_html(data, filename="pair_grid_with_pvalues.html"):
    """
    Create a PairGrid with scatter plots in the upper triangle, histograms in the diagonal,
    and display p-values for Pearson correlation in the lower triangle.

    Parameters:
    - data (DataFrame): The DataFrame containing the data for the PairGrid.
    - filename (str, optional): The name of the HTML file to save the plot. Default is "pair_grid_with_pvalues.html".
    """
    # Create a PairGrid and map p-values
    g = sns.PairGrid(data)
    g.map_upper(sns.scatterplot)
    g.map_lower(display_pvalue)
    g.map_diag(sns.histplot, color="green")

    for ax in g.axes.flat:
        ax.xaxis.label.set_size(16)
        ax.yaxis.label.set_size(16)

    # Add a title
    g.fig.suptitle("Pair Plot with P-Values", y=1.02)

    # Automatically create the 'images' folder if it doesn't exist
    os.makedirs("images", exist_ok=True)

    # Append the folder path to the filename
    full_filename = os.path.join("images", filename)

    # Save the plot as an HTML file using mpld3
    mpld3.save_html(g.fig, full_filename)

    return g

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