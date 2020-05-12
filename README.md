# Discord-Reaction-GeneratorBOT
A discord - reaction based generator bot, which takes a random line from a file in a folder and sends it to users who reacts on the message. With an inbuilt optional cool-down system.

# Download
- You can download this directly from the command line using the following command: 
- "git clone https://github.com/4-04/Discord-Reaction-GeneratorBOT/"
- Once downloaded, edit the config.json file, and run the 'main.py' file.

# How to use
- This bot is very simple to set up and use.
- As explained earlier, when you have downloaded it you have to edit the config.json file with your desired settings (optional), but you will have to edit the token and prefix in order for the bot to run, otherwise it may cause an error.
- When you are done with that you will have to configure the bot as you would like. The files for each gen type has to be inside a folder 
that starts with "gen_", for example: "gen_premium", now the bot will automatically enable the command (prefix)start premium. And all the files inside that folder will be automatically be recognized for the bot as valid files. 

# Important
- Each line in the files inside the gen_(whatever) folders can be whatever you would want too, EXCEPT for the line number 1 and 2. In the line number 1 it has to be the emoji id of the reaction type for that file. For instance a filed name movies1.txt, inside the folder gen_movies, would have the first line as the emoji id you want to have for someone to react on that message. 
- The second line has to be the cooldown for that gen, if you want no cooldown simply set that line to 0.
- So inside movies1.txt it would look something like this:
 "line1 : <@emoji_for_this_file>
  line2 : 30
  line3 : ....
  line4 : ......
"""
- If you fail to meet theese requirements the bot may make an error
