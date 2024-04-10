import pygal
from pygal.style import Style
import logging
import platform
import webbrowser
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# get user's default web browser command based on their platform
def get_default_browser():
    system = platform.system()
    if system == "Windows":
        return "start"
    elif system == "Darwin":  # macOS
        return "open"
    else:  # Linux, Unix, etc.
        return "xdg-open"

def generate_graph(data, chart_type, start_date, end_date, symbol):
    # chart styling
    custom_style = Style(
        background='white',
        plot_background='white',
        foreground='black',
        opacity='1',
        opacity_hover='.9',
        transition='400ms ease-in',
        colors=('red', 'blue', 'green', 'orange')
    )
    chart = pygal.Line(style=custom_style, show_legend=True,
                       title=f"Stock Data for {symbol}: {start_date} to {end_date}") if chart_type == 'line' \
        else pygal.Bar(style=custom_style, show_legend=True,
                       title=f"Stock Data for {symbol}: {start_date} to {end_date}")

    # to prevent x-axis values overlapping and improve readability
    chart.x_label_rotation = -60

    # extract dates and data values for chart
    dates = sorted(data.keys())
    chart.x_labels = dates
    opens = [data[date]["Open"] for date in dates]
    highs = [data[date]["High"] for date in dates]
    lows = [data[date]["Low"] for date in dates]
    closes = [data[date]["Close"] for date in dates]

    # add chart data
    chart.add('Open', opens)
    chart.add('High', highs)
    chart.add('Low', lows)
    chart.add('Close', closes)

       # Define the file path relative to the static directory
    # Render chart to SVG file
    file_name = f'{symbol}_{start_date}_to_{end_date}_chart.svg'
    file_path = os.path.join('static', 'graphs', file_name)  # Full path for file saving
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    chart.render_to_file(file_path)

# Log the success
    logging.info(f"Chart generated and available at {file_path}")

# Return the relative path to the saved file, without 'static/'
# At the point where you return the relative path to the saved file
    return os.path.join('graphs', file_name).replace('\\', '/')


