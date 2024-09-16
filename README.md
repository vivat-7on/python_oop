# Fitness Tracker Module

## Описание

Этот модуль фитнес-трекера предназначен для обработки данных тренировок и вычисления результатов для трёх видов активности: бега, спортивной ходьбы и плавания. Модуль использует парадигму объектно-ориентированного программирования (ООП) для расчета различных метрик, таких как дистанция, средняя скорость и расход энергии, а также для отображения результатов в удобном формате.

## Стек технологий

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/OOP-000000?logo=python&logoColor=white)


## Как использовать

1. **Импортируйте модуль:**

   ```python
   from fitness_tracker import Running, SportsWalking, Swimming, read_package, main
   ```

2. **Создайте экземпляры тренировок:**

   ```python
   running = Running(action=15000, duration=1, weight=75)
   walking = SportsWalking(action=9000, duration=1, weight=75, height=180)
   swimming = Swimming(action=720, duration=1, weight=80, length_pool=25, count_pool=40)
   ```

3. **Получите информацию о тренировке:**

   ```python
   print(running.show_training_info().get_message())
   ```

4. **Запустите основной скрипт:**

   ```python
   if __name__ == '__main__':
       packages = [
           ('SWM', [720, 1, 80, 25, 40]),
           ('RUN', [15000, 1, 75]),
           ('WLK', [9000, 1, 75, 180])
       ]

       for workout_type, data in packages:
           training = read_package(workout_type, data)
           main(training)
   ```

## Функции

- `get_distance()`: Вычисляет дистанцию в километрах.
- `get_mean_speed()`: Определяет среднюю скорость в км/ч.
- `get_spent_calories()`: Рассчитывает количество сожжённых калорий (реализовано для каждого типа тренировки).
- `show_training_info()`: Возвращает объект с информацией о тренировке.

## Примеры

**Результат для плавания:**
```
Тип тренировки: Swimming; Длительность: 1.000 ч.; Дистанция: 1.380 км; Ср. скорость: 1.380 км/ч; Потрачено ккал: 78.750.
```

**Результат для бега:**
```
Тип тренировки: Running; Длительность: 1.000 ч.; Дистанция: 9.750 км; Ср. скорость: 9.750 км/ч; Потрачено ккал: 157.500.
```

**Результат для спортивной ходьбы:**
```
Тип тренировки: SportsWalking; Длительность: 1.000 ч.; Дистанция: 5.850 км; Ср. скорость: 5.850 км/ч; Потрачено ккал: 302.500.
```

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/fitness-tracker.git
   ```

2. Перейдите в каталог проекта:

   ```bash
   cd fitness-tracker
   ```

3. Установите необходимые зависимости (если есть):

   ```bash
   pip install -r requirements.txt
   ```

4. Запустите основной скрипт:

   ```bash
   python main.py
   ```
