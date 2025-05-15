FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Installation des dépendances générales
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libgtk-3-0 \
    libnss3 \
    fonts-liberation \
    xdg-utils

# Installation de Google Chrome
RUN wget --no-check-certificate "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" -O /tmp/chrome.deb
RUN dpkg -i /tmp/chrome.deb || apt-get -fy install
RUN rm /tmp/chrome.deb

# Téléchargement et installation de ChromeDriver (adaptez la version selon votre besoin)
ARG CHROME_DRIVER_VERSION=136.0.7103.113
RUN wget "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver_linux64.zip -d /opt/
RUN chmod 755 /opt/chromedriver
RUN ln -s /opt/chromedriver /usr/local/bin/chromedriver

# Copie du code de l'application
COPY . .


# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]