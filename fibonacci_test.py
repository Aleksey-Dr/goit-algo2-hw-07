import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# Реалізація Splay Tree
# Цей клас забезпечує основну функціональність Splay Tree,
# таку як вставка, пошук та перестановка вузлів (splaying).
# Ми не будемо заглиблюватись в деталі його реалізації тут,
# оскільки це доволі складна структура даних.
class Node:
    def __init__(self, key, value, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, node):
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if grandparent:
                if (grandparent.left == parent and parent.left == node) or \
                   (grandparent.right == parent and parent.right == node):
                    self._rotate(parent)
                else:
                    self._rotate(node)
            self._rotate(node)
        self.root = node

    def _rotate(self, node):
        parent = node.parent
        grandparent = parent.parent
        if grandparent:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node
        node.parent = grandparent
        
        if parent.left == node:
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
        else:
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent
        parent.parent = node

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return
        
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                node.value = value
                self._splay(node)
                return

        new_node = Node(key, value, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)
    
    def find(self, key):
        node = self.root
        while node:
            if key == node.key:
                self._splay(node)
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

# Функція fibonacci_lru з декоратором @lru_cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Функція fibonacci_splay
def fibonacci_splay(n, tree):
    # Попытка найти значение в дереве
    found_value = tree.find(n)
    
    # Если значение найдено (не равно None), вернуть его
    if found_value is not None:
        return found_value
    
    # Если значение не найдено, вычислить его
    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    
    # Вставить вычисленное значение в дерево
    tree.insert(n, result)
    return result

# Увімкнути інтерактивний режим
plt.ion()

# Набір чисел Фібоначчі для обчислення
fib_numbers = list(range(0, 1000, 50))
splay_tree = SplayTree()
results = []
lru_cache_times = []
splay_tree_times = []

# Вимірювання часу для LRU Cache
for n in fib_numbers:
    lru_cache_times.append(timeit.timeit(lambda: fibonacci_lru(n), number=100))

# Вимірювання часу для Splay Tree
for n in fib_numbers:
    splay_tree_times.append(timeit.timeit(lambda: fibonacci_splay(n, splay_tree), number=100))
    results.append({
        'n': n,
        'lru_cache_time': lru_cache_times[-1],
        'splay_tree_time': splay_tree_times[-1]
    })

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(fib_numbers, lru_cache_times, marker='o', label='LRU Cache')
plt.plot(fib_numbers, splay_tree_times, marker='x', label='Splay Tree')
plt.xlabel('Число Фібоначчі (n)')
plt.ylabel('Середній час виконання (секунди)')
plt.title('Порівняння часу виконання для LRU Cache та Splay Tree')
plt.grid(True)
plt.legend()
plt.show(block=False)  # Графік відображається без блокування

# ANSI escape-послідовності для кольору та скидання кольору
RED = '\033[91m'
GREEN = '\033[92m' # Код для яскраво-зеленого кольору
BLUE = '\033[94m'  # Код для яскраво-синього кольору
RESET = '\033[0m'

# Виведення таблиці з кольоровим заголовком
print(f"{RED}{'n':<10} {'LRU Cache Time (s)':<20} {'Splay Tree Time (s)':<20}{RESET}")
print(f"{RED} {'-' * 55} {RESET}")
for result in results:
    print(f"{BLUE}{result['n']:<10}{RESET} {GREEN}{result['lru_cache_time']:<20.8f}{RESET} {result['splay_tree_time']:<20.8f}".format(
        result['n'],
        result['lru_cache_time'],
        result['splay_tree_time']
    ))

plt.show(block=True)  # Блокує виконання, щоб вікно не закрилося одразу