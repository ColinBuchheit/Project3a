from flask import Flask, render_template, request, flash, url_for
from markupsafe import Markup
import csv
from datetime import datetime
from dataFetcher import getStockData
from graphGenerator import generate_graph
import os
from time import time
from main import preprocess_data

app = Flask(__name__)

def get_stock_symbols():
    stock_symbols = []
    with open('stocks.csv', newline='') as csvfile:
        stockreader = csv.DictReader(csvfile)
        for row in stockreader:
            stock_symbols.append(row['Symbol'])
    return stock_symbols

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_symbols = get_stock_symbols()
    graph_svg = None  # Initialize graph_svg to None

    if request.method == 'POST':
        chart_type = request.form.get('chart_type')
        if chart_type not in ['bar', 'line']:
            flash('Invalid chart type selected.')
            return render_template('index.html', stock_symbols=stock_symbols, graph_svg=graph_svg)
        
        time_series = request.form.get('time_series')
        if time_series not in ['intraday', 'daily', 'weekly', 'monthly']:
            flash('Invalid time series selected.')
            return render_template('index.html', stock_symbols=stock_symbols, graph_svg=graph_svg)
        
        try:
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
            if end_date < start_date:
                flash("Error: The end date must be after the start date.")
                return render_template('index.html', stock_symbols=stock_symbols, graph_svg=graph_svg)
        except ValueError:
            flash("Error: Invalid date format. Please use YYYY-MM-DD.")
            return render_template('index.html', stock_symbols=stock_symbols, graph_svg=graph_svg)
        
        symbol = request.form.get('symbol')
        api_function = {
            "intraday": "TIME_SERIES_INTRADAY",
            "daily": "TIME_SERIES_DAILY",
            "weekly": "TIME_SERIES_WEEKLY",
            "monthly": "TIME_SERIES_MONTHLY"
        }.get(time_series, "TIME_SERIES_DAILY")
        api_key = "V6BVQP0SPVJAVA6X"
        raw_data = getStockData(symbol, api_function, api_key)

        if not raw_data:
            flash(f"Failed to fetch data for symbol: {symbol}")
        else:
            filtered_data = preprocess_data(raw_data, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if not filtered_data:
                flash("No data available for the selected date range.")
            else:
                graph_filename = generate_graph(filtered_data, chart_type, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), symbol)
                
                absolute_file_path = os.path.join(app.root_path, app.static_folder, graph_filename)
                
                try:
                    with open(absolute_file_path, 'r') as file:
                        graph_svg = Markup(file.read())
                except Exception as e:
                    flash(f"An error occurred reading the graph file: {str(e)}")

    return render_template('index.html', stock_symbols=stock_symbols, graph_svg=graph_svg)

if __name__ == '__main__':
    app.run(debug=True)
