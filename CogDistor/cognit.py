import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle
import CBTbot

bot_name = "Nexbot"
script_answers = [
    "I’m sorry that you feel this way. Did anything in particular trigger this feeling?\
    \nPlease provide a detailed explanation of the situation.",
    "What were you thinking at the time?",
    "Please, Rate how intense this feeling was (1-100), where 1 represents the least intensity and 100 represents the highest intensity.",
    "What has happened to make you believe the thought is true?",
    "What evidence is there that this thought is not true?",
    "Taking the information into account, is there an alternative way of thinking about the situation? Please give an example",
    "How would you rate your mood now? (1-100) where 1 represents the least intensity and 100 represents the highest intensity.",
]

# List of the cognitive distortions
CD = {
    'Always Being Right'        : 'DEFINITION: This way of thinking is characterized by a strong need or need to be right or to have other\
                                people affirm one\'s beliefs, opinions, or actions. It might make it difficult to consider different\
                                perspectives or to admit mistakes, which can pose problems in relationships and communication.\
                                \nLINK WITH TIPS:\nhttps://www.therapynowsf.com/blog/always-being-right-gearing-up-for-intellectual-battle',
    'Blaming'                   : 'DEFINITION: Attributing negative occurrences or events to someone or something else instead of accepting\
                                responsibility or taking into account the impact of one\'s own actions or beliefs is the cognitive distortion\
                                known as "blaming." Blaming can result in negative behaviors and emotions including rage, resentment, and avoidance.\
                                \nLINK WITH TIPS: \nhttps://www.vacounseling.com/blaming-cognitive-distortion/',
    'Catastrophizing'           :'DEFINITION: Predicting a negative outcome and jumping to the conclusion that if the negative outcome did\
                                in fact happen, it would be a catastrophe.\
                                \nLINK WITH TIPS: \nhttps://positivepsychology.com/catastrophizing/',
    'Control Fallacies'         : 'DEFINITION: The fallacy of control occurs when you believe you have too much power over a circumstance\
                                or your lot in life.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/control-fallacies-delving-deeper-into-cognitive-distortions',
    'Emotional Reasoning'       : 'DEFINITION: When a person uses emotional reasoning, a cognitive distortion, they come to the\
                                conclusion that something\ is true regardless of the available evidence. Your thoughts are obscured\
                                by your emotions, and your reality is similarly obscured.\
                                \nLINK WITH TIPS: \nhttps://theeverygirl.com/17-of-the-easiest-ways-to-get-healthier-now/',
    'Fallacy Of Change'         : 'DEFINITION: This mental fallacy assumes that people ought to adapt to fit their own interests.\
                                The person will exert pressure on others to alter their behavior because they believe doing so\
                                will make them happier. They are convinced that changing a person is necessary for happiness.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/the-fallacy-of-change-and-the-pursuit-of-happiness',
    'Fallacy Of Fairness'       : 'DEFINITION: The idea that fairness and equality should be the foundation of everything in life\
                                is known as the Fallacy of Fairness.\
                                \nhttps://www.therapynowsf.com/blog/the-fallacy-of-fairness-an-overview-of-this-cognitive-distortion',
    'Filtering'                 : 'DEFINITION: When we keep just the negative memories and the negative feelings associated with them,\
                                mental filtering takes place and we reject the positive recollections.\
                                \nLINK WITH TIPS: \nhttps://www.vacounseling.com/mental-filtering-cognitive-distortion/',
    'Global Labelling'          : 'DEFINITION: Labeling is a cognitive distortion in which we extrapolate from a single\
                                attribute of a person to that person as a whole.\
                                \nLINK WITH TIPS: \nhttps://courageousandmindful.com/overcoming-labeling-and-mislabeling-a-cognitive-distortion/',
    'Heaven\'s Reward Fallacy'  : 'DEFINITION: The distortion known as Heaven\'s Reward Fallacy is founded on the justification that your rewards\
                                should be determined by how hard you work.\
                                \nLINK WITH TIPS: \nhttps://cognitiontoday.com/heavens-reward-fallacy/',
    'Jumping to Conclusions'    : 'DEFINITION: Making arbitrary, negative assumptions about the thoughts of others or the future.\
                                \nLINK WITH TIPS: \
                                \nhttps://www.therapynowsf.com/blog/jumping-to-conclusions-learn-how-to-stop-making-anxiety-fueled-mental-leaps',
    'Overgeneralization'        : 'DEFINITION: A type of cognitive distortion called overgeneralization occurs when someone extrapolates\
                                information from one incident to all other events.\
                                \nLINK WITH TIPS: \nhttps://www.verywellmind.com/overgeneralization-3024614',
    'Personalization'           : 'DEFINITION: Personalization is the idea that something is totally your fault even when you had little\
                                to no influence on the outcome.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/personalization-a-common-type-of-negative-thinking',
    'Polarized'                 : 'DEFINITION: This distortion, also known as "all-or-nothing" or "black-and-white thinking,"\
                                happens when people regularly think in extremes without taking all the relevant information into account.\
                                \nLINK WITH TIPS: \nhttps://exploringyourmind.com/polarized-thinking-cognitive-distortion/',
    'Shoulds'                   : 'DEFINITION: "Should" statements are irrational rules you make for yourself and others\
                                without taking into account the particulars of a situation.\
                                They are cognitive distortions. You tell yourself that there should be no exceptions to how things should be done.\
                                \nLINK WITH TIPS: \nhttps://www.therapynowsf.com/blog/should-statements-reframe-the-way-you-think'
}


relaxation_exercise = "I have detected that your mood hasn't improved, Hence please go throught our recommendations in the website "

class CBTBot:
    def __init__(self):
        self.step = 0
        self.sia = SentimentIntensityAnalyzer()
        self.automatic_thought = None
        self.cognitive_distortion = None
        self.pre_mood_rating = None
        self.post_mood_rating = None

    def run_session(self):
        print("Hello!\nMy name is Nexbot and I'm going to give you support to your self-directed CBT Therapy session.")
        print("So, how have you been feeling?")
        while True:
            user_input = input("You: ")
            self.process_input(user_input)

    def process_input(self, user_input):
        if (self.step == 3 or self.step == 7):  # Check mood rating
            response = self.check_rating(user_input)
            print(response)
            # Check whether the mood has improved
            if self.step == 7 and (self.post_mood_rating - self.pre_mood_rating) >= 0:
                print(relaxation_exercise)
                self.step = 0
        else:
            answer = self.get_response(user_input)
            if (
                answer
                == "Hello! So, tell me how have you been feeling?"
                or answer == "Bye. Hope I've been helpful."
            ):
                self.step = 0
            if answer == "none":
                if self.step == 0 and self.sia.polarity_scores(user_input)["compound"] > 0:
                    print("I'm glad that you feel this way :)")
                    self.step = 0
                else:
                    self.get_script_answer()
                    if self.step == 1:
                        self.automatic_thought = user_input
                    self.step += 1
            else:
                print(f"{bot_name}: {answer}")

    def get_script_answer(self):
        print(script_answers[self.step])

    def get_response(self, user_input):
        # ... (Your response matching logic)
        return "none"  # In this case the dialogue flow continues

    def check_rating(self, user_input):
        kai_answer = "Please enter a valid answer"
        if user_input.isnumeric():
            rating = int(user_input)
            if 1 <= rating <= 100:
                if self.step == 7:
                    kai_answer = self.detect_cognitive_distortion()
                    self.post_mood_rating = rating
                else:
                    kai_answer = script_answers[self.step]
                    self.step += 1
                    self.pre_mood_rating = rating
        return kai_answer

    def detect_cognitive_distortion(self):
        pickled_model = pickle.load(open("../data/cognitive_distortion_detector_model.pkl", "rb"))
        self.cognitive_distortion = pickled_model.predict([self.automatic_thought])[0]
        if self.cognitive_distortion != "NO":
            msg = (
                "I have detected a potential cognitive distortion: "
                + self.cognitive_distortion
                + "\n"
                + CD[self.cognitive_distortion]
            )
            return msg

def cognit():
    bot = CBTBot()
    bot.run_session()

if __name__ == "__main__":
    cognit()
