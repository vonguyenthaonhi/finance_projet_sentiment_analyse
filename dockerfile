FROM ubuntu:20.04

RUN apt update && apt-get install -y curl && apt-get install -y python3 && apt-get install -y python3-pip

RUN mkdir -p /home/finance_projet/webapp_put_call

# Installer Google Chrome stable
ENV DEBIAN_FRONTEND=noninteractive

RUN wget -q -O - https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > google-chrome.deb \
    && dpkg -i google-chrome.deb \
    && apt-get install -f -y \
    && rm google-chrome.deb

# Installer ChromeDriver via WebDriverManager (cela gère automatiquement les versions)
RUN pip3 install webdriver-manager

WORKDIR /home/finance_projet/webapp_put_call

COPY . .

RUN chmod +x *.sh

RUN python3 -m pip install -r requirements.txt

WORKDIR /app


# Commande pour lancer FastAPI avec uvicorn (backend)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
