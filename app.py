from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector
import random

app = Flask(__name__)
app.secret_key = "my_super_secret_key"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="password", 
        database="mywebsite"
    )

@app.route("/")
def home():
    if "username" in session:
        return f"<h1>Welcome, {session['username']}!</h1><a href='/logout'>Log out</a>"
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    user = request.form["username"]
    pwd = request.form["password"]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (user, pwd))
    account = cursor.fetchone()
    conn.close()
    
    if account:
        session["username"] = user
        return redirect(url_for("home"))
    return render_template("index.html", message="Invalid username or password.")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form["username"]
        phone = request.form["phone"]
        pwd = request.form["password"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (user,))
        if cursor.fetchone():
            return render_template("signup.html", message="Username already taken.")
            
        # Insert new user
        cursor.execute("INSERT INTO users (username, phone, password) VALUES (%s, %s, %s)", (user, phone, pwd))
        conn.commit()
        conn.close()
        
        return redirect(url_for("home"))
        
    return render_template("signup.html")

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        phone = request.form["phone"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE phone = %s", (phone,))
        account = cursor.fetchone()
        conn.close()
        
        if account:
            # Generate a 6-digit OTP
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            session['reset_phone'] = phone
            
            # SIMULATE SMS: Print directly to the VS Code terminal
            print(f"\n" + "="*40)
            print(f"📱 SMS SENT TO {phone}: Your OTP is {otp}")
            print("="*40 + "\n")
            
            return render_template("forgot.html", step=2)
        else:
            return render_template("forgot.html", step=1, message="Phone number not found.")
            
    return render_template("forgot.html", step=1)

@app.route("/reset", methods=["POST"])
def reset():
    entered_otp = request.form["otp"]
    new_pwd = request.form["new_password"]
    
    if "otp" in session and entered_otp == session["otp"]:
        phone = session["reset_phone"]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE phone = %s", (new_pwd, phone))
        conn.commit()
        conn.close()
        
        # Clear OTP from session
        session.pop("otp", None)
        session.pop("reset_phone", None)
        
        return redirect(url_for("home"))
    else:
        return render_template("forgot.html", step=2, message="Invalid OTP.")

if __name__ == "__main__":
    app.run(debug=True, port=8000)