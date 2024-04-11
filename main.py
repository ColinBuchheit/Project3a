from datetime import datetime
import logging
from dataFetcher import getStockData
from userInput import getStockSymbol, getChartType, getStartDate, getEndDate
from graphGenerator import generate_graph
from timeSeriesFunctions import getTimeSeriesFunction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from datetime import datetime

def preprocess_data(raw_data, start_date, end_date):
    # Initialize container for filtered data
    filtered_data = {}

    # Define both date and datetime formats
    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'
    
    # Convert start and end dates to datetime objects for comparison
    start_datetime = datetime.strptime(start_date, date_format)
    end_datetime = datetime.strptime(end_date, date_format).replace(hour=23, minute=59, second=59)

    # Iterate through the raw data items
    for date_str, details in raw_data.items():
        # Check if the date string includes a time component
        try:
            # Attempt to parse as datetime
            date = datetime.strptime(date_str, datetime_format)
        except ValueError:
            # Fallback to date-only parsing
            date = datetime.strptime(date_str, date_format)
        
        #vheck if the date falls within the specified range
        if start_datetime <= date <= end_datetime:
            #adapt key lookup to your data structure as needed
            filtered_data[date_str] = {
                "Open": details.get("Open") or details.get("1. open"),
                "High": details.get("High") or details.get("2. high"),
                "Low": details.get("Low") or details.get("3. low"),
                "Close": details.get("Close") or details.get("4. close"),
                "Volume": details.get("Volume") or details.get("5. volume", "N/A")
            }

    return filtered_data

def main():
    apikey = "V6BVQP0SPVJAVA6X"

    print("Stock Data Visualizer")
    print("---------------------")

    #loop until user chooses to exit
    while True:
        #get stock symbol
        symbol = getStockSymbol()

        # get chart type
        chartType = getChartType()

        # get time series function
        timeSeriesFunction = getTimeSeriesFunction(symbol)

        # get start date
        startDate = getStartDate()

        # get end date
        endDate = getEndDate(startDate)

        # fetch stock data from Alpha Vantage
        raw_data = getStockData(symbol, timeSeriesFunction, apikey)
        if not raw_data:
            logging.error(f"Failed to fetch data for symbol: {symbol}")
            return

      

        # preprocess the fetched data
        formattedStartDate = startDate.strftime('%Y-%m-%d')
        formattedEndDate = endDate.strftime('%Y-%m-%d')
        data = preprocess_data(raw_data, formattedStartDate, formattedEndDate)

        # generate and display the graph
        if not data:
            logging.error("No data available for the selected date range.")
        else:
            generate_graph(data, chartType, formattedStartDate, formattedEndDate, symbol)

        # ask user to continue or exit
        choice = input("\nWould you like to view more stock data? (y/n): ").strip().lower()
        if choice != "y":
            break

if __name__ == "__main__":
    main()