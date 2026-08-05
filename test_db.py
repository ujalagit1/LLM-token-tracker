from database import connection

if connection.is_connected():
    print("Connected to MySQL Successfully!")
else:
    print("Connection Failed")