from datetime import datetime, timedelta
from flask import Flask, render_template_string
import requests, os
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Zugangsdaten und URL-Template (am besten später über Umgebungsvariablen steuern)
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
URL_TEMPLATE = os.environ.get("URL_TEMPLATE")

print(URL_TEMPLATE)

def fetch_timetable(kw):
    url = URL_TEMPLATE.format(kw=kw) 
    try:
        response = requests.get(
            url, auth=HTTPBasicAuth(USERNAME, PASSWORD), timeout=10
        )
        if response.status_code == 200:
            # Erzwingt die automatische Erkennung der korrekten Zeichenkodierung (z.B. ISO-8859-1)
            response.encoding = response.apparent_encoding
            return response.text
        else:
            return f"<p style='color: red;'>Fehler beim Laden: HTTP Statuscode {response.status_code}</p>"
    except Exception as e:
        return f"<p style='color: red;'>Verbindungsfehler: {e}</p>"


@app.route("/")
def index():
  now = datetime.now()
  kw = now.isocalendar()[1]
  kw_str = f"{kw:02d}"  # Zweistellig formatiert (z.B. "09")
  content = fetch_timetable(kw_str)

  html = f"""
    <!doctype html>
    <html lang="de">
    <head>
        <meta charset="utf-8">
        <title>Stundenplan - Aktuelle KW {kw_str}</title>
    </head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h2>Aktuelle Kalenderwoche ({kw_str})</h2>
        <div style="margin-top: 20px;">
            {content}
        </div>
        <div style="margin-bottom: 20px;">
            <a href="/next"><button style="padding: 10px 20px; font-size: 12pt; cursor: pointer;">Zur nächsten Woche</button></a>
        </div>
    </body>
    </html>
    """
  return html


@app.route("/next")
def next_week():
  next_date = datetime.now() + timedelta(days=7)
  kw = next_date.isocalendar()[1]
  kw_str = f"{kw:02d}"
  content = fetch_timetable(kw_str)

  html = f"""
    <!doctype html>
    <html lang="de">
    <head>
        <meta charset="utf-8">
        <title>Stundenplan - Nächste KW {kw_str}</title>
    </head>
    <body style="font-family: sans-serif; padding: 20px;">
        <h2>Nächste Kalenderwoche ({kw_str})</h2>
        <div style="margin-top: 20px;">
            {content}
        </div>
        <div style="margin-bottom: 20px;">
            <a href="/"><button style="padding: 10px 20px; font-size: 12pt; cursor: pointer;">Aktuelle Woche</button></a>
        </div>
    </body>
    </html>
    """
  return html


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
