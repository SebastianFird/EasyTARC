# EasyTARC
EasyTARC is a local Windows application for keeping track of the time spent on individual projects, meetings, etc. during your working hours.
EasyTARC - Easy time accounts recording control - This is my first opensource project. With the help of this project I want to improve my knowledge of the programming language Python and the framework Tkinter, as well as familiarize myself with the development of desktop applications. 


Installation instructions:

To get a first impression of EasyTARC, download the latest release and put the files into your preferred directory. Then go to the folder Version_X_X_EXE and execute the file EasyTARC.exe. Next a License_request.txt file will appear, then run the User_License_Creator.exe file and your personal license file will be in the directory. Now you can run the EasyTARC.exe again and test the program.


License:

The license is only for knowing the circle of users in your team or company. If only you want to use the program for yourself, a license is not really necessary. Therefore you can simply issue the license yourself with the file User_License_Creator.exe.


Encryption:

The user data is stored in an encrypted database called EasyTARC_Database_User_crypted.sql.gz. The encryption is made from a combination of the user name and a password.


You like EasyTARC and want to use it in your team or company? 
Then these are your next steps:

The executable files in the folder Version_X_X_EXE are great for a first impression, but there are still dummy passwords in the source code. To really use EasyTARC with specific passwords in your team or company, you have to define the passwords in the source code (file easytarc_pw_container.py) and then create your own EasyTARC.exe and User_License_Creator.exe. To create these files you need Python and the extension pyinstaller. Then you can use the Windows PowerShell with the command "pyinstaller -F -w -i "Logo.ico" EasyTARC.py" and the command "pyinstaller -F -w User_License_Creator.py" to create your own executables with your passwords.




Release 1.6.1:

![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/4d784647-f3c9-42f1-ae5f-cb8ce09b637b)
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/0a5af677-9daf-4de4-93fc-edb450ee3381)
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/a703e96c-c411-4d5c-bfda-5afd70afe6c8)


History:

![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/e183dc77-8c0c-4cb7-aa41-86dfda06af7d)
![grafik](https://github.com/SebastianFird/EasyTARC/assets/137194398/ef3b7424-f783-4292-916b-4e76de729557)










