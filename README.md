# RCSManager

Script para ingreso de campañas RCS

Se debe crear un archivo .env con el siguiente contenido reemplazando donde corresponda

```text
SERVER1=<ip_rcs1>
SERVER2=<ip_rcs2>
SERVER3=<ip_rcs3>
SERVER4=<ip_rcs4>
SERVER5=<ip_rcs5>
SERVER6=<ip_rcs6>
PASSWORD=<password>
PASSWORD_2=<password_2>
ACCOUNT_ID=<account_id>
ACCOUNT_KEY=<account_key>
SEND_RCS_URL=<send_rcs_url>
SECAM_URL=<secam_url>
SECAM_USER=<secam_user>
SECAM_PASSWORD=<secam_password>
```

Instalación dependencias:

```bash
cd RCSManager
mkdir data
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
playwright install-deps
playwright install
```

Ejecución:

La presentación (.pptx) debe tener el siguiente [formato](https://docs.google.com/presentation/d/1dkA8mPbiWVA_Ks54sS4PcYQex7aj_CM4/edit#slide=id.p1) y se debe cargar en la carpeta /data al igual que las imagenes (jpg, gif y png), también se puede ingresar el archivo .zip.

```python
python main.py
```

Al ejecutar solicita ingresar las campaign_id de cada mensaje RCS

1. extrae info de campaña desde archivo pptx
2. genera JSON
3. crea campaña en SECAM
4. sube las imagenes a SECAM
5. envia mensaje RCS para  pruebas
6. extrae las URL de RCS WEB
7. muestra texto para ingreso a plantilla
