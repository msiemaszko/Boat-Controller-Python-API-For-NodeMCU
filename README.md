# Boat-Controller-Python-API-For-NodeMCU
![alt text](https://github.com/ACEengineering/Boat-Controller-Python-API-For-NodeMCU/blob/main/UI_screenshot_02.png?raw=true)
Figure 1. ANTT API that communicates with NodeMCU that is installed on a Tug Boat. ANTT Alows to build a command list that will be executed by a boat and will return values such as speed of the motors and GPS coordinates.

Project written in Python to send commands to  a NodeMCU microcontroller which will controll dual motor on the boat.
To be able to run this project you will need to install latest version of Python then install following libraries:
- customtkinter
- requests

In the future i will include the code from the NodeMCU that controls the boat.

Version control:
- Version 1 completed on 27 February 2023:
        Initial UI without Automatic functionality.
- Version 2 completed on 01 March 2023:
        Updated UI with added Output side bar. 
- Version 3 completed on 03 March 2023:
        Added autoatic functionality to control dual motors with set of commands.
- Version 4 completed on 08 March 2023:
        Added updating outputs coming from a webserver.
- Version 5 completed on 22 March 2023:
        Terms on the UI have been adjusted to the standarised approach of the project.
- Version 6 completed on 12 April 2023:
        Read and Write program functions have been added, this will allow user to export and import commands from and to the list.
- Version 7 completed on 19 April 2023:
        Spelling correction and extended description. Updated picture with a real GPS data.

API has been named ANTT - Automatic Navigation Tug Tool which has been developed to control a Tug boat for Solent Univeristy.
And this solution was tested in a water tank on Univertisty permises on 5th of April, final step and testing will be conducted at Timsbury Lake on 10th of May, where the Tug Boat will be controlled with ANTT and demonstarted to stake holders.

