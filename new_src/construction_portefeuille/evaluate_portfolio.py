import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class EvaluatePortfolio:
    """A class for analyzing portfolio performance against a benchmark."""

    def __init__(self, stock_files, portfolio_weights_path, benchmark_ticker="XLE"):
        self.stock_files = stock_files
        self.portfolio_weights_path = portfolio_weights_path
        self.benchmark_ticker = benchmark_ticker
        self.stock_data = {}
        self.full_data = None
        self.daily_portfolio_returns = None
        self.benchmark_returns = None
        self.performance_metrics = None

    def load_data(self):
        """Load stock and portfolio weight data."""
        portfolio_weights_df = pd.read_csv(self.portfolio_weights_path)
        portfolio_weights_df["Date"] = pd.to_datetime(portfolio_weights_df["Date"])

        self.stock_data = {}

        for ticker, path in self.stock_files.items():
            df = pd.read_csv(path, parse_dates=["Date"])  
            self.stock_data[ticker] = df[["Date", "Daily Return"]] 

        merged_stock_data = list(self.stock_data.values())[0]
        for ticker, df in self.stock_data.items():
            if ticker != "BHP":  # Skip the first since it's already initialized
                merged_stock_data = merged_stock_data.merge(
                    df, on="Date", how="inner", suffixes=("", f"_{ticker}")
                )

        column_mapping = {
            "Daily Return": "BHP",
            "Daily Return_BP": "BP",
            "Daily Return_FMC": "FMC",
            "Daily Return_Stora_Enso": "Stora_Enso",
            "Daily Return_Total_Energies": "Total_Energies"
        }
        
        self.full_data = merged_stock_data.merge(portfolio_weights_df, on="Date", how="inner")
        self.full_data.rename(columns=column_mapping, inplace=True)
        self.full_data.set_index("Date", inplace=True)

    def extract_stock_returns_and_weights(self):
        """
        Extracts stock returns and corresponding portfolio weights from the dataset.
        
        :return: Tuple of DataFrames (stock_returns, stock_weights)
        """
        available_stocks = [col for col in self.stock_files.keys() if col in self.full_data.columns]
        
        returns_columns = ["BHP", "BP", "FMC", "Stora_Enso", "Total_Energies"]
        weights_columns = [
            "BHP_Group_Normalized_Weight", "BP_PLC_Normalized_Weight", 
            "FMC_Corp_Normalized_Weight", "Stora_Enso_Normalized_Weight", 
            "Total_Energies_Normalized_Weight"
        ]
        
        stock_returns = self.full_data[returns_columns]
        stock_weights = self.full_data[weights_columns]
        stock_weights.columns = returns_columns 
        
        return stock_returns, stock_weights

    def compute_daily_portfolio_returns(self):
        """
        Computes daily weighted portfolio returns.
        
        :return: Series representing daily portfolio returns.
        """
        stock_returns, stock_weights = self.extract_stock_returns_and_weights()
        daily_portfolio_returns = (stock_returns * stock_weights).sum(axis=1)
        return daily_portfolio_returns
    
    def fetch_benchmark_data(self):
        """Fetch and process benchmark data."""
        benchmark_data = yf.download(self.benchmark_ticker, start=self.full_data.index.min(), end=self.full_data.index.max())
        benchmark_prices = benchmark_data["Close"].reindex(self.full_data.index).fillna(method='ffill')
        self.benchmark_returns = benchmark_prices.pct_change().dropna()
        
    def compute_performance_metrics(self):
        """Compute portfolio and benchmark performance metrics."""
        cumulative_portfolio_returns = (1 + self.daily_portfolio_returns).cumprod()
        cumulative_benchmark_returns = (1 + self.benchmark_returns).cumprod()
        
        portfolio_volatility = self.daily_portfolio_returns.std() * np.sqrt(252)
        benchmark_volatility = self.benchmark_returns.std() * np.sqrt(252)
        
        portfolio_cagr = (cumulative_portfolio_returns.iloc[-1]) ** (1 / max(1, (len(self.daily_portfolio_returns) / 252))) - 1
        benchmark_cagr = (cumulative_benchmark_returns.iloc[-1]) ** (1 / max(1, (len(self.benchmark_returns) / 252))) - 1 if not cumulative_benchmark_returns.empty else np.nan
        
        portfolio_sharpe = portfolio_cagr / portfolio_volatility
        benchmark_sharpe = benchmark_cagr / benchmark_volatility
        
        self.performance_metrics = pd.DataFrame({
            "Metric": ["CAGR", "Volatility", "Sharpe Ratio", ],
            "Portfolio": [portfolio_cagr, portfolio_volatility, portfolio_sharpe],
            "Benchmark (SPN/XLE)": [benchmark_cagr, benchmark_volatility, benchmark_sharpe]
        })

        self.performance_metrics.to_csv("new_data/performance_metrics.csv", index=False)
        
    def plot_performance(self):
        """Plot cumulative returns of the portfolio vs. the benchmark."""
        cumulative_portfolio_returns = (1 + self.daily_portfolio_returns).cumprod()
        cumulative_benchmark_returns = (1 + self.benchmark_returns).cumprod()
        
        plt.figure(figsize=(10, 5))
        plt.plot(cumulative_portfolio_returns, label="Portfolio", linewidth=2)
        plt.plot(cumulative_benchmark_returns, label="Benchmark (XLE)", linewidth=2)
        plt.title("Portfolio vs. Benchmark Performance")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.legend()
        plt.grid()
        plt.show()

    def run_analysis(self):
        """Run the full analysis pipeline."""
        self.load_data()
        self.extract_stock_returns_and_weights()
        self.daily_portfolio_returns = self.compute_daily_portfolio_returns()
        self.fetch_benchmark_data()
        self.compute_performance_metrics()
        self.plot_performance()
        
        return self.performance_metrics


# Example Usage
if __name__ == "__main__":
    stock_files = {
        "BHP": "new_data/full_data/BHP_Group_updated_financial_data.csv",
        "BP": "new_data/full_data/BP_PLC_updated_financial_data.csv",
        "FMC": "new_data/full_data/FMC_Corp_updated_financial_data.csv",
        "Stora_Enso": "new_data/full_data/Stora_Enso_updated_financial_data.csv",
        "Total_Energies": "new_data/full_data/Total_Energies_updated_financial_data.csv"
    }
    portfolio_weights_path = "new_data/portfolio_weights.csv"
    
    analyzer = EvaluatePortfolio(stock_files, portfolio_weights_path)
    metrics = analyzer.run_analysis()
    print(metrics)