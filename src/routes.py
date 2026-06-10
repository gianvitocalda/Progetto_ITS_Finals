from flask import Blueprint, request, jsonify

from src.handlers.rider_handler import (
    ottieni_tutti,
    elimina_rider,
    media_voti_rider
)

from src.handlers.review_handler import (
    crea_recensione,
    aggiorna_commento
)

deliver_bp = Blueprint("deliver", __name__, url_prefix="/deliver")


@deliver_bp.route("/riders", methods=["GET"])
def get_riders():
    try:
        vehicle = request.args.get("vehicle")
        riders = ottieni_tutti(vehicle)

        return jsonify(riders), 200

    except Exception as e:
        return jsonify({
            "errore": "Errore durante il recupero dei rider",
            "dettaglio": str(e)
        }), 500


@deliver_bp.route("/riders/<int:rider_id>", methods=["DELETE"])
def delete_rider(rider_id):
    try:
        eliminato = elimina_rider(rider_id)

        if not eliminato:
            return jsonify({
                "errore": f"Rider con id {rider_id} non trovato"
            }), 404

        return jsonify({
            "messaggio": f"Rider {rider_id} eliminato"
        }), 200

    except Exception as e:
        return jsonify({
            "errore": "Errore durante l'eliminazione del rider",
            "dettaglio": str(e)
        }), 500


@deliver_bp.route("/riders/<int:rider_id>/media", methods=["GET"])
def get_media(rider_id):
    try:
        risultato = media_voti_rider(rider_id)

        if risultato is None:
            return jsonify({
                "errore": f"Rider con id {rider_id} non trovato"
            }), 404

        return jsonify(risultato), 200

    except Exception as e:
        return jsonify({
            "errore": "Errore durante il calcolo della media voti",
            "dettaglio": str(e)
        }), 500


@deliver_bp.route("/reviews", methods=["POST"])
def add_review():
    try:
        dati = request.get_json()

        if dati is None:
            return jsonify({
                "errore": "Body JSON mancante"
            }), 400

        if "rider_id" not in dati:
            return jsonify({
                "errore": "Campo obbligatorio mancante: rider_id"
            }), 400

        if "customer_name" not in dati:
            return jsonify({
                "errore": "Campo obbligatorio mancante: customer_name"
            }), 400

        if "rating" not in dati:
            return jsonify({
                "errore": "Campo obbligatorio mancante: rating"
            }), 400

        rider_id = int(dati["rider_id"])
        rating = int(dati["rating"])

        if rating < 1 or rating > 5:
            return jsonify({
                "errore": "Il rating deve essere compreso tra 1 e 5"
            }), 400

        nuova = crea_recensione(
            rider_id,
            dati["customer_name"],
            rating,
            dati.get("comment")
        )

        if nuova is None:
            return jsonify({
                "errore": "Rider non trovato"
            }), 404

        return jsonify(nuova), 201

    except ValueError:
        return jsonify({
            "errore": "rider_id e rating devono essere numeri interi"
        }), 400

    except Exception as e:
        return jsonify({
            "errore": "Errore durante la creazione della recensione",
            "dettaglio": str(e)
        }), 500


@deliver_bp.route("/reviews/<int:review_id>", methods=["PUT"])
def patch_review(review_id):
    try:
        dati = request.get_json()

        if dati is None:
            return jsonify({
                "errore": "Body JSON mancante"
            }), 400

        if "comment" not in dati:
            return jsonify({
                "errore": "Campo obbligatorio mancante: comment"
            }), 400

        aggiornata = aggiorna_commento(
            review_id,
            dati["comment"]
        )

        if aggiornata is None:
            return jsonify({
                "errore": "Recensione non trovata"
            }), 404

        return jsonify(aggiornata), 200

    except Exception as e:
        return jsonify({
            "errore": "Errore durante l'aggiornamento della recensione",
            "dettaglio": str(e)
        }), 500