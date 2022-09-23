import fileinput
import re
import helper
import os

status = {
    1: "MAIL",
    2: "RCPT",
    3: "DATA",
    250: "250 OK",
    354:"354 Start mail input; end with . on a line by itself",
    4: ".",
    500:"500 Syntax error: command unrecognized",
    501:"501 Syntax error in parameters or arguments",
    503:"503 Bad sequence of commands"
}#end of dictionary

output = []

def parse(line, socket, code, currStatus):
    if line == "\n.\n":
        currStatus = status[4]
    # elif line == "\n":
    #     return currStatus
    if currStatus == status[354] and line != "\n":
        output.append(line)
        if lineList[-1]==status[4]:
            currStatus=status[4]
            command=status[4]
        else:
            return currStatus
    # Your program should be structured as a loop that:
    # • Reads a line of input from standard input (the keyboard in Linux).
    # • If/when “end-of-file” is reached on standard input (i.e., when control-D is typed from the keyboard
    # under Linux), terminate your program. Otherwise...
    # • Echo the line of input to standard output (i.e., print the line of input exactly as it was input to
    #outPrint(line, socket, code)
    #print(currStatus)
    # standard output [i.e., to the Linux window in which you entered the command to execute your
    # program]).
    #print("\n*" + line, end='')
    # • When well-formed (syntax and order) SMTP commands are read, print responses as described
    # below in section titled “Responses for Well-Formed Commands”.
    lineList = re.split('[\s\t\0\n:]', line)
    lineList = list(filter(None,lineList))
    command = lineList[0]

    #print(lineList)
    # • For invalid (ill-formed) commands, print out the error message as described in the section below
    # titled “Error Processing”.
    if command in status.values():
        if command == status[1] == currStatus:
            #lineList = re.split(':', lineList[1])
            #command = lineList[0]
            if lineList[1]!="FROM":
                outPrint(status[500], socket, code)
            elif helper.validPath(lineList[2])==False: #: add check valid path
                outPrint(status[501], socket, code)
            else: 
                #output.append(line)
                outPrint(status[250], socket, code)
                return status[2]
        elif command == status[2] == currStatus:
            #lineList = re.split(':', lineList[1])
            #command = lineList[0]
            if lineList[1]!="TO":
                outPrint(status[500], socket, code)
            elif helper.validPath(lineList[2])==False: #: add check for valid path
                outPrint(status[501], socket, code)
            else: 
                path = os.path.join('forward/', helper.getDomain(lineList[2]))
                f = open(path,"a+")
                outPrint(status[250], socket, code)
                return status[3]
                #output.append(line)
        elif command == status[3] == currStatus:
            outPrint(status[354], socket, code)
            currStatus = status[354]
            output.append(line)
        elif command == status[4]:
            outPrint(status[250], socket, code)
            for s in output:
                f.write(s)
            output.clear()
            return status[4]
        else:
            outPrint(status[503], socket, code)
    elif currStatus != status[354]:
        #print("Error caused by" + command)
        outPrint(status[500], socket, code)
    return currStatus

def outPrint(str, socket, code):
    socket.send(str.strip('[\s\t\0\n]').encode(code))
    print(str.strip('[\s\t\0\n]'))