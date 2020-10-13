THIS PROJECT IS CURRENTLY OUTDATED, WILL UPDATE SOON.

Twitch Selenium Automation

Features:

--> browser headless-mode idler when running without graphic

--> channel points farmer when running with graphic

# Requirements: Docker

Tutorial: 
1) Make a clone of this repositorie 

$ git clone https://github.com/stevanstetzvanin/twdocker.git

2) Go inside the folder

$ cd twdocker

3) Edit the file data.json with your twitch credentials and the channels you want to idle

4) Execute the docker command

$ docker run -it  -v $PWD/data.json:/usr/src/app/data.json joaobruno/docker:1.1

