from os.path import join, dirname
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Select
from bokeh.models.widgets import RadioButtonGroup
from bokeh.io import curdoc
from collections import defaultdict


#Function To Read Data 
def read_zillow_csv(filename, skip=7):
    df=pd.read_csv(filename)
    dfcopy = df.copy()
    df["County+State"] = df["RegionName"].str.upper() + df["State"]
    df=df.set_index('County+State')
    df=df.T[skip:]
    df['dates']=df.index
    df['dates']=pd.to_datetime(df['dates'])
    county_choices=defaultdict(list)
    for ind in range(len(dfcopy.State)):
        county_choices[dfcopy.loc[ind]['State']].append(dfcopy.loc[ind]['RegionName'])
    return (df, county_choices)

#Function to Convert Data Into ColumnDataSource For Bokeh
def get_dataset(src, countystate):
    df = src[['dates',countystate]]
    df.columns=['dates','price']
    return ColumnDataSource(df)    


#Function to Update based on User's Selection on State
def update_plot_state(attrname, old, new):
    state = state_select.value
    mode_select.active = 2
    if state == ' ':
        plot.title.text = "Please select a state"
    else:
        county_select.options = [' '] + sorted(county_choices[state])   
        plot.title.text = "Please select a county"

#Function to Update based on User's Selection on County
def update_plot_county(attrname, old, new):
    mode_select.active = 2
    county = county_select.value.upper()
    if county == ' ':
        plot.title.text = "Pleaes select a county"
    else:
        plot.title.text = "Please select whether you want to include predictions"

    
#Function to Update based on User's Selection on whether historical data only or including predictions    
def update_plot_mode(attrname, old, new):
    state = state_select.value 
    county = county_select.value.upper()
    choice_prediction = mode_select.active
    if choice_prediction == 0:
        src = get_dataset(zillow_df,county+state)
        zillow_cs.data=src.data
        zillow_cs_with_prediction.data=src.data
        plot.title.text = county.title()+", " + state + ". Only historical data are shown."
    elif choice_prediction == 1:
        src1 = get_dataset(zillow_df,county+state)
        zillow_cs.data = src1.data
        if county+state in list(zillow_df_with_prediction.columns.values):
            src2 = get_dataset(zillow_df_with_prediction,county+state)
            zillow_cs_with_prediction.data=src2.data 
            file_name_error= 'data/predict_error_new.csv'
            file_name_error=(join(dirname(__file__), file_name_error))
            error_db = pd.read_csv(file_name_error)
            plot.title.text = county.title()+", " + state + " with predictions" +  " (Percentage Error={0:0.1f}%)".format(100* error_db[county+state].tolist()[0])
        else:
            zillow_cs_with_prediction.data=src1.data 
            plot.title.text = county.title()+", " + state + ". No predictions have been made yet for this county."
    elif choice_prediction == ' ':
        plot.title.text = "Please select options for predictions"




#Default Choices
county='LOS ANGELES'
state='CA'
countystate = county+state
empty_df = pd.DataFrame() 

#Read data file and convert to ColumnDataSource (without prediction)
file_name= 'data/County_Zhvi_AllHomes.csv'
file_name=(join(dirname(__file__), file_name))
zillow_df, county_choices = read_zillow_csv(file_name, 7)
zillow_cs = get_dataset(zillow_df, countystate)

#Read data file and convert to ColumnDataSource (with prediction)
file_name_with_prediction = 'data/Price_WithPredictions_new.csv'
file_name_with_prediction=(join(dirname(__file__), file_name_with_prediction))
zillow_df_with_prediction = pd.read_csv(file_name_with_prediction,parse_dates=[-1])
zillow_cs_with_prediction = get_dataset(zillow_df, countystate)


#Create Buttons for Updates
state_select = Select(value=' ',title='State',options=[' '] + sorted(county_choices.keys()))
county_select = Select(value=' ',title='County', options=[' '] + sorted(county_choices[state]))
mode_select = RadioButtonGroup(labels=[ "Historical Data (Filled Circles)", "Historical Data (Filled Circles) with Predictions (Unfilled Circles)"], active=2)


#Plotting Figures
title = "Please select a state"
plot=figure(title=title, toolbar_location="right",x_axis_type="datetime",plot_width=800)
plot1=plot.circle(x='dates',y='price',source=zillow_cs,size=8)
plot2=plot.circle(x='dates',y='price',source=zillow_cs_with_prediction,size=8)
plot2.glyph.fill_alpha=0.1
plot.xaxis.axis_label = None
plot.yaxis.axis_label = "Housing Price"
plot.yaxis.axis_label_text_font_size = "14pt"
plot.yaxis.formatter= NumeralTickFormatter(format="$0,0")
plot.axis.axis_label_text_font_style = "bold"
plot.title.text_font_size = '16pt'

#Update figures based on User's Selections
state_select.on_change('value', update_plot_state)
county_select.on_change('value', update_plot_county)
mode_select.on_change('active', update_plot_mode)
control = column(state_select,county_select,mode_select)

#Format the Output
curdoc().add_root(row(control, plot, width=800))
curdoc().title="Price"
