<h1>MakiMessenger [REWORK]</h1><br>
This is bs and process of learning code, code is not structured planned and poorly written <br>
An messenger that allows users to communicate to each other in a local network setting.<br> [7,810 Files, 917 Folders] [180 MB]<br>
This is a proof of concept don't rely on this as an secure option, because it is not.
<hr>
<span style='color:red'><strong>[There is currently limited functionality and works partially, this is currently in development during COVID19 and will be completed soon, thanks.]<br>
[FIREWALL PROBLEMS][If you are getting a Timeout Error please disable firewall on PORT 5050 for python.exe/ maki_messenger.exe.]</span></strong>
<hr>
<h4>Introduction</h4>
This program has a client and server script in which one computer has to be a dedicated server in which will save changes and accounts, etc.
<br>
<hr>
<h4>Start Up</h4>
When starting the program, a login/registration window will appear in which you can sign in or register. This will be cross-checked with the server database, which is a persistent log on that specific computer. If you decide to change the location of the server to another computer, you must copy the database file and note down the IP of the new computer. Please note that there is no password recovery, please ask your admin for the password.
<br>
<p align="center">
  <img src='https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/program_preview.PNG' width=400>
</p>
<hr>
<h4>Main Usage</h4>
<i>Once you registered and logged in, there are 3 main sections to look out for, these include:</i>
<hr>
<br><strong>Live User Window</strong>
<br>This is located in the top left of the window and will show you the people that are currently on the app and connected to the server, these will be users on the same network as you. They all have an option to be added to your friends' list, with the button "Add" on the contacts name.
<hr>
<br><strong>Contacts List</strong>
<br>This is located in the left bottom of the window and will include users that you have added to your contacts list, this will be tied to your account and will be persistently stored on the server and client. You can initiate a chat with any user in your contacts list by just clicking on their name on this window. Note that there isn't any friend requests and anyone can communicate with anyone, however, if you do not want to communicate with this user you have the option to block.
<hr>
<br><strong>Message Content Box</strong>
<br>By default this will relay all comments posted in a type of 'group chat' containing all known users, this chat will not be saved locally but will be saved on the server-side. You have the option to keep these logs for a min of a day. If you click on a user that you have added as a friend a chat will be initiated between you 2 clients and saved locally permanently and server-side temporarily. There is currently no option to delete comments from chats so beware. Text and emojis are currently only supported. Images and GIFS will eventually have added functionality.
<p align="center">
  <img src='https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/day4_finalv2.PNG' width=400>
</p>
<hr>
<br><strong>Server-Side</strong>
<br>There is currently no GUI for the server-side, but you can access the main server script through the shell. Just initiate the script to start it.
The server package comes with the server script to run locally.
But also the file 'database.csv' which stores users' credentials and SHA-256 hash.
Added functionality will be included, with such commands to ban users for a set period of time, and set admin priveledges to select users, etc.
<br> GUI will be added eventually but will be very rudimentary, thanks.
<hr>
<br><strong>Server-Side (lite) v1</strong>
<br>This version of the server will run natively on a electronic module such as the ESP8266, where a mini network can
be set up and you can communicate with people on the same network. This will not gurantee you a secure messaging app.<br>
<hr>
<br><strong>Security Features</strong>
<br>I aim to make this program as secure as possible, but you may wish to increase security by making the network password, a long, unguessable passphrase, you can obtain one from the website <a href='https://www.rempe.us/diceware/#eff'> here.</a>
<br>Im reviewing the module Cryptography to improve security of this app.
<br><i>Network Security Features Include:</i>
<ul>
  <li>4 Layer Encryption [development]</li> 
  <li>Use of DH Key Exchange [DONE]</li>
  <li>4096-bit Private Keys [DONE]</li>
  <li>E2EE Encryption [development]</li>
  <li>Passwords Stored in SHA-256 [DONE]</li>
  <li>Asymmetric Encryption [development]</li>
  <li>Email Validation [DONE]</li>
  <li>2-Factor Authentication [DONE]</li>
  <li>Encrypted Chat Files [development]</li>
  <li>Input Injection [continous]</li>
  <li>(Optional) Automated Google Drive File Backup [development]</li>
</ul>
<br>Futhermore I do intent to add a layer of complexity and security with the use of common sense in a sort of point system.
<br>This includes making sure the user is in an known location, the device is recognised by device's MAC address, the screen size match and timezones.
<hr>
<br><strong>Features</strong>
<br>I want to add the feature chats can be saved in Google Drive Backups (optional).
<br>But also have the option for it to be stored on a centralised server (host).
<hr>
<br><strong>Acknowledgements</strong>
<br>desklamp2 - Diceware Link
<br>--> https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
<br>--> https://cryptography.io/en/latest/hazmat/primitives/
<br>--> https://docs.python.org/3/library/tkinter.html
<br>--> https://hackernoon.com/10-common-security-gotchas-in-python-and-how-to-avoid-them-e19fbe265e03
<br>--> https://effbot.org/tkinterbook/canvas.html
<br>--> https://github.com/amiralis/pyDH
<br>--> https://nitratine.net/blog/post/encryption-and-decryption-in-python/
<br>--> https://wiki.mozilla.org/Security/Server_Side_TLS
<br>--> https://github.com/pyca/pyopenssl
<br>--> https://www.websecurity.digicert.com/en/uk/security-topics/what-is-ssl-tls-https
<hr>
<br><strong>Rework Av1.0.0</strong>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Working/clientv2.PNG", width=400>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/server_config_window.PNG", width=400>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Resources/loading.png", width=400>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Working/plan.png", width=700>
</p>
<hr>
<br><strong>Security</strong>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/maki_slide1.png", width=700>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/maki_slide2.png", width=700>
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/Pictures/maki_slide3.png", width=700>
</p>
<hr>
<br><strong>Android App [development]</strong>
<!-- https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/AndroidApp/flow1.gif -->
<p align="center">
  <img src="https://raw.githubusercontent.com/makiisthenes/MakiMessenger/master/AndroidApp/flow1.gif", width=350>
</p>
TODO: Android App Development<br>
These are things required in order to complete the MakiMessenger App:<br>
Android App <br>
<ul>
  <li>Gallery Image Selection Properly Implemented with Firebase</li>
  <li>Show Image with Cropped Circle Lining</li>
  <li>Email and Password are Stored in Backend with MongoDB</li>
  <li>Persistant Storage of Username and Password</li>
  <li>WebSocket Properly Implemented</li>
  <li>Making Sure Only 3 Email Resend Requests can be made in a 3min Period.</li>
  <li>Making an local SQLite DB for Chats Saves.</li>
  <li>External Saves for Photos and Videos</li>
  <li>Saved Instances between Activities</li>
  <li>Analytical Tools</li>
  <li>Recycler View Implementation</li>
  <li>Json Parser and Array Append</li>
  <li>Activity Intent Parameters</li>
  <li>Signal Protocol for Messaging</li>
  <li>Maybe Addition of OAuth2 for Google, Twitter</li>
</ul>
