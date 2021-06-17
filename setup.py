#    server-setup, generates configs and fetches tuinity jar
#    Copyright (C) 2021  hapeshiva                      Author
#    Copyright (C) 2021  Ethan Hemingway (LethalEthan)  Co-Author
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from os.path import exists
import time
try:
    import psutil
    import requests
    import shutil
    import sys
except Exception as e:
    print("Could not import one or more libraries, run the corresponding setup file to install dependencies!: ", e)
    exit()
try:
    import yaml
except Exception as e:
    print("Could not import yaml: ", e)
    noyaml = True

# Detect python version, only runs on 3+
if (sys.version_info > (3, 0)):
    print("Python 3 has been detected you may continue\n")
else:
    exit("Python 2 has been detected please run in Python3!")
# Set basic vars
version = "3.0.3"
server_jar = "undefined.jar"
server_path = "server/"
maxmem = float(psutil.virtual_memory().total / 1000000000) # Used for maxmem check, don't want users using more memory than they can handle on their system
# Forks and knives
tuinity_url = "https://ci.codemc.io/job/Spottedleaf/job/Tuinity/lastSuccessfulBuild/artifact/tuinity-paperclip.jar"
purpur_url = "https://purpur.pl3x.net/api/v1/purpur/1.16.5/latest/download"
paper_url = "https://papermc.io/api/v1/paper/1.16.5/latest/download" # Uses old API version since v2 rquires a bit more faffing which I'll get around to
airplane_url = "https://dl.airplane.gg/latest/Airplane-JDK11/launcher-airplane.jar"

print("hapeshiva server setup", version, "\n")
print("Co-authored by LethalEthan")
print("Warning for 1.17 java 16 will be required! get it at: https://adoptopenjdk.net/?variant=openjdk16&jvmVariant=hotspot\n")
print("Thanks to YouHaveTrouble for the optimisation guide we used https://github.com/YouHaveTrouble/minecraft-optimization")
# Initial user input
def InitialUserInput():
    global memory
    global optimise
    global server_path
    # Ask for customised configs
    while True:
        try:
            optimise = str(input("Do you want optimised server configs? (y, n) "))
        except ValueError:
            print("Please enter yes or no")
        else:
            if optimise.casefold().startswith("y") or optimise.casefold().startswith("n"):
                break
            else:
                print("Please enter yes or no")
    # Get Server path from user
    while True:
        try:
            server_path = str(input("What folder/directory would you like the server to be in? "))
        except ValueError:
            print("please enter the folder name")
        else:
            if exists(server_path):
                try:
                    rm = str(input("Warning server directory already exists!, remove current configs? (y, n) "))
                except ValueError:
                    print("Enter yes or no")
                else:
                    #Detect if dots are contained in path as path traversal may occur
                    if (server_path.__contains__(".")):
                        print("Warning dot found in directory, path traversal may occur")
                    # Don't use backslashes
                    if (server_path.__contains__("\\")):
                        print("Path cannot contain backslashes")
                    if not (server_path.__contains__("/")):
                        server_path = server_path + "/"
                    if rm.casefold().startswith("y"):
                        print("\nRemoving, you have 4 seconds to cancel!!\n")
                        time.sleep(4)
                        try:
                            if exists(server_path + "paper.yml"):
                                os.remove(server_path + "paper.yml")
                            if exists(server_path + "bukkit.yml"):
                                os.remove(server_path + "bukkit.yml")
                            if exists(server_path + "tuinity.yml"):
                                os.remove(server_path + "tuinity.yml")
                            if exists(server_path + "purpur.yml"):
                                os.remove(server_path + "purpur.yml")
                            if exists(server_path + "server.properties"):
                                os.remove(server_path + "server.properties")
                        except Exception as e:
                            print("One or more removal of config files failed: ", e)
                        else:
                            print("Removed existing configs")
                            print("Server path is: ", server_path)
                            break
                    elif rm.casefold().startswith("n"):
                        return
                    else:
                        print("Please enter yes or no")
            else:
                # Detect if dots are contained in path as path traversal may occur
                if (server_path.__contains__(".")):
                    print("Warning dot found in directory, path traversal may occur")
                    os.mkdir(server_path)
                # Don't use backslashes
                if (server_path.__contains__("\\")):
                    print("Path cannot contain backslashes")
                # Add slash
                if not (server_path.__contains__("/")):
                    #print("added slash")
                    server_path = server_path + "/"
                    print("Server path is: ", server_path)
                    try:
                        os.mkdir(server_path)
                    except Exception as e:
                        print("Error creating directory: ", e)
                        exit()
                    else:
                        print("Directory created")
                        break
                else:
                    print("Server path is: ", server_path)
                    try:
                        os.mkdir(server_path)
                    except Exception as e:
                        print("Error creating directory: ", e)
                        exit()
                    else:
                        print("Directory created")
                        break

def ServerPathValidate():
    global server_path
    # Detect if dots are contained in path as path traversal may occur
    if (server_path.__contains__(".")):
        print("Warning dot found in directory, path traversal may occur")
        os.mkdir(server_path)
    # Don't use backslashes
    if (server_path.__contains__("\\")):
        print("Path cannot contain backslashes")
    # Add slash
    if not (server_path.__contains__("/")):
        #print("added slash")
        server_path = server_path + "/"
        print("Server path is: ", server_path)
        try:
            os.mkdir(server_path)
        except Exception as e:
            print("Error creating directory: ", e)
            exit()
        else:
            print("Directory created")
    else:
        print("Server path is: ", server_path)
        try:
            os.mkdir(server_path)
        except Exception as e:
            print("Error creating directory: ", e)
            exit()
        else:
            print("Directory created")

def ForkSelect():
    # Fork Select
    global server_jar
    while True:
        try:
            print("""
            Select which fork you want, if you're unsure choose 1

            1. Tuinity
            2. Paper
            3. Airplane
            4. Purpur
            """)
            fork_select = int(input("Enter the number for the fork you would like: "))
        except ValueError:
            print("Enter a number from the list!")
        else:
            if fork_select > 0 and fork_select < 5:
                if fork_select == 1:
                    print("You've chosen Tuinity, How do you say it and what does it mean?")
                    server_jar = "tuinity-paperclip.jar"
                    Download(tuinity_url)
                    break
                if fork_select == 2:
                    print("You've chosen Paper, it's not called paperspigot")
                    server_jar = "paperclip-1.16.5.jar"
                    Download(paper_url)
                    break
                if fork_select == 3:
                    print("You've chosen Airplane, zoom")
                    server_jar = "launcher-airplane-jdk11.jar"
                    Download(airplane_url)
                    break
                if fork_select == 4:
                    print("You've chosen Purpur, flying squids?")
                    server_jar = "purpurclip-1.16.5.jar"
                    Download(purpur_url)
                    break
            else:
                print("Enter a number from the list!")

#Download Jar /
def Download(fork):
    # If server_jar is undefined exit, Something ain't right
    if server_jar == "undefined.jar":
        print("Something went wrong")
        time.sleep(8)
        exit()
    # Check if server_jar exists already
    if exists(server_jar):
        while True:
            try:
                rm = str(input("Server jar already downloaded, do you want to re-download (y) or use the current jar (n)? (y, n) "))
            except ValueError:
                print("Please enter yes or no")
            else:
                if rm.casefold().startswith("y"):
                    try:
                        os.remove(server_jar)
                        if exists(server_path + server_jar):
                            os.remove(server_path + server_jar)
                    except Exception as e:
                        print("Could not remove existing Jar!: ", e)
                        return
                    else:
                        print("Removed old Jar")
                        break
                elif rm.casefold().startswith("n"):
                    try:
                        print("moving current Jar to server directory")
                        os.remove(server_path + server_jar)
                        shutil.move(server_jar, server_path)
                    except Exception as e:
                        print("Could not move Jar: ", e)
                        return
                    else:
                        print("Moved Jar to server directory")
                        return
                else:
                    print("Please enter yes or no")
    print("Downloading Jar...")
    response = requests.get(fork)
    if response.ok:
        print("Download completed!")
        try:
            open(server_jar, "wb").write(response.content)
        except Exception as e:
            print("Could not save Jar: ", e)
        else:
            print("Saved Jar successfully!")
        if exists(server_path + server_jar):
            while True:
                try:
                    rm = str(input("Would you like to replace the existing Jar in server directory? (y, n) "))
                except ValueError:
                    print("Please enter yes or no")
                else:
                    if rm.casefold().startswith("y"):
                        try:
                            os.remove(server_path + server_jar)
                            shutil.move(server_jar, server_path)
                        except Exception as e:
                            print("Could not replace Jar: ", e)
                            break
                        else:
                            print("Replace Jar!")
                    elif rm.casefold().startswith("n"):
                        break
                    else:
                        print("Please Enter yes or no")
        else:
            try:
                shutil.move(server_jar, server_path)
            except Exception as e:
                print("Could not move server Jar: ", e)
            else:
                print("Moved server Jar into server directory")
    else:
        print("Something went wrong trying to download Jar!")
        exit()

#Create Start scripts
def CreateStartScripts():
    while True:
        try:
            memory = int(input("How much memory do you want to allocate in GB? "))
        except EOFError:
            memory = 4
            break
        except ValueError:
            print("Please enter a number")
        else:
            if memory > 0 and memory <= maxmem - 2:
                print("\nMemory value is within range of max available memory, continuing")
                break
            else:
                print("\nThe memory value you defined is higher than the available system memory detected! This will cause a crash!")
                override = str(input("f you believe this is an error you can override this message, do you want to override? (y, n) "))
                if override.casefold().startswith("y"):
                    print("Overrided")
                    break
    mem = str(memory)
    try:
        if exists("start.sh"):
            os.remove("start.sh")
        if exists("start.bat"):
            os.remove("start.bat")
        if exists(server_path + "start.sh"):
            os.remove(server_path + "start.sh")
        if exists(server_path + "start.bat"):
            os.remove(server_path + "start.bat")
    except Exception as e:
        print("Could not remove one or more start scripts: ", e)
    else:
        print("Removed existing start scripts")
    pre_arg = "java -Xms" + mem + "G -Xmx" + mem + "G"
    post_arg = " -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar " + server_jar + " nogui"
    try:
        sh = open("start.sh", "w")
        bat = open("start.bat", "w")
    except Exception as e:
        print("Could not open start scripts: ", e)
        return
    else:
        print("Created start scripts, writing...")
    # Create Shell script
    try:
        sh.write(pre_arg + post_arg)
        sh.close()
    except Exception as e:
        print("Could not write start.sh: ", e)
    else:
        print("Written start.sh")
    # Create Batch script
    try:
        bat.write(pre_arg + post_arg)
        bat.close()
    except Exception as e:
        print("Could not write start.bat: ", e)
    else:
        print("Written start.bat")
    # Move Shell script
    try:
        shutil.move("start.sh", server_path)
    except Exception as e:
        print("Could not move start.sh to server_path: ", e)
    # Move Batch script
    try:
        shutil.move("start.bat", server_path)
    except Exception as e:
        print("Could not move start.bat to server_path: ", e)

# View distance And Server Port
def SetViewDistanceAndPort():
    global view_distance
    global no_tick_dist
    global total_distance
    # Remove existing server.props in current dir
    if exists("server.properties"):
        try:
            os.remove("server.properties")
        except Exception as e:
            print("Could not remove server.properties: ", e)
            return
    # Check for server.props in server_path
    if exists(server_path + "server.properties"):
        rm = input("Current server.properties found, would you like to remove it so the view distance and port can be set? (y, n) ")
        if rm.casefold().startswith("y"):
            try:
                os.remove(server_path + "server.properties")
            except Exception as e:
                print("Could not remove server.properties: ", e)
                return
        else:
            return
    else:
        try:
            config = open(server_path + "server.properties", "a")
        except Exception as e:
            print("Could not create server.properties in server_path: ", e)
            return
        # View Distance
        while True:
            try:
                view_distance = int(input("\nInput your view_distance in chunks excluding no-tick (reccomended: 4): "))
            # Incorrect input e.g.nfi437y
            except ValueError:
                print("Please enter a number")
            # On correct input with validation
            else:
                if view_distance <= 32 and view_distance >= 3:
                    config.write("view-distance=" + str(view_distance) + "\n")
                    print("View Distance set Succesfully")
                    if view_distance == 32:
                        print("You have set the maximum view distance available so no-tick cannot be set!")
                    break
                else:
                    print("View distance must be between 3 - 32")
        # No Tick distance
        if view_distance != 32:
            while True:
                try:
                    no_tick_dist = int(input("Input your desired no-tick view distance: (max: " + str(32 - view_distance) + "), (-1 to disable) "))
                except ValueError:
                    print("Enter an integer below: " + str(32 - view_distance))
                else:
                    total_distance = view_distance + no_tick_dist
                    if total_distance > 32:
                        print("view distance + no tick should be less than 32!")
                    if no_tick_dist == -1:
                        print("No-tick disabled")
                        break
                    if no_tick_dist <= 0:
                        print("No-tick disabled")
                        no_tick_dist = -1
                        break
                    if total_distance < 32 and total_distance > 0:
                        print("No-tick view distance set successfully")
                        break
        # Server port
        while True:
            try:
                server_port = int(input("\nInput your server_port (from 1000 to 99999, default 25565): "))
            # Incorrect Input e.g. Ajibijbewia
            except ValueError:
                print("Please enter a valid port")
            # On correct input and validation
            else:
                if server_port > 1000 and server_port < 99999:
                    try:
                        config.write("server-port=" + str(server_port) + "\n")
                    except Exception as e:
                        print("Could not set server-port: ", e)
                        break
                    else:
                        print("Server port set successfully")
                        break
                else:
                    print("Server port must be 1000 - 99999")
        try:
            config.close()
        except Exception as e:
            print("Could not close server.properties: ", e)
        else:
            print("saved and move successfully")

def SpigotConfig():
    with open("spigot.yaml", 'w+') as config:
        try:
            yamyam = yaml.safe_load(config)
        except yaml.YAMLError as e:
            print(e)
        #config[''] = view_distance - 1

def PaperConfig():
    with open("paper.yaml", 'w+') as config:
        try:
            yamyam = yaml.safe_load(config)
        except yaml.YAMLError as e:
            print(e)
        #config[''] = view_distance - 1
# Copy optimised configs and create startup scripts /
def CopyConfig():
    # Copy optimised configs
    global optimise
    counter = 0
    if optimise.casefold().startswith("y"):
        print("\nMoving optimised server configs")
        # Bukkit
        if exists("bukkit.yml"):
            try:
                shutil.copy("bukkit.yml", server_path)
            except Exception as e:
                print("Could not copy bukkit.yml: ", e)
                counter = counter + 1
            else:
                print("Copied bukkit.yml")
        # Spigot
        if exists("spigot.yml"):
            try:
                shutil.copy("spigot.yml", server_path)
            except Exception as e:
                print("Could not copy spigot.yml: ", e)
                counter = counter + 1
            else:
                print("Copied spigot.yml")
        # Paper
        if exists("paper.yml"):
            try:
                shutil.copy("paper.yml", server_path)
            except Exception as e:
                print("Could not copy paper.yml: ", e)
                counter = counter + 1
            else:
                print("Copied paper.yml")
        # Tuinity
        if exists("tuinity.yml"):
            try:
                shutil.copy("tuinity.yml", server_path)
            except Exception as e:
                print("Could not copy tuinity.yml: ", e)
                counter = counter + 1
            else:
                print("Copied tuinity.yml")
    if counter > 0:
        print("One or more configs could not be copied :( total: ", counter )
    print("\nServer is ready! Use start.bat (Windows) or start.sh (Linux). Go to server directory and test! Thanks for using hapeshiva server setup")
# End
def End():
    print("Setup is complete")
    while True:
        try:
            rm = str(input("Would you like to keep the temporary files that are outside the server directory? (y, n)"))
        except ValueError:
            print("Please enter yes or no")
        else:
            if rm.casefold().startswith("n"):
                print("\nRemoving original yml files and removing the jar outside of server")
                try:
                    if exists("bukkit.yml"):
                        os.remove("bukkit.yml")
                    if exists("spigot.yml"):
                        os.remove("spigot.yml")
                    if exists("paper.yml"):
                        os.remove("paper.yml")
                    if exists("tuinity.yml"):
                        os.remove("tuinity.yml")
                    if exists("server.properties"):
                        os.remove("server.properties")
                except Exception as e:
                    print("Could not delete one or more configs: ", e)
                else:
                    print("\nCleaned up!")
                    break
            elif rm.casefold().startswith("y"):
                print("Keeping temp files")
                break
            else:
                print("Please enter yes or no")
    end = input("\nPress any key to close...")
    if end != "dontclose":
        exit()
    else:
        while True:
            pass

InitialUserInput()
ForkSelect()
CreateStartScripts()
SetViewDistanceAndPort()
#SpigotConfig()
CopyConfig()
End()
