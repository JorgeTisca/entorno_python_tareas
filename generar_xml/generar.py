import base64
import urllib

import requests
from Crypto.Cipher import AES


class AESCipher:
    def __init__(self, key):
        """Convierte la clave de hexadecimal a bytes"""
        self.key = bytes.fromhex(key)

    def encrypt(self, raw):
        """Cifra el texto usando AES en modo ECB"""
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(raw.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")

    def _pad(self, s):
        """Añade padding para que el texto sea múltiplo de 16 bytes"""
        pad_len = 16 - (len(s) % 16)
        return s + chr(pad_len) * pad_len


# Paso 1: Cadena XML
originalString = """<?xml version="1.0" encoding="UTF-8"?>
<P>
  <business>
    <id_company>SNBX</id_company>
    <id_branch>01SNBXBRNCH</id_branch>
    <user>SNBXUSR0456</user>
    <pwd>CLAVESEGURA</pwd>
  </business>
  <url>
    <reference>FACTURA123</reference>
    <amount>1500.75</amount>
    <moneda>USD</moneda>
    <canal>O</canal>
    <omitir_notif_default>0</omitir_notif_default>
    <promociones>A,6,12</promociones>
    <id_promotion>SNBX98765432</id_promotion>
    <fh_vigencia>30/12/2028</fh_vigencia>
    <mail_cliente>cliente@ejemplo.com</mail_cliente>
    <nb_fpago>TRANSFER</nb_fpago>
    <cardblock>N</cardblock>
    <dom>0</dom>
    <datos_adicionales>
      <data id="1" display="true">
        <label>Modelo</label>
        <value>ZX-300</value>
      </data>
      <data id="2" display="true">
        <label>Garantía</label>
        <value>2 años</value>
      </data>
    </datos_adicionales>
    <version>IntegraWPPv2</version>
  </url>
</P>"""

key = "5dcc67393750523cd165f17e1efadd21"

# Paso 2: Cifrando la cadena
cipher = AESCipher(key)
xmlcifrado = cipher.encrypt(originalString)

print("Texto Cifrado:")
print(xmlcifrado)
# Paso 3: Servicio de Generación
url = "https://sandboxpo.mit.com.mx/gen"
encodedString = urllib.parse.quote(
    f"<pgs><data0>SNDBX123</data0><data>{xmlcifrado}Cifrada</data></pgs>", "UTF-8"
)
payload = "xml=" + encodedString
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
