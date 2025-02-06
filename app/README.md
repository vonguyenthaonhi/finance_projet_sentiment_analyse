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



### 2. Lancer avec Docker (recommandé) 🐳
You can also deploy the application via Docker. Make sure you have Docker installed first.
```
docker pull lucasvazelle/webappfinance
docker run -p 8000:8000 lucasvazelle/webappfinance
```
Excecute http://localhost:8000/ on your Browser
