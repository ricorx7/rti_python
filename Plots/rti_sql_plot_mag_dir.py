from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, save, output_file
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar, Range1d
from bokeh.transform import transform
from bokeh.palettes import RdBu, Spectral, RdYlBu, RdGy, YlGnBu, Inferno, Plasma, PuBu, Greys, Magma, Viridis

import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import rti_python.Plots.dataframe_html_table_summary as df_summary
import rti_python.Plots.csv_summary as csv_summary


def plot_mag_dir(project_name, adcp, earth_vel_east_df, earth_vel_north_df, num_bins, bt_range_df=None, ss_code=None, ss_config=None, max_vel=80.0, smoothing='hamming', smoothing_win=50, flip_y_axis=False):
    """
    Create a magnitude and direction plots.  This will use the incoming East and North velocities.
    :param project_name: Project name for the file name.
    :param adcp: ADCP information.
    :param earth_vel_east_df: East velocity dataframe. [ensnum, numbeams, numbins, beam, bin0 ... bin199]
    :param earth_vel_north_df: North velocity dataframe. [ensnum, numbeams, numbins, beam, bin0 ... bin199]
    :param num_bins: Number of bins to plot.
    :param bt_range_df: Average depth for each ensemble.
    :param ss_code: Subsystem code.
    :param ss_config: Subsystem Config Index.
    :param max_vel: Maximum velocity to remove the BAD_Velocity and screen data.
    :param smoothing: Smoothing function to use. (boxcar,blackman,hamming,bartlett,blackmanharris,NONE)
    :param smoothing_win: Smoothing window.
    :param flip_y_axis: Flip the x axis so minimum is at top.
    :return:
    """
    # BAD VELOCITY
    BAD_VEL = 88.888

    # Scale factor to allow the quivers to fit on the screen
    SCALE_FACTOR = 1

    # Check for data to plot
    if earth_vel_north_df is None or earth_vel_east_df is None:
        return

    # If there is no data, than we cannot create a plot
    if earth_vel_east_df.empty or earth_vel_north_df.empty:
        return

    # Create a default subsystem query string
    ss_str = "_{}_{}".format(ss_config, ss_code)

    # Get the number of bins in the df
    # Get the number of ensembles in the df
    if num_bins <= 0:
        num_bins = adcp['numbins']
    num_ens = len(earth_vel_east_df.index)

    # Init the data
    x0_ens = []
    y0_ens = []
    x1_ens = []
    y1_ens = []
    length_vals = []
    speed_vals = []

    # Clean up the data
    earth_vel_east_df = earth_vel_east_df.drop(['ensnum', 'numbeams', 'numbins', 'beam'], axis=1)      # Ensemble number and beam column not needed
    earth_vel_north_df = earth_vel_north_df.drop(['ensnum', 'numbeams', 'numbins', 'beam'], axis=1)    # Ensemble number and beam column not needed
    earth_vel_east_df = earth_vel_east_df.interpolate()                         # Fill in any missing data (mean of prev/next)
    earth_vel_north_df = earth_vel_north_df.interpolate()                       # Fill in any missing data
    earth_vel_east_df = earth_vel_east_df.replace([None], 0.0)                  # Remove None so we can square
    earth_vel_north_df = earth_vel_north_df.replace([None], 0.0)                # Remove None so we can square
    earth_vel_east_df[earth_vel_east_df >= max_vel] = 0.0                       # Values marked bad set to 0
    earth_vel_north_df[earth_vel_north_df >= max_vel] = 0.0                     # Values marked bad set to 0

    # DataTable and CSV for East and North Velocity
    file_name = project_name + '{}_Summary East Velocity.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    df_summary.generate_html_page(file_name, project_name, "Summary East Velocity", earth_vel_east_df)
    file_name = project_name + '{}_Summary East Velocity.csv'.format(ss_str)
    file_name = os.path.join('html', file_name)
    csv_summary.generate_csv(file_name, earth_vel_east_df)
    file_name = project_name + '{}_Summary North Velocity.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    df_summary.generate_html_page(file_name, project_name, "Summary North Velocity", earth_vel_north_df)
    file_name = project_name + '{}_Summary North Velocity.csv'.format(ss_str)
    file_name = os.path.join('html', file_name)
    csv_summary.generate_csv(file_name, earth_vel_north_df)


    # Calculate the magnitude
    df_mag = pd.DataFrame(np.sqrt(np.square(earth_vel_east_df) + np.square(earth_vel_north_df)))
    df_mag[df_mag >= max_vel] = 0.0  # Values marked bad set to 0
    # df_mag[(~(np.abs(df_mag-df_mag.mean()) > (1*df_mag.std())))] = 0.0
    # df_mag[(np.abs(df_mag-df_mag.mean())<=(5.0*df_mag.std()))] = 0.0
    # print(df_mag)

    # Average the data
    if smoothing:
        df_mag = df_mag.rolling(window=smoothing_win, win_type=smoothing).mean()
        df_mag = df_mag.replace([None], 0.0)                # Remove NaN

        if bt_range_df is not None and not bt_range_df.empty:
            print(bt_range_df)
            bt_range_df["SmoothedBinRange"] = bt_range_df["BinRange"].rolling(window=5).mean()
            #bt_range_df["BinRange"] = bt_range_df["SmoothedBinRange"].bfill()         # bfill used to replace NaN for the first window values with the first good value
            bt_range_df["BinRange"] = bt_range_df["BinRange"].interpolate()           # Fill in any missing data (mean of prev/next)
            print(bt_range_df)

    # Calculate the direction
    df_dir = pd.DataFrame(np.degrees(np.arctan2(earth_vel_east_df, earth_vel_north_df)))

    # Create the quivers
    for index, row in df_mag.iterrows():

        for bin_loc in range(num_bins):
            bin_str = 'bin' + str(bin_loc)

            ens_loc = index
            mag = row[bin_str]
            vel_dir = df_dir.iloc[ens_loc][bin_str]
            speed_vals.append(mag)

            # Correct direction
            if vel_dir < 0:
                vel_dir = 360.0 + vel_dir

            # Apply scale factor to length
            length_val = mag / SCALE_FACTOR  # Scale the length to fit better on the screen
            length_vals.append(length_val)

            # Generate angle for water direction
            x1_val = ens_loc + length_val * np.cos(vel_dir)
            y1_val = bin_loc + length_val * np.sin(vel_dir)

            x0_ens.append(ens_loc)  # X = ensemble
            y0_ens.append(bin_loc)  # Y = bin
            x1_ens.append(x1_val)  # x1 = length and angle
            y1_ens.append(y1_val)  # y1 = length and angle

    # Turn the 2D array to 1D
    length = np.asarray(length_vals)
    speed = np.asarray(speed_vals)

    """
    # Calculate the U and V directions for the direction lines
    df_U = pd.DataFrame(-1 - earth_vel_east_df ** 2 + earth_vel_north_df)
    df_V = pd.DataFrame(1 + earth_vel_east_df - earth_vel_north_df ** 2)
    
    Y, X = np.meshgrid(xx, yy)
    #U = -1 - X ** 2 + Y
    #V = 1 + X - Y ** 2
    U = X
    V = Y
    speed = np.sqrt(U * U + V * V)
    theta = np.arctan(V / U)
    x0 = X[::2, ::2].flatten()
    y0 = Y[::2, ::2].flatten()
    length = speed[::2, ::2].flatten() / 40
    angle = theta[::2, ::2].flatten()
    x1 = x0 + length * np.cos(angle)
    y1 = y0 + length * np.sin(angle)
    xs, ys = self.streamlines(xx, yy, U.T, V.T, density=2)
    """

    # cm = np.array(["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"])  # Green / White / Red
    # cm = np.array(["#C7E9B4", "#7FCDBB", "#41B6C4", "#1D91C0", "#225EA8", "#0C2C84"])      #  Green / Blue
    #cm = np.array(['#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff'])  # Blue to white
    # cm = np.array(['#000000', '#084594', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff'])  # Black to Blue to white
    # cm = np.array(YlGnBu[9])  # 9 Is the colormap version
    cm = np.array(Spectral[11])
    # cm = np.array(Inferno[9])
    # cm = np.array(RdYlBu[9])
    #cm = np.array(Plasma[256])
    #cm = np.array(Greys[256])
    # cm = np.array(Inferno[256])
    # cm = np.array(Magma[256])
    # cm = np.array(Virdis[256])
    # cm = np.array(PuBu[9])
    # cm = np.array(['#f7fbff', '#deebf7', '#c6dbef', '#6baed6', '#9ecae1', '#4292c6', '#2171b5', '#084594'])  # White to Blue
    ix = ((length - length.min()) / (length.max() - length.min()) * 5).astype('int')
    colors = cm[ix]
    # this is the colormap from the original NYTimes plot
    mapper = LinearColorMapper(palette=cm, low=speed.min(), high=speed.max())
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                         ticker=BasicTicker(desired_num_ticks=len(cm)),
                         label_standoff=6, border_line_color=None, location=(0, 0))

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

    # Create Vector plot
    p1 = figure(x_range=(0, num_ens), y_range=(0, num_bins), tools=TOOLS, title="{} - Water Profile - Magnitude and Direction".format(project_name))
    p1.segment(x0_ens, y0_ens, x1_ens, y1_ens, color=colors, line_width=1)
    p1.xaxis.axis_label = "Ensembles"
    p1.yaxis.axis_label = 'Bins'
    if not flip_y_axis:
        p1.y_range = Range1d(num_bins, 0)
        print("Upward Facing ADCP")


    # p3 = figure(x_range=p1.x_range, y_range=p1.y_range)
    # p3.multi_line(xs, ys, color="#ee6666", line_width=2, line_alpha=0.8)

    # Combine the data into a Data frame for ColumnDataSource for the plot
    speed_df = pd.DataFrame()
    speed_df['speed'] = speed_vals
    speed_df['ens'] = x0_ens
    speed_df['bin'] = y0_ens
    source = ColumnDataSource(speed_df)

    # Create Magnitude plot
    p2 = figure(x_range=p1.x_range, y_range=p1.y_range, tools=TOOLS, toolbar_location='left',
                title="{} - Water Profile - Water Velocity".format(project_name))
    p2.rect(x='ens', y='bin', width=1, height=1, source=source, fill_color=transform('speed', mapper), dilate=True,
            line_color=None)
    p2.xaxis.axis_label = "Ensembles"
    p2.yaxis.axis_label = 'Bins'
    p2.add_layout(color_bar, 'right')
    p2.select_one(HoverTool).tooltips = [
        ('ens', '@ens'),
        ('bin', '@bin'),
        ('speed', '@speed'),
    ]
    if not flip_y_axis:
        p2.y_range = Range1d(num_bins, 0)

    # Draw the bottom track line
    if bt_range_df is not None and not bt_range_df.empty:
        # Combine the data into a Data frame for ColumnDataSource for the plot
        source_bt_range = ColumnDataSource(bt_range_df)

        p2.line(x='index', y='BinRange', source=source_bt_range, line_width=5, line_color="White")

    # Save Combined Vector and Mag HTML
    file_name = project_name + '{}_combined_vector.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    output_file(file_name, title="{} - Water Vectors and Magnitude".format(project_name))
    save(gridplot([[p1, p2]], sizing_mode='stretch_both', merge_tools=True))  # Just save to file

    # Save Vector HTML
    # New colobar created, because previous one is associated with mag plot
    color_bar1 = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                          ticker=BasicTicker(desired_num_ticks=len(cm)),
                          label_standoff=6, border_line_color=None, location=(0, 0))
    p1.add_layout(color_bar1, 'right')
    file_name = project_name + '{}_vector.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    output_file(file_name, title="{} - Water Magnitude".format(project_name))
    save(gridplot([[p1]], sizing_mode='stretch_both'))  # Just save to file

    # Save Magnitude HTML
    file_name = project_name + '{}_mag.html'.format(ss_str)
    file_name = os.path.join('html', file_name)
    output_file(file_name, title="{} - Water Vectors".format(project_name))
    save(gridplot([[p2]], sizing_mode='stretch_both'))  # Just save to file


def streamlines(self, x, y, u, v, density=1):
    ''' Return streamlines of a vector flow.

    * x and y are 1d arrays defining an *evenly spaced* grid.
    * u and v are 2d arrays (shape [y,x]) giving velocities.
    * density controls the closeness of the streamlines. For different
      densities in each direction, use a tuple or list [densityx, densityy].

    '''

    # Set up some constants - size of the grid used.
    NGX = len(x)
    NGY = len(y)

    # Constants used to convert between grid index coords and user coords.
    DX = x[1]-x[0]
    DY = y[1]-y[0]
    XOFF = x[0]
    YOFF = y[0]

    # Now rescale velocity onto axes-coordinates
    u = u / (x[-1]-x[0])
    v = v / (y[-1]-y[0])
    speed = np.sqrt(u*u+v*v)
    # s (path length) will now be in axes-coordinates, but we must
    # rescale u for integrations.
    u *= NGX
    v *= NGY
    # Now u and v in grid-coordinates.

    NBX = int(30*density)
    NBY = int(30*density)
    blank = np.zeros((NBY,NBX))

    bx_spacing = NGX/float(NBX-1)
    by_spacing = NGY/float(NBY-1)

    def blank_pos(xi, yi):
        return int((xi / bx_spacing) + 0.5), \
               int((yi / by_spacing) + 0.5)

    def value_at(a, xi, yi):
        if type(xi) == np.ndarray:
            x = xi.astype(np.int)
            y = yi.astype(np.int)
        else:
            x = np.int(xi)
            y = np.int(yi)

        a00 = a[y,x]
        a01 = a[y,x+1]
        a10 = a[y+1,x]
        a11 = a[y+1,x+1]
        xt = xi - x
        yt = yi - y
        a0 = a00*(1-xt) + a01*xt
        a1 = a10*(1-xt) + a11*xt
        return a0*(1-yt) + a1*yt

    def rk4_integrate(x0, y0):
        # This function does RK4 forward and back trajectories from
        # the initial conditions, with the odd 'blank array'
        # termination conditions. TODO tidy the integration loops.

        def f(xi, yi):
            dt_ds = 1./value_at(speed, xi, yi)
            ui = value_at(u, xi, yi)
            vi = value_at(v, xi, yi)
            return ui*dt_ds, vi*dt_ds

        def g(xi, yi):
            dt_ds = 1./value_at(speed, xi, yi)
            ui = value_at(u, xi, yi)
            vi = value_at(v, xi, yi)
            return -ui*dt_ds, -vi*dt_ds

        check = lambda xi, yi: xi>=0 and xi<NGX-1 and yi>=0 and yi<NGY-1

        bx_changes = []
        by_changes = []

        # Integrator function
        def rk4(x0, y0, f):
            ds = 0.01               # min(1./NGX, 1./NGY, 0.01)
            stotal = 0
            xi = x0
            yi = y0
            xb, yb = blank_pos(xi, yi)
            xf_traj = []
            yf_traj = []
            while check(xi, yi):
                # Time step. First save the point.
                xf_traj.append(xi)
                yf_traj.append(yi)
                # Next, advance one using RK4
                try:
                    k1x, k1y = f(xi, yi)
                    k2x, k2y = f(xi + .5*ds*k1x, yi + .5*ds*k1y)
                    k3x, k3y = f(xi + .5*ds*k2x, yi + .5*ds*k2y)
                    k4x, k4y = f(xi + ds*k3x, yi + ds*k3y)
                except IndexError:
                    # Out of the domain on one of the intermediate steps
                    break
                xi += ds*(k1x+2*k2x+2*k3x+k4x) / 6.
                yi += ds*(k1y+2*k2y+2*k3y+k4y) / 6.
                # Final position might be out of the domain
                if not check(xi, yi): break
                stotal += ds
                # Next, if s gets to thres, check blank.
                new_xb, new_yb = blank_pos(xi, yi)
                if new_xb != xb or new_yb != yb:
                    # New square, so check and colour. Quit if required.
                    if blank[new_yb,new_xb] == 0:
                        blank[new_yb,new_xb] = 1
                        bx_changes.append(new_xb)
                        by_changes.append(new_yb)
                        xb = new_xb
                        yb = new_yb
                    else:
                        break
                if stotal > 2:
                    break
            return stotal, xf_traj, yf_traj

        integrator = rk4

        sf, xf_traj, yf_traj = integrator(x0, y0, f)
        sb, xb_traj, yb_traj = integrator(x0, y0, g)
        stotal = sf + sb
        x_traj = xb_traj[::-1] + xf_traj[1:]
        y_traj = yb_traj[::-1] + yf_traj[1:]

        # Tests to check length of traj. Remember, s in units of axes.
        if len(x_traj) < 1: return None
        if stotal > .2:
            initxb, inityb = blank_pos(x0, y0)
            blank[inityb, initxb] = 1
            return x_traj, y_traj
        else:
            for xb, yb in zip(bx_changes, by_changes):
                blank[yb, xb] = 0
            return None

    # A quick function for integrating trajectories if blank==0.
    trajectories = []

    def traj(xb, yb):
        if xb < 0 or xb >= NBX or yb < 0 or yb >= NBY:
            return
        if blank[yb, xb] == 0:
            t = rk4_integrate(xb*bx_spacing, yb*by_spacing)
            if t is not None:
                trajectories.append(t)

    # Now we build up the trajectory set. I've found it best to look
    # for blank==0 along the edges first, and work inwards.
    for indent in range((max(NBX,NBY))//2):
        for xi in range(max(NBX,NBY)-2*indent):
            traj(xi+indent, indent)
            traj(xi+indent, NBY-1-indent)
            traj(indent, xi+indent)
            traj(NBX-1-indent, xi+indent)

    xs = [np.array(t[0])*DX+XOFF for t in trajectories]
    ys = [np.array(t[1])*DY+YOFF for t in trajectories]

    return xs, ys