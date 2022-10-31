#!/usr/bin/python
# KDE Klipper Script to beautify information (Highlighting and sanitizing)
# Original code by ASJ (https://repo01.osl.basefarm.net/asj/KDETools/)
# Edited by Mikabend to work on i3wm with the use of xsel*
# Modified by saaknes to work with python 3, Windows, PowerShell and to maintain column output(multiple whitespace)
# This script gets from primary clipboard
# This edit uses "xclip" instead of "xsel" to support more signs and characters
# Added -t text/html to xclip command to make use of direct paste in notefield
# Dependency: xclip

from sys import stdin, stdout, argv, version_info, path, platform, exit
import subprocess
import re

png = path[0] + "/bfy-icon.png"
ico = path[0] + "/bfy-icon.ico"

if platform in ("linux","linux2"):
    p = subprocess.Popen(["xclip", "-selection", "c", "-o"], stdout=subprocess.PIPE)
elif platform == "win32":
    p = subprocess.Popen(["powershell.exe", "Get-Clipboard -Format Text"], stdout=subprocess.PIPE)

out, err = p.communicate()
try:
    Inputstring = out.decode('utf-8')
except Exception as e:
    print("Getting text from clipboard failed", e)
    exit(1)

if not out:
    print("No text in clipboard")
    exit(0)

def paste(ToPaste):
    # Python 3 requires a bytearray as input for Popen
    if version_info > (2, 9):
        Output = bytearray()
        Output.extend(ToPaste.encode("utf-8"))
    else:
        Output = ToPaste

    if platform in ("linux","linux2"):
        p = subprocess.Popen(["xclip", "-selection", "c", "-t", "text/html"], stdin=subprocess.PIPE)
        p.communicate(input=Output)

    elif platform == "win32":
        p = subprocess.Popen(['clip.exe'], stdin=subprocess.PIPE)
        p.communicate(input=Output)
 
def Beautify(Inputstring):
    BeautifulString = ""
    newInputstring = ""

    for line in Inputstring.splitlines():
        if line.startswith(" "):
            line = "&nbsp;" + line[1:]
        newInputstring += line.rstrip().replace('<', '&lt;').replace('>', '&gt;') + "\n"
    while "  " in newInputstring:
        newInputstring = newInputstring.replace("  ", "&nbsp;&nbsp;")
    newInputstring = newInputstring.replace('$&nbsp;&nbsp;','$ &nbsp;')
    newInputstring = newInputstring.replace('$&nbsp;','$ ')

    
    Beautifiers = [beautifyWindows, beautifyVsphere, beautifyMSM, beautifyPowerShell, beautifyTerminal, beautifyImage, beautifyOther]

    for beautifier in Beautifiers:
        BeautifulString = beautifier(newInputstring)
    
        if BeautifulString:
            if platform in ("linux","linux2"):
                subprocess.call(["notify-send", "--hint=int:transient:1", "-i", png, "-a", beautifier.__name__, "Use: ctrl+v"])
            elif platform == "win32":
                notification = r"""[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
                                   $objBalloon = New-Object System.Windows.Forms.NotifyIcon
                                   $objBalloon.Icon = "{icon}"
                                   $objBalloon.BalloonTipIcon = "Info"
                                   $objBalloon.BalloonTipTitle = "{Beautifier}"
                                   $objBalloon.BalloonTipText = "Use: Ctrl+V"
                                   $objBalloon.Visible = $True
                                   $objBalloon.ShowBalloonTip(3000)
                                   $objBalloon.Dispose()""".format(Beautifier=beautifier.__name__, icon=ico)
                subprocess.call(["powershell.exe", notification])
            break
    
    paste(BeautifulString)    # pastes to CLIPBOARD

#Windows Events detect:
def beautifyWindows(ParseString):
    if "&lt;/Event&gt;" in ParseString and "Log Name:" in ParseString:
        BeautifulString = ""
        skip = False
        description = False
        for line in ParseString.splitlines():
            newLine = ""
            if skip or line == "Event Xml:":
                skip = True
                if line == "&lt;/Event&gt;":
                    skip = False
                    description = False
                continue
            
            if line.startswith("Description:"):
                description = True
                newLine += "<b>{}</b>".format(line)
            elif description:
                newLine += line
            elif ":&nbsp;" in line or ": " in line:
                if ":&nbsp;" in line:
                    split = line.split(":&nbsp;")
                elif ": " in line:
                    split = line.split(": ")

                if len(split) == 2:
                    if "Error" in split[1]:
                        split[1] = "<b><font color=\"#ff0000\">{}</font></b>".format(split[1])
                    elif "Information" in split[1]:
                        split[1] = "<font color=\"#a9a9a9\">{}</font>".format(split[1])
                    elif "Warning" in split[1]:
                        split[1] = "<font color=\"#daa520\">{}</font>".format(split[1])
                    elif "Critical" in split[1]:
                        split[1] = "<span style=\"background-color: rgb(255, 0, 0);\"><b><font color=\"#ffff00\">{}</font></b></span>".format(split[1])

                    newLine += "<b>{}:</b> {}".format(split[0], split[1])
                else:
                    newLine += line
            else:
                newLine += line

            BeautifulString = BeautifulString + newLine + "</br>"

        return BeautifulString

#vSphere Events detect:
def beautifyVsphere(ParseString):
    BeautifulString = ""
    if ("info" in ParseString or "warning" in ParseString or "error" in ParseString) and ("-" in ParseString or "." in ParseString) and ":" and not "mailcomponents" in ParseString:
        if "-" in ParseString or "." in ParseString:
            if ":" in ParseString:

                BeautifulString = ""
                entries = []
                entry = ""

                for line in ParseString.splitlines():
                    if line=="":
                        entries.append(entry)
                        entry = ""
                    else:
                        entry = entry + line + "\n"

                for entry in entries:
                    tempfoo = {"description": "", "severity": "", "date": "", "desc2": "", "host": "", "doer": ""}

                    linec = 0
                    for line in entry.splitlines():
                        if linec == 0:
                            if "to Green" in line: foo2 = "<font color=\"#008000\"> %s </font>" % line
                            elif "to Yellow" in line: foo2 = "<font color=\"#daa520\"> %s </font>" % line
                            elif "to Red" in line: foo2 = "<font color=\"#ff0000\"> %s </font>" % line
                            elif "to Gray" in line: foo2 = "<font color=\"#a9a9a9\"> %s </font>" % line
                            else: foo2 = line
                            tempfoo["description"] = foo2
                        elif "info" in line or "warning" in line or "error" in line:
                            if "info" in line: foo2 = "<font color=\"#a9a9a9\"> %s </font>" % line
                            elif "warning" in line: foo2 = "<font color=\"#daa520\"> %s </font>" % line
                            elif "error" in line: foo2 = "<font color=\"#ff0000\"> %s </font>" % line
                            elif "user" in line: foo2 = "<font color=\"#0000cd\"> %s </font>" % line
                            tempfoo["severity"] = foo2
                        elif ("." in line or "-" in line) and ":" in line:
                            tempfoo["date"] = line
                        else:
                            tempfoo["desc2"] = tempfoo["desc2"] + line + "</br>"

                        linec = linec + 1

                    if tempfoo["description"] == "" or tempfoo["date"] == "" or tempfoo["severity"] == "":
                        return

                    BeautifulString = BeautifulString + "<b>%s - (%s) - %s</b></br>%s</br>" % (tempfoo["date"], tempfoo["severity"], tempfoo["description"], tempfoo["desc2"])
        return BeautifulString

#MSM Notes
def beautifyMSM(ParseString):
    BeautifulString = ""

    foo = ParseString.split("\n")[0]
    if (foo[:6] == "Public" or foo[:7] == "Private") and foo.count("/")>1 and foo.count(":")>1:
        
        for line in ParseString.splitlines():
            if (line[:6] == "Public" or line[:7] == "Private") and line.count("/")>1 and line.count(":")>1:
                if line[:6] == "Public":
                    offset = 0 
                    if BeautifulString!="": BeautifulString = BeautifulString + "</br>"
                    BeautifulString = BeautifulString + '<b><span style="background-color: rgb(255, 240, 245);"> Public | '
                else:
                    offset = 1
                    if BeautifulString!="": BeautifulString = BeautifulString + "</br>"
                    BeautifulString = BeautifulString + '<b><span style="background-color: rgb(240, 255, 240);"> Private | '

                BeautifulString = BeautifulString + line[6+offset:25+offset] + " | " #Date
                BeautifulString = BeautifulString + line[25+offset:] #Name
                BeautifulString = BeautifulString + "</span></b></br>"
            else:
                BeautifulString = BeautifulString + line + "</br>"
        return "<div style='border-left: 1px solid black; padding-left: 7px; margin-left: 5px;'>" + BeautifulString + "</div>"

def beautifyPowerShell(ParseString):
    BeautifulString = ""

    if "PS " in ParseString and "&gt;" in ParseString:
        for line in ParseString.splitlines():
            if "PS " in line[0:8] and "&gt;" in line:
                if BeautifulString != "" and BeautifulString[-10:] != "</br></br>":
                    BeautifulString = BeautifulString + "</br>"
                BeautifulString = BeautifulString + "<b>" + line.rstrip() + "</b></br>"
            elif "DISKPART&gt;" == line[0:12]:
                if BeautifulString != "" and BeautifulString[-10:] != "</br></br>":
                    BeautifulString = BeautifulString + "</br>"
                BeautifulString = BeautifulString + "<b>" + line.rstrip() + "</b></br>"
            else:
                BeautifulString = BeautifulString + line.rstrip() + "</br>"
        
        BeautifulString = "<div style='background-color: rgb(1,36,86); color: rgb(238,237,240); margin: 5px; padding: 10px;'><font face=\"Courier New\">" + BeautifulString + "</font></div>"

        return BeautifulString

#Terminal text (Aka. terminal-output from various sources)
def beautifyTerminal(ParseString):
    BeautifulString = ""

    if "@" in ParseString or ParseString.startswith("-bash-"):
        for line in ParseString.splitlines():
            newline = ""
            if re.search("[\w]+@[\w]+", line) or line.startswith("-bash-"):
                if BeautifulString != "" and BeautifulString[-10:] != "</br></br>":
                    BeautifulString=BeautifulString + "</br>"
                newline = "<b>" + line + "</b>"

            if newline=="":
                newline = line

            BeautifulString = BeautifulString + newline + "</br>"

        BeautifulString = "<div style='background-color: black; color:white; margin: 5px; padding: 10px;'><font face=\"Courier New\">" + BeautifulString + "</font></div>"
        return BeautifulString

#Marval image
def beautifyImage(ParseString):
    if "Attachment.ashx" in ParseString:
        BeautifulString = ""
        for line in ParseString.splitlines():
            newline = ""
            if "Attachment.ashx" in line:
                newline = "<img src='%s' /></b>" % line.rstrip()
                break
        BeautifulString = BeautifulString + newline + "</br>"
    
        return BeautifulString

#Other text
def beautifyOther(ParseString):
    BeautifulString = ""
    for line in ParseString.splitlines():
        BeautifulString = BeautifulString + line + "</br>"

    BeautifulString = "<div style='background-color: black; color:white; margin: 5px; padding: 10px;'><font face=\"Courier New\">" + BeautifulString + "</font></div>"

    return BeautifulString

Beautify(Inputstring)

