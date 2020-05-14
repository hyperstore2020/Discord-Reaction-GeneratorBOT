# Discord-Reaction-GeneratorBOT
A discord - reaction based generator bot, which takes a random line from a file in a folder and sends it to users who reacts on the message. With an inbuilt optional cool-down system.

# Download
- You can download this directly from the command line using the following command: 
- "git clone https://github.com/4-04/Discord-Reaction-GeneratorBOT/"
- Once downloaded, edit the config.json file, and run the 'main.py' file.
- Alternatively you can download theese files manually by clicking the "download now" button on Github.

# How to use
- This bot is very simple to set up and use.
- As explained earlier, when you have downloaded it you have to edit the config.json file with your desired settings (optional), but you will have to edit the token and prefix in order for the bot to run, otherwise it may cause an error.
- When you are done with that you will have to configure the bot as you would like. The files for each gen type has to be inside a folder 
that starts with "gen_", for example: "gen_premium", now the bot will automatically enable the command (prefix)start premium. And all the files inside that folder will be automatically be recognized for the bot as valid files. 

# Important
- Each line in the files inside the gen_(whatever) folders can contain whatever lines you would want to, EXCEPT for the line number 1 and 2. 
- The line number 1 in the file has to be the emoji ID, that you wish to use for that file. 
- The second line has to be the cooldown in seconds for that specific file, if you want no cooldown simply set that line to 0.
- The bot will automatically exclude the first two lines when sending a random line to the user. 
- (you can get the emojis on Discord by typing \ before sending the emoji in chat) (an emoji ID looks something like this <:test_emoji:710171225267372144>)

- If you fail to meet theese requirements the bot may raise an  error
