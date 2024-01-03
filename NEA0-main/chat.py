import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from update_intents import trigger_update
import time
import subprocess



def load_model():
    global model, all_words, tags, device, intents

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

load_model()

bot_name = "Chatbot"


def handle_unknown_response(user_input):
    return {"status": "unknown", "message": "I do not understand this. Can you tell me what I should say?", "input": user_input}

    # print("I do not understand this. Can you tell me what I should say?")
    # correct_response = input("Your answer: ")
    # new_data = {"input": user_input, "response": correct_response}

    # with open('new_data.json', 'a') as file:  # Append mode
    #     json.dump(new_data, file)
    #     file.write('\n')  # For readability in the JSON file
    # time.sleep(4)
    # trigger_update()

    # now resave intents        
    # trigger training 
    
def handle_user_response(user_input, answer):

    print('saving response ....')
    new_data = {"input": user_input, "response": answer}

    with open('new_data.json', 'a') as file:  # Append mode
        json.dump(new_data, file)
        file.write('\n')  # For readability in the JSON file
    time.sleep(2)
    trigger_update()


    filename = 'train.py'
    subprocess.run(['python', filename])

    load_model()

    return "Thank you for your response. I will remember this next time."

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    print('we are here')
    print(prob.item())
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    else:
        return handle_unknown_response(msg)    


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

