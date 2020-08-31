<h1 align="center">sanctuary-zero</h1>
<p align="center">A command-line bound implementation of secure synchronous lightweight chatroom with zero logging and total transience built using WebSockets, Fernet Cryptography, Asyncio and Prompt Toolkit</p>

<p align="center">
    <img src="https://img.shields.io/github/issues/t0xic0der/sanctuary-zero?style=flat-square&logo=appveyor&color=teal">
    <img src="https://img.shields.io/github/forks/t0xic0der/sanctuary-zero?style=flat-square&logo=appveyor&color=teal">
    <img src="https://img.shields.io/github/stars/t0xic0der/sanctuary-zero?style=flat-square&logo=appveyor&color=teal">
    <img src="https://img.shields.io/github/license/t0xic0der/sanctuary-zero?style=flat-square&logo=appveyor&color=teal">
</p>

## Good news
This project is now listed in the [Projects using Python Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).

## Features
1.  Provides real-time conversation using synchronous WebSocket objects
2.  Incredibly lightweight with memory usage as low as just 4MB over Python runtime
3.  Restricted console refresh rate and native support for SSH, CHROOT and RDP
4.  Zero logging or data storage to minimize database vulnerabilities
5.  Accessible across internet with both IPv4 and IPv6 support by-design
6.  No-frills user alias and random-generated keys for chatroom creation
7.  Hardened protection using password-based Fernet symmetric-key cryptography
8.  Transient chatrooms stay valid as long as at least one user is present
9.  State-of-the-art active chatroom and user session management
10. Convenient userlist and casted message history maintenance
11. Maintain low profile and avoid detection by limiting network activity to a minimum
12. Prevent continuous polling by optimizing message transfers on said events

## Usage
### Server setup
- Install `python3` and `pip` with your GNU/Linux distribution-specific package managers.
- Install and upgrade `virtualenv` if not already done.
```
$ pip3 install virtualenv --user
```
- Clone the repository on your local storage and make it your current working directory.
```
$ git clone https://github.com/t0xic0der/sanctuary-zero.git
$ cd sanctuary-zero
```
- Create and activate the virtual environment.
```
$ virtualenv venv
$ source venv/bin/activate
```
- Install all dependencies for the project.
```
(venv) $ pip3 install -r requirements.txt
```
- Run the **Sanctuary Zero Server** with the tweakable options shown below.
```
(venv) $ python3 main.py --version
SNCTRYZERO Server by t0xic0der, version 19082020
```
```
(venv) $ python3 main.py --version
(venv) $ python3 main.py --help
Usage: main.py [OPTIONS]

Options:
  -c, --chatport TEXT  Set the port value for the server [0-65536]  [required]
  -6, --ipprotv6       Start the server on an IPv6 address  [required]
  -4, --ipprotv4       Start the server on an IPv4 address  [required]
  --version            Show the version and exit.
  --help               Show this message and exit.
```
```
(venv) $ python3 main.py -c 9696 -4
[10:35:18] SNCTRYZERO ⮞ Starting SNCTRYZERO v19082020...
[10:35:18] SNCTRYZERO ⮞ IP version : 4
[10:35:18] SNCTRYZERO ⮞ SNCTRYZERO was started up on 'ws://0.0.0.0:9696/'
[10:45:57] USERJOINED ⮞ m3x1c0@37777D41
[10:51:24] USEREXITED ⮞ m3x1c0@37777D41
```

### Client setup
- Make sure that the **Sanctuary Zero Server** is running and is reachable.
- On another computer in the same network (applicable for both IPv6 and IPv4 options) or in a different network (applicable for a general IPv6 option or a forwarded IPv4 option), open up a terminal.
- Install `python3` and `pip` with your GNU/Linux distribution-specific package managers.
- Install and upgrade `virtualenv` if not already done.
```
$ pip3 install virtualenv --user
```
- Clone the repository on your local storage and make it your current working directory.
```
$ git clone https://github.com/t0xic0der/sanctuary-zero.git
$ cd sanctuary-zero
```
- Create and activate the virtual environment.
```
$ virtualenv venv
$ source venv/bin/activate
```
- Install all dependencies for the project.
```
(venv) $ pip3 install -r requirements.txt
```
- Run the **Sanctuary Zero Client** with the tweakable options shown below.
```
(venv) $ python3 cnew.py --version
SNCTRYZERO Client by t0xic0der, version 19082020
```
```
(venv) $ python3 cnew.py --help
Usage: cnew.py [OPTIONS]

Options:
  -u, --username TEXT  Enter the username that you would identify yourself with  [required]
  -p, --password TEXT  Enter the chatroom password for decrypting the messages
  -c, --chatroom TEXT  Enter the chatroom identity you would want to enter in
  -s, --servaddr TEXT  Enter the server address you would want to connect to [required]
  --version            Show the version and exit.
  --help               Show this message and exit.
```
- Create a new password-protected chatroom using the following and share the chatroom identity and password for others to join.
```
(venv) $ python3 cnew.py -u m3x1c0 -s ws://192.168.43.194:9696/
[10:45:57] SNCTRYZERO ⮞ Starting Sanctuary ZERO v19082020 up...
[10:45:57] SNCTRYZERO ⮞ Connected to ws://192.168.43.194:9696/ successfully
[10:45:57] SNCTRYZERO ⮞ Session started at Sat Aug 22 10:45:57 2020
[10:45:57] SNCTRYZERO ⮞ A new chatroom was generated
[10:45:57] SNCTRYZERO ⮞ A new password was generated
[10:45:57] SNCTRYZERO ⮞ Chatroom identity ⮞ 37777D41
[10:45:57] SNCTRYZERO ⮞ Chatroom password ⮞ 8vEreL6GevaSm078G2rf5Mi168WX-RC_58gX_bcg6uU=
[10:45:57] SNCTRYZERO ⮞ Share the chatroom identity and password to add members!
[10:45:57] SNCTRYZERO ⮞ Your conversations are protected with end-to-end encryption
[10:45:57] USERJOINED ⮞ m3x1c0 joined - ['m3x1c0'] are connected - Indexes updated
[10:45:57] m3x1c0     ⮞
```
- To join a chatroom created by someone else, use the following.
```
(venv) $ python3 cnew.py -u m3x1c0 -p 8vEreL6GevaSm078G2rf5Mi168WX-RC_58gX_bcg6uU= -c 37777D41 -s ws://192.168.43.194:9696/
[10:51:41] SNCTRYZERO ⮞ Starting Sanctuary ZERO v19082020 up...
[10:51:41] SNCTRYZERO ⮞ Connected to ws://192.168.43.194:9696/ successfully
[10:51:41] SNCTRYZERO ⮞ Session started at Sat Aug 22 10:51:41 2020
[10:51:41] SNCTRYZERO ⮞ A valid chatroom identity was entered
[10:51:41] SNCTRYZERO ⮞ A valid chatroom password was entered
[10:51:41] SNCTRYZERO ⮞ Chatroom identity ⮞ 37777D41
[10:51:41] SNCTRYZERO ⮞ Chatroom password ⮞ 8vEreL6GevaSm078G2rf5Mi168WX-RC_58gX_bcg6uU=
[10:51:41] SNCTRYZERO ⮞ Share the chatroom identity and password to add members!
[10:51:41] SNCTRYZERO ⮞ Your conversations are protected with end-to-end encryption
[10:51:41] USERJOINED ⮞ m3x1c0 joined - ['m3x1c0'] are connected - Indexes updated
[10:51:41] m3x1c0     ⮞
```
- Use `@username` to refer to a specific username.
- Hit **`Ctrl+C`** at any point of time to exit out of the client.
```
[10:52:22] USERJOINED ⮞ m3x1c0 joined - ['m3x1c0'] are connected - Indexes updated
[10:52:22] m3x1c0     ⮞                                                                                                                                                                                                                                                         
[10:53:21] SNCTRYZERO ⮞ Leaving SNCTRYZERO...
```
- All users of a chatroom would be automatically notified about the users connecting or leaving whenever that event takes place.

## Screenshots
### Server
![](pictures/servpics.png)
### Client
![](pictures/clinpics.png)

## Vulnerabilities
<p align="justify">As most of the functions and routines have been implemented on the client-side to reduce the weight and complexity of the server-side code, the chatroom is vulnerable to monkey patching. Though the risk of information breach has been significantly minimized with the introduction of hardened protection based on Fernet symmetric-key cryptography, still it is highly recommended not to share confidential and sensitive information over the chatrooms. In such a state, it can be used for all kinds of conversation and as long as the chatroom is not opened up to the internet, you should not have to worry about any vulnerabilities.</p>

## Disclaimer
<p align="justify">When you use Sanctuary Zero - you agree to not hold its contributors responsible for any data loss or breach that may occur due to the use of this chatroom application. You agree that you are aware of the experimental condition of Sanctuary Zero and that you would want to use it at your own risk.</p>

## Contribute
<p align="justify">You may request for the addition of new features in the <a href="https://github.com/t0xic0der/sanctuary-zero/issues">issues</a> page but as the project is singlehandedly maintained - it might take time to develop on them. Please consider forking the repository and contributing to its development. :heart:</p>
