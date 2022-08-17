from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.colorchooser import askcolor
import requests, json
import string
import sqlite3

connection = sqlite3.connect("palettes.db")


cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS colors (color1 TEXT, color2 TEXT, color3 TEXT)")

root = Tk()
root.title("Outfitist")
root.geometry("900x700")

paletteColors = ["","",""]

def change_color(colorNum):
    colors = askcolor(title="Tkinter Color Chooser")
    if colorNum == 1 :
        color1.configure(bg=colors[1])
        paletteColors[0] = colors[1]
    elif colorNum == 2 :
        color2.configure(bg=colors[1])
        paletteColors[1] = colors[1]
    elif colorNum == 3 :
        color3.configure(bg=colors[1])
        paletteColors[2] = colors[1]

def savePalette():
    busted_display = Label(root, text="Added new palette", font=("Arial", "13"))
    busted_display.place(x=645,y=140)
    root.after(2000, busted_display.destroy)
    cursor.execute("INSERT INTO colors VALUES ('"+paletteColors[0]+"', '"+paletteColors[1]+"', '"+paletteColors[2]+"')")
    connection.commit()
    return True

def updateWeather():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = cityBox.get()
    API_KEY = "2b540f45bc7ca92b95eb259f5ddd9e46"
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperatureKelvin = main['temp']
        temperatureDegrees = 1.8*(temperatureKelvin-273) + 32
        report = data['weather']
        weatherInfo.set(string.capwords(str(report[0]['description'])))
        tempVar.set(str(round(temperatureDegrees)) + "°F")
    else:
        weatherInfo.set("Error in the HTTP request")

    outfitInfo.set("")

    if any(item['main'].lower() == 'rain' for item in report):
        outfitInfo.set("\t• Gear up for some rain!\n")
    if any(item['main'].lower() == 'snow' for item in report):
        outfitInfo.set("\t• Gear up for some snow!\n")
    if any(item['main'].lower() == 'drizzle' for item in report):
        outfitInfo.set("\t• Watch out for some drizzling!\n")

    temperatureDegrees = round(temperatureDegrees)
    if temperatureDegrees < 70:
        outfitInfo.set(outfitInfo.get() + "\t• Wear some long sleeves and pants")
    if temperatureDegrees >= 70 and temperatureDegrees <= 75:
        outfitInfo.set(outfitInfo.get() + "\t• Wear either long sleeves and pants or a t-shirt and shorts")
    if temperatureDegrees > 76:
        outfitInfo.set(outfitInfo.get() + "\t• Wear a t-shirt and shorts")
    
    getColorPalette()

def getColorPalette():
    randomrow = cursor.execute("SELECT * FROM colors ORDER BY RANDOM() LIMIT 1").fetchall()
    row = randomrow[0]
    outfitColor1.place(x=506,y=300)
    outfitColor2.place(x=551,y=300)
    outfitColor3.place(x=596,y=300)

    randomButton.place(x=527,y=340)

    outfitColor1.configure(bg=row[0])
    outfitColor2.configure(bg=row[1])
    outfitColor3.configure(bg=row[2])


#Color palette buttons 
test = Label(root, text="Create Color Palette", font=("Arial",13,'bold'))
test.place(x=631,y=12)

color1 = Label(root, text="    ",bg="white", font=("Arial", 25))
color1.bind("<Button-1>", lambda e: change_color(1))
color2 = Label(root, text="    ",bg="white", font=("Arial", 25))
color2.bind("<Button-1>", lambda e: change_color(2))
color3 = Label(root, text="    ",bg="white", font=("Arial", 25))
color3.bind("<Button-1>", lambda e: change_color(3))
color1.place(x=636,y=50)
color2.place(x=681,y=50)
color3.place(x=726,y=50)
Button(root, text="Save", command=savePalette).place(x=665,y=100)

#Weather
weatherLabel = Label(root, text="Weather",font=("Arial",13,'bold'))
weatherLabel.place(x=40,y=10)
cityLabel = Label(root, text="City: ")
cityLabel.place(x=40,y=40)
cityBox = Entry(root, width=15)
cityBox.insert(0, "Budd Lake")
cityBox.place(x=75,y=40)
Button(root, text='→', command=updateWeather).place(x=222,y=38)

weatherInfo = StringVar()
weatherInfo.set("")
weatherInfoLabel = Label(root, textvariable=weatherInfo, font=("Arial", 25, "bold"))
weatherInfoLabel.place(x=40,y=160)

tempVar = StringVar()
tempVar.set("")
temperatureLabel = Label(root, textvariable=tempVar, font=("Arial", 50, "bold")).place(x=40,y=100)

#Outfit
Label(root, text="Outfit Recommendations:",font=("Arial",13,'bold')).place(x=40,y=230)
outfitInfo = StringVar()
outfitInfo.set("")
outfitInfoLabel = Label(root, textvariable=outfitInfo,anchor='w',justify='left')
outfitInfoLabel.place(x=40,y=250)

colorStringVar = StringVar()
outfitColor1 = Label(root, text="    ", bg="white", font=("Arial", 25))
outfitColor2 = Label(root, text="    ", bg="white", font=("Arial", 25))
outfitColor3 = Label(root, text="    ", bg="white", font=("Arial", 25))

randomButton = Button(root, text="Random", command=getColorPalette)


root.mainloop()
