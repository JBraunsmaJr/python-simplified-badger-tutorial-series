def ingest_market(filepath: str):
    header: list = []

    with open(filepath, "r") as file:
        while True:
            current_line = file.readline()

            if not current_line:
                break

            if current_line.startswith('#'):
                header = current_line[1:].strip().split(',')
                continue

            if current_line.strip() == "" or len(header) <= 0:
                continue

            result: dict = dict()
            split = current_line.strip().split(',')

            for index in range(len(split)):
                result[header[index]] = split[index]

            yield result


def display_market():
    id_count = 1
    for item in ingest_market("example.csv"):
        item["id"] = id_count
        id_count += 1
        print(f"We have {item['count']} of {item['name']} in stock. With an id of {item['id']}")


display_market()