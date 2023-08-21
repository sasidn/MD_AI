# Importing Libraries
import re
from nltk.corpus import wordnet
import itertools

# List of Keywords
list_words = [
    'hello', 'bye',
    'suicide', 'kill', 'die', 'want', 'feel',
    'stupid', 'dumb', 'asshole',
    'think', 'was', 'thought', 'thinking'
]

# Dictionary to store synonyms for each keyword
list_syn = {}

# Loop through the list of keywords and find synonyms using WordNet
for word in list_words:
    synonyms = []
    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            # Remove special characters and add synonym to the list
            lem_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', lem.name())
            synonyms.append(lem_name)
    list_syn[word] = set(synonyms)


# List of synonyms for each intent
greetings_synonyms = list(list_syn['hello']) + ['hey']
goodbyes_synonyms = list(list_syn['bye'])
insult_synonyms = list(list_syn['stupid']) + list(list_syn['dumb']) + list(list_syn['asshole'])
suicide_synonyms = list(list_syn['suicide']) + list(list_syn['kill']) + list(list_syn['die'])
automaticThought_synonyms = list(list_syn['think']) + list(list_syn['was']) + list(list_syn['thought']) + list(list_syn['thinking'])

# Dictionary to store keywords and their synonyms
list_keywords = {
    'greetings': greetings_synonyms,
    'goodbyes': goodbyes_synonyms,
    'insult': insult_synonyms,
    'suicide': suicide_synonyms,
    'automaticThought': automaticThought_synonyms
}


# Dictionary to store compiled regular expression patterns for each intent
keywords_dict = {}
for keyword in list_keywords:
    keywords_dict[keyword] = []
    # Generate compiled regex patterns for each synonym
    for synonym in list(list_keywords[keyword]):
        pattern = re.compile('.*\\b' + synonym + '\\b.*')
        keywords_dict[keyword].append(pattern)

# Dictionary to store responses for each intent
responses = {
    'greetings': 'Hello! So, tell me how have you been feeling?',
    'suicide': 'If you are feeling vulnerable and need help, Please call 112 or 914 590 055 to seek help.',
    'goodbyes': 'Bye. Hope I\'ve been helpful.',
    'insult': 'Oh! that\'s mean :(',
    'automaticThought': 'When you were in that situation and that thought came to you, how did you feel?'
}

# Function to get the appropriate response based on user input
def get_response(msg):
    print("User Input:", msg)
    matched_intent = None
    # Search for keywords in user input
    for intent, patterns in keywords_dict.items():
        for pattern in patterns:
            if pattern.search(msg):
                print(f"Matched Intent: {intent}")
                matched_intent = intent
                break
        if matched_intent:
            break

    # Return the corresponding response if intent is matched
    if matched_intent in responses:
        response = responses[matched_intent]
        print("Bot Response:", response)
        return response
    return 'none'  # If no intent is matched



# Main code
user_input = input('You: ')  # Get user input
response = get_response(user_input)  # Get the chatbot's response
print('Bot:', response)  # Print the response
