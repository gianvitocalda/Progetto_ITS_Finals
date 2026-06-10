from data.start_database import get_connection
from src.utils import row_to_dict


def crea_recensione(rider_id, customer_name, rating, comment=None):
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
        """
        INSERT INTO reviews (rider_id, customer_name, rating, comment)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (rider_id, customer_name, rating, comment)
    )

    nuova_id = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE riders SET total_deliveries = total_deliveries + 1 WHERE id = %s",
        (rider_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "id": nuova_id,
        "rider_id": rider_id,
        "customer_name": customer_name,
        "rating": rating,
        "comment": comment
    }


def aggiorna_commento(review_id, comment):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM reviews WHERE id = %s",
        (review_id,)
    )

    recensione = cursor.fetchone()

    if recensione is None:
        cursor.close()
        conn.close()
        return None

    cursor.execute(
        "UPDATE reviews SET comment = %s WHERE id = %s",
        (comment, review_id)
    )

    conn.commit()

    cursor.execute(
        "SELECT * FROM reviews WHERE id = %s",
        (review_id,)
    )

    colonne = [desc[0] for desc in cursor.description]
    aggiornata = cursor.fetchone()

    cursor.close()
    conn.close()

    return row_to_dict(colonne, aggiornata)