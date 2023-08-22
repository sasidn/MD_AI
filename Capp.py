from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="MindNex",
        password="MindNex",
        database="MindNex"
    )
    print("Connected to MySQL database")
except mysql.connector.Error as err:
    print("Error connecting to MySQL database:", err)
    conn = None

mycursor = conn.cursor()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/recommendation.html')
def recommended_articles():
    mycursor.execute("SELECT * FROM recommended_articles")
    recommended_articles_data = mycursor.fetchall()

    mycursor.execute("SELECT * FROM recommended_videos")
    recommended_videos_data = mycursor.fetchall()

    return render_template(
        'recommendation.html',
        recommended_articles=recommended_articles_data,
        recommended_videos=recommended_videos_data
    )
if __name__ == "__main__":
    app.run(debug=True)
