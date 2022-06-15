from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('Hackeriskunal1@')
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://dtsugfnitsprzh:ee38463eb1e518aea9bb97c434350608abdc0879191f83e3bd7dcad6e71ace1d@ec2-34-198-186-145.compute-1.amazonaws.com:5432/d4313pslkaneut"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# create db Model
class Cafes(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    banner_img_url = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    productivity = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    open = db.Column(db.String(25), nullable=False)
    close = db.Column(db.String(25), nullable=False)


class Contacts(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

db.create_all()

@app.route("/add", methods=["POST", "GET"])
def post_new_cafe():
    if request.method == "POST":
        name = request.form.get("cafe_name")
        map_url = request.form.get("map_url")
        img_url = request.form.get("image_url")
        banner_img_url = request.form.get("banner_img_url")
        phone = request.form.get("phone")
        productivity = request.form.get("productivity")
        seats = request.form.get("seat")
        description = request.form.get("description")
        address = request.form.get("address")
        opening = request.form.get("opening-time")
        timing = request.form.get("closing-time")
        full_date = datetime.now()
        date = full_date.strftime("%d %b")
        entry = Cafes(
            cafe_name=name,
            map_url=map_url,
            image_url=img_url,
            banner_img_url=banner_img_url,
            phone=phone,
            productivity=productivity,
            date=date,
            seats=seats,
            description=description,
            address=address,
            open=opening,
            close=timing
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("places"))
    return render_template("add.html")


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = Cafes.query.get(post_id)
    return render_template("show_post.html", post=requested_post)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/places")
def places():
    posts = Cafes.query.all()
    return render_template("places.html", posts=posts)


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("msg")
        entry = Contacts(
            name=name,
            email=email,
            date=datetime.now(),
            phone_num=phone,
            msg=message,
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("contact.html")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = Cafes.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)

