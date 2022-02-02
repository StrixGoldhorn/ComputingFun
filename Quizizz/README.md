# Intro
This folder contains a short analysis on Quizizz.com and a python CLI tool with trivial functions.

<br/>

## Table of Contents
- [Intro](#intro)
	- [Table of Contents](#table-of-contents)
	- [Analysis](#analysis)
	- [Python CLI Tool](#python-cli-tool)
		- [How to use](#how-to-use)
		- [Functions](#functions)
			- [Quick Overview](#quick-overview)
			- [View Players](#view-players)
			- [Questions and Answers](#questions-and-answers)

<br/>

## Analysis
The brief analysis skims through a few API endpoints on game.quizizz.com

It also includes a short description on how to earn more points than intended.

[It can be accessed here.](analysis.md)

<br/>

## Python CLI Tool

### How to use

Download [main.py](main.py) and [recon.py](recon.py) into the same folder

Open Powershell/Cmd in the folder

Type `python main.py` followed by respective args. `-h` for help.

*Note: On Unix, you have to `chmod +x main.py` to give it execute permissions*

For most functions, you **NEED TO JOIN** the game room for it to work. The game room also **NEEDS TO BE PUBLIC**, ie does not require login.



### Functions

Defaults to only printing the room hash unless args are supplied.

#### Quick Overview

`-o` or `--overview`

This prints a quick overview of the game, with details such as the name, amount of attempts available, total score of players, total players, and game settings

#### View Players

`-p` or `--players`

This prints the list of players in the game, with their respective name, platform, user agent, OS, and score.

*Note: The game room **NEEDS TO BE PUBLIC**, ie does not require login.*

#### Questions and Answers

`-a` or `--answers`

This prints the list of questions and answers.

*Note: The game room **NEEDS TO BE PUBLIC**, ie does not require login.*