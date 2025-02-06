### API with fast api et frontend 

This app allow to visualize, launch webscrap, calculate weights in a porfolio based on energies stocks.

### 1. Lancer l'application en local 💻

First, clone the repository and activate your virtual environment. Install Chrome and dependencies (see README.MD at the base of the project).

#### Backend

1. 📄 Launch api server 
 ```

uvicorn main:app --reload --port 8000
 ```

#### Frontend


2 📊 On other terminal, Launch the streamlit app

 ```
streamlit run frontend.py --server.port 8001 
 ```



### 2. Launch with Docker (recommended) 🐳

#### prerequisite

You can also deploy the application with Docker. Make sure you have Docker installed first.

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

#### 1. First way

Run **from the root** of the Git repository
```
docker-compose pull 
docker-compose up -d
```
Excecute http://localhost:8000/ on your Browser for backend api
Excecute http://localhost:8501/ on your Browser for frontend 


#### 1. Second way

Run **from the root** of the Git repository

```
docker pull lucasvazelle/finance_projet_sentiment_analyse-backend
docker pull lucasvazelle/finance_projet_sentiment_analyse-frontend
docker-compose up -d
```
Excecute http://localhost:8000/ on your Browser for backend api
Excecute http://localhost:8501/ on your Browser for frontend 

