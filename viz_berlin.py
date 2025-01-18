import requests
import xml.etree.ElementTree as ET
from owslib.wms import WebMapService


url = "https://api.viz.berlin.de/geoserver/mdhwfs/wfs?REQUEST=GetFeature&SERVICE=WFS&SRSNAME=EPSG%3A25833&VERSION=1.1.0&typename=baustellen_sperrungen"
wms = WebMapService(url)
print(list(wms.contents))


# response = requests.get(url)
# # data = BeautifulSoup(response.text, features="xml")
# if response.status_code == 200:
#     xml_data = response.content
#     root = ET.fromstring(xml_data)
#     print(root)
