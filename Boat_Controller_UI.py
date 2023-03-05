#Boat Controller User Interface for University Project that will fnd application in automation of a boat control via following API.
#This project was write by Filip Zdebel @ www.ACEEngineering.uk with use of examples from Github in customtkinter library.

import customtkinter
import time
import requests
import random

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

###List of variables:
ip_address = ""
html_code = ""

wait = 0
wait_str = ""

motor_1_speed = 200
motor_1_speed_string = "Motor 1 Speed: "
motor_2_speed = 200
motor_2_speed_string = "Motor 2 Speed: "
motor_1_2_speed = 200
motor_1_2_speed_string = "Motor 1 and 2 Speed: "

delay = 0
delay_ms = 0
delay_remaining = 0

gps_latitude = 0
gps_latitude_str = "Latitude: "
gps_longitude = 0
gps_longitude_str = "Longitude: "
gps_heading_str = "Heading: "
gps_heading = "180 deg"

command_str = "Command: "
current_command = ""

label = ""
command_list = []
command_forward = "Forward"
command_reverse = "Reverse"
command_stop = "Stop"
command_wait = "Wait"
command_turn_right = "Turn right"
command_turn_left = "Turn left"
command_motor_1_speed = "Motor 1 Speed"
command_motor_2_speed = "Motor 2 Speed"
command_motor_1_2_speed = "Motor 1&2 Speed"

# the following commands are defining the case number within the ESP8266 controller
send_command_forward = "2"
send_command_turn_left = "4"
send_command_stop = "5"
send_command_turn_right = "6"
send_command_reverse = "8"
send_command_motor_1_speed_100 = "10"
send_command_motor_1_speed_150 = "11"
send_command_motor_1_speed_200 = "12"
send_command_motor_1_speed_250 = "13"
send_command_motor_1_speed_300 = "14"
send_command_motor_2_speed_100 = "15"
send_command_motor_2_speed_150 = "16"
send_command_motor_2_speed_200 = "17"
send_command_motor_2_speed_250 = "18"
send_command_motor_2_speed_300 = "19"
send_command_motor_1_2_speed_100 = "20"
send_command_motor_1_2_speed_150 = "21"
send_command_motor_1_2_speed_200 = "22"
send_command_motor_1_2_speed_250 = "23"
send_command_motor_1_2_speed_300 = "24"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Boat Controller Python API for ESP8266 Boat Webserver")
        self.geometry(f"{1180}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create left sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=14, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Boat Controller", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.ip_address_label = customtkinter.CTkLabel(self.sidebar_frame, text="IP address:", anchor="w")
        self.ip_address_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.ip_address_entry = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Boat IP address")
        self.ip_address_entry.grid(row=3, column=0, padx=20, pady=10)
        self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Connect", fg_color= "grey", command=self.connect)
        self.connect_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
       
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["100%", "110%", "120%", "130%", "140%", "150%"],command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))


        # create tabview
        self.mode_tabview = customtkinter.CTkTabview(self, width = 660)
        self.mode_tabview.grid(row=0,  column=1, rowspan=14, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.mode_tabview.add("Automatic")
        self.mode_tabview.add("Manual")
        self.mode_tabview.add("Autonomous")
        self.mode_tabview.tab("Manual").grid_columnconfigure(3, weight=1)  # configure grid of individual tabs
        self.mode_tabview.tab("Automatic").grid_columnconfigure(4, weight=1) # configure grid of individual tabs
        self.mode_tabview.tab("Automatic").grid_rowconfigure(12, weight=1) # configure grid of individual tabs
        self.mode_tabview.tab("Autonomous").grid_columnconfigure(3, weight=1) # configure grid of individual tabs

        # tabview Automatic
        self.scrolable_frame = customtkinter.CTkScrollableFrame(self.mode_tabview.tab("Automatic"))
        self.scrolable_frame.grid(row=2, rowspan = 14, column=0, padx=20, pady=20, sticky = "nsw")
        self.automatic_label_1 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text="Automatic controll", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.automatic_label_1.grid(row=0, column=0, columnspan = 4, padx=10, pady=10, sticky = "we")
        self.run_program_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Run program", fg_color= "Green", command=self.run_program)
        self.run_program_button.grid(row=1, column=0, padx=10, pady=10)
        self.stop_program_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Stop program", fg_color= "Red", command=self.stop_program)
        self.stop_program_button.grid(row=1, column=3, padx=10, pady=10)

        self.automatic_label_2 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text="Add automatic commands", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.automatic_label_2.grid(row=2, column=1, columnspan = 3, padx=10, pady=10)

        # adding the command buttons
        self.automatic_button_forward = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Forward", command=self.automatic_command_forward)
        self.automatic_button_forward.grid(row=3, column=2, padx=10, pady=10)
        self.automatic_button_left = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Turn Left", command=self.automatic_command_left)
        self.automatic_button_left.grid(row=4, column=1, padx=10, pady=10)
        self.automatic_button_stop = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Stop", command=self.automatic_command_stop)
        self.automatic_button_stop.grid(row=4, column=2, padx=10, pady=10)
        self.automatic_button_right = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Turn Right", command=self.automatic_command_right)
        self.automatic_button_right.grid(row=4, column=3, padx=10, pady=10)
        self.automatic_button_reverse = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Reverse", command=self.automatic_command_reverse)
        self.automatic_button_reverse.grid(row=5, column=2, padx=10, pady=10)

        self.automatic_label_3 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text=("Motor 1 speed set to: " + str(motor_1_speed)))
        self.automatic_label_3.grid(row=6, column=2, columnspan = 2, padx=10, pady=0)
        self.automatic_button_motor_1_speed = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Motor 1 speed", command=self.automatic_command_motor_1_speed)
        self.automatic_button_motor_1_speed.grid(row=7, column=1, padx=10, pady=10)
        self.slider_1 = customtkinter.CTkSlider(self.mode_tabview.tab("Automatic"), from_=100, to=300, number_of_steps=4, command=self.slider_1_command)
        self.slider_1.grid(row=7, column=2, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="ew")
        
        self.automatic_label_4 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text=("Motor 2 speed set to: " + str(motor_2_speed)))
        self.automatic_label_4.grid(row=8, column=2, columnspan = 2, padx=10, pady=0)
        self.automatic_button_motor_2_speed = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Motor 2 speed", command=self.automatic_command_motor_2_speed)
        self.automatic_button_motor_2_speed.grid(row=9, column=1, padx=10, pady=10)
        self.slider_2 = customtkinter.CTkSlider(self.mode_tabview.tab("Automatic"), from_=100, to=300, number_of_steps=4, command=self.slider_2_command)
        self.slider_2.grid(row=9, column=2, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.automatic_label_5 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text=("Motor 1&2 speed set to: " + str(motor_1_2_speed)))
        self.automatic_label_5.grid(row=10, column=2, columnspan = 2, padx=10, pady=0)
        self.automatic_button_motor_1_2_speed = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Motor 1&2 speed", command=self.automatic_command_motor_1_2_speed)
        self.automatic_button_motor_1_2_speed.grid(row=11, column=1, padx=10, pady=10)
        self.slider_3 = customtkinter.CTkSlider(self.mode_tabview.tab("Automatic"), from_=100, to=300, number_of_steps=4, command=self.slider_3_command)
        self.slider_3.grid(row=11, column=2, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.automatic_wait_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Wait XXXX ms", command=self.automatic_command_wait)
        self.automatic_wait_button.grid(row=12, column=1, padx=10, pady=10)
        self.automatic_wait_entry = customtkinter.CTkEntry(self.mode_tabview.tab("Automatic"), placeholder_text="milliseconds")
        self.automatic_wait_entry.grid(row=12, column=2, padx=10, pady=10)

        self.newlist1 = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Clear commands", command=self.newlist)
        self.newlist1.grid(row=13, column=3, padx=10, pady=10)

        # tabview Manual
        self.manual_label_1 = customtkinter.CTkLabel(self.mode_tabview.tab("Manual"), text="Manual")
        self.manual_label_1.grid(row=0, column=0, padx=20, pady=20, sticky = "")

        # tabview Autonomous
        self.autonomous_label_1 = customtkinter.CTkLabel(self.mode_tabview.tab("Autonomous"), text="Autonomous")
        self.autonomous_label_1.grid(row=0, column=0, padx=20, pady=20, sticky = "ew")

        # create Right sidebar frame with widgets
        self.sidebar_2_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_2_frame.grid(row=0, column=2, rowspan=14, sticky="nsew")
        self.sidebar_2_frame.grid_rowconfigure(6, weight=1)

        self.label_outputs = customtkinter.CTkLabel(self.sidebar_2_frame, text = "Outputs:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_outputs.grid(row = 0, column = 0 , padx=(55,55), pady=10, sticky="")
        self.label_m1_speed_str = customtkinter.CTkLabel(self.sidebar_2_frame, text=motor_1_speed_string)
        self.label_m1_speed_str.grid(row=1, column=0, padx=10, pady=10, sticky="")
        self.label_m1_speed = customtkinter.CTkLabel(self.sidebar_2_frame, text=motor_1_speed)
        self.label_m1_speed.grid(row=2, column=0,padx=10, pady=10,sticky="")

        self.label_m2_speed_str = customtkinter.CTkLabel(self.sidebar_2_frame, text=motor_2_speed_string)
        self.label_m2_speed_str.grid(row=4,column=0, padx=10, pady=10, sticky="")
        self.label_m2_speed = customtkinter.CTkLabel(self.sidebar_2_frame, text=motor_2_speed)
        self.label_m2_speed.grid(row=5, column=0, padx=10, pady=10, sticky="")

        self.label_gps_latitude_str = customtkinter.CTkLabel(self.sidebar_2_frame, text=gps_latitude_str)
        self.label_gps_latitude_str.grid(row=7, column=0, padx=10, pady=10, sticky="")
        self.label_gps_latitude = customtkinter.CTkLabel(self.sidebar_2_frame, text=gps_latitude)
        self.label_gps_latitude.grid(row=8, column=0, padx=10, pady=10, sticky="")

        self.label_gps_heading_str = customtkinter.CTkLabel(self.sidebar_2_frame, text=gps_heading_str)
        self.label_gps_heading_str.grid(row=9, column=0, padx=10, pady=10, sticky="")
        self.label_gps_heading = customtkinter.CTkLabel(self.sidebar_2_frame, text=gps_heading)
        self.label_gps_heading.grid(row=10, column=0, padx=10, pady=10, sticky="")

        self.label_gps_longitude_str = customtkinter.CTkLabel(self.sidebar_2_frame, text=gps_longitude_str)
        self.label_gps_longitude_str.grid(row=11, column=0, padx=10, pady=10, sticky="")
        self.label_gps_longitude = customtkinter.CTkLabel(self.sidebar_2_frame, text=gps_longitude)
        self.label_gps_longitude.grid(row=12, column=0, padx=10, pady=10, sticky="")

        self.label_current_command_str = customtkinter.CTkLabel(self.sidebar_2_frame, text = (command_str + current_command))
        self.label_current_command_str.grid(row = 13, column = 0, padx=10, pady=10, sticky="nsew")
        self.label_delay_reianing = customtkinter.CTkLabel(self.sidebar_2_frame, text=("Command time left: " + str(delay_remaining)))
        self.label_delay_reianing.grid(row=14, column=0, padx=10, pady=10, sticky="")


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def connect(self):
        self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Connect", fg_color= "grey", command=self.connect)
        self.connect_button.grid(row=4, column=0, padx=20, pady=10)
        ip_address = "http://" + str(self.ip_address_entry.get())
        print(ip_address)
        r = requests.get(ip_address)
        print(r.status_code)
        time.sleep(1)
        try:
            response = requests.get(ip_address, timeout = (3, 5))
            print(response.status_code)
            self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Connected", fg_color= "green", command=self.connect)
            self.connect_button.grid(row=4, column=0, padx=20, pady=10)
            print("Server connected")
        except requests.exceptions.Timeout:
            print("The request timed out")
            self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Not Connect", fg_color= "red", command=self.connect)
            self.connect_button.grid(row=4, column=0, padx=20, pady=10)
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Not Connect", fg_color= "red", command=self.connect)
            self.connect_button.grid(row=4, column=0, padx=20, pady=10)
        return(ip_address)

    def run_program(self):
        #self.destroy()
        #self.__init__()
        ip_address = "http://" + str(self.ip_address_entry.get())
        urlend = "/boat?a="
        url = ip_address + urlend
        command = ""
        payload = {}
        headers = {}
        last_move_command = ""
        x = 0
        y = 0
        delay = 0
        speed = 0
        force_stop_program = 0
        global current_command
        global delay_ms
        global delay_remaining

        print("Program started")
        print("")
        print("Checking the list for key phrases...")

        print("")
        print("Executing commands...")
        number_commands = len(command_list)
        while x < number_commands:
            y = 0
            if force_stop_program == 1:
                x = number_commands
            elif command_list[x] == command_forward:
                current_command = command_forward
                last_move_command = send_command_forward
                print("Moving forward")
                command = send_command_forward
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
            elif command_list[x] == command_reverse:
                current_command = command_reverse
                last_move_command = send_command_reverse
                print("Reversing")
                command = send_command_reverse
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)

            elif command_list[x] == command_wait:
                delay = int(command_list[x+1])/1000
                delay_ms = int(command_list[x+1])
                print("Waiting", delay_ms , "milliseconds.")
                x = x + 1
                refresh_rate = delay*10
                while y < refresh_rate:
                    if force_stop_program == 1:
                        y = refresh_rate
                    time.sleep(0.1)
                    response = requests.request("POST", ip_address, headers=headers,data=payload)
                    html_code = response.text
                    y = y + 1
                    delay_remaining = delay_ms - (y * 100)
                    self.update_outputs(current_command, html_code, delay_remaining)
                delay_remaining = 0
            elif command_list[x] == command_motor_1_speed:
                #current_command = command_motor_1_speed
                speed = int(command_list[x+1])
                if speed == 100:
                    command = send_command_motor_1_speed_100
                elif speed == 150:
                    command = send_command_motor_1_speed_150
                elif speed == 200:
                    command = send_command_motor_1_speed_200
                elif speed == 250:
                    command = send_command_motor_1_speed_250
                elif speed == 300:
                    command = send_command_motor_1_speed_300
                print(command_motor_1_speed, speed )
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
                time.sleep(0.1)
                if last_move_command != "":
                    apicommand = str(url + last_move_command)
                    response = requests.request("POST", apicommand, headers=headers,data=payload)
                    print(apicommand)
                x = x + 1
            elif command_list[x] == command_motor_2_speed:
                #current_command = command_motor_2_speed
                speed = int(command_list[x+1])
                if speed == 100:
                    command = send_command_motor_2_speed_100
                elif speed == 150:
                    command = send_command_motor_2_speed_150
                elif speed == 200:
                    command = send_command_motor_2_speed_200
                elif speed == 250:
                    command = send_command_motor_2_speed_250
                elif speed == 300:
                    command = send_command_motor_2_speed_300
                print(command_motor_2_speed, speed )
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
                time.sleep(0.1)
                if last_move_command != "":
                    apicommand = str(url + last_move_command)
                    response = requests.request("POST", apicommand, headers=headers,data=payload)
                    print(apicommand)
                x = x + 1
            elif command_list[x] == command_motor_1_2_speed:
                #current_command = command_motor_1_2_speed
                speed = int(command_list[x+1])
                if speed == 100:
                    command = send_command_motor_1_2_speed_100
                elif speed == 150:
                    command = send_command_motor_1_2_speed_150
                elif speed == 200:
                    command = send_command_motor_1_2_speed_200
                elif speed == 250:
                    command = send_command_motor_1_2_speed_250
                elif speed == 300:
                    command = send_command_motor_1_2_speed_300
                print(command_motor_1_2_speed, speed )
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
                time.sleep(0.1)
                if last_move_command != "":
                    apicommand = str(url + last_move_command)
                    response = requests.request("POST", apicommand, headers=headers,data=payload)
                    print(apicommand)
                x = x + 1
            elif command_list[x] == command_turn_right:
                current_command = command_turn_right
                last_move_command = send_command_turn_right
                print("Turning right")
                command = send_command_turn_right
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
            elif command_list[x] == command_turn_left:
                current_command = command_turn_left
                last_move_command = send_command_turn_left
                print("Turning left")
                command = send_command_turn_left
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
            elif command_list[x] == command_stop:
                current_command = command_stop
                last_move_command = send_command_stop
                print("Stopping")
                command = send_command_stop
                apicommand = str(url + command)
                response = requests.request("POST", apicommand, headers=headers,data=payload)
                print(apicommand)
            else:
                print("Invalid command")
            
            html_code = response.text

            self.update_outputs(current_command, html_code, delay_remaining)
            x = x + 1

        if force_stop_program == 1:
            time.sleep(0.1)
            command = send_command_stop
            apicommand = str(url + command)
            response = requests.request("POST", apicommand, headers=headers,data=payload)
            print(apicommand)
        
        print("")
        print("end of commands")

    def stop_program(self):
        global force_stop_program
        force_stop_program = 1
        print("Program stopped")

    def automatic_command_forward(self):
        command_list.append(command_forward)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = command_forward)
        label.pack()
        print("Command forward added")
        print(command_list)

    def automatic_command_left(self):
        command_list.append(command_turn_left)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = command_turn_left)
        label.pack()
        print("Command turn left added")
        print(command_list)

    def automatic_command_stop(self):
        command_list.append(command_stop)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = command_stop)
        label.pack()
        print("Command stop added")
        print(command_list)

    def automatic_command_right(self):
        command_list.append(command_turn_right)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = command_turn_right)
        label.pack()
        print("Command turn right added")
        print(command_list)

    def automatic_command_reverse(self):
        command_list.append(command_reverse)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = command_reverse)
        label.pack()
        print("Command reverse added")
        print(command_list)

    def automatic_command_wait(self):
        wait = self.automatic_wait_entry.get()
        if wait == "":
            print("Enter time to wait in milliseconds")
        else:
            command_list.append(command_wait)
            command_list.append(wait)
            wait_str = command_wait + " " + str(wait) + " milliseconds"
            label = customtkinter.CTkLabel(self.scrolable_frame, text = wait_str)
            label.pack()
            print("Command wait added")
            print(command_list)



    def automatic_command_motor_1_speed(self):
        motor_1_speed = int(self.slider_1.get())
        command_list.append(command_motor_1_speed)
        command_list.append(motor_1_speed)
        motor_1_speed_string = command_motor_1_speed + " " + str(motor_1_speed)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = motor_1_speed_string)
        label.pack()
        print("Command motor 1 speed added")
        print(command_list)

    def automatic_command_motor_2_speed(self):
        motor_2_speed = int(self.slider_2.get())
        command_list.append(command_motor_2_speed)
        command_list.append(motor_2_speed)
        motor_2_speed_string = command_motor_2_speed + " " + str(motor_2_speed)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = motor_2_speed_string)
        label.pack()
        print("Command motor 2 speed added")
        print(command_list)

    def automatic_command_motor_1_2_speed(self):
        motor_1_2_speed = int(self.slider_3.get())
        command_list.append(command_motor_1_2_speed)
        command_list.append(motor_1_2_speed)
        motor_1_2_speed_string = command_motor_1_2_speed + " " + str(motor_1_2_speed)
        label = customtkinter.CTkLabel(self.scrolable_frame, text = motor_1_2_speed_string)
        label.pack()
        print("Command motor 1&2 speed added")
        print(command_list)

    def slider_1_command(self, value):
        print(value)
        motor_1_speed = int(self.slider_1.get())
        self.automatic_label_3.configure(text=("Motor 1 speed set to: " + str(motor_1_speed)))
        print("slider value changed to: " + str(motor_1_speed))

    def slider_2_command(self, value):
        print(value)
        motor_2_speed = int(self.slider_2.get())
        self.automatic_label_4.configure(text=("Motor 2 speed set to: " + str(motor_2_speed)))
        print("slider value changed to: " + str(motor_2_speed))

    def slider_3_command(self, value):
        print(value)
        motor_1_2_speed = int(self.slider_3.get())
        self.automatic_label_5.configure(text=("Motor 1&2 speed set to: " + str(motor_1_2_speed)))
        print("slider value changed to: " + str(motor_1_2_speed))


    def update_outputs(self, current_command, html_code, delay_remaining):
        print(command_str + current_command)
        print(html_code[132:135])
        print(html_code[154:157])
        motor_1_speed = int(html_code[132:135]) 
        motor_2_speed = int(html_code[154:157]) 
        self.label_m1_speed.configure(text=motor_1_speed)
        self.label_m2_speed.configure(text=motor_2_speed)
        self.label_delay_reianing.configure(text=("Command time left: " + str(delay_remaining)))
        self.label_current_command_str.configure(text = (command_str + current_command))
        
        gps_latitude = random.randint(0, 1000)
        gps_longitude = random.randint(0, 1000)
        gps_heading = str(random.randint(0, 360)) + " deg"
        self.label_gps_latitude.configure(text=gps_latitude)
        self.label_gps_heading.configure(text=gps_heading)
        self.label_gps_longitude.configure(text=gps_longitude)

        self.update()

    def newlist(self):
        self.scrolable_frame = customtkinter.CTkScrollableFrame(self.mode_tabview.tab("Automatic"))
        self.scrolable_frame.grid(row=2, rowspan = 14, column=0, padx=20, pady=20, sticky = "nsw")
        command_list.clear()
        print("Commands cleared")


if __name__ == "__main__":
    app = App()
    app.mainloop()