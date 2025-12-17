#!/bin/bash
# generate-dkim.sh
DOMAIN=${1:-yourdomain.com}
SELECTOR=${2:-mail}

mkdir -p postfix/opendkim/keys/${DOMAIN}
cd postfix/opendkim/keys/${DOMAIN}

# Генерация приватного ключа
openssl genrsa -out ${SELECTOR}.private 2048

# Генерация публичного ключа
openssl rsa -in ${SELECTOR}.private -out ${SELECTOR}.public -pubout

# Форматирование ключа для DNS TXT записи
echo -n "v=DKIM1; k=rsa; p=" > ${SELECTOR}.txt
grep -v '^-' ${SELECTOR}.public | tr -d '\n' >> ${SELECTOR}.txt

echo "DKIM ключ сгенерирован для ${DOMAIN}"
echo "DNS TXT запись для DKIM:"
echo "Имя: ${SELECTOR}._domainkey"
echo "Значение: $(cat ${SELECTOR}.txt)"
echo ""
echo "Публичный ключ:"
cat ${SELECTOR}.public