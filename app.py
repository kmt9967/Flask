#------------------Imports--------------------------------------
#pip install flask
from flask import Flask, render_template , request 
from wtforms import StringField, TextAreaField,PasswordField,validators 
#pip install flask_mysqldb
from flask_mysqldb import MySQL
#-------------------Declares--------------------------------------

app = Flask(__name__)
#-------------------Sql Configurations--------------------------------------

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="ecomm"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

db= MySQL(app)
#-------------------Class--------------------------------------
#pip install wtforms
# pip install passlib 
class Register():
    fullname= StringField("fullname" , [validators.Length(min=3 , max=50)])
    email= StringField("email" , [ validators.Length(min=6 , max=50 )])
    password= PasswordField("pass" , [validators.Length(min=8 , max=12) ,
    validators.DataRequired(), 
    validators.EqualTo("confirm" , message="The Password is not Match")])
    confirm = PasswordField("confirm")


#-------------------Routing--------------------------------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/products')
def products():
    cur= db.connect.cursor()
    run= cur.execute("SELECT * FROM `products`")
    data= cur.fetchall() 
    if (run>0):
        return render_template("products.html" , products=data)
    else:
        msg="Products Not Found"
        return render_template("products.html" , msg=msg)

@app.route('/single_p/<id>')
def s_product(id):
    cur= db.connect.cursor()
    run= cur.execute("SELECT * FROM `products` Where id = %s",[id])
    data= cur.fetchone()
    if (run>0):
        return render_template("s_product.html" , s_prod=data)
    else:
        msg="Products Not Found"
        return render_template("s_product.html" , msg=msg)

@app.route('/register' , methods=['GET' , 'POST'])
def register():
    if request.method=="POST":
        return request.form
    return render_template("register.html")

#-------------------Main--------------------------------------

if __name__=="__main__":
    app.run(debug="true", port= 3000 )