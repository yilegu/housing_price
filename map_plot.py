import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file, save
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.palettes import Viridis256, RdYlBu11
from bokeh.models import HoverTool, ColumnDataSource, ColorBar, LinearColorMapper, NumeralTickFormatter


zillow_df=pd.read_csv('County_MedianListingPrice_AllHomes.csv')
zillow_df["County+State"] = zillow_df["RegionName"].str.upper() + '+' + zillow_df["State"]
zillow_df=zillow_df.set_index('County+State')
counties_df=pd.DataFrame(counties).T
counties_df['County+State']=counties_df['name'].str.upper()+ '+' + counties_df['state'].str.upper()

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states if code.lower() not in EXCLUDED]
state_ys = [states[code]["lats"] for code in states if code.lower() not in EXCLUDED]

county_xs=[counties[code]["lons"] for code in counties if counties[code]["state"] not in EXCLUDED]
county_ys=[counties[code]["lats"] for code in counties if counties[code]["state"] not in EXCLUDED]
county_ct=[counties[code]["name"] for code in counties if counties[code]["state"] not in EXCLUDED]
county_st=[counties[code]["state"].upper() for code in counties if counties[code]["state"] not in EXCLUDED]


#colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]

color_low=zillow_df['2017-01'].min()
color_high=zillow_df['2017-01'].max()
color_mapper = LinearColorMapper(palette=RdYlBu11, low=color_low, high=color_high/3)
color_mapper.low_color='#313695'
color_mapper.high_color='#a50026'
color_mapper.nan_color='gray'

county_values = []
# step = (zillow_df['2017-01'].max()/1.5 - zillow_df['2017-01'].min())/11;
for county_id in counties:
    if counties[county_id]["state"] in EXCLUDED:
        continue
    try:
        price = zillow_df['2017-01'][counties_df.loc[county_id[0]].loc[county_id[1]]['County+State'].upper()]
        if price > 0:
            county_values.append(price)
        else:
            county_values.append(np.nan)
    except KeyError:
        county_values.append(np.nan)

p = figure(title="Housing Price", toolbar_location="left",
           plot_width=1100, plot_height=700)


county_dict={'county_xs':county_xs, 'county_ys':county_ys,'county_ct':county_ct, 'county_st':county_st, 'county_values':county_values}
county_cds=ColumnDataSource(county_dict)


countyplot=p.patches("county_xs", "county_ys",
          fill_color={'field':'county_values', 'transform': color_mapper}, fill_alpha=0.7,
          line_color="white", line_width=0.5,source=county_cds)

p.patches(state_xs, state_ys, fill_alpha=0.0,
          line_color="#884444", line_width=2, line_alpha=0.3)

hover=HoverTool(tooltips=[("County","@county_ct"),("State","@county_st"), ("Price", "@county_values")],renderers=[countyplot])
p.add_tools(hover)

color_bar = ColorBar(color_mapper=color_mapper,
                     label_standoff=2,major_label_text_align="right", border_line_color=None, location=(0,0),formatter=NumeralTickFormatter(format="$0,0"))
color_bar.formatter

p.add_layout(color_bar, 'right')

output_file("ds.html", title="Housing Example")

show(p)
