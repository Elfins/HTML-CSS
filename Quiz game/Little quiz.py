print("Welcome!")


player = input("would you like to anwser some questions? ") #Tiek uzdots jautajums ar iespēju atbildet "input"

if player.lower() != "yes": #Ja ievada "Yes" programma turpinās, ja tiek uzrakstīts kaut kas cits programma izslēdzās.
    quit()

print("Great! Let me ask you some questions") #ja tiek atbildets ar "Yes" parādās frāze :print

#1. daļa
answer = input("Is it raining outside? ") #Jautajums - vai laukā līst lietus.
if answer.lower() == "no": #ja atbilde ir vienāda ar "no" parādas "print" un programma izslēdzās.
    print('Great! You can go outside.')
    quit()


 #2. daļa
if answer.lower() == "yes": #ja atbilde ir vienāda ar '== "Yes"' programma paziņo "print"
    print('Ohh!')

answer = input("Do you have umbrella? ") #Jautajums vai tev ir lietussargs?
if answer.lower() == "yes": #Ja atbilde ir vienāda ar '== "Yes"' tiek izprintets "print" programma izsledzas.
    print('Great! you can go outside!')
    quit()

#3. daļa
if answer.lower() == "no": #Ja atbilde uz jautajumu ir vienāda "== "no", tad tiek paziņots "print"
    print("Better wait a bit for it to settle down.")

while True:   #Kamer atbilde uz jautajumu "Is it still raining?" bus vienāda ar (== "yes") tiks paziņots "print" taču jautājums tiks visu laiku atkartots kamēr atbilde nebūs "No"
    answer = input("Is it still raining? ")
    if answer.lower() == "yes":
        print('Okey, better wait abit more')
        continue #kamer atbilde bus "Yes" jautajumu atkartos.
    if answer.lower() == "no": #kad atbilde ir "no" tiek izprintēts "print"
        print('Great! you can go outside.')
        break

print("Thanks for your anwsers, have a great day! ") #Beidzoties jautājumiem pazino "print"