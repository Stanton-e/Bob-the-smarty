import os
import subprocess
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
import torch
import time
import requests
import transformers
import importlib
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed, GPT2Tokenizer, GPT2LMHeadModel, load_tf_weights_in_gpt2
from dotenv import load_dotenv

sys.stderr = open(os.devnull, 'w')
#----------------------------------------------------
#                 Bob the smarty
#                       by
#                     Stan44
#           Version: 0.0.3 Alpha Stable
#                 
#----------------------------------------------------
load_dotenv()

module_folder = "modules"
loaded_modules = {}
module_files = [
    filename[:-3]
    for filename in os.listdir(module_folder)
    if filename.endswith(".py") and not filename.startswith("__")
]
for module_file in module_files:
    module = importlib.import_module(f"{module_folder}.{module_file}")
    loaded_modules[module_file] = module

# Access the loaded module using the file name
module_name = "example_module"
loaded_module = loaded_modules.get(module_name)
if loaded_module:
    # Do something with the loaded module
    pass
else:
    print(f"Module '{module_name}' not found.")

window = tk.Tk()
window.title("Bob the Smarty")
window.geometry("600x400")
chat_display = ScrolledText(window, height=20)
chat_display.pack(fill=tk.BOTH, expand=True)
user_input_entry = tk.Entry(window)
user_input_entry.pack(fill=tk.X)

response_history = []
# Load and initialize your Hugging Face model
print('Loading AI model...')
model_path = 'gpt2-medium'  # Path to the GPT-2 model
tokenizer = GPT2Tokenizer.from_pretrained(model_path, padding='max_length', truncation=True, padding_side='left')
tokenizer.add_special_tokens({'pad_token': '[PAD]'})
model = GPT2LMHeadModel.from_pretrained(model_path)
generator = pipeline('text-generation', model='gpt2-medium')
encoded_input = None
attention_mask = None
def generate_response(input_text, response_history):
    conversation_history = [input_text] + response_history  # Include the input text in the conversation history
    encoded_input = tokenizer.encode_plus(conversation_history, return_tensors="pt", padding='longest', truncation=True, padding_side='left')
    input_ids = encoded_input.input_ids
    attention_mask = input_ids.ne(tokenizer.pad_token_id).long()
    set_seed(42)
    response = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=100,
        num_return_sequences=1,
        temperature=0.8,
        top_k=50,
        pad_token_id=tokenizer.pad_token_id  # Set the pad token ID for open-end generation
    )
    response_text = tokenizer.decode(response[0], skip_special_tokens=True)
    response_history.append(response_text)
    response_history = response_history[-3:]  # Keep the response history within a certain limit
    return response_text, response_history
    

def similar_response(response_text, previous_response):
    if response_text == previous_response:
        return True

    return False

print('The model has been loaded...')

def process_user_input():
    global response_history
    user_input = user_input_entry.get()
    if user_input.lower() == 'quit':
        chat_display.insert(tk.END, "Thank you for using the program. We hope you enjoyed it.\n")
        sys.exit()
    else:
        response, response_history = generate_response(user_input, response_history[::-1])
        chat_display.insert(tk.END, f"You: {user_input}\n")
        chat_display.insert(tk.END, f"Bob: {response}\n\n")
    user_input_entry.delete(0, tk.END)

def submit_button_click():
    process_user_input()

submit_button = tk.Button(window, text="Send", command=submit_button_click)
submit_button.pack()

print('Everything has loaded. Please enjoy, and remember that nothing this says is true or factual.')

window.bind('<Return>', lambda event: process_user_input())
# Start the GUI event loop
window.mainloop()
