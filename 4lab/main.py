"""
Лабораторная работа №4: Полиморфизм
Тема: «Общий интерфейс и наследование для разнородных данных»
Временные интервалы в разных форматах
"""

from abc import ABC, abstractmethod
from typing import List, Union, Dict, Any
from datetime import timedelta
import math


# БАЗОВЫЙ АБСТРАКТНЫЙ КЛАСС (ИНТЕРФЕЙС)


class TimeInterval(ABC):
    """
    Абстрактный базовый класс для временных интервалов.
    Определяет общий интерфейс для всех форматов временных интервалов.
    """
    
    def __init__(self, value: str):
        """
        Инициализация интервала.
        
        Args:
            value: строка, содержащая значение интервала в конкретном формате
        """
        self.value = value
        self.seconds = self._parse_to_seconds(value)
    
    @abstractmethod
    def _parse_to_seconds(self, value: str) -> float:
        """
        Абстрактный метод для преобразования строкового значения в секунды.
        Должен быть реализован в каждом классе-наследнике.
        
        Returns:
            длительность интервала в секундах
        """
        pass
    
    @abstractmethod
    def get_format_name(self) -> str:
        """
        Возвращает название формата интервала.
        
        Returns:
            строковое название формата
        """
        pass
    
    def get_seconds(self) -> float:
        """
        Возвращает длительность интервала в секундах.
        
        Returns:
            длительность в секундах
        """
        return self.seconds
    
    def get_formatted(self) -> str:
        """
        Возвращает человекочитаемое строковое представление интервала.
        Формат: X h Y min Z s
        
        Returns:
            отформатированная строка
        """
        total_seconds = int(self.seconds)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours} h")
        if minutes > 0:
            parts.append(f"{minutes} min")
        if seconds > 0 or not parts:
            parts.append(f"{seconds} s")
        
        return " ".join(parts)
    
    def get_hms_format(self) -> str:
        """
        Возвращает интервал в формате ЧЧ:ММ:СС.
        
        Returns:
            строка в формате ЧЧ:ММ:СС
        """
        total_seconds = int(self.seconds)
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def __str__(self) -> str:
        """
        Строковое представление объекта.
        
        Returns:
            описание интервала
        """
        return f"{self.get_format_name()}: {self.value} = {self.get_formatted()}"
    
    def __repr__(self) -> str:
        """
        Репрезентация объекта для отладки.
        
        Returns:
            детальное описание
        """
        return f"{self.__class__.__name__}('{self.value}', seconds={self.seconds})"
    
    # Операторы сравнения для поддержки операций min/max
    def __lt__(self, other: 'TimeInterval') -> bool:
        return self.seconds < other.seconds
    
    def __le__(self, other: 'TimeInterval') -> bool:
        return self.seconds <= other.seconds
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TimeInterval):
            return False
        return abs(self.seconds - other.seconds) < 0.001
    
    def __add__(self, other: 'TimeInterval') -> float:
        """
        Перегрузка оператора сложения.
        Возвращает сумму в секундах.
        """
        return self.seconds + other.seconds


# КЛАССЫ ДЛЯ РАЗНЫХ ФОРМАТОВ ВРЕМЕННЫХ ИНТЕРВАЛОВ


class HmsTimeInterval(TimeInterval):
    """Класс для интервала в формате часы:минуты:секунды (HH:MM:SS)"""
    
    def _parse_to_seconds(self, value: str) -> float:
        """
        Парсит строку формата "часы:минуты:секунды".
        Пример: "01:30:00" = 1 час 30 минут = 5400 секунд
        
        Args:
            value: строка в формате HH:MM:SS
            
        Returns:
            длительность в секундах
        """
        try:
            parts = value.split(":")
            if len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
            elif len(parts) == 2:
                hours = 0
                minutes, seconds = map(int, parts)
            elif len(parts) == 1:
                hours = 0
                minutes = 0
                seconds = int(parts[0])
            else:
                raise ValueError(f"Неверный формат времени: {value}")
            
            return hours * 3600 + minutes * 60 + seconds
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга HMS формата '{value}': {e}")
    
    def get_format_name(self) -> str:
        return "Часы:минуты:секунды"


class MsTimeInterval(TimeInterval):
    """Класс для интервала в миллисекундах"""
    
    def _parse_to_seconds(self, value: str) -> float:
        """
        Парсит строку с миллисекундами.
        Пример: "90000" = 90000 мс = 90 секунд
        
        Args:
            value: строка с количеством миллисекунд
            
        Returns:
            длительность в секундах
        """
        try:
            milliseconds = int(value)
            return milliseconds / 1000.0
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга миллисекунд '{value}': {e}")
    
    def get_format_name(self) -> str:
        return "Миллисекунды"


class MinSecTimeInterval(TimeInterval):
    """Класс для интервала в формате минуты секунды (MM SS)"""
    
    def _parse_to_seconds(self, value: str) -> float:
        """
        Парсит строку формата "минуты секунды".
        Пример: "3 45" = 3 минуты 45 секунд = 225 секунд
        
        Args:
            value: строка в формате "минуты секунды"
            
        Returns:
            длительность в секундах
        """
        try:
            parts = value.split()
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
            elif len(parts) == 1:
                minutes = int(parts[0])
                seconds = 0
            else:
                raise ValueError(f"Неверный формат минут и секунд: {value}")
            
            return minutes * 60 + seconds
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга минут и секунд '{value}': {e}")
    
    def get_format_name(self) -> str:
        return "Минуты и секунды"


class HoursTimeInterval(TimeInterval):
    """Класс для интервала в часах (десятичный формат)"""
    
    def _parse_to_seconds(self, value: str) -> float:
        """
        Парсит строку с часами в десятичном формате.
        Пример: "2.5" = 2.5 часа = 9000 секунд
        
        Args:
            value: строка с количеством часов (может быть десятичной дробью)
            
        Returns:
            длительность в секундах
        """
        try:
            hours = float(value)
            return hours * 3600
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга часов '{value}': {e}")
    
    def get_format_name(self) -> str:
        return "Часы (десятичные)"


class SecondsTimeInterval(TimeInterval):
    """Класс для интервала в секундах"""
    
    def _parse_to_seconds(self, value: str) -> float:
        """
        Парсит строку с секундами.
        Пример: "3600" = 3600 секунд = 1 час
        
        Args:
            value: строка с количеством секунд
            
        Returns:
            длительность в секундах
        """
        try:
            return float(value)
        except ValueError as e:
            raise ValueError(f"Ошибка парсинга секунд '{value}': {e}")
    
    def get_format_name(self) -> str:
        return "Секунды"


# ФАБРИКА ДЛЯ СОЗДАНИЯ ОБЪЕКТОВ


class TimeIntervalFactory:
    """
    Фабрика для создания объектов временных интервалов
    на основе строкового описания формата и значения.
    """
    
    @staticmethod
    def create_interval(format_type: str, value: str) -> TimeInterval:
        """
        Создает объект временного интервала нужного типа.
        
        Args:
            format_type: тип формата (hms, ms, minsec, hours, seconds)
            value: значение интервала в строковом формате
            
        Returns:
            объект TimeInterval соответствующего класса
        """
        format_type = format_type.lower().strip()
        
        if format_type == "hms":
            return HmsTimeInterval(value)
        elif format_type == "ms":
            return MsTimeInterval(value)
        elif format_type == "minsec":
            return MinSecTimeInterval(value)
        elif format_type == "hours":
            return HoursTimeInterval(value)
        elif format_type == "seconds":
            return SecondsTimeInterval(value)
        else:
            raise ValueError(f"Неизвестный формат временного интервала: {format_type}")


# КОЛЛЕКЦИЯ ДЛЯ ХРАНЕНИЯ И ОБРАБОТКИ ИНТЕРВАЛОВ


class TimeIntervalCollection:
    """
    Коллекция для хранения и обработки временных интервалов разных форматов.
    Реализует общий интерфейс для работы с разнородными данными.
    """
    
    def __init__(self):
        """Инициализация пустой коллекции."""
        self.intervals: List[TimeInterval] = []
    
    def add_interval(self, interval: TimeInterval) -> None:
        """
        Добавляет интервал в коллекцию.
        
        Args:
            interval: объект временного интервала
        """
        self.intervals.append(interval)
    
    def add_from_string(self, format_type: str, value: str) -> None:
        """
        Создает и добавляет интервал на основе строкового описания.
        
        Args:
            format_type: тип формата
            value: значение интервала
        """
        interval = TimeIntervalFactory.create_interval(format_type, value)
        self.add_interval(interval)
    
    def clear(self) -> None:
        """Очищает коллекцию."""
        self.intervals.clear()
    
    def get_count(self) -> int:
        """
        Возвращает количество интервалов в коллекции.
        
        Returns:
            количество интервалов
        """
        return len(self.intervals)
    
    def sum(self) -> Dict[str, Any]:
        """
        Вычисляет сумму всех интервалов в коллекции.
        
        Returns:
            словарь с результатом в разных форматах
        """
        if not self.intervals:
            return {"seconds": 0, "formatted": "0 s", "hms": "00:00:00"}
        
        total_seconds = sum(interval.get_seconds() for interval in self.intervals)
        
        # Создаем фиктивный интервал для форматирования
        dummy = SecondsTimeInterval(str(total_seconds))
        
        return {
            "seconds": total_seconds,
            "formatted": dummy.get_formatted(),
            "hms": dummy.get_hms_format()
        }
    
    def avg(self) -> Dict[str, Any]:
        """
        Вычисляет среднее значение интервалов в коллекции.
        
        Returns:
            словарь со средним значением в разных форматах
        """
        if not self.intervals:
            return {"seconds": 0, "formatted": "0 s", "hms": "00:00:00"}
        
        total_seconds = sum(interval.get_seconds() for interval in self.intervals)
        avg_seconds = total_seconds / len(self.intervals)
        
        # Создаем фиктивный интервал для форматирования
        dummy = SecondsTimeInterval(str(avg_seconds))
        
        return {
            "seconds": avg_seconds,
            "formatted": dummy.get_formatted(),
            "hms": dummy.get_hms_format()
        }
    
    def max(self) -> Dict[str, Any]:
        """
        Находит максимальный интервал в коллекции.
        
        Returns:
            словарь с максимальным интервалом в разных форматах
        """
        if not self.intervals:
            return {"seconds": 0, "formatted": "0 s", "hms": "00:00:00", "original": None}
        
        max_interval = max(self.intervals)
        
        return {
            "seconds": max_interval.get_seconds(),
            "formatted": max_interval.get_formatted(),
            "hms": max_interval.get_hms_format(),
            "original": str(max_interval)
        }
    
    def min(self) -> Dict[str, Any]:
        """
        Находит минимальный интервал в коллекции.
        
        Returns:
            словарь с минимальным интервалом в разных форматах
        """
        if not self.intervals:
            return {"seconds": 0, "formatted": "0 s", "hms": "00:00:00", "original": None}
        
        min_interval = min(self.intervals)
        
        return {
            "seconds": min_interval.get_seconds(),
            "formatted": min_interval.get_formatted(),
            "hms": min_interval.get_hms_format(),
            "original": str(min_interval)
        }
    
    def filter_by_min_seconds(self, min_seconds: float) -> List[TimeInterval]:
        """
        Фильтрует интервалы по минимальной длительности.
        
        Args:
            min_seconds: минимальная длительность в секундах
            
        Returns:
            список интервалов, длительность которых >= min_seconds
        """
        return [interval for interval in self.intervals if interval.get_seconds() >= min_seconds]
    
    def filter_by_max_seconds(self, max_seconds: float) -> List[TimeInterval]:
        """
        Фильтрует интервалы по максимальной длительности.
        
        Args:
            max_seconds: максимальная длительность в секундах
            
        Returns:
            список интервалов, длительность которых <= max_seconds
        """
        return [interval for interval in self.intervals if interval.get_seconds() <= max_seconds]
    
    def find_by_format(self, format_name: str) -> List[TimeInterval]:
        """
        Находит все интервалы заданного формата.
        
        Args:
            format_name: название формата для поиска
            
        Returns:
            список интервалов заданного формата
        """
        return [interval for interval in self.intervals if interval.get_format_name() == format_name]
    
    def print_all(self) -> None:
        """Выводит информацию о всех интервалах в коллекции."""
        print(f"\nКоллекция содержит {self.get_count()} интервалов:")
        print("-" * 60)
        for i, interval in enumerate(self.intervals, 1):
            print(f"{i:3d}. {interval}")
        print("-" * 60)


# КЛАСС ДЛЯ ОБРАБОТКИ ВВОДА/ВЫВОДА


class TimeIntervalProcessor:
    """
    Класс для обработки ввода/вывода и взаимодействия с пользователем.
    """
    
    def __init__(self):
        """Инициализация процессора с пустой коллекцией."""
        self.collection = TimeIntervalCollection()
    
    def load_intervals_from_list(self, intervals_list: List[Dict[str, str]]) -> None:
        """
        Загружает интервалы из списка словарей.
        
        Args:
            intervals_list: список словарей вида {'format': 'hms', 'value': '01:30:00'}
        """
        for interval_data in intervals_list:
            try:
                self.collection.add_from_string(
                    interval_data['format'], 
                    interval_data['value']
                )
            except ValueError as e:
                print(f"Ошибка при загрузке интервала {interval_data}: {e}")
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Обрабатывает команду пользователя.
        
        Args:
            command: команда (sum, avg, max, min)
            
        Returns:
            словарь с результатом выполнения команды
        """
        command = command.lower().strip()
        
        if command == "sum":
            result = self.collection.sum()
            result["operation"] = "Сумма"
            return result
        elif command == "avg":
            result = self.collection.avg()
            result["operation"] = "Среднее"
            return result
        elif command == "max":
            result = self.collection.max()
            result["operation"] = "Максимум"
            return result
        elif command == "min":
            result = self.collection.min()
            result["operation"] = "Минимум"
            return result
        else:
            raise ValueError(f"Неизвестная команда: {command}")
    
    def print_result(self, result: Dict[str, Any]) -> None:
        """
        Выводит результат выполнения команды в удобном формате.
        
        Args:
            result: словарь с результатом
        """
        operation = result.get("operation", "Результат")
        
        print(f"\n{operation}:")
        print(f"  В секундах: {result['seconds']:.2f} с")
        print(f"  Форматировано: {result['formatted']}")
        print(f"  Формат ЧЧ:ММ:СС: {result['hms']}")
        
        if "original" in result and result["original"]:
            print(f"  Исходный интервал: {result['original']}")


# ПРИМЕР ИСПОЛЬЗОВАНИЯ


def main():
    """
    Основная функция с примерами использования системы.
    """
    print("=" * 70)
    print("ЛАБОРАТОРНАЯ РАБОТА №4: ПОЛИМОРФИЗМ")
    print("Тема: Общий интерфейс и наследование для разнородных данных")
    print("=" * 70)
    
    # Создаем процессор
    processor = TimeIntervalProcessor()
    
    # Пример 1: Загрузка интервалов в разных форматах
    print("\n" + "="*70)
    print("ПРИМЕР 1: ЗАГРУЗКА ИНТЕРВАЛОВ В РАЗНЫХ ФОРМАТАХ")
    print("="*70)
    
    intervals_data = [
        {"format": "hms", "value": "01:30:00"},      # 1 час 30 минут
        {"format": "ms", "value": "90000"},          # 90 секунд
        {"format": "minsec", "value": "3 45"},       # 3 минуты 45 секунд
        {"format": "hours", "value": "2.5"},         # 2.5 часа
        {"format": "seconds", "value": "3600"},      # 1 час
        {"format": "hms", "value": "00:45:30"},      # 45 минут 30 секунд
        {"format": "ms", "value": "1500"},           # 1.5 секунды
    ]
    
    print("\nЗагружаем интервалы:")
    for data in intervals_data:
        print(f"  {data['format']}: {data['value']}")
    
    processor.load_intervals_from_list(intervals_data)
    
    # Выводим информацию о всех интервалах
    processor.collection.print_all()
    
    # Пример 2: Выполнение операций через общий интерфейс
    print("\n" + "="*70)
    print("ПРИМЕР 2: ВЫПОЛНЕНИЕ ОПЕРАЦИЙ ЧЕРЕЗ ОБЩИЙ ИНТЕРФЕЙС")
    print("="*70)
    
    # Команды для обработки
    commands = ["sum", "avg", "max", "min"]
    
    for command in commands:
        try:
            result = processor.process_command(command)
            processor.print_result(result)
        except ValueError as e:
            print(f"Ошибка при выполнении команды '{command}': {e}")
    
    # Пример 3: Фильтрация и поиск
    print("\n" + "="*70)
    print("ПРИМЕР 3: ФИЛЬТРАЦИЯ И ПОИСК")
    print("="*70)
    
    # Фильтрация интервалов длительностью более 60 секунд
    print("\nИнтервалы длительностью более 60 секунд:")
    long_intervals = processor.collection.filter_by_min_seconds(60)
    for i, interval in enumerate(long_intervals, 1):
        print(f"  {i}. {interval}")
    
    # Поиск интервалов в формате HMS
    print("\nИнтервалы в формате 'Часы:минуты:секунды':")
    hms_intervals = processor.collection.find_by_format("Часы:минуты:секунды")
    for i, interval in enumerate(hms_intervals, 1):
        print(f"  {i}. {interval}")
    
    # Пример 4: Демонстрация полиморфизма
    print("\n" + "="*70)
    print("ПРИМЕР 4: ДЕМОНСТРАЦИЯ ПОЛИМОРФИЗМА")
    print("="*70)
    
    # Создаем интервалы разных типов
    print("\nСоздаем интервалы разных типов:")
    interval1 = HmsTimeInterval("02:15:30")
    interval2 = MsTimeInterval("75000")  # 75 секунд
    interval3 = HoursTimeInterval("0.75")  # 0.75 часа = 45 минут
    
    # Добавляем их в список (полиморфизм: разные типы в одном списке)
    polymorphic_list = [interval1, interval2, interval3]
    
    print("\nОбрабатываем интервалы через общий интерфейс:")
    for i, interval in enumerate(polymorphic_list, 1):
        print(f"\nИнтервал {i}:")
        print(f"  Тип: {interval.get_format_name()}")
        print(f"  Секунды: {interval.get_seconds():.2f}")
        print(f"  Форматировано: {interval.get_formatted()}")
        print(f"  ЧЧ:ММ:СС: {interval.get_hms_format()}")
    
    # Пример 5: Создание коллекции вручную
    print("\n" + "="*70)
    print("ПРИМЕР 5: СОЗДАНИЕ КОЛЛЕКЦИИ ВРУЧНУЮ")
    print("="*70)
    
    # Создаем новую коллекцию
    manual_collection = TimeIntervalCollection()
    
    # Добавляем интервалы вручную
    manual_collection.add_interval(HmsTimeInterval("00:10:00"))
    manual_collection.add_interval(MinSecTimeInterval("5 30"))
    manual_collection.add_interval(SecondsTimeInterval("7200"))
    
    manual_collection.print_all()
    
    # Вычисляем сумму
    sum_result = manual_collection.sum()
    print(f"\nСумма всех интервалов: {sum_result['formatted']}")
    
    print("\n" + "="*70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("="*70)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    pass # Ваш код здесь
