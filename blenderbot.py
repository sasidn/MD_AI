from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")

# Define a function to generate a response
def generate_response(user_input):
    input_ids = tokenizer.encode(user_input, return_tensors="pt", max_length=1024, truncation=True)
    # Generate a response from the model
    response_ids = model.generate(input_ids, max_length=1024, num_return_sequences=1)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response


