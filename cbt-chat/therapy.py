import random

# Define list of negative thought patterns
negative_thoughts = [
    'All-or-nothing thinking',
    'Overgeneralization',
    'Mental filtering',
    'Discounting the positive',
    'Jumping to conclusions',
    'Magnification and minimization',
    'Emotional reasoning',
    'Should statements',
    'Labeling and mislabeling',
    'Personalization'
]

# Define a list of positive thought patterns
positive_thoughts = [
    'Balanced thinking',
    'Evidence gathering',
    'Identifying exceptions',
    'Thinking in shades of grey',
    'Mindfulness',
    'Gratitude',
    'Self-compassion',
    'Relaxation',
    'Assertiveness',
    'Problem-solving'
]

# Define a function that prompts the user to describe a negative event and uses CBT techniques to help them reframe their thoughts
def cbt_prompt():
    print('Think of a negative event that happened recently. Describe it briefly:')
    event_description = input()
    print('Which of the following negative thought patterns do you think you might be using?')
    for i, thought in enumerate(negative_thoughts):
        print('{}) {}'.format(i + 1, thought))
    thought_index = int(input()) - 1
    thought_description = negative_thoughts[thought_index]
    positive_thought_description = positive_thoughts[thought_index]
    print('Okay, it sounds like you might be using {}.'.format(thought_description))
    print('Let\'s try to reframe your thoughts to be more positive.')
    print('What is a more balanced way of thinking about this situation?')
    balanced_thought = input()
    print('That\'s a great way of thinking about it! Here is a positive thought to replace the negative one:')
    print('{}'.format(positive_thought_description))
    print('{}'.format(balanced_thought))

# Start the conversation
print('Welcome to the CBTBot. Type something to begin...')

while True:
    try:
        user_input = input()

        # If the user types "help", prompt them to describe a negative event and use CBT techniques to help them reframe their thoughts
        if user_input.lower() == 'help':
            cbt_prompt()

        # If the user's message does not contain the keyword "help", generate a random response
        else:
            bot_responses = [
                "I see. Tell me more about that.",
                "How does that make you feel?",
                "What do you think about the situation?",
                "Do you have any other thoughts on this?"
            ]
            bot_response = random.choice(bot_responses)
            print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError):
        break
