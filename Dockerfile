FROM python:3
LABEL version="1.0.0" description="Automação Twich" maintainer="João Bruno, Stevan Stetz"
WORKDIR /usr/src/app
COPY /99pin-unstable /etc/apt/preferences.d/99pin-unstable
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" | tee -a /etc/apt/sources.list && apt update -y && apt upgrade -y && apt install -y python-pip && apt install -y python3-pip && pip install selenium &&  python3 -m pip install pyvirtualdisplay 
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux32.tar.gz && tar -xvzf geckodriver-v0.24.0-linux32.tar.gz && chmod +x geckodriver && mv geckodriver /usr/local/bin/geckodriver
RUN wget http://ftp.us.debian.org/debian/pool/main/f/firefox/firefox_80.0-1_amd64.deb && dpkg -i firefox_80.0-1_amd64.deb && apt-get install -f --install
COPY /twitch.py /usr/src/app/twitch.py
RUN /bin/bash -c 'chmod +x /usr/src/app/twitch.py'
CMD [ "python", "/usr/src/app/twitch.py" ]
