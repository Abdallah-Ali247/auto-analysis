import numpy as np
import pandas as pd
import statistics as st
import matplotlib.pyplot as plt
import seaborn as sns
import random

from all_plots import cat_plot, cont_plot, other_columns # my custom functions



# ************************************************************************************
# ***************************    Preprocessing  ************************************** 
# ************************************************************************************


# check if there is an ID columns ****************************************
def check_id(df):

  id_names = [col for col in df if 'id' in col.lower() ] # list of columns have 'id' in its name

  i_d = [col for col in df if df[col].nunique() == df.shape[0]] # list of all columns has unique values == number of all df rows

  if len(i_d) == 1 :                                            # if there is one column so it must be the index
    #df.set_index(id[0], inplace=True)                          # set the column as index
    df.drop(columns=i_d[0], inplace=True)   # drop the 'id' column because it makes plot so bad
    return df
  elif len(i_d) > 1 : # if we have more than one column in id list
    sub_id = [col for col in i_d if col in id_names]  # check if any of these columns have "id" in its name
    if len(sub_id) == 1 :  # check if sub_id have only one column
      df.drop(columns=sub_id[0], inplace=True)   # drop the 'id' column because it makes plot so bad
      return df
  else:
    return df

# check high number of nulls ******************************************************
 
def check_nulls(df):
  """
  1. function takes data frame
  2. drop the column has more than 50% nulls
  3. return data frame
  """
  df = check_id(df) # check if there ara an id column in df

  # list of some possible string values can be found insted of 'nulls'
  missing_str = ['miss','not found','unknown','NA','unspecified','other','N/A','invalid','none','null','empty','@','/','$','%','&','?','!','~','|','\\','< >','[]']
  df.replace(missing_str, np.nan, inplace=True) # replace any noise value in df by 'NAN'

  for col in df: #  loop foe each col in df

    if df[col].isna().sum()/len(df) > 0.5 : # check if column has more than 50% nulls
      df.drop(columns=col, inplace=True) # drop the column has more than 50% nulls


  return df # return df after drop column with more than 50% nulls



# function handle nulls & convert types ********************************************
 
def clean_data(df):
  '''
  1. function takes data frame
  2. create list of any column types not [int , float, bool]
  3. check the values type inside each column
  4. handle missing values according to values type
  5. convert column type to a suitable type
  6. return data frame
  '''
  df = check_nulls(df) # drop any column has more than 50% nulls
  numerical_column = ['int64', 'float64', 'int32', 'int16', 'int8', 'float32', 'uint8', 'uint16', 'uint32', 'uint64', 'bool']

  obj_col = [col for col in df if df[col].dtype not in numerical_column] # create list of any column types not [int , float, bool]

  for col in df: # loop on each col in df
    if col in obj_col : # if col type not [int, float, bool]
        t=[] # empty list to store some types of each single value int the column

        for i in range(25): # loop on from 0 to 24
          if not pd.isnull(df[col][i]): # check the first 25 value in each column if not null
            t.append(type(df[col][i])) # if the value is not null , appent it's type in `t` list

        if st.mode(t) == str: # check on the mode of `t` list if is 'str', then the column should be 'object'
          # convert the 'sting values' iside column to lower case
          df[col] = df[col].str.lower() # make sure that all values in the same shape
          df[col] = df[col].fillna(df[col].mode()[0]) # fill nulls in this column with the mode of the column

        elif st.mode(t) == bool: # check the mode of `t` if bool
          df[col] = df[col].fillna(df[col].mode()[0]) # fill nulls with the mode
          df[col] = df[col].astype(int) # convert the column to int , (1 for Ture and 0 for False)

        elif (st.mode(t) == float) or (st.mode(t) == int): # if the mode of `t` is numeric
          df[col] = pd.to_numeric(df[col], errors='coerce') # convert it to numeric, and replace any value(/,+,@) cann't converted to NAN
          df[col] = df[col].fillna(df[col].mean()) # fill nulls with the mean of the column

    elif df[col].dtype == bool : # check if column type is bool
      df[col] = df[col].fillna(df[col].mode()[0]) # fill nulls with the mode
      df[col] = df[col].astype(int) # convert the column to int , (1 for Ture and 0 for False)

    else: # if not in obj_col or not bool , it must be [int , float]
      df[col] = pd.to_numeric(df[col], errors='coerce')  # convert it to numeric, and replace any value(/,+,@) cann't converted to NAN
      df[col] = df[col].fillna(df[col].mean()) # fill nulls with the mean of the column

  return df


# cluster columns types *************************************************************
def split_type(df):

  '''
  cat_list = [ col for col in obj_list if df[col].nunique() <= 15  ] # list with categorical column have <= 15 class
  conti_cat_list = [col for col in df if df[col].dtype in [int,float] and df[col].nunique() <= 15 ] # categorical columns from numerical columns
  cat_list += conti_cat_list # add conti_cat_list to cat_list
  '''

  numerical_column = ['int64', 'float64', 'int32', 'int16', 'int8', 'float32', 'uint8', 'uint16', 'uint32', 'uint64', 'bool']

  obj_list = []    # create list of non numerical columns (and) any column with number of unique <=15
  for col in df.columns:
      if df[col].dtype not in numerical_column or df[col].nunique() <= 15:
          obj_list.append(col)

  cat_list = [ col for col in obj_list if df[col].nunique() <= 15  ] # list of column with only number of unique <=15

  conti_list = [ col for col in df if df[col].dtype in numerical_column and col not in cat_list ] # list of numerical continuous columns

  hue_cat = [ col for col in cat_list if df[col].nunique() < 4 ]  # list of categorical column have < 4 class (for hue in plots)

  other_list = [ col for col in df if col not in cat_list and col not in conti_list and col not in hue_cat] # other columns not in [cat_list, conti_list, hue_cat ]

  return cat_list, conti_list, hue_cat , other_list



# ***********************************************************************************
# *******************************   All In One    ***********************************
# ***********************************************************************************

def all_in_one(df):

  df = clean_data(df) # handle nulls & dtypes

  # cluster types of columns
  cat_list, conti_list, hue_cat, other_list = split_type(df)


  all_figs={'cat_fig':[],'cont_fig':[]}


  for col in df :  # loop in each column in df
    
    if col in cat_list:  # check if the column is categorical
      cat_fig_data = cat_plot(df, col, conti_list, hue_cat) # apply all categorical plots on current column
      all_figs['cat_fig'].append(cat_fig_data)
    
    elif col in conti_list :
      cont_fig_data = cont_plot(df, col, conti_list, cat_list, hue_cat) # apply all continuous plots on current column
      all_figs['cont_fig'].append(cont_fig_data)
    else:
      continue  

  
  return all_figs , other_list


