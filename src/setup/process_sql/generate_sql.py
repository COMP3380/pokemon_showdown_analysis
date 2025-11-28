import json


def generate_type(source: str, dest: str) -> None:
    queries: list[str] = []

    with open(source, "r") as f:
        data: dict = json.load(f)

    typechart: dict[str, dict[str, int]] = data["typechart"]

    # Populate the Type table first
    for t in typechart:
        queries.append(f"INSERT INTO Type (name) VALUES ({t});")

    # Populate the TypeEffectiveness table
    for df in typechart:
        for att in typechart[df]:
            # Ignore weather/status effects, only include types
            if att in typechart:
                queries.append(
                    f"INSERT INTO TypeEffectiveness (attackingType, defendingType, effectiveness) VALUES ({att}, {df}, {typechart[df][att]});")

    with open(dest, "w") as f:
        for q in queries:
            # print(q)
            f.write(q.strip() + "\n")

    print("Finished writing Type and TypeEffectiveness queries into", dest)


def generate_item(source: str, dest: str) -> None:
    queries: list[str] = []

    with open(source, "r") as f:
        data: dict = json.load(f)

    items: dict[str, dict[str, str]] = data["items"]

    for i in items:
        queries.append(
            f"INSERT INTO Item (id, name) VALUES ({i}, {items[i]['name']});")

    with open(dest, "w") as f:
        for q in queries:
            # print(q)
            f.write(q.strip() + "\n")

    print("Finished writing Item queries into", dest)


def generate_ability(source: str, dest: str) -> None:
    queries: list[str] = []

    with open(source, "r") as f:
        data: dict = json.load(f)

    abilities: dict[str, dict[str, str]] = data["abilities"]

    for a in abilities:
        queries.append(
            f"INSERT INTO Ability (id, name) VALUES ({a}, {abilities[a]['name']});")

    with open(dest, "w") as f:
        for q in queries:
            # print(q)
            f.write(q.strip() + "\n")

    print("Finished writing Ability queries into", dest)


def main() -> None:
    generate_type(
        "../../data/showdown_data_processed/typechart.json", "./type.sql")
    generate_item(
        "../../data/showdown_data_processed/items.json", "./item.sql")
    generate_ability(
        "../../data/showdown_data_processed/abilities.json", "./ability.sql")


if __name__ == "__main__":
    main()
