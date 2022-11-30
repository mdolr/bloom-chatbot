import random
from termcolor import colored
import src.config as config
import src.audio as audio
import src.utils as utils
from src.inference import infer
import os
from pynput.keyboard import Key, Listener


def user_input(config):
    """
    Returns the user input either by using keyboard input
    or by letting the user speak and using speech recognition
    """

    # If the program is configured to work with the microphone
    if config.AUDIO_INPUT:
        print(colored(f'{config.USER_NAME}: ', "yellow") +
              colored("### 🤫 PRESS SPACE TO RECORD ####", "white"))

        with Listener(
            on_press=audio.recorder_handler
        ) as listener:
            listener.join()

        message = audio.voice_input
        return message

    # Else use a simple keyboard input
    else:
        message = input(colored(f"{config.USER_NAME}: ", "yellow"))
        return message


def generate_response(config, full_prompt, seed):
    """
    Generating a response using Bloom inference to autocomplete
    the conversation given the prompt
    """

    # We start by infering by adding a new line starting with BOT_NAME:
    resp = infer(f"{full_prompt}\n{config.BOT_NAME}: ", seed)

    # We then get the response's generated text which contains the full_prompt
    # until now and remove the previous part to only keep the new response
    response = resp[0]["generated_text"].split(
        f'{config.BOT_NAME}:')[-1].strip()

    # We also make sure to remove new line for the user if Bloom added some
    response = response.split(config.USER_NAME)[0]
    response = f'{config.BOT_NAME}: {response}'

    response = utils.punctuation_cut(response)

    if response is None:
        return generate_response(config, full_prompt, seed + random.randint(0, 9999))

    return response


def discussion(config, prompts, seed):
    """
    Main function of the program, handles the loop between the user and the chatbot.
    This function works recursively.

    This function always start by generating a bot message and then ask the user
    for a response.
    """

    # Generating a bot response

    # The full conversation until now
    full_prompt = "\n".join(prompts)

    # We generate a response from the chatbot using Bloom inference
    bot_response = generate_response(config, full_prompt, seed)

    if config.AUDIO_OUTPUT:
        utils.clear_previous_console_line()
    print(colored(bot_response.replace('\n', ''), "green"))
    prompts.append(bot_response)

    # If AUDIO_OUTPUT is set to true
    # play the audio of the response using text to speech
    if config.AUDIO_OUTPUT:
        audio.text_to_speech(bot_response.split(config.BOT_NAME)[1].strip())

    # Asking the user for a response
    message = user_input(config)

    # The new prompt added by the user is added to the prompts until now
    new_prompt = f"{config.USER_NAME}: {message.strip()}"
    prompts.append(new_prompt)

    # We start a new round of discussion
    discussion(config, prompts, seed)


def initialize(config):
    """
    A function to initialize the conversation
    """
    prompts = [config.SCENARIO]
    seed = random.randint(0, 99999)

    # clear the console
    os.system('clear')

    # Audio input instructions
    if config.AUDIO_INPUT:
        print(colored('-' * 45 + "\nAudio controls:\n- Press SPACEBAR to record or re-record (while the message is in cyan)\n- Press ENTER to validate your message (when the message is in cyan)\n" + '-' * 45 + '\n', "red"))

    # Print the context prompt
    print(colored(f"\x1B[3m {prompts[0]} \x1B[0m", "blue"))

    # In case the user needs to start the conversation
    if config.FIRST_MESSAGE_USER:
        message = user_input(config)

        # The new prompt added by the user is added to the prompts until now
        new_prompt = f"{config.USER_NAME}: {message.strip()}"
        prompts.append(new_prompt)

    discussion(config, prompts, seed)


initialize(config)
