import sqlite3
from datetime import datetime

DATABASE = "support.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(conn, table_name, column_name):

    columns = conn.execute(
        f"PRAGMA table_info({table_name})"
    ).fetchall()

    return any(
        column["name"] == column_name
        for column in columns
    )


def add_column_if_missing(
    conn,
    table_name,
    column_name,
    column_type
):

    if not column_exists(
        conn,
        table_name,
        column_name
    ):

        conn.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_type}
            """
        )


def initialize_database():

    conn = get_db_connection()

    # ==========================================
    # USERS TABLE
    # ==========================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password_hash TEXT NOT NULL,

            role TEXT DEFAULT 'customer',

            created_at TEXT

        )
    """)

    # ==========================================
    # TICKETS TABLE
    # ==========================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket_id TEXT UNIQUE,

            customer_name TEXT NOT NULL,

            query TEXT NOT NULL,

            department TEXT,

            category TEXT DEFAULT 'General',

            priority TEXT DEFAULT 'Medium',

            priority_score INTEGER DEFAULT 50,

            resolution TEXT DEFAULT '',

            escalation TEXT DEFAULT 'Handled by AI',

            feedback TEXT DEFAULT 'No Feedback',

            status TEXT DEFAULT 'Open',

            created_at TEXT

        )
    """)

    # ==========================================
    # UPGRADE EXISTING TICKETS TABLE
    # ==========================================

    columns_to_add = [

        ("ticket_id", "TEXT"),

        ("category", "TEXT"),

        ("priority", "TEXT"),

        ("priority_score", "INTEGER"),

        ("resolution", "TEXT"),

        ("escalation", "TEXT"),

        ("feedback", "TEXT"),

        ("status", "TEXT"),

        ("created_at", "TEXT")

    ]

    for column_name, column_type in columns_to_add:

        add_column_if_missing(
            conn,
            "tickets",
            column_name,
            column_type
        )

    # ==========================================
    # FEEDBACK TABLE
    # ==========================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket_id TEXT,

            rating TEXT,

            comment TEXT,

            created_at TEXT

        )
    """)

    # ==========================================
    # UPDATE OLD TICKETS
    # ==========================================

    tickets = conn.execute(
        "SELECT * FROM tickets"
    ).fetchall()

    for ticket in tickets:

        # Create ticket ID if missing

        if not ticket["ticket_id"]:

            ticket_id = (
                "TKT-" +
                datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                ) +
                str(ticket["id"])
            )

            conn.execute(
                """
                UPDATE tickets

                SET ticket_id = ?

                WHERE id = ?
                """,
                (
                    ticket_id,
                    ticket["id"]
                )
            )

        # Fill missing values

        conn.execute(
            """
            UPDATE tickets

            SET

                category =
                    COALESCE(
                        category,
                        'General'
                    ),

                priority =
                    COALESCE(
                        priority,
                        'Medium'
                    ),

                priority_score =
                    COALESCE(
                        priority_score,
                        50
                    ),

                resolution =
                    COALESCE(
                        resolution,
                        ''
                    ),

                escalation =
                    COALESCE(
                        escalation,
                        'Handled by AI'
                    ),

                feedback =
                    COALESCE(
                        feedback,
                        'No Feedback'
                    ),

                status =
                    COALESCE(
                        status,
                        'Open'
                    ),

                created_at =
                    COALESCE(
                        created_at,
                        ?
                    )

            WHERE id = ?
            """,
            (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                ticket["id"]
            )
        )
        conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'customer',
        created_at TEXT NOT NULL
    )
""")

    conn.commit()

    conn.close()

    print(
        "✅ Database initialized successfully."
    )


if __name__ == "__main__":

    initialize_database()