import mysql.connector
import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sreeja@23",
    database="attendance_db"
)

cursor = conn.cursor()

def mark_attendance(user_id):
    now = datetime.datetime.now()
    date = now.date()
    time = now.strftime("%H:%M:%S")

    # Check duplicate
    cursor.execute("SELECT * FROM attendance WHERE id=%s AND date=%s", (user_id, date))
    result = cursor.fetchone()

    if result is None:
        cursor.execute("INSERT INTO attendance (id, date, time, status) VALUES (%s,%s,%s,%s)",
                       (user_id, date, time, "Present"))
        conn.commit()
        print(f"Attendance marked for ID {user_id}")
    else:
        print(f"Already marked for ID {user_id}")