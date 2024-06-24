# R-OSE flight parameters v1.3
# Input section

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import re, math, os, csv
from flight_result import Flight_result
from datetime import datetime

# Setting utc time for data 
now = datetime.utcnow()
dt_string = now.strftime("%d/%m/%y-%H:%M-UTC")
#print(dt_string)

class Flight_input():

	def __init__(self):
		# Setting window paramater
		self.main_window = Tk()
		self.main_window.title("R-OSE : The stratospheric balloon flight parameters")
		self.main_window.geometry("1120x1060")
		self.main_window.minsize(1120,1060)
		self.main_window.config(background='#cacfcc')

		# Setting principal frame
		self.top_frame = Frame(self.main_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)
		self.section1_frame = Frame(self.main_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)
		self.section2_frame = Frame(self.main_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)
		self.alert_section_frame = Frame(self.main_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)		
		self.bottom_frame = Frame(self.main_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)

		self.create_widgets()

		# Declare position of section
		self.top_frame.pack()
		self.section1_frame.pack()
		self.section2_frame.pack()
		self.alert_section_frame.pack()		
		self.bottom_frame.pack()


	def create_widgets(self):
		# Setting main section
		self.create_title()
		self.create_subtitle()
		self.create_logo()

		self.create_flight_parameter()
		self.create_air_density_parameter()
		self.create_alert_section()
		self.create_button()	

	#---------------------------------Top Section-----------------------------------#

	def create_title(self):
		title_text = "Welcome to the stratospheric balloon flight parameters"
		label_title = Label(self.top_frame, text=title_text, font=("babel", 15), bg='#cacfcc', fg='black')
		label_title.pack()

	def create_subtitle(self):
		subtitle_text = "Designed by R-OSE \n and inspired from the Tawhiri CUSF Landing Prediction Software"
		label_subtitle = Label(self.top_frame, text=subtitle_text, font=("babel", 10), bg='#cacfcc', fg='black')
		label_subtitle.pack()

	def create_logo(self):
		image = Image.open("logo_v4_2.png")
		img = image.resize((500,200))
		self.logo = ImageTk.PhotoImage(img)
		self.label_logo = tk.Label(self.top_frame, image=self.logo)
		self.label_logo.image = self.logo  # Keep a reference to the image object
		self.label_logo.pack(pady=10)

	def read_data(self):		
		if os.path.exists("save_flight_data.csv") == False:
			# First use of the program or if data is erase, default. 
			self.payload_mass = ""
			self.balloon_mass = ""
			self.balloon_nb = ""
			self.launch_volume = ""
			self.parachute_diameter = ""
			self.excess_weight_neck_lift = ""			
			self.temperature_celcius = ""
			self.ambient_pressure = 101.3
			self.humidity_level = ""				
		else:
			with open("save_flight_data.csv", "r") as file:
				# Show the last recorded data
				last_line = file.readlines()[-1]			
				last_line = last_line.strip("\n")
				last_line = [x for x in last_line.split(",") if x!=""]					
				self.payload_mass = last_line[-9]
				self.balloon_mass = last_line[-8]
				self.balloon_nb = last_line[-7]
				self.launch_volume = last_line[-6]
				self.parachute_diameter = last_line[-5]
				self.excess_weight_neck_lift = last_line[-4]				
				self.temperature_celcius = last_line[-3]
				self.ambient_pressure = last_line[-2]
				self.humidity_level = last_line[-1]						
		return 			

#-----------------------------------Section 1------------------------------------------#

	def create_flight_parameter(self):
		# Add last data in these section from read_data function  
		self.read_data()

		# Title row
		label_flight_parameter_title = Label(self.section1_frame, text="Flight Parameter", font=("babel 12 underline"), bg='#cacfcc', fg='black')
		label_flight_parameter_title.grid(row=0, column=0, columnspan=2, pady=5)

		# Payload Mass
		label_payload_mass = Label(self.section1_frame, text="Payload Mass (g) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_payload_mass.grid(row=1, column=0, sticky=W)		
		self.input_payload_mass = Entry(self.section1_frame, font=("babel", 12), bg='white', fg='black')
		self.input_payload_mass.grid(row=1, column=1)
		default_last_payload_mass = self.payload_mass
		self.input_payload_mass.insert(0, default_last_payload_mass)

		# Balloon Mass
		label_balloon_mass = Label(self.section1_frame, text="Balloon Mass (g) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_balloon_mass.grid(row=2, column=0, sticky=W)
		self.input_balloon_mass = Entry(self.section1_frame, font=("babel", 12), bg='white', fg='black')
		self.input_balloon_mass.grid(row=2, column=1)
		default_last_balloon_mass = self.balloon_mass
		self.input_balloon_mass.insert(0, default_last_balloon_mass)

		# Balloon Number
		label_balloon_number = Label(self.section1_frame, text="Balloon Number :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_balloon_number.grid(row=3, column=0, sticky=W)
		self.input_balloon_number = Entry(self.section1_frame, font=("babel", 12), bg='white', fg='black')
		self.input_balloon_number.grid(row=3, column=1)
		default_last_balloon_number = self.balloon_nb
		self.input_balloon_number.insert(0, default_last_balloon_number)

		# Launch Volume
		label_launch_volume = Label(self.section1_frame, text="Launch Volume (m\u00b3) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_launch_volume.grid(row=4, column=0, sticky=W)
		self.input_launch_volume = Entry(self.section1_frame, font=("babel", 12), bg='white', fg='black')
		self.input_launch_volume.grid(row=4, column=1)		 
		default_last_launch_volume = self.launch_volume
		self.input_launch_volume.insert(0, default_last_launch_volume)

		# Parachute diameter
		label_parachute_diameter = Label(self.section1_frame, text="Parachute diameter (m) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_parachute_diameter.grid(row=5, column=0)
		self.input_parachute_diameter = Entry(self.section1_frame, font=("babel", 12), bg='white', fg='black')
		self.input_parachute_diameter.grid(row=5, column=1) 
		default_last_parachute_diameter = self.parachute_diameter
		self.input_parachute_diameter.insert(0, default_last_parachute_diameter)

		# Excess Weight Neck lift
		label_excess_weight_neck_lift_title = Label(self.section1_frame, text="Balloon filling tube (g) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_excess_weight_neck_lift_title.grid(row=6, column=0, sticky=W)
		self.input_excess_weight_neck_lift = Entry(self.section1_frame, font=("babel", 12), bg='white', fg='black')
		self.input_excess_weight_neck_lift.grid(row=6, column=1)		
		defaut_last_excess_weight_neck_lift = self.excess_weight_neck_lift
		self.input_excess_weight_neck_lift.insert(0, defaut_last_excess_weight_neck_lift)


#------------------------------Section 2--------------------------------------#

	def create_air_density_parameter(self):
		# Add last data in these section from read_data function  
		self.read_data()

		# Title Air Density
		label_air_density_title = Label(self.section2_frame, text="Air density parameter", font=("babel 12 underline"), bg='#cacfcc', fg='black')
		label_air_density_title.grid(row=0, column=0, columnspan=2, pady=5)
	
		# Subtitle note
		note = "From launch day and time"
		label_air_density_note = Label(self.section2_frame, text=note, font=("babel", 10), bg='#cacfcc', fg='black')
		label_air_density_note.grid(row=1, column=0, columnspan=2)

		# Temperature
		label_temperature_celcius = Label(self.section2_frame, text="Temperature (°C) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_temperature_celcius.grid(row=2, column=0, sticky=W)
		self.input_temperature_celcius = Entry(self.section2_frame, font=("babel", 12), bg='white', fg='black')
		self.input_temperature_celcius.grid(row=2, column=1)
		default_last_temperature = self.temperature_celcius
		self.input_temperature_celcius.insert(0, default_last_temperature)

		# Pressure
		label_ambient_pressure_title = Label(self.section2_frame, text="Ambient pressure (kPa) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_ambient_pressure_title.grid(row=3, column=0, sticky=W)
		self.input_ambient_pressure = Entry(self.section2_frame, font=("babel", 12), bg='white', fg='black')
		self.input_ambient_pressure.grid(row=3, column=1)		
		default_last_ambiant_pressure = self.ambient_pressure
		self.input_ambient_pressure.insert(0, default_last_ambiant_pressure)

		# Humidity Level
		label_humidity_level_title = Label(self.section2_frame, text="Humidity level (%) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_humidity_level_title.grid(row=4, column=0, sticky=W)
		self.input_humidity_level = Entry(self.section2_frame, font=("babel", 12), bg='white', fg='black')
		self.input_humidity_level.grid(row=4, column=1)		
		default_last_humidity_level = self.humidity_level
		self.input_humidity_level.insert(0, default_last_humidity_level)

	def create_alert_section(self):
		# Alert row
		self.label_alert = Label(self.alert_section_frame, text="", font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_alert.pack(pady=10)	

	def add_data_values(self):
		# Show alert info if needed 		
		self.label_alert.config(text="")
		if len(self.input_payload_mass.get())==0 or len(self.input_balloon_mass.get())==0 or len(self.input_balloon_number.get())==0 or len(self.input_launch_volume.get())==0 or len(self.input_parachute_diameter.get())==0 or len(self.input_excess_weight_neck_lift.get())==0 or len(self.input_temperature_celcius.get())==0 or len(self.input_ambient_pressure.get())==0 or len(self.input_humidity_level.get())==0:
			self.label_alert.config(text = "You must fill the fields!")	
		else:
			try:
				# Adding input in variable
				payload_mass = float(self.input_payload_mass.get())
				balloon_mass = float(self.input_balloon_mass.get())
				balloon_nb = int(self.input_balloon_number.get())					
				launch_volume = float(self.input_launch_volume.get())
				parachute_diameter = float(self.input_parachute_diameter.get())	
				excess_weight_neck_lift = float(self.input_excess_weight_neck_lift.get())
				temperature_celcius = float(self.input_temperature_celcius.get())
				ambient_pressure = float(self.input_ambient_pressure.get())
				humidity_level = float(self.input_humidity_level.get())
				if parachute_diameter == 0:
					# Please use a parachute
					self.label_alert.config(text = "Warning : You must add a parachute!")
			except ValueError:
				# To prevent errors in calculations in the next step
				self.label_alert.config(text="Only digit in the fields!")
			finally:			
				# If all input is good, it's time to save everything
				def save_data():
					# Saving input variable for data file
					date_time = dt_string																			
					data_file.writerow([date_time, payload_mass, balloon_mass, balloon_nb, launch_volume, parachute_diameter , excess_weight_neck_lift, temperature_celcius, ambient_pressure, humidity_level])
								
				if os.path.exists("save_flight_data.csv") == False:
				# For first use or if data file doesn't exist			
					with open("save_flight_data.csv", "w") as file:
						data_file = csv.writer(file)						
						data_file.writerow(["date_time","payload_mass(g)", "balloon_mass(g)", "nb_ballon", "launch_vol(m\u00b3)", "parachute_diameter(m)", "excess_weight_neck_lift(g)", "temperature_°C", "ambient_pressure(kPa)", "humidity_level(%)"])
						save_data()											
				else:
				# Adding data in the file			
					with open("save_flight_data.csv", "a") as file:
						data_file = csv.writer(file)
						save_data()		

				# Open the result window
				self.main_window.destroy()				
				start = Flight_result()
				start.rc_window.mainloop()


#------------------------------Bottom section--------------------------------------#

	def create_button(self):
		# Calculate button --> Execute add_data_values, checking input and saving + Open new window
		calculate_button = Button(self.bottom_frame, text="Calculate", font=("babel", 12), bg='#cacfcc', fg='black', command=self.add_data_values)
		calculate_button.grid(row=0, column=1 , padx=30, ipadx=100, ipady=8 , pady=20)

		# Close program
		close_button = Button(self.bottom_frame, text="Close", font=("babel", 14), bg='#cacfcc', fg='black', command=self.close_main_window)
		close_button.grid(row=0, column=2, padx=30, ipadx=80, ipady=5 , pady=20)	
				
	def close_main_window(self):
		self.main_window.destroy()

if __name__ == "__main__":
	start = Flight_input()
	start.main_window.mainloop()	



if __name__ == "__main__":
	start = Flight_result()
	start.rc_window.mainloop()
