import os
from fetch_info_stocks import FinancialDataFetcher
from add_pcr import PutCallRatioAdder
from construct_portfolio import ConstructPortfolio
from evaluate_portfolio import EvaluatePortfolio

def main():
    # Step 1: Fetch Financial Data
    print("\n=== Fetching Financial Data ===")
    SYMBOLS = {
        "Total Energies": "TTE.PA",
        "FMC Corp": "FMC",
        "BP PLC": "BP",
        "Stora Enso": "STE",
        "BHP Group": "BHP"
    }
    START_DATE = "2019-01-01"
    END_DATE = "2024-12-31"
    output_stock_info = "new_data/stock_infos"

    fetcher = FinancialDataFetcher(SYMBOLS, START_DATE, END_DATE)
    fetcher.export_to_csv(output_stock_info)

    # Step 2: Add Put-Call Ratio Data
    print("\n=== Adding Put-Call Ratio Data ===")
    output_full_data = "new_data/full_data"
    pcr_adder = PutCallRatioAdder(output_full_data)

    pcr_adder.add_put_call_ratio_us(
        os.path.join(output_stock_info, "FMC_Corp_financial_data.csv"),
        "new_data/webscrapped_call_put_ratio/ratios.csv",
        "FMC Corp"
    )
    pcr_adder.add_put_call_ratio_us(
        os.path.join(output_stock_info, "BHP_Group_financial_data.csv"),
        "new_data/webscrapped_call_put_ratio/ratios.csv",
        "BHP Group"
    )
    pcr_adder.add_put_call_ratio_eu(
        os.path.join(output_stock_info, "BP_PLC_financial_data.csv"),
        "new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv",
        "BP PLC"
    )
    pcr_adder.add_put_call_ratio_eu(
        os.path.join(output_stock_info, "Stora_Enso_financial_data.csv"),
        "new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv",
        "Stora Enso"
    )
    pcr_adder.add_put_call_ratio_eu(
        os.path.join(output_stock_info, "Total_Energies_financial_data.csv"),
        "new_data/direct_download_call_put/Put_Call Ratio STOXX50 - Données Historiques.csv",
        "Total Energies"
    )

    # Step 3: Construct Portfolio
    print("\n=== Constructing Portfolio ===")
    file_paths = [
        os.path.join(output_full_data, "BHP_Group_updated_financial_data.csv"),
        os.path.join(output_full_data, "BP_PLC_updated_financial_data.csv"),
        os.path.join(output_full_data, "FMC_Corp_updated_financial_data.csv"),
        os.path.join(output_full_data, "Stora_Enso_updated_financial_data.csv"),
        os.path.join(output_full_data, "Total_Energies_updated_financial_data.csv")
    ]
    stock_names = ["BHP_Group", "BP_PLC", "FMC_Corp", "Stora_Enso", "Total_Energies"]
    bullish_threshold = -1
    bearish_threshold = 1

    portfolio_constructor = ConstructPortfolio(file_paths, stock_names)
    portfolio_constructor.merge_put_call_ratios()
    portfolio_constructor.calculate_signals(bullish_threshold, bearish_threshold)
    portfolio_constructor.calculate_dynamic_portfolio_weights()
    portfolio_weights_file = "new_data/portfolio_weights.csv"
    portfolio_constructor.save_weights_to_csv(portfolio_weights_file)

    # Step 4: Evaluate Portfolio
    print("\n=== Evaluating Portfolio Performance ===")
    stock_files = {
        "BHP": file_paths[0],
        "BP": file_paths[1],
        "FMC": file_paths[2],
        "Stora_Enso": file_paths[3],
        "Total_Energies": file_paths[4]
    }
    
    evaluator = EvaluatePortfolio(stock_files, portfolio_weights_file)
    metrics = evaluator.run_analysis()

    print("\n=== Portfolio Performance Metrics ===")
    print(metrics)

if __name__ == "__main__":
    main()



