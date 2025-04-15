# generate_georss.py
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_georss():
    url = 'https://api.terrestra.tech/latest-truck-data'
    username = 'talabre'
    password = 'cosmos_talabre_2024'

    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        data = response.json()

        rss = ET.Element("rss", version="2.0", attrib={
            "xmlns:geo": "http://www.w3.org/2003/01/geo/wgs84_pos#"
        })
        channel = ET.SubElement(rss, "channel")
        ET.SubElement(channel, "title").text = "Últimos datos de camiones"
        ET.SubElement(channel, "link").text = url
        ET.SubElement(channel, "description").text = "Feed de ubicación de camiones actualizado"

        for item in data:
            entry = ET.SubElement(channel, "item")
            ET.SubElement(entry, "title").text = f"Camión {item.get('truckPatent', 'sin patente')}"
            ET.SubElement(entry, "geo:lat").text = str(item['lat'])
            ET.SubElement(entry, "geo:long").text = str(item['lon'])
            ET.SubElement(entry, "pubDate").text = item['currTime']

            # Agrega todos los campos como texto
            details = "\n".join([f"{k}: {v}" for k, v in item.items()])
            ET.SubElement(entry, "description").text = details

        # Guardar el archivo GeoRSS
        xml_str = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
        with open("latest_truck_data.xml", "w", encoding="utf-8") as f:
            f.write(xml_str)

        print("✅ GeoRSS actualizado")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
