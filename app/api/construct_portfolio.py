import pandas as pd


class ConstructPortfolio:
    """
    A class to analyze Put-Call Ratios, generate trading signals, and compute dynamic portfolio weights.
    """

    def __init__(self, file_paths, stock_names):
        self.file_paths = file_paths
        self.stock_names = stock_names
        self.merged_data = None
        self.signal_data = None
        self.weight_data = None

    def merge_put_call_ratios(self):
        """
        Merges 'Put-Call Ratio' data for multiple stocks into a single DataFrame aligned by date.
        """
        stock_data = {
            name: pd.read_csv(file_path)
            for name, file_path in zip(self.stock_names, self.file_paths)
        }
        put_call_ratios = {
            name: df[["Date", "Put-Call Ratio"]] for name, df in stock_data.items()
        }
        merged_data = None

        for name, df in put_call_ratios.items():
            df = df.rename(columns={"Put-Call Ratio": name})
            if merged_data is None:
                merged_data = df
            else:
                merged_data = pd.merge(merged_data, df, on="Date", how="outer")

        merged_data["Date"] = pd.to_datetime(merged_data["Date"])
        merged_data.set_index("Date", inplace=True)
        self.merged_data = merged_data

    def calculate_signals(self, bullish_threshold, bearish_threshold):
        """
        Calculates trading signals based on Put-Call Ratio.
        """
        if self.merged_data is None:
            raise ValueError(
                "Merged data is not available. Run merge_put_call_ratios first."
            )

        signal_data = self.merged_data.copy()

        for stock in self.stock_names:
            signal_data[f"{stock}_Signal"] = self._generate_signals(
                signal_data[stock], bullish_threshold, bearish_threshold
            )

        self.signal_data = signal_data

    @staticmethod
    def _generate_signals(put_call_ratios, bullish_threshold, bearish_threshold):
        """
        Generates buy/sell/hold signals based on Put-Call Ratio trends.
        """
        streak = 0
        signals = []
        for ratio in put_call_ratios:
            if ratio < bullish_threshold:
                streak += 1
            elif ratio > bearish_threshold:
                streak -= 1
            else:
                streak = 0  # Reset for neutral

            if streak >= 3:
                signals.append("Buy")
            elif streak <= -3:
                signals.append("Sell")
            else:
                signals.append("Hold")
        return signals

    def calculate_dynamic_portfolio_weights(self):
        """
        Calculates daily portfolio weights dynamically based on signal data for multiple stocks,
        while ensuring constraints on max and min exposure per stock.
        """
        if self.signal_data is None:
            raise ValueError(
                "Signal data is not available. Run calculate_signals first."
            )

        initial_weight = 1 / len(self.stock_names)
        weight_data = pd.DataFrame(index=self.signal_data.index)

        for stock in self.stock_names:
            weight_data[f"{stock}_Weight"] = initial_weight

        for i in range(1, len(weight_data)):
            total_weight = 0
            for stock in self.stock_names:
                prev_weight = weight_data.iloc[
                    i - 1, weight_data.columns.get_loc(f"{stock}_Weight")
                ]
                signal = self.signal_data.iloc[
                    i, self.signal_data.columns.get_loc(f"{stock}_Signal")
                ]

                if signal == "Buy":
                    new_weight = min(
                        prev_weight * 1.1, 0.40
                    )  # Increase by 10%, max 40% (before normalization)
                elif signal == "Sell":
                    new_weight = max(
                        prev_weight * 0.90, 0.05
                    )  # Decrease by 10%, min 5% (before normalization)
                else:
                    new_weight = prev_weight  # Hold

                weight_data.iloc[i, weight_data.columns.get_loc(f"{stock}_Weight")] = (
                    new_weight
                )
                total_weight += new_weight

            # Normalize weights to ensure the total portfolio sums to 1
            for stock in self.stock_names:
                weight_data.iloc[
                    i, weight_data.columns.get_loc(f"{stock}_Weight")
                ] /= total_weight

        self.weight_data = weight_data

    def save_weights_to_csv(self, file_path):
        """
        Saves the normalized portfolio weights to a CSV file.
        """
        if self.weight_data is None:
            raise ValueError(
                "Weight data is not available. Run calculate_dynamic_portfolio_weights first."
            )

        self.weight_data.to_csv(file_path)


# Example usage
if __name__ == "__main__":
    file_paths = [
        "new_data/full_data/BHP_Group_updated_financial_data.csv",
        "new_data/full_data/BP_PLC_updated_financial_data.csv",
        "new_data/full_data/FMC_Corp_updated_financial_data.csv",
        "new_data/full_data/Stora_Enso_updated_financial_data.csv",
        "new_data/full_data/Total_Energies_updated_financial_data.csv",
    ]
    stock_names = ["BHP_Group", "BP_PLC", "FMC_Corp", "Stora_Enso", "Total_Energies"]
    bullish_threshold = -1
    bearish_threshold = 1

    pcranalyzer = ConstructPortfolio(file_paths, stock_names)
    pcranalyzer.merge_put_call_ratios()
    pcranalyzer.calculate_signals(bullish_threshold, bearish_threshold)
    pcranalyzer.calculate_dynamic_portfolio_weights()
    pcranalyzer.save_weights_to_csv("new_data/portfolio_weights.csv")
