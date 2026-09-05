# Local Flask Login System with OTP

A Python (Flask) web application demonstrating user authentication, session management, and a password reset flow using a local MySQL database. 

## Prerequisites
* Python 3.x
* MySQL Server (e.g., MySQL Workbench)

## Setup Instructions

1. **Configure the Database**
   Run the following SQL commands in your MySQL environment to set up the database and the `users` table:
   ```sql
   CREATE DATABASE mywebsite;
   USE mywebsite;

   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       password VARCHAR(50) NOT NULL,
       phone VARCHAR(15)
   );
## 2. Install Dependencies
Open your terminal and install the required Python libraries:

pip install flask mysql-connector-python

## 3.Update Database Credentials (Important)
Because this runs locally, you must update the connection script with your own system's MySQL password. Open app.py and modify the get_db_connection() function. Replace "password" with your actual local MySQL server password.


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="YOUR_ACTUAL_PASSWORD", # Change this to your local MySQL password!
        database="mywebsite"
    )
    
## 4.Run the Server
Start the application by running:


### Password Reset & OTP Configuration
By default, this project simulates SMS messages by printing the 6-digit OTP directly to your terminal. This avoids third-party costs while testing locally.

Optional: Send Real SMS Texts
If you want to send actual text messages to phones, you will need a third-party service like Twilio. Do not install the Twilio library unless you intend to set this up.

## 1.Create a free Twilio account and verify your phone number.

## 2.Install the Twilio Python package in your terminal:


pip install twilio

## 3.Open app.py and add this import at the very top:


from twilio.rest import Client

## 4.In the /forgot route, replace the simulated print() statements with this API call, substituting your Twilio credentials:

account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)

try:
    message = client.messages.create(
        body=f"Your website OTP is {session['otp']}",
        from_='YOUR_TWILIO_PHONE_NUMBER',
        to=f"+91{phone}" # Ensure correct country code
    )
except Exception as e:
    print(f"SMS Failed: {e}")

Bash
python app.py
Navigate to http://127.0.0.1:8000 in your web browser.