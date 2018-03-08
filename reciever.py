import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


port = 12345
s.bind(('',port))
print("socket binded to port",port)
s.listen(5)
print("socket is listening")


while True:
    c, addr = s.accept()
    message = ""
    while True:
        one_char = c.recv(1)
        message += one_char
        if one_char == '\n':
            break
          
    print(message)
    
    #Now write to file
    with open("../newLib/waypoints/tasks.txt",'a') as file_obj:
        file_obj.write(message.encode())
            


    c.close()
