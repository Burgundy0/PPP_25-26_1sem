import asyncio
import random
from collections import deque

# Генерация бинарной матрицы NxM
async def generate_matrix(n: int, m: int, probability: float = 0.3):
    
    await asyncio.sleep(0)
    return [[1 if random.random() < probability else 0 for _ in range(m)] for _ in range(n)]

# Поиск размера острова
async def bfs_island(matrix, i, j, visited):
   
    await asyncio.sleep(0)
    n, m = len(matrix), len(matrix[0])
    queue = deque([(i, j)])
    visited.add((i, j))
    size = 0

    while queue:
        x, y = queue.popleft()
        size += 1
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and matrix[nx][ny] == 1 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return size

# Нахождение всех островов
async def detect_islands(matrix):
   
    visited = set()
    islands = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 1 and (i, j) not in visited:
                islands.append(await bfs_island(matrix, i, j, visited))
    return islands

# Подсчёт строк/столбцов с количеством единиц
async def count_rows_cols(matrix, threshold=3):

    await asyncio.sleep(0)
    n, m = len(matrix), len(matrix[0])
    rows = [i for i, row in enumerate(matrix) if sum(row) > threshold]
    cols = [j for j in range(m) if sum(matrix[i][j] for i in range(n)) > threshold]
    return rows, cols

# Печать матрицы
def print_matrix(matrix):
   
    print("\nИгровое поле:")
    for row in matrix:
        print(" ".join("#" if x else "." for x in row))
    print()

# Главный анализ
async def analyze_field(n, m, p=0.3):
    
    matrix = await generate_matrix(n, m, p)
    print_matrix(matrix)

    # Запуск задач параллельно
    islands_task = asyncio.create_task(detect_islands(matrix))
    rows_cols_task = asyncio.create_task(count_rows_cols(matrix, 3))

    islands = await islands_task
    rows, cols = await rows_cols_task

    print("Острова:", len(islands))
    if islands:
        print("   Размеры:", islands)
        print(f"   Мин: {min(islands)}, Макс: {max(islands)}, Средний: {sum(islands)/len(islands):.2f}")
    else:
        print("   Островов нет")

    print(f"\nСтрок с >3 единицами: {len(rows)} {rows}")
    print(f"Столбцов с >3 единицами: {len(cols)} {cols}")

# Точка входа
async def main():
    
    n = int(input("Введите N: "))
    m = int(input("Введите M: "))
    p = float(input("Введите вероятность (0-1, по умолчанию 0.3): ") or 0.3)
    await analyze_field(n, m, p)

if __name__ == "__main__":
    asyncio.run(main())


