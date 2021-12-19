# phishing login
## Features
 - ecnrypted admin page
 - beginners friendly
 - custom link name for victim
 - latest google and instagram pages
 - easy custom site adding
## Installation
 - clone repository
 ```
 git clone https://github.com/srneckuba/phishing_login.git
 ```
 - go to cloned repository
 ```
 cd phishing_login/
 ```
 - install python3 and pip
 ```
 apt-get install python3 python3-pip
 ```
 - install requirments
 ```
 pip3 install -r requirements.txt
 ```
## usage
### configuration
- edit main.config
```
local_server_adress=127.0.0.1;                    #local network adress
internet_server_adress=127.0.0.1;                 #leave same as local_server_adress if you are not port fowarding
server_directory=/home/srneckuba/phishing_login/; #full path to server directory
sleep_time=1;                                     #time to wait between checks for admin input 1 is recomended
max_time=10;                                      #maximum time for reaction in admin panel 10 is a enough for checking if victim's input is correct 
admin_password=example1;                          #password for opening admin admin page
encryption_password=example2;                     #password for decrypting admin page
```
### runing and using
```
python3 main.py main.config
```
#### open admin page
- open http://internet_server_adress/admin?password=admin_password in browser. With example values from main.config http://127.0.0.1/admin?password=example1
- after opening url you should see one input box. Enter encryption_password and click outside input box. If you entered correct encryption password you should see empty table
#### prepare link for victim 
- link is in format http://local_server_adress/?network=network&name=link_name. Network should be google or instagram and link_name should be some identification of  victim. With example values from main.config http://127.0.0.1/?network=google&name=victim1
#### action
- after victims open his link http://127.0.0.1/?network=google&name=victim1 you should see new table row in admin panel
- in table you should see random generated cookie, victim's ip adress, network, name and some empty columns
##### step number 1
- first google page is email or username input
- after victim entered email you shoud see it in table in column with name step1.
- you now have 10 seconds to decide if email is correct or not. (you can change max_time for different time than 10 seconds)
- after 10 seconds automatic value will be used. (automatic value is under column name and you can change it by clicking on it).
- if victim's input is incorrect victim must enter email again and whole proccess is repeating until you select that input is correct.
##### step number 2
- second google page is password input
- after victim entered password you shoud see it in table in column with name step2.
- you have 10 seconds to decide if password is correct or not. (you can change max_time for different time than 10 seconds)
- after 10 seconds automatic value will be used. (automatic value is under column name and you can change it by clicking on it).
- if victim's input is incorrect victim must enter password again and whole proccess is repeating until you select that input is correct.
- after selecting that input is correct you have 10 seconds to decide if step number 3 is needed (step number 3 is 2 factor authetification) 
- after 10 seconds automatic value will be used. (automatic value is under column name and you can change it by clicking on it).
- if you selected that you dont't need step number 3 victim will be redirected to final_content.html
##### step number 3
- third google page is 2 factor autentification
- process is still same after victim's input you have 10 seconds to decide if 2FA code is correct
- if not victim must enter code again
##### controll
- if there are some extra rows without link_name you can click on DEL in last column to delete them
