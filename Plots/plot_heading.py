import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, save, output_file
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, Range1d
from bokeh.transform import transform
from bokeh.palettes import RdBu, Spectral, RdYlBu, RdGy, YlGnBu, Inferno, Plasma, PuBu, Greys, Magma, Viridis


def plot_heading(project_name, heading_df, ss_code=None, ss_config=None):

    # Check for data to plot
    if heading_df is None:
        return

    # If there is no data, than we cannot create a plot
    if heading_df.empty:
        return

    # Create a default subsystem query string
    ss_str = "_{}_{}".format(ss_config, ss_code)

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

    # Create plot
    p2 = figure(tools=TOOLS, toolbar_location='left', title="{} - Heading".format(project_name))

    # Combine the data into a Data frame for ColumnDataSource for the plot
    p2.line(x='datetime', y='heading', source=ColumnDataSource(heading_df), line_width=5, line_color="White")
    p2.xaxis.axis_label = "DateTime"
    p2.yaxis.axis_label = 'heading'

    # Save Magnitude HTML
    file_name = project_name + '{}_heading.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    output_file(file_name, title="{} - Heading".format(project_name))
    save(gridplot([[p2]], sizing_mode='stretch_both'))  # Just save to file