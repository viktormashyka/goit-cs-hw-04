
# Розробіть програму, яка паралельно обробляє та аналізує текстові файли для пошуку визначених ключових слів.

# 2. Реалізація багатопроцесорного підходу до обробки файлів (використовуючи multiprocessing):

# Розділіть список файлів між різними процесами.
# Кожен процес має обробляти свою частину файлів, шукаючи ключові слова.
# Використайте механізм обміну даними (наприклад, через Queue) для збору та виведення результатів пошуку.

# Критерії прийняття
# - Реалізовано багатопроцесорний підхід до обробки файлів.
# - Забезпечено розподілення файлів між потоками/процесами.
# - Код вимірює та виводить час виконання для кожної з версій.
# - Забезпечено обробку помилок і винятків, особливо при роботі з файловою системою.
# - Обидві версії програми повертають словник, де ключ — це пошукове слово, а значення — список шляхів файлів, де це слово знайдено.

from multiprocessing import Process, Queue
import time

list_of_files = ['./file1.txt', './file2.txt', './file3.txt', './file4.txt', './file5.txt']

def read(file):
    with open(file, 'r') as f:
        return f.read()

def search(file, word):
    return word in read(file)

def read_files(files, word):
    result = {}
    for file in files:
        if search(file, word):
            if word in result:
                result[word].append(file)
            else:
                result[word] = [file]
    return result

def search_files(files, words):
    result = {}
    for word in words:
        result[word] = read_files(files, word)
    return result

def process_search(files, words, queue):
    result = search_files(files, words)
    queue.put(result)

if __name__ == '__main__':
    words = ['possession', 'star', 'passage', 'blood', 'earth', 'life', 'death', 'time']
    start = time.time()
    
    # Розподіл файлів між процесами
    num_processes = 2
    files_per_process = len(list_of_files) // num_processes
    processes = []
    queue = Queue()

    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = (i + 1) * files_per_process if i != num_processes - 1 else len(list_of_files)
        process_files = list_of_files[start_index:end_index]
        process = Process(target=process_search, args=(process_files, words, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Об'єднання результатів
    final_result = {}
    while not queue.empty():
        result = queue.get()
        for word, files_dict in result.items():
            for word, files in files_dict.items():
                if word in final_result:
                    final_result[word].extend(files)
                else:
                    final_result[word] = files

    print(final_result)
    print('Time:', time.time() - start)