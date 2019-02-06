from flask import Flask,jsonify
from flask_restful import Resource, Api
app = Flask(__name__)

sentiments = [
    {
        'customer': 'member',
        'devicetype': 'MobileApp',
        'text': 'I ALWAYS HAVE TROUBLE PAYING MY BILL',
        'date_posted': 'April 20, 2018',
        'rating': 0
    },
    {
        'customer': 'member',
        'devicetype': 'website',
        'text': 'CANNOT MAKE PAYMENT. APP IS ALWAYS DOWN.',
        'date_posted': 'April 20, 2018',
        'rating': 3
    }
]

@app.route("/sentiments")
def get_books():
    return jsonify({'books': sentiments})

@app.route('/sentiments/<int:rating>')
def get_sentimentby_rating(rating):
    return_value = {}
    for sentiment in sentiments:
        if sentiment["rating"] == rating:
            return_value = {
                'customer': sentiment["customer"],
                'devicetype': sentiment["devicetype"],
                'text': sentiment["text"]
            }
    return jsonify(return_value)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
