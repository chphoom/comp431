from smtplib import SMTP
import SMTPserver
import socket
import sys
#import serverHelper

socStatus = {
    220: "220 hostname",
    250: "250 hello echo pleased to meet you",
    221: "221 hostname closing conneection"

}  # end of dictionary

#from client
code = "utf-8"
DATASIZE = 256

# In this assignment you will write a program that will extend and convert your SMTP
# “server” program (HW 1) into a “real” SMTP server that is able to interacts with the
# SMTP “client” program provided by the TAs (Client.py), which mimics the behaviors of a
# real user mail agent and SMTP client. And as real clients and servers, your HW 3
# programs will interoperate over a network by using a TCP socket.
# To do this you will need to:
# • Implement the final portions of the SMTP protocol,
# • Replace the stdin/stdout I/O for SMTP commands with socket I/O, and
# • Do some additional message processing and formatting in the SMTP client.
# The final portions of the SMTP protocol are the generation of a greeting message by the
# server upon receipt of a connection, and the generation of the HELO message by the
# client in response to the server’s greeting message.

s = socket.socket()  # create a socket object
# print ("Socket successfully created")
#port = 8000+9634  # 8000 + last 4 digits of PID


while True:
    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    # Your SMTP server program requires only a single command line argument: the port
    # number on which it should listen for connections from clients.
    port = int(sys.argv[1])
    s.bind(('', port))
    # print ("socket binded to %s" %(port))

    # put the socket into listening mode
    s.listen(5)
    # print ("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs

    # Establish connection with client.
    c, addr = s.accept()
    # print ('Got connection from', addr )

    hostname = c.getpeername()

    # create standard greeting
    # send a thank you message to the client. encoding to send byte type
    SMTPserver.outPrint(socStatus[220].replace("hostname", hostname[0].strip('[\s\t\0\n]')), c, code)

    # After sending this message the server must receive and acknowledge
    # a valid SMTP HELO command from the client before proceeding with mail processing
    line = c.recv(DATASIZE).decode(code)
    #print(line)
    # (see the following section). The HELO message is acknowledged by the server with a 250
    # message. By convention, the text of the acknowledgement of the HELO message echoes
    # the text of the HELO message and includes the phrase “pleased to meet you.” If the server
    # receives an invalid HELO message (as defined by the grammar below) it should emit
    # either a 500 or a 501 error as appropriate.
    # <helo-cmd> ::= “HELO” <whitespace> <domain> <nullspace> <CRLF>
    if line.split()[0]!="HELO":
        SMTPserver.outPrint(SMTPserver.status[500], c, code);
    else:
        SMTPserver.outPrint(socStatus[250].replace("echo", line.lstrip("HELO")), c, code)
        # Once the HELO command has been received (the formal grammar for the HELO
        # command is given below) and acknowledged, the server enters its message processing
        # loop and begins processing messages until the QUIT command is received.
        currStatus = SMTPserver.status[1]
        while  line != "QUIT":
            line = c.recv(DATASIZE).decode(code)
            if currStatus == SMTPserver.status[4]:
                if line != "QUIT":
                    currStatus = SMTPserver.status[1]
            newStat = SMTPserver.parse(line, c, code, currStatus)
            currStatus = newStat   
        #if line == "QUIT":
        if currStatus == SMTPserver.status[4]:
            SMTPserver.outPrint(socStatus[221].replace("hostname", hostname), c , code)
            s.close()
        else:
            #TODO handle when QUIT is recieved without . message
            SMTPserver.outPrint(SMTPserver.status[500], c, code)

# As in Homework 1, when the server processes mail messages, it should append each
# message that it receives into a “forward-file” (in the subdirectory “forward” which you
# can assume already exists). However, different from Homework 1, the forward-file
# filename should be the domain name of the receiver as specified in the RCPT TO field of
# the SMTP command. Thus, for example, if a message is received by the server addressed
# to jeffay@cs.unc.edu (i.e., the server received the command “RCPT TO:
# <jeffay@cs.unc.edu>”), then the message should be appended to the file
# forward/cs.unc.edu in the current working directory. Each message appended to a forward
# file should only contain the massage associated with that mail transaction, i.e what comes
# after the DATA command and before the QUIT command. (in particular, HELO, MAIL
# FROM, RCPT TO, DATA, and QUIT commands with their corresponding replies should
# never be written to forward-files. “.” should be written to the forward-files.).
# Your server should deal with any protocol errors it encounters as your HW1 program did.
# That is, if your server encounters a protocol error in some message it receives from the
# client, your server program should generate the appropriate 500, 501, or 503 response
# message. However, now your server should send the error response message to the client
# via the connection socket and not print the message to standard output. If your server
# encounters any non-protocol error from which it cannot recover, the server should close its
# connection to the client (if a connection existed), print to standard output a meaningful 1-
# line error message, and return to its initial state and await the next connection from a new
# client. If an error occurs when creating the welcoming socket simply print a meaningful 1-
# line error message and terminate your program.
# Your server program should echo (print) all of the message it receives from the client
# program and the message sent through the socket to standard output. Your server program
# will perform all of its protocol I/O to a socket. In particular, it should not interact with the
# user directly in any way. Specifically, it should not output prompts (other than printing out
# the data that go through the socket) and it should not read commands or other inputs from
# the keyboard or a file.