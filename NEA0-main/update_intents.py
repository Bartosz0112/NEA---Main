import json
from datetime import datetime

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# def update_intents(new_data, intents):
#     print('we are updating')
#     print(new_data)
#     for entry in new_data:
#         print(f"Question: {entry['input']}\nSuggested Answer: {entry['response']}")
#         tag = input("Enter the tag for this Q&A (or 'new' to create a new tag): ")
        
#         if tag == 'new':
#             new_tag = input("Enter new tag name: ")
#             new_pattern = entry['input']
#             new_response = entry['response']
#             intents['intents'].append({"tag": new_tag, "patterns": [new_pattern], "responses": [new_response]})
#         else:
#             for intent in intents['intents']:
#                 if intent['tag'] == tag:
#                     intent['patterns'].append(entry['input'])
#                     intent['responses'].append(entry['response'])
#                     break


def update_intents(new_data, intents):
    for entry in new_data:
        print(f"Question: {entry['input']}\nSuggested Answer: {entry['response']}")

        now = datetime.now()
        id_string = now.strftime("%Y%m%d%H%M%S")

        tag = "user_responses-" + id_string
        # Check if the tag already exists
        existing_tag = next((intent for intent in intents['intents'] if intent['tag'] == tag), None)

        if existing_tag is not None:
            # Tag exists, add patterns and responses
            existing_tag['patterns'].append(entry['input'])
            existing_tag['responses'].append(entry['response'])
        else:
            # Create a new tag
            new_intent = {
                "tag": tag,
                "patterns": [entry['input']],
                "responses": [entry['response']]
            }
            intents['intents'].append(new_intent)
# Load existing intents and new data

# Update intents with new data
def trigger_update():
    new_data = []
    intents = load_data('intents.json')
    with open('new_data.json', 'r') as file:
        for line in file:
            new_data.append(json.loads(line.strip()))
    update_intents(new_data, intents)
    # Save the updated intents
    save_data(intents, 'intents.json')
    print("intents.json has been updated with new Q&A pairs.")

    # clear new_data.json
    with open('new_data.json', 'w') as file:
        file.write('')
    

