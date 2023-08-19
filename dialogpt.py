from transformers import AutoTokenizer, AutoModelWithLMHead
import torch

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-large',padding_side="left")
model = AutoModelWithLMHead.from_pretrained('microsoft/DialoGPT-large')


# Define a function to generate a response
def chat_with_dialogpt(user_input):
    chat_history_ids = None
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids],
                              dim=-1) if chat_history_ids is not None else new_user_input_ids

    # Generate a response from the chatbot
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=100,
        top_p=0.7,
        temperature=0.8
    )

    # Decode and print the chatbot's response
    chat_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return chat_response


