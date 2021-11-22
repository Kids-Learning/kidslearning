from re import A, template
from flask import Flask, render_template, request,jsonify
from flask.globals import session
from DBConnection import Db
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #session key
static_path = "C:\\Users\\user\\Desktop\\project\\Kids Learning\\static\\"
# session["log_id"]="0"


@app.route('/')
def hello_world():
    session["log_id"]="0"
    return render_template("Login.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('Login.html'), 404



@app.route('/resetpassword')
def resetpassword():
    return render_template("reset-password.html")

@app.route('/resetpassword_post', methods=['post'])
def resetpassword_post():
    db= Db()
    email=request.form['email']
    qry="SELECT * FROM login WHERE username='"+email+"'" 
    res=db.selectOne(qry)
    if res is not None:
        type = res["type"]
        log_id=str(res["log_id"])
        password=res["password"]
        if (type == "admin"):
            name="admin"
        elif type == "parent":
            qry1="SELECT * FROM parents WHERE log_id='"+log_id+"'"
            res1=db.selectOne(qry1)
            name=res1["name"]
        elif type == "teacher":
            qry2="SELECT * FROM teachers WHERE log_id='"+log_id+"'"
            res2=db.selectOne(qry2)
            name=res2["name"]
        else:
            name=""
        if name !="":
            s = smtplib.SMTP(host='smtp.gmail.com', port=587)
            s.starttls()
            s.login("malabrkidslearning@gmail.com", "kids@malabar")
            msg = MIMEMultipart()  # create a message.........."
            message = "Messege from DNTL"
            msg['From'] = "malabrkidslearning@gmail.com"
            msg['To'] = email
            msg['Subject'] = "Hai "+name+" Your Password For Kids Learning Web App"
            body = "Your Account Password Reset Successfully. You Can login using This password - " + str(password)
            msg.attach(MIMEText(body, 'plain'))
            s.send_message(msg)
            return '''<script>alert (" We have emailed your password ! ");window.location='/'</script>'''
        else:
             return '''<script>alert (" Invalid user ! ");window.location='/resetpassword'</script>'''

    else:
         return '''<script>alert (" Invalid user ! ");window.location='/resetpassword'</script>'''

@app.route('/logout')
def logout():
    session["log_id"]="0"
    return render_template("Login.html")





@app.route('/login_post', methods=["post"])
def login_post():
    db = Db()
    username = request.form["username"]
    password = request.form["password"]
    qry = "SELECT * FROM login WHERE username='" + username + "' AND PASSWORD='" + password + "'"
    
    res = db.selectOne(qry)
    if res is not None:
        type = res["type"]
        session['log_id']=res["log_id"]
        if (type == "admin"):
            return render_template("Admin/Homepage.html")
        elif type == "parent":
            return render_template("Parent/HomePage.html")
        elif type == "teacher":
            return render_template("Teacher/HomePage.html")
    else:
        return '''<script>alert ("Invalid username or password");window.location='/'</script>'''


@app.route('/parentsignup')
def parent_signup():
    return render_template("Parent Signup_2.html")


@app.route('/parentsignup_post', methods=['post'])
def parentsignup_post():
    db = Db()
    name = request.form['name']
    phone = request.form['phone']
    gender = request.form['gender']
    photo = request.files['photo']
    photo.save(static_path + "parent\\" + photo.filename)
    path = "/static/parent/" + photo.filename
    email = request.form['email']
    dob = request.form['dateofbirth']
    place = request.form['place']
    password = request.form['password']
    qry2="SELECT * FROM parents WHERE email='"+email+"'"
    res=db.selectOne(qry2)
    if res is None:
        qry = "INSERT INTO login(`username`,`password`,`type`) VALUES('" + email + "','" + password + "','pending') "
        lid = db.insert(qry)
        qry2 = "INSERT INTO parents(`name`,`photo`,`phone`,`email`,`dob`,`place`,`gender`,log_id)VALUES('" + name + "','" + path + "','" + phone + "','"+email+"','" + dob + "','" + place + "','" + gender + "','" + str(lid) + "')"
        db.insert(qry2)
        return '''<script>alert ("Parent singup sucessfully,After Admin Verification You will Recieve a Mail From Our Team");window.location='/'</script>'''
    else:
        return '''<script>alert ("Email Alredy Exist");window.location='/parentsignup'</script>'''



@app.route('/teachersignup')
def teacher_signup():
    return render_template("Teacher Signup_2.html")


@app.route('/teachersigup_post', methods=['post'])
def teachersigup_post():
    db = Db()
    name = request.form['name']
    phone = request.form['phone']
    gender = request.form['gender']
    qualification = request.form['qualification']
    photo = request.files['photo']
    photo.save(static_path + "teachers\\" + photo.filename)
    path = "/static/teachers/" + photo.filename
    email = request.form['email']
    dob = request.form['dateofbirth']
    place = request.form['place']
    password = request.form['password']
    qry2="SELECT * FROM teachers WHERE email='"+email+"'"
    res= db.selectOne(qry2)
    if res is None:
        qry = "INSERT INTO login(`username`,`password`,`type`) VALUES('" + email + "','" + password + "','pendingt') "
        lid = db.insert(qry)
        qry1 = "INSERT INTO teachers(`name`,`phone`,`photo`,`place`,`qualification`,`dob`,`gender`,email,log_id)VALUES('" + name + "','" + phone + "','" + path + "','" + place + "','" + qualification + "','" + dob + "','" + gender + "','" + email + "','" + str(lid) + "')"
        db.insert(qry1)
        return '''<script>alert ("Teachers singup sucessfully,After Admin Verification You will Recieve a Mail From Our Team");window.location='/'</script>'''
    else:
        return '''<script>alert ("Email Alredy Exist");window.location='/teachersignup'</script>'''


#---------------------------------ADMIN-------------------------------------------------------------------
# @app.route('/admin_index')
# def admin_index():
#     db= Db()
#     qry="SELECT * FROM login WHERE type='admin'"
#     res=db.select(qry)
#     print(res)
#     return render_template("Admin/admin_index.html", i=res)

@app.route('/view_parent_req')
def view_parent_req():
    db= Db()
    qry="SELECT * FROM login INNER JOIN parents ON login.log_id=parents.log_id WHERE login.type='pending'"
    res=db.select(qry)
    return render_template("Admin/view_parent_req.html",data=res)

@app.route('/approve_reject/<id>/<st>/<email>')
def approve_reject(id,st,email):
    db= Db()
    qry="UPDATE login SET TYPE='"+st+"' WHERE log_id='"+id+"'"
    res=db.update(qry)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("malabrkidslearning@gmail.com", "kids@malabar")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from DNTL"
    msg['From'] = "malabrkidslearning@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Kids Learning Web App Verification"
    if(st=="parent"):
        body = "Your Account has been verified by Our Team You Can Login with your email and Password"
    else:
         body = "Your Account has been rejected by Our Team You Can't Login with your email and Password"
   

    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    if(st=="parent"):
        return '''<script>alert ("Parent Approved Successfuly");window.location='/view_parent_req'</script>'''
    else:
         return '''<script>alert ("Parent Request Rejected");window.location='/view_parent_req'</script>'''
 

@app.route('/view_teacher_req')
def view_teacher_req():
    db= Db()
    qry="SELECT * FROM login INNER JOIN teachers ON login.log_id=teachers.log_id WHERE login.type='pendingt'"
    res=db.select(qry)
    return render_template("Admin/view_teachers_req.html",data=res)

@app.route('/approve_reject_t/<id>/<st>/<email>')
def approve_reject_t(id,st,email):
    db= Db()
    qry="UPDATE login SET TYPE='"+st+"' WHERE log_id='"+id+"'"
    res=db.update(qry)
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login("malabrkidslearning@gmail.com", "kids@malabar")
    msg = MIMEMultipart()  # create a message.........."
    message = "Messege from DNTL"
    msg['From'] = "malabrkidslearning@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Kids Learning Web App Verification"
    if(st=="teacher"):
        body = "Your Account has been verified by Our Team You Can Login with your email and Password"
    else:
         body = "Your Account has been rejected by Our Team Please Connect to Our Team For Review"
   

    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    if(st=="teacher"):
        return '''<script>alert ("Teacher request Approved Successfuly");window.location='/view_teacher_req'</script>'''
    else:
         return '''<script>alert ("Teacher Request Rejected");window.location='/view_teacher_req'</script>'''






@app.route('/addrhymes')
def add_rhymes():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Add Rhymes.html")


@app.route('/addrhyme_post', methods=['post'])
def addrhyme_post():
    db = Db()
    rhyme = request.form["rhyme"]
    file = request.files["file"]
    file.save(static_path + "rhymes\\" + file.filename)
    path = "/static/rhymes/" + file.filename
    qry = "INSERT INTO rhymes (NAME,FILE) VALUES ('" + rhyme + "','" + path + "')"
    res = db.insert(qry)
    return '''<script>alert ("Rhyme Inserted Successfully ");window.location='/addrhymes'</script>'''


@app.route('/viewrhymes')
def view_rhymes():
    db = Db()
    qry = "select * from rhymes"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Rhyms.html", data=res)


@app.route('/deleterhyme/<id>')
def deleterhyme(id):
    db = Db()
    qry = "DELETE FROM rhymes WHERE r_id='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert ("Rhyme Deleted Successfully ");window.location='/viewrhymes'</script>'''


@app.route('/viewparants')
def view_parants():
    db = Db()
    qry = "SELECT * FROM parents"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Parants.html", data=res)


@app.route('/viewstudents/<id>')
def view_students(id):
    db = Db()
    qry = "SELECT * FROM  student WHERE p_id='" + id + "'"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Students.html", data=res)


@app.route('/viewteachers')
def view_teachers():
    db = Db()
    qry = "SELECT * FROM teachers "
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Teachers.html", data=res)


@app.route('/deleteteachers/<id>')
def deleteteachers(id):
    db = Db()
    qry = "DELETE FROM teachers WHERE log_id='" + id + "'"
    res = db.delete(qry)
    qry1="DELETE FROM login WHERE log_id='"+id+"'"
    db.delete(qry1)
    return '''<script>alert (" Teacher Removed Successfully ");window.location='/viewteachers'</script>'''


@app.route('/searchtechers', methods=['post'])
def searchteachers():
    db = Db()
    search = request.form['search']
    qry = "SELECT * FROM teachers WHERE NAME LIKE  '%" + search + "%'"
    res = db.select(qry)
    return render_template("Admin/View Teachers.html", data=res)


@app.route('/viewcomplaint')
def view_complaint():
    db = Db()
    qry = "SELECT complaint.*,parents.* FROM complaint INNER JOIN parents ON complaint.p_id=parents.log_id"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Complaint.html", data=res)


@app.route('/viewcomplaint_post', methods=['post'])
def viewcomplaint_post():
    datefrom = request.form['datefrom']
    dateto = request.form['dateto']
    db = Db()
    qry = "SELECT complaint.*,parents.* FROM complaint INNER JOIN parents ON complaint.p_id=parents.log_id WHERE date between '" + datefrom + "'and '" + dateto + "'"
    res = db.select(qry)
    print(res)
    print(qry)
    return render_template("Admin/View Complaint.html", data=res)


@app.route('/sentreplay/<id>')
def sent_replay(id):
    db = Db()
    qry = "SELECT * FROM complaint WHERE c_id='" + id + "'"
    res = db.selectOne(qry)
    return render_template("Admin/Sent Replay.html", data=res)


@app.route('/sentreply_post', methods=['post'])
def sentreplay_post():
    db = Db()
    reply = request.form['reply']
    c_id = request.form['c_id']
    qry = "UPDATE complaint SET reply='" + reply + "' WHERE c_id='" + c_id + "'"
    res = db.update(qry)
    return '''<script>alert ("sent reply Successfully ");window.location='/viewcomplaint'</script>'''


@app.route('/addquestion')
def add_question():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Add Questions.html")


@app.route('/addquestion_post', methods=['post'])
def addquestion_post():
    db = Db()
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']
    qry = "INSERT INTO question (question,optiona,optionb,optionc,optiond,answer)VALUES('" + question + "','" + option1 + "','" + option2 + "','" + option3 + "','" + option4 + "','" + answer + "')"
    res = db.insert(qry)
    return '''<script>alert ("Question Added Successfully ");window.location='/addquestion'</script>'''


@app.route('/viewquestion')
def view_questions():
    db = Db()
    qry = "select * from question"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Question View.html", data=res)



@app.route('/deletequestion/<id>')
def deletequestion(id):
    db = Db()
    qry = "DELETE FROM question WHERE q_id ='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert (" Questions  Removed Successfully ");window.location='/viewquestion'</script>'''


@app.route('/editquestion/<id>')
def edit_question(id):
    db = Db()
    qry = "SELECT * FROM question WHERE q_id='" + id + "'"
    res = db.selectOne(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Edit Question.html", data=res)


@app.route('/editquestion_post', methods=['post'])
def editquestion_post():
    db = Db()
    q_id = request.form['q_id']
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    answer = request.form['answer']
    qry = "UPDATE question SET question='" + question + "',optiona='" + option1 + "',optionb='" + option2 + "',optionc='" + option3 + "',optiond='" + option3 + "',answer='" + answer + "' WHERE q_id='" + q_id + "'"
    res = db.update(qry)
    return '''<script>alert (" Questions  Edited Successfully ");window.location='/viewquestion'</script>'''


@app.route('/addnumericalproblem')
def add_numericproblem():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Add Numerical Problems.html")


@app.route('/addnumerical_post', methods=['post'])
def addnumerical_post():
    db = Db()
    question = request.form["question"]
    answer = request.form["answer"]
    qry = "INSERT INTO numerical_problem (question,answer) VALUES ('" + question + "','" + answer + "')"
    res = db.insert(qry)
    return '''<script>alert ("Numerical Questions Added Successfully ");window.location='/addnumericalproblem'</script>'''


@app.route('/viewnumericalproblem')
def view_numercalproblem():
    db = Db()
    qry = "select * from numerical_problem"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Numerical Problems.html", data=res)


@app.route('/deletenumericalproblem/<id>')
def deletenumericalpoblem(id):
    db = Db()
    qry = "DELETE FROM numerical_problem WHERE num_id='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert ("Numerical Questions  Removed Successfully ");window.location='/viewnumericalproblem'</script>'''


@app.route('/editnumericalproblem/<id>')
def editnumericalproblem(id):
    db = Db()
    qry = "SELECT * FROM numerical_problem WHERE num_id='" + id + "'"
    res = db.selectOne(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Edit Numerical Problem.html", data=res)


@app.route('/editnumericalproblem_post', methods=['post'])
def editnumericalproblem_post():
    db = Db()
    num_id = request.form['num_id']
    question = request.form['question']
    answer = request.form['answer']
    qry = "UPDATE numerical_problem SET question='" + question + "',answer='" + answer + "' WHERE num_id='" + num_id + "'"
    res = db.update(qry)
    return '''<script>alert ("Numerical Problems  Edited  Successfully ");window.location='/viewnumericalproblem'</script>'''


@app.route('/addobject')
def add_object():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Add object.html")


@app.route('/addobject_post', methods=['post'])
def addobject_post():
    db = Db()
    name = request.form["name"]
    file = request.files["file"]
    file.save(static_path + "objects\\" + file.filename)
    path = "/static/objects/" + file.filename
    qry = "INSERT INTO objects (NAME,photo) VALUES ('" + name + "','" + path + "')"
    res = db.insert(qry)
    return '''<script>alert ("Object  Inserted Successfully ");window.location='/addobject'</script>'''


@app.route('/viewobject')
def view_object():
    db = Db()
    qry = "select * from objects"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Objects.html", data=res)


@app.route('/deleteobject/<id>')
def deleteobject(id):
    db = Db()
    qry = "DELETE FROM objects WHERE ob_id ='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert ("Object  Deleted  Successfully ");window.location='/viewobject'</script>'''


@app.route('/editobject/<id>')
def edit_object(id):
    db = Db()
    qry = "SELECT * FROM objects where ob_id='" + id + "'"
    res = db.selectOne(qry)
    return render_template("Admin/Edit Object.html", data=res)


@app.route('/editobject_post', methods=['post'])
def editobject_post():
    db = Db()
    ob_id = request.form['ob_id']
    name = request.form["name"]
    if 'file' in request.files:
        file = request.files["file"]
        if file.filename != '':
            file.save(static_path + "objects\\" + file.filename)
            path = "/static/objects/" + file.filename
            qry = "UPDATE objects SET NAME='" + name + "',photo='" + path + "'WHERE ob_id='" + ob_id + "'"
            res = db.update(qry)
        else:
            qry = "UPDATE objects SET NAME='" + name + "' WHERE ob_id='" + ob_id + "'"
            res = db.update(qry)
    else:
        qry = "UPDATE objects SET NAME='" + name + "' WHERE ob_id='" + ob_id + "'"
        res = db.update(qry)
    return '''<script>alert ("Object  Edited  Successfully ");window.location='/viewobject'</script>'''


@app.route('/addwords')
def add_words():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Add Words.html")


@app.route('/addwords_post', methods=['post'])
def addwords_post():
    db = Db()
    word = request.form['word']
    qry = "INSERT INTO word (word) VALUES ('" + word + "')"
    res = db.insert(qry)
    return '''<script>alert ("Word Added Successfully ");window.location='/addwords'</script>'''


@app.route('/viewwords')
def view_words():
    db = Db()
    qry = "SELECT * FROM word"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View words.html", data=res)


@app.route('/deletewords/<id>')
def delete_words(id):
    db = Db()
    qry = "DELETE FROM word WHERE w_id = '" + id + "'"
    res = db.delete(qry)
    return '''<script>alert ("Word  Deleted  Successfully ");window.location='/viewwords'</script>'''


@app.route('/editwords/<id>')
def edit_words(id):
    db = Db()
    qry = "SELECT * FROM word WHERE w_id='" + id + "'"
    res = db.selectOne(qry)
    return render_template("Admin/Edit Words.html", data=res)


@app.route('/editwords_post', methods=['post'])
def editwords_post():
    db = Db()
    w_id = request.form['w_id']
    word = request.form['word']
    qry = "UPDATE word SET word='" + word + "' WHERE w_id='" + w_id + "'"
    res = db.update(qry)
    return '''<script>alert ("Word  Edited  Successfully ");window.location='/viewwords'</script>'''


@app.route('/addimagepuzzle')
def addimage_puzzle():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Add Image Puzzle.html")


@app.route('/addimagepuzzle_post', methods=['post'])
def addimagepuzzle_post():
    db = Db()
    puzzle = request.form['puzzle']
    photo = request.files['photo']
    photo.save(static_path + "puzzleimage\\" + photo.filename)
    path = "/static/puzzleimage/" + photo.filename
    time = request.form['time']
    qry = "INSERT INTO puzzle (puzzle,image,TIME)VALUES('" + puzzle + "','" + path + "','" + time + "')"
    res = db.insert(qry)

    fname=photo.filename
    from PIL import Image
    img = Image.open(static_path+ "puzzleimage\\"+fname)
    baseWidth = 800
    baseheight = 800
    img = img.resize((baseWidth, baseheight), Image.ANTIALIAS)
    img.save(static_path+ "puzzleimage\\"+'jigsaw_resized_' + puzzle + ".jpg")
    iPath = static_path+ "puzzleimage\\"+"jigsaw_resized_" + puzzle + ".jpg"
    import cv2
    img = cv2.imread(iPath)
    k = 1

    for i in range(0, 800, 200):
        for j in range(0, 800, 200):
            crop_img = img[i:i + 200, j:j + 200]
            cv2.imshow('img', crop_img)
            cv2.imwrite(
                static_path+ "puzzleimage\\"+'jigsaw_sliced_' + str(
                    k) + "-" + puzzle + ".jpg", crop_img)
            k = k + 1

    return '''<script>alert ("Puzzle  Inserted Successfully ");window.location='/addimagepuzzle'</script>'''


@app.route('/viewimagepuzzle')
def view_image_puzzle():
    db = Db()
    qry = "SELECT * FROM puzzle"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/View Image Puzzle.html", data=res)


@app.route('/deleteimagepuzzle/<id>')
def delete_imagepuzzle(id):
    db = Db()
    qry = "DELETE FROM puzzle WHERE puz_id='" + id + "'"
    res = db.delete(qry)
    return '''<script>alert ("Puzzle  Deleted  Successfully ");window.location='/viewimagepuzzle'</script>'''


@app.route('/editimagepuzzle/<id>')
def editimagepuzzle(id):
    db = Db()
    qry = "SELECT * FROM puzzle WHERE puz_id='" + id + "'"
    res = db.selectOne(qry)
    return render_template("Admin/Edit Image Puzzle.html", data=res)


@app.route('/editimagepuzzle_post', methods=['post'])
def editimagepuzzle_post():
    db = Db()
    puz_id = request.form['puz_id']
    puzzle = request.form['puzzle']
    time = request.form['time']
    if 'photo' in request.files:
        photo = request.files["photo"]
        if photo.filename != '':
            photo.save(static_path + "puzzleimage\\" + photo.filename)
            path = "/static/puzzleimage/" + photo.filename
            qry = "UPDATE puzzle SET puzzle='" + puzzle + "',image='" + path + "',TIME='" + time + "' WHERE puz_id='" + puz_id + "'"
            res = db.update(qry)
            print("hhhh1")
            return '''<script>alert ("Image Puzzle  Edited  Successfully ");window.location='/viewimagepuzzle'</script>'''
        else:
            qry = "UPDATE puzzle SET puzzle='" + puzzle + "',TIME='" + time + "' WHERE puz_id='" + puz_id + "'"
            res = db.update(qry)
            print("hhhh2")
            return '''<script>alert ("Image Puzzle  Edited  Successfully ");window.location='/viewimagepuzzle'</script>'''
    else:
        qry = "UPDATE puzzle SET puzzle='" + puzzle + "',TIME='" + time + "' WHERE puz_id='" + puz_id + "'"
        res = db.update(qry)
        print("hhhh3")
        return '''<script>alert ("Image Puzzle  Edited  Successfully ");window.location='/viewimagepuzzle'</script>'''

@app.route('/changepassword')
def change_password():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Admin/Change Password.html")

@app.route('/changepassword_post', methods=['post'])
def changepassword_post():
    db=Db()
    email=request.form['email']
    oldpassword=request.form['oldpassword']
    newpassword=request.form['newpassword']
    qry="UPDATE login SET password='"+newpassword+"' WHERE username='"+email+"' AND password='"+oldpassword+"' "
    res=db.update(qry)
    return '''<script>alert ("Password  Changed  Successfully ,Please Login again");window.location='/'</script>'''


# ---------------------------------------PARENT  ------------------------------------

@app.route('/changepassword_parent')
def change_passwordparent():
    return render_template("Parent/Change Password.html")

@app.route('/changepasswordparent_post',methods=['post'])
def changepasswordparent_post():
    db=Db()
    lid=str(session["log_id"])
    email=request.form['email']
    oldpassword=request.form['oldpassword']
    newpassword=request.form['newpassword']
    qry1="select * from login where username='"+email+"' and password='"+oldpassword+"' and log_id='"+lid+"'"
    res1=db.selectOne(qry1)
    if res1 is not None:
        qry="UPDATE login SET password='"+newpassword+"' WHERE username='"+email+"' AND password='"+oldpassword+"' AND log_id='"+str(session["log_id"])+"'"
        print(qry)
        res=db.update(qry)
        return '''<script>alert ("Password  Changed  Successfully ");window.location='/'</script>'''
    else:
        return '''<script>alert ("Your Email ID or Password Was Invalid ");window.location='/'</script>'''


@app.route('/addstudent')
def addstudent():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Parent/Add Student.html")


@app.route('/addstudent_post',methods=['post'])
def addstudent_post():
    db = Db()
    name=request.form['name']
    phone=request.form['phone']
    age=request.form['age']
    photo = request.files['photo']
    photo.save(static_path + "student\\" + photo.filename)
    path = "/static/student/" + photo.filename
    gender=request.form['gender']
    standered=request.form['standered']
    email=request.form['email']
    qry1="INSERT INTO login (username,password,type)VALUES('"+email+"','"+phone+"','student') "
    lid=db.insert(qry1)
    qry="INSERT INTO student (`name`,`phone`,`age`,`photo`,`gender`,`standered`,p_id,log_id)VALUES ('"+name+"','"+phone+"','"+age+"','"+path+"','"+gender+"','"+ standered+"','"+str(session["log_id"])+"','"+str(lid)+"')"
    res=db.insert(qry)
    return '''<script>alert ("Student Added Successfully ");window.location='/addstudent'</script>'''

@app.route('/viewstudent')
def viewstudent():
    db=Db()
    qry="SELECT * FROM student WHERE p_id='"+str(session["log_id"])+"' "
    res=db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Parent/ViewStudent.html", data=res)

@app.route('/deletestudent/<id>')
def deleteStudent(id):
    db=Db()
    qry="DELETE FROM student WHERE s_id='"+id+"'"
    res=db.delete(qry)
    return '''<script>alert ("Student Deleted Successfully ");window.location='/viewstudent'</script>'''

@app.route('/editstudent/<id>')
def edit_student(id):
    db=Db()
    qry="SELECT * FROM student WHERE s_id='"+id+"' "
    res=db.selectOne(qry)   
    return render_template("Parent/EditStudent.html", data=res)

@app.route('/editstudent_post',methods=['post'])
def edit_student_post():
    db=Db()
    s_id=request.form['s_id']
    name=request.form['name']
    phone=request.form['phone']
    age=request.form['age']
    standered=request.form['standered']
    gender = request.form['gender']
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename !='':
            photo.save(static_path + "student\\" + photo.filename)
            path = "/static/student/" + photo.filename
            qry="UPDATE student SET name='"+name+"',phone='"+phone+"',age='"+age+"',photo='"+path+"',standered='"+standered+"',gender='"+gender+"' WHERE s_id='"+s_id+"'"
            res=db.update(qry)
        else:
             qry="UPDATE student SET name='"+name+"',phone='"+phone+"',age='"+age+"',standered='"+standered+"',gender='"+gender+"' WHERE s_id='"+s_id+"'"
             res=db.update(qry)
    else:
         qry="UPDATE student SET name='"+name+"',phone='"+phone+"',age='"+age+"',standered='"+standered+"',gender='"+gender+"' WHERE s_id='"+s_id+"'"
         res=db.update(qry)
    return '''<script>alert ("Student Edited Successfully ");window.location='/viewstudent'</script>'''


@app.route('/viewteachers_parent')
def viewteachers():
    db= Db()
    qry="SELECT *FROM teachers"
    res=db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Parent/View Teachers2.html",data=res)

@app.route("/par_chat_teacher/<uid>/<name>")
def par_chat_teacher(uid, name):
    session["seluid"]=uid
    session["selname"]=name
    return render_template('Parent/chat_teacher.html', toid=uid, name=name)
   


@app.route("/par_chat_teacher_chk",methods=['post'])        # refresh messages chatlist
def par_chat_teacher_chk():
    uid=request.form['idd']
    qry = "select date,msg,form_id from chat where (form_id='" + str(
        session['log_id']) + "' and to_id='" + uid + "') or ((form_id='" + uid + "' and to_id='" + str(
        session['log_id']) + "')) order by chat_id desc"
    c = Db()
    res = c.select(qry)
    return jsonify(res)


@app.route("/par_chat_teacher_post",methods=['POST'])
def par_chat_teacher_post():
    id=str(session["seluid"])
    name=str(session["selname"])
    ta=request.form["ta"]
    qry="insert into chat(msg,date,form_id,to_id) values('"+ta+"',CURDATE(),'"+str(session['log_id'])+"','"+id+"')"
    d=Db()
    d.insert(qry)
    return render_template('Parent/chat_teacher.html', toid=id, name=name)
    



import matplotlib
import datetime
matplotlib.use('Agg')
from matplotlib import pyplot as plt
def piechart(stat, scor, filename):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    # labels = 'Sale', 'Purchase'
    # sizes = [random.randint(10,30), random.randint(30,50)]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(scor, explode=explode, labels=stat, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.savefig(static_path+"graphs/"+filename, dpi=100)
    return "/static/graphs/"+filename




@app.route('/viewperfomance/<id>')
def viewperfomance(id):
    db=Db()
    dt=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


    ####        puzzle result
    qry="SELECT COUNT(`pr_id`)FROM `puzzle_result` WHERE `s_id`='"+id+"'"
    total_pr=db.selectOne(qry)
    qry1="SELECT COUNT(`pr_id`)FROM `puzzle_result` WHERE `s_id`='"+id+"' AND result='pass'"
    mark_pr=db.selectOne(qry1)

    pr_stat=['pass', 'fail']
    pr_score=[]
    pr_score.append(int(mark_pr['COUNT(`pr_id`)']))                                         # pass
    pr_score.append(int(total_pr['COUNT(`pr_id`)']) - int(mark_pr['COUNT(`pr_id`)']))       # fail
    pr_filename=dt+"_pr.png"
    pr_chart=piechart(pr_stat, pr_score, pr_filename)

    ####        puzzle  result end
    ################################ question result

    qry2="SELECT COUNT(`qr_id`) FROM `question_result` WHERE `st_id`='"+id+"'"
    total_qr=db.selectOne(qry2)
    qry3="SELECT COUNT(`qr_id`) FROM `question_result` WHERE `st_id`='"+id+"' AND result='1'"
    mark_qr=db.selectOne(qry3)

    qr_stat=['pass', 'fail']
    qr_score=[]
    qr_score.append(int(mark_qr['COUNT(`qr_id`)']))                                         # pass
    qr_score.append(int(total_qr['COUNT(`qr_id`)']) - int(mark_qr['COUNT(`qr_id`)']))       # fail
    qr_filename=dt+"_qr.png"
    qr_chart=piechart(qr_stat, qr_score, qr_filename)

    ####        question result end
    #########     Numerical result

    qry4="SELECT COUNT(`nr_id`) FROM  `numerical_result` WHERE `st_id`='"+id+"'"
    total_nr=db.selectOne(qry4)
    qry5="SELECT COUNT(`nr_id`) FROM  `numerical_result` WHERE `st_id`='"+id+"'AND result='pass'"
    mark_nr=db.selectOne(qry5)

    nr_stat=['pass', 'fail']
    nr_score=[]
    nr_score.append(int(mark_nr['COUNT(`nr_id`)']))                                         # pass
    nr_score.append(int(total_nr['COUNT(`nr_id`)']) - int(mark_nr['COUNT(`nr_id`)']))       # fail
    nr_filename=dt+"_nr.png"
    nr_chart=piechart(nr_stat, nr_score, nr_filename)
                     #########     Numerical result End
                      #########     Object result
    qry6="SELECT COUNT(`or_id`) FROM `object_result` WHERE `st_id`='"+id+"'"
    total_or=db.selectOne(qry6)
    qry7="SELECT COUNT(`or_id`) FROM `object_result` WHERE `st_id`='"+id+"' AND result='pass'"
    mark_or=db.selectOne(qry7)

    or_stat=['pass', 'fail']
    or_score=[]
    or_score.append(int(mark_or['COUNT(`or_id`)']))                                         # pass
    or_score.append(int(total_or['COUNT(`or_id`)']) - int(mark_or['COUNT(`or_id`)']))       # fail
    or_filename=dt+"_or.png"
    or_chart=piechart(or_stat, or_score, or_filename)
             #########     Object  result End

    qry8="SELECT COUNT(`wr_id`) FROM `word_result` WHERE `st_id`='"+id+"'"
    total_wr=db.selectOne(qry8)
    qry9="SELECT COUNT(`wr_id`) FROM `word_result` WHERE `st_id`='"+id+"' AND result='yes'"
    mark_wr=db.selectOne(qry9)

    wr_stat=['pass', 'fail']
    wr_score=[]
    wr_score.append(int(mark_wr['COUNT(`wr_id`)']))                                         # pass
    wr_score.append(int(total_wr['COUNT(`wr_id`)']) - int(mark_wr['COUNT(`wr_id`)']))       # fail
    wr_filename=dt+"_wr.png"
    wr_chart=piechart(wr_stat, wr_score, wr_filename)

    qry10="SELECT COUNT(`hw_id`) FROM `handwriting`WHERE `st_id`='"+id+"'"
    total_hw=db.selectOne(qry10)
    qry11="SELECT COUNT(`hw_id`) FROM `handwriting` WHERE `st_id`='"+id+"' AND result='1'"
    mark_hw=db.selectOne(qry10)

    hw_stat=['pass', 'fail']
    hw_score=[]
    hw_score.append(int(mark_hw['COUNT(`hw_id`)']))                                         # pass
    hw_score.append(int(total_hw['COUNT(`hw_id`)']) - int(mark_hw['COUNT(`hw_id`)']))       # fail
    hw_filename=dt+"_hw.png"
    hw_chart=piechart(hw_stat, hw_score, hw_filename)


    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Parent/ViewPerfomance.html",total_pr=total_pr,mark_pr=mark_pr, pr_chart=pr_chart ,total_qr=total_qr,mark_qr=mark_qr, qr_chart=qr_chart ,total_nr=total_nr,mark_nr=mark_nr,nr_chart=nr_chart,total_or=total_or,mark_or=mark_or,or_chart=or_chart,total_wr=total_wr,mark_wr=mark_wr,wr_chart=wr_chart,total_hw=total_hw,mark_hw=mark_hw,hw_chart=hw_chart)

@app.route('/sent_complaint')
def sent_complaint():
     if str(session["log_id"])=="0":
            return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
     else:
         return render_template("Parent/send_complaints.html")

   

@app.route('/sentcomplaint', methods=['post'])
def send_complaints():
    db= Db()
    complaint= request.form["complaint"]
    plid=session["log_id"]
    qry="INSERT INTO `complaint` (`p_id`,`complaint`,`date`,`reply`) VALUES('"+str(plid)+"','"+complaint+"',curdate(),'pending')"
    res = db.insert(qry)
    return '''<script>alert ("sent complaint Successfully");window.location='/sent_complaint'</script>'''

@app.route('/viewreply')
def viewreply():
    db= Db()
    p_id=session["log_id"]
    qry="SELECT *FROM complaint WHERE p_id = '"+str(p_id)+"'"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Parent/viewreply.html", data=res)

    

# ---------------------------------------TEACHER------------------------------------

@app.route('/changepassword_teacher')
def change_passwordteacher():
    return render_template("Teacher/Change Password.html")

@app.route('/changepasswordteacher_post',methods=['post'])
def changepasswordteacher_post():
    db=Db()
    lid=str(session["log_id"])
    email=request.form['email']
    oldpassword=request.form['oldpassword']
    newpassword=request.form['newpassword']
    qry1="select * from login where username='"+email+"' and password='"+oldpassword+"' and log_id='"+lid+"'"
    res1=db.selectOne(qry1)
    if res1 is not None:
         qry="UPDATE login SET password='"+newpassword+"' WHERE username='"+email+"' AND password='"+oldpassword+"' AND log_id='"+str(session["log_id"])+"'"
         print(qry)
         res=db.update(qry)
         return '''<script>alert ("Password  Changed  Successfully Please Login Again");window.location='/'</script>'''
    else:
        return '''<script>alert ("Your Email ID or Password Was Invalid ");window.location='/'</script>'''

@app.route('/viewprofile')
def viewprofile():
    db=Db()
    qry="SELECT * FROM teachers WHERE log_id='"+str(session["log_id"])+"'"
    res=db.selectOne(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Teacher/ViewProfile.html", i=res)

@app.route('/studymaterials')
def studymaterials():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Teacher/studymaterial.html")

@app.route('/studymaterials_post', methods=['post'])
def studymaterials_post():
    db = Db()
    subject= request.form['subject']
    file = request.files["file"]
    file.save(static_path + "studymaterial\\" + file.filename)
    path = "/static/studymaterial/" + file.filename
    qry="INSERT INTO study_meterials(subject,file,t_id,date)VALUES('"+subject+"','"+path+"','"+str(session["log_id"])+"',curdate())"
    res=db.insert(qry)
    return '''<script>alert ("Study Material Added Successfully ");window.location='/studymaterials'</script>'''

@app.route('/viewstudymeterial')
def viewstudymeterial():
    db= Db()
    qry="SELECT * FROM study_meterials WHERE t_id='"+str(session["log_id"])+"'"
    res=db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Teacher/View Studymaterials.html", data=res)

@app.route('/deletestudymeterial/<id>')
def deletestudymeterial(id):
    db=Db()
    qry="DELETE FROM study_meterials WHERE m_id='"+id+"'"
    res=db.delete(qry)
    return '''<script>alert ("Study Material Deleted Successfully ");window.location='/viewstudymeterial'</script>'''

@app.route('/editstudymeterial/<id>')
def editstudymeterial(id):
    db=Db()
    qry="SELECT * FROM study_meterials WHERE m_id='"+id+"'"
    res=db.selectOne(qry)   
    return render_template("Teacher/Edit studymeterial.html", data=res)

@app.route('/editstudymeterial_post',methods=['post'])
def editstudymeterial_post():
    db=Db()
    m_id=request.form['m_id']   
    subject= request.form['subject']
    qry="UPDATE study_meterials SET subject='"+subject+"' WHERE m_id='"+m_id+"'"
    res=db.update(qry)
    return '''<script>alert ("Study Material Name Edited Successfully ");window.location='/viewstudymeterial'</script>'''

@app.route('/addexam')
def adddexam():
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Teacher/Add Exam.html")


@app.route('/addexam_post', methods=['post'])
def adddexam_post():
    db = Db()
    subject= request.form['subject']
    date = request.form['date']
    time = request.form['time']
    qry="INSERT INTO exam(subject,date,time,t_id)VALUES('"+subject+"','"+date+"','"+time+"','"+str(session["log_id"])+"')"
    res=db.insert(qry)
    return '''<script>alert ("Exam Added Successfully ");window.location='/addexam'</script>'''

@app.route('/viewexam')
def viewexam():
    db= Db()
    qry="SELECT * FROM exam WHERE t_id='"+str(session["log_id"])+"'"
    res=db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Teacher/View Exam.html", data=res)

@app.route('/deleteexam/<id>')
def deleteexam(id):
    db=Db()
    qry="DELETE FROM exam WHERE ex_id='"+id+"'"
    res=db.delete(qry)
    return '''<script>alert ("Exam Deleted Successfully ");window.location='/viewexam'</script>'''

@app.route('/editexam/<id>')
def editexam(id):
    db= Db()
    qry="SELECT * FROM exam WHERE ex_id ='"+id+"'"
    res=db.selectOne(qry)
    return render_template('Teacher/Edit Exam.html',data=res)

@app.route('/editexam_post',methods=['post'])
def editexam_post():
    db= Db()
    ex_id=request.form['ex_id']
    subject= request.form['subject']
    date=request.form['date']
    time=request.form['time']
    qry="UPDATE exam SET subject='"+subject+"',date='"+date+"',time='"+time+"' WHERE ex_id='"+ex_id+"'"
    res = db.update(qry)
    return '''<script>alert ("Exam Edited Successfully ");window.location='/viewexam'</script>'''


@app.route('/addexam_question/<id>')
def addquestion_teacher(id):
    session["ex_id"]=id
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template('Teacher/Add Exam Questions.html')

@app.route('/addexamquestion_post', methods=['post'])
def addexamquestion_post():
    db = Db()
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3= request.form['option3']
    option4= request.form['option4']
    answer= request.form['answer']
    qry="INSERT INTO exam_question(`question`,`optiona`,`optionb`,`optionc`,`optiond`,`answer`,`ex_id`)VALUES('"+question+"','"+option1+"','"+option2+"','"+option3+"','"+option4+"','"+answer+"','"+str(session['ex_id'])+"')"
    res = db.insert(qry)
    return viewexam_questions(str(session['ex_id']))

@app.route('/viewexam_questions/<id>')
def viewexam_questions(id):
    db=Db()
    session["ex_id"]=id
    qry="SELECT * FROM exam_question WHERE ex_id='"+id+"'"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template('Teacher/View Exam Question.html',data=res)

@app.route('/delectexamquestion/<id>/<exid>')
def delectexamquestion(id,exid):
    db=Db()
    qry=" DELETE FROM exam_question WHERE exq_id='"+id+"'"
    res=db.delete(qry)
    # path="/viewexam_questions/"+str(exid)
    return '''<script>alert ("Exam Question Deleted Successfully ");window.location='/viewexam_questions1'</script>'''
    # return viewexam_questions(exid)


@app.route('/viewexam_questions1')
def viewexam_questions1():
    db=Db()
    qry="SELECT * FROM exam_question WHERE ex_id='"+str(session["ex_id"])+"'"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template('Teacher/View Exam Question.html',data=res)

@app.route('/editexamquestion/<id>/<exid>')
def editexamquestion(id,exid):
    db= Db()
    qry=" SELECT *FROM exam_question WHERE exq_id ='"+id+"'"
    print(qry)
    session["ex_id"]=exid
    res=db.selectOne(qry)
    return render_template('Teacher/Edit Exam Questions.html',data=res)

@app.route('/editexamquestion_post',methods=['post'])
def editexam_question():
    db= Db()
    exq_id= request.form['exq_id']
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3= request.form['option3']
    option4= request.form['option4']
    answer= request.form['answer']
    qry = "UPDATE exam_question SET question='" + question + "',optiona='" + option1 + "',optionb='" + option2 + "',optionc='" + option3 + "',optiond='" + option4 + "',answer='" + answer + "' WHERE exq_id='" + exq_id + "'"
    print(qry)
    res=db.update(qry)
    return '''<script>alert ("Exam Question Edited Successfully ");window.location='/viewexam_questions1'</script>'''

@app.route('/viewstudent_teacher')
def viewStudentTeacher():
    db=Db()
    qry="SELECT student.*,parents.name AS p_name,parents.phone AS p_phone FROM student INNER JOIN parents ON student.p_id=parents.log_id"
    res = db.select(qry)
    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template('Teacher/ViewStudent.html',data=res)



@app.route("/teacher_chat_parent/<uid>/<name>")
def techer_chat_parent(uid, name):
    session["selpid"]=uid
    session["selpname"]=name
    return render_template('Teacher/chat_parent.html', toid=uid, name=name)
   


@app.route("/teacher_chat_parent_chk",methods=['post'])        # refresh messages chatlist
def teacher_chat_parent_chk():
    uid=request.form['idd']
    qry = "select date,msg,form_id from chat where (form_id='" + str(
        session['log_id']) + "' and to_id='" + uid + "') or ((form_id='" + uid + "' and to_id='" + str(
        session['log_id']) + "')) order by chat_id desc"
    c = Db()
    res = c.select(qry)
    return jsonify(res)


@app.route("/teacher_chat_parent_post",methods=['POST'])
def par_chat_parent_post():
    id=str(session["selpid"])
    name=str(session["selpname"])
    ta=request.form["ta"]
    qry="insert into chat(msg,date,form_id,to_id) values('"+ta+"',CURDATE(),'"+str(session['log_id'])+"','"+id+"')"
    d=Db()
    d.insert(qry)
    return render_template('Teacher/chat_parent.html', toid=id, name=name)
    




@app.route('/viewperfomanceteacher/<id>')
def viewperfomance_teacher(id):
    db=Db()
    dt=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


    ####        puzzle result
    qry="SELECT COUNT(`pr_id`)FROM `puzzle_result` WHERE `s_id`='"+id+"'"
    total_pr=db.selectOne(qry)
    qry1="SELECT COUNT(`pr_id`)FROM `puzzle_result` WHERE `s_id`='"+id+"' AND result='pass'"
    mark_pr=db.selectOne(qry1)

    pr_stat=['pass', 'fail']
    pr_score=[]
    pr_score.append(int(mark_pr['COUNT(`pr_id`)']))                                         # pass
    pr_score.append(int(total_pr['COUNT(`pr_id`)']) - int(mark_pr['COUNT(`pr_id`)']))       # fail
    pr_filename=dt+"_pr.png"
    pr_chart=piechart(pr_stat, pr_score, pr_filename)

    ####        puzzle  result end
    ################################ question result

    qry2="SELECT COUNT(`qr_id`) FROM `question_result` WHERE `st_id`='"+id+"'"
    total_qr=db.selectOne(qry2)
    qry3="SELECT COUNT(`qr_id`) FROM `question_result` WHERE `st_id`='"+id+"' AND result='1'"
    mark_qr=db.selectOne(qry3)

    qr_stat=['pass', 'fail']
    qr_score=[]
    qr_score.append(int(mark_qr['COUNT(`qr_id`)']))                                         # pass
    qr_score.append(int(total_qr['COUNT(`qr_id`)']) - int(mark_qr['COUNT(`qr_id`)']))       # fail
    qr_filename=dt+"_qr.png"
    qr_chart=piechart(qr_stat, qr_score, qr_filename)

    ####        question result end
    #########     Numerical result

    qry4="SELECT COUNT(`nr_id`) FROM  `numerical_result` WHERE `st_id`='"+id+"'"
    total_nr=db.selectOne(qry4)
    qry5="SELECT COUNT(`nr_id`) FROM  `numerical_result` WHERE `st_id`='"+id+"'AND result='pass'"
    mark_nr=db.selectOne(qry5)

    nr_stat=['pass', 'fail']
    nr_score=[]
    nr_score.append(int(mark_nr['COUNT(`nr_id`)']))                                         # pass
    nr_score.append(int(total_nr['COUNT(`nr_id`)']) - int(mark_nr['COUNT(`nr_id`)']))       # fail
    nr_filename=dt+"_nr.png"
    nr_chart=piechart(nr_stat, nr_score, nr_filename)
                     #########     Numerical result End
                      #########     Object result
    qry6="SELECT COUNT(`or_id`) FROM `object_result` WHERE `st_id`='"+id+"'"
    total_or=db.selectOne(qry6)
    qry7="SELECT COUNT(`or_id`) FROM `object_result` WHERE `st_id`='"+id+"' AND result='pass'"
    mark_or=db.selectOne(qry7)

    or_stat=['pass', 'fail']
    or_score=[]
    or_score.append(int(mark_or['COUNT(`or_id`)']))                                         # pass
    or_score.append(int(total_or['COUNT(`or_id`)']) - int(mark_or['COUNT(`or_id`)']))       # fail
    or_filename=dt+"_or.png"
    or_chart=piechart(or_stat, or_score, or_filename)
             #########     Object  result End

    qry8="SELECT COUNT(`wr_id`) FROM `word_result` WHERE `st_id`='"+id+"'"
    total_wr=db.selectOne(qry8)
    qry9="SELECT COUNT(`wr_id`) FROM `word_result` WHERE `st_id`='"+id+"' AND result='yes'"
    mark_wr=db.selectOne(qry9)

    wr_stat=['pass', 'fail']
    wr_score=[]
    wr_score.append(int(mark_wr['COUNT(`wr_id`)']))                                         # pass
    wr_score.append(int(total_wr['COUNT(`wr_id`)']) - int(mark_wr['COUNT(`wr_id`)']))       # fail
    wr_filename=dt+"_wr.png"
    wr_chart=piechart(wr_stat, wr_score, wr_filename)

    qry10="SELECT COUNT(`hw_id`) FROM `handwriting`WHERE `st_id`='"+id+"'"
    total_hw=db.selectOne(qry10)
    qry11="SELECT COUNT(`hw_id`) FROM `handwriting` WHERE `st_id`='"+id+"' AND result='1'"
    mark_hw=db.selectOne(qry10)

    hw_stat=['pass', 'fail']
    hw_score=[]
    hw_score.append(int(mark_hw['COUNT(`hw_id`)']))                                         # pass
    hw_score.append(int(total_hw['COUNT(`hw_id`)']) - int(mark_hw['COUNT(`hw_id`)']))       # fail
    hw_filename=dt+"_hw.png"
    hw_chart=piechart(hw_stat, hw_score, hw_filename)

    if str(session["log_id"])=="0":
        return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
    else:
        return render_template("Teacher/ViewPerfomance.html",total_pr=total_pr,mark_pr=mark_pr, pr_chart=pr_chart ,total_qr=total_qr,mark_qr=mark_qr, qr_chart=qr_chart ,total_nr=total_nr,mark_nr=mark_nr,nr_chart=nr_chart,total_or=total_or,mark_or=mark_or,or_chart=or_chart,total_wr=total_wr,mark_wr=mark_wr,wr_chart=wr_chart,total_hw=total_hw,mark_hw=mark_hw,hw_chart=hw_chart)


# @app.route('/viewperfomanceteacher/<id>')
# def viewperfomance_teacher(id):
#     db=Db()
#     qry="SELECT COUNT(`pr_id`)FROM `puzzle_result` WHERE `s_id`='"+id+"'"
#     total_pr=db.selectOne(qry)
#     qry1="SELECT COUNT(`pr_id`)FROM `puzzle_result` WHERE `s_id`='"+id+"' AND result='pass'"
#     mark_pr=db.selectOne(qry1)

    

#     qry2="SELECT COUNT(`qr_id`) FROM `question_result` WHERE `st_id`='"+id+"'"
#     total_qr=db.selectOne(qry2)
#     qry3="SELECT COUNT(`qr_id`) FROM `question_result` WHERE `st_id`='"+id+"' AND result='1'"
#     mark_qr=db.selectOne(qry3)

#     qry4="SELECT COUNT(`nr_id`) FROM  `numerical_result` WHERE `st_id`='"+id+"'"
#     total_nr=db.selectOne(qry4)
#     qry5="SELECT COUNT(`nr_id`) FROM  `numerical_result` WHERE `st_id`='"+id+"'AND result='pass'"
#     mark_nr=db.selectOne(qry5)

#     qry6="SELECT COUNT(`or_id`) FROM `object_result` WHERE `st_id`='"+id+"'"
#     total_or=db.selectOne(qry6)
#     qry7="SELECT COUNT(`or_id`) FROM `object_result` WHERE `st_id`='"+id+"' AND result='pass'"
#     mark_or=db.selectOne(qry7)

#     qry8="SELECT COUNT(`wr_id`) FROM `word_result` WHERE `st_id`='"+id+"'"
#     total_wr=db.selectOne(qry8)
#     qry9="SELECT COUNT(`wr_id`) FROM `word_result` WHERE `st_id`='"+id+"' AND result='yes'"
#     mark_wr=db.selectOne(qry9)

#     qry10="SELECT COUNT(`hw_id`) FROM `handwriting`WHERE `st_id`='"+id+"'"
#     total_hw=db.selectOne(qry10)
#     qry11="SELECT COUNT(`hw_id`) FROM `handwriting` WHERE `st_id`='"+id+"' AND result='1'"
#     mark_hw=db.selectOne(qry10)
#     if str(session["log_id"])=="0":
#         return '''<script>alert ("Invalid Access Please Login ");window.location='/'</script>'''
#     else:
#         return render_template("Teacher/ViewPerfomance.html",total_pr=total_pr,mark_pr=mark_pr,total_qr=total_qr,mark_qr=mark_qr,total_nr=total_nr,mark_nr=mark_nr,total_or=total_or,mark_or=mark_or,total_wr=total_wr,mark_wr=mark_wr,total_hw=total_hw,mark_hw=mark_hw)





#-------------------------------------------------ANDRIOD-STUDENT--------------------------------------------------

@app.route('/login_post_student', methods=["post"])
def login_post_student():
    db = Db()
    username = request.form["username"]
    password = request.form["password"]
    qry = "SELECT * FROM login WHERE username='" + username + "' AND PASSWORD='" + password + "'"
    res = db.selectOne(qry)
    if res is not None:
        return jsonify (status="ok",log_id=res['log_id'],type=res['type'])
    else:
        return jsonify(status="no")
    


@app.route('/viewstudent_android', methods=['post'])
def viewstudent_android():
    db=Db()
    lid=request.form['lid']
    qry="SELECT * FROM student WHERE log_id='"+lid+"'"
    res = db.selectOne(qry)
    if res is not None:
        return jsonify(status="ok",name=res['name'],phone=res['phone'],photo=res['photo'],age=res['age'],gender=res['gender'],standered=res['standered'])
    else:
        return jsonify(status="no")

@app.route('/viewmaterial_student',methods=['post'])
def viewmaterial_student():
    db=Db()
    qry="SELECT * FROM study_meterials INNER JOIN teachers ON `teachers`.`log_id`=study_meterials.`t_id`"
    res=db.select(qry)
    if len(res)==0:
        return jsonify(status="no")
    else:
        return jsonify(status="ok",users=res)

@app.route('/viewnumericalproblem_student', methods=['post'])
def viewnumericalproblem_student():
    db= Db()
    qry="SELECT * FROM numerical_problem"
    res=db.select(qry)
    print(res)
    if len(res)==0:
            return jsonify(status="no")
    else:
        return jsonify(status="ok",users=res)


@app.route('/addnumerical_mark',methods=['post'])
def addnumerical_mark():
    st_id=request.form['lid']
    print(st_id)
    nr_id=request.form['num_id']
    status=request.form['status']
    
    db=Db()
    qry="SELECT * FROM numerical_result WHERE st_id='"+st_id+"' and num_id='"+nr_id+"'"
    res=db.selectOne(qry)
    if res is None:
        qry2="INSERT INTO `numerical_result` (st_id,num_id,result) VALUES ('"+st_id+"','"+nr_id+"','"+status+"')"
        db.insert(qry2)
        return jsonify(status="no")
    else:
        qry2="UPDATE numerical_result SET result='"+status+"' WHERE st_id='"+st_id+"' AND num_id='"+nr_id+"'"
        db.update(qry2)
        return jsonify(status="ok",users=res)

@app.route('/viewimagepuzzle_student',methods=['post'])
def viewiamgepuzzle_student ():
    db=Db()
    qry="SELECT * FROM puzzle"
    res=db.select(qry)
    if len(res)==0:
        return jsonify(status="no")
    else:
        return jsonify(status="ok",users=res)

@app.route('/and_puzzleresults',methods=['post'])
def puzzleresuts_student():
    db= Db()
    puz_id=request.form['puzzleid']
    s_id=request.form['lid']
    result=request.form['result']
    time_taken= request.form['time']
    qry="INSERT INTO puzzle_result (puz_id,s_id,result,time_taken)  VALUES('"+puz_id+"','"+s_id+"','"+result+"','"+time_taken+"')"
    res=db.insert(qry)
    if len(res)==0:
        return jsonify(status="no")
    else:
        return jsonify(status="ok",users=res)


@app.route('/view_acc_img',methods=['POST'])
def ed_f_v():
    # print("m")

   # "\uploads\images\jigsaw\jigsaw_sliced\1 - arch.jpg"

    import random
    list = []
    for i in range(1000):
        r = random.randint(1, 16)
        if r not in list: list.append(r)
    abc = ""
    for ii in list:
        abc = abc + str(ii) + ","

    # print(abc)

    res = abc
    if res is not None:
        return jsonify(status='ok',fname=res)
    else:
        return jsonify(status='no')


@app.route('/viewexam_student',methods=['POST'])
def viewexam_student():
    db=Db()
    qry="SELECT exam.*, teachers.name FROM exam INNER JOIN teachers ON `teachers`.`log_id`=exam.t_id"
    res=db.select(qry)
    if len(res)==0:
        return jsonify(status="no")
    else:
        return jsonify(status="ok",users=res)

@app.route('/loadquestions_student' ,methods=['post'])
def loadquestions_student():
    ex_id=request.form['ex_id']
    db=Db()
    qry="SELECT * FROM `exam_question` WHERE ex_id='"+ex_id+"'"
    res=db.select(qry)
    if len(res)==0:
        return jsonify(status="no")
    else:
        return jsonify(status="ok", ln=len(res),users=res)

@app.route('/markinsert_student', methods=['post'])
def markinsert_student():
    db=Db()
    mark=request.form['mark']
    ex_id=request.form['ex_id']
    lid=request.form['lid']
    qry = "INSERT INTO  `exam_result`(`ex_id`,`s_id`,`result`,`date`)VALUES ('"+ex_id+"','"+lid+"','"+mark+"',CURDATE())"
    res= db.insert(qry)
    return jsonify(status="ok")

@app.route('/viewwords_student',methods=['POST'])
def viewwords_student():
    db=Db()
    qry= "SELECT * FROM word"
    res=db.select(qry)
    return jsonify(status="ok", data=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
