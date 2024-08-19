#!/usr/bin/env python3
# main.py
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
from models import load_models, select_model, ask_to_save_response, save_response
from prompts import load_prompts, handle_custom_prompt, find_missing_prompts, load_model_responses
from generation import generate
from utils import *
from user_messages import *

# Check and add responses folder for saving model output
responses_dir = responses_dir
if not os.path.exists(responses_dir):
    os.makedirs(responses_dir)

prompts_file = prompts_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Use the load_models function to load the models
models = load_models()

def main_1_userselect():
    context = []
    prompts = load_prompts(prompts_file)
    selected_model = None
    prompt = None  # Initialize prompt to None to ensure it's selected in the first iteration

    while True:
        if not selected_model:
            selected_model_names = select_model(models, allow_multiple=False)
            if selected_model_names is None:
                break  # Exit the loop and end the program
            selected_model = selected_model_names[0]  # Assuming only one model is selected for this option, take the first item

        # Use select_category function for consistent category selection
        selected_category = select_category(list(prompts.keys()))
        if selected_category is None:
            break  # Exit if the user chooses to exit during category selection

        if selected_category == 'custom':
            prompt = handle_custom_prompt(prompts, prompts_file)
            if prompt is None:
                continue  # Skip the rest of the loop if no custom prompt is provided
        else:
            # Display prompt options within the selected category
            print(msg_select_prompt_single())
            category_prompts = prompts[selected_category]
            for idx, prompt_option in enumerate(category_prompts, start=1):
                print(f"{idx}. {PROMPT_COLOR}{prompt_option}{RESET_STYLE}")
            prompt_selection = input(msg_enter_prompt_selection()).strip()
            try:
                prompt_idx = int(prompt_selection) - 1
                prompt = category_prompts[prompt_idx]
                print(msg_prompt_confirm(prompt))
                if not confirm_selection():
                    continue
            except (ValueError, IndexError):
                print(msg_invalid_retry())
                continue
            
        print(msg_generating_selected(selected_model, prompt))
        try:
            # Ensure selected_model is a string, not a list
            context, response, response_time, char_count, word_count = generate(selected_model, prompt, context)
        except Exception as e:
            logging.error(msg_word_error() + msg_error_simple(e))
            print(msg_word_error() + msg_error_simple(e))
            continue

        print_response_stats(response, response_time, char_count, word_count)
        
        if ask_to_save_response():
            rating = get_user_rating()
            save_response(selected_model, prompt, response, rating, response_time, char_count, word_count)

        # Ask if user wants to continue with the same model
        use_same_model = confirm_selection(msg_use_same_model(selected_model))
        if use_same_model:
            # If 'y', continue with the same model but prompt will be re-selected in the next iteration
            continue
        else:
            # If 'n', reset selected_model to allow model selection
            selected_model = None

def main_2_model_prompt_selection_sequence():
    prompts = load_prompts(prompts_file)  # Loads prompts categorized
    selected_models = select_model(models, allow_multiple=True)
    if not selected_models:
        print(msg_no_models())
        return

    # New Step: Select a prompt category first
    categories = list(prompts.keys())
#    print(msg_select_category())
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
            quantity_input = input(msg_prompt_quantity())
            # Convert the user's input into an integer
            quantity = int(quantity_input.strip())
            break  # Exit the loop if the input is successfully converted
        except ValueError:
            # Handle the case where the conversion fails
            print(msg_invalid_number())

    for model_name in selected_models:
        for prompt in selected_prompts:
            for _ in range(quantity):
                print(msg_generating_msg(model_name, prompt))
                try:
                    context, response, response_time, char_count, word_count = generate(model_name, prompt, None)
                    print_response_stats(response, response_time, char_count, word_count)
                    # Directly save the response without user confirmation
                    save_response(model_name, prompt, response, "", response_time, char_count, word_count)
                except Exception as e:
                    logging.error(msg_error_simple(e))
                    print(msg_error_simple(e))
                time.sleep(sleep_time)  # Adjust sleep time as needed

def main_3_model_category_selection_sequence():
    prompts = load_prompts(prompts_file)  # Loads prompts categorized
    selected_models = select_model(models, allow_multiple=True)
    if not selected_models:
        print(msg_no_models())
        return

    categories = list(prompts.keys())
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
                print(msg_generating_msg(model_name, prompt))
                try:
                    context, response, response_time, char_count, word_count = generate(model_name, prompt, None)
                    print_response_stats(response, response_time, char_count, word_count)
                    # Directly save the response without user confirmation
                    save_response(model_name, prompt, response, "", response_time, char_count, word_count)
                except Exception as e:
                    logging.error(msg_error_simple(e))
                    print(msg_error_simple(e))
                time.sleep(sleep_time)  # Adjust sleep time as needed

def main_4_all_prompts_to_single_model():
    print("\nOption 4: All Prompts to Single Model")
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
        print(f"\nSending " + msg_word_prompt() + " to " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE}: {PROMPT_COLOR}{prompt}{RESET_STYLE}")
        try:
            context, response, response_time, char_count, word_count = generate(model_name, prompt, None)
            print_response_stats(response, response_time, char_count, word_count)
            # Directly save the response without user confirmation
            save_response(model_name, prompt, response, "", response_time, char_count, word_count)
        except Exception as e:
            logging.error(msg_error_response(prompt, e))
            print(msg_error_response(prompt, e))
        time.sleep(sleep_time)  # Throttle requests to avoid overwhelming the model

def main_5_review_missing_prompts():
    print("\nOption 5: View Unsent Prompts to Model")
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

    print(f"\nFound {len(missing_prompts)} unsent " + msg_word_prompt() + "s for " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE}.")
    selected_prompts = multi_selection_input("\n" + msg_user_nudge() + msg_word_select() + " " + msg_word_prompt() + f"s to send (or hit {BOLD_EFFECT}" + msg_word_select() + f"{RESET_STYLE} to send all): ", missing_prompts)
    if not selected_prompts:
        selected_prompts = missing_prompts  # If user hits enter without selecting, use all missing prompts

    for prompt in selected_prompts:
        print(f"\nSending " + msg_word_prompt() + " to " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE}: {PROMPT_COLOR}{prompt}{RESET_STYLE}")
        try:
            context, response, response_time, char_count, word_count = generate(model_name, prompt, None)
            print_response_stats(response, response_time, char_count, word_count)
            # Directly save the response without user confirmation
            save_response(model_name, prompt, response, "", response_time, char_count, word_count)
        except Exception as e:
            logging.error(msg_word_error() + msg_error_response(prompt, e))
            print(msg_word_error() + msg_error_response(prompt, e))
        time.sleep(sleep_time)  # Throttle requests to avoid overwhelming the model

def main_6_iterate_summary():
    print("\nOption 6: Summarize Content from Excel File Using Selected Prompt")

    # Select a single model
    selected_model_names = select_model(models, allow_multiple=False)
    if selected_model_names is None:
        print(msg_farewell())
        return
    selected_model = selected_model_names[0]

    # Automatically select the "Comprehension and Summarization" category
    prompts = load_prompts(prompts_file)
    category_prompts = prompts.get("Comprehension and Summarization", [])
    if not category_prompts:
        print(msg_summary_prompt_missing())
        return

    # Let the user select a prompt from the "Comprehension and Summarization" category
    print(msg_select_summary_prompt())
    for idx, prompt_option in enumerate(category_prompts, start=1):
        print(f"{idx}. {PROMPT_COLOR}{prompt_option}{RESET_STYLE}")
    prompt_selection = input("\n" + msg_user_nudge() + msg_word_enter() + " the " + msg_word_number() + " of the " + msg_word_prompt() + " you want to use: ").strip()
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

def main_7_query_responses():
    print("\nOption 7: Query Existing Responses")
    selected_models = select_model(models, allow_multiple=True)
    if not selected_models:
        print(msg_no_models())
        return

    prompts = load_prompts(prompts_file)  # Loads prompts categorized
    categories = list(prompts.keys())
    selected_category = select_category(categories)
    if not selected_category:
        print(msg_farewell())
        return

    category_prompts = prompts[selected_category]
    print(f"\n" + msg_word_select() + " " + msg_word_prompt() + "s from the " + msg_word_category() + f" '{CATEGORY_COLOR}{selected_category}{RESET_STYLE}':")
    selected_prompts = multi_selection_input("\n" + msg_user_nudge() + msg_word_enter() + " your choices: ", category_prompts)
    if not selected_prompts:
        print(msg_no_prompts())
        return

    for model_name in selected_models:
        for prompt in selected_prompts:
            print(f"\nSearching for responses from " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE} to " + msg_word_prompt() + f": {PROMPT_COLOR}{prompt}{RESET_STYLE}")
            responses = load_model_responses(model_name)
            matching_responses = [response for response in responses if response['prompt'] == prompt]
            if matching_responses:
                for response in matching_responses:
                    print(f"\nResponse from " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE} to " + msg_word_prompt() + f" '{PROMPT_COLOR}{prompt}{RESET_STYLE}':\n{response['response']}")
            else:
                print(msg_no_matching())

# Creating a styled, blinged-out message
welcome_message = (
    f"{BLINK_EFFECT}{BOLD_EFFECT}{MODEL_COLOR}✨🌟 Welcome ✨ "
    f"{CATEGORY_COLOR}🎈✨ to the ✨🎈 "
    f"{PROMPT_COLOR}🚀✨ Prompt ✨🚀 "
    f"{RESPONSE_COLOR}🎉✨ Machine! ✨🎉"
    f"{RESET_STYLE}"
)

def task_complete_msg():
    """Displays the message for next steps after a task completes."""
    print("\n" + msg_user_nudge() + "❓ What would you like to do next?")
    print(f"{PROMPT_COLOR}m.{RESET_STYLE} {BOLD_EFFECT} {emoji_menu_main}Return to Main Menu{RESET_STYLE}")
    print(f"{PROMPT_COLOR}b.{RESET_STYLE} {BOLD_EFFECT} {emoji_menu_back}Go Back {RESET_STYLE}(Repeat this mode)")
    print(f"{PROMPT_COLOR}q.{RESET_STYLE} {BOLD_EFFECT} {emoji_menu8_exit}Quit the application{RESET_STYLE}")

def main():
    last_action = None

    while True:
        print(welcome_message)
        print(f"\n{STATS_COLOR}{BOLD_EFFECT}" + msg_word_select() + f"{RESET_STYLE} a mode:")
        # The menu option numbers will be magenta, the option name will be bold, and the parentheses will be regular
        print(f"{PROMPT_COLOR}1.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu1_single}Single Prompt, Model, and Rate{RESET_STYLE} (Manual)")
        print(f"{PROMPT_COLOR}2.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu2_prompt}Model & Prompt Selection{RESET_STYLE} (Sequence)")
        print(f"{PROMPT_COLOR}3.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu3_category}Model & Category Selection{RESET_STYLE} (Sequence)")
        print(f"{PROMPT_COLOR}4.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu4_all}All Prompts to Single Model{RESET_STYLE} (Sequence)")
        print(f"{PROMPT_COLOR}5.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu5_unsent}Unsent Prompts for Model{RESET_STYLE} (Sequence)")
        print(f"{PROMPT_COLOR}6.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu6_summary}Summary Prompts on Excel{RESET_STYLE} (Sequence)")
        print(f"{PROMPT_COLOR}7.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu7_query}Query Completed Responses{RESET_STYLE}")
        print(f"{PROMPT_COLOR}q.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu8_exit}Quit{RESET_STYLE}")

        if last_action:
            print(f"\n{PROMPT_COLOR}b.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu_back}Back {RESET_STYLE}(Repeat this mode)")

        choice = input(msg_user_nudge() + msg_word_enter() + f" your choice: {RESET_STYLE}").strip().lower()

        if choice == 'q':
            print(msg_farewell())
            break
        elif choice == 'b' and last_action:
            choice = last_action
        else:
            last_action = choice

        if choice == '1':
            main_1_userselect()
        elif choice == '2':
            main_2_model_prompt_selection_sequence()
        elif choice == '3':
            main_3_model_category_selection_sequence()
        elif choice == '4':
            main_4_all_prompts_to_single_model()
        elif choice == '5':
            main_5_review_missing_prompts()
        elif choice == '6':
            main_6_iterate_summary()
        elif choice == '7':
            main_7_query_responses()
        else:
            print(msg_invalid_retry())

        task_complete_msg()
        next_action = input("\n" + msg_user_nudge() + "Your choice: ").strip().lower()
        if next_action == 'q':
            print(msg_farewell())
            break
        elif next_action == 'm':
            continue  # This will restart the loop, showing the main menu
        elif next_action == 'b' and last_action:
            # Set choice to last_action to repeat it in the next iteration
            choice = last_action
        else:
            print(msg_invalid_returning())
            continue

if __name__ == "__main__":
    main()