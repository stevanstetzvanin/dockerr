FROM python:3
LABEL version="1.2" description="Automação Twitch" maintainer="João Bruno, Stevan Stetz"
WORKDIR /usr/src/app
COPY /99pin-unstable /etc/apt/preferences.d/99pin-unstable
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" | tee -a /etc/apt/sources.list && apt update -y && apt upgrade -y && apt install -y python-pip && pip install selenium
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz && tar -xvzf geckodriver-v0.24.0-linux32.tar.gz && chmod +x geckodriver && mkdir drivers && mv geckodriver /usr/src/app/drivers/geckodriver
RUN apt-get -y install firefox-esr
COPY /twitch.py /usr/src/app/twitch.py
RUN /bin/bash -c 'chmod +x /usr/src/app/twitch.py'
CMD [ "python", "/usr/src/app/twitch.py" ]
