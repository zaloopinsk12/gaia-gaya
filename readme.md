# Gaia Training



## Установка
1. Обновляем сервер:
   ```bash
   sudo apt update
   sudo apt upgrade
   
2. Клонируем репозиторий:
   ```bash
   git clone https://github.com/zaloopinsk12/gaia-gaya.git

3. Переходим в папку скрипта:
   ```bash
   cd gaia-gaya

4. Создаем виртуальное окружение:
   ```bash
   python3 -m venv venv

5. Активируем виртуальное окружение:
   ```bash
   source venv/bin/activate

6. Устанавливаем библиотеки:
   ```bash
   pip install web3==6.20.1 fake_useragent loguru

7. Устанавливаем tmux
   ```bash
   sudo apt install tmux
   ```

## Первый запуск
1. Запускаем tmux:
   
   ```bash
   tmux
   ```
2. Активируем виртуальное окружение:

   ```bash
   source venv/bin/activate
   ```

3. Грузим любой приватник в `data/keys.txt`, и прокси в `data/proxies.txt`. Если прокси нет то просто оставляем пару пустых строк

4. Запускаем скрипт, жмем `1` и `Enter`. Должны создаться аккаунты в файл `data/accounts.txt`:
   ```bash
   python3 main.py
   ```

   
## Все последующие запуски

1. Запускаем tmux:
   ```bash
   tmux
   ```

2. После этого жмем `CTRL+B S` чтобы открылся список сессий. Ищем нашу первую сессию, если сессия сбилась либо её просто нет:
   ```bash
   source venv/bin/activate
   python3 main.py
   ```

## Остановка
   Чтобы остановить работу скрипта, находим рабочую сессию и жмем `CTRL+C` много раз

## Важно
   Не забывайте активировать виртуальное окружение перед каждым запуском скрипта.
