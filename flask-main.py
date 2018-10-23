from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, ReviewTextForm
from sklearn.externals import joblib

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def home():
    form = ReviewTextForm()
    if form.validate_on_submit():
        if form.reviewText.data == 'Good':
            flash('Your sentiment is positive!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Your sentiment is negative', 'warning')
    return render_template('home.html', posts=posts, form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/comment", methods=['GET', 'POST'])
def comment():
    form = ReviewTextForm()
    if form.validate_on_submit():
        print(form.reviewText.data)
        newVector = joblib.load('classfical-vectorizer.joblib')
        newModel = joblib.load('classical-model.joblib')
        myVectortest = newVector.transform([form.reviewText.data])
        joblibPrectict = newModel.predict(myVectortest)
        print(joblibPrectict)
        for index, feedback in enumerate(joblibPrectict):
            if feedback == 1:
                flash('Your sentiment is positive!', 'success')
                # return redirect(url_for('comment'))
            else:
                flash('Your sentiment is negative', 'warning')
    return render_template('home.html', title='Comment', form=form)


if __name__ == '__main__':
    app.run(debug=True)