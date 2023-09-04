# EasyTARC
EasyTARC is a local Windows application for keeping track of the time spent on individual projects, meetings, etc. during your working hours.

EasyTARC - Easy time accounts recording control - This is my first opensource project. With the help of this project I want to improve my knowledge of the programming language Python and the framework Tkinter, as well as familiarize myself with the development of desktop applications. 

____________________________________________________________________
Release 1.6.1:

Main-Window:
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/f3e8fee1-83e5-4ea1-a1be-21708ee151d8)
While working, the work window function is useful to keep track of time and still be able to work with concentration, you can choose between two work windows and also switch at any time.
Here you can see the bar window:
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/cd03b556-370d-4089-9c80-6175bb95a2b6)
And here is the second work window, the mini window:
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/9bc97586-4b5d-44ae-b9c6-1e38269023af)


____________________________________________________________________
Installation instructions:

To get a first impression of EasyTARC, download the latest release and put the files into your preferred directory. Then go to the folder Version_X_X_EXE and execute the file EasyTARC.exe. Next a License_request.txt file will appear, then run the User_License_Creator.exe file and your personal license file will be in the directory. Now you can run the EasyTARC.exe again and test the program.


License:

The license is only for knowing the circle of users in your team or company. If only you want to use the program for yourself, a license is not really necessary. Therefore you can simply issue the license yourself with the file User_License_Creator.exe.


Encryption:

The user data is stored in an encrypted database called EasyTARC_Database_User_crypted.sql.gz. The encryption is made from a combination of the user name and a password.


You like EasyTARC and want to use it in your team or company? 
Then these are your next steps:

The executable files in the folder Version_X_X_EXE are great for a first impression, but there are still dummy passwords in the source code. To really use EasyTARC with specific passwords in your team or company, you have to define the passwords in the source code (file easytarc_pw_container.py) and then create your own EasyTARC.exe and User_License_Creator.exe. To create these files you need Python and the extension pyinstaller. Then you can use the Windows PowerShell with the command "pyinstaller -F -w -i "Logo.ico" EasyTARC.py" and the command "pyinstaller -F -w User_License_Creator.py" to create your own executables with your passwords.
For further information please contact me.

____________________________________________________________________
A short excursion into the development:


![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/e183dc77-8c0c-4cb7-aa41-86dfda06af7d)
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/b2133689-ee91-4670-9454-dfa6e6b293f5)

The development of the app took place for the most part not in this repository, but in a non-public repository. 








