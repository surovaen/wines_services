FROM nginx:stable-alpine

ENV DOLLAR $

COPY ./deploy/nginx/django-default.conf.template /etc/nginx/templates/default.conf.template
