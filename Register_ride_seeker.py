#!C:/Users/User/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\n")
import cgi, os, pymysql
from datetime import datetime
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
username = form.getvalue("username")
email = form.getvalue("email")
password = form.getvalue("password")
gender = form.getvalue("gender")
phone_no = form.getvalue("phone_no")
dob = form.getvalue("dob")
address = form.getvalue("address")
role = form.getvalue("role")
aadhar_file = form['aadhar'] if 'aadhar' in form else None

upload_path = "uploads"
saved_file_name = ""

if username and email and password and gender and phone_no and dob and address and role and aadhar_file.filename:
    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        saved_file_name = os.path.basename(aadhar_file.filename)
        file_path = os.path.join(upload_path, saved_file_name)

        with open(file_path, "wb") as f:
            f.write(aadhar_file.file.read())

        con = pymysql.connect(
            host="localhost",
            port=3307,
            user="root",
            password="",
            database="studentdb"
        )
        cur = con.cursor()

        cur.execute("INSERT INTO ride_seeker (username, email, password, gender, phone_no, dob, address, role, aadhar_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (username, email, password, gender, phone_no, dob, address, role, saved_file_name))
        con.commit()
        con.close()

        print("""
        <script>
        alert("Registration Successful!");
        window.location.href = 'ride-seeker.html';
        </script>
        """)


    except Exception as e:
        print(f"<script>alert('Error: {str(e)}');</script>")

# HTML Page (registration form with styling)
print(f"""
<!DOCTYPE html>
<html>
<head>
  <title>Register - RideSeeker</title>
  <style>
    body {{
      background: #fff8e1;
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
    }}
    .register-container {{
      width: 400px;
      margin: 80px auto;
      padding: 30px;
      background-color: #e9f5e9;
      border-radius: 15px;
      box-shadow: 0 0 15px rgba(0,0,0,0.2);
    }}
    h2 {{
      text-align: center;
      color: #2e7d32;
    }}
    input[type="text"], input[type="email"], input[type="password"], input[type="date"], textarea, select {{
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 8px;
    }}
    input[type="file"] {{
      margin: 10px 0;
    }}
    input[type="submit"] {{
      width: 100%;
      background-color: #2e7d32;
      color: white;
      border: none;
      padding: 12px;
      border-radius: 8px;
      font-size: 16px;
      cursor: pointer;
    }}
    input[type="submit"]:hover {{
      background-color: #1b5e20;
    }}
  </style>
</head>
<body>
  <div class="register-container">
    <h2>Register - RideSeeker</h2>
    <form method="post" enctype="multipart/form-data" action="register_seeker.py">
      <label>Username:</label>
      <input type="text" name="username" required>

      <label>Email:</label>
      <input type="email" name="email" required>

      <label>Password:</label>
      <input type="password" name="password" required>
      
      <label>Gender:</label>
      <select name="gender" required>
        <option value="">Select</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
      </select>

      <label>Phone Number:</label>
      <input type="text" name="phone_no" required>

      <label>Date of Birth:</label>
      <input type="date" name="dob" required>

      <label>Address:</label>
      <textarea name="address" rows="3" required></textarea>

      <label>Role:</label>
      <select name="role" required>
        <option value="">Select Role</option>
        <option value="RideSeeker">RideSeeker</option>
      </select>

      <label>Aadhar Card (file upload):</label>
      <input type="file" name="aadhar" required>

      <input type="submit" value="Register">
    </form>
  </div>
</body>
</html>
""")
