# Gaia Training



## Установка
1. Обновляем сервер:
   ```bash
   sudo apt update
   sudo apt upgrade
   
2. Клонируем код:
   ```bash
   git clone https://github.com/zaloopinsk12/gaia-gaya.git
   cd gaia-gaya

3. Устанавливаем библиотеки:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install web3==6.20.1 fake_useragent loguru
## Запуск
   ```bash
   python3 main.py
