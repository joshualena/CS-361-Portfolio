import requests


class StockInsightCLI:
    def __init__(self):
        self.base_url = 'http://localhost:5000/'

    def fetch_stock_data(self, endpoint, params):
        try:
            response = requests.get(f'{self.base_url}{endpoint}', params=params)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
        return None

    def handle_top_stocks(self):
        print("Fetching top-performing stocks...")
        data = self.fetch_stock_data('top_stocks', {})
        if data:
            top_gainers = data[:5]  # Get the top 5 gainers
            print("Top 5 gainers:")
            for stock in top_gainers:
                self.display_stock_info(stock)
        else:
            print("Could not retrieve data.")

    def handle_bottom_stocks(self):
        print("Fetching bottom-performing stocks...")
        data = self.fetch_stock_data('bottom_stocks', {})
        if data:
            top_losers = data[:5]  # Get the top 5 losers
            print("Top 5 losers:")
            for stock in top_losers:
                self.display_stock_info(stock)
        else:
            print("Could not retrieve data.")

    def handle_daily_open_close(self):
        symbol = input("Enter the stock symbol (e.g., AAPL for Apple): ").strip().upper()
        print(f"Fetching the most recent open and close prices for {symbol}...")
        data = self.fetch_stock_data('daily_open_close', {'symbol': symbol})
        if data:
            print(f"Date: {data['date']}, Open: {data['open']}, Close: {data['close']}")
        else:
            print("Could not retrieve data.")

    # TODO: Implement news functionality

    # TODO: Implement alerts functionality

    def display_stock_info(self, stock):
        print(f"Ticker: {stock['ticker']}, Price: {stock['price']}, Change Percentage: {stock['change_percentage']}")

    def display_welcome_message(self):
        welcome_message = '''
--------------------------
|  StockInsight CLI v1.0 |
--------------------------
Welcome to StockInsight CLI! Your one-stop solution for real-time financial market insights.

Dive into the financial market with live data, from top-performing stocks to critical 
trading alerts, all at your fingertips.

Main Commands:
  - top-stocks: View top-performing stocks
  - bottom-stocks: View lowest-performing stocks
  - daily-open-close: Get the most recent open and close prices for a stock
  - alerts: Set up trading alerts
  - news: Access the latest financial news
  - help: List all commands with descriptions
  - exit: Exit the application
'''
# TODO: Add new commands to welcome prompt

        print(welcome_message)

    def run(self):
        self.display_welcome_message()

        while True:
            command = input("\nPlease enter a command (type 'help' for options): ").strip().lower()

            if command == 'exit':
                print("Exiting StockInsight CLI. Goodbye!")
                break

            elif command == 'top-stocks':
                self.handle_top_stocks()

            elif command == 'bottom-stocks':
                self.handle_bottom_stocks()

            elif command == 'daily-open-close':
                self.handle_daily_open_close()

            elif command == 'help':
                self.display_command_help()

            else:
                print(f"Unknown command: {command}. Please type 'help' for options.")

    def display_command_help(self):
        # Display available commands
        help_message = {
            'top-stocks': 'View top-performing stocks',
            'bottom-stocks': 'View lowest-performing stocks',
            'daily-open-close': 'View the most recent open and close prices for a given symbol',
            # TODO: Add new commands here
        }
        print("Available commands:")
        for cmd, description in help_message.items():
            print(f'  - {cmd}: {description}')


if __name__ == "__main__":
    stock_insight_cli = StockInsightCLI()
    stock_insight_cli.run()
