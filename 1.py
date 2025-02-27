# Модель M/M/c: Расчет времени ожидания
import math

def mmc_waiting_time(lambd, mu, c):
    rho = lambd / (c * mu)
    if rho >= 1:
        return float('inf')  # Система перегружена

    # Вероятность нулевой очереди
    p0 = 1 / (sum([(c * rho) ** n / math.factorial(n) for n in range(c)]) +
              (c * rho) ** c / (math.factorial(c) * (1 - rho)))

    # Формула времени ожидания
    Wq = (((c * rho) ** c) / (math.factorial(c) * (1 - rho) ** 2)) * p0 / (c * mu - lambd)
    return Wq * 60  # В минутах


# Пример вызова:
lambd = 4500  # Интенсивность потока (чел/час)
mu = 1000  # Пропускная способность турникета (чел/час)
c = 5  # Количество турникетов

Wq = mmc_waiting_time(lambd, mu, c)
print(f"Среднее время ожидания: {Wq:.2f} минут")
