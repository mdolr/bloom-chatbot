def clear_previous_console_line():
    print(
        "\033[A                                                           \033[A")


def punctuation_cut(message):
    """
    A function to cut the message to the last punctuation
    """

    if message[-1] in [".", "!", "?"]:
        return message

    # In case the bot starts to repeat the context prompt
    if '*' in message:
        return message.split('*')[0] + '.'

        # Else If we find punctuations cut the sentence on the last punctuation
    elif '!' in message:
        return '!'.join(message.split('!')[:-1]) + '!'
    elif '?' in message:
        return '?'.join(message.split('?')[:-1]) + '?'
    elif '.' in message:
        return '.'.join(message.split('.')[:-1]) + '.'
    elif ',' in message:
        return ','.join(message.split(',')[:-1]) + '.'
