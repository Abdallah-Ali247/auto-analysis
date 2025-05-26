import numpy as np
import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
import seaborn as sns
import random

from io import BytesIO
import base64

# Set the Seaborn style to darkid
sns.set_theme(style='darkgrid')


# ***********************************************************************************
# *************************       Prepare Plots 1      ******************************
# ***********************************************************************************

# Boxen Plot  *********************************************************
def boxen_plot(df, col, axs=None):
  # Plot the boxenplot
  ax = sns.boxenplot(data=df[col], color='steelblue', saturation=0.8, linewidth=1.5, ax=axs)

  # Set plot title and labels
  ax.set_title(f"{col} Boxen Plot".title(), fontsize=14)
  ax.set_xlabel(f"{col}", fontsize=12)
  ax.set_ylabel("Values", fontsize=12)

  # Customize the x-axis tick labels
  ax.set_xticklabels(['A'], fontsize=10)  # Only one label as there is only one data point

  # display grid
  ax.yaxis.grid(True)

  # Calculate Q1 and Q3 using numpy
  q1 = np.percentile(df[col], 25)
  q3 = np.percentile(df[col], 75)

  # Add a horizontal line at the median
  ax.axhline(y=q1, color='b', linestyle='-', linewidth=2)
  ax.axhline(y=df[col].median(), color='green', linestyle='-', linewidth=3)
  ax.axhline(y=df[col].mean(), color='r', linestyle='--', linewidth=1.2)
  ax.axhline(y=q3, color='orange', linestyle='-', linewidth=2)

  # Add a legend
  q1_legend = plt.Line2D([], [], color='b', linestyle='-', linewidth=1.2, label='Q1')
  median_legend = plt.Line2D([], [], color='green', linestyle='-', linewidth=1.2, label='Median')
  mean_legend = plt.Line2D([], [], color='r', linestyle='--', markersize=5, label='Mean')
  q2_legend = plt.Line2D([], [], color='orange', linestyle='-', linewidth=1.2, label='Q2')



  # Add a legend with custom labels and customize font size and legend size
  legend = ax.legend(handles=[q1_legend, median_legend, mean_legend, q2_legend], loc='upper right',fontsize=8)
  legend.get_title().set_fontsize(9)
  legend.get_frame().set_linewidth(0.5)


# Strip Plot    ***************************************************************
def strip_plot(df, colx,coly,hue=None, axs=None):

  palette=None
  if hue:
    palette='tab10'
    # Create a strip plot with custom point appearance
    ax = sns.stripplot(data=df, x=colx, y=coly, hue=hue, dodge=True , palette=palette, linewidth=0.5, edgecolor='black', ax=axs)

    # Add a legend with custom labels and customize font size and legend size
    ax.set_title(f'{colx} vs {coly} group by  {hue}'.title())
    legend = axs.legend(title=f'{hue}'.title(), loc=(-0.1, 0.9), fontsize=8)
    legend.get_title().set_fontsize(9)
    legend.get_frame().set_linewidth(0.5)

  else:
    # Create a strip plot with custom point appearance
    ax = sns.stripplot(data=df, x=colx, y=coly, linewidth=0.5, edgecolor='black', ax=axs)

    ax.set_title(f'{colx} vs {coly}'.title())


# Pie Plot      **************************************************************
def pie_plot(df, col, ax=None):

    # Calculate value counts
    value_counts = df[col].value_counts().sort_values(ascending=False)

    # Set the explode of the first and biggest sector
    explode = [0] * len(value_counts)
    explode[0] = 0.07

    # Set edge properties
    edge_props = {'linewidth': 2, 'edgecolor': 'white'}

    # Create pie plot
    ax.pie(value_counts, labels=value_counts.index, explode=explode, shadow=True,
           wedgeprops=edge_props, autopct='%1.1f%%')

    # Set aspect ratio to make it a circle
    ax.axis('equal')

    # Add a title
    ax.set_title(f'{col} Distribution'.title())

    # Create custom legend labels with ratios
    legend_labels = [f'{label} : {round((count / value_counts.sum()) * 100, 2)} %'
                     for label, count in zip(list(value_counts.index), list(value_counts))]


    # Add a legend with custom labels and customize font size and legend size
    legend = ax.legend(legend_labels, title='Class : Ratio', loc=(0, 0), fontsize=8)
    legend.get_title().set_fontsize(9)
    legend.get_frame().set_linewidth(0.5)


# Count Plot           ****************************************************
def count_plot(df, col, axs=None):
    # Create countplot
    ax = sns.countplot(y=df[col], data=df, palette='hot', ax=axs)
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())}\n', (p.get_width(), p.get_y()+0.5), ha='left', va='center', color='black', size=9)

    # Set plot title and labels
    ax.set_title(f'{col} Distribution'.title())
    ax.set_xlabel('Count')
    ax.set_ylabel(f'{col}')

# Bar Plot   ***************************************************************
def bar_plot(df, colx,coly,colh=None, axs=None):

  palette='hot' if colh else None

  # Create barplot with hue and dodge
  ax = sns.barplot(x=colx, y=coly, hue=colh,palette=palette, dodge=True, data=df, ax=axs)

  # Set plot title and labels
  ax.set_xlabel(f'{colx}')
  ax.set_ylabel(f'{coly}')

  # Add a legend with custom labels and customize font size and legend size
  if colh:
    ax.set_title(f'{colx} vs {coly} group by  {colh}'.title())
    legend = ax.legend(title=f'{colh}'.title(), loc=(0.9, 0.8), fontsize=8)
    legend.get_title().set_fontsize(9)
    legend.get_frame().set_linewidth(0.5)
  else:
    ax.set_title(f'{colx} vs {coly}')


# Violin Plot   ****************************************************
def violin_plot(df, colx,coly,colh=None,axs=None):
    palette='hot' if colh else None

    ax=sns.violinplot(x=colx, y=coly, hue=colh,data=df, palette=palette, ax=axs)

    # Set plot title and labels
    ax.set_xlabel(f'{colx}')
    ax.set_ylabel(f'{coly}')

    # Add a legend with custom labels and customize font size and legend size
    if colh:
      ax.set_title(f'{colx} vs {coly} group by  {colh}'.title())
      legend = ax.legend(title=f'{colh}'.title(), loc=(0.9, 0.8), fontsize=8)
      legend.get_title().set_fontsize(9)
      legend.get_frame().set_linewidth(0.5)
    else:
      ax.set_title(f'{colx} vs {coly}')

# Box Plot    *********************************************************
def box_plot(df, colx, coly, colh=None, axs=None):

    palette= 'tab10' if colh else None

    ax= sns.boxplot(x=colx, y=coly, hue=colh, palette=palette, data=df, ax=axs)

    # Set plot title and labels
    ax.set_xlabel(f'{colx}')
    ax.set_ylabel(f'{coly}')

    # Add a legend with custom labels and customize font size and legend size
    if colh:
      ax.set_title(f'{colx} vs {coly} group by {colh}'.title())
      legend = ax.legend(title=f'{colh}'.title(), loc=(0.87, 0.8), fontsize=8)
      legend.get_title().set_fontsize(9)
      legend.get_frame().set_linewidth(0.5)
    else:
      if colx :
       ax.set_title(f'{colx} vs {coly}'.title())
      else :
        ax.axhline(df[coly].mean(), color='red', linestyle='dashed', linewidth=2)
        mean_legend = plt.Line2D([], [], color='r', linestyle='--', markersize=5, label='Mean')
        legend = ax.legend(handles=[mean_legend], loc='upper right',fontsize=8)
        ax.set_title(f'{coly} Box Plot'.title())
        ax.set_ylabel("Years")
        ax.set_xlabel(f"{coly}".title())






# ***********************************************************************************
# *************************       Prepare Plots 2      ******************************
# ***********************************************************************************


# Scatter Plot     *****************************************************
def scatter_plot(df, colx, coly, hue=None, style=None, axs=None):

  pallet= 'tab10' if hue else None

  # Create scatter plot
  ax = sns.scatterplot(data=df, x=colx, y=coly, hue=hue, style=style, palette=pallet, ax=axs)

  # Set plot title and labels
  ax.set_xlabel(f"{colx}", fontsize=12)
  ax.set_ylabel(f"{coly}", fontsize=12)


  # Add a grid
  ax.grid(True, linestyle='--', linewidth=0.5)

  # Add a legend with custom labels and customize font size and legend size
  if hue:
    ax.set_title(f'{colx} vs {coly} group by {hue}'.title())
    legend = ax.legend(title=f'{hue}'.title(), loc=(0.8, 0.28), fontsize=8)
    legend.get_title().set_fontsize(9)
    legend.get_frame().set_linewidth(0.5)
    if style:
      ax.set_title(f'{colx} vs {coly} group by  {hue} & {style}'.title())
  else:
    ax.set_title(f'{colx} vs {coly}'.title())


# Hisogram   **********************************************************
def hist_plot(df, col, axs=None):

  # calc number of bins
  n = int(np.ceil(df.shape[0]**0.5))
  # Create histogram
  ax = sns.histplot(df[col], bins=n, kde=True, color='#5614b3', line_kws={'linewidth': 2}, ax=axs)
  ax.lines[0].set_color('crimson') # Kde color

  # Add labels and title
  ax.set_xlabel(f'{col}')
  ax.set_ylabel('Frequency')
  ax.set_title(f'{col} Histogram'.title())


# Line Plot ************************************************************
def line_plot(df, colx, coly, axs=None):

  # Create the line plot
  ax= sns.lineplot(data=df, x=colx, y=coly, color='blue', marker='o', markersize=4, markeredgecolor='red', markerfacecolor='yellow', ax=axs)

  # add title and legend
  ax.set_title(f'{colx} & {coly} Line Plot '.title())
  ax.grid(True)
  ax.legend(['Data'], loc='upper left')

# HeatMap     *******************************************************************
def heat_map(df, axs=None):
  
  numeric_cols = df.select_dtypes(include='number')
  corr_matrix = numeric_cols.corr()
  #corr = df.corr()
  ax = sns.heatmap(corr_matrix, annot=True,  annot_kws={'size': 8}, fmt='.2', ax=axs)

  # Set plot title and labels
  ax.set_title('Heatmap')

  # Set font size of column names
  ax.tick_params(labelsize=9)






  

# ***************************************************************************************************
# ***********************   All Categorical Plots in one Figure    **********************************
# ***************************************************************************************************


def cat_plot(df, colx,coly,colh=None):
  # Create a figure and subplots
  fig, axes = plt.subplots(3, 3, figsize=(16, 10))

  # set the background color of the figure to light gray
  fig.set_facecolor('#cccccc')
  
  # Adjust the spacing between subplots
  plt.subplots_adjust(hspace=0.5, wspace=0.3)

  # *********************************************************
  # ************ Plot on the subplots (First Row) ***********
  # *********************************************************

  pie_plot(df, colx, axes[0, 0])
  count_plot(df, colx, axs=axes[0,1])

  rand_col = random.choice(coly) # Choose a random column from the conti_list
  strip_plot(df, colx, rand_col, axs=axes[0, 2])

    # *********************************************************
    # ************ Plot on the subplots (Second Row) ***********
    # *********************************************************

  if len(colh)>1:
    rand_col = random.choice(coly) # Choose a random column from the conti_list
    h_col = random.choice([col for col in colh if col != rand_col and col != colx]) # Choose a random column from the colh exclude rand_col
    bar_plot(df, colx, rand_col, h_col, axs=axes[1,0])

    rand_col = random.choice(coly) # Choose a random column from the conti_list
    h_col = random.choice([col for col in colh if col != rand_col and col != colx]) # Choose a random column from the colh exclude rand_col
    strip_plot(df, colx, rand_col, h_col, axs=axes[1, 1])

    rand_col = random.choice(coly) # Choose a random column from the conti_list
    h_col = random.choice([col for col in colh if col != rand_col and col != colx]) # Choose a random column from the colh exclude rand_col
    violin_plot(df, colx, rand_col, h_col, axs=axes[1,2])

    # *********************************************************
    # ************ Plot on the subplots (Third Row) ***********
    # *********************************************************

    rand_col = random.choice(coly) # Choose a random column from the conti_list
    h_col = random.choice([col for col in colh if col != rand_col and col != colx])  # Choose a random column from the colh exclude rand_col
    strip_plot(df, colx, rand_col, h_col, axs=axes[2, 0])

    rand_col = random.choice(coly) # Choose a random column from the conti_list
    h_col = random.choice([col for col in colh if col != rand_col and col != colx])  # Choose a random column from the colh exclude rand_col
    box_plot(df, colx, rand_col, h_col, axs=axes[2,1])

    rand_col = random.choice(coly) # Choose a random column from the conti_list
    h_col = random.choice([col for col in colh if col != rand_col and col != colx]) # Choose a random column from the colh exclude rand_col
    bar_plot(df, colx, rand_col, h_col, axs=axes[2,2])

  # Set a big title for the entire figure
  fig.suptitle(f"{colx} analysis \n{'*'*20}".title(), fontsize=16)

  #capture the figure and Save it to a temporary buffer.
  buf = BytesIO()
  fig.savefig(buf, format="png")  
  # Embed the result in the html output.
  data = base64.b64encode(buf.getbuffer()).decode("ascii")

  return data






# *****************************************************************************************************
# ***********************   All Continuous Plots in one Figure    *************************************
# *****************************************************************************************************


def cont_plot(df, colx, cont_list, cat_list, colh):
  # Create a figure and subplots
  fig, axes = plt.subplots(3, 3, figsize=(16, 10))

  # set the background color of the figure to light gray
  fig.set_facecolor('#cccccc')

  # Adjust the spacing between subplots
  plt.subplots_adjust(hspace=0.5, wspace=0.3)

  # *********************************************************
  # ************ Plot on the subplots (First Row) ***********
  # *********************************************************
  hist_plot(df, colx, axs=axes[0, 0])

  if len(cont_list) > 1 :
    rand_col = random.choice([col for col in cont_list if col != colx]) # Choose a random column from the conti_list
    line_plot(df, colx, rand_col, axes[0, 1])

    rand_col = random.choice([col for col in cont_list if col != colx]) # Choose a random column from the conti_list
    scatter_plot(df, colx, rand_col, axs=axes[0, 2])

  # *********************************************************
  # ************ Plot on the subplots (Second Row) ***********
  # *********************************************************

  boxen_plot(df, colx, axs=axes[1, 0])
  
  if len(cont_list) > 1 :
    heat_map(df, axs=axes[1, 1])


  rand_cat = random.choice(cat_list) # Choose a random column from the cat_list
  h_col = random.choice([col for col in colh if col != rand_cat]) if len(colh)>1 else colh[0] # Choose a random column from the colh exclude rand_cat
  box_plot(df, rand_cat, colx, h_col, axs=axes[1, 2])


  # *********************************************************
  # ************ Plot on the subplots (Third Row) ***********
  # *********************************************************

  if len(cont_list) > 1 and len(cat_list) > 1 :
    rand_col = random.choice([col for col in cont_list if col != colx]) # Choose a random column from the conti_list
    rand_cat = random.choice(cat_list) # Choose a random column from the cat_list
    h_col = random.choice([col for col in colh if col != rand_cat]) if len(colh)>1 else colh[0] # Choose a random column from the colh exclude rand_cat
    scatter_plot(df, colx, rand_col, rand_cat, h_col, axs=axes[2, 0])


    rand_col = random.choice([col for col in cont_list if col != colx]) # Choose a random column from the conti_list
    rand_cat = random.choice(cat_list) # Choose a random column from the cat_list
    scatter_plot(df, colx, rand_col, rand_cat, axs=axes[2, 1])

    rand_col = random.choice([col for col in cont_list if col != colx]) # Choose a random column from the conti_list
    rand_cat = random.choice(cat_list) # Choose a random column from the cat_list
    h_col = random.choice([col for col in colh if col != rand_cat]) if len(colh)>1 else colh[0] # Choose a random column from the colh exclude rand_cat
    scatter_plot(df, colx, rand_col, rand_cat, h_col, axs=axes[2, 2])

  # Set a big title for the entire figure
  fig.suptitle(f"{colx} analysis \n{'*'*20}".title(), fontsize=16)

  # capture the figure and Save it to a temporary buffer.
  buf = BytesIO()
  fig.savefig(buf, format="png")
  # Embed the result in the html output.
  data = base64.b64encode(buf.getbuffer()).decode("ascii")

  return data


# ***************************************************************************************************
# ***********************      Display Columns Have no Plots    *************************************
# ***************************************************************************************************

def other_columns(other_list):

    # Calculate the number of lines required
    num_lines = np.ceil(len(other_list) / 5)  # number of lines 5

    # Create a blank plot
    fig, ax = plt.subplots()

    # Set the x-axis range
    ax.set_xlim(0, 5)
    # Set the y-axis range
    ax.set_ylim(0, num_lines)

    # Hide the axes
    ax.axis('off')

    # Set the plot title
    ax.set_title(f"Columns That Have No Plots (High Cardinality)\n{'*'*50}")

    # Add text annotations for each value
    for i, value in enumerate(other_list):
        line_num = i // 5  # Line Number
        col_num = i % 5  # Column number
        ax.text(col_num + 0.5, line_num + 0.5, value, ha='center', va='center', fontsize=12)

    #capture the figure and Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")  
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data


















