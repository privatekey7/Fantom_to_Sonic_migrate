# 🌉 FTM to S Bridge

Скрипт для автоматизации миграции FTM в Sonic. Поддерживает работу с множеством кошельков и настраиваемыми задержками между транзакциями.

## 📋 Требования

- Python 3.8+
- Установленные зависимости из requirements.txt

## 🛠 Установка

1. Создайте виртуальное окружение: python -m venv venv

2. Активируйте виртуальное окружение: venv\Scripts\activate

3. Установите зависимости: pip install -r requirements.txt

4. Настройте задержки между кошельками в файле config.py

4. Запустите скрипт: python main.py  


## ⚠️ Важные замечания

- Минимальный баланс для бриджинга: 1 FTM
- Fee для транзакции: 0.1 FTM
- Скрипт автоматически рассчитывает газ и вычитает его из суммы депозита
- Задержка между транзакциями: 300-600 секунд (настраивается в config.py)

## 🔍 Функционал

- Поддержка множества кошельков
- Автоматический расчет газа
- Цветной вывод логов
- Проверка баланса перед отправкой
- Отслеживание статуса транзакций
- Настраиваемые задержки между операциями

## 📱 Контакты

- [Telegram канал](https://t.me/privatekey7)
- [GitHub](https://github.com/privatekey7)
- [Powered by Pavel Durov](https://t.me/privatekey7)    
