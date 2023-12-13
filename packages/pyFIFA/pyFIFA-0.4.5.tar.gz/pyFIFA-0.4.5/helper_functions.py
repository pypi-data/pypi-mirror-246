"""Includes helper functions"""
import random
from pyfiglet import Figlet
from trivia import ask_trivia_question
from time import sleep
from pyfiglet import Figlet

used_colors = list()
def userGameSimulation(t1, t2, t1_score, t2_score):
    printTeam(t1, t2)
    t1_actual_score = 0
    t2_actual_score = 0
    t1_count = 0
    t2_count = 0
    print("\033[1mFabrizio Romano\033[0m's match prediction:")
    sleep(1)
    if t1_score == t2_score:
        print("Tie")
    elif t1_score > t2_score:
        print("Prediction: " + "\033[32m\033[1m" + t1.nation + "\033[0m" + " wins")
    else:
        print("Prediction: " + "\033[32m\033[1m" + t2.nation + "\033[0m wins\n")
    sleep(1)
    print("\033[1m"+t1.nation +"\033[0m " + str(t1_score) + " - " + str(t2_score) + " " + "\033[1m"+t2.nation +"\033[0m")
    sleep(1)
    print("\n\033[3mChange the outcome of the match by correctly answering trivia questions!\033[0m")
    print("\nYou will receive questions\n")
    input("\033[1m\033[7mPress enter to start the match\n\033[0m")

    # Adjust the number of iterations to be the sum of t1_score and t2_score
    total_attacks = t1_score + t2_score
    for _ in range(total_attacks):
        if t1_count < t1_score:
            t1_count += 1
            print(f"\033[1m{t1.midfielder}\033[0m finds \033[1m{t1.key_outfielder}\033[0m on the attack!\nHe's through on goal!")
            correct = ask_trivia_question()
            if correct:
                printGoal()
                t1_actual_score += 1
                print(f"\033[1m{t1.nation}\033[0m Scores! Goal by \033[1m{t1.key_outfielder}\033[0m!")
            else:
                print(f"What a defensive play by \033[1m{t2.key_defender} \033[0m...")
            print(f"\n\033[3mScore remains...\033[0m\n\033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[1m{t2.nation}")
            print()
        if t2_count < t2_score:
            t2_count += 1
            print(f"\033[1m{t2.midfielder}\033[0m finds \033[1m{t2.key_outfielder}\033[0m on the attack! It's all up to \033[1m{t1.key_defender}\033[0m to stop it!")
            correct = ask_trivia_question()
            if correct:
                print(f"What a defensive play by \033[1m{t1.key_defender}\033[0m...\n")
            else:
                t2_actual_score += 1
                print(f"Scored by \033[1m{t2.key_outfielder}\033[0m")
            print(f"It's \033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[1m{t2.nation}\033[0m")
        
    #if attacks are 0 then simulate once
    if total_attacks == 0:
        print(f"\033[1m{t1.midfielder}\033[0m finds \033[1m{t1.key_outfielder}\033[0m on the attack! He's through on goal!")
        correct = ask_trivia_question()
        if correct:
            printGoal()
            t1_actual_score += 1
            print(f"\n\033[3mScore remains...\033[0m\n\033[1m{t1.nation}\033[0m's \033[1m{t1.key_outfielder}\033[0m!")
            print()
        else:
            print(f"What a defensive play by {t2.key_defender}...")
        print(f"\n\033[3mScore remains...\033[0m\n\033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[1m{t2.nation}\033[0m")
        print()
        print(f"\033[1m{t2.midfielder}\033[0m finds \033[1m{t2.key_outfielder}\033[0m on the attack! It's all up to \033[1m{t1.key_defender}\033[0m to stop it!")
        correct = ask_trivia_question()
        if correct:
            print(f"What a defensive play by \033[1m{t1.key_defender}\033[0m from \033[1m{t1.nation}\033[0m...")
            input("\033[1m\033[7mPress enter to continue\n\033[0m")
        else:
            t2_actual_score += 1
            print(f"Scored by \033[1m{t2.key_outfielder}\033[0m")
        print(f"It's \033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[1m{t2.nation}\033[0m")
    return t1_actual_score, t2_actual_score


def scoreCalc(offense, defense):
    return max(0, offense - defense)

def calculateGameCPU_group_stages(t1, t2):
    """"""
    t1_score = scoreCalc(random.randint(t1.offense-2,t1.offense+2), random.randint(t2.defense-2, t2.offense+2))
    t2_score = scoreCalc(random.randint(t2.offense-2,t2.offense+2), random.randint(t1.defense-2, t1.offense+2))
    if t1_score == t2_score:
        return [t1,t2]
    elif t1_score > t2_score:
        return [t1]
    else:
        return [t2]
def calculateGameCPU_knockouts(t1, t2):
    """Calculates games between teams"""
    
    t1_score = scoreCalc(random.randint(t1.offense-2,t1.offense+2), random.randint(t2.defense-2, t2.offense+2))
    t2_score = scoreCalc(random.randint(t2.offense-2,t2.offense+2), random.randint(t1.defense-2, t1.offense+2))
    
    #Extra time
    if t1_score == t2_score:
        print("")
        t1_score = scoreCalc(random.randint(t1.offense-2,t1.offense), random.randint(t2.defense-2, t2.offense))
        t2_score = scoreCalc(random.randint(t2.offense-2,t2.offense), random.randint(t1.defense-2, t1.offense))
        if t1_score > t2_score:
            return t1
        elif t1_score < t2_score:
            return t2
    else:
        if t1_score > t2_score:
            return t1
        else:
            return t2
    # Penalties
    t1_penalties = 0
    t2_penalties = 0

    while t1_penalties < 5 and t2_penalties < 5:
        t1_penalty_score = random.randint(0, 1)
        t2_penalty_score = random.randint(0, 1)

        if t1_penalty_score > t2_penalty_score:
            t1_penalties += 1
        else:
            t2_penalties += 1

    if t1_penalties > t2_penalties:
        return t1
    else:
        return t2

def calculateGameUser_groupStage(t1, t2): 
    t1_score = scoreCalc(random.randint(t1.offense - 2, t1.offense + 2), random.randint(t2.defense - 2, t2.defense + 2))
    t2_score = scoreCalc(random.randint(t2.offense - 2, t2.offense + 2), random.randint(t1.defense - 2 , t1.defense + 2))
    #Go through rounds
    t1_actual_score, t2_actual_score = userGameSimulation(t1, t2, t1_score, t2_score)
    print("\033[2mThe referee has blown the wistle...\033[0m")
    sleep(1)
    if t1_actual_score < t2_actual_score:
        print(f"Final score: \033[31m\033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[32m\033[1m{t2.nation}\033[0m")
        input("\033[1m\033[7mPress enter to continue\n\033[0m")
        return [t2]
    elif t1_actual_score > t2_actual_score:
        print(f"Final score: \033[32m\033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[31m\033[1m{t2.nation}\033[0m")
        input("\033[1m\033[7mPress enter to continue\n\033[0m")
        return [t1]
    else:
        print(f"Final score: \033[1m{t1.nation}\033[0m {t1_actual_score} - {t2_actual_score} \033[1m{t2.nation}\033[0m")
        input("\033[1m\033[7mPress enter to continue\n\033[0m")
        return [t1, t2]
def calculateGameUser_knockout(t1, t2): 
    print(f"\033[1m{t1.nation}\033[0m vs \033[1m{t2.nation}\033[0m")
    # Initial match simulation
    t1_score = scoreCalc(random.randint(t1.offense - 2, t1.offense + 2), random.randint(t2.defense - 2, t2.defense + 2))
    t2_score = scoreCalc(random.randint(t2.offense - 2, t2.offense + 2), random.randint(t1.defense - 2, t1.defense + 2))
    t1_actual_score, t2_actual_score = userGameSimulation(t1, t2, t1_score, t2_score)

    # Extra time if scores are tied
    if t1_actual_score == t2_actual_score:
        print("The score is tied...\nMatch is going to extra time!")
        t1_score = scoreCalc(random.randint(t1.offense - 2, t1.offense), random.randint(t2.defense - 2, t2.defense))
        t2_score = scoreCalc(random.randint(t2.offense - 2, t2.offense), random.randint(t1.defense - 2, t1.defense))
        extra_time_t1_actual_score, extra_time_t2_actual_score = userGameSimulation(t1, t2, t1_score, t2_score)

        if extra_time_t1_actual_score != extra_time_t2_actual_score:
            if extra_time_t1_actual_score > extra_time_t2_actual_score:
                return t1
            else:
                return t2

    # Penalties if still tied after extra time
    if t1_actual_score == t2_actual_score:
        t1_penalties, t2_penalties = 0, 0
        rounds = 0
        while rounds < 5 or t1_penalties == t2_penalties:
            t1_penalty_score = random.randint(0, 1)
            t2_penalty_score = random.randint(0, 1)
            t1_penalties += t1_penalty_score
            t2_penalties += t2_penalty_score
            printGoal() if t1_penalty_score > 0 else None
            print(f"\033[1m{t1.nation}\033[0m has scored!") if t1_penalty_score > 0 else None
            printGoal() if t2_penalty_score > 0 else None
            print(f"\033[1m{t2.nation}\033[0m has scored!") if t2_penalty_score > 0 else None
            print(f"\033[1m{t1.nation}\033[0m {t1_penalties} - {t2_penalties} \033[1m{t2.nation}\033[0m")
            rounds += 1

        return t1 if t1_penalties > t2_penalties else t2
    else:
        return t1 if t1_actual_score > t2_actual_score else t2

def stars(num_starz):
    return '* '*num_starz

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

def printGoal():
    f = Figlet(font='slant')
    print("\033[92m" + f.renderText('GOAL!') + "\033[0m")

def printTeam(team1,team2):
    f = Figlet(font='slant')
    print(f.renderText(team1.nation))
    sleep(.8)
    print(f.renderText("vs"))
    sleep(.8)
    print(f.renderText(team2.nation))
    sleep(.8)
    input("\033[1m\033[7mPress enter to continue\n\033[0m")
