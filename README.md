# TestTaskSurf

Тестовое задание для Surf. Представляет из себя сервис по размещению объявлений.
Стек:
-FastAPI
-PostgreSQL
-Docker
-Aiogram

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Installation

Тут представлены инструкция, с помощью которых можно развернуть проект

```bash
# Склонируйте репозиторий
git clone https://github.com/your-username/your-project.git

# Переместитесь в папку проекта
cd your-project

# Установите необходимые библиотеки
pip install -r requirements.txt

#Поместите папку config в проект
```

Также попробовал добавить функционал разворачивания проекта в докере (см. Dockerfile в корневой папке)
``` bash
docker build -t myapp
```

Также необходимо получить в личном сообщении админский токен с помощью которого будут создаваться новые, либо сгенерировать его самостоятельно используя секретный ключ из конфига
## Usage
# Run the project
``` bash
python main.py  #Вне докера

docker run -d -p 8080:80 myapp #В нём
```
