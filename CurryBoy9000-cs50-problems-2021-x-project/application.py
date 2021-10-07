from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///mxwebsite.db")

@app.route("/")
@login_required
def index():
        return render_template("index.html")

StuGender = ''
StuGrade = ''
StuType = ''
StuSelection = ''
StuGroup = ''

@app.route("/stuinfo", methods=["GET", "POST"])
@login_required
def stuinfo():
    LQS = "SELECT * FROM student_information"
    eq = LQS.count("=")
    if request.method == "GET":
        rows = db.execute("SELECT * FROM student_information")
        return render_template("stuinfo.html", rows=rows)
        
    else:
        if request.values.get('Gender'):
            global StuGender
            StuGender = request.values.get('Gender')
            LQS = LQS + " WHERE Gender = '" + StuGender + "'"
            eq = LQS.count("=")
            
        if request.values.get('Grade'):
            global StuGrade 
            StuGrade = request.values.get('Grade')
            if eq == 0:
                LQS = LQS + " WHERE Grade = '" + StuGrade + "'"
                eq = LQS.count("=")
            else:
                LQS = LQS + " AND Grade = '" + StuGrade + "'"
                eq = LQS.count("=")
    
        if request.values.get('Student_Type'):
            global StuType 
            StuType = request.values.get('Student_Type')
            if eq == 0:
                LQS = LQS + " WHERE Student_Type = '" + StuType + "'"
                eq = LQS.count("=")
            else:
                LQS = LQS + " AND Student_Type = '" + StuType + "'"
                eq = LQS.count("=")
                
        if request.values.get('Student_Selection'):
            global StuSelection 
            StuSelection = request.values.get('Student_Selection')
            if eq == 0:
                LQS = LQS + " WHERE Student_Selection = '" + StuSelection + "'"
                eq = LQS.count("=")
            else:
                LQS = LQS + " AND Student_Selection = '" + StuSelection + "'"
                eq = LQS.count("=")
        
        if request.values.get('Student_Group'):
            global StuGroup
            StuGroup = request.values.get('Student_Group')
            if eq == 0:
                LQS = LQS + " WHERE Student_Group = '" + StuGroup + "'"
                eq = LQS.count("=")
            else:
                LQS = LQS + " AND Student_Group = '" + StuGroup + "'"
                eq = LQS.count("=")
        
        rows = db.execute(LQS)
        
        return render_template("stuinfo.html", rows=rows)
        
def clearStuInfo():
    rows = db.execute("SELECT * FROM student_information")
    return render_template("stuinfo.html", rows=rows)
    
@app.route("/facinfo", methods=["GET", "POST"])
@login_required
def facinfo():
    LQS = "SELECT * FROM faculty_information"
    eq = LQS.count("=")
    if request.method == "GET":
        rows = db.execute("SELECT * FROM faculty_information")
        return render_template("facinfo.html", rows=rows)
        
    else:
        if request.values.get('Gender'):
            global FacGender
            FacGender = request.values.get('Gender')
            LQS = LQS + " WHERE Gender = '" + FacGender + "'"
            eq = LQS.count("=")
            

        if request.values.get('Department'):
            global FacDepartment 
            FacDepartment = request.values.get('Department')
            if eq == 0:
                LQS = LQS + " WHERE Department = '" + FacDepartment + "'"
                eq = LQS.count("=")
            else:
                LQS = LQS + " AND Department = '" + FacDepartment + "'"
                eq = LQS.count("=")
    
        rows = db.execute(LQS)

        return render_template("facinfo.html", rows=rows)

def clearFacInfo():
    rows = db.execute("SELECT * FROM faculty_information")
    return render_template("facinfo.html", rows=rows)

@app.route("/stuCOVIDinfo/<Student_ID>")
@login_required
def stuCOVIDinfo(Student_ID):
    if request.method == "GET":
        QLS = "SELECT StuID, First_Name, Last_Name FROM student_information WHERE StuID = " + str(Student_ID)
        rows = db.execute(QLS)
        return render_template("stuCOVIDinfo.html", rows=rows)
    
@app.route("/submitStuCOVIDinfo")
@login_required
def submitStuCOVIDinfo():
    if request.method == "GET":
        Student_ID = request.args.get('StuID')
        StuTest = request.args.get('Test')
        StuDate = request.args.get('Date_of_Test')
        StuResult = request.args.get('Test_Result')
        StuQ = request.args.get('Quarantine')
        StuQSD = request.args.get('Quarantine_Start_Date')
        StuQED = request.args.get('Quarantine_End_Date')
        StuPN = request.args.get('Parents_Notified')
    
        QSL = db.execute("SELECT StuID FROM student_COVID_information WHERE StuID = " + str(Student_ID))
        if QSL:
            QLS = "UPDATE student_COVID_information SET StuID = " + str(Student_ID) + ", Test = '" + str(StuTest) + "', Date_of_Test = '" + str(StuDate) + "', Test_Result = '" + str(StuResult) + "', Quarantine = '" + str(StuQ) + "', Quarantine_Start_Date = '" + str(StuQSD) + "', Quarantine_End_Date = '" + str(StuQED) + "', Parents_Notified = '" + str(StuPN) + "'"
            rows = db.execute(QLS)
            swors = db.execute("SELECT * FROM student_COVID_information WHERE StuID = " + str(Student_ID))
            return render_template("saveStuCOVIDinfo.html", swors=swors)
        else:
            QLS = "INSERT INTO student_COVID_information (StuID, Test, Date_of_Test, Test_Result, Quarantine, Quarantine_Start_Date, Quarantine_End_Date, Parents_Notified) VALUES (" + str(Student_ID) + ", '" + str(StuTest) + "', '" + str(StuDate) + "', '" + str(StuResult) + "', '" + str(StuQ) + "', '" + str(StuQSD) + "', '" + str(StuQED) + "', '" + str(StuPN) + "')"
            rows = db.execute(QLS)
            swors = db.execute("SELECT * FROM student_COVID_information WHERE StuID = " + str(Student_ID)) 
            return render_template("saveStuCOVIDinfo.html", swors=swors)

@app.route("/facCOVIDinfo/<Faculty_ID>")
@login_required
def facCOVIDinfo(Faculty_ID):
    QLS = "SELECT FacID, First_Name, Last_Name FROM faculty_information WHERE FacID = " + str(Faculty_ID)
    rows = db.execute(QLS)
    return render_template("facCOVIDinfo.html", rows=rows)

@app.route("/submitFacCOVIDinfo")
@login_required
def submitFacCOVIDinfo():
    if request.method == "GET":
        Faculty_ID = request.args.get('FacID')
        FacTest = request.args.get('Test')
        FacDate = request.args.get('Date_of_Test')
        FacResult = request.args.get('Test_Result')
        FacQ = request.args.get('Quarantine')
        FacQSD = request.args.get('Quarantine_Start_Date')
        FacQED = request.args.get('Quarantine_End_Date')
        
        QSL = db.execute("SELECT FacID FROM faculty_COVID_information WHERE FacID = " + str(Faculty_ID))
        if QSL:
            QLS = "UPDATE faculty_COVID_information SET FacID = " + str(Faculty_ID) + ", Test = '" + str(FacTest) + "', Date_of_Test = '" + str(FacDate) + "', Test_Result = '" + str(FacResult) + "', Quarantine = '" + str(FacQ) + "', Quarantine_Start_Date = '" + str(FacQSD) + "', Quarantine_End_Date = '" + str(FacQED) + "'"
            rows = db.execute(QLS)
            swors = db.execute("SELECT * FROM faculty_COVID_information WHERE FacID = " + str(Faculty_ID))
            return render_template("saveFacCOVIDinfo.html", swors=swors)
        else:
            QLS = "INSERT INTO faculty_COVID_information (FacID, Test, Date_of_Test, Test_Result, Quarantine, Quarantine_Start_Date, Quarantine_End_Date) VALUES (" + str(Faculty_ID) + ", '" + str(FacTest) + "', '" + str(FacDate) + "', '" + str(FacResult) + "', '" + str(FacQ) + "', '" + str(FacQSD) + "', '" + str(FacQED) + "')"
            rows = db.execute(QLS)
            swors = db.execute("SELECT * FROM faculty_COVID_information WHERE FacID = " + str(Faculty_ID)) 
            return render_template("saveFacCOVIDinfo.html", swors=swors)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]


        # Redirect user to home page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        # hash the password and insert a new user in the database
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                 username=request.form.get("username"),
                                 hash=hash)
        # unique username constraint violated?
        if not new_user_id:
            return apology("username taken", 400)

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Display a flash message
        flash("Registered!")

        # Redirect user to home page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        