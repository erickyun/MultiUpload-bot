curl -L "$CONFIG_IN_URL" -o /app/.env; curl -L "$CONFIG_IN_URL" -o .env; chmod +x go-ul_x64; gunicorn app:app & python3 bot.py
