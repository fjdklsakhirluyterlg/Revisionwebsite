from enum import unique
from flask import Flask, render_template, url_for, request, redirect, send_from_directory, send_file, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import smtplib
import ssl
from email.message import EmailMessage
from itertools import permutations
from sqlalchemy.sql import text
import os
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

db.create_all()

class Emaillist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emailadd = db.Column(db.String(1000), unique=True)
    complete = db.Column(db.Boolean)

db.create_all()

def fib(num): 
    result = []
    count = 0
    n1 = 0
    n2 = 1
    while count < int(num):
       result.append(n1)
       nth = n1 + n2
       n1 = n2
       n2 = nth
       count += 1
    return result

def collatz(num):
    return num

def send_email(address):
    sender_email = "drive.banerjee.armaan@gmail.com"
    receiver_email = address
    password = "ixsrblyncyrupttv"
    message = EmailMessage()
    subject = "HI there"
    body = f"Hello there, you have been emailed from me, your email adress is {address}"
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    html = f"""
    <html>
        <body>
            <h1>{subject}</h1>
            <br>
            <p>{body}</p>
        </body>
    </html>
    """

    message.add_alternative(html, subtype="html")

    context = ssl.create_default_context()

    print("Sending Email!")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Success")

def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False

def coefficient(x,y):
    x_1 = x[0]
    x_2 = x[1]
    x_3 = x[2]
    y_1 = y[0]
    y_2 = y[1]
    y_3 = y[2]

    a = y_1/((x_1-x_2)*(x_1-x_3)) + y_2/((x_2-x_1)*(x_2-x_3)) + y_3/((x_3-x_1)*(x_3-x_2))

    b = (-y_1*(x_2+x_3)/((x_1-x_2)*(x_1-x_3))
         -y_2*(x_1+x_3)/((x_2-x_1)*(x_2-x_3))
         -y_3*(x_1+x_2)/((x_3-x_1)*(x_3-x_2)))

    c = (y_1*x_2*x_3/((x_1-x_2)*(x_1-x_3))
        +y_2*x_1*x_3/((x_2-x_1)*(x_2-x_3))
        +y_3*x_1*x_2/((x_3-x_1)*(x_3-x_2)))

    return a,b,c

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/bitcoin')
def get_bitcoin():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()

    x = data["bpi"]["GBP"]["rate"]
    return f"<p>The bitcoin price is {x}</p>"

@app.route('/tfl')
def get_tfl():
    def is_tube_on():
        liste = ["District", "Central", "Circle", "Piccadilly", "Bakerloo", "Hammersmith-City", "Jubilee", "Metropolitan", "Victoria", "Northern"]
        bad = []
        status_bad = []
        r = []

        for line in liste:
            reply = requests.get("https://api.tfl.gov.uk/Line/" + line + "/Status")

            data = reply.json()

            Status = (data[0]["lineStatuses"][0]["statusSeverityDescription"])

            if Status != "Good Service":
                bad.append(line)
                status_bad.append(Status)
        
        for l in bad:
            response = requests.get(f"https://api.tfl.gov.uk/Line/{l}/Status")

            d = response.json()

            reason = (d[0]["lineStatuses"][0]["reason"])
            r.append(reason)
        
        return r
    
    return f"<p>The following are problematic: {is_tube_on()}</p>"

@app.route('/physics')
def physics():
    return '<h1> Physics</h1> <p style="text-align:center"> Welcome to the physics homepage, here you can learn about physics</p>'

@app.route('/longitudinal-waves-and-transverse-waves')
def explain_waves():
    x = "<p> A longitudinal wave is when the osicalltions are parralel to the wave motion</p><p>A transverse wave is when the osciallations are perpendicular to the wave motion<p>"
    di = "<div style='background-color: #5c32a8'><p> A longitudinal wave is faster than a transverse wave, this is because there is less firction</p><p> A longitudinal wave can also travel in solids, liquids and gasses because it does not depend on the shear strength of the medium it is travelling in, if that medium is like a liquid then ti does not have enough shear strength to support the oscillations, and so transverse waves cannot travel in liquids or gasses</p><p> However, longitudinal waves cannot travel throguh vacuums because there is no particles to bump into each other</p></div>"
    return f"{x}{di}"

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/testphp')
def test_php():
    return render_template('testphp.html')

@app.route("/<name>")
def user(name):
    if is_integer_num(name):
        return f"Your int squared = {name**2}"
    else:
        return render_template('name.html', content=f"{name}")

@app.route('/loops')
def loops():
    return render_template('anothertest.html')

@app.route('/snake')
@app.route('/snakegame.html')
def snake():
    return render_template('snakegame.html')

@app.route('/505')
def error():
    return "You stupid bugger, go fix this now"

@app.route('/resonance')
def resonance():
    return render_template('resonance.html')

@app.route('/math/square/<number>')
def square(number):
    try:
        return f"Your number squared is {float(number)**2}"
    except Exception as e:
        return e

@app.route('/math/add/<number>')
def add_num(number):
    try:
        x = [x for x in number]
        return sum(x)
    except:
        return f"Cannot calculate {number} please make it a list"

@app.route('/math/quadfinder/<lofquadpoints>')
def findthisquadeq(lofquadpoints):
    try:
        x = lofquadpoints[:2]
        y = lofquadpoints[3:]
        z = coefficient(x, y)
        aa = z[0]
        bb = z[1]
        cc = z[2]
        return f"{aa}x^2 + {bb}x + {cc}"
    except:
        return "Could not compute"

@app.route('/math/factorial/<number>')
def factorial(number):
    try:
        x = 1
        for i in int(number):
            x = x*i
        return x
    except:
        return "You must try with an integer"  

@app.route('/chemistry/periodic-table')
def periodic_table():
    return render_template("periodictable.html")

#@app.route("/admin/login", methods=["POST", "GET"])
#def login():
    #if request.method == "POST":
        #user = request.form["nm"]
        #return redirect(url_for("admin/user", usr=user))

#@app.route("/admin/<usr>")
#def user(usr):
    #return f"<h1>{usr}</h1>"

@app.route('/minesweeper')
def minesweeper():
    return render_template('minesweeper.html')

@app.get('/todo')
def show_todo():
    todo_list = db.session.query(Todo).all()
    return render_template("todo.html", todo_list=todo_list)

@app.post("/todo/add")
def todo_add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("show_todo"))

@app.get("/todo/update/<int:todo_id>")
def update(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("show_todo"))

@app.get("/todo/delete/<int:todo_id>")
def delete(todo_id):
    # todo = Todo.query.filter_by(id=todo_id).first()
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("show_todo"))

@app.route('/newsletter')
def show_emails():
    emails = db.session.query(Emaillist.emailadd).all()
    return render_template("newsletter.html", msg=emails)

@app.route("/newsletter/add", methods=["POST", "GET"])
def add_newsletter():
    try:
        if request.method == "POST":
            emails = db.session.query(Emaillist.emailadd).all()
            emailx = request.form.get("newsletter")
            if emailx in emails:
                flash("Already subscribed!", category="error")
            else:
                new_email = Emaillist(emailadd=str(emailx), complete=False)
                db.session.add(new_email)
                db.session.commit()
                return redirect(url_for("show_emails"))
        else:
            return "What?"
    except Exception as e:
        return f"Could not be carried out because {e}" 

@app.route('/history')
def history():
    return "Coming soon!"

@app.route('/emailer', methods=["POST", "GET"])
def emailer():
    if request.method == "POST":
        try:
            Email = request.form["Email"]
            send_email(Email)
            return "Sent the email successfully"
        except:
            return f"Did not work properly, are you sure you meant to send it to {Email}"
    else:
        return render_template('emailer.html')
        
@app.route('/math/fibonacci', methods=["POST", "GET"])
def fibonnaci():
    if request.method == "POST":
        x = request.form["Fibnum"]
        y = fib(x)
        return render_template('fibonacci.html', fibnums=y)
    else:
        return render_template('fibonacci.html')

@app.route('/math/permutate', methods=["POST", "GET"])
def permutate():
    if request.method == "POST":
        y = request.form["permutations"]
        haha = list(permutations(y))
        return render_template("permutations.html", permutations=haha, len=len(haha))
    else:
        return render_template('permutations.html')

@app.route('/math/permutate/unique', methods=["POST", "GET"])
def unique_permutate():
    if request.method == "POST":
        li = []
        y = request.form["permutations"]
        haha = list(permutations(y))
        for perm in haha:
            if perm in li:
                pass
            else:
                li.append(perm[::-1])
        
        return render_template("permutations.html", permutations=li, len=len(li))
    else:
        return render_template('permutations.html')

# @app.route("/files/get")
# def send_randomfile():
#         x = os.listdir("/Users/mohuasen/prev/all/Armaan/PDFS")
#         file = random.choice(x)
#         try:
#             return send_file(file)
        # except Exception as e:
            # return e

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)