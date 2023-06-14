import psycopg2

def get_db_connection():
    connection = psycopg2.connect(
        user="ynpravee",
        password="Sari@9505",
        host="localhost",
        port="5432",
        database="function_hall_booking"
    )
    return connection
