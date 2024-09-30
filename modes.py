#!/usr/bin/env python3
# modes.py
# for testing local models responses on the droplet

"""
Module Docstring
"""

__author__ = "Alex Bishop"
__version__ = "0.3.0"
__license__ = "MIT"

import os
import time
import logging
from config import *
from models import *
from prompts import *
from generation import *
from utils import *
from user_messages import *
from analyze_excel import *
import random
import json
import openai
from config import OPENAI_API_KEY  # Ensure you have this in your config

# Track current pre-prompt mode (default: "normal")
current_mode = "normal"  # Default mode

def get_current_mode():
    """Returns the current mode."""
    return current_mode

def set_current_mode(new_mode):
    """Updates the current mode."""
    global current_mode
    current_mode = new_mode

# Check and add responses folder for saving model output
responses_dir = responses_dir
if not os.path.exists(responses_dir):
    os.makedirs(responses_dir)

prompts_file = prompts_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use the load_models function to load the models
models = load_models()

# Define list of compute analysis methods
def all_non_ai_modes():
    """
    This function returns the list of all non-AI evaluation modes.
    """
    return [
        "Count Sentences",
        "Count Tokens",
        "Count Characters",
        "Count Words",
        "Extract Named Entities",
        "Cosine Similarity Analysis",
        "Sentiment Polarity Analysis",
        "Sentiment Subjectivity Analysis",
        "Flagged Words and Phrases Analysis",
        "Spelling Error Check",
        "BERTScore Analysis",
        "Token Matching Analysis",
        "Semantic Similarity Analysis",
        "Noun-Phrase Extraction"
    ]

def display_generating_message(model_name, prompt, message_type="generating"):
    current_mode = get_current_mode()
    pre_prompt_message = preprompt_modes.get(current_mode, "")
    
    if message_type == "selected":
        print(f"🔄 Generating response for model: {model_name} with pre-prompt: '{pre_prompt_message}' and prompt: {prompt}")
    elif message_type == "sending":
        print(f"📤 Sending prompt to model: {model_name} with pre-prompt: '{pre_prompt_message}' and prompt: {prompt}")
    elif message_type == "generating":
        print(f"🔄 Generating response for model: {model_name} with pre-prompt: '{pre_prompt_message}' and prompt: {prompt}")
    else:
        print(f"⚠️ Unknown message type for model: {model_name}")

def main_1_model_prompt_selection_sequence():
    prompts = load_prompts(prompts_file)  # Loads prompts categorized
    selected_models = select_model(models, allow_multiple=True)
    print(menu1_title())
    if not selected_models:
        print(msg_no_models())
        return

    # Use select_category function for consistent category selection
    categories = list(prompts.keys())
    # Exclude the "Summarization" category from the list
    categories = [category for category in categories if category != summary_category_name]

    selected_category = select_category(categories)
    if not selected_category:
        print(msg_farewell())
        return

    # Display prompts within the selected category
    category_prompts = prompts[selected_category]
    print(msg_prompts_from_category(selected_category))
    selected_prompts = multi_selection_input("\n", category_prompts)
    if not selected_prompts:
        print(msg_no_prompts())
        return

    # Ask for the quantity of times to send each prompt
    while True:
        try:
            # Display the prompt and capture the user's input
            quantity_input = input(msg_prompt_quantity()).strip()
            # Check if input is empty and default to 1
            if quantity_input == "":
                quantity = 1
            else:
                # Convert the user's input into an integer
                quantity = int(quantity_input)
            break  # Exit the loop if the input is successfully converted or empty
        except ValueError:
            # Handle the case where the conversion fails
            print(msg_invalid_number())

    for model_name in selected_models:
        for prompt in selected_prompts:
            for _ in range(quantity):
                display_generating_message(model_name, prompt, "generating")
                try:
                    response, response_time, char_count, word_count = generate(model_name, prompt, current_mode)
                    print_response_stats(response, response_time, char_count, word_count)
                    # Directly save the response without user confirmation
                    save_response(model_name, prompt, response, response_time, char_count, word_count, current_mode)
                except Exception as e:
                    logging.error(msg_error_simple(e))
                    print(msg_error_simple(e))
                time.sleep(sleep_time)  # Adjust sleep time as needed

def main_2_model_category_selection_sequence():
    prompts = load_prompts(prompts_file)  # Loads prompts categorized
    selected_models = select_model(models, allow_multiple=True)
    print(menu2_title())
    if not selected_models:
        print(msg_no_models())
        return

    # Use select_category function for consistent category selection
    categories = list(prompts.keys())
    # Exclude the "Summarization" category from the list
    categories = [category for category in categories if category != summary_category_name]

    selected_category = select_category(categories)
    if selected_category is None:
        print(msg_farewell())
        return
    elif selected_category == 'custom':
        # Handle custom prompt logic here
        print("Custom " + msg_word_prompt() + " logic not shown for brevity.")
        return
    else:
        # Use the selected category name directly to access prompts
        category_prompts = prompts[selected_category]
        for model_name in selected_models:
            for prompt in category_prompts:
                display_generating_message(model_name, prompt, "generating")
                try:
                    response, response_time, char_count, word_count = generate(model_name, prompt, current_mode)
                    print_response_stats(response, response_time, char_count, word_count)
                    # Directly save the response without user confirmation
                    save_response(model_name, prompt, response, response_time, char_count, word_count, current_mode)
                except Exception as e:
                    logging.error(msg_error_simple(e))
                    print(msg_error_simple(e))
                time.sleep(sleep_time)  # Adjust sleep time as needed

def main_3_all_prompts_to_single_model():
    print(menu3_title())
    selected_model_names = select_model(models, allow_multiple=False)
    if selected_model_names is None:
        print(msg_farewell())
        return
    selected_model = selected_model_names[0]  # Assuming only one model is selected for this option, take the first item

    model_name = selected_model  # Capture the selected model's name

    prompts = load_prompts(prompts_file, flat=True)  # Load all prompts, assuming a flat structure
    if not prompts:
        print(msg_no_prompts())
        return

    for prompt in prompts:
        display_generating_message(model_name, prompt)
        try:
            response, response_time, char_count, word_count = generate(model_name, prompt, current_mode)
            print_response_stats(response, response_time, char_count, word_count)
            # Directly save the response without user confirmation
            save_response(model_name, prompt, response, response_time, char_count, word_count, current_mode)
        except Exception as e:
            logging.error(msg_error_response(prompt, e))  # Ensure msg_error_response is defined to handle this
            print(msg_error_response(prompt, e))  # And here as well
        time.sleep(sleep_time)  # Throttle requests to avoid overwhelming the model

def main_4_review_missing_prompts():
    print(menu4_title())
    selected_model_names = select_model(models, allow_multiple=False)
    if selected_model_names is None:
        print(msg_farewell())
        return
    selected_model = selected_model_names[0]

    model_name = selected_model  # Capture the selected model's name

    missing_prompts = find_missing_prompts(model_name)
    if not missing_prompts:
        print(msg_no_missing_prompts())
        return

    selected_prompts = multi_selection_input(msg_unsent_prompts(), missing_prompts)
    if not selected_prompts:
        selected_prompts = missing_prompts  # If user hits enter without selecting, use all missing prompts

    for prompt in selected_prompts:
        display_generating_message(model_name, prompt)
        try:
            response, response_time, char_count, word_count = generate(model_name, prompt, current_mode)
            print_response_stats(response, response_time, char_count, word_count)
            # Directly save the response without user confirmation
            save_response(model_name, prompt, response, response_time, char_count, word_count, current_mode)
        except Exception as e:
            logging.error(msg_error_response(prompt, str(e)))  # Ensure to convert exception to string
            print(msg_error_response(prompt, str(e)))
        time.sleep(sleep_time)  # Throttle requests to avoid overwhelming the model

def process_excel_file(model_name, prompt, excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path, engine=excel_engine)

    # Define the new column name based on the model name
    summary_column_name = f"{model_name}-Summary"

    # Ensure the new summary column exists, if not, create it
    if summary_column_name not in df.columns:
        df[summary_column_name] = pd.Series(dtype='object')

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        content = row['Message_Content']  # Assuming the content is in column B
        # Extract the first 15 words from the content
        first_15_words = ' '.join(content.split()[:summary_excerpt_wordcount])
        
        # Print the message including the first 15 words of the content
        display_generating_message(model_name, prompt, "generating")
        print(f"'{first_15_words}...'")
        
        # Generate the summary using the selected model and prompt
        try:
            _, response, _, _, _ = generate(model_name, f"{PROMPT_COLOR}{prompt}{RESET_STYLE} {content}", current_mode)
        except Exception as e:
            logging.error(msg_error_response(prompt, e))
            response = msg_error_simple(e)
        # Prepend the prompt to the response
        full_response = f"{prompt}\n{response}"
        df.at[index, summary_column_name] = full_response  # Write the prompt and response to the new summary column
        time.sleep(3)  # Add a 3-second delay between API calls

    # Save the modified DataFrame back to the Excel file
    df.to_excel(excel_path, index=False, engine=excel_engine)
    print(msg_excel_completed(excel_path))

def main_5_iterate_summary():
    print(menu5_title())

    # Select a single model
    selected_model_names = select_model(models, allow_multiple=False)
    if selected_model_names is None:
        print(msg_farewell())
        return
    selected_model = selected_model_names[0]

    # Automatically select the "Comprehension and Summarization" category
    prompts = load_prompts(prompts_file)
    category_prompts = prompts.get(summary_category_name, [])
    if not category_prompts:
        print(msg_summary_prompt_missing())
        return

    # Let the user select a prompt from the "Comprehension and Summarization" category
    print(msg_select_summary_prompt())
    for idx, prompt_option in enumerate(category_prompts, start=1):
        print(f"{idx}. {PROMPT_COLOR}{prompt_option}{RESET_STYLE}")
    prompt_selection = input(msg_enter_prompt_num()).strip()
    try:
        prompt_idx = int(prompt_selection) - 1
        prompt = category_prompts[prompt_idx]
    except (ValueError, IndexError):
        print(msg_invalid_retry())
        return  # Optionally, you could loop back to prompt selection instead of returning

    print(msg_prompt_confirm(prompt))

    # Use the predefined Excel file path from config.py
    excel_path = summary_input_xls

    # Process the Excel file
    process_excel_file(selected_model, prompt, excel_path)

def main_6_query_responses():
    print(menu6_title())
    selected_models = select_model(models, allow_multiple=True)
    if not selected_models:
        print(msg_no_models())
        return

    prompts = load_prompts(prompts_file)  # Loads prompts categorized

    # Use select_category function for consistent category selection
    categories = list(prompts.keys())
    # Exclude the "Summarization" category from the list
    categories = [category for category in categories if category != summary_category_name] 

    selected_category = select_category(categories)
    if not selected_category:
        print(msg_farewell())
        return

    category_prompts = prompts[selected_category]
    # Use msg_select_prompt_from_cat to display the selected category
    print(msg_select_prompt_from_cat(selected_category))

    selected_prompts = multi_selection_input("\n" + msg_user_nudge() + msg_word_enter() + " your choices: ", category_prompts)
    if not selected_prompts:
        print(msg_no_prompts())
        return

    for model_name in selected_models:
        for prompt in selected_prompts:
            print(msg_search_query(model_name, prompt))
            responses = load_model_responses(model_name)
            matching_responses = [response for response in responses if response['prompt'] == prompt]
            if matching_responses:
                for response in matching_responses:
                    print(msg_query_display_results(model_name, prompt, response))
            else:
                print(msg_no_matching())

def main_7_random_model_prompt():
    print(menu7_title())

    while True:  # This loop allows re-rolling
        # Load models
        models = load_models()  # Assuming this function returns a list of model dictionaries

        # Load prompts from Excel instead of JSON
        try:
            prompts_df = pd.read_excel('prompts_benchmarks.xlsx', engine='openpyxl')  # Adjust the path if necessary
            all_prompts = prompts_df['Prompt_Text'].tolist()  # Assuming your Excel has a column named 'Prompt'
        except FileNotFoundError:
            print("File 'prompts_benchmarks.xlsx' not found.")
            return
        except Exception as e:
            print(f"Failed to load prompts from Excel: {e}")
            return

        if not all_prompts:
            print("No prompts available.")
            return

        # Randomly select a model
        selected_model = random.choice(models)
        model_name = selected_model['name']  # Extract the model name

        # Randomly select a prompt
        prompt = random.choice(all_prompts)

        # Display the randomized selection to the user
        print(f"\nRandomly selected {msg_word_model()}: {MODELNAME_COLOR}{BOLD_EFFECT}{model_name}{RESET_STYLE}")
        print(f"Randomly selected {msg_word_prompt()}: {PROMPT_COLOR}{prompt}{RESET_STYLE}")

        # Ask user to proceed or re-roll
        proceed = confirm_selection(msg_confirm_selection())
        if proceed:
            # Proceed with generation using the selected model and prompt
            try:
                display_generating_message(model_name, prompt, "generating")
                response, response_time, char_count, word_count = generate(model_name, prompt, current_mode)
                print_response_stats(response, response_time, char_count, word_count)
                # Optionally save the response without user confirmation
                save_response(model_name, prompt, response, response_time, char_count, word_count, current_mode)
            except Exception as e:
                logging.error(msg_error_simple(e))
                print(msg_error_simple(e))

            # After generation, ask if the user wants to roll again
            roll_again = confirm_selection(msg_roll_dice_again())
            if not roll_again:
                break  # Correctly placed to exit the while True loop if the user does not want to roll again
        else:
            # If the user chooses not to proceed, ask immediately if they want to roll again
            roll_again = confirm_selection(msg_roll_dice_again())
            if not roll_again:
                break  # Exit the loop if the user does not want to roll again

def main_8_export_to_excel():
    print(menu8_title())
    export_all_responses()

def main_9_response_evaluation():
    print(menu9_title())
    
    # Define the simplified menu for analysis
    modes_of_analysis = [
        "Compute Evaluations (All)",        # All non-AI analyses
        "Gemini Evaluations (6 Aspects)",   # Gemini-specific evaluations
        "Mistral Evaluations (6 Aspects)",  # Mistral-specific evaluations
        "Merge Excel Evaluation Results"    # Merge compute, Gemini, and Mistral eval results into a single excel file
    ]

    # Display menu to select analysis mode
    selected_mode = single_selection_input("Select the analysis mode to run:", modes_of_analysis)
    if not selected_mode:
        print("No mode selected. Exiting.")
        return

    # File paths
    file_path = 'prompt_responses.xlsx'
    output_file_path = None  # Default to None unless needed

    # Pass the selected mode to the processing function
    if selected_mode == "Compute Evaluations (All)":
        output_file_path = 'prompt_responses.xlsx'
    elif selected_mode == "Gemini Evaluations (6 Aspects)":
        output_file_path = 'prompt_responses_gemini.xlsx'
    elif selected_mode == "Mistral Evaluations (6 Aspects)":
        output_file_path = 'prompt_responses_mistral.xlsx'

    process_selected_analysis_modes(file_path, output_file_path, selected_mode)

    # If it was the merge option, no need for further output file references
    if selected_mode != "Merge Excel Evaluation Results":
        print(f"✅ {selected_mode} completed and saved to {output_file_path}.\n")

def main_10_preprompt_mode():
    print(f"DEBUG: Before mode selection, current_mode = {get_current_mode()}")  # Check current mode before change
    print(menu10_title())
    print("Select the pre-prompt mode:")
    for i, mode in enumerate(preprompt_modes.keys()):
        print(f"{i + 1}. {mode}")
    selected_mode = int(input("Enter the number of the mode: ")) - 1

    mode_list = list(preprompt_modes.keys())
    if 0 <= selected_mode < len(mode_list):
        set_current_mode(mode_list[selected_mode])  # Update the mode using setter
        print(f"DEBUG: After selection, current_mode = {get_current_mode()}")
        print(f"Pre-prompt mode set to '{get_current_mode()}' 🎭")
    else:
        print("Invalid selection. Mode not changed.")