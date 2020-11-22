# start from base
FROM selenium/standalone-firefox:latest

RUN sudo apt-get -yqq update                            &&\
    sudo apt-get -yqq install python3-pip python3-dev   &&\
    pip3 install selenium                               &&\
    pip3 install beautifulsoup4





