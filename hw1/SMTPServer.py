import fileinput
import re
import helper
import os


status = {
    1: "MAIL",
    2: "RCPT",
    3:"DATA",
    250:"250 OK",
    354:"354 Start mail input; end with . on a line by itself",
    4:".",
    500:"500 Syntax error: command unrecognized",
    501:"501 Syntax error in parameters or arguments",
    503:"503 Bad sequence of commands"
}#end of dictionary

output = []

# Your program should be structured as a loop that:
# • Reads a line of input from standard input (the keyboard in Linux).
currStatus = status[1];
for line in fileinput.input():
    if currStatus == status[354] and line != "\n":
        output.append(line)
    # • If/when “end-of-file” is reached on standard input (i.e., when control-D is typed from the keyboard
    # under Linux), terminate your program. Otherwise...
    # • Echo the line of input to standard output (i.e., print the line of input exactly as it was input to
    print(line, end='')
    #print(currStatus)
    # standard output [i.e., to the Linux window in which you entered the command to execute your
    # program]).
    #print("\n*" + line, end='')
    # • When well-formed (syntax and order) SMTP commands are read, print responses as described
    # below in section titled “Responses for Well-Formed Commands”.
    lineList = re.split('[\s\t\0\n]', line)
    lineList = list(filter(None,lineList))
    command = lineList[0]
    # • For invalid (ill-formed) commands, print out the error message as described in the section below
    # titled “Error Processing”.
    if command in status.values():
        if command == status[1] == currStatus:
            lineList = re.split(':', lineList[1])
            command = lineList[0]
            if lineList[0]!="FROM":
                print(status[500])
            elif helper.validPath(lineList[1])==False: #: add check valid path
                print(status[501])
            else: 
                output.append(line)
                print(status[250])
                currStatus = status[2]
        elif command == status[2] == currStatus:
            lineList = re.split(':', lineList[1])
            command = lineList[0]
            if lineList[0]!="TO":
                print(status[500])
            elif helper.validPath(lineList[1])==False: #: add check for valid path
                print(status[501])
            else: 
                path = os.path.join('forward/', lineList[2])
                f = open(path,"a+")
                print(status[250])
                currStatus = status[3]
                output.append(line)
        elif command == status[3] == currStatus:
            print(status[354])
            currStatus = status[354]
            output.append(line)
        elif command == status[4]:
            print(status[250])
            for s in output:
                f.write(s)
            currStatus = status[1]
            output.clear()
        else:
            print(status[503])
    elif currStatus != status[354]:
        print(status[500])