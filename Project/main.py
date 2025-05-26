from flask import Flask, render_template, Response, request
import numpy as np
import pandas as pd
import seaborn as sns
import io 
from autoAnalysis import all_in_one # my custom func



app = Flask(__name__)

# Dataset names
dataset_names = ["titanic", "tips", "penguins",  "taxis", "dots", "exercise", "geyser", "glue", "iris", "mpg", ]


# home page
@app.route('/')
def index():
    return render_template('home.html', dataset_names=dataset_names)



# create analysis page
@app.route('/load_dataset', methods=['POST'])
def load_dataset():

    valid = False # var to check if there is df or not 
    if 'dataset_file' not in request.files: # if there is no name "dataset_file" in my request
        # Load dataset from select box
        df_name = request.form.get('dataset_name') # get "dataset_name" from my request
        if df_name:
            df = sns.load_dataset(df_name) # load data using sns
            valid = True
    else:

        file = request.files['dataset_file'] # get file from my request 
        if file.filename == '': # if there is no file name
            flash('No file selected')  # message "No file"
            return redirect(request.url)
        try :
            df = pd.read_csv(file) # read csv file using pandas 
            df_name = file.filename[:-4] # get only file name without extention (.csv)
            valid = True
        except:
            
            return render_template('result.html', valid=valid)


    # Get the first 5 rows of the loaded dataset
    head_table = df.head().to_html(classes='table table-striped')

    # Get the dataset information
    buffer = io.StringIO() #create a buffer from StringIO
    df.info(buf=buffer) # save the df.info in buffer
    info_table = buffer.getvalue() # get value from the buffer

    # Calculate the summary statistics
    pd.set_option('display.float_format', lambda x: f'{x:.2f}')# set the float format for pandas outputs
    try: 
        des_n = df.describe().to_html(classes='table table-striped')
    except:
        des_n = None
    try :
        des_c = df.describe(exclude=[int,float]).to_html(classes='table table-striped')
    except:
        des_c = None 
    try:    
        # display plots 
        fig_data,other_list = all_in_one(df) # my custom function to display plots to each column in df 
    except:
        fig_data,other_list = None, None

    return render_template('result.html', valid=valid, df_name=df_name, head_table=head_table,
                           info_table=info_table, des_n=des_n, des_c=des_c, 
                           data=fig_data,other_list=other_list)



if __name__ == "__main__":
    app.run(debug=True)
