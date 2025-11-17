FROM openresty/openresty:alpine

COPY . /etc/nginx/

RUN apk add --no-cache \
    lua-resty-jwt \
    lua-resty-forminput

RUN mkdir -p /var/www/public_files \
    && mkdir -p /var/www/protected_files \
    && chown -R nginx:nginx /var/www

RUN chmod -R 755 /var/www