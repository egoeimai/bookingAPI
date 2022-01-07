import requests

reqUrl = "https://demoft.sednasystem.com/API/getaccess.asp?l=demoapifleet&p=demoapifleet&appname=apiboatcharter"

headersList = {
 "Accept": "*/*",
 "User-Agent": "opa36",
 "connection": "Keep-alive"
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
import xml.etree.ElementTree as ET
xml=ET.fromstring(response.text)

print(xml[0].attrib['authtoken'])

