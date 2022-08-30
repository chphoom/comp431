import fileinput
import re
import helper


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
    if currStatus == status[354]:
        output.append(line)
    # • If/when “end-of-file” is reached on standard input (i.e., when control-D is typed from the keyboard
    # under Linux), terminate your program. Otherwise...
    # • Echo the line of input to standard output (i.e., print the line of input exactly as it was input to
    if line == "\n" and currStatus == status[354]:
        output.append(status[4])
        print(status[4])
        print(status[250])
        currStatus == status[1]
        f.write(output)
    else: print(line)
    # standard output [i.e., to the Linux window in which you entered the command to execute your
    # program]).
    #print("\n*" + line, end='')
    # • When well-formed (syntax and order) SMTP commands are read, print responses as described
    # below in section titled “Responses for Well-Formed Commands”.
    lineList = re.split('\s\t\0\n', line)
    command = lineList[0];
    # • For invalid (ill-formed) commands, print out the error message as described in the section below
    # titled “Error Processing”.
    if command in status.values():
        if command == status[1] == currStatus:
            if lineList[2]!="FROM:" or helper.validPath(lineList[3])==False: #: add check valid path
                print(status[501])
            else: 
                output.append(line)
                currStatus = status[2]
        elif command == status[2] == currStatus:
            if lineList[2]!="TO:" or helper.validPath(lineList[3])==False: #: add check for valid path
                print(status[501])
            else: 
                path = "forward/" + lineList[3]
                f = open(path,"w+")
                currStatus = status[3]
                output.append(line)
        elif command == status[3] == currStatus:
            currStatus = status[354]
            output.append(line)
        else:
            print(status[503])
    elif currStatus != status[354]:
        print(status[500])