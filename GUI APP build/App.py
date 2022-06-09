import tkinter as tk
from tkinter import Canvas, filedialog, Text
import os
#Aplikācija

root = tk.Tk()
apps = []
#terminala parada faila nosaukumu
if os.path.isfile("save.txt"):
    with open("save.txt", "r") as f:
        tempApps = f.read()
        tempApps = tempApps.split(",")
    
        apps = [x for x in tempApps if x.strip()] #Nonem atstarpes starp viens otru, kad palaiž no jauna


#Ar pogu pievienot failus.
def addapp():
    
#Pievienojot jaunu failu vienu vins pastums uz leju un otro uz augšu.
    for widget in frame.winfo_children():
        widget.destroy()


     #Pievieno failu un iekraso viņu apkart ar krāsu   
    filename= filedialog.askopenfilename(initialdir="/", title="Select File",
    filetypes=(("executables","*.exe"), ("all files","*.*")))
    apps.append(filename)
    print(filename)
    for app in apps:
        label = tk.Label(frame, text=app, bg="red")
        label.pack()


#Palaist aplikācijas kuras ir izvelētas

def runApps():
    for app in apps:
        os.startfile(app)


#Background Krāsa un izmēri apliācijai

Canvas = tk.Canvas(root, height=700, width=700, bg="lightblue")
Canvas.pack()

# Virs slānu krāsa neliels rāmītis.

frame = tk.Frame(root, bg="white")
frame.place(relheight=0.8, relwidth=0.8, relx=0.1, rely=0.1)

#Pogas

openfile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="black", command=addapp)
openfile.pack()

runApps = tk.Button(root, text="Run apps", padx=10, pady=5, fg="white", bg="black", command=runApps)
runApps.pack()

#Ielāde saglabātos failus, pēc izslegšanas un ieslēgšanas.
for app in apps:
    label= tk.Label(frame, text=app)
    label.pack()


root.mainloop()

# izveido failu un saglabā izvēlētos failus.
with open('save.txt', 'w') as f:
    for app in apps:
        f.write(app+ ",")