# ./nginx/Dockerfile
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY mime.types /etc/nginx/mime.types


RUN mkdir -p /app/staticfiles