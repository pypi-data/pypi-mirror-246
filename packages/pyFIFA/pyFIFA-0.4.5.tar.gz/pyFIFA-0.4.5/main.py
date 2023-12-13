"""Calls main function"""
from pyfiglet import Figlet
import random
import time
from world_cup import WorldCup, Group
import trivia
from helper_functions import calculateGameCPU_group_stages


#this is for introduction. I.e. each time you run game it will say you had an illustrious carrier at one of these 3
random_soccer_teams = [
    "AC Milan",
    "Juventus FC",
    "Internazionale",
    
    "FC Barcelona",
    "Real Madrid",
    "Atletico de Madrid",

    "Manchester United",
    "Manchester City",
    "Liverpool",
    
    "Bayern Munich",
    "Borussia Dortmund",
]


def isNum(inp):
    for i in inp:
        if not i.isdigit():
            return False
    return True


def checkValidInputInt(upperLim,lowerLim,inputQuestion):
    #upper lim and lower lim are INCLUSIVE
    loop=True
    while(loop):
        out=input(inputQuestion)
        if len(out)>0 and isNum(out) and int(out)<=upperLim and int(out)>=lowerLim:
            loop=False
            return out
        else:
            print("Invalid Input, try again")


def main():
    f = Figlet(font='slant')
    print(f.renderText('Welcome to PyFIFA!'))

    print('''
\033[1mGithub\033[0m:
https://github.com/Rafinator123/OOP-Fifa-In-Terminal\033[0m

\033[1mPyFIFA\033[0m is an interactive text-based soccer game inspired by the 2023 FIFA World 
Cup in Qatar. 
          
Team are ranked by historical preformance and are divided into 4 pots. 
Teams with higher \033[1mOFFENSE\033[0m and \033[1mDEFENSE\033[0m are likely to be more successful in the \033[1mPyFIFA\033[0m.
          
However, teams with lower \033[1mOFFENSE\033[0m and \033[1mDEFENSE\033[0m provide the player more challenging gameplay.
Winning games involves a blend of luck and trivia knowledge.
Players must correctly answer world cup trivia questions

\033[1mHow to play\033[0m:
1. Enter your name and choose your team
2. Answer trivia questions to win games
3. Hope the odds are in your favor 
4. Win the \033[1mPyFIFA\033[0m World Cup!
            ''')


    f_name = input("\033[1mWhat is your first name?\033[0m\n")
    print()
    l_name = input("\033[1mWhat is your last name?\033[0m\n")
    print()
    print('''Coach\033[1m:''',f_name,l_name,"\033[0m")

    print(f'''\nAfter an ilustrious career working at \033[1m{random_soccer_teams[random.randint(0,len(random_soccer_teams)-1)]}\033[0m, you've been approached 
from the following clubs to manage them at the world cup.\n''')
       
    # time.sleep(3)

    ratings=["Easy","Medium","Hard","Very Hard"]
    # Print four teams here going from easy difficulty to hard:
    wc = WorldCup()
    randomized_team_selection =[]
    randomized_team_selection.append(wc.pot1[random.randint(0, len(wc.pot1)-1)])
    randomized_team_selection.append(wc.pot2[random.randint(0, len(wc.pot2)-1)])
    randomized_team_selection.append(wc.pot3[random.randint(0, len(wc.pot3)-1)])
    randomized_team_selection.append(wc.pot4[random.randint(0, len(wc.pot4)-1)])
    
    #todo: print out the stars
    for i in range(0,4):
        off_stars = randomized_team_selection[i].defense * "*"
        deff_stars = randomized_team_selection[i].offense * "*"
        print(f"({i + 1}) \033[1m{randomized_team_selection[i].nation:<20}\033[0m Difficulty: {ratings[i]:<10} OFFENSE: {off_stars:<10} DEFENSE: {deff_stars}")     
        
    #validate input 
    player_nation = randomized_team_selection[ int(checkValidInputInt(5,1,"\n\033[1mEnter your choice:\033[0m "))-1]

    # time.sleep(2)
    #todo:  Print out your team stats
    wc.currUser = player_nation
    print()
    print(f"You have chosen \033[1m{player_nation.nation}\033[0m as your team! Good luck!")
    print()
    choice = checkValidInputInt(2,1,"\033[1mView current standings?\033[0m\n(1) Yes\n(2) No\n\033[1mEnter your choice: \033[0m")
    verbose = False
    if(int(choice)==1):
        verbose = True
    wc.simulate(verbose)
    
main()
