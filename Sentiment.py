import mysql.connector
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DATABASE

def get_sentiments(username):
    db = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cursor = db.cursor()

    sentiment_model_name = "finiteautomata/bertweet-base-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

    #delete_sql = "TRUNCATE TABLE MoodTracker"
    #delete_sql = "DELETE FROM MoodTracker WHERE username = %s"
    #cursor.execute(delete_sql, (username,))
    #db.commit()

    # Retrieve chat messages from the "messages" table
    select_messages_sql = "SELECT user_response, message_id, IFNULL(chat_id,1), date, username FROM messages WHERE username = %s"
    cursor.execute(select_messages_sql, (username,))
    messages = cursor.fetchall()

    sentiments = []

    # Process each chat user response and get its sentiment
    for message in messages:
        user_input = message[0]
        message_id = message[1]
        chat_id = message[2]
        tracking_date = message[3]
        username = message[4]

        input_ids = tokenizer.encode(user_input, return_tensors="pt")
        logits = sentiment_model(input_ids).logits
        sentiment = logits.argmax().item()
        sentiments.append(sentiment)

        # Insert sentiment, message_id, tracking_date, and username into Mood_Tracker table
        insert_mood_tracker_sql = "INSERT INTO MoodTracker (tracking_date, sentiment, message_id, username,chat_id) VALUES (%s, %s, %s, %s,%s)"
        mood_tracker_values = (tracking_date, sentiment, message_id, username,chat_id)
        cursor.execute(insert_mood_tracker_sql, mood_tracker_values)

    db.commit()
    cursor.close()
    db.close()

    return sentiments


