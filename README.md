# 🐢 turtlerino 🐢

## **turtlerino is a twitch chat tool used to enhance a users experience on the platform.** 

###### [image example](https://i.imgur.com/3sZZasx.png)

###### If you have any issues or requests you can contact me on twitch: @turtoise and discord: Turtoise#6731 




**How to download**

Click the big green code button and then click download zip, then unzip the file


**How to begin**

To start off you need to use an oauth, this is like a password to only allow sending messages to twitch and nothing else. To get this open turtlerino.exe and click the cogwheel, when you click this 3 options pop up, click "login" and then click the link. This will generate the oauth needed. Enter the oauth into the input box and then press enter. Now you can send messages into channels!


**How to send messages** 

When opening turtlerino there will be 3 key stages when sending a message which are:
1. channel box - This is where you put the channel you want your messages to send to 

2. ratelimit - This is how fast you want the gap between each message to be (default 1100 ms = 1.1seconds) [Follow the twitch ratelimits](https://dev.twitch.tv/docs/irc/guide#rate-limits)  if you are a vip/mod then 110 ms will be the correct amount to set it to. If you want to send a message every hour or so then just convert the hour into milliseconds and put it in there. 
 
3. message box - This is where you type what you want to send into a channel  - This can contain custom commands, built in commands and tags, e.g. /pastebincommand or /pyramid 50 TriHard or TriHard * WideHard * WideHardo 

4. ctrl + enter - This is a keybind that is used to spam messages based on the ratelimit set 


**Checkboxes** 
*Open to checkbox suggestions* 
Checkboxes are shown on the main window of turtlerino - these are all  options you can use that will edit the original message that is going to be sent to a channel. 

The current checkboxes right now are: 

| Checkbox name | What it does |
|---------------|--------------|
| Rainbow per message | sends /color in rainbow hex codes based on your settings (prime or turbo) |
| Rainbow timer | sends /color in rainbow hex codes based on the seconds set in settings (prime or turbo) |
| /me | adds /me infront of your message |
| Pepege mode | capitalizes every other letter |
| MrDestructoid | converts your message to binary |

**commands** 

When opening the commands window you will see a table of each command and what they will send, theres 3  options which are: 

1. new or previous command name - This is what you want your command to be called (can be anything) or what command you want to edit (will replace the original message) 
2. new message - This will be what the command reacts to, command messages can be text with  newlines and also a pastebin link (examples are shown) press enter on this input box and it will add the command name and the message.
3. remove command - This will remove the command name and what it was going to send when pressing enter

1. "*" = newline (can be used as a command and also in the message box raw)
2. "*{RAINBOW}" = newline with rainbow (can be used as a command and also in the message box raw)
3. "{1}" = insert the first word after the command e.g. the input of /insertcommand nice which has "have a {1} day" tied to it will send have a nice day 

**rainbow settings** 
This is where you set what you want your username rainbow colours to look like (if you have the colour per message ticked) and how often you want to change your colour (if you have the colour timer ticked)

Here you will find multiple input boxes buttons and sliders, use the slider to set the start and end values, then you can set what you would like it to increase by each message (if you dont want one value to increase or decrease then set it to 0) 

Hue has an increase and a decrease value to make the rainbow smoother going forwards up to the end hue and then backwards back to the start hue.

There are also definitions on what each value means which will help explain what they do to help you create what type of user colour you want. 


