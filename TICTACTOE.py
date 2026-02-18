from tkinter import *
from tkinter import messagebox 

def Buttonclicker(button):
    global PlayerX, monitor 
    if button["text"] == "" and PlayerX == True:
        button["text"] = "X"
        PlayerX = False
        PlayerWinner()
        monitor = monitor + 1
        LabelTurn()
    elif button ["text"] == "" and PlayerX == False:
        button["text"] = "O"
        PlayerX = True
        PlayerWinner()
        monitor = monitor + 1
        LabelTurn()
    else:
        messagebox.showinfo("Error", "You already entered!!!")


# 123,456,789,159,357,147,258,369

def Resetround():
     global PlayerX, monitor, button1,button2,button3,button4,button5,button6,button7,button8,button9,button10 
     PlayerX = True
     monitor = 0
     
     for btn in [button1, button2, button3, button4, button5, button6, button7, button8, button9]:
        btn["text"] = ""
        btn["bg"] = "#D2B48C"
     LabelTurn()



def Buttonwinner(b1,b2,b3):
    b1["bg"] = "green"
    b2["bg"] = "green"
    b3["bg"] = "green"


def LabelTurn():
     global Playerxturn, Playeroturn, PlayerX
     if PlayerX == True:
          Playerxturn.place(x=25, y=300)
          Playeroturn.place_forget()
     else:    
          Playeroturn.place(x=625, y=300)
          Playerxturn.place_forget()


def HideLabels():
     global Playerxturn, Playeroturn
     Playerxturn.place_forget()
     Playeroturn.place_forget()


def PlayerWinner():
    global button1,button2,button3,button4,button5,button6,button7,button8,button9
    if button1["text"] == "X" and button2["text"] == "X" and button3["text"] == "X" or button4["text"] == "X" and button5["text"] == "X" and button6["text"] == "X" or button7["text"] == "X" and button8["text"] == "X" and button9["text"] == "X" or button1["text"] == "X" and button5["text"] == "X" and button9["text"] == "X" or button3["text"] == "X" and button5["text"] == "X" and button7["text"] == "X" or button1["text"] == "X" and button4["text"] == "X" and button7["text"] == "X" or button2["text"] == "X" and button5["text"] == "X" and button8["text"] == "X" or button3["text"] == "X" and button6["text"] == "X" and button9["text"] == "X":
       if button1["text"] == "X" and button2["text"] == "X" and button3["text"] == "X":
            Buttonwinner(button1,button2,button3)
       if button4["text"] == "X" and button5["text"] == "X" and button6["text"] == "X":
            Buttonwinner(button4,button5,button6)
       if button7["text"] == "X" and button8["text"] == "X" and button9["text"] == "X":
            Buttonwinner(button7,button8,button9)
       if button1["text"] == "X" and button5["text"] == "X" and button9["text"] == "X":
            Buttonwinner(button1,button5,button9)       
       if button3["text"] == "X" and button5["text"] == "X" and button7["text"] == "X":
            Buttonwinner(button3,button5,button7)
       if button1["text"] == "X" and button4["text"] == "X" and button7["text"] == "X":
            Buttonwinner(button1,button4,button7)    
       if button2["text"] == "X" and button5["text"] == "X" and button8["text"] == "X":
            Buttonwinner(button2,button5,button8)
       if button3["text"] == "X" and button6["text"] == "X" and button9["text"] == "X":
            Buttonwinner(button3,button6,button9)
       HideLabels()
       messagebox.showinfo("Congrats!!!!!!","Player X Won!")
       Resetround()

    elif button1["text"] == "O" and button2["text"] == "O" and button3["text"] == "O" or button4["text"] == "O" and button5["text"] == "O" and button6["text"] == "O" or button7["text"] == "O" and button8["text"] == "O" and button9["text"] == "O" or button1["text"] == "O" and button5["text"] == "O" and button9["text"] == "O" or button3["text"] == "O" and button5["text"] == "O" and button7["text"] == "O" or button1["text"] == "O" and button4["text"] == "O" and button7["text"] == "O" or button2["text"] == "O" and button5["text"] == "O" and button8["text"] == "O" or button3["text"] == "O" and button6["text"] == "O" and button9["text"] == "O":
       if button1["text"] == "O" and button2["text"] == "O" and button3["text"] == "O":
            Buttonwinner(button1,button2,button3)
       if button4["text"] == "O" and button5["text"] == "O" and button6["text"] == "O":
            Buttonwinner(button4,button5,button6)
       if button7["text"] == "O" and button8["text"] == "O" and button9["text"] == "O":
            Buttonwinner(button7,button8,button9)
       if button1["text"] == "O" and button5["text"] == "O" and button9["text"] == "O":
            Buttonwinner(button1,button5,button9)       
       if button3["text"] == "O" and button5["text"] == "O" and button7["text"] == "O":
            Buttonwinner(button3,button5,button7)
       if button1["text"] == "O" and button4["text"] == "O" and button7["text"] == "O":
            Buttonwinner(button1,button4,button7)    
       if button2["text"] == "O" and button5["text"] == "O" and button8["text"] == "O":
            Buttonwinner(button2,button5,button8)
       if button3["text"] == "O" and button6["text"] == "O" and button9["text"] == "O":
            Buttonwinner(button3,button6,button9)
       HideLabels()
       messagebox.showinfo("Congrats!!!!!!","Player O Won!")  
       Resetround()
    elif monitor ==8:
        HideLabels()
        messagebox.showinfo("","This game are tied!")
        Resetround()


window = Tk()
window.geometry('750x600')
window.title('Tic Tac Toe')
window.config(bg="#AF8258")

PlayerX = True

# monitor is for checking if all buttons are touchable
monitor = 0


#top
button1 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button1))
button1.place(x=225, y=150, anchor='center')

button2 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button2))
button2.place(x=375, y=150, anchor='center')

button3 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button3))
button3.place(x=525, y=150, anchor='center')

#mid
button4 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button4))
button4.place(x=225, y=300, anchor='center')

button5 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button5))
button5.place(x=375, y=300, anchor='center')

button6 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button6))
button6.place(x=525, y=300, anchor='center')

#bot
button7 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button7))
button7.place(x=225, y=450, anchor='center')

button8 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button8))
button8.place(x=375, y=450, anchor='center')

button9 = Button(window, text="", bg="#D2B48C", fg="black", font=("Arial", 32, "bold"), width=5, height=2, command=lambda: Buttonclicker(button9))
button9.place(x=525, y=450, anchor='center')

#Reset button

button10 = Button (window, text="Reset",bg="#D2B48C", fg="black", font=("arial",10,"bold"), width=5, height= 1,command= Resetround)
button10.place(x=375, y=550, anchor="center")

#Turn
Playerxturn = Label(window,text="Player X Turn", fg="black", font=("arial",12,"bold"),bg="#AF8258")
Playeroturn = Label(window,text="Player O Turn", fg="black", font=("arial",12,"bold"),bg="#AF8258")

LabelTurn()

window.mainloop()