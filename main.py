from dotenv import load_dotenv
load_dotenv()

from data.start_database import inizializza_database
from src.app import create_app

inizializza_database()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)