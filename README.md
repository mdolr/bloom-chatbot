# Bloom Chatbot

A chatbot built with the Bloom open-source model inspired by sentdex work and re-used later for a class project

## Setup

1. `git clone`
2. `cd bloom-chatbot`
3. `pip install -r requirements.txt`
4. Edit `src/config.py` to your liking
5. `python main.py`

## Configuration

You can use the `src/config.py` file to change the settings of the chatbot.

The `SCENARIO` variable is the initial prompt that is given to the model for it to get some context. It should describe in which context does the conversation occurs and who are the different actors.

`BOT_NAME` and `USER_NAME` respectively represent the name of the bot and the name of the user within the conversation. They will be prefixed before every message of the discussion.

`AUDIO_OUTPUT` is a boolean that indicates whether the bot should use text to speech for its response.

`AUDIO_INPUT` is a boolean that indicates whether the user should input using speech recognition -> This setting is useful if you try to practice pronounciation in a different language for example.

`LANGUAGE` and `AUDIO_LANGUAGE` are the language of the conversation and the language of the audio output. They should be set to the same value if you want to use both audio features.

- `AUDIO_LANGUAGE` should be set to a BCP-47 from [Google documentation](https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages?hl=fr)
- `LANGUAGE` should be set to a language code like 'en', 'fr', ...

## License

[Bloom](https://huggingface.co/bigscience/bloom) is an open-source model distributed under its specific license, your use of this software should align with the license of the model.

I am not responsible for any results and/or damages caused by the use of this software.
