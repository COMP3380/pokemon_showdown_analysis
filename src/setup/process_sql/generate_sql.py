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


def main() -> None:
    generate_type(
        "../../data/showdown_data_processed/typechart.json", "./type.sql")


if __name__ == "__main__":
    main()
