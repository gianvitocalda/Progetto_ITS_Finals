from dotenv import load_dotenv
import os
load_dotenv()

from data.start_database import inizializza_database
from src.app import create_app

PORT = os.getenv("DB_PORT", "5000")

inizializza_database()

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)