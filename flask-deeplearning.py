from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, ReviewTextForm
from sklearn.externals import joblib
from keras import backend as K

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



@app.route("/deeplearning", methods=['GET', 'POST'])
def deeplearning():
    form = ReviewTextForm()
    if form.validate_on_submit():
        print(form.reviewText.data)
        newVector = joblib.load('deeplearning-vectorizer-nongram.joblib')
        newModel = joblib.load('deeplearning-model-nongram.joblib')
        myVectortest = newVector.transform([form.reviewText.data])
        actualPredict = newModel.predict(myVectortest)
        feedback = (actualPredict > 0.5)
        if feedback:
            flash('Your sentiment is positive!', 'success')
            K.clear_session()
        else:
            flash('Your sentiment is negative', 'warning')
            K.clear_session()
    K.clear_session()
    return render_template('home.html', title='Comment', form=form)

@app.route("/classical", methods=['GET', 'POST'])
def classical():
    form = ReviewTextForm()
    if form.validate_on_submit():
        print(form.reviewText.data)
        newVector = joblib.load('classical-vectorizer-nongram.joblib')
        newModel = joblib.load('classical-model-nongram.joblib')
        myVectortest = newVector.transform([form.reviewText.data])
        feedback = newModel.predict(myVectortest)
        print("Actual predict from classical", feedback)

        if feedback == 1:
            flash('Your feedback is positive!', 'success')

        else:
            flash('Your feedback is negative', 'warning')

    return render_template('classicalhome.html', title='classical', form=form)



if __name__ == '__main__':
    app.run(debug=True)