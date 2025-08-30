import time
import random
from collections import OrderedDict

# Клас LRUCache
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: any) -> any:
        if key not in self.cache:
            return -1
        # Переміщуємо використаний елемент в кінець
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: any, value: any):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            # Видаляємо найстаріший (перший) елемент
            self.cache.popitem(last=False)

# Функція для генерації запитів
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n // 2), random.randint(n // 2, n - 1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)
            queries.append(("Range", left, right))
    return queries

# Функції без кешу
def range_sum_no_cache(arr, left, right):
    return sum(arr[left:right + 1])

def update_no_cache(arr, index, value):
    arr[index] = value

# Функції з кешем
def range_sum_with_cache(arr, left, right, cache):
    key = (left, right)
    result = cache.get(key)
    if result != -1:  # Cache hit
        return result
    else:  # Cache miss
        s = sum(arr[left:right + 1])
        cache.put(key, s)
        return s

def update_with_cache(arr, index, value, cache):
    arr[index] = value
    # Інвалідація кешу: видаляємо всі діапазони, що містять змінений індекс
    invalid_keys = [key for key in cache.cache.keys() if key[0] <= index <= key[1]]
    for key in invalid_keys:
        del cache.cache[key]

# Основний блок програми
if __name__ == '__main__':
    N = 100_000
    Q = 50_000
    K = 1000

    # Генерація вихідного масиву та запитів
    array_base = [random.randint(1, 100) for _ in range(N)]
    queries = make_queries(n=N, q=Q)

    # ------------------ Вимірювання без кешу ------------------
    array_no_cache = list(array_base)  # Копія масиву для тесту без кешу
    start_time_no_cache = time.time()
    
    for query_type, *args in queries:
        if query_type == "Range":
            range_sum_no_cache(array_no_cache, *args)
        elif query_type == "Update":
            update_no_cache(array_no_cache, *args)

    end_time_no_cache = time.time()
    total_time_no_cache = end_time_no_cache - start_time_no_cache
    
    # ------------------ Вимірювання з кешем ------------------
    array_with_cache = list(array_base) # Копія масиву для тесту з кешем
    lru_cache = LRUCache(K)
    start_time_with_cache = time.time()
    
    for query_type, *args in queries:
        if query_type == "Range":
            range_sum_with_cache(array_with_cache, *args, lru_cache)
        elif query_type == "Update":
            update_with_cache(array_with_cache, *args, lru_cache)

    end_time_with_cache = time.time()
    total_time_with_cache = end_time_with_cache - start_time_with_cache
    
    # ------------------ Виведення результатів ------------------
    print(f"Без кешу : {total_time_no_cache: >8.2f} c")
    print(f"LRU-кеш  : {total_time_with_cache: >8.2f} c", end="")
    if total_time_with_cache > 0:
        speedup = total_time_no_cache / total_time_with_cache
        print(f" (прискорення ×{speedup:.1f})")
    else:
        print()