### The Put-Call Ratio as a Sentiment Indicator: Impact on Portfolio Performance and Risk Management. Application to the energy sector

## The project 
This project explores the use of the Put-Call Ratio (PCR) as a sentiment indicator for portfolio management and risk estimation in the energy sector. The objective is to determine whether the PCR can be used as an alternative to AI-based sentiment analysis models by studying:

The relationship between PCR (US and Europe) and stock returns using cross-correlation analysis.
The effectiveness of PCR as an investment signal, by integrating its influence into a dynamic portfolio strategy.
The impact of PCR on risk management by comparing Historical VaR and Sentiment Adjusted VaR.

## Project structure

📁 new_data/ (Raw data and collection scripts)

- 📂 webscraping/ → Scripts to retrieve the US and European Put-Call Ratio.
- 📂 portfolio/ → Data formatting and implementation of the sentiment-based portfolio model.
- 📄 données_rendement/ → Historical stock returns collected from Yahoo Finance with yfinance.


📁 new_output/ (Results and visualisations)

📊 Charts and analysis → Visualisations of cross-correlations and VaR (Historical vs Adjusted).
📄 Results files → Data and calculations of risk and sentiment indicators.

📁 domain/ (Analysis scripts and statistical models).
📄 correlation_croisee_put_call_and_series.py → Analysis of cross-correlations between PCR and yields.
📄 var_analysis.py → Calculation of Historical and Adjusted VaR with integration of PCR.
