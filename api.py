from flask import Flask, jsonify
import datetime

app = Flask(__name__)

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def parse_pace(pace_str):
    try:
        pace = datetime.datetime.strptime(pace_str, '%M:%S')
        return (pace.minute, pace.second)
    except ValueError:
        raise APIException("Invalid pace format, expected MM:SS", status_code=400)

def split_times(pace, distance=42.195):
    (pace_min, pace_sec) = parse_pace(pace)
    splits = []
    for i in range(1, 43):
        split_min = pace_min * i
        split_sec = pace_sec * i
        split_min += split_sec // 60
        split_sec = split_sec % 60
        splits.append((i, split_min, split_sec))
    return splits

@app.route("/api/calculate/<string:pace>")
def calculate(pace):
    try:
        splits = split_times(pace)
        return jsonify(splits), 200
    except APIException as e:
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
        return response

if __name__ == "__main__":
    app.run(debug=True)
