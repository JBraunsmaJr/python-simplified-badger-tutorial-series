with open("../../March-06-2022_ReadWriteFiles/starter-content/example.txt") as example_file:
    line_number = 0
    while True:
        current_line = example_file.readline()

        if not current_line:
            break

        print(f"[{line_number}]\t{current_line.strip()}")
        line_number += 1
