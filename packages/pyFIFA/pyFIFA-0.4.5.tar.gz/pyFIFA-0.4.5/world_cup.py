"""App file containing class definitions"""
from helper_functions import calculateGameCPU_group_stages, calculateGameCPU_knockouts, calculateGameUser_groupStage, calculateGameUser_knockout, checkValidInputInt, printTeam
import time

class Nation:
    def __init__(self, c: str, n: str, o: str, mid : str, d: str, off, deff: str) -> None:
        self.coach = c
        self.nation = n
        self.key_outfielder = o
        self.key_defender = d
        self.offense = off
        self.midfielder = mid
        self.defense = deff
        pass
        
class Group:
    """Class containing each group where group has 4 nations that will play against each other"""
    def __init__(self, l, n1,n2,n3,n4) -> None:
        self.letter = l
        self.group = {}
        self.group["a"] = [n1,0]
        self.group["b"] = [n2,0]
        self.group["c"] = [n3,0]
        self.group["d"] = [n4,0]
        return
    def simulateGroupStagePlayer(self, currUser):
        def getPoints(t1, t2):
            if (self.group[t1][0].nation == currUser.nation):
                winner = calculateGameUser_groupStage(self.group[t1][0], self.group[t2][0])
                if len(winner) > 1:
                    self.group[t1][1] += 1
                    self.group[t2][1] += 1
                else:
                    if winner[0] == self.group[t1][0]:
                        self.group[t1][1] += 3
                    else:
                        self.group[t2][1] += 3
            elif (self.group[t2][0].nation == currUser.nation):
                winner = calculateGameUser_groupStage(self.group[t2][0], self.group[t1][0])
                if len(winner) > 1:
                    self.group[t1][1] += 1
                    self.group[t2][1] += 1
                else:
                    if winner[0] == self.group[t1][0]:
                        self.group[t1][1] += 3
                    else:
                        self.group[t2][1] += 3
            else:    
                winner = calculateGameCPU_group_stages(self.group[t1][0], self.group[t2][0])
                if len(winner) > 1:
                    self.group[t1][1] += 1
                    self.group[t2][1] += 1
                else:
                    if winner == self.group[t1][0]:
                        self.group[t1][1] += 3
                    else:
                        self.group[t2][1] += 3
        """Simulaes games for the whole group."""
        #First round
        time.sleep(1.5)
        print("--------------------")
        print("Match Day: 1/3")
        print("--------------------")
        time.sleep(1.5)
        getPoints("a","b")
        getPoints("c","d")
        #Second round
        time.sleep(1.5)
        print("--------------------")
        print("Match Day: 2/3")
        print("--------------------")
        time.sleep(1.5)
        getPoints("a","d")
        getPoints("b","c")
        #third round
        time.sleep(1.5)
        print("--------------------")
        print("Final Match Day")
        print("--------------------")
        time.sleep(1.5)
        getPoints("a","c")
        getPoints("b", "d")
        self.printOutTable()
        # getPoints(self.group["a"],self.group["b"])
        # getPoints(self.group["c"],self.group["d"])
        # self.printOutTable()
        # #Second round
        # getPoints(self.group["a"],self.group["d"])
        # getPoints(self.group["b"],self.group["c"])
        # self.printOutTable()
        # #third round
        # getPoints(self.group["a"],self.group["c"])
        # getPoints(self.group["b"],self.group["d"])
        # self.printOutTable()
        #Exit prematurely if you fail to go through
        
    def simulateGroupStageCPU(self):
        def getPoints(t1, t2):
            winner = calculateGameCPU_group_stages(self.group[t1][0], self.group[t2][0])
            if len(winner) > 1:
                self.group[t1][1] += 1
                self.group[t2][1] += 1
            else:
                if winner == t1:
                    self.group[t1][1] += 3
                else:
                    self.group[t2][1] += 3
        """Simulaes games for the whole group."""
        # First round
        getPoints("a","b")
        getPoints("c","d")
        #Second round
        getPoints("a","d")
        getPoints("b","c")
        #third round
        getPoints("a","c")
        getPoints("b", "d")
    
    # Need to fix this 
    def printOutTable(self):
        print(f"\033[5mGroup {self.letter}\033[0m")
        sorted_nations = sorted(self.group.values(), key=lambda x: x[1], reverse=True)
        for i, (nation, points) in enumerate(sorted_nations, start=1):
            print(f"{i}. \033[1m{nation.nation}\033[0m - Points: {points}")
        print("\n")
        
class WorldCup:
    def __init__(self):
        self.currUser = ""
        self.groups = []
        self.pot1 =[]
        self.pot2 =[]
        self.pot3 =[]
        self.pot4 = []
        # Group A
        qatar = Nation("Félix Sánchez Bas", "Qatar", "Akram Afif", "Boualem Khoukhi", "Bassam Al-Rawi", 1, 1)
        ecuador = Nation("Gustavo Alfaro", "Ecuador", "Enner Valencia", "Carlos Gruezo", "Piero Hincapié", 3, 3)
        senegal = Nation("Aliou Cissé", "Senegal", "Sadio Mané", "Idrissa Gueye", "Kalidou Koulibaly", 4, 3)
        netherlands = Nation("Louis van Gaal", "Netherlands", "Memphis Depay", "Frenkie de Jong", "Virgil van Dijk", 5, 5)
        groupA = Group("A",qatar, ecuador, senegal, netherlands)
        self.pot1.append(netherlands)
        self.pot2.append(senegal)
        self.pot3.append(ecuador)
        self.pot4.append(qatar)
        self.groups.append(groupA)
        # Group B
        england = Nation("Gareth Southgate", "England", "Harry Kane", "Jude Bellingham", "Harry Maguire", 5, 5)
        iran = Nation("Dragan Skočić", "Iran", "Sardar Azmoun", "Alireza Jahanbakhsh", "Milad Mohammadi", 3, 2)
        usa = Nation("Gregg Berhalter", "USA", "Christian Pulisic", "Weston McKennie", "John Brooks", 3, 3)
        wales = Nation("Rob Page", "Wales", "Gareth Bale", "Aaron Ramsey", "Joe Rodon", 3, 2)
        groupB = Group("B",england, iran, usa, wales)
        self.pot1.append(england)
        self.pot2.append(usa)
        self.pot3.append(wales)
        self.pot4.append(iran)
        self.groups.append(groupB)
        
        # Group C
        argentina = Nation("Lionel Scaloni", "Argentina", "Lionel Messi", "Alexis MacAllister", "Emiliano Martínez", 5, 5)
        saudi_arabia = Nation("Hervé Renard", "Saudi Arabia", "Salem Al-Dawsari", "Abdullah Otayf", "Yasser Al-Shahrani", 2, 2)
        mexico = Nation("Gerardo Martino", "Mexico", "Raúl Jiménez", "Héctor Herrera", "Guillermo Ochoa", 4, 4)
        poland = Nation("Paulo Sousa", "Poland", "Robert Lewandowski", "Grzegorz Krychowiak", "Kamil Glik", 4, 3)
        groupC = Group("C",argentina, saudi_arabia, mexico, poland)
        self.pot1.append(argentina)
        self.pot2.append(mexico)
        self.pot3.append(poland)
        self.pot4.append(saudi_arabia)
        self.groups.append(groupC)
        
        # Group D
        france = Nation("Didier Deschamps", "France", "Kylian Mbappé", "Antoine Griezmann", "Raphael Varane", 5, 5)
        australia = Nation("Graham Arnold", "Australia", "Mat Ryan", "Aaron Mooy", "Mathew Leckie", 3, 3)
        denmark = Nation("Kasper Hjulmand", "Denmark", "Christian Eriksen", "Pierre-Emile Højbjerg", "Simon Kjaer", 4, 4)
        tunisia = Nation("Mondher Kebaier", "Tunisia", "Youssef Msakni", "Wahbi Khazri", "Dylan Bronn", 2, 1)
        groupD = Group("D",france, australia, denmark, tunisia)
        self.pot1.append(france)
        self.pot2.append(denmark)
        self.pot3.append(australia)
        self.pot4.append(tunisia)
        self.groups.append(groupD)
        
        # Group E
        spain = Nation("Luis Enrique", "Spain", "Álvaro Morata", "Sergio Busquets", "Pau Torres", 5, 5)
        costa_rica = Nation("Luis Fernando Suárez", "Costa Rica", "Joel Campbell", "Bryan Ruiz", "Keylor Navas", 3, 3)
        germany = Nation("Hansi Flick", "Germany", "Thomas Müller", "Leon Goretzka", "Mauel Neuer", 4, 4)
        japan = Nation("Hajime Moriyasu", "Japan", "Takefusa Kubo", "Gaku Shibasaki", "Maya Yoshida", 4, 3)
        groupE = Group("E",spain, costa_rica, germany, japan)
        self.pot1.append(spain)
        self.pot2.append(germany)
        self.pot3.append(japan)
        self.pot4.append(costa_rica)
        self.groups.append(groupE)
        
        # Group F
        belgium = Nation("Roberto Martínez", "Belgium", "Romelu Lukaku", "Kevin De Bruyne", "Thibaut Courtois", 5, 5)
        canada = Nation("John Herdman", "Canada", "Jonathan David", "Scott Arfield", "Alphonso Davies", 2, 3)
        morocco = Nation("Vahid Halilhodžić", "Morocco", "Achraf Hakimi", "Hakim Ziyech", "Romain Saïss", 3, 4)
        croatia = Nation("Zlatko Dalić", "Croatia", "Ivan Perišić", "Luka Modrić", "Domagoj Vida", 4, 4)
        groupF = Group("F",belgium, canada, morocco, croatia)
        self.pot1.append(belgium)
        self.pot2.append(croatia)
        self.pot3.append(morocco)
        self.pot4.append(canada)
        self.groups.append(groupF)
        
        # Group G
        brazil = Nation("Tite (Adenor Leonardo Bacchi)", "Brazil", "Neymar Jr.", "Casemiro", "Marquinhos", 5, 5)
        serbia = Nation("Dragan Stojković", "Serbia", "Dušan Tadić", "Sergej Milinković-Savić", "Aleksandar Kolarov", 3, 4)
        switzerland = Nation("Murat Yakin", "Switzerland",  "Xherdan Shaqiri", "Granit Xhaka","Manuel Akanji", 3, 3)
        cameroon = Nation("Toni Conceição", "Cameroon", "Eric Maxim Choupo-Moting", "André-Frank Zambo Anguissa", "Joël Matip", 4, 2)
        groupG = Group("G",brazil, serbia, switzerland, cameroon)
        self.pot1.append(brazil)
        self.pot2.append(serbia)
        self.pot3.append(switzerland)
        self.pot4.append(cameroon)
        self.groups.append(groupG)
        
        # Group H
        portugal = Nation("Fernando Santos", "Portugal", "Cristiano Ronaldo", "Bruno Fernandes", "Ruben Dias", 5, 5)
        ghana = Nation("Otto Addo", "Ghana", "Andre Ayew", "Thomas Partey", "Daniel Amartey", 3, 3)
        uruguay = Nation("Óscar Tabárez", "Uruguay", "Luis Suárez", "Federico Valverde", "José María Giménez", 4, 4)
        korea_republic = Nation("Paulo Bento", "Korea Republic", "Son Heung-min", "Hwang Hee-chan", "Kim Min-jae", 2, 2)
        groupH = Group("H",portugal, ghana, uruguay, korea_republic)
        self.pot1.append(portugal)
        self.pot2.append(uruguay)
        self.pot3.append(ghana)
        self.pot4.append(korea_republic)
        self.groups.append(groupH)
        
    def groupStages(self):
        winners = {}
        for i in range(len(self.groups)):
            #winner needs to be collected and we need to check this.
            check = False
            for key in self.groups[i].group:
                if self.groups[i].group[key][0].nation == self.currUser.nation:
                    check = True
            if check:
                self.groups[i].simulateGroupStagePlayer(self.currUser)
            else:
                self.groups[i].simulateGroupStageCPU()
            #collect the top winners
            #count sort
            count_sort = []
            for key in self.groups[i].group:
                currNation = self.groups[i].group[key]
            sorted_nations = sorted(self.groups[i].group.values(), key=lambda x: x[1], reverse=True)
            for j in range(1,3):
                code = self.groups[i].letter + str(j)
                winners[code] = sorted_nations[j-1][0]
        #input("Press enter to continue:")
        return winners
    def round16(self, group_stage_winners):
        r16_winners = {}
        def knockout(t1, t2):
            if t1.nation == self.currUser.nation:
                winner = calculateGameUser_knockout(t1,t2)
            if t2.nation == self.currUser.nation:
                winner = calculateGameUser_knockout(t2,t1)
            else:
                winner = calculateGameCPU_knockouts(t1,t2)
            return winner
        # Group A  vs Group B
        A1B2 = knockout(group_stage_winners["A1"],group_stage_winners["B2"])
        A2B1 = knockout(group_stage_winners["A2"],group_stage_winners["B1"])
        r16_winners["A1B2"] = A1B2
        r16_winners["A2B1"] = A2B1
        # Group C vs Group D
        C1D2 = knockout(group_stage_winners["C1"],group_stage_winners["D2"])
        C2D1 = knockout(group_stage_winners["C2"],group_stage_winners["D1"])
        r16_winners["C1D2"] = C1D2
        r16_winners["C2D1"] = C2D1
        # Group E vs Group F 
        E1F2 = knockout(group_stage_winners["E1"],group_stage_winners["F2"])
        E2F1 = knockout(group_stage_winners["E2"],group_stage_winners["F1"])
        r16_winners["E1F2"] = E1F2
        r16_winners["E2F1"] = E2F1
        # Group G vs Group H
        G1H2 = knockout(group_stage_winners["G1"],group_stage_winners["H2"])
        G2H1 = knockout(group_stage_winners["G2"],group_stage_winners["H1"])
        r16_winners["G1H2"] = G1H2
        r16_winners["G2H1"] = G2H1
        return r16_winners
    def quarterFinals(self, r16_winners):
        def knockout(t1, t2):
            if t1.nation == self.currUser:
                winner = calculateGameUser_knockout(t1,t2)
            if t2.nation == self.currUser:
                winner = calculateGameUser_knockout(t2,t1)
            else:
                winner = calculateGameCPU_knockouts(t1,t2)
            return winner
        quarter_finals_winners = {}
        #first match
        left_bracket_1 = knockout(r16_winners["A1B2"], r16_winners["C1D2"])
        quarter_finals_winners["l1"] = left_bracket_1
        left_bracket_2 = knockout(r16_winners["E1F2"], r16_winners["G1H2"])
        quarter_finals_winners["l2"] = left_bracket_2
        right_bracket_1 = knockout(r16_winners["A2B1"],r16_winners["C2D1"])
        quarter_finals_winners["r1"] = right_bracket_1
        right_bracket_2 = knockout(r16_winners["G2H1"],r16_winners["E2F1"])
        quarter_finals_winners["r2"] = right_bracket_2
        return quarter_finals_winners
    def semiFinals(self, quarter_finals_winners):
        def knockout(t1, t2):
            if t1.nation == self.currUser.nation:
                winner = calculateGameUser_knockout(t1,t2)
            if t2.nation == self.currUser.nation:
                winner = calculateGameUser_knockout(t2,t1)
            else:
                winner = calculateGameCPU_knockouts(t1,t2)
            return winner
        finals = {}
        #first match
        final_left = knockout(quarter_finals_winners["l1"], quarter_finals_winners["l2"])
        final_right = knockout(quarter_finals_winners["r1"], quarter_finals_winners["r2"])
        finals["l"] = final_left
        finals["r"] = final_right
        return finals
    def finals(self, finals):
        def knockout(t1, t2):
            if t1.nation == self.currUser.nation:
                winner = calculateGameUser_knockout(t1,t2)
            if t2.nation == self.currUser.nation:
                winner = calculateGameUser_knockout(t2,t1)
            else:
                winner = calculateGameCPU_knockouts(t1,t2)
            return winner
        #first match
        world_cup_champion  = knockout(finals["l"], finals["r"])
        return world_cup_champion
    
    def simulate(self, verbose:bool):
        winners = {}
        winners = self.groupStages()
        #Print it out depending on whether roundof16 is 
        if self.currUser in winners.values():
            print("Congratulations!\nYou've made it to the round of 16...\n")
            input("\033[7m\033[1mPress enter to continue\033[0m")
        else:
            choice = checkValidInputInt(2,1,"You've been knocked out...\n Do you want to see the results regardless?\n 1) Yes show me! \n 2) No I'm done...")
            exit if choice == 2 else None
        winners = self.round16(winners)
        if self.currUser in winners.values():
            print("Congratulations! You've made it to the the quarter finals...\n")
            input("\033[7m\033[1mPress enter to continue\033[0m")
        else:
            choice = checkValidInputInt(2,1,"You've been knocked out...\n Do you want to see the results regardless?\n 1) Yes show me! \n 2) No I'm done...")
            exit if choice == 2 else None
        winners = self.quarterFinals(winners)
        if self.currUser in winners.values():
            print("Congratulations! You've made it to the semi-finals...\n")
            input("\033[7m\033[1mPress enter to continue\033[0m")
        else:
            choice = checkValidInputInt(2,1,"You've been knocked out...\n Do you want to see the results regardless?\n 1) Yes show me! \n 2) No I'm done...")
            exit if choice == 2 else None
        winners = self.semiFinals(winners)
        if self.currUser in winners.values():
            print("Congratulations! You've made it to the world cup finals...\n")
            input("\033[7m\033[1mPress enter to continue\033[0m")
        else:
            choice = checkValidInputInt(2,1,"You've been knocked out...\n Do you want to see the results regardless?\n 1) Yes show me! \n 2) No I'm done...")
            exit if choice == 2 else None
        winner = self.finals(winners)
        if self.currUser == winner:
            print("\nYou are the world cup champions!")
        else:
            choice = checkValidInputInt(2,1,"You've been knocked out...\n Do you want to see the results regardless?\n 1) Yes show me! \n 2) No I'm done...")
            exit if choice == 2 else None
        print(f"{winner.nation} has won the world cup!!")
        return
        