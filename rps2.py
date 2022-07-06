#!/bin/python3

import random
import operator
import re
import os

predictions = []
choices = ['r', 'p', 's']
last_five = []
machine_move = ""
move_holder = ""
uinput = ""
scores = [0,0]

#clear console
clear = lambda: os.system('clear')
clear()

print("#" * 50)
print(" " * 8 + "Simple AI Rock, Paper and Scissors")
print(" " * 15 + "By: Niko Kilponen")
print("#" * 50)
print("\n")

print("(r)ock, (p)aper, (s)cissors or (e)xit")

def user_input():	
	uinput = input("Your choice?") #get user input
	uinput = uinput.lower() #make it lower case
	
	if uinput == "r" or uinput == "p" or uinput == "s": #check if input is correct
		last_five.append(uinput) #append last player move to last_five list
		
		if len(last_five) > 5: #if last_five list contains more than 5 items
			del last_five[0] #delete first item from last_five list
			
		predict(uinput)
	
	elif uinput == "e":
		quit()
	
	else: #if user input was incorrect
		print("Please use 'r', 'p' or 's'")
		user_input()

def predict(uinput):
	last_four = ""
	machine_next = ""
	five_str = ""
	
	if len(last_five) < 5: #if there has not been 5 player moves yet
		machine_move = random.choice(choices) #use random to pick machine move
		game(uinput, machine_move)

	elif len(predictions) == 0 and len(last_five) == 5: #if there is no data in predictions
		temp = "" #temp string for containing last 5 player moves
		temp_data = [] #hold temp data to be moved to predictions
		
		for i in range(0, len(last_five)): #make string from last 5 player moves
			temp += last_five[i] #store moves in temp
		
		temp_data.append(temp) #append last 5 moves to temp_data
		temp_data.append(1) #append integer to -1 position in temp_data list
		predictions.append(temp_data[:]) #add new pattern to predictions
		machine_move = random.choice(choices) #play random move for machine
		game(uinput, machine_move)
		
	elif len(predictions) != 0 and len(last_five) == 5: #check if there is data in predictions
		match = []
		best_match = [] #best match found from predictions
		highest_match = 0
		temp_index = 0
		temp_list = []
		five_str = ""
		
		if machine_next != "":
			machine_move = machine_next #use predicted move as current move for machine
		
		for i in range(1,5): #make string of last 4 moves from last 5 player moves
			last_four += last_five[i]
			
		for i in range(0,len(predictions)): #try to find matches from predictions
			match = re.search(r'^{}.$'.format(last_four), predictions[i][0])
			
			if match and predictions[i][1] > highest_match: #find most used pattern
				highest_match = predictions[i][1]
				best_match = predictions[i] #add most used pattern to best match
				move_holder = best_match[0][-1] #add machine prediction for next round

		for i in range(0,5):
			five_str += str(last_five[i])

		#find if last 5 player moves match anything in predictions
		for i in range(0,len(predictions)):
			pattern_match = re.search(five_str, predictions[i][0])
			
			if pattern_match: #if pattern is found append it to temp list
				temp_list.append(pattern_match)
				temp_index = i #store index of found pattern for further use
	
		if len(temp_list) > 0: #if pattern has been found
			predictions[temp_index][1] += 1 #add +1 to spesific pattern
			machine_move = machine_next
			machine_next = move_holder
			game(uinput, machine_move)
			
		else: #if no pattern has been found, make new pattern to predictions
			temp = ""
			temp_data = []
			for i in range(0, len(last_five)):
				temp += last_five[i]
			
			temp_data.append(temp)
			temp_data.append(1)
			predictions.append(temp_data[:])
			
			machine_move = random.choice(choices)
			game(uinput, machine_move)
		
		

def game(uinput, machine_move):
	outcome = ""
	winrate = 0

	#counter players move with data recieved from predictions
	if machine_move == "r":
		machine_move = "p"
	
	elif machine_move == "p":
		machine_move = "s"
	
	elif machine_move == "s":
		machine_move = "r"
		
	#check for winner
	if uinput == machine_move:
		outcome = f"Both played: {uinput}, Draw!"
		
	elif uinput == "r":
		if machine_move == "s":
			outcome = "You Win!"
			scores[0] += 1 #add +1 to player score
			
		else:
			outcome = "You Lose!"
			scores[1] += 1 #add +1 to machine score
			
	elif uinput == "p":
		if machine_move == "r":
			outcome = "You Win!"
			scores[0] += 1
			
		else:
			outcome = "You Lose!"
			scores[1] += 1
			
	elif uinput == "s":
		if machine_move == "p":
			outcome = "You Win!"
			scores[0] += 1
			
		else:
			outcome = "You Lose!"
			scores[1] += 1
			
	if scores[1] != 0: #check for division by zero
		winrate = (scores[0] / (scores[0] + scores[1])) * 100 #calculate winrate	
	
	elif scores[0] > 0 & scores[1] == 0:
		winrate = 100
		 
	#clear console
	clear()
	
	print("\n")
	print("#" * 50)
	print("\n")
	print(f"Player: {uinput}" + " " * 5 + f"Machine: {machine_move}" + " " * 5 + f"{outcome}")
	print("\n")
	print(f"Player Score: {scores[0]}" + " " * 5 + f"Machine Score: {scores[1]}")
	print("\n")
	print(f"Player Win Rate: {round(winrate, 1)}%")
	print("\n")
	print("#" * 50)
	print("\n")
	
	user_input()
	
user_input()
