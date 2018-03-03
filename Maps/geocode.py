import logging

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# api-endpoint
url = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyA_wOxjHNfPhmKu2zBo8N5HXsEpewgIQF0"


# [START form]
@app.route('/')
def index():
    return render_template('form.html')


# [END form]

# [START result]
@app.route('/result', methods=['POST', 'GET'])
def api_message():
    locate = request.form.get('location', None)
    payload = {'address': locate}

    response = requests.get(url=url, params=payload)
    data = response.json()

    if data['status'] != 'OK':
        print "Error"
        error = "Search came up with no results. Try Again."

        return render_template(
            'result.html',
            passed="no",
            message=error
        )

    else:
        id = data['results'][0]["place_id"]
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']

        return render_template(
            'result.html',
            passed="yes",
            id=id,
            latitude=latitude,
            longitude=longitude
        )


# [END result]

if __name__ == '__main__':
    app.run(debug=True)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
