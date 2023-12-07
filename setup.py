import os,time


print("Welcome.")

script = "skulker.py"  #Script name
name = "Skulker" # Name
upxdir = 'C:/Users/Sam/Desktop/proj/_Dependencies/upx-4.1.0-win64' #UPX directory (supply your own)
iconfile = 'CustomTkinter_icon_Windows.ico' #Replaced icon
l = f"dist\\{name}\\_internal\\customtkinter\\assets\\icons\\CustomTkinter_icon_Windows.ico" #old icon path


main_command = f'pyinstaller --noconfirm --onedir --windowed --icon "{iconfile}" --name "{name}" --clean --upx-dir "{upxdir}"  "{script}"'
iconcopy = f"xcopy {iconfile} {l} /Y"
lice = f"xcopy LICENSE dist\\{name} /Y"
theme1 = f"xcopy theme10.json dist\\{name} /Y"
theme2 = f"xcopy theme11.json dist\\{name} /Y"
imagine = f"xcopy Imagine_1.3.1_Unicode dist\\{name} /Y /E"
compiler_command = ' "C:\\Program Files (x86)\\Inno Setup 6\\iscc.exe" ' + f"/O'{name}_setup' setup.iss"

commands = [main_command,iconcopy,lice,theme1 , theme2 , imagine ,compiler_command]
OLD_TIME = time.time()
for command in commands:
    os.system(command)
    # print(f'\nCommand "{command}" completed successfully.\n')
    

NEW_TIME = time.time() - OLD_TIME
print(f"Compiled successfully.\nTime: {str(NEW_TIME)}")

# os.system(compiler_command)