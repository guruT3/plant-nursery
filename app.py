from flask import Flask, render_template, request, redirect, url_for,flash
from  forms import AddressForm,LoginForm,SignupForm,CheckoutForm,Feedbackform
from plants import plants
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config["SECRET_KEY"]="8459c311a463d3c4383af37c1eaf7f68"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///stor.db'
db=SQLAlchemy(app)

class Store(db.Model): 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone_number= db.Column(db.String(100), nullable=False)
  password= db.Column(db.String(100), nullable=False)

class Orderplace(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)  
  email = db.Column(db.String(100), nullable=False)
  phone_number = db.Column(db.String(100), nullable=False)
  address = db.Column(db.String(100), nullable=False)
  pincode = db.Column(db.String(100), nullable=False)
  order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
  db.create_all()


@app.route("/")
def home():
  return render_template("home.html",title="Welcome to Flora Botanical") #pheko yahna pe jo phek na hai aur navigation bar banao

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Store.query.filter_by(email=email).first()
        
        if user and user.password == password:
            return redirect(url_for("showproduct"))
        else:
            flash("Invalid login details")
    
    return render_template("login.html", title="LOGIN PAGE", form=form)

@app.route("/signup",methods=["GET","POST"])
def signup():
  form=SignupForm()
  if form.validate_on_submit():
    new_usr=Store(name=form.username.data,email=form.email.data ,password=form.password.data,phone_number=form.phone_number.data,)
    db.session.add(new_usr)
    db.session.commit()
    flash("signup success")
    return redirect(url_for("login"))
  return render_template("signup.html", title="SIGNUP PAGE", form=form)
    

@app.route("/shopnow") #shows all the  list of plants or dictionary
def shopnow():
  return redirect(url_for("login")) #if you want dictonary then use render_template("shopnow.html",plants=plants) import karke details of plant

@app.route("/deliveryinfo",methods=["GET","POST"])
def deliveryinfo(): 
  form=AddressForm()
  plant_id = request.args.get("plant_id")
  if form.validate_on_submit():
    delivery=Orderplace(name=form.name.data,email=form.email.data,phone_number=form.phone_number.data,address=form.address.data,pincode=form.pincode.data)
    db.session.add(delivery)
    db.session.commit()
    return redirect(url_for("payments",plant_id=plant_id))
  return render_template("deliveryinfo.html",title="Delivery Info",form=form,plant_id=plant_id)

    

@app.route("/about")
def knowmore():
  return render_template("about.html",title="ABOUT PAGE") #add about us page here

@app.route("/newarrivals")
def newarrivals():
  return render_template("newarrivals.html",title="NEW ARRIVALS",plants=plants) #add new arrivals here by adding condition that 

@app.route("/offersection")
def offersection():
  return render_template("offersection.html",title="GRAB YOUR PLANT",plants=plants) #add offer section here

#help
@app.route("/help")
def help():
  return render_template("help.html",title="HELP") #add help page here MEANS ADD how to use our web app set wise guide and how to buy a plant where to find the plants

@app.route("/payments", methods=["GET", "POST"])
def payments():
    form = CheckoutForm()
    plant_id = request.args.get("plant_id")
    selected_plant = plants.get(plant_id)

    if form.validate_on_submit():
        return redirect(url_for("ordersuccess"))

    return render_template("payments.html", form=form, plant=selected_plant)


@app.route("/plantcaredetails")
def plantcaredetails():
  return render_template("plantcaredetails.html") #add care page here and FAQS section

@app.route("/ordernow")
def ordernow():
  return redirect(url_for("deliveryinfo")) #set odernow as button

@app.route("/ordersuccess")
def ordersuccess():
  return render_template("ordersuccess.html",title="SUCCESS") #phele sjhow order success then redirect to home page html wale ka kamm hai


@app.route("/contact",methods=["GET","POST"])
def contact():
  form=Feedbackform()
  if form.validate_on_submit():
    return redirect(url_for("feedback"))
  return render_template("contact.html",title="CONTACT us",form=form)


@app.route("/showproduct")
def showproduct():
  return render_template("showproduct.html",title="AVAILABLE PRODUCTS ",plants=plants) 

@app.route("/plant/<plant_id>")
def plant_detail(plant_id):
    plant = plants.get(plant_id)
    if plant:
        return render_template("plant_detail.html", title="DETAILS", plant=plant, plant_key=plant_id)
    else:
        flash("Plant not found.")
        return redirect(url_for("showproduct"))



@app.route("/faqs")
def faqs():
  return render_template("faqs.html",title="FAQS") #add faqs page her



@app.route("/feedback")
def feedback():
   return render_template("feedback.html",title="FEEDBACK") #add feedback page here








@app.route("/wishlist")
def wishlist():
  return render_template("wishlist.html",title="WHITELIST",plants=plants) #add whitelist pag





















if __name__ == "__main__":
  app.run(debug=True)


