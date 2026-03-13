from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ---------------- MYSQL CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pranitha@30",
    database="student_platform"
)

cursor = db.cursor()

# ---------------- LOGIN PAGE ----------------
@app.route('/')
def home():
    return render_template("login.html")


# ---------------- LOGIN CHECK ----------------
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    query = "SELECT * FROM admin WHERE username=%s AND password=%s"
    cursor.execute(query,(username,password))

    result = cursor.fetchone()

    if result:
        return redirect(url_for('dashboard'))
    else:
        return "Invalid Login"


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# ---------------- ADD STUDENT ----------------
@app.route('/add_student', methods=['GET','POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        email = request.form['email']
        phone = request.form['phone']

        query = """
        INSERT INTO students(name,department,year,email,phone)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(query,(name,department,year,email,phone))
        db.commit()

        return redirect(url_for('view_students'))

    return render_template("add_student.html")


# ---------------- VIEW STUDENTS ----------------
@app.route('/view_students')
def view_students():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template("view_students.html", students=students)


# ---------------- UPLOAD ACTIVITY ----------------
@app.route('/upload_activity', methods=['GET','POST'])
def upload_activity():

    if request.method == 'POST':

        student_id = request.form['student_id']
        activity_name = request.form['activity_name']
        activity_date = request.form['activity_date']

        query = """
        INSERT INTO activities(student_id,activity_name,date)
        VALUES(%s,%s,%s)
        """

        cursor.execute(query,(student_id,activity_name,activity_date))
        db.commit()

        return redirect(url_for('view_activities'))

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template("upload_activity.html", students=students)


# ---------------- VIEW ACTIVITIES ----------------
@app.route('/view_activities')
def view_activities():

    query = """
    SELECT activities.activity_id,
           students.name,
           activities.activity_name,
           activities.date
    FROM activities
    JOIN students
    ON activities.student_id = students.student_id
    """

    cursor.execute(query)
    activities = cursor.fetchall()

    return render_template("view_activities.html", activities=activities)


# ---------------- ADD ATTENDANCE ----------------
@app.route('/add_attendance', methods=['GET','POST'])
def add_attendance():

    if request.method == 'POST':

        student_id = request.form['student_id']
        date = request.form['date']
        status = request.form['status']

        query = """
        INSERT INTO attendance(student_id,date,status)
        VALUES(%s,%s,%s)
        """

        cursor.execute(query,(student_id,date,status))
        db.commit()

        return redirect(url_for('view_attendance'))

    cursor.execute("SELECT student_id,name FROM students")
    students = cursor.fetchall()

    return render_template("add_attendance.html", students=students)


# ---------------- VIEW ATTENDANCE ----------------
@app.route('/view_attendance')
def view_attendance():

    query = """
    SELECT attendance.id,
           students.name,
           attendance.date,
           attendance.status
    FROM attendance
    JOIN students
    ON attendance.student_id = students.student_id
    """

    cursor.execute(query)
    attendance = cursor.fetchall()

    return render_template("view_attendance.html", attendance=attendance)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    return redirect(url_for('home'))


# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)