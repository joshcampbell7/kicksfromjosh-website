
from itertools import product
from os import error
from flask import Flask,render_template,url_for,request,session

import sqlite3

from werkzeug.utils import redirect


app = Flask(__name__)
app.config["SECRET_KEY"] = "joshua"


def getLoginDetails():
    if "Email" not in session:
        LoggedIn = False
        UserID = ""
        noOfItems = 0
    
    else:
        LoggedIn = True
        Email = session["Email"]
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT ID FROM Users WHERE Email = ?",(Email,))
        UserID = c.fetchone()[0]
        
        c.execute("SELECT COUNT (ProductID) FROM Cart WHERE UserID = ?",(str(UserID)))
        noOfItems = c.fetchone()[0]
        c.close()

    return(LoggedIn,noOfItems,UserID)


@app.route("/home", methods=["GET","POST"])
def index():
    
    
    return render_template("home.html")

@app.route("/products",methods=['GET', 'POST'])
def root():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    rows = c.execute("SELECT * FROM Products")


    return render_template("products.html" ,data=rows)

@app.route("/productitem/<Productid>",methods=['GET', 'POST'])
def Productitems(Productid):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    rows = c.execute("SELECT * FROM Products WHERE ID = ?",(Productid))

    return render_template("item_page.html",data = rows)


@app.route("/addcart" , methods = ["GET","POST"])
def add_to_cart():
    if "Email" not in session:
        return redirect(url_for(loginform))
    else:
        with sqlite3.connect("data.db") as conn:
            Size = request.form.get("size")
            ProductID = request.form.get("ProductID")
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            c.execute("SELECT ID FROM Users WHERE Email = '" + session['Email'] + "'")
            UserID = c.fetchone()[0]
            c.execute("INSERT INTO Cart(UserID,ProductID,Size) values(?,?,?)",(UserID, ProductID, Size))
            conn.commit()
            return redirect(url_for("viewcart"))
        
            
@app.route("/viewcart")
def viewcart():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT ID FROM Users WHERE Email = '" + session['Email'] + "'")
    UserID = c.fetchone()[0]
    c.execute("SELECT Products.Name , Products.Price , Products.Image , Cart.Size FROM Products,Cart WHERE Products.ID == Cart.ProductID AND Cart.UserID == ?",(str(UserID)))
    products = c.fetchall()

        
    return render_template("cart.html",products = products)

@app.route("/loginform" , methods = ["GET","POST"])
def loginform():

    return render_template("login.html",error = " ")


@app.route("/login",methods = ["GET","POST"])
def login():
    Email = request.form["Email"]
    Password = request.form["Password"]

    if isValid(Email,Password) == True:
        session['Email'] = Email
        return redirect(url_for("root"))
    
    else:
        error = "Invalid email or password try again"
        return render_template("login.html",error=error)

def isValid(email,password):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Users")
    data = c.fetchall()
    for row in data:
        if row[1] == email and row[2] == password:
            return True
            
    return False
              
@app.route("/signup",methods = ["GET","POST"])
def signup():
    Email = request.form["Email"]
    Password = request.form["Password"]

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("INSERT INTO Users (Email,Password) values(?,?)",(Email,Password))
    conn.commit()
    conn.close()
        
    return render_template("login.html")

@app.route("/registerform")
def registerform() :
    return render_template("signup.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return("confirmation.html")


@app.route("/logout",methods= ["GET","POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)