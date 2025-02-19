### The Put-Call Ratio as a Sentiment Indicator: Impact on Portfolio Performance and Risk Management. Application to the energy sector

## The project 
This project explores the use of the Put-Call Ratio (PCR) as a sentiment indicator for portfolio management and risk estimation in the energy sector. The objective is to determine whether the PCR can be used as an alternative to AI-based sentiment analysis models by studying:

The relationship between PCR (US and Europe) and stock returns using cross-correlation analysis.
The effectiveness of PCR as an investment signal, by integrating its influence into a dynamic portfolio strategy.
The impact of PCR on risk management by comparing Historical VaR and Sentiment Adjusted VaR.

## Authors: VO Nguyen Thao Nhi, TARVERDIAN Mariam, VAZELLE Lucas

## Project structure

📁 new_data/ → Raw data, webscrapped date and final data in use

📁 new_src/ → Scripts for data processing, portfolio construction and evaluation, and risk analysis.

- 📂 webscraping/ → Scripts to retrieve the US and European Put-Call Ratio.
- 📂 construction_portefeuille/
  - Historical stock returns collected from Yahoo Finance with yfinance.
  - Data formatting and implementation of the sentiment-based portfolio model.
- 📂 domain/ → Analysis scripts and statistical models.
  - 📄 correlation_croisee_put_call_and_series.py → Analyzes the cross-correlations between the Put-Call ratio (PCR) and asset yields.
  - 📄 var_analysis.py → Calculates Historical and Adjusted VaR with the integration of PCR, providing risk estimation.

📁 new_output/ (Results and visualisations)

- 📊 Charts and analysis → Visualisations of cross-correlations, Cumulative returns (Portfolio and benchmark) and VaR (Historical vs Adjusted).
- 📄 Results files → Data and calculations of the portfolio, as well as of risk and sentiment indicators.

📁 app/ → app to visualize, launch webscrap, calculate weights in a porfolio based on energies stocks.

# Installation
1. Installer Chrome et Python 3.10

2. Cloner le dépôt GitHub :
    ```bash
    git clone https://github.com/lucasvazelle/finance_projet_sentiment_analyse.git
    cd finance_projet_sentiment_analyse
    ```
    
3. Créer l'environnement virtuel :

    - **Sur Windows** :

    ```bash
    python -m venv venv --python=python3.10
    ```

    - **Sur Linux/Mac** :
      
   ```bash
    python3.10 -m venv venv
    ```


4. Activer l'environnement virtuel

    - **Sur Windows** :

        ```bash
        .\venv\Scripts\Activate
        ```

    - **Sur Linux/Mac** :

        ```bash
        source venv/bin/activate
        ```

5. Installer les dépendances
   
    - **Sur Windows** :

    ```bash
    pip install -r requirements.txt
    pip install --upgrade typing_extensions    
    ```

    - **Sur Linux/Mac** :
  

 ## API with fast api et frontend with Docker (recommended) 🐳

This app allow to visualize, launch webscrap, calculate weights in a porfolio based on energies stocks.

#### prerequisite

You can also deploy the application with Docker. Make sure you have Docker installed first.

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### 1. First way

Run **from the root** of the Git repository

  ```bash
  docker-compose pull 
  docker-compose up -d
  ```
Excecute http://localhost:8000/ on your Browser for backend api
Excecute http://localhost:8501/ on your Browser for frontend 


#### 2. Second way

Run **from the root** of the Git repository

  ```bash
  docker pull lucasvazelle/finance_projet_sentiment_analyse-backend
  docker pull lucasvazelle/finance_projet_sentiment_analyse-frontend
  docker-compose up -d
  ```

Excecute http://localhost:8000/ on your Browser for backend api
Excecute http://localhost:8501/ on your Browser for frontend 



```bash
  python3 -m pip install -r requirements.txt
  python3 -m pip install --upgrade typing_extensions
```


