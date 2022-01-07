
from flask import Flask, request, render_template


from datetime import datetime

from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route('/api/v1/analytics/pageview', methods=['GET'])
def view():
    import requests

    reqUrl = "https://demoft.sednasystem.com/API/getaccess.asp?l=demoapifleet&p=demoapifleet&appname=apiboatcharter"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "opa36",
        "connection": "Keep-alive"
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload, headers=headersList)
    import xml.etree.ElementTree as ET
    xml = ET.fromstring(response.text)

    print(xml[0].attrib['authtoken'])

    return xml[0].attrib['authtoken']


if __name__ == "__main__":
    app.run()
