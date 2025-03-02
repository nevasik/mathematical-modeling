import math
import random
import matplotlib.pyplot as plt

def piecewise_lambda(minute_from_8h):
    """
    Функция, которая возвращает интенсивность λ (чел/мин),
    исходя из того, какая сейчас минута с 8:00 (0..30).

    minute_from_8h: целое число, 0 <= minute_from_8h < 30.
    """
    if 0 <= minute_from_8h < 10:
        return 1.0  # 8:00-8:10
    elif 10 <= minute_from_8h < 15:
        return 3.0  # 8:10-8:15
    elif 15 <= minute_from_8h < 20:
        return 6.0  # 8:15-8:20 (пик)
    elif 20 <= minute_from_8h < 25:
        return 3.0  # 8:20-8:25 (ещё приходят)
    else:
        return 1.0  # 8:25-8:30 (редкие опоздавшие)

def generate_poisson_arrivals_piecewise(total_minutes=30):
    """
    Генерируем arrivals для каждого из 30 минут (с 8:00 до 8:30).
    При этом для каждой минуты t мы берём λ(t) из piecewise_lambda(t) и
    генерируем Poisson(λ(t)) человек.

    Возвращает список arrivals, где arrivals[i] - число людей,
    пришедших в минуту (8:00 + i).
    """
    arrivals = []
    for m in range(total_minutes):
        lam = piecewise_lambda(m)  # интенсивность для минуты m
        # Генерируем одно число из Пуассона с параметром lam (т.к. dt=1 мин)
        # Метод Кнута (наивный)
        L = math.exp(-lam)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= random.random()
        arrivals.append(k - 1)
    return arrivals

def minute_to_hhmm(minute_from_8h):
    """
    Преобразует "количество минут от 8:00" в строку формата HH:MM.
    Например, 0 -> "08:00", 5 -> "08:05", 20 -> "08:20".
    """
    base_hour = 8
    hh = base_hour + (minute_from_8h // 60)  # на всякий случай, если > 60
    mm = minute_from_8h % 60
    return f"{hh:02d}:{mm:02d}"

# --- ОСНОВНАЯ ЧАСТЬ ---

arrivals = generate_poisson_arrivals_piecewise(total_minutes=30)
time_labels = [minute_to_hhmm(m) for m in range(30)]  # ["08:00", "08:01", ..., "08:29"]

# Построим графики
plt.figure(figsize=(12,5))

# 1) Линейный график с приходами
plt.subplot(1,2,1)
plt.plot(time_labels, arrivals, marker='o')
plt.title("Приход людей к паре (начало в 08:20)")
plt.xlabel("Время (часы:минуты)")
plt.ylabel("Число пришедших за минуту")
plt.xticks(rotation=45)
plt.grid(True)

# 2) Гистограмма распределения (сколько минут встретили 0 чел, 1 чел, 2 чел, ...)
plt.subplot(1,2,2)
plt.hist(arrivals, bins=range(0, max(arrivals)+2), edgecolor='black', alpha=0.7)
plt.title("Распределение числа пришедших за 1 минуту")
plt.xlabel("Число студентов")
plt.ylabel("Частота (кол-во минут с таким приходом)")
plt.grid(True)

plt.tight_layout()
plt.show()

# Итоговые цифры
total_people = sum(arrivals)
print("Cгенерированный список (первые 10 значений):", arrivals[:10])
print(f"Всего пришло людей за период 8:00-8:30: {total_people}")


# Функция generate_poisson_arrivals:
# На вход: λ (людей в минуту), T (общая длительность, минут), dt (шаг, минут). На каждом шаге «Δt» мы генерируем целое число людей по закону Пуассона с параметром μ=λ⋅Δt.
# В итоге получаем список «arrivals[i]» — сколько людей пришло в i-й отрезок (i-я минута). Это классическая «дискретизированная» версия моделирования потока.

#Графики:
# Линейный (слева): показывает, что в какие-то минуты приходит 0 человек, в какие-то 1, 2, 3 или даже 4–5.
# Гистограмма (справа): показывает, как часто мы наблюдаем 0, 1, 2… человек в рамках одной минуты. При λ=2 в минуту пик обычно приходится на 1–2 человека, но есть вероятность и 0, и 3, и 4.
# Интерпретация: Если мы фиксируем λ=2 чел/мин, то в среднем за 30 минут придёт 2×30=60, но фактически может быть и 58, и 62, и т.п. (случайные колебания).
# Это даёт «реалистичную» статистику, которую затем можно прокинуть в модель очереди (например, M/M/1, если время обслуживания тоже экспоненциально).
