import math
import random
import matplotlib.pyplot as plt

# --- 1. Параметры расписания (в минутах от 08:00) ---
# Для удобства переведём всё время в "минуты с начала дня 08:00".
# 08:00 -> 0
# 08:20 -> 20
# 09:40 -> 100
# 09:50 -> 110
# 11:10 -> 190
# 11:20 -> 200
# 12:40 -> 280
# 12:50 -> 290
# 14:10 -> 370
# 14:40 -> 400
# 16:00 -> 480

# Определим интервалы (start_minute, end_minute, (arrivals_min, arrivals_max))
# Можно настроить по своему усмотрению:
schedule_intervals = [
    (0,   20,   (0,  2)),  # 08:00 - 08:20 (небольшой поток)
    (20,  100,  (2,  5)),  # 08:20 - 09:40 (идёт пара, пик был прямо перед 08:20,
    #   но допустим 2..5 в минуту)
    (100, 110,  (0,  1)),  # 09:40 - 09:50 (перерыв, мало людей)
    (110, 190,  (2,  5)),  # 09:50 - 11:10 (вторая пара)
    (190, 200,  (0,  1)),  # 11:10 - 11:20 (перерыв)
    (200, 280,  (2,  4)),  # 11:20 - 12:40 (третья пара)
    (280, 290,  (0,  1)),  # 12:40 - 12:50 (перерыв)
    (290, 370,  (2,  5)),  # 12:50 - 14:10 (четвёртая пара)
    (370, 400,  (0,  1)),  # 14:10 - 14:40 (перерыв)
    (400, 480,  (2,  4)),  # 14:40 - 16:00 (пятая пара)
]

def get_arrivals_min_max(current_minute):
    """
    Возвращаем (arrivals_min, arrivals_max) для заданной минуты с 08:00,
    основываясь на расписании schedule_intervals.
    """
    for (start_m, end_m, (mn, mx)) in schedule_intervals:
        if start_m <= current_minute < end_m:
            return (mn, mx)
    return (0, 0)  # если вдруг за пределами расписания

def simulate_one_day(
        total_minutes=480,  # с 08:00 до 16:00
        service_min_sec=2.0,
        service_max_sec=5.0,
        seed=None
):
    """
    Имитация работы одного турникета с расписанием пар за весь день (08:00-16:00).
    Каждая итерация = 1 минута.

    ПАРАМЕТРЫ:
      - total_minutes : общее время моделирования (480 мин = 8 часов)
      - service_min_sec, service_max_sec : границы равномерного распределения
        на время обслуживания (секунды).
      - seed : фиксатор для случайного генератора (опционально).

    ВОЗВРАЩАЕТ:
      словарь с:
        time_points       : список минут [0..total_minutes-1]
        queue_length      : длина очереди на конце каждой минуты
        waiting_times     : время ожидания (минуты) для каждого обслуженного
        server_busy       : 0/1 (свободен/занят) в конце каждой минуты
    """
    if seed is not None:
        random.seed(seed)

    # Переводим секунды в минуты, чтобы работать в одних единицах
    # 1 сек = 1/60 мин
    service_min_min = service_min_sec / 60.0
    service_max_min = service_max_sec / 60.0

    time_points = list(range(total_minutes))
    queue_length = []
    waiting_times = []
    server_busy = []

    queue = []  # список (время_прихода) для каждого человека
    server_busy_time = 0.0  # на сколько минут турникет ещё занят

    for minute in time_points:
        # --- 1) Генерация приходов ---
        (mn, mx) = get_arrivals_min_max(minute)
        arrivals_num = random.randint(mn, mx)
        for _ in range(arrivals_num):
            queue.append(minute)  # человек пришёл в 'minute'

        # --- 2) Обслуживание ---
        if server_busy_time > 0:
            # сервер занят, уменьшим время
            server_busy_time -= 1.0
            if server_busy_time < 0:
                server_busy_time = 0
        else:
            # сервер свободен
            if len(queue) > 0:
                arrival_t = queue.pop(0)
                waiting = minute - arrival_t
                waiting_times.append(waiting)

                # Генерируем время обслуживания (равномерное [service_min_min..service_max_min])
                dur = random.uniform(service_min_min, service_max_min)

                # Установим, что турникет будет занят на dur минут
                server_busy_time = dur
        queue_length.append(len(queue))

        if server_busy_time > 0:
            server_busy.append(1)
        else:
            server_busy.append(0)

    return {
        "time_points": time_points,
        "queue_length": queue_length,
        "waiting_times": waiting_times,
        "server_busy": server_busy
    }

# --- 3. Проведём серию экспериментов ---

# (A) БАЗОВЫЕ ПАРАМЕТРЫ
base_service_min_sec = 2.0
base_service_max_sec = 5.0

# Эксперименты: [(имя_сценария, (service_min_sec, service_max_sec), seed), ...]
# Можно также варьировать total_minutes (T), но здесь оставим 480 мин (весь день).
experiments = [
    ("Scenario1", (2.0, 5.0), 42),  # Базовый сценарий: 2..5 сек, seed=42
    ("Scenario2", (3.0, 8.0), 42), # Увеличим время обслуживания: 3..8 сек
    ("Scenario3", (1.0, 3.0), 42), # Уменьшим время обслуживания: 1..3 сек
]

results_all = {}

for (label, (smin, smax), sd) in experiments:
    res = simulate_one_day(
        total_minutes=480,
        service_min_sec=smin,
        service_max_sec=smax,
        seed=sd
    )
    results_all[label] = res

# --- 4. Визуализация результатов ---
plt.figure(figsize=(12,8))

colors = ['blue', 'red', 'green']
for i, label in enumerate(results_all.keys()):
    r = results_all[label]
    q_len = r["queue_length"]
    t_points = r["time_points"]
    plt.plot(t_points, q_len, label=f"{label} (service: {experiments[i][1][0]}-{experiments[i][1][1]} sec)",
             color=colors[i])

plt.xlabel("Минуты с 08:00 (0..480)")
plt.ylabel("Длина очереди (число людей)")
plt.title("Длина очереди во времени (разные сценарии времени обслуживания)")
plt.legend()
plt.grid(True)
plt.show()

# Выведем текстовую статистику:
for i, label in enumerate(results_all.keys()):
    r = results_all[label]
    q_len = r["queue_length"]
    waits = r["waiting_times"]
    srv = r["server_busy"]

    avg_q = sum(q_len)/len(q_len)
    max_q = max(q_len) if q_len else 0
    avg_w = sum(waits)/len(waits) if waits else 0
    max_w = max(waits) if waits else 0
    utilization = sum(srv)/len(srv)*100

    print(f"--- {label} ---")
    print(f"Service time range: {experiments[i][1][0]}..{experiments[i][1][1]} sec")
    print(f"Средняя длина очереди: {avg_q:.2f}, макс: {max_q}")
    print(f"Среднее время ожидания: {avg_w:.2f} мин, макс: {max_w:.2f}")
    print(f"Загрузка турникета: {utilization:.1f}%\n")

# schedule_intervals
# Массив, определяющий кусочно-заданный диапазон (arrivals_min,arrivals_max) для разных промежутков в минутах от 8:00.Например, (0, 20, (0,2)) означает с 8:00 до 8:20 (минуты 0..19) генерировать от 0 до 2 человек в минуту.

# get_arrivals_min_max(current_minute). Смотрит, в какой интервал расписания попадает current_minute и возвращает (mn, mx). # Если current_minute > 480 или < 0, вернёт (0,0), но в наших пределах это не должно случиться.

# simulate_one_day(...) Моделирует 480 минут (8:00–16:00) пошагово. # На каждом шаге (каждой минуте) генерирует число пришедших (по randint(mn, mx)), учитывая расписание, и добавляет их в очередь.
# Если турникет свободен, берёт из очереди студента, рассчитывает его время ожидания (текущая_минута - время_прихода), затем генерирует случайное время обслуживания (равномерное) и «занимает» турникет на это время.
# Хранит:
    # queue_length (длину очереди в конце каждой минуты),
    # waiting_times (время ожидания каждого обслуженного),
    # server_busy (1 или 0 для каждой минуты).

# Серия экспериментов
# В данном примере мы варьируем только границы времени обслуживания (2–5, 3–8, 1–3 секунд). Можно добавить эксперименты, меняя arrivals_min–max в самом schedule_intervals или общее время total_minutes.

# График
# Рисуем временную динамику длины очереди для всех экспериментов на одном графике (с разными цветами). Видно, как изменяются «горбы» очереди в течение дня для разных скоростей обслуживания.

# Текстовая статистика
    # Средняя/максимальная длина очереди,
    # Среднее/максимальное время ожидания (в минутах),
    # Загрузка турникета (в %).
