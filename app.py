from flask import Flask, jsonify, render_template
from main import (
    predict_this_weeks_games,
    get_current_SEC_overUnder_lines,
    predict_anyWeek_SEC_totalScores,
    get_current_week,
)

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Winner Prediction Page
@app.route("/predict-winners")
def predict_winners():
    winners, matchups = predict_this_weeks_games()
    # Send data to HTML page
    return render_template("predict-winners.html", matchups=zip(matchups, winners))


# OverUnder Prediction Page
@app.route("/overunder")
def over_under():
    current_week = get_current_week()
    overunder_lines = get_current_SEC_overUnder_lines()
    sec_predictions = predict_anyWeek_SEC_totalScores(current_week)

    # predictions = [
    #     (
    #         game,
    #         predicted_score,
    #         over_under_line,
    #         "over" if predicted_score > over_under_line else "under",
    #     )
    #     for game, predicted_score, over_under_line in zip(
    #         sec_predictions.keys(), sec_predictions.values(), overunder_lines.values()
    #     )
    # ]
    predictions = []
    i = 0
    # Remember sec_predictions is a list of tuples in this format: (home_team, away_team, total_score)
    for game in sec_predictions:
        home_team = game[0]
        away_team = game[1]
        total_score = game[2]
        over_under_line = overunder_lines[i][2]
        over_under = "over" if float(total_score) > float(over_under_line) else "under"
        predictions.append(
            (home_team, away_team, total_score, over_under_line, over_under)
        )
        i += 1

    # Send data to HTML page
    return render_template("overunder.html", predictions=predictions)


if __name__ == "__main__":
    app.run(debug=True)
