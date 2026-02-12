from flask import Flask, request, render_template_string
import sqlite3
import os
import requests
from lxml import etree
import threading

app = Flask(__name__)

# ---- SQLi ----
@app.route("/login")
def login():
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = '" + user + "'"
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(query)
    return "Logged in"

# ---- XSS ----
@app.route("/xss")
def xss():
    name = request.args.get("name")
    return "<h1>Hello " + name + "</h1>"

# ---- RCE ----
@app.route("/rce")
def rce():
    cmd = request.args.get("cmd")
    return os.popen(cmd).read()

# ---- SSRF ----
@app.route("/ssrf")
def ssrf():
    url = request.args.get("url")
    return requests.get(url).text

# ---- SSTI ----
@app.route("/ssti")
def ssti():
    template = request.args.get("tpl")
    return render_template_string(template)

# ---- XXE ----
@app.route("/xxe", methods=["POST"])
def xxe():
    xml = request.data
    parser = etree.XMLParser(resolve_entities=True)
    root = etree.fromstring(xml, parser)
    return str(root.text)

# ---- Race Condition ----
balance = 1000
lock = threading.Lock()

@app.route("/withdraw")
def withdraw():
    global balance
    amount = int(request.args.get("amount"))
    if balance >= amount:
        balance -= amount
    return str(balance)

# ---- Access Control ----
@app.route("/admin")
def admin():
    return "Admin panel"

# ---- CORS Misconfig ----
@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

app.run(host="0.0.0.0", port=5000)


Flag = CTF{hEllO_WorLD}
