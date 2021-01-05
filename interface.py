import myFunctions
import requests
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

import io
from PIL import Image, ImageTk
from urllib.request import urlopen


myFunctions.textPrettier()

class Application:
  
  colores = {
    "bg": "#263238", 
    "fg":"white", 
    "btnExit":"#b41323", 
    "btnConsulta":"#035e03"}

  def __init__(self, wind):
    super().__init__()
    self.wind = wind
    self.wind.resizable(False, False)
    self.wind.title("COVID-19")
    self.wind.iconbitmap("virus.ico")
    self.wind.config(bg = Application.colores["bg"])
    #Frame data
    self.frame_main_data = tk.Frame(self.wind, bg = Application.colores["bg"])

    tk.Label(
      self.frame_main_data, 
      text = "Country: ", 
      font = ("bold"),
      bg = Application.colores["bg"], 
      fg = Application.colores["fg"]
      ).grid(row = 0, column = 0)

    self.combo_Countrys = ttk.Combobox(self.frame_main_data, width = 30)
    self.combo_Countrys.grid(row = 0, column = 1)
    #Importante, extrae todos los datos de los paises en la API
    self.get_countrys()
    self.frame_main_data.grid(row = 0, column = 0, pady = (20, 20), padx = (20, 20))
    #end frame data country
    #starts frame btns of main window
    self.frame_main_btns = tk.Frame(self.wind, bg = Application.colores["bg"])
    
    btnSalir = tk.Button(
      self.frame_main_btns, 
      text = "Salir", 
      bd = 5, 
      fg = Application.colores["fg"], 
      bg = Application.colores["btnExit"], 
      command = self.wind.destroy, 
      width = 15)
    btnSalir.grid(row = 0, column = 0, sticky = "WE", padx = (0, 15))
    
    btnConsulta = tk.Button(
      self.frame_main_btns, 
      text = "Consulta", 
      bd = 5, 
      fg = Application.colores["fg"],
      bg = Application.colores["btnConsulta"],
      command = self.consulta,
      width = 15
      )
    btnConsulta.grid(row = 0, column = 1, sticky = "WE", padx = (15, 0))
    
    self.frame_main_btns.grid(row = 1, column = 0, pady = (0, 20))
    #frame global data:
    self.global_data = tk.Frame(self.wind, bg = Application.colores["bg"])
    self.global_info = requests.get("https://api.covid19api.com/summary").json()
    
    self.NewConfirmedCases = myFunctions.place_value(self.global_info["Global"]["NewConfirmed"])
    self.TotalConfirmed = myFunctions.place_value(self.global_info["Global"]["TotalConfirmed"])
    self.NewDeaths = myFunctions.place_value(self.global_info["Global"]["NewDeaths"])
    self.GlobalDeaths = myFunctions.place_value(self.global_info["Global"]["TotalDeaths"])
    self.NewRecovered = myFunctions.place_value(self.global_info["Global"]["NewRecovered"])
    self.TotalRecovered = myFunctions.place_value(self.global_info["Global"]["TotalRecovered"])

    tk.Label(self.global_data, text = "Nuevos casos confirmados: ", bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 0, column = 0, sticky = "E")
    tk.Label(self.global_data, text = self.NewConfirmedCases, bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 0, column = 1)
    
    tk.Label(self.global_data, text = "Total casos confirmados: ", bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 1, column = 0, sticky = "E")
    tk.Label(self.global_data, text = self.TotalConfirmed, bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 1, column = 1)
    
    tk.Label(self.global_data, text = "Nuevos casos fallecidos: ", bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 2, column = 0, sticky = "E")
    tk.Label(self.global_data, text = self.NewDeaths, bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 2, column = 1)

    tk.Label(self.global_data, text = "Total fallecidos: ", bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 3, column = 0, sticky = "E")
    tk.Label(self.global_data, text = self.GlobalDeaths, bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 3, column = 1)

    tk.Label(self.global_data, text = "Nuevos casos de recuperados: ", bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 4, column = 0, sticky = "E")
    tk.Label(self.global_data, text = self.NewRecovered, bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 4, column = 1)
    
    tk.Label(self.global_data, text = "Total casos recuperados: ", bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 5, column = 0, sticky = "E")
    tk.Label(self.global_data, text = self.TotalRecovered, bg = Application.colores["bg"], fg = Application.colores["fg"], font = ("bold")).grid(row = 5, column = 1)
    
    self.theMessage = tk.StringVar()
    self.message = tk.Label(self.global_data, textvariable = self.theMessage, bg = Application.colores["bg"], fg = Application.colores["fg"] ).grid(row = 6, column = 0, columnspan = 2, rowspan = 2)

    self.global_data.grid(row = 2, column = 0, sticky = "WE")
    #end frame global data

  def get_countrys(self):
    list_countrys = []
    my_request = requests.get("https://api.covid19api.com/countries").json()
    for i in range(len(my_request)):
      list_countrys.append(my_request[i]["Country"])
    list_countrys.sort()
    self.combo_Countrys["values"]  = list_countrys
    self.combo_Countrys["state"] = "readonly"
    
  def consulta(self):
    self.usr_country = self.combo_Countrys.get()
    if len(self.usr_country) == 0:
      messagebox.showerror("Campo vacio", "Se debe de elegir un país para realizar la consulta")
    else:
      try:
        self.Date = []
        self.Confirmed = []
        self.Deaths = []
        self.Recovered = []
        self.Active = []
        dataCountry = requests.get(f"https://api.covid19api.com/dayone/country/{self.usr_country}").json()
        for i in range(len(dataCountry)):
          self.Date.append(dataCountry[i]["Date"][:10])
          self.Confirmed.append(dataCountry[i]["Confirmed"])
          self.Deaths.append(dataCountry[i]["Deaths"])
          self.Recovered.append(dataCountry[i]["Recovered"])
          self.Active.append(dataCountry[i]["Active"])
        
        try:
          if len(self.Date) != 0:
            self.theMessage.set("")

            plt.plot(self.Active, marker = "+", color = "darkred", linestyle = ":")
            plt.plot(self.Recovered, marker = ".", color = "forestgreen", linestyle = ":")
            plt.plot(self.Confirmed, marker = "o", color = "darkorange", linestyle = ":")
            plt.plot(self.Deaths, marker = "x", color = "black", linestyle = ":")
            
            plt.title("Afectaciones de COVID-19 en {}".format(self.usr_country))
            
            plt.ylabel("No. Casos")
            ls = len(self.Date) - 1
            plt.xlabel(
              f"Dias transcurridos desde el día 0\nPeriodo: {self.Date[0]} al {self.Date[ls]}\nAl {self.Date[ls]} hay Activos: {myFunctions.place_value(self.Active[ls])} | Recuperados: {myFunctions.place_value(self.Recovered[ls])} | Confirmados: {myFunctions.place_value(self.Confirmed[ls])} | Fallecidos: {myFunctions.place_value(self.Deaths[ls])}"
              )
            
            plt.legend(["Activos","Recuperados","Confirmados","fallecidos"])
            plt.grid(linestyle='-', linewidth=.5)
            # plt.grid(color='r', linestyle='-', linewidth=2)
            
            plt.show()
          else:
            self.theMessage.set(f"El servidor no cuenta con información de: {self.combo_Countrys.get()}")

        except KeyError:
          print("error de key error")
      except NameError:
        print(NameError)
      #day 1 = https://api.covid19api.com/dayone/country/south-africa/status/confirmed