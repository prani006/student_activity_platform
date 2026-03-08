import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pranitha@30",
    database="student_platform"
)

cursor = conn.cursor()
print("===== ADMIN LOGIN =====")
username = input("Enter username: ")
password = input("Enter password: ")

cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
result = cursor.fetchone()

if result is None:
    print("❌ Invalid Login")
    exit()
else:
    print("✅ Login Successful")

while True:
    print("\n===== STUDENT ACTIVITY PLATFORM =====")
    print("1. View Students")
    print("2. Add Student")
    print("3. Assign Activity to Student")
    print("4. View Student Activities")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        cursor.execute("SELECT * FROM students")
        for row in cursor:
            print(row)

    elif choice == "2":
        name = input("Enter name: ")
        dept = input("Enter department: ")
        year = int(input("Enter year: "))
        email = input("Enter email: ")
        phone = input("Enter phone: ")

        query = "INSERT INTO students (name, department, year, email, phone) VALUES (%s,%s,%s,%s,%s)"
        values = (name, dept, year, email, phone)
        cursor.execute(query, values)
        conn.commit()
        print("✅ Student Added Successfully!")

    elif choice == "3":

        print("\nAvailable Students:")
        cursor.execute("SELECT student_id, name FROM students")
        for row in cursor:
            print(row)

        print("\nAvailable Activities:")
        cursor.execute("SELECT activity_id, activity_name FROM activities")
        for row in cursor:
            print(row)

        student_id = int(input("Enter student ID: "))
        activity_id = int(input("Enter activity ID: "))

        query = "INSERT INTO student_activities (student_id, activity_id) VALUES (%s,%s)"
        values = (student_id, activity_id)
        cursor.execute(query, values)
        conn.commit()

        print("✅ Activity Assigned Successfully!")

    elif choice == "4":
        query = """
        SELECT s.name, a.activity_name
        FROM students s
        JOIN student_activities sa ON s.student_id = sa.student_id
        JOIN activities a ON sa.activity_id = a.activity_id
        """
        cursor.execute(query)
        for row in cursor:
            print(row)

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid choice!")

conn.close()