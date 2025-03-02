import random
import math
import matplotlib.pyplot as plt

def generate_arrivals(T, arrivals_min, arrivals_max):
    """
    Генерация случайного потока людей на интервале 0..T (каждая единица - минута).
    arrivals_min, arrivals_max: int, границы распределения.

    Возвращает список, где i-й элемент - число людей, пришедших в минуту i.
    """
    arrivals = []
    for _ in range(T):
        # случайно целое число из [arrivals_min, arrivals_max]
        a = random.randint(arrivals_min, arrivals_max)
        arrivals.append(a)
    return arrivals

def generate_service_times(num_people, mode='uniform', param1=2.0, param2=5.0):
    """
    Генерация времени обслуживания для num_people человек.
    mode='uniform': равномерное распределение [param1, param2].
    mode='exp': экспоненциальное с параметром mu = param1 (тогда param2 не используется).

    Возвращает список времен обслуживания.
    """
    service_times = []
    if mode == 'uniform':
        for _ in range(num_people):
            # равномерное от param1 до param2
            st = random.uniform(param1, param2)
            service_times.append(st)
    elif mode == 'exp':
        mu = param1
        for _ in range(num_people):
            # Генерация экспоненциальной случайной величины
            r = random.random()
            # метод обратных функций: st = -ln(1 - r) / mu
            st = -math.log(r) / mu
            service_times.append(st)
    else:
        raise ValueError("Unknown mode. Use 'uniform' or 'exp'.")
    return service_times

# ПАРАМЕТРЫ МОДЕЛИ
T = 60                # длительность моделирования (например, 60 "минут")
arrivals_min = 0      # минимум человек в минуту
arrivals_max = 5      # максимум человек в минуту

# Генерируем поток
arrivals = generate_arrivals(T, arrivals_min, arrivals_max)

# Подсчитаем общее число людей
total_people = sum(arrivals)

# Генерируем время обслуживания
# 1) Равномерное [2, 5] секунд (как пример)
service_times_uniform = generate_service_times(total_people, mode='uniform', param1=2.0, param2=5.0)
# 2) Экспоненциальное (среднее 1/mu); пусть mu=1/3 -> среднее время обслуживания = 3 сек
service_times_exp = generate_service_times(total_people, mode='exp', param1=(1/3))

# --- ПОСТРОЕНИЕ ГРАФИКОВ ---

# 1. График потока: сколько людей пришло в каждую минуту
plt.figure(figsize=(10, 6))

plt.subplot(2,2,1)
plt.plot(range(T), arrivals, marker='o')
plt.title("Приход людей за каждую минуту")
plt.xlabel("Минута")
plt.ylabel("Число человек")
plt.grid(True)

# 2. Гистограмма распределения количества людей (по минутам)
plt.subplot(2,2,2)
plt.hist(arrivals, bins=range(arrivals_min, arrivals_max+2), align='left', edgecolor='black')
plt.title("Гистограмма (число человек в минуту)")
plt.xlabel("Число пришедших за минуту")
plt.ylabel("Частота")
plt.grid(True)

# 3. Гистограмма равномерного времени обслуживания [2..5]
plt.subplot(2,2,3)
plt.hist(service_times_uniform, bins=20, edgecolor='black', color='skyblue')
plt.title("Время обслуживания (Uniform [2..5] секунд)")
plt.xlabel("Время, сек")
plt.ylabel("Частота")
plt.grid(True)

# 4. Гистограмма экспоненциального времени обслуживания
plt.subplot(2,2,4)
plt.hist(service_times_exp, bins=20, edgecolor='black', color='lightgreen')
plt.title("Время обслуживания (Exp со ср. ≈ 3 сек)")
plt.xlabel("Время, сек")
plt.ylabel("Частота")
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"Всего сгенерировано людей за {T} минут: {total_people}")
