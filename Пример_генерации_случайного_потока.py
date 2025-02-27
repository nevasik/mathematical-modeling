import numpy as np
import matplotlib.pyplot as plt

def generate_arrival_rate(t_start, t_end, min_rate=50, max_rate=200):
    """
    Генерация случайной интенсивности потока людей по времени.

    Формула:
    λ(t) = min_rate + (max_rate - min_rate) * U[0,1]
    где U[0,1] - равномерное распределение

    Параметры:
    t_start, t_end - временной интервал (часы)
    min_rate - минимальная интенсивность (чел/час)
    max_rate - максимальная интенсивность (чел/час)
    """
    time_intervals = np.linspace(t_start, t_end, 100)
    rates = min_rate + (max_rate - min_rate) * np.random.rand(100)
    return time_intervals, rates

# Пример вызова для интервала 8:00-12:00
time_points, arrival_rates = generate_arrival_rate(
    t_start=8.0,  # 8:00 в десятичном формате
    t_end=12.0,    # 12:00
    min_rate=100,
    max_rate=400
)

# Визуализация
plt.figure(figsize=(10, 4))
plt.plot(time_points, arrival_rates, 'b-', linewidth=2)
plt.title("Случайная интенсивность потока людей\nλ(t) = 100 + 300·U[0,1]")
plt.xlabel("Время (часы)", fontsize=12)
plt.ylabel("Людей в час", fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(np.arange(8, 12.5, 0.5))
plt.yticks(np.arange(100, 450, 50))
plt.show()