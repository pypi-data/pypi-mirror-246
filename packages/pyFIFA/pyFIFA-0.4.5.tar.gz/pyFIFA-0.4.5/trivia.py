import random
import helper_functions
#todo: Add more questions
#todo: Randomize
trivia = [
    ("Which country won the first FIFA World Cup in 1930?", ["Brazil", "Uruguay", "Italy", "Germany"], 1),
    ("Who holds the record for the most goals in World Cup history?", ["Ronaldo", "Pele", "Miroslav Klose", "Gerd Müller"], 2),
    ("Which country has won the most FIFA World Cup titles?", ["Argentina", "Germany", "Italy", "Brazil"], 3),
    ("In what year was the World Cup first broadcast in color?", ["1966", "1970", "1974", "1978"], 1),
    ("Who is the only player to win three World Cups?", ["Pelé", "Maradona", "Zidane", "Beckenbauer"], 0),
    ("Which country hosted the first World Cup held in Africa?", ["Egypt", "Nigeria", "South Africa", "Morocco"], 2),
    ("What is the highest number of goals scored by a team in a single World Cup match?", ["10", "12", "15", "9"], 2),
    ("Who scored the 'Hand of God' goal in the 1986 World Cup?", ["Diego Maradona", "Pelé", "Lionel Messi", "Ronaldo"], 0),
    ("Which nation first introduced the World Cup trophy known as the Jules Rimet Trophy?", ["France", "Brazil", "Italy", "Uruguay"], 0),
    ("Which country won the first ever Women's World Cup in 1991?", ["China", "Germany", "Norway", "United States"], 3),
    ("Who was the youngest player to play in a World Cup?", ["Pelé", "Norman Whiteside", "Lionel Messi", "Michael Owen"], 1),
    ("Which team won the 2014 FIFA World Cup held in Brazil?", ["Spain", "Argentina", "Brazil", "Germany"], 3),
    ("What was unique about the 1950 World Cup final?", ["No final match was played", "It was played indoors", "It was won on penalties", "It featured co-winners"], 0),
    ("Which country has hosted the World Cup the most times?", ["Brazil", "France", "Italy", "Mexico"], 3),
    ("What is the maximum number of substitutions allowed in a World Cup match?", ["2", "3", "4", "5"], 1),
    ("Which country won the 2006 FIFA World Cup?", ["Italy", "France", "Brazil", "Germany"], 0),
    ("Who was the captain of the England team that won the World Cup in 1966?", ["Bobby Moore", "Geoff Hurst", "Gordon Banks", "Bobby Charlton"], 0),
    ("Which player scored the fastest goal in World Cup history?", ["Hakan Şükür", "Pele", "Miroslav Klose", "Cristiano Ronaldo"], 0),
    ("Which country has appeared in three World Cup finals but never won?", ["Netherlands", "Portugal", "Czech Republic", "Hungary"], 0),
    ("What was the official mascot for the 2014 FIFA World Cup in Brazil?", ["Zakumi", "Fuleco", "Goleo", "Pique"], 1),
    ("Which player has the most World Cup red cards?", ["Zinedine Zidane", "Cafu", "Rigobert Song", "Diego Maradona"], 2),
    ("What year was the first World Cup held?", ["1930", "1934", "1928", "1942"], 0),
    ("Who scored the winning goal in the 2010 World Cup final?", ["Andres Iniesta", "David Villa", "Wesley Sneijder", "Arjen Robben"], 0),
    ("What is the record number of World Cup goals scored by a single player in a tournament?", ["11", "13", "9", "10"], 1),
    ("Which country hosted the 2010 FIFA World Cup?", ["South Africa", "Germany", "Brazil", "Spain"], 0),
    ("How many times has Brazil won the FIFA World Cup?", ["4", "5", "6", "3"], 1),
    ("Who won the Golden Boot in the 1998 World Cup?", ["Ronaldo", "Davor Šuker", "David Beckham", "Zinedine Zidane"], 1),
    ("In which World Cup did Diego Maradona score his famous 'Hand of God' goal?", ["1982", "1986", "1990", "1994"], 1),
    ("Which country was the first to win the World Cup twice?", ["Brazil", "Italy", "Uruguay", "Argentina"], 2),
    ("Who was the top scorer in the 2018 FIFA World Cup?", ["Harry Kane", "Romelu Lukaku", "Kylian Mbappé", "Cristiano Ronaldo"], 0),
    ("Which country won its first World Cup in 2018?", ["France", "Croatia", "Belgium", "Russia"], 0),
    ("What color card signifies a temporary suspension in a World Cup match?", ["Red", "Yellow", "Green", "Blue"], 1),
    ("Which player scored a hat-trick in the 2018 World Cup final?", ["Kylian Mbappé", "Mario Mandžukić", "Antoine Griezmann", "Paul Pogba"], 0),
    ("Which country has the most World Cup final appearances?", ["Brazil", "Germany", "Italy", "Argentina"], 1),
    ("What year did FIFA introduce the World Cup tournament for women?", ["1991", "1985", "1995", "2000"], 0),
    ("Which country won its first World Cup title in 1958?", ["Sweden", "Brazil", "Germany", "Argentina"], 1),
    ("Who scored England's goal in the 1966 World Cup final?", ["Geoff Hurst", "Martin Peters", "Bobby Charlton", "Roger Hunt"], 0),
    ("What is the smallest country by population to qualify for a World Cup?", ["Iceland", "Trinidad and Tobago", "Slovenia", "Jamaica"], 0),
    ("Who was the oldest player to participate in a World Cup?", ["Essam El-Hadary", "Peter Shilton", "Dino Zoff", "Roger Milla"], 0),
    ("What is the name of the World Cup trophy?", ["FIFA Cup", "Jules Rimet Trophy", "World Cup Trophy", "Victory Cup"], 2),
    ("Which country hosted and won the World Cup in 1998?", ["France", "Brazil", "Italy", "Spain"], 0)
]

def ask_trivia_question():
    # No more questions left
    if not trivia:
        return

    question, options, correct_index = random.choice(trivia)
    trivia.remove((question, options, correct_index))

    print("\n\033[1m"+question +"\033[0m")
    for i, option in enumerate(options):
        print(f"({i + 1}) {option}")

    user_choice = helper_functions.checkValidInputInt(4,1,"\033[1mChoose your answer:\033[0m ")

    if int(user_choice)-1 == correct_index:
        return True
    else:
        print("\n\033[31mIncorrect...\033[0m\nThe answer is\033[1m", options[correct_index], "\033[0m\n")
        return False
