"""
Лабораторная работа №3: Генерация перестановок и комбинаций
"""

from typing import List, Dict, Any
from datetime import datetime


# ГЛОБАЛЬНЫЕ КОЛЛЕКЦИИ ДЛЯ ТРАССИРОВКИ


execution_log = []  # Шаги вычислений
partial_results = []  # Частичные результаты
final_results = []  # Итоговые комбинации

def clear_collections():
    """Очистка всех коллекций"""
    global execution_log, partial_results, final_results
    execution_log = []
    partial_results = []
    final_results = []

def log_step(action: str, data: dict = None):
    """Запись шага вычисления"""
    if data is None:
        data = {}
    execution_log.append({
        'action': action,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })

def save_partial_result(name: str, result: Any):
    """Сохранение частичного результата"""
    partial_results.append({
        'name': name,
        'result': result,
        'timestamp': datetime.now().isoformat()
    })

def save_final_result(name: str, result: Any):
    """Сохранение итогового результата"""
    final_results.append({
        'name': name,
        'result': result,
        'count': len(result) if hasattr(result, '__len__') else 0
    })


# РЕКУРСИВНЫЕ ФУНКЦИИ


def generate_permutations(elements: List, depth: int = 0) -> List[List]:
    """
    Генерация всех перестановок элементов.
    Фиксирует каждый шаг вычислений.
    """
    log_step('start_permutations', {
        'elements': elements.copy() if elements else [],
        'depth': depth,
        'step': 'начало вычислений'
    })
    
    # Базовый случай
    if len(elements) <= 1:
        result = [elements]
        log_step('base_case_permutations', {
            'elements': elements.copy() if elements else [],
            'result': result.copy(),
            'depth': depth
        })
        save_partial_result(f'базовый_случай_глубина_{depth}', result)
        return result
    
    all_permutations = []
    log_step('start_iterations', {
        'total_iterations': len(elements),
        'depth': depth
    })
    
    for i in range(len(elements)):
        # Шаг 1: Выбор головы
        head = elements[i]
        tail = elements[:i] + elements[i+1:]
        
        log_step('select_head', {
            'head': head,
            'tail': tail.copy(),
            'iteration': i,
            'depth': depth
        })
        
        # Шаг 2: Рекурсивный вызов для хвоста
        log_step('recursive_call', {
            'head': head,
            'remaining_elements': tail.copy(),
            'depth_before': depth,
            'depth_after': depth + 1
        })
        
        tail_permutations = generate_permutations(tail, depth + 1)
        
        # Фиксация промежуточных результатов
        save_partial_result(f'перестановки_хвоста_{head}_глубина_{depth}', tail_permutations)
        log_step('got_tail_permutations', {
            'head': head,
            'tail_permutations_count': len(tail_permutations),
            'depth': depth
        })
        
        # Шаг 3: Создание полных перестановок
        for perm in tail_permutations:
            full_permutation = [head] + perm
            all_permutations.append(full_permutation)
            
            # Фиксация каждой новой перестановки
            log_step('new_permutation', {
                'permutation': full_permutation.copy(),
                'depth': depth
            })
            save_partial_result(f'перестановка_{len(all_permutations)}', full_permutation)
    
    log_step('end_permutations', {
        'total_permutations': len(all_permutations),
        'depth': depth,
        'step': 'завершение вычислений'
    })
    
    return all_permutations

def generate_combinations(elements: List, r: int, depth: int = 0) -> List[List]:
    """
    Генерация всех комбинаций из r элементов.
    Фиксирует каждый шаг вычислений.
    """
    log_step('start_combinations', {
        'elements': elements.copy() if elements else [],
        'r': r,
        'depth': depth,
        'step': 'начало вычислений'
    })
    
    # Базовые случаи
    if r == 0:
        result = [[]]
        log_step('base_case_r0', {
            'result': result.copy(),
            'depth': depth
        })
        save_partial_result(f'базовый_случай_r0_глубина_{depth}', result)
        return result
    
    if len(elements) < r:
        result = []
        log_step('base_case_insufficient', {
            'elements': elements.copy() if elements else [],
            'r': r,
            'depth': depth
        })
        save_partial_result(f'базовый_случай_недостаточно_глубина_{depth}', result)
        return result
    
    all_combinations = []
    log_step('start_combination_iterations', {
        'total_iterations': len(elements),
        'depth': depth
    })
    
    for i in range(len(elements)):
        # Шаг 1: Выбор текущего элемента
        current = elements[i]
        remaining = elements[i+1:]
        
        log_step('select_current', {
            'current': current,
            'remaining': remaining.copy(),
            'iteration': i,
            'depth': depth
        })
        
        # Шаг 2: Рекурсивный вызов для оставшихся элементов
        log_step('recursive_combination_call', {
            'current': current,
            'remaining_elements': remaining.copy(),
            'new_r': r - 1,
            'depth_before': depth,
            'depth_after': depth + 1
        })
        
        remaining_combinations = generate_combinations(remaining, r - 1, depth + 1)
        
        # Фиксация промежуточных результатов
        save_partial_result(f'комбинации_остатка_{current}_глубина_{depth}', remaining_combinations)
        log_step('got_remaining_combinations', {
            'current': current,
            'remaining_combinations_count': len(remaining_combinations),
            'depth': depth
        })
        
        # Шаг 3: Создание полных комбинаций
        for comb in remaining_combinations:
            full_combination = [current] + comb
            all_combinations.append(full_combination)
            
            # Фиксация каждой новой комбинации
            log_step('new_combination', {
                'combination': full_combination.copy(),
                'depth': depth
            })
            save_partial_result(f'комбинация_{len(all_combinations)}', full_combination)
    
    log_step('end_combinations', {
        'total_combinations': len(all_combinations),
        'depth': depth,
        'step': 'завершение вычислений'
    })
    
    return all_combinations


# ФУНКЦИИ АНАЛИЗА И ВЫВОДА


def analyze_execution():
    """Анализ выполнения и вывод статистики"""
    print("\n" + "="*60)
    print("АНАЛИЗ ВЫПОЛНЕНИЯ")
    print("="*60)
    
    # Статистика по шагам вычислений
    print(f"\nШАГИ ВЫЧИСЛЕНИЙ: {len(execution_log)} записей")
    
    # Группировка по действиям
    action_counts = {}
    for entry in execution_log:
        action = entry['action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    print("\nРаспределение по действиям:")
    for action, count in sorted(action_counts.items()):
        print(f"  {action}: {count}")
    
    # Частичные результаты
    print(f"\nЧАСТИЧНЫЕ РЕЗУЛЬТАТЫ: {len(partial_results)} записей")
    if partial_results:
        print("Примеры частичных результатов:")
        for i, result in enumerate(partial_results[:5], 1):
            name = result['name']
            res = result['result']
            if isinstance(res, list) and len(res) > 3:
                res_preview = f"{res[:3]}... (всего {len(res)})"
            else:
                res_preview = res
            print(f"  {i}. {name}: {res_preview}")
    
    # Итоговые результаты
    print(f"\nИТОГОВЫЕ РЕЗУЛЬТАТЫ: {len(final_results)} записей")
    for result in final_results:
        print(f"\n  {result['name']}:")
        print(f"    Количество: {result['count']}")
        if result['count'] <= 10:
            for i, item in enumerate(result['result'], 1):
                print(f"      {i}. {item}")
        else:
            print(f"    Первые 5: {result['result'][:5]}")
            print(f"    ... и еще {result['count'] - 5} элементов")
    
    # Глубина рекурсии
    max_depth = 0
    for entry in execution_log:
        if 'depth' in entry['data']:
            max_depth = max(max_depth, entry['data']['depth'])
    print(f"\nМАКСИМАЛЬНАЯ ГЛУБИНА РЕКУРСИИ: {max_depth}")

def print_detailed_log(limit: int = 20):
    """Вывод детального лога выполнения"""
    print("\n" + "="*60)
    print("ДЕТАЛЬНЫЙ ЛОГ ВЫПОЛНЕНИЯ")
    print("="*60)
    
    for i, entry in enumerate(execution_log[:limit], 1):
        action = entry['action']
        data = entry['data']
        
        # Форматирование данных
        data_str = ""
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 3:
                value = f"{value[:3]}... (всего {len(value)})"
            data_str += f" {key}={value}"
        
        depth = data.get('depth', 0)
        indent = "  " * depth
        print(f"{i:3d}. {indent}{action}{data_str}")

def print_results(title: str, results: List[List]):
    """Простой вывод результатов"""
    print(f"\n{title}:")
    print(f"Найдено {len(results)} вариантов:")
    for i, item in enumerate(results, 1):
        print(f"  {i:2d}. {item}")


if __name__ == "__main__":
    # Пример 1: Генерация перестановок
    print("="*60)
    print("ПРИМЕР 1: ГЕНЕРАЦИЯ ПЕРЕСТАНОВОК")
    print("="*60)
    
    clear_collections()
    
    test_data = ['A', 'B', 'C']
    print(f"\nВходные данные: {test_data}")
    
    permutations = generate_permutations(test_data)
    save_final_result("Перестановки ABC", permutations)
    
    print_results("Все перестановки", permutations)
    analyze_execution()
    
    # Пример 2: Генерация комбинаций
    print("\n\n" + "="*60)
    print("ПРИМЕР 2: ГЕНЕРАЦИЯ КОМБИНАЦИЙ")
    print("="*60)
    
    clear_collections()
    
    test_data = [1, 2, 3, 4]
    r = 2
    print(f"\nВходные данные: {test_data}")
    print(f"Размер комбинации (r): {r}")
    
    combinations = generate_combinations(test_data, r)
    save_final_result(f"Комбинации C({len(test_data)},{r})", combinations)
    
    print_results("Все комбинации", combinations)
    analyze_execution()
    
    # Вывод детального лога
    print_detailed_log(15)
    
    # Пример 3: Другой набор данных
    print("\n\n" + "="*60)
    print("ПРИМЕР 3: ПЕРЕСТАНОВКИ ИЗ 4 ЭЛЕМЕНТОВ")
    print("="*60)
    
    clear_collections()
    
    test_data = ['X', 'Y', 'Z', 'W']
    print(f"\nВходные данные: {test_data}")
    
    permutations = generate_permutations(test_data)
    save_final_result("Перестановки XYZW", permutations)
    
    print(f"\nНайдено {len(permutations)} перестановок")
    print(f"Первые 5 перестановок: {permutations[:5]}")
    
    analyze_execution()
    
    print("\n" + "="*60)
    print("ВСЯ ИНФОРМАЦИЯ СОХРАНЕНА В КОЛЛЕКЦИЯХ:")
    print("="*60)
    print(f"Всего шагов вычислений: {len(execution_log)}")
    print(f"Всего частичных результатов: {len(partial_results)}")
    print(f"Всего итоговых результатов: {len(final_results)}")
