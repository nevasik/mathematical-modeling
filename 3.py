import random
import math
import matplotlib.pyplot as plt

def simulate_single_turnstile(
        T=60,                # общее время моделирования в минутах
        arrivals_min=0,      # минимум пришедших за 1 минуту
        arrivals_max=5,      # максимум пришедших за 1 минуту
        service_rate=1/3.0,  # параметр mu для экспоненциального обслуживания (1/3 => среднее 3 мин)
        seed=None
):
    """
    Имитация работы одноканальной системы (турникет) за T минут.

    ПАРАМЕТРЫ:
    T              - длительность моделирования (в минутах).
    arrivals_min   - минимальное число вновь пришедших людей в минуту.
    arrivals_max   - максимальное число вновь пришедших людей в минуту.
    service_rate   - интенсивность обслуживания (му), исп. в экспоненциальном распределении.
                     (например, 1/3 => в среднем 3 минуты на одного человека)
    seed           - начальное значение для генератора случайных чисел (для воспроизводимости, опционально).

    ВОЗВРАЩАЕТ:
    словарь с результатами:
      - time_points        (список минут [0..T-1]),
      - queue_length       (длина очереди на конец каждой минуты),
      - waiting_times      (список времен ожидания для всех обслуженных),
      - server_busy_flag   (1 или 0 в каждую минуту, занят турникет или нет).
    """
    if seed is not None:
        random.seed(seed)

    time_points = list(range(T))
    queue_length = []      # длина очереди на конец каждой минуты
    waiting_times = []     # индивидуальное время ожидания каждого обслуженного студента
    server_busy_flag = []  # список (0/1) - занят ли сервер в конце каждой минуты

    # Очередь: будем хранить в ней кортежи (time_of_arrival)
    queue = []

    # Сколько ещё минут (в дробном виде) турникет будет занят (обслуживает текущего человека)
    server_busy_time = 0.0

    # Вспомогательный счётчик, чтобы фиксировать "момент начала обслуживания"
    # Для каждого человека определим, когда он реально начал обслуживаться (T_start).
    # Тогда W = T_start - T_arrive.

    # Для упрощения каждую минуту:
    # 1. Генерируем arrivals
    # 2. Пробуем "продвинуть" обслуживание на 1 минуту
    # 3. Если сервер освободился в этой минуте, взять из очереди следующего (если есть)

    for minute in time_points:
        # --- 1) Генерация новых пришедших людей ---
        arrivals_num = random.randint(arrivals_min, arrivals_max)  # число пришедших
        # Записываем их время прихода (minute)
        for _ in range(arrivals_num):
            queue.append(minute)

        # --- 2) Обслуживание ---
        if server_busy_time > 0:
            # сервер занят, уменьшаем время на 1 минуту
            server_busy_time -= 1.0
            if server_busy_time < 0:
                server_busy_time = 0
        else:
            # сервер свободен, берем нового человека из очереди (если есть)
            if len(queue) > 0:
                # возьмём первого (FIFO)
                arrival_time = queue.pop(0)
                # время начала обслуживания = текущая минута
                start_service_time = minute
                # время ожидания
                wait = start_service_time - arrival_time
                waiting_times.append(wait)

                # сгенерируем время обслуживания (экспоненциальное)
                # service_rate = mu
                # если X ~ Exp(mu), среднее = 1/mu
                # метод обратных функций:
                r = random.random()
                service_duration = -math.log(r) / service_rate  # в минутах

                # т.к. мы моделируем покадрово (по 1 минуте), мы фиксируем
                # что сервер будет еще service_duration-1 занятый последовательно.
                server_busy_time = service_duration  # кол-во минут

        # Запись текущей длины очереди и занятости
        queue_length.append(len(queue))
        # Флаг занятости сервера
        if server_busy_time > 0:
            server_busy_flag.append(1)
        else:
            server_busy_flag.append(0)

    results = {
        "time_points": time_points,
        "queue_length": queue_length,
        "waiting_times": waiting_times,
        "server_busy": server_busy_flag
    }
    return results


# --- Запуск имитации ---
res = simulate_single_turnstile(
    T=60,             # 60 минут
    arrivals_min=0,   # 0..5 человек в минуту
    arrivals_max=5,
    service_rate=1/3, # среднее время обслуживания ~ 3 мин
    seed=42           # чтобы пример был воспроизводим
)

time_points = res["time_points"]
queue_length = res["queue_length"]
waiting_times = res["waiting_times"]
server_busy = res["server_busy"]

# --- ПОСТРОЕНИЕ ГРАФИКОВ ---
plt.figure(figsize=(12,6))

# График 1: Длина очереди по времени
plt.subplot(2,2,1)
plt.plot(time_points, queue_length, marker='o', label='Длина очереди')
plt.xlabel("Время (мин)")
plt.ylabel("Число людей в очереди")
plt.title("Длина очереди во времени")
plt.grid(True)
plt.legend()

# График 2: Сервер (турникет) занят или нет
plt.subplot(2,2,2)
plt.plot(time_points, server_busy, drawstyle='steps-post', color='orange', label='Занят(1) / свободен(0)')
plt.ylim(-0.1, 1.1)
plt.xlabel("Время (мин)")
plt.ylabel("Состояние сервера")
plt.title("Занятость турникета во времени")
plt.grid(True)
plt.legend()

# График 3: Гистограмма времён ожидания
plt.subplot(2,2,3)
plt.hist(waiting_times, bins=20, edgecolor='black', alpha=0.7)
plt.xlabel("Время ожидания (мин)")
plt.ylabel("Частота")
plt.title("Распределение времени ожидания")
plt.grid(True)

# График 4: Эмпирическое распределение waiting_times (CDF)
sorted_waits = sorted(waiting_times)
cdf_y = [(i+1)/len(sorted_waits) for i in range(len(sorted_waits))]
plt.subplot(2,2,4)
plt.plot(sorted_waits, cdf_y, marker='.')
plt.xlabel("Время ожидания (мин)")
plt.ylabel("F(w)")
plt.title("Эмпирическая функция распределения (CDF)")
plt.grid(True)

plt.tight_layout()
plt.show()

# Печатаем простую статистику
print(f"Средняя длина очереди: {sum(queue_length)/len(queue_length):.2f}")
print(f"Макс. длина очереди: {max(queue_length)}")
if waiting_times:
    print(f"Среднее время ожидания: {sum(waiting_times)/len(waiting_times):.2f} мин")
    print(f"Максимальное время ожидания: {max(waiting_times):.2f} мин")
    print(f"Обслужено людей: {len(waiting_times)}")
else:
    print("Никто не был обслужен (нет времени ожидания).")

server_utilization = sum(server_busy)/len(server_busy)  # доля минут, когда сервер был занят
print(f"Загрузка турникета (доля занятости): {server_utilization*100:.1f}%")
