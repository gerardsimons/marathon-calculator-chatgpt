from flask import Flask, request, render_template

app = Flask(__name__)

def split_time(pace: str) -> list:
    hours, minutes, seconds = map(int, pace.split(":"))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    split_times = [(i+1, "{:02d}:{:02d}:{:02d}".format(i * total_seconds // 3600,
                                                        i * total_seconds // 60 % 60,
                                                        i * total_seconds % 60)) for i in range(26)]
    return split_times

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pace = request.form.get("pace")
        if pace:
            split_times = split_time(pace)
            return render_template("index.html", split_times=split_times)
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()
