import sqlite3

from config import DATABASE_PATH


def execute_sql(query):
    """
    Execute only SELECT queries on the SQLite database.
    """

    query = query.strip()

    if not query.lower().startswith("select"):
        return "Only SELECT queries are allowed."

    connection = None

    try:

        connection = sqlite3.connect(DATABASE_PATH)

        cursor = connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        if not rows:
            return "No records found."

        output = ""

        output += " | ".join(columns)
        output += "\n"
        output += "-" * 60
        output += "\n"

        for row in rows:
            output += " | ".join(str(value) for value in row)
            output += "\n"

        return output

    except Exception as e:

        return f"SQL Error: {e}"

    finally:

        if connection:
            connection.close()