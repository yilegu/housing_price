from os.path import join, dirname
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import row, column
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.us_counties import data as counties
from bokeh.models import HoverTool, ColumnDataSource, ColorBar, LinearColorMapper, NumeralTickFormatter, Select
from bokeh.io import curdoc
from bokeh.palettes import Viridis256, RdYlBu11
from collections import defaultdict


def get_dataset(src, countystate):
    df = src[['dates',countystate]]
    df.columns=['dates','price']
    return ColumnDataSource(df)


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
    

def make_plot(source,title):
    plot=figure(title=title, toolbar_location="right",x_axis_type="datetime",plot_width=800)
    plot_glyph=plot.circle(x='dates',y='price',source=source,size=8)
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Housing Price"
    plot.yaxis.axis_label_text_font_size = "14pt"
    plot.yaxis.formatter= NumeralTickFormatter(format="$0,0")
    plot.axis.axis_label_text_font_style = "bold"
    plot.title_text_font_size = '20pt'
    plot.title_text_align = 'center'
    
    return plot, plot_glyph

def update_plot_county(attrname, old, new):
    mode_select.value = ' '
    county = county_select.value.upper()
    if county == ' ':
        plot.title.text = "Pleaes select a county"
    else:
        plot.title.text = "Please select whether you want to include predictions"

    
def update_plot_state(attrname, old, new):
    state = state_select.value
    mode_select.value = ' '
    if state == ' ':
        plot.title.text = "Please select a state"
    else:
        county_select.options = [' '] + sorted(county_choices[state])   
        plot.title.text = "Please select a county"
       
def update_plot_mode(attrname, old, new):
    state = state_select.value 
    county = county_select.value.upper()
    choice_prediction = mode_select.value
    if choice_prediction == 'Historical Data Only':
        src = get_dataset(zillow_df,county+state)
        zillow_cs.data=src.data
        zillow_cs_with_prediction.data=src.data
        plot.title.text = county.title()+", " + state + ". Only historical data are shown."
    elif choice_prediction == 'With Prediction':
        src1 = get_dataset(zillow_df,county+state)
        zillow_cs.data = src1.data
        if county+state in list(zillow_df_with_prediction.columns.values):
            src2 = get_dataset(zillow_df_with_prediction,county+state)
            zillow_cs_with_prediction.data=src2.data 
            file_name_error= 'data/predict_error_new.csv'
            file_name_error=(join(dirname(__file__), file_name_error))
            error_db = pd.read_csv(file_name_error)
            plot.title.text = county.title()+", " + state + " with predictions " +  "(Percentage Error={0:0.1f}%)".format(100* error_db[county+state].tolist()[0])
        else:
            zillow_cs_with_prediction.data=src1.data 
            plot.title.text = county.title()+", " + state + ". No predictions have been made yet for this county."
    elif choice_prediction == ' ':
        plot.title.text = "Please select options for predictions"

#######################################################
###The first part is to make the interactive map plot##
#######################################################


##########################################################################
###The second part is to make the time series plot for a selected county##
##########################################################################
  
#plot_circle.glyph.fill_alpha=0.1
#Default Choices
county='LOS ANGELES'
state='CA'
mode='Historical Data'
countystate = county+state
empty_df = pd.DataFrame() 

file_name= 'data/County_Zhvi_AllHomes.csv'
file_name=(join(dirname(__file__), file_name))

zillow_df, county_choices = read_zillow_csv(file_name, 7)

file_name_with_prediction = 'data/Price_WithPredictions_new.csv'
file_name_with_prediction=(join(dirname(__file__), file_name_with_prediction))
zillow_df_with_prediction = pd.read_csv(file_name_with_prediction,parse_dates=[-1])


state_select = Select(value=' ',title='State',options=[' '] + sorted(county_choices.keys()))
county_select = Select(value=' ',title='County', options=[' '] + sorted(county_choices[state]))
mode_select = Select(value=' ',title='With or Without Predictions', options=[' ', 'Historical Data Only','With Prediction'])

zillow_cs = get_dataset(zillow_df, countystate)
zillow_cs_with_prediction = get_dataset(zillow_df, countystate)

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
#plot.title_text_align = 'center'

state_select.on_change('value', update_plot_state)
county_select.on_change('value', update_plot_county)
mode_select.on_change('value', update_plot_mode)


control1 = column(state_select,county_select)
control2 = column(mode_select)

############We combine them here#########
curdoc().add_root(row(control1,control2, plot, width=800))
curdoc().title="Price"
