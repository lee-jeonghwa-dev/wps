FROM    ubuntu:18.04
MAINTAINER  chajee308@gmail.com

# 패키지 업그레이드, python3 설치
RUN     apt -y update
RUN     apt -y dist-upgrade
RUN     apt -y install python3-pip

# Nginx, uWSGI 설치 (Webserver, WSGI)
RUN     apt -y install nginx supervisor
RUN     pip3 install uwsgi

# docker build할때의 PATH해 해당하는 폴더의 전체 내용을
# Image의 /srv/project/폴더 내부에 복사
COPY        requirements_production.txt /tmp/requirements.txt
RUN         pip3 install -r /tmp/requirements.txt

COPY        ./  /srv/project
WORKDIR     /srv/project

ENV         DJANGO_SETTINGS_MODULE config.settings.production

# Nginx
# 기존에 존재하던 Nginx 설정 파일들 삭제
RUN         rm -rf /etc/nginx/sites-available/*
RUN         rm -rf /etc/nginx/sites-enabled/*

# 프로젝트 Nginx설정파일 복사 및 enabled로 링크 설정
RUN         cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/
RUN         ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

# supervisord설정 파일 복사
RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

EXPOSE  80

# Command로 supervisord 실행
CMD         supervisord -n