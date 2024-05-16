# R-OSE flight simulator v1.3
# Result section

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import re, math, os, csv, pyperclip, webbrowser

class Flight_result():

	def __init__(self):
		#rc = Result Calculator
		self.rc_window = Tk()		
		self.rc_window.title("R-OSE : The stratospheric balloon flight simulator")
		self.rc_window.geometry("1100x1100")
		self.rc_window.minsize(1100,1000)
		#self.rc_window.resizable(width=False, height= False)
		self.rc_window.config(background='#cacfcc')

		self.rc_top_frame = Frame(self.rc_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)
		self.rc_section1_frame = Frame(self.rc_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)
		self.rc_section2_frame = Frame(self.rc_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)
		self.rc_bottom_frame = Frame(self.rc_window, bg='#cacfcc', bd=0, relief=RAISED, highlightthickness=0)

		self.create_widgets()

		self.rc_top_frame.pack()
		self.rc_section1_frame.pack()
		self.rc_section2_frame.pack()		
		self.rc_bottom_frame.pack()		

	def create_widgets(self):
		self.create_title()
		self.create_subtitle()
		self.create_logo()	

		self.create_result_parameter()
		self.create_variable_parameter()
		self.create_constant_parameter()
		self.create_button()


#---------------------------------Top Section-----------------------------------#

	def create_title(self):
		title_text = "Welcome to the stratospheric balloon flight simulator"
		label_title = Label(self.rc_top_frame, text=title_text, font=("babel", 15), bg='#cacfcc', fg='black')
		label_title.pack()

	def create_subtitle(self):
		subtitle_text = "Designed by R-OSE \n and inspired from the Tawhiri CUSF Landing Prediction Software"
		label_subtitle = Label(self.rc_top_frame, text=subtitle_text, font=("babel", 10), bg='#cacfcc', fg='black')
		label_subtitle.pack()
	
	
	def create_logo(self):		
		image = Image.open("logo_v4_2.png")
		img = image.resize((500,200))
		self.logo = ImageTk.PhotoImage(img)
		self.label_logo = tk.Label(self.rc_top_frame, image=self.logo)
		self.label_logo.pack(pady=10)
		
	def read_data(self):
		with open("save_flight_data.csv", "r") as file:
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

#------------------------------------------------Math--------------------------------------------#
	
	def calculate_total_mass(self):	
		self.read_data()		
		payload_m = float(self.payload_mass)
		balloon_m = float(self.balloon_mass)
		n = int(self.balloon_nb)
		total_mass = (payload_m + balloon_m*n)/1000
		descent_mass = (payload_m + ((n-1)*balloon_m))/1000
		return (total_mass, descent_mass)
		
	def calculate_balloon_geometry(self):
		self.read_data()
		launch_vol = float(self.launch_volume)
		pi = math.pi
		balloon_radius = ((3*launch_vol)/(4*pi))**(1/3)				
		balloon_area = (balloon_radius**2)*pi
		balloon_ground_diameter = round((balloon_radius*2),3)
		return (balloon_radius, balloon_area, balloon_ground_diameter)


	def calculate_air_density(self):	
		self.read_data()		
		humidity = float(self.humidity_level)
		pressure = 	float(self.ambient_pressure)
		temperature_celcius = float(self.temperature_celcius)

		humidity = humidity/100
		pressure = pressure*1000
		rs = 287.06 # J/Kg*K constant
		air_density = round((1/(rs*(273.15 + temperature_celcius)))*(pressure-(230.617*humidity*(math.e)**((17.625*temperature_celcius)/(243.04+temperature_celcius)))),3) 
		return air_density	


	def gaz_density(self):		
		he_density = 0.178
		difference_density = self.calculate_air_density()-he_density
		return (he_density, difference_density)

	def general_constant(self):
		gravity = 9.80665
		# Drag coefficient for a sphere is 0.47, 
		# But depending on the variation of the form it could vary between 0.30 to 0.47
		balloon_drag_coefficient = 0.35
		parachute_drag_coefficient = 2.3
		return (gravity, balloon_drag_coefficient, parachute_drag_coefficient)
	
	def calculate_neck_lift(self):
		self.read_data()	
		difference_gaz = self.gaz_density()	
		balloon_mass = float(self.balloon_mass)
		excess_weight = float(self.excess_weight_neck_lift)
		pi = math.pi
		balloon_radius = self.calculate_balloon_geometry()
		lift_off_mass = (((4/3)*pi*(balloon_radius[0]**3)*(difference_gaz[1])) - (balloon_mass/1000)) - excess_weight/1000									
		lift_off_message = round(lift_off_mass,2)					
		return lift_off_message	

	def burst_diameter(self):		
		self.read_data()
		balloon_m = float(self.balloon_mass)  				    
		burst_d = (((balloon_m**3)*0.00000000066346)-(0.0000040849*(balloon_m**2))+(0.01027*balloon_m+1.0102))	
		burst_diameter = round(burst_d, 3)
		return burst_diameter

	def burst_altitude(self):		
		self.burst_diameter()
		launch_vol = float(self.launch_volume)		
		pi = math.pi				        
		burst_alt = -7238.3*math.log(launch_vol/((((self.burst_diameter()/2)**3)*4*pi)/3))
		burst_altitude = round(burst_alt,0)		
		return burst_altitude 

	def ascent_velocity(self):
		gaz_difference = self.gaz_density()
		gravity = self.general_constant()
		balloon_dc = self.general_constant()
		total_mass = self.calculate_total_mass()
		self.read_data()
		launch_vol = float(self.launch_volume)		
		n = int(self.balloon_nb)
		balloon_area = self.calculate_balloon_geometry()

		try:		
			ascent_velocity = math.sqrt((gravity[0]*(-total_mass[0]+(n*(gaz_difference[1]*launch_vol))))/(0.5*balloon_dc[1]*self.calculate_air_density()*balloon_area[1]*n))			
			sd_ascent_velocity = round(ascent_velocity, 2)
			ascent_message = sd_ascent_velocity						
		except ValueError:
			ascent_message = "The balloon doesn't float!"						
		return ascent_message


	def descent_velocity(self):
		gaz_difference = self.gaz_density()
		gravity = self.general_constant()
		balloon_dc = self.general_constant()
		parachute_dc = self.general_constant()
		descent_mass = self.calculate_total_mass()
		self.read_data()
		launch_vol = float(self.launch_volume)		
		parachute_radius = float(self.parachute_diameter)	
		n = int(self.balloon_nb)
		balloon_area = self.calculate_balloon_geometry()
		balloon_radius = self.calculate_balloon_geometry()
		pi = math.pi 

		try:
			descent_velocity = math.sqrt((2*gravity[0]*(descent_mass[1]-((n-1)*(gaz_difference[1]))*(4/3*pi*(balloon_radius[0]**3))))/(self.calculate_air_density()*pi*(((n-1)*(balloon_dc[1]*(balloon_radius[0]**2)))+parachute_dc[2]*((parachute_radius/2)**2))))
			sd_descent_velocity = round(descent_velocity, 2)
			descent_message = sd_descent_velocity						
		except ValueError:
			descent_message = "The balloon doesn't descent"
		return descent_message

#-----------------------------------Section 1 Flight Result Parameter------------------------------------------#

	def create_result_parameter(self): 
		# Title row
		label_result_title = Label(self.rc_section1_frame, text="Calculation result", font=("babel 12 underline"), bg='#cacfcc', fg='black')
		label_result_title.grid(row=0,column=0, columnspan=3, pady=10)

		# Burst altitude row
		label_burst_altitude = Label(self.rc_section1_frame, text="Burst Altitude (m) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_burst_altitude.grid(row=1, column=0, sticky=W, pady=2)		
		label_show_burst_altitude = Label(self.rc_section1_frame, text=self.burst_altitude(), font=("babel", 12), bg='#cacfcc', fg='black')
		label_show_burst_altitude.grid(row=1, column=1, pady=2)
		button_copy_burst_altitude = Button(self.rc_section1_frame, text='Copy', font=("babel", 12), bg='#cacfcc', fg='black', command=self.copy_result_burst_altitude)
		button_copy_burst_altitude.grid(row=1, column=2, padx=10, ipadx=20)

		# Ascent velocity row
		label_ascent_velocity = Label(self.rc_section1_frame, text="Ascent Velocity (m/s) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_ascent_velocity.grid(row=2, column=0, sticky=W, pady=2)		
		label_show_ascent_velocity = Label(self.rc_section1_frame, text=self.ascent_velocity(), font=("babel", 12), bg='#cacfcc', fg='black')
		label_show_ascent_velocity.grid(row=2, column=1)
		button_copy_ascent_velocity = Button(self.rc_section1_frame, text='Copy', font=("babel", 12), bg='#cacfcc', fg='black', command=self.copy_result_ascent_velocity)
		button_copy_ascent_velocity.grid(row=2, column=2, padx=10, ipadx=20)

		# Descent velocity row
		label_descent_velocity = Label(self.rc_section1_frame, text="Descent Velocity (m/s) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_descent_velocity.grid(row=3, column=0, sticky=W, pady=2)		
		label_show_descent_velocity = Label(self.rc_section1_frame, text=self.descent_velocity() , font=("babel", 12), bg='#cacfcc', fg='black')
		label_show_descent_velocity.grid(row=3, column=1)
		button_copy_descent_velocity = Button(self.rc_section1_frame, text='Copy', font=("babel", 12), bg='#cacfcc', fg='black', command=self.copy_result_descent_velocity)
		button_copy_descent_velocity.grid(row=3, column=2, padx=10, ipadx=20)

		# Lift-off row
		label_lift_off = Label(self.rc_section1_frame, text="Neck-lift per balloon (kg) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_lift_off.grid(row=4, column=0, sticky=W, pady=2)		
		label_show_lift_off = Label(self.rc_section1_frame, text=self.calculate_neck_lift(), font=("babel", 12), bg='#cacfcc', fg='black')
		label_show_lift_off.grid(row=4, column=1)

	def copy_result_burst_altitude(self):
		burst_altitude = self.burst_altitude()	
		pyperclip.copy(burst_altitude)

	def copy_result_ascent_velocity(self):
		ascent_velocity = self.ascent_velocity()	
		pyperclip.copy(ascent_velocity)

	def copy_result_descent_velocity(self):
		descent_velocity = self.descent_velocity()	
		pyperclip.copy(descent_velocity)

	def open_cusf_sondehub_predictor(self):
		webbrowser.open_new("https://predict.sondehub.org/")

#-----------------------------------Section 2 Variable Parameter------------------------------------------#

	def create_variable_parameter(self): 
		# Title row
		label_variable_title = Label(self.rc_section2_frame, text="Variable Parameter", font=("babel 12 underline"), bg='#cacfcc', fg='black')
		label_variable_title.grid(row=0,column=0, columnspan=2, pady=10)		

		# Total Mass
		label_total_mass = Label(self.rc_section2_frame, text="Total Mass (kg) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_total_mass.grid(row=1, column=0, sticky=W)		
		total_mass_kg = self.calculate_total_mass()		
		self.label_show_total_mass = Label(self.rc_section2_frame, text=total_mass_kg[0], font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_total_mass.grid(row=1, column=1, ipadx=20)

		# Ground Balloon Diameter
		label_ground_diameter = Label(self.rc_section2_frame, text="Ground Diameter (m) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_ground_diameter.grid(row=2, column=0, sticky=W)
		ground_diameter = self.calculate_balloon_geometry()
		self.label_show_ground_diameter = Label(self.rc_section2_frame, text=ground_diameter[2], font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_ground_diameter.grid(row=2, column=1, ipadx=20)

		# Burst Balloon Diameter
		label_burst_diameter = Label(self.rc_section2_frame, text="Burst Diameter (m) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_burst_diameter.grid(row=3, column=0, sticky=W)		
		self.label_show_burst_diameter = Label(self.rc_section2_frame, text=self.burst_diameter(), font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_burst_diameter.grid(row=3, column=1, ipadx=20)

		# Air Density
		label_air_density = Label(self.rc_section2_frame, text="Air Density (kg/m\u00b3) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_air_density.grid(row=4, column=0, sticky=W)				
		self.label_show_air_density = Label(self.rc_section2_frame, text=self.calculate_air_density(), font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_air_density.grid(row=4, column=1, ipadx=10)
		


	
#-----------------------------------Section 2 Constant Parameter------------------------------------------#
		
	def create_constant_parameter(self):
		#Title row
		label_constant_title = Label(self.rc_section2_frame, text="Constant Parameter", font=("babel 12 underline"), bg='#cacfcc', fg='black')
		label_constant_title.grid(row=0, column=2, columnspan=4, pady=10)

		# Gravity
		label_gravity = Label(self.rc_section2_frame, text="Gravity (m/s\u00b2) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_gravity.grid(row=1, column=2, sticky=W)
		gravity = self.general_constant()
		self.label_show_gravity = Label(self.rc_section2_frame, text=round(gravity[0],3), font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_gravity.grid(row=1, column=3, ipadx=10)

		# Helium Density
		label_he_density = Label(self.rc_section2_frame, text="Density of Helium (kg/m\u00b3) :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_he_density.grid(row=2, column=2, sticky=W)
		he_density = self.gaz_density()
		self.label_show_he_density = Label(self.rc_section2_frame, text=he_density[0], font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_he_density.grid(row=2, column=3, ipadx=10)
	
		# Balloon Drag Coefficient
		label_balloon_drag_coeff = Label(self.rc_section2_frame, text="Balloon Drag Coefficient :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_balloon_drag_coeff.grid(row=3, column=2, sticky=W)
		balloon_dc = self.general_constant()
		self.label_show_balloon_drag_coeff = Label(self.rc_section2_frame, text=balloon_dc[1], font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_balloon_drag_coeff.grid(row=3, column=3, ipadx=20)

		# Parachute Drag Coefficient
		label_parachute_drag_coeff = Label(self.rc_section2_frame, text="Parachute Drag Coefficient :", font=("babel", 12), bg='#cacfcc', fg='black')
		label_parachute_drag_coeff.grid(row=4, column=2, sticky=W)
		parachute_dc = self.general_constant()
		self.label_show_parachute_drag_coeff = Label(self.rc_section2_frame, text=parachute_dc[2], font=("babel", 12), bg='#cacfcc', fg='black')
		self.label_show_parachute_drag_coeff.grid(row=4, column=3, ipadx=20)


	def create_button(self):
		open_website_button = Button(self.rc_section1_frame, text="Open CUSF : SondeHub Predictor", command=self.open_cusf_sondehub_predictor)
		open_website_button.grid(row=5, column=0, columnspan=3, ipady=10, pady=20)

		run_again_button = Button(self.rc_bottom_frame, text="Run again", font=("babel", 14), bg='#cacfcc', fg='black', command=self.run_again_flight_calculation_window)
		run_again_button.grid(row=0, column=0, padx=30 , ipadx=80, pady=20)

		close_button = Button(self.rc_bottom_frame, text="Close", font=("babel", 14), bg='#cacfcc', fg='black', command=self.close_calculation_window)
		close_button.grid(row=0, column=1, padx=30, ipadx=80, pady=20)
		#close_button.grid(row=5, column=0, columnspan=3, pady=20, ipadx=200)

	def run_again_flight_calculation_window(self):
		from flight_input import Flight_input
		self.rc_window.destroy()				
		start = Flight_input()
		start.main_window.mainloop()

	def close_calculation_window(self):
		self.rc_window.destroy()




if __name__ == "__main__":
	start = Flight_result()
	start.rc_window.mainloop()