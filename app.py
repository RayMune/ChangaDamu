from flask import Flask, render_template, request, redirect, flash
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from flask import session as flask_session
import os

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database setup
engine = create_engine("sqlite:///blood.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define models
class Donor(Base):
    __tablename__ = 'donors'
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    phone = Column(String(20))
    blood_type = Column(String(5))

class Recipient(Base):
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    hospital = Column(String(100))
    ward = Column(String(50))
    bed_number = Column(String(10))
    blood_type = Column(String(5))

# Create tables on first run
Base.metadata.create_all(engine)

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_type = request.form.get("user_type")

        if user_type == "donor":
            donor = Donor(
                email=request.form.get("donor_email"),
                phone=request.form.get("donor_phone"),
                blood_type=request.form.get("donor_blood_type")
            )
            session.add(donor)
            session.commit()
            flash("Thank you for volunteering to donate blood!")

        elif user_type == "recipient":
            recipient = Recipient(
                name=request.form.get("recipient_name"),
                email=request.form.get("recipient_email"),
                phone=request.form.get("recipient_phone"),
                hospital=request.form.get("hospital"),
                ward=request.form.get("ward"),
                bed_number=request.form.get("bed_number"),
                blood_type=request.form.get("recipient_blood_type")
            )
            session.add(recipient)
            session.commit()
            flash("Your blood request has been submitted!")

        return redirect("/")

    return render_template("index.html")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") 

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            flask_session["admin_logged_in"] = True
        else:
            flash("Incorrect password.")
            return redirect("/admin")

    if not flask_session.get("admin_logged_in"):
        return '''
            <form method="post">
                <input type="password" name="password" placeholder="Admin Password" required>
                <input type="submit" value="Login">
            </form>
        '''

    donors = session.query(Donor).all()
    recipients = session.query(Recipient).all()
    return render_template("admin.html", donors=donors, recipients=recipients)

@app.route("/admin/logout")
def admin_logout():
    flask_session.pop("admin_logged_in", None)
    flash("Logged out successfully.")
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)