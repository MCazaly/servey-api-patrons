import csv


def get_patrons(path, whitelist):
    with open(path, "r") as file:
        reader = csv.reader(file, delimiter=",")
        keys = next(reader)
        patrons = {}
        for row in reader:
            patron = {}
            for index, key in enumerate(keys):
                if key in whitelist:
                    new_key = key.lower().replace(" ", "_")
                else:
                    continue
                value = row[index]
                try:
                    value = float(value)  # Convert monetary values to numeric
                except ValueError:
                    pass
                patron[new_key] = value
            patrons[patron["user_id"]] = patron
    return patrons
