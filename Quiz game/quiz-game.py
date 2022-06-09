
print ("Welcome to my little quiz!")

playing = input("Do you want to play?" )

if playing.lower() != "yes":
    quit()

print ("Okey! Lets play:")
score = 0

answer = input("What does CPU stand for? ")
if answer.lower() == "central processing unit":
    print('Correct!')
    score += 1
else:
    print('Incorrect!')

answer = input("What does GPU stand for? ")
if answer.lower() == "graphics processing unit":
    print('Correct!')
    score += 1
else:
    print('Incorrect!')

print("You got " + str(score) + " Question correct!" )
print("You got " + str((score / 4 ) * 100 ) + "%. " )