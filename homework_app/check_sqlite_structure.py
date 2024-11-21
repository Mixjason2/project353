import sqlite3

# ระบุตำแหน่งไฟล์ฐานข้อมูล
db_path = 'your_database.db'

# เชื่อมต่อกับฐานข้อมูล SQLite
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# ดึงข้อมูลโครงสร้างของตาราง
cursor.execute("PRAGMA table_info(homework);")
columns = cursor.fetchall()

# แสดงชื่อคอลัมน์ของตาราง
if columns:
    print("Columns in 'homework' table:")
    for column in columns:
        print(f"Column: {column[1]} | Type: {column[2]}")
else:
    print("Table 'homework' not found or no columns available.")

# ปิดการเชื่อมต่อ
connection.close()