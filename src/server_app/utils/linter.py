def process_linter_results(filename: str, results: dict) -> dict:
    with open(filename, "r") as file:
        for line in file.readlines():
            splitted = line.split(":")
            if splitted[0] not in results.keys():
                results[splitted[0]] = ""
            results[splitted[0]] += f"{''.join(splitted[1:])}\n"
    return results
