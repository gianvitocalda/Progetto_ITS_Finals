import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


def inizializza_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("[DB] Connessione riuscita. Verifica struttura in corso...")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riders (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                vehicle VARCHAR NOT NULL,
                total_deliveries INT DEFAULT 0
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                rider_id INT NOT NULL,
                customer_name VARCHAR NOT NULL,
                rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment VARCHAR,
                CONSTRAINT fk_rider FOREIGN KEY (rider_id)
                REFERENCES riders(id)
                ON DELETE CASCADE
            );
        """)

        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM riders;")

        if cursor.fetchone()[0] == 0:

            print("[DB] Tabelle vuote. Inserimento di 5 record demo...")

            riders_data = [
                ('Marco Rossi', 'Bicicletta', 120),
                ('Annamaria Bianchi', 'Scooter', 340),
                ('Luca Verdi', 'Auto', 85),
                ('Giulia Neri', 'Monopattino', 42),
                ('Alessandro Gallo', 'Scooter', 510)
            ]

            cursor.executemany(
                "INSERT INTO riders (name, vehicle, total_deliveries) VALUES (%s,%s,%s)",
                riders_data
            )

            reviews_data = [
                (1, 'Giovanni S.', 5, 'Consegna velocissima e cibo caldissimo!'),
                (2, 'Elena M.', 4, 'Molto gentile, ha avuto solo un attimo di ritardo per il traffico.'),
                (3, 'Roberto F.', 5, 'Tutto perfetto, consigliato.'),
                (1, 'Alice V.', 2, 'Il pacco era un po schiacciato.'),
                (5, 'Stefano B.', 5, 'Super professionale.')
            ]

            cursor.executemany(
                """
                INSERT INTO reviews
                (rider_id, customer_name, rating, comment)
                VALUES (%s,%s,%s,%s)
                """,
                reviews_data
            )

            conn.commit()

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[DB] Errore durante l'inizializzazione: {e}")