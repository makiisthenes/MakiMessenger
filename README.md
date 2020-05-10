<h1>MakiMessenger</h1><br>
An messenger that allows users to communicate to each other in a local network setting.
<hr>
<span style='color:red'><strong>[There is currently limited functionality and works partially, this is currently in development during COVID19 and will be completed soon, thanks.][If you are getting a Timeout Error please disable firewall on port 5050 for python.exe or connect to an vpn.]</span></strong>
<hr>
<h4>Introduction</h4>
This program has a client and server script in which one computer has to be a dedicated server in which will save changes and accounts, etc.
<br>
<hr>
<h4>Start Up</h4>
When starting the program, a login/registration window will appear in which you can sign in or register. This will be cross checked with the server database, which is a persistant log on that specific computer. If you decide to change the location of the server to another computer, you must copy the database file and note down the IP of the new computer. Please note that there is no password recovery, please ask your admin for the password.
<br>
<p align="center">
  <img src='https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/program_preview.PNG' width=400>
</p>
<hr>
<h4>Main Usage</h4>
<i>Once you registered and logged in, there are 3 main sections to look out for, these include:</i>
<hr>
<br><strong>Live User Window</strong>
<br>This is located in the top left of the window and will show you the people that are currently on the app and connected to the server, these will be users on the same network as you. They all have an option to be added to your friends list, with the button "Add" on the contacts name.
<hr>
<br><strong>Contacts List</strong>
<br>This is located in the left bottom of the window and will include users that you have added to your contacts list, this will be tied to your account and will be persistantly stored on the server and client. You can initiate a chat with any user in your contacts list by just clicking on thier name on this window. Note that there isnt any friend requests and anyone can communicate with anyone, however if you do not want to communicate with this user you have the option to block.
<hr>
<br><strong>Message Content Box</strong>
<br>By defualt this will relay all comments posted in an type of 'groupchat' containing all known users, this chat will not be saved locally but will be saved on the server-side. You have the option to keep these logs for a min of a day. If you click on a user that you have added as a friend a chat will be initaited between you 2 clients and saved locally permanently and server-side temporarily. There is currently no option to delete comments from chats so beware. Text and emojis are currently only supported. Images and GIFS will eventually have added functionality.
<p align="center">
  <img src='https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/day4_finalv2.PNG' width=400>
</p>
<hr>
<br><strong>Server-Side</strong>
<br>There is currently no GUI for the server side, but you can access the main server script through the shell. Just initiate the script to start it.
The server package comes with the server script to run locally.
But also the file 'database.csv' which stores users credentials and SHA-256 hash.
Added functionality will be included, with such commands to ban users for a set period of time, and set admin priveledges to select users, etc.
<br> GUI will be added eventually but will be very rudimentary, thanks.
