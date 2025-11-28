import pymssql

SERVER: str = "uranium.cs.umanitoba.ca"
USER: str = "vuqh1"
PASSWORD: str = "7990597"
DATABASE: str = "cs3380"


def execute_sql_file(cursor, filename: str) -> None:
    with open(filename, "r") as f:
        sql: str = f.read()

    cursor.execute(sql)


def main() -> None:
    connection = pymssql.connect(
        server=SERVER, user=USER, password=PASSWORD, database=DATABASE
    )
    cursor = connection.cursor()

    execute_sql_file(cursor, "init.sql")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
