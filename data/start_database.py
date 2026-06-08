import os
import psycopg2
from dotenv import load_dotenv

# Carica le variabili dal file .env
load_dotenv()

def inizializza_database():
    try:
        # Recupera le credenziali mascherate dal file .env
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()
        
        print("[DB] Connessione riuscita. Verifica struttura in corso...")

        # 1. Crea la tabella riders se non esiste
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS riders (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                vehicle VARCHAR NOT NULL,
                total_deliveries INT DEFAULT 0
            );
        """)

        # 2. Crea la tabella reviews se non esiste
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                rider_id INT NOT NULL,
                customer_name VARCHAR NOT NULL,
                rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment VARCHAR,
                CONSTRAINT fk_rider FOREIGN KEY (rider_id) REFERENCES riders(id) ON DELETE CASCADE
            );
        """)
        conn.commit()

        # 3. Controllo duplicati: Popola solo se la tabella riders è totalmente vuota
        cursor.execute("SELECT COUNT(*) FROM riders;")
        if cursor.fetchone()[0] == 0:
            print("[DB] Tabelle vuote. Inserimento di 5 record demo...")
            
            # 5 Record per i Riders
            riders_data = [
                ('Marco Rossi', 'Bicicletta', 120),
                ('Annamaria Bianchi', 'Scooter', 340),
                ('Luca Verdi', 'Auto', 85),
                ('Giulia Neri', 'Monopattino', 42),
                ('Alessandro Gallo', 'Scooter', 510)
            ]
            cursor.executemany(
                "INSERT INTO riders (name, vehicle, total_deliveries) VALUES (%s, %s, %s);", 
                riders_data
            )

            # 5 Record per le Reviews (collegate ai rider con id da 1 a 5)
            reviews_data = [
                (1, 'Giovanni S.', 5, 'Consegna velocissima e cibo caldissimo!'),
                (2, 'Elena M.', 4, 'Molto gentile, ha avuto solo un attimo di ritardo per il traffico.'),
                (3, 'Roberto F.', 5, 'Tutto perfetto, consigliato.'),
                (1, 'Alice V.', 2, 'Il pacco era un po schiacciato, ma il rider è stato comunque educato.'),
                (5, 'Stefano B.', 5, 'Super professionale, conosce tutte le scorciatoie della città!')
            ]
            cursor.executemany(
                "INSERT INTO reviews (rider_id, customer_name, rating, comment) VALUES (%s, %s, %s, %s);", 
                reviews_data
            )
            
            conn.commit()
            print("[DB] Popolamento completato con successo (5 record inseriti).")
        else:
            print("[DB] Il database contiene già i dati. Nessuna modifica effettuata.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[DB] Errore durante l'inizializzazione: {e}")