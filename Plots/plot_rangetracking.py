import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, save, output_file
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, Range1d
from bokeh.transform import transform
from bokeh.palettes import RdBu, Spectral, RdYlBu, RdGy, YlGnBu, Inferno, Plasma, PuBu, Greys, Magma, Viridis


def plot_rangetracking(project_name, voltage_df, ss_code=None, ss_config=None):

    # Check for data to plot
    if voltage_df is None:
        return

    # If there is no data, than we cannot create a plot
    if voltage_df.empty:
        return

    # Create a default subsystem query string
    ss_str = "_{}_{}".format(ss_config, ss_code)

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

    # Create plot
    plot = figure(tools=[TOOLS], title="{} - Voltage".format(project_name), x_axis_type="datetime")

    # Combine the data into a Data frame for ColumnDataSource for the plot
    plot.line(x='datetime', y='voltage', source=ColumnDataSource(voltage_df), line_width=5, line_color="Goldenrod")

    # Set the labels
    plot.xaxis.axis_label = "Date/Time"
    plot.yaxis.axis_label = 'Voltage'

    # Set the tool tip
    plot.select_one(HoverTool).tooltips = [
        ('ENS Num', '@ensnum'),
        ('Date/Time', '@datetime{%F}'),
        ('Beam', '@beam'),
    ]
    plot.select_one(HoverTool).formatters = {
        'datetime': 'datetime'                          # use 'datetime' formatter for 'datetime' field
    }
    plot.select_one(HoverTool).mode = 'vline'           # display a tooltip whenever the cursor is vertically in line with a glyph

    # Save plot to HTML
    file_name = project_name + '{}_rt.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    output_file(file_name, title="{} - Range Tracking".format(project_name))
    save(gridplot([[plot]], sizing_mode='stretch_both'))  # Just save to file