# Importiamo la funzione dal file start_database dentro la cartella data
from data.start_database import inizializza_database

if __name__ == "__main__":
    # Avvia il controllo e il popolamento del DB all'accensione del programma
    inizializza_database()
    
    # Da qui sotto parte la logica del tuo main pulito
    print("\n--- Il programma principale è avviato correttamente! ---")