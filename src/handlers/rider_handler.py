from data.start_database import get_connection
from src.utils import row_to_dict, rows_to_dict


def ottieni_tutti(vehicle=None):
    conn = get_connection()
    cursor = conn.cursor()

    if vehicle:
        cursor.execute(
            "SELECT * FROM riders WHERE vehicle = %s",
            (vehicle,)
        )
    else:
        cursor.execute("SELECT * FROM riders")

    colonne = [desc[0] for desc in cursor.description]
    riders = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows_to_dict(colonne, riders)


def elimina_rider(rider_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reviews WHERE rider_id = %s",
        (rider_id,)
    )

    cursor.execute(
        "DELETE FROM riders WHERE id = %s",
        (rider_id,)
    )

    eliminato = cursor.rowcount > 0

    conn.commit()
    cursor.close()
    conn.close()

    return eliminato


def media_voti_rider(rider_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM riders WHERE id = %s",
        (rider_id,)
    )

    rider = cursor.fetchone()

    if rider is None:
        cursor.close()
        conn.close()
        return None

    cursor.execute(
        "SELECT AVG(rating) AS media FROM reviews WHERE rider_id = %s",
        (rider_id,)
    )

    risultato = cursor.fetchone()

    cursor.close()
    conn.close()

    media = risultato[0]

    if media is None:
        return {
            "rider_id": rider_id,
            "media_voti": None,
            "messaggio": "Nessuna recensione trovata"
        }

    return {
        "rider_id": rider_id,
        "media_voti": round(float(media), 2)
    }