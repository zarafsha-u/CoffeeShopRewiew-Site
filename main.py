from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms import AddCafe

app = Flask(__name__)
Bootstrap(app)
app.secret_key = '123'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe_.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique= True, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    wifi = db.Column(db.String(80), nullable=False)
    coffee_price= db.Column(db.String(10), nullable=False)
    environment= db.Column(db.String(10), nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)

# db.create_all()


@app.route("/")
def home():
    cafe = db.session.query(Cafe).all()
    return render_template('home_page.html', cafes= cafe)

@app.route('/search', methods=['GET', 'POST'])
def cafe_by_location():
    if request.method == "POST":
        search = request.form.get('input')
        cafes = db.session.query(Cafe).all()
        if len(search) == 2:
            state = search.upper()
            cafes_in_state =[cafe for cafe in cafes if state in cafe.location]
            if len(cafes_in_state) >= 1:
                length_enough = True
            if len(cafes_in_state) == 0 :
                length_enough = False
            return render_template('search.html', state = cafes_in_state, length_1 = length_enough)
        else:
            city_or_name = search.title()
            cafe_by_city_or_name = [cafe for cafe in cafes if city_or_name in cafe.name or city_or_name in cafe.location]
            if len(cafe_by_city_or_name) >= 1:
                length_enough = True
            if len(cafe_by_city_or_name) == 0:
                length_enough = False
            return render_template('search.html', other = cafe_by_city_or_name, length_2= length_enough)

    return render_template('search.html')


@app.route('/add-cafe', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafe()
    cafes = db.session.query(Cafe).all()
    if form.validate_on_submit():
        name = (form.name.data).title()
        location = form.name.data
        wifi = form.wifi.data
        price = form.coffee_price.data
        env= form.environment.data
        rating = form.overall_rating.data
        cafe_list = [cafe.name for cafe in cafes]
        if name in cafe_list:
            return render_template('result.html', already_added= True)
        else:
            new_cafe = Cafe(name= name, location = location, wifi= wifi, coffee_price=price, environment=env, overall_rating=rating )
            db.session.add(new_cafe)
            db.session.commit()
            return render_template('result.html', already_added=False)
    return render_template('add-cafe.html', form = form)



if __name__ == '__main__':
    app.run(debug=True)

