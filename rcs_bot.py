import os
import re
from pathlib import Path
from loguru import logger
from playwright.sync_api import Page, Playwright
from models import MensajeRCS, MensajeRCS_v2
from dotenv import load_dotenv
import json

load_dotenv()


def upload_images(page: Page):
    """
    Sube imágenes de la carpeta "data" a la página especificada.

    Parameters:
    - page: objeto Page de pytest-play para la página donde se subirán las imágenes.
    """
    # Obtener todos los archivos en la carpeta "data".
    files = Path(__file__).parent.glob("data/*")
    # Crear un patrón para filtrar solo los archivos de imagen.
    pattern = r".*\.(jpg|gif|png)$"
    files_to_upload = []
    # Acceder a la página de subida de archivos.
    page.get_by_role("list").get_by_role("link", name="Multimedia para RCS").click()
    # Filtrar solo los archivos de imagen usando patron regex.
    files_to_upload = [f for f in files if re.match(pattern, f.name)]
    # Subir cada archivo de imagen.
    for file in files_to_upload:
        page.get_by_role("link", name="Upload file").click()
        page.get_by_role("textbox").set_input_files(file)
        page.get_by_role("button", name="Upload").click()
        logger.info(f"{file.name} Uploaded")


def login(playwright: Playwright, headless=False):
    """
    Inicia sesión en una página web.

    Parameters:
    - playwright: objeto Playwright con la librería de automatización de navegadores.
    - headless: si se debe ejecutar el navegador en modo headless (opcional, default es False).

    Returns:
    - Objeto Page con la página web tras iniciar sesión.
    - Objeto Browser con el navegador utilizado para iniciar sesión.
    - Objeto Context con el contexto de la página web tras iniciar sesión.
    """
    # Abrir el navegador y crear un nuevo contexto.
    browser = playwright.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    # Abrir la página de inicio de sesión.
    page.goto(os.environ.get("SECAM_URL"))
    # Ingresar credenciales de inicio de sesión.
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill(os.environ.get("SECAM_USER"))
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(os.environ.get("SECAM_PASSWORD"))
    # Hacer clic en el botón "Log In".
    page.get_by_role("button", name="Log In").click()
    return page, browser, context


def create_rcs_campaign(page: Page, msg_list: list[MensajeRCS_v2]):
    """
    Crea una o más campañas RCS en una página web.

    Parameters:
    - page: objeto Page con la página web donde se crearán las campañas.
    - msg_list: lista de objetos MensajeRCS con la información de cada campaña a crear.
    """

    # Acceder a la página de creación de campañas RCS.
    page.get_by_role("list").get_by_role("link", name="Mensajes RCS").click()
    # Crear una campaña RCS por cada objeto MensajeRCS en la lista.
    for msg in msg_list:
        # Acceder a la página de creación de una campaña RCS.
        page.get_by_role("link", name="New").click()
        # Ingresar información de la campaña RCS.
        page.get_by_label("ID [KEY]:").click()
        page.get_by_label("ID [KEY]:").fill(msg.id)
        page.locator("#DTE_Field_data-title").click()
        page.locator("#DTE_Field_data-title").fill(msg.name)
        page.locator("#DTE_Field_data-json").click()
        page.locator("#DTE_Field_data-json").fill(json.dumps(msg.rcs_msg.get_agent_message(), indent=4))
        page.locator("#DTE_Field_data-msg").click()
        page.locator("#DTE_Field_data-msg").fill(msg.fallback_msg)
        # Hacer clic en el botón "Create" para crear la campaña.
        page.get_by_role("button", name="Create").click()
        # Para testing comentar la linea anterior y utilizar la siguiente linea para que cierre la ventana en vez de crear una campaña RCS.
        # page.get_by_role("button", name="×").click()
        logger.info(f"RCS Campaign Created id={msg.id},name={msg.name}.")
