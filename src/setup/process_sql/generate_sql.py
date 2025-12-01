import json


def generate_type(source: str, dest: str) -> None:
    queries: list[str] = []

    with open(source, "r") as f:
        data: dict = json.load(f)

    typechart: dict[str, dict[str, int]] = data["typechart"]

    # Populate the Type table first
    for t in typechart:
        queries.append(f"INSERT INTO Type (name) VALUES ('{t}');")

    # Populate the TypeEffectiveness table
    for df in typechart:
        for att in typechart[df]:
            # Ignore weather/status effects, only include types
            if att in typechart:
                queries.append(
                    f"INSERT INTO TypeEffectiveness (attackingType, defendingType, effectiveness) VALUES ('{att}', '{df}', {typechart[df][att]});")

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
            f"INSERT INTO Item (id, name) VALUES (\'{i}\', \'{items[i]['name']}\');")

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
            f"INSERT INTO Ability (id, name) VALUES (\'{a}\', \'{abilities[a]['name']}\');")

    with open(dest, "w") as f:
        for q in queries:
            # print(q)
            f.write(q.strip() + "\n")

    print("Finished writing Ability queries into", dest)


def generate_move(source: str, dest: str) -> None:
    queries: list[str] = []

    with open(source, "r") as f:
        data: dict = json.load(f)

    moves: dict[str, dict[str, str | int | bool]] = data["moves"]

    for m in moves:
        acc: str = "NULL" if moves[m]["accuracy"] is True else str(
            moves[m]["accuracy"])
        queries.append(
            f"INSERT INTO Move (id, name, type, power, category, pp, accuracy) VALUES (\'{m}\', \'{moves[m]['name']}\', \'{moves[m]['type']}\', {moves[m]['power']}, \'{moves[m]['category']}\', {moves[m]['pp']}, {acc});")

    with open(dest, "w") as f:
        for q in queries:
            # print(q)
            f.write(q.strip() + "\n")

    print("Finished writing Move queries into", dest)


def generate_metadata(dest: str) -> None:
    # hardcoded because i'm lazy
    INSERT_METAGAME: str = "INSERT INTO Metagame (name) VALUES ('{}');"
    INSERT_PERIOD: str = "INSERT INTO Period (id, startDate, endDate) VALUES {};"
    INSERT_CUTOFF: str = "INSERT INTO Cutoff (elo) VALUES ({});"
    INSERT_MAPF: str = "INSERT INTO MetagameAllowsPokemonFrom (parentMetagame, childMetagame) VALUES ('{}', '{}');"

    PERIODS: list[str] = [
        "('2025-07', '2025-07-01 00:00:00.000', '2025-07-31 23:59:59.997')",
        "('2025-08', '2025-08-01 00:00:00.000', '2025-08-31 23:59:59.997')",
        "('2025-09', '2025-09-01 00:00:00.000', '2025-09-30 23:59:59.997')",
        "('2025-10', '2025-10-01 00:00:00.000', '2025-10-31 23:59:59.997')"
    ]
    METAGAMES: list[str] = ["Ubers", "OU", "UU", "RU", "NU", "PU", "ZU"]
    CUTOFFS: list[int] = [0, 1760, 1825]

    with open(dest, "w") as f:
        for m in METAGAMES:
            f.write(INSERT_METAGAME.format(m.strip()) + "\n")

        for p in PERIODS:
            f.write(INSERT_PERIOD.format(p.strip()) + "\n")

        for c in CUTOFFS:
            f.write(INSERT_CUTOFF.format(c) + "\n")

        for i in range(len(METAGAMES) - 1):
            for j in range(i + 1, len(METAGAMES)):
                f.write(INSERT_MAPF.format(
                    METAGAMES[i].strip(), METAGAMES[j].strip()) + "\n")

    print("Finished writing Metagame, Period, Cutoff, MetagameAllowsPokemonFrom queries into", dest)


def generate_pokedex(source: str, dest: str) -> None:
    # more complicated metagame mapping
    METAGAMES: dict[str, str] = {
        "Ubers": "Ubers",
        "OU": "OU",
        "UUBL": "OU",
        "UU": "UU",
        "RUBL": "UU",
        "RU": "RU",
        "NUBL": "RU",
        "NU": "NU",
        "PUBL": "NU",
        "PU": "PU",
        "ZUBL": "PU",
        "ZU": "ZU",
        "NFE": "ZU",
        "LC": "ZU"
    }
    INSERT_POKEMON: str = "INSERT INTO Pokemon VALUES ('{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {});"

    queries: list[str] = []

    with open(source, "r") as f:
        data: dict = json.load(f)

    pokedex: dict[str, dict[str, str | list[str]
                            | dict[str, int]]] = data["pokedex"]

    # Insert Pokemon table first
    for p in pokedex:
        name: str = pokedex[p]["name"]
        type1: str = pokedex[p]["types"][0]
        type2: str
        if len(pokedex[p]["types"]) > 1:
            type2 = ("\'" + pokedex[p]["types"][1] + "\'")
        else:
            type2 = "NULL"
        hp: int = pokedex[p]["baseStats"]["hp"]
        atk: int = pokedex[p]["baseStats"]["atk"]
        df: int = pokedex[p]["baseStats"]["def"]
        spa: int = pokedex[p]["baseStats"]["spa"]
        spd: int = pokedex[p]["baseStats"]["spd"]
        spe: int = pokedex[p]["baseStats"]["spe"]
        tier: str
        if ("tier" in pokedex[p] and pokedex[p]["tier"] in METAGAMES):
            tier = ("\'" + METAGAMES[pokedex[p]["tier"]] + "\'")
        else:
            tier = "NULL"

        queries.append(INSERT_POKEMON.format(p, name, type1,
                                             type2, hp, atk, df, spa, spd, spe, tier))

    # Insert PokemonHasAbility table
    for p in pokedex:
        abilities: list[str] = pokedex[p]["abilities"]
        for a in abilities:
            queries.append(
                f"INSERT INTO PokemonHasAbility (pokemon, ability) VALUES ('{p}', '{a}');")

    # Insert PokemonLearnsMove table
    for p in pokedex:
        moves: list[str] = pokedex[p]["moves"]
        for m in moves:
            queries.append(
                f"INSERT INTO PokemonLearnsMove (pokemon, move) VALUES ('{p}', '{m}');")

    with open(dest, "w") as f:
        for q in queries:
            # print(q)
            f.write(q.strip() + "\n")

    print("Finished writing Pokemon, PokemonHasAbility and PokemonLearnsMove queries into", dest)


def main() -> None:
    generate_type(
        "../../data/showdown_data_processed/typechart.json", "./type.sql")
    generate_item(
        "../../data/showdown_data_processed/items.json", "./item.sql")
    generate_ability(
        "../../data/showdown_data_processed/abilities.json", "./ability.sql")
    generate_move(
        "../../data/showdown_data_processed/moves.json", "./move.sql")
    generate_metadata("./metadata.sql")
    generate_pokedex(
        "../../data/showdown_data_processed/pokedex.json", "./pokedex.sql")


if __name__ == "__main__":
    main()
