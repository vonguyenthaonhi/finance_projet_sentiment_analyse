FROM ubuntu:20.04

RUN apt update && apt-get install -y curl && apt-get install -y python3 && apt-get install -y python3-pip

RUN mkdir -p /home/finance_projet/webapp_put_call

# Installer Google Chrome stable
RUN apt-get update && \
    apt-get install -y curl --fix-missing && \
    curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb --fix-missing -o Dpkg::Use-Pty=0 && \
    rm google-chrome-stable_current_amd64.deb

# Installer ChromeDriver via WebDriverManager (cela gère automatiquement les versions)
RUN pip3 install webdriver-manager

WORKDIR /home/finance_projet/webapp_put_call

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install --upgrade typing_extensions

COPY . . 

WORKDIR /home/finance_projet/webapp_put_call/app
# Commande pour lancer FastAPI avec uvicorn (backend)
CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000"]
