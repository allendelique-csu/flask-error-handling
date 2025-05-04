from flask import Flask, render_template
import requests, logging

app = Flask(__name__)

# Custom error handler for 404 Not Found
@app.route("/pastComic/<comicNum>")
def pastComic(comicNum):
    # Log the error
    try:
        logging.debug(f"Fetching comic number: {comicNum}")
        if not comicNum.isdigit():
            raise ValueError(f"Comic number must be a digit. Received: '{comicNum}'")
        elif int(comicNum) > 3000:
            raise ValueError(f"Comic number must be less than 3001. Received: '{comicNum}'")
        # Fetch the comic data from the API
        URL = f"https://xkcd.com/{comicNum}/info.0.json"
        response = requests.get(URL)
        if(response.status_code != 200):
            raise ValueError("Error connecting to XKCD API")
        data = response.json()
        return render_template("pastComic.html", data=data)
    except ValueError as e:
        # Log the error
        logging.error(f"Invalid comic number: {comicNum} - {e}")
        # If the comic number is not a digit, return a 404 error
        return render_template("not_found.html", errorMsg=e)
    except Exception as e:
        print(e)
        # Log the error
        logging.error(f"Error fetching comic number {comicNum}: {e}")
        # If the comic number is not found, return a 404 error
        return render_template("not_found.html", errorMsg=e)

@app.route('/')
def home():
    try:
        # Fetch the comic data from the API
        URL = "https://xkcd.com/info.0.json"
        response = requests.get(URL)
        if(response.status_code != 200):
            raise ValueError("Error connecting to XKCD API")
        data = response.json()
        return render_template("index.html")
    except ValueError as e:
        # Log the error
        logging.error(f"Error with home: {e}")
        # If the comic number is not found, return a 404 error
        return render_template("not_found.html", errorMsg=e)
    

if __name__ == '__main__':
    app.run(debug=True)