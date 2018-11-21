FROM    ubuntu:18.04
MAINTAINER  chajee308@gmail.com

# 패키지 업그레이드, python3 설치
RUN     apt -y update
RUN     apt -y dist-upgrade
RUN     apt -y install python3-pip

# docker build할때의 PATH해 해당하는 폴더의 전체 내용을
# Image의 /srv/project/폴더 내부에 복사
COPY        requirements_production.txt /tmp/requirements.txt
RUN         pip3 install -r /tmp/requirements.txt

COPY        ./  /srv/project
WORKDIR     /srv/project

ENV         DJANGO_SETTINGS_MODULE config.settings.production

# 프로세스를 실행할 명령
WORKDIR     /srv/project/app
#RUN         python3 manage.py runserver