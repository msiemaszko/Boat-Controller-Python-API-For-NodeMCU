#Boat Controller User Interface for University Project that will fnd application in automation of a boat control via following API.
#This project was write by Filip Zdebel @ www.ACEEngineering.uk with use of examples from Github in customtkinter library.
#Code Version: Version 7 of the API
#Version Date: 19 April 2023

import customtkinter
import time
import requests
import json

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

###List of variables:
ip_address = ""
html_code = ""
connected = 0

wait = 0
wait_str = ""


display_motor_1_speed = "0"
display_motor_2_speed = "0"
motor_1_speed = 3
motor_1_speed_string = "Motor 1 Speed: "
motor_2_speed = 3
motor_2_speed_string = "Motor 2 Speed: "
motor_1_2_speed = 3
motor_1_2_speed_string = "Motor 1 and 2 Speed: "

delay = 0
delay_ms = 0
delay_remaining = 0

gps_latitude = "0.00000"
gps_latitude_str = "Latitude: "
gps_longitude = "0.00000"
gps_longitude_str = "Longitude: "
gps_heading_str = "Course Over Ground: "
gps_heading = "0 deg"

command_str = "Command: "
current_command = ""

out_data = ""
label = ""
command_list = []
command_forward = "Ahead"
command_reverse = "Astern"
command_stop = "Stop"
command_wait = "Run Time"
command_turn_right = "Starboard"
command_turn_left = "Port"
command_motor_1_speed = "Motor 1 Speed"
command_motor_2_speed = "Motor 2 Speed"
command_motor_1_2_speed = "Motor 1&2 Speed"

# the following commands are defining the case number within the ESP8266 controller
send_command_forward = "2"
send_command_turn_left = "4"
send_command_stop = "5"
send_command_turn_right = "6"
send_command_reverse = "8"
send_command_motor_1_speed_1 = "10"
send_command_motor_1_speed_2 = "11"
send_command_motor_1_speed_3 = "12"
send_command_motor_1_speed_4 = "13"
send_command_motor_1_speed_5 = "14"
send_command_motor_2_speed_1 = "15"
send_command_motor_2_speed_2 = "16"
send_command_motor_2_speed_3 = "17"
send_command_motor_2_speed_4 = "18"
send_command_motor_2_speed_5 = "19"
send_command_motor_1_2_speed_1 = "20"
send_command_motor_1_2_speed_2 = "21"
send_command_motor_1_2_speed_3 = "22"
send_command_motor_1_2_speed_4 = "23"
send_command_motor_1_2_speed_5 = "24"

send_command_request_motor_1_speed = "28"
send_command_request_motor_2_speed = "29"

send_command_request_latitude = "30"
send_command_request_longditude = "31"
send_command_request_speed = "32"
send_command_request_curse = "33"
send_command_request_no_of_satelites = "34"
send_command_request_gps_date = "35"
send_command_request_gps_time = "36"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Automatic Navigation Tug Tool")
        self.geometry(f"{1180}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3, 4), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create left sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=14, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Interface:", font=customtkinter.CTkFont(size=20, weight="bold"))
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
        self.automatic_label_1 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text="Automatic Navigation", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.automatic_label_1.grid(row=0, column=0, columnspan = 4, padx=10, pady=10, sticky = "we")
        self.run_program_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Run program", fg_color= "Green", command=self.run_program)
        self.run_program_button.grid(row=1, column=0, padx=10, pady=10)
        self.stop_program_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Stop program", fg_color= "Red", command=self.stop_program)
        self.stop_program_button.grid(row=1, column=1, padx=10, pady=10)
        self.read_program_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Read program", fg_color= "Orange", command=self.read_program)
        self.read_program_button.grid(row=1, column=2, padx=10, pady=10)
        self.write_program_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Write program", fg_color= "Orange", command=self.write_program)
        self.write_program_button.grid(row=1, column=3, padx=10, pady=10)

        self.automatic_label_2 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text="Add automatic commands", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.automatic_label_2.grid(row=2, column=1, columnspan = 3, padx=10, pady=10)

        # adding the command buttons
        self.automatic_button_forward = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Ahead", command=self.automatic_command_forward)
        self.automatic_button_forward.grid(row=3, column=2, padx=10, pady=10)
        self.automatic_button_left = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Port", command=self.automatic_command_left)
        self.automatic_button_left.grid(row=4, column=1, padx=10, pady=10)
        self.automatic_button_stop = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Stop", command=self.automatic_command_stop)
        self.automatic_button_stop.grid(row=4, column=2, padx=10, pady=10)
        self.automatic_button_right = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Starboard", command=self.automatic_command_right)
        self.automatic_button_right.grid(row=4, column=3, padx=10, pady=10)
        self.automatic_button_reverse = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Astern", command=self.automatic_command_reverse)
        self.automatic_button_reverse.grid(row=5, column=2, padx=10, pady=10)

        self.automatic_label_3 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text=("Motor 1 speed set to: " + str(motor_1_speed)))
        self.automatic_label_3.grid(row=6, column=2, columnspan = 2, padx=10, pady=0)
        self.automatic_button_motor_1_speed = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Motor 1 speed", command=self.automatic_command_motor_1_speed)
        self.automatic_button_motor_1_speed.grid(row=7, column=1, padx=10, pady=10)
        self.slider_1 = customtkinter.CTkSlider(self.mode_tabview.tab("Automatic"), from_=1, to=5, number_of_steps=4, command=self.slider_1_command)
        self.slider_1.grid(row=7, column=2, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.automatic_label_4 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text=("Motor 2 speed set to: " + str(motor_2_speed)))
        self.automatic_label_4.grid(row=8, column=2, columnspan = 2, padx=10, pady=0)
        self.automatic_button_motor_2_speed = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Motor 2 speed", command=self.automatic_command_motor_2_speed)
        self.automatic_button_motor_2_speed.grid(row=9, column=1, padx=10, pady=10)
        self.slider_2 = customtkinter.CTkSlider(self.mode_tabview.tab("Automatic"), from_=1, to=5, number_of_steps=4, command=self.slider_2_command)
        self.slider_2.grid(row=9, column=2, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.automatic_label_5 = customtkinter.CTkLabel(self.mode_tabview.tab("Automatic"), text=("Motor 1&2 speed set to: " + str(motor_1_2_speed)))
        self.automatic_label_5.grid(row=10, column=2, columnspan = 2, padx=10, pady=0)
        self.automatic_button_motor_1_2_speed = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Motor 1&2 speed", command=self.automatic_command_motor_1_2_speed)
        self.automatic_button_motor_1_2_speed.grid(row=11, column=1, padx=10, pady=10)
        self.slider_3 = customtkinter.CTkSlider(self.mode_tabview.tab("Automatic"), from_=1, to=5, number_of_steps=4, command=self.slider_3_command)
        self.slider_3.grid(row=11, column=2, columnspan = 2, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.automatic_wait_button = customtkinter.CTkButton(self.mode_tabview.tab("Automatic"), text="Run Time (ms)", command=self.automatic_command_wait)
        self.automatic_wait_button.grid(row=12, column=1, padx=10, pady=10)
        self.automatic_wait_entry = customtkinter.CTkEntry(self.mode_tabview.tab("Automatic"), placeholder_text="Run Time (ms)")
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
        self.label_m1_speed = customtkinter.CTkLabel(self.sidebar_2_frame, text=display_motor_1_speed)
        self.label_m1_speed.grid(row=2, column=0,padx=10, pady=10,sticky="")

        self.label_m2_speed_str = customtkinter.CTkLabel(self.sidebar_2_frame, text=motor_2_speed_string)
        self.label_m2_speed_str.grid(row=4,column=0, padx=10, pady=10, sticky="")
        self.label_m2_speed = customtkinter.CTkLabel(self.sidebar_2_frame, text=display_motor_2_speed)
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

        if connected == 1:
            self.update_outputs(current_command, html_code, delay_remaining)


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
            connected = 1
        except requests.exceptions.Timeout:
            print("The request timed out")
            self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Not Connect", fg_color= "red", command=self.connect)
            self.connect_button.grid(row=4, column=0, padx=20, pady=10)
            connected = 0
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
            self.connect_button = customtkinter.CTkButton(self.sidebar_frame, text="Not Connect", fg_color= "red", command=self.connect)
            self.connect_button.grid(row=4, column=0, padx=20, pady=10)
            connected = 0
        return(ip_address)

    def run_program(self):
        ip_address = "http://" + str(self.ip_address_entry.get())
        urlend = "/command?a="
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
        while x < number_commands and force_stop_program != 1:
            y = 0
            if command_list[x] == command_forward:
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
                refresh_rate = delay * 2
                while y < refresh_rate and force_stop_program != 1:
                    time.sleep(0.1)
                    y = y + 1
                    delay_remaining = delay_ms - (y * 500)
                    print("running time left: ",  delay_remaining)
                    print("stop program = ", force_stop_program)
                    if delay_remaining != 0:
                        self.update_outputs(current_command, html_code, delay_remaining)
                delay_remaining = 0
            elif command_list[x] == command_motor_1_speed:
                #current_command = command_motor_1_speed
                speed = int(command_list[x+1])
                if speed == 1:
                    command = send_command_motor_1_speed_1
                elif speed == 2:
                    command = send_command_motor_1_speed_2
                elif speed == 3:
                    command = send_command_motor_1_speed_3
                elif speed == 4:
                    command = send_command_motor_1_speed_4
                elif speed == 5:
                    command = send_command_motor_1_speed_5
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
                if speed == 1:
                    command = send_command_motor_2_speed_1
                elif speed == 2:
                    command = send_command_motor_2_speed_2
                elif speed == 3:
                    command = send_command_motor_2_speed_3
                elif speed == 4:
                    command = send_command_motor_2_speed_4
                elif speed == 5:
                    command = send_command_motor_2_speed_5
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
                if speed == 1:
                    command = send_command_motor_1_2_speed_1
                elif speed == 2:
                    command = send_command_motor_1_2_speed_2
                elif speed == 3:
                    command = send_command_motor_1_2_speed_3
                elif speed == 4:
                    command = send_command_motor_1_2_speed_4
                elif speed == 5:
                    command = send_command_motor_1_2_speed_5
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

            print("stop program = ", force_stop_program)
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

    def read_program(self):
        global command_list
        read_list = []
        read_command = open('commands.txt', 'r')
        # reading the file
        data = read_command.read()
        read_list = data.replace('\n', '').split(",")
        print(command_list)
        print(read_list)
        for a in read_list:
            command_list.append(a)
        print(command_list)
        print("This programm will execute a list of command that came from text file.")
        print("the list of commands is a follows: ", command_list)
        read_command.close()

        delay = 0
        speed = 0
        x = 0

        number_commands = len(read_list)
        if number_commands > 0:
            while x < number_commands:
                if read_list[x] == command_forward:
                    out_data = str(read_list[x] + "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                elif read_list[x] == command_reverse:
                    out_data = str(read_list[x] + "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                elif read_list[x] == command_wait:
                    out_data = str(read_list[x] + " " + str(read_list[x+1]) + " (ms)" + "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                    x = x + 1
                elif read_list[x] == command_motor_1_speed:
                    out_data = str(read_list[x] + " " + str(read_list[x+1]) + "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                    x = x + 1
                elif read_list[x] == command_motor_2_speed:
                    out_data = str(read_list[x] + " " + str(read_list[x+1]) + "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                    x = x + 1
                elif read_list[x] == command_motor_1_2_speed:
                    out_data = str(read_list[x] + " " + str(read_list[x+1]) + "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                    x = x + 1
                elif read_list[x] == command_turn_right:
                    out_data = str(read_list[x] +  "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                elif read_list[x] == command_turn_left:
                    out_data = str(read_list[x] +  "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                elif read_list[x] == command_stop:
                    out_data = str(read_list[x] +  "\n")
                    label = customtkinter.CTkLabel(self.scrolable_frame, text = out_data)
                    label.pack()
                x = x + 1
        else:
            print("File has no commands.")
        print("")
        print("end of commands")


    def write_program(self):
        write_command = open('commands.txt', 'w')
        delay = 0
        speed = 0
        x = 0

        number_commands = len(command_list)
        while x < number_commands:
            if command_list[x] == command_forward:
                print("Moving forward")
                out_data = str(command_list[x] + "," + "\n")
                write_command.write(out_data)
            elif command_list[x] == command_reverse:
                print("Reversing")
                out_data = str(command_list[x] + "," + "\n")
                write_command.write(out_data)
            elif command_list[x] == command_wait:
                delay = int(command_list[x+1])
                print("Waiting", delay , "seconds.")
                out_data = str(command_list[x] + "," + str(command_list[x+1])+ "," + "\n")
                write_command.write(out_data)
                x = x + 1
            elif command_list[x] == command_motor_1_speed:
                speed = int(command_list[x+1])
                print("Speed set to:", speed )
                out_data = str(command_list[x] + "," + str(command_list[x+1])+ "," + "\n")
                write_command.write(out_data)
                x = x + 1
            elif command_list[x] == command_motor_2_speed:
                speed = int(command_list[x+1])
                print("Speed set to:", speed )
                out_data = str(command_list[x] + "," + str(command_list[x+1])+ "," + "\n")
                write_command.write(out_data)
                x = x + 1
            elif command_list[x] == command_motor_1_2_speed:
                speed = int(command_list[x+1])
                print("Speed set to:", speed )
                out_data = str(command_list[x] + "," + str(command_list[x+1])+ "," + "\n")
                write_command.write(out_data)
                x = x + 1
            elif command_list[x] == command_turn_right:
                print("Turning right")
                out_data = str(command_list[x] + "," + "\n")
                write_command.write(out_data)
            elif command_list[x] == command_turn_left:
                print("Turning left")
                out_data = str(command_list[x] + "," + "\n")
                write_command.write(out_data)
            elif command_list[x] == command_stop:
                if x+1 <= number_commands:
                    print("Stopping")
                    out_data = str(command_list[x] + "," + "\n")
                    write_command.write(out_data)
                else:
                    out_data = str(command_list[x] + "\n")
                    write_command.write(out_data)
            x = x + 1
        print("")
        print("end of commands")
        write_command.close()

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
            wait_str = command_wait + " " + str(wait) + " (ms)"
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
        ip_address = "http://" + str(self.ip_address_entry.get())
        urlend = "/command?a="
        url = ip_address + urlend
        command = ""
        payload = {}
        headers = {}

        #request motor 1 speed
        command = send_command_request_motor_1_speed
        apicommand = str(url + str(command))
        response = requests.request("POST", apicommand, headers=headers,data=payload)
        print(apicommand)
        print(response.text)
        display_motor_1_speed = response.text

        #request motor 2 speed
        command = send_command_request_motor_2_speed
        apicommand = str(url + str(command))
        response = requests.request("POST", apicommand, headers=headers,data=payload)
        print(apicommand)
        print(response.text)
        display_motor_2_speed = response.text

        #request latitude
        command = send_command_request_latitude
        apicommand = str(url + str(command))
        response = requests.request("POST", apicommand, headers=headers,data=payload)
        print(apicommand)
        print(response.text)
        gps_latitude = response.text

        #request longtitude
        command = send_command_request_longditude
        apicommand = str(url + str(command))
        response = requests.request("POST", apicommand, headers=headers,data=payload)
        print(apicommand)
        print(response.text)
        gps_longitude = response.text

        #request course
        command = send_command_request_curse
        apicommand = str(url + str(command))
        response = requests.request("POST", apicommand, headers=headers,data=payload)
        print(apicommand)
        print(response.text)
        gps_heading = response.text + " deg"

        self.label_m1_speed.configure(text=display_motor_1_speed)
        self.label_m2_speed.configure(text=display_motor_2_speed)
        self.label_delay_reianing.configure(text=("Command time left: " + str(delay_remaining)))
        self.label_current_command_str.configure(text = (command_str + current_command))
        self.label_gps_latitude.configure(text=gps_latitude)
        self.label_gps_heading.configure(text=gps_heading)
        self.label_gps_longitude.configure(text=gps_longitude)
        self.stop_program_button .configure(command=self.stop_program)

        self.update()

    def newlist(self):
        self.scrolable_frame = customtkinter.CTkScrollableFrame(self.mode_tabview.tab("Automatic"))
        self.scrolable_frame.grid(row=2, rowspan = 14, column=0, padx=20, pady=20, sticky = "nsw")
        command_list.clear()
        print("Commands cleared")


if __name__ == "__main__":
    app = App()
    app.mainloop()