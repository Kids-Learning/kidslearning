from flask import Flask, render_template, request
from flask.globals import session
from DBConnection import Db

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #session key
static_path = "C:\\Users\\user\\Desktop\\project\\Kids Learning\\static\\"


@app.route('/')
def hello_world():
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
    return render_template("Parent Signup.html")


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
    qry = "INSERT INTO login(`username`,`password`,`type`) VALUES('" + email + "','" + password + "','parent') "
    lid = db.insert(qry)

    qry2 = "INSERT INTO parents(`name`,`photo`,`phone`,`dob`,`place`,`gender`,log_id)VALUES('" + name + "','" + path + "','" + phone + "','" + dob + "','" + place + "','" + gender + "','" + str(
        lid) + "')"
    db.insert(qry2)
    return '''<script>alert ("Parent singup sucessfully");window.location='/'</script>'''


@app.route('/teachersignup')
def teacher_signup():
    return render_template("Teacher Signup.html")


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
    qry = "INSERT INTO login(`username`,`password`,`type`) VALUES('" + email + "','" + password + "','teacher') "
    lid = db.insert(qry)
    qry1 = "INSERT INTO teachers(`name`,`phone`,`photo`,`place`,`qualification`,`dob`,`gender`,email)VALUES('" + name + "','" + phone + "','" + path + "','" + place + "','" + qualification + "','" + dob + "','" + gender + "','" + email + "')"
    db.insert(qry1)
    return '''<script>alert ("Teachers singup sucessfully");window.location='/'</script>'''


@app.route('/addrhymes')
def add_rhymes():
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
    return render_template("Admin/View Parants.html", data=res)


@app.route('/viewstudents/<id>')
def view_students(id):
    db = Db()
    qry = "SELECT * FROM  student WHERE p_id='" + id + "'"
    res = db.select(qry)
    return render_template("Admin/View Students.html", data=res)


@app.route('/viewteachers')
def view_teachers():
    db = Db()
    qry = "SELECT * FROM teachers "
    res = db.select(qry)
    return render_template("Admin/View Teachers.html", data=res)


@app.route('/deleteteachers/<id>')
def deleteteachers(id):
    db = Db()
    qry = "DELETE FROM teachers WHERE t_id='" + id + "'"
    res = db.delete(qry)
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
    return '''<script>alert ("Puzzle  Inserted Successfully ");window.location='/addimagepuzzle'</script>'''


@app.route('/viewimagepuzzle')
def view_image_puzzle():
    db = Db()
    qry = "SELECT * FROM puzzle"
    res = db.select(qry)
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
            return '''<script>alert ("Image Puzzle  Edited  Successfully ");window.location='/viewimagepuzzle'</script>'''
        else:
            qry = "UPDATE puzzle SET puzzle='" + puzzle + "',TIME='" + time + "' WHERE puz_id='" + puz_id + "'"
            res = db.update(qry)
            return '''<script>alert ("Image Puzzle  Edited  Successfully ");window.location='/viewimagepuzzle'</script>'''
    else:
        qry = "UPDATE puzzle SET puzzle='" + puzzle + "',TIME='" + time + "' WHERE puz_id='" + puz_id + "'"
        res = db.update(qry)
        return '''<script>alert ("Image Puzzle  Edited  Successfully ");window.location='/viewimagepuzzle'</script>'''


# ---------------------------------------PARENT  ------------------------------------

@app.route('/addstudent')
def addstudent():
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
    qry="INSERT INTO student (`name`,`phone`,`age`,`photo`,`gender`,`standered`,p_id)VALUES ('"+name+"','"+phone+"','"+age+"','"+path+"','"+gender+"','"+ standered+"','"+str(session["log_id"])+"')"
    res=db.insert(qry)
    return '''<script>alert ("Student Added Successfully ");window.location='/addstudent'</script>'''

@app.route('/viewstudent')
def viewstudent():
    db=Db()
    qry="SELECT * FROM student WHERE p_id='"+str(session["log_id"])+"' "
    res=db.select(qry)
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
            qry="UPDATE student SET name='"+name+"',phone='"+phone+"',age='"+age+"',photo='"+path+"',standered='"+standered+"' WHERE s_id='"+s_id+"'"
            res=db.update(qry)
        else:
             qry="UPDATE student SET name='"+name+"',phone='"+phone+"',age='"+age+"',standered='"+standered+"' WHERE s_id='"+s_id+"'"
             res=db.update(qry)
    else:
         qry="UPDATE student SET name='"+name+"',phone='"+phone+"',age='"+age+"',standered='"+standered+"' WHERE s_id='"+s_id+"'"
         res=db.update(qry)
    return '''<script>alert ("Student Edited Successfully ");window.location='/viewstudent'</script>'''


# ---------------------------------------TEACHER------------------------------------
@app.route('/viewprofile')
def viewprofile():
    db=Db()
    qry="SELECT * FROM teachers WHERE log_id='"+str(session["log_id"])+"'"
    res=db.selectOne(qry)
    return render_template("Teacher/ViewProfile.html", i=res)




if __name__ == '__main__':
    app.run()