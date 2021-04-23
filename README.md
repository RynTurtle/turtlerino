# 🐢 turtlerino 🐢

## **turtlerino is a twitch chat tool used to enhance a users experience on the platform.** 

[image example](https://i.imgur.com/HilfahP.png)

## To begin I would highly recommend for you to research on ratelimits that twitch has **[here](https://dev.twitch.tv/docs/irc/guide#command--message-limit).**


turtlerino spam based commands are only for channels that you are mod/vip in (no delay in messages) basic commands and the rainbow feature will work in most chats.

Most of the tools are in the form of textboxes like this: [] [x] they are unchecked  on default so you dont accidently do something you dont want to.
Sliders are also used, the one underneat spam burst is the amount of lines you want to send into chat and the one underneath all of the rainbow boxes is how often you want to send /color. 

To start off you need to add your oauth (this is basically a unique password to send messages to chat) [here](https://twitchapps.com/tmi/) **do not show this to anyone**
In the text file "account_options" copy and paste your oauth into this making sure it only says oauth: one time.
Once you have done that you can now run the file called turtlerino 
The box at the top is where you write what channel you want to send to **turtoise** for example.
The box at the bottom is where you send all your messages, If you would like to spam singular messages check spam burst and leave the line count as 1 then hold enter.




| Checkboxes | What they do |
| -------- |------------- |
| spam burst | uses multiple connections to send messages in chat super quick | 
| colour per msg | every time you send a message in chat it will change your username colour (prime+ members only) |
| rainbow | enables non prime changing colour every specified amount of seconds on the slider |
| prime | enables sending a hex code in a rainbow order instead of it being random default twitch colours |
| /me | sends every message received from the texbox with /me infront 


**There are also custom commands built into the chatbox**

/pyramid (amount) (message) sends a pyramid in chat with a max character of 500 if its more than that it wont send into chat preventing a half pyramid to send. 
/trihard will send TriHard 7 into chat

To add custom commands you will need to click settings there you will find a command: and then a textbox with / already entered in. To create a valid command you need to type (command)(space)(message to send) and then press enter, close the settings window, type out your command in chat and enjoy :) 

There is not a way to delete a command yet as a button so if you really want to delete a command open the commands file with notepad or any text editor and make sure when deleting a command the formatting of {command: message to send} is still correct or you may risk it being invalid.

Windows may detect turtlerino as a virus. This is because it has an untrusted unsigned exe which would cost a yearly payment which im not willing to do. If you would not want this message disable your antivirus or run the main_gui python file instead of turtlerino.exe, the files and what they do are all there so if you do not trust the program you can see everything that it does.



