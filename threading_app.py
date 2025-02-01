# Розробіть програму, яка паралельно обробляє та аналізує текстові файли для пошуку визначених ключових слів.

# 1. Реалізація багатопотокового підходу до обробки файлів (використовуючи threading):

# Розділіть список файлів між різними потоками.
# Кожен потік має шукати задані ключові слова у своєму наборі файлів.
# Зберіть і виведіть результати пошуку з усіх потоків.

# Критерії прийняття
# - Реалізовано багатопотоковий підхід до обробки файлів.
# - Забезпечено розподілення файлів між потоками/процесами.
# - Код вимірює та виводить час виконання для кожної з версій.
# - Забезпечено обробку помилок і винятків, особливо при роботі з файловою системою.
# - Обидві версії програми повертають словник, де ключ — це пошукове слово, а значення — список шляхів файлів, де це слово знайдено.

from threading import Thread
import time

list_of_files = ['./file1.txt', './file2.txt', './file3.txt', './file4.txt', './file5.txt']

def read(file):
    try:
        with open(file, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {file} not found.")
        return ""
    except IOError:
        print(f"Error reading file {file}.")
        return ""

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

def threaded_search(files, words, result, index):
    result[index] = search_files(files, words)

if __name__ == '__main__':
    words = ['possession', 'star', 'passage', 'blood', 'earth', 'life', 'death', 'time']
    start = time.time()
    
    # Розподіл файлів між потоками
    num_threads = 2
    files_per_thread = len(list_of_files) // num_threads
    threads = []
    results = [None] * num_threads

    for i in range(num_threads):
        start_index = i * files_per_thread
        end_index = (i + 1) * files_per_thread if i != num_threads - 1 else len(list_of_files)
        thread_files = list_of_files[start_index:end_index]
        thread = Thread(target=threaded_search, args=(thread_files, words, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Об'єднання результатів
    final_result = {}
    for result in results:
        for word, files_dict in result.items():
            for word, files in files_dict.items():
                if word in final_result:
                    final_result[word].extend(files)
                else:
                    final_result[word] = files

    print(final_result)
    print('Time:', time.time() - start)