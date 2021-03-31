from tkinter import *
import twitch_spam as spam
import json
import twitch_irc as twitch
import random
with open("commands.json") as custom_commands_file:
    custom_cmd = json.load(custom_commands_file)

commandslist = ["/pyramid",]

root = Tk(className="turtlerino")
root.geometry("350x350+900+4")  # width x height, position of window width height
root.config(bg="#212121")  # TriKool
root.iconbitmap('icon.ico')  # icon top left


chan_entry = Entry(root, background="#1E1E1E",foreground="white",borderwidth=1)
chan_entry.place(width=100, height=30, relx=0.5, rely=0.0, anchor="n") # south
# send to chan_entry.get()  (the channel listed there it will send to)


def entry_box_send(keypress):
    message = str(e.get())
    channel = str("#" + chan_entry.get())
    if e.get() == "":  # if the text box has nothing in it do nothing
        pass
    else:
        for commands in commandslist:
            if commands in e.get():
                twitch.commands(message, channel, slash_me_answer.get(),color_each_msg_answer.get())  # handle the commands
        if e.get() in custom_cmd:
            if spam_answer.get() == "On":
                twitch.custom_commands(message, channel, slash_me_answer.get(),color_each_msg_answer.get())  # handle the custom commands
            else:
                e.delete(0, "end")  # delete entry box
                twitch.custom_commands(message, channel, slash_me_answer.get(),color_each_msg_answer.get())  # handle the custom commands
        else:
            if spam_answer.get() == "Off":  # if spam is disabled
                e.delete(0, "end")  # then delete entry box
                if message.startswith("/"):
                    twitch.send(message, channel, "Off",color_each_msg_answer.get())  # if command detected send it without /me
                else:
                    twitch.send(message, channel, slash_me_answer.get(),color_each_msg_answer.get())  # send one message

                # if its not disabled then the entry box wont be deleted
            else:
                # when using the spam command in entry box it will use all the sockets in the list and send the message
                starting_number = 0
                burst_spam_amount = horizontal.get()
                while True:
                    for all_sockets in spam.sockets():
                        if starting_number == burst_spam_amount:  # if the burst amount is sent then stop.
                            return
                        starting_number += 1
                        if color_each_msg_answer.get() == "On":
                            twitch.rainbow("On",channel,slash_me_answer)

                        if slash_me_answer.get() == "On":
                            if not message.startswith("/"):  # wont send commands with /me enabled
                                spam.sendRaw_as_spam("PRIVMSG " + channel + " :/me " + message, all_sockets)  # send the same message over all sockets with /me

                            else:
                                spam.sendRaw_as_spam("PRIVMSG " + channel + " :" + message,all_sockets)  # send the same message over all sockets without /me (for commands)

                        else:
                            spam.sendRaw_as_spam("PRIVMSG " + channel + " :" + message, all_sockets)  # send the same message over all sockets without /me


def command(text_box):  # example: /trihard TriHard 7 (command  then space then what you want the command to send)
    global custom_cmd
    command = command_name_entry.get().split(" ")
    command_name = command[0]
    what_to_send = command[1:]
    what_to_send = " ".join(what_to_send)
    a_dict = {command_name: what_to_send}

    with open('commands.json') as f:
        data = json.load(f)

    data.update(a_dict) # updates json file

    with open('commands.json', 'w') as f: # writes the new data in the file
        json.dump(data, f)


    with open("commands.json") as custom_commands_file:
        custom_cmd = json.load(custom_commands_file)



def settings():
    global command_name_entry
    root = Tk(className="settings")
    root.geometry("250x250+900+4")  # width x height, position of window width height
    root.config(bg="#212121")  # TriKool
    command_name_label = Label(root, text="Command:")
    command_name_label.place(width=95, height=30, relx=0.0, rely=0.0, anchor="nw")
    command_name_entry = Entry(root, background="#1E1E1E", foreground="white", highlightcolor="black",borderwidth=1)
    command_name_entry.insert(0,"/")
    command_name_entry.bind('<Return>', command)
    command_name_entry.place(width=70, height=30, relx=0.4, rely=0.0, anchor="nw")


e = Entry(root, background="#1E1E1E", foreground="white", highlightcolor="black",borderwidth=1)   # using e.get will get the sentence within the entry box
e.place(width=350, height=45, relx=0.5, rely=1.0, anchor="s")  # south

root.bind('<Return>', entry_box_send)


spam_answer = StringVar()  # the answer of whether or not spamming is enabled is a string(on,off)
c = Checkbutton(root, text="spam burst?",variable=spam_answer, onvalue="On", offvalue="Off", background="#1F1F1F", foreground="red", activebackground="red")
c.deselect()  # deselects the box by default
c.grid(column=0, row=2)


rainbow_answer = StringVar()  # the answer of whether or not spamming is enabled is a string(on,off)
c2 = Checkbutton(root, text="rainbow?",variable=rainbow_answer, onvalue="On", offvalue="Off", background="#1F1F1F", foreground="orange", activebackground="orange")
c2.deselect()  # deselects the box by default
c2.place(relx= 0.999, rely = 0.11, anchor="e")

prime_answer = StringVar()  # the answer of whether or not spamming is enabled is a string(on,off)
c3 = Checkbutton(root, text="prime?",variable=prime_answer, onvalue="On", offvalue="Off", background="#1F1F1F", foreground="yellow", activebackground="yellow")
c3.deselect()  # deselects the box by default
c3.place(relx= 0.999, rely = 0.17, anchor="e")

slash_me_answer = StringVar()  # the answer of whether or not spamming is enabled is a string(on,off)
c4 = Checkbutton(root, text="/me?",variable=slash_me_answer, onvalue="On", offvalue="Off", background="#1F1F1F", foreground="green", activebackground="green")
c4.deselect()  # deselects the box by default
c4.place(relx= 0.999, rely = 0.24, anchor="e")

color_each_msg_answer = StringVar()
c5 = Checkbutton(root, text="colour per msg?",variable=color_each_msg_answer, onvalue="On", offvalue="Off", background="#1F1F1F", foreground="red", activebackground="red")
c5.deselect()  # deselects the box by default
c5.place(relx= 0.999, rely = 0.01, anchor="ne")


horizontal_rainbow = Scale(root, from_=1, to=30, orient=HORIZONTAL,length=86,background="#212121", foreground="blue", activebackground="blue")
horizontal_rainbow.config(highlightbackground="#212121",length=45)
horizontal_rainbow.place(relx=0.999, rely=0.35, anchor="e")


horizontal = Scale(root, from_=1, to=100, orient=HORIZONTAL,length=86,background="#212121", foreground="red", activebackground="red")
horizontal.config(highlightbackground="#212121")
horizontal.grid(column=0, row=3)

setting_button = Button(root, text="Settings",pady=1,padx=1, command=settings,background="#212121", foreground="white", activebackground="white")  # changes size of button and name of it
setting_button.place(relx=0.0, rely=0.87, anchor="sw")


def timer_rainbow():
    counter = 0
    channel = str("#" + chan_entry.get())
    if counter < 10:
        if rainbow_answer.get() == "On":
            if prime_answer.get() == "On":
                twitch.rainbow(rainbow_answer.get(), channel, slash_me_answer.get())
            else:
                pleb_colours = ['Blue', 'BlueViolet', 'CadetBlue', 'Chocolate', 'Coral', 'DodgerBlue', 'Firebrick', 'GoldenRod', 'Green', 'HotPink', 'OrangeRed', 'Red','SeaGreen', 'SpringGreen', 'YellowGreen']
                try:
                    twitch.sendcommand("/color " + random.choice(pleb_colours), channel)
                except:
                    pass

        counter += 1
        root.after(horizontal_rainbow.get() * 1000, timer_rainbow)  # milliseconds


timer_rainbow()
root.mainloop()
