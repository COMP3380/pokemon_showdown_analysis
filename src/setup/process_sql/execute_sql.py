import pymssql
from pathlib import Path
SQL_DIR = Path(__file__).resolve().parent  

SERVER: str = "uranium.cs.umanitoba.ca"
USER: str = "vuqh1"
PASSWORD: str = "7990597"
DATABASE: str = "cs3380"


def execute_sql_file(cursor, filename: Path) -> None:
    print("Reading", filename)
    with open(filename, "r") as f:
        sql: str = f.read()

    print("Executing", filename)
    cursor.execute(sql)
    print("Finished execution of", filename)


def main() -> None:
    connection = pymssql.connect(
        server=SERVER, user=USER, password=PASSWORD, database=DATABASE
    )
    cursor = connection.cursor()

    execute_sql_file(cursor, SQL_DIR / "init.sql")
    execute_sql_file(cursor, SQL_DIR / "type.sql")
    execute_sql_file(cursor, SQL_DIR / "item.sql")
    execute_sql_file(cursor, SQL_DIR / "ability.sql")
    execute_sql_file(cursor, SQL_DIR / "move.sql")
    execute_sql_file(cursor, SQL_DIR / "metadata.sql")
    execute_sql_file(cursor, SQL_DIR / "pokedex.sql")
    for p in ["2025-07", "2025-08", "2025-09"]:
        for m in ["Ubers", "UU", "RU", "NU", "PU", "ZU"]:
            execute_sql_file(cursor, SQL_DIR / f"stats_{p}_{m}_0.sql")
            execute_sql_file(cursor, SQL_DIR / f"stats_{p}_{m}_1760.sql")
        execute_sql_file(cursor, SQL_DIR / f"stats_{p}_OU_0.sql")
        execute_sql_file(cursor, SQL_DIR / f"stats_{p}_OU_1825.sql")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
