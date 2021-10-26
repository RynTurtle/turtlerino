
# todo: if a word is wrapped by quotes then treat it like an emote and do not capitilise it
# e.g. HeLoO GuYs Pepege (so you can type emotes with the setting enabled and not have them ruined by it)
# or have a list of emotes from ffz/7tv/bttv combined and check if its there then dont capitilise it


def pepege(message):
    number_for_letters = 0 
    new_message = []
    for letters in message:
        number_for_letters += 1

        if number_for_letters % 2 == 0: # if its even
            new_message.append(letters.upper())
        else:
            new_message.append(letters.lower())

    return "".join(new_message)
