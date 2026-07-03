#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
# -*- coding: utf-8 -*-
print("Content-Type: text/html; charset=utf-8\n")

import cgi, os, pymysql
from datetime import datetime
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
username = form.getvalue("username")  # this should ideally come from session

# Fallback for testing
if not username:
    username = "seller1"

# Connect to DB
con = pymysql.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="studentdb"
        )
cur = con.cursor()

# Fetch seller details
cur.execute("SELECT username, email, dob, address, aadhar_file FROM ride_sharer WHERE username=%s AND role='ride_sharer'", (username,))
seller = cur.fetchone()

print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Seller Profile - DailyNuts</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #fdf6e3;
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            background: #fff8e1;
            margin: 50px auto;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h2 {
            text-align: center;
            color: #2e7d32;
        }
        .profile-item {
            margin: 15px 0;
            font-size: 18px;
        }
        .label {
            font-weight: bold;
            color: #558b2f;
        }
        a.button {
            display: block;
            text-align: center;
            margin-top: 30px;
            padding: 10px;
            background: #8bc34a;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }
        a.button:hover {
            background: #689f38;
        }
    </style>
</head>
<body>
""")

if seller:
    uname, email, dob, address, aadhar_file = seller
    print(f"""
    <div class="container">
        <h2>Seller Profile</h2>s
        <div class="profile-item"><span class="label">Username:</span> {uname}</div>
        <div class="profile-item"><span class="label">Email:</span> {email}</div>
        <div class="profile-item"><span class="label">Date of Birth:</span> {dob}</div>
        <div class="profile-item"><span class="label">Address:</span> {address}</div>
        <div class="profile-item"><span class="label">Aadhar Number:</span> {aadhar_file}</div>
        <a href="seller_dashboard.py" class="button">Back to Dashboard</a>
    </div>
    """)
else:
    print("<h3 style='color:red; text-align:center;'>Seller not found or invalid role.</h3>")

print("</body></html>")

con.close()
