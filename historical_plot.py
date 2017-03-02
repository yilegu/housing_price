from os.path import join, dirname
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file, save
from bokeh.layouts import row, column
from bokeh.sampledata.us_states import data as states
from bokeh.palettes import Viridis256
from bokeh.models import HoverTool, ColumnDataSource, ColorBar, LinearColorMapper, NumeralTickFormatter, Select
from bokeh.io import curdoc
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
    plot.circle(x='dates',y='price',source=source,size=8)
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Housing Price"
    plot.yaxis.axis_label_text_font_size = "14pt"
    plot.yaxis.formatter= NumeralTickFormatter(format="$0,0")
    plot.axis.axis_label_text_font_style = "bold"
    plot.title_text_font_size = '20pt'
    plot.title_text_align = 'center'
    
    return plot

def update_plot_county(attrname, old, new):
    county = county_select.value.upper()
    src = get_dataset(zillow_df,county+state_select.value)
    zillow_cs.data=src.data
    plot.title.text = "Price Data for "+county.title()+", "+state_select.value

    
def update_plot_state(attrname, old, new):
    state = state_select.value
    county_select.options = sorted(county_choices[state])
    src = get_dataset(zillow_df,sorted(county_choices[state])[0].upper()+state)
    zillow_cs.data=src.data
    plot.title.text = "Price Data for "+sorted(county_choices[state])[0].title()+", "+state
    
    
	
#Default Choices
county='LOS ANGELES'
state='CA'
countystate = county+state

file_name= 'data/County_Zhvi_AllHomes.csv'
file_name=(join(dirname(__file__), file_name))

zillow_df, county_choices = read_zillow_csv(file_name, 7)


state_select = Select(value=state,title='State',options=sorted(county_choices.keys()))
county_select = Select(value=county,title='County', options=sorted(county_choices[state]))

zillow_cs = get_dataset(zillow_df, countystate)
plot=make_plot(zillow_cs,"Price Data for "+county.title()+", "+state)

state_select.on_change('value', update_plot_state)
county_select.on_change('value', update_plot_county)

controls = column(state_select,county_select)

curdoc().add_root(row(controls, plot, width=800))
curdoc().title="Price"
