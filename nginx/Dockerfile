FROM nginx:latest

RUN mkdir -p /app/staticfiles

COPY nginx.conf /etc/nginx/nginx.conf
COPY mime.types /etc/nginx/mime.types  

EXPOSE 80