# Project3
INFOTC 4320 Project 3/3a: Stock Data Visualizer

## Project Requirements:
The application should:
   1. Ask the user to enter the stock symbol for the company they want data for.
   2. Ask the user for the chart type they would like.
   3. Ask the user for the time series function they want the api to use.
   4. Ask the user for the beginning date in YYYY-MM-DD format.
   5. Ask the user for the end date in YYYY-MM-DD format.
   6. The end date should not be before the begin date
   7. Generate a graph and open in the user’s default browser.

## 3a Requirments
  1. Create a flask application for your project
  2. Write code to populate the form with stock symbols
  3. Containerize the application using Docker

## Project Structure Overview:

### Main Module (`main.py`):
- Entry point of the application.
- Orchestrates user interaction, gathers input, and calls necessary functions from other modules.

### User Input Module (`userInput.py`):
- Handles user interaction by providing functions to prompt the user for input.
- Functions include:
  - `getStockSymbol()`: Prompts for the stock symbol.
  - `getChartType()`: Prompts for the chart type.
  - `getTimeSeriesFunction()`: Prompts for the time series function.
  - `getStartDate()`: Prompts for the start date.
  - `getEndDate()`: Prompts for the end date.

### Time Series Functions Module (`timeSeriesFunctions.py`):
- Provides functions to prompt the user for selecting the time series function they want the API to use.
- Functions include:
  - `getTimeSeriesFunction()`: Presents options for choosing time series functions like Intraday, Daily, Weekly, and Monthly.

### Data Fetcher Module (`dataFetcher.py`):
- Responsible for fetching data from the Alpha Vantage API.
- Functions include:
  - `getStockData()`: Constructs API URL based on user input, sends a request, and retrieves JSON response containing stock data.

### Graph Generator Module (`graphGenerator.py`):
- Responsible for generating graphs based on the fetched stock data.
- Functions include:
  - `generateGraph()` to create visual representations of the data, using libraries like Matplotlib or Plotly.

### Additional Files:
- `.gitignore`: Specifies which files and directories Git should ignore, such as Python bytecode files (*.pyc).

### Workflow:
1. The user runs `main.py` to start the application.
2. They are prompted to input the stock symbol, chart type, time series function, start date, and end date.
3. User input is validated, and the appropriate API URL is constructed.
4. The application fetches data from the Alpha Vantage API using `dataFetcher.py`.
5. If data is successfully retrieved, it's used to generate graphs.
6. Any errors or exceptions encountered during the process are appropriately handled and displayed to the user.

## How to run using docker
Prerequisites
Before starting, make sure the user has Docker and Docker Compose installed on their machine. 
- Install Docker
- Install Docker Compose

Once installing the project from https://github.com/ColinBuchheit/Project3a , open the folder in either a cmd terminal or inside an IDE and run this through the project terminal.  

Run these commands

1. docker-compose up
automatically build the images if they are not already built and start all services defined in docker-compose.yml.
  optionally run 'docker-compose up -d' for running Docker Compose in detached mode

2. Open your web browser and go to http://localhost:5000


