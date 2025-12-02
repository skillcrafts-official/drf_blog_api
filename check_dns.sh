#!/bin/bash
echo "��� Monitoring DNS propagation for portfolio-blog-api.ru"
echo "⏰ Started at: $(date)"
echo "----------------------------------------"

while true; do
    echo "[$(date +%H:%M:%S)] Checking..."
    
    # Проверка через разные DNS серверы
    echo "Google DNS (8.8.8.8):"
    IP_GOOGLE=$(dig @8.8.8.8 portfolio-blog-api.ru A +short)
    echo "  $IP_GOOGLE"
    
    echo "Cloudflare DNS (1.1.1.1):"
    IP_CLOUDFLARE=$(dig @1.1.1.1 portfolio-blog-api.ru A +short)
    echo "  $IP_CLOUDFLARE"
    
    echo "Local DNS:"
    IP_LOCAL=$(dig portfolio-blog-api.ru A +short)
    echo "  $IP_LOCAL"
    
    if [ "$IP_GOOGLE" = "37.77.105.19" ] && \
       [ "$IP_CLOUDFLARE" = "37.77.105.19" ]; then
        echo "✅ ✅ ✅ DNS FULLY PROPAGATED! ✅ ✅ ✅"
        echo "��� Domain portfolio-blog-api.ru now points to 37.77.105.19"
        break
    elif [ "$IP_LOCAL" = "37.77.105.19" ]; then
        echo "⚠️  DNS propagating... (local OK, external pending)"
    else
        echo "❌ Still waiting for DNS propagation..."
    fi
    
    echo "----------------------------------------"
    sleep 60  # Проверяем каждую минуту
done
