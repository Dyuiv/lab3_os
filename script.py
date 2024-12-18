import threading
from collections import defaultdict

INPUT_FILE = 'contacts.txt'
OUTPUT_FILE = 'result.txt'
NUM_THREADS = 4
def process_chunk(lines):
    result = defaultdict(list)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(";")
        if len(parts) != 4:
            continue
        lastname, firstname, secondname, phone = parts
        first_letter = lastname[0].upper() if lastname else '#'
        result[first_letter].append((lastname, firstname, secondname, phone))
    return result

def merge_dicts(main_dict, local_dict):
    for key, values in local_dict.items():
        main_dict[key].extend(values)

def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chunk_size = max(1, len(lines) // NUM_THREADS)
    chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]

    results = []
    threads = []
    lock = threading.Lock()

    def worker(c):
        local_result = process_chunk(c)
        with lock:
            results.append(local_result)

    for c in chunks:
        thread = threading.Thread(target=worker, args=(c,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    final_result = defaultdict(list)
    for r in results:
        merge_dicts(final_result, r)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for letter in sorted(final_result.keys()):
            f.write(f"Буква: {letter}\n")
            for (lastname, firstname, patronymic, phone) in final_result[letter]:
                f.write(f"{lastname};{firstname};{patronymic};{phone}\n")
            f.write("\n")

if __name__ == "__main__":
    main()
