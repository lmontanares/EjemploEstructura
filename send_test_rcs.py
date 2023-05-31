import os
import requests
from loguru import logger
from dotenv import load_dotenv

load_dotenv()
campañas = []


msisdns: list[str] = ["52000000001"]


def send_rcs_message(id: str, msisdn: str = "52000000001"):
    """
    Envía un mensaje RCS a un número de teléfono específico.

    Parameters:
    - id: id del mensaje RCS a enviar
    - msisdn: número de teléfono al que se enviará el mensaje (opcional, default es 52000000001)

    Returns:
    - Resultado de la solicitud de envío de mensaje RCS.
    """
    logger.info(f"Sending {id} to {msisdn}.")
    r = requests.post(
        url=os.environ.get("SEND_RCS_URL"),
        json={
            "account_id": os.environ.get("ACCOUNT_ID"),
            "account_key": os.environ.get("ACCOUNT_KEY"),
            "msisdn": msisdn,
            "transaction_id": "prueba_cliente",
            "rcs_message_id": id,
            "campaign_id": "prueba_cliente",
            "eta": "now",
            "validity": "720",
            "priority": "0",
            "ticket_id": "666",
            "ctx": {},
        },
    )
    print(r.status_code, r.reason)
    print(r.text)


if __name__ == "__main__":
    for campaña in campañas:
        for msisdn in msisdns:
            send_rcs_message(campaña, msisdn)
            print(input("Press Enter to continue..."))
