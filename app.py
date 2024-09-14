from flask import Flask, jsonify, render_template
from main import predict_this_weeks_games, get_current_SEC_overUnder_lines, predict_anyWeek_SEC_totalScores

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Winner Prediction Page
@app.route('/predict-winners')
def predict_winners():
    winners, matchups = predict_this_weeks_games()
    return jsonify({'winners': winners, 'matchups': matchups})

# OverUnder Prediction Page
@app.route('/overunder')
def overunder():
    overUnder_lines = get_current_SEC_overUnder_lines()
    predicted_scores = predict_anyWeek_SEC_totalScores(3)  # You can modify the week as needed
    return jsonify({
        'over_under_lines': overUnder_lines,
        'predicted_scores': predicted_scores
    })

if __name__ == '__main__':
    app.run(debug=True)
