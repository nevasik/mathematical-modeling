# import heapq
#
# def dijkstra(graph, start):
#     """
#     Алгоритм Дейкстры для поиска кратчайших путей от начальной вершины до всех остальных.
#
#     :param graph: Граф в виде словаря смежности {вершина: {сосед: вес}}
#     :param start: Начальная вершина
#     :return: Словарь кратчайших расстояний
#     """
#     # Инициализируем расстояния: все бесконечность, кроме стартовой вершины
#     distances = {vertex: float('infinity') for vertex in graph}
#     distances[start] = 0
#
#     # Приоритетная очередь (куча) для хранения (расстояние, вершина), идет пока у нас есть не обработанные вершны
#     priority_queue = [(0, start)]
#
#     while priority_queue:
#         # Извлекаем вершину с минимальным текущим расстоянием
#         current_distance, current_vertex = heapq.heappop(priority_queue) # извлекает и возвращает наименьшее элемент из кучи
#
#         # Если текущее расстояние больше уже известного - пропускаем
#         if current_distance > distances[current_vertex]:
#             continue
#
#         # Проверяем всех соседей текущей вершины
#         for neighbor, weight in graph[current_vertex].items():
#             distance = current_distance + weight
#
#             # Если найден более короткий путь - обновляем
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 heapq.heappush(priority_queue, (distance, neighbor))
#
#     return distances
#
#
# # Пример графа (словарь)
# graph = {
#     'A': {'B': 5, 'C': 1},
#     'B': {'A': 5, 'C': 2, 'D': 1},
#     'C': {'A': 1, 'B': 2, 'D': 4},
#     'D': {'B': 1, 'C': 4, 'E': 3},
#     'E': {'D': 3}
# }
#
# # Запуск алгоритма от вершины 'A'
# distances = dijkstra(graph, 'A')
#
# # Вывод результатов
# print("Кратчайшие расстояния от вершины A:")
# for vertex, distance in distances.items():
#     print(f"До {vertex}: {distance}")
#
#
# # A --5-- B --1-- D --3-- E
# # |     / |     /
# # 1   2   4   4
# # | /     | /
# # C --------

import heapq


def dijkstra(matrix, start):
    n = len(matrix)
    distances = [float('inf')] * n  # Создается список `distances`, хранящий кратчайшие расстояния от стартовой вершины до каждой вершины. Изначально все расстояния устанавливаются в бесконечность (`float('inf')`).
    distances[start] = 0
    heap = [(0,
             start)]  # Создается приоритетная очередь (куча) `heap`, используя модуль `heapq`. В неё добавляется начальная вершина со значением расстояния 0. Куча хранит кортежи `(расстояние, номер_вершины)`, упорядоченные по расстоянию.

    while heap:  # Создается приоритетная очередь (куча) `heap`, используя модуль `heapq`. В неё добавляется начальная вершина со значением расстояния 0. Куча хранит кортежи `(расстояние, номер_вершины)`, упорядоченные по расстоянию.
        current_dist, u = heapq.heappop(
            heap)  # Извлекается вершина `u` с наименьшим расстоянием `current_dist` из приоритетной очереди.
        if current_dist > distances[u]:  # пропускаем, так как есть больше и идем дальше
            continue

        for v in range(n):  # цикл перебирает все вершины графа
            weight = matrix[u][v]  # получаем вес ребра между вершинами
            if weight == 0:  # пропускаем петли и отсутствующие ребра
                continue

            print(distances)
            print('Следующая вершина графа')
            # Оно проверяет, можно ли улучшить кратчайшее расстояние до вершины `v`, пройдя через вершину `u`. Если `distances[v]` (текущее расстояние до `v`) больше, чем `distances[u] + weight`
            # (расстояние до `u` плюс вес ребра между `u` и `v`), то найден более короткий путь.
            if distances[v] > distances[u] + weight:
                print('Найден более короткий путь до вершины: ', v)
                print('Было:', distances[v])
                print("Стало:", distances[u], '+', weight)
                distances[v] = distances[u] + weight  # Обновляется кратчайшее расстояние до вершины `v`.
                heapq.heappush(heap, (distances[v], v))  # вершина v обновленная добавляется в очередь

    return distances


matrix = [
    [0, 4, 0, 3, 5, 9, 7, 4, 10, 2],
    [4, 0, 6, 8, 3, 7, 10, 0, 4, 9],
    [1, 6, 0, 2, 6, 9, 3, 7, 5, 8],
    [3, 8, 2, 0, 9, 7, 1, 0, 3, 10],
    [5, 3, 6, 9, 0, 2, 6, 1, 4, 9],
    [9, 7, 9, 7, 2, 0, 3, 10, 8, 2],
    [7, 10, 0, 1, 6, 3, 0, 9, 4, 8],
    [4, 0, 7, 6, 1, 10, 9, 0, 5, 1],
    [10, 4, 0, 0, 4, 8, 4, 0, 0, 2],
    [2, 9, 8, 10, 9, 2, 8, 1, 2, 0]
]

# Вычисляем кратчайшие пути от вершины 0
start_node = int(input())
shortest_paths = dijkstra(matrix, start_node)

# Выводим результаты
print(f"Кратчайшие расстояния от вершины {start_node}:")
for i, dist in enumerate(shortest_paths):
    print(f"До вершины {i}: {dist if dist != float('inf') else 'недостижима'}")
