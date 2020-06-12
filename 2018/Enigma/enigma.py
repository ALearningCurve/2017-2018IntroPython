

def check_plug_board(letter, plug_board):
    try:    
        from_dictionary = plug_board[letter]
    except: 
        from_dictionary = letter
    if from_dictionary == "":
        return letter
    return from_dictionary


class enigma_machine(object):
    

    @staticmethod
    def set_wheel_choices(i):
        wheel_0 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] # 0,1,2,3,4....
        wheel_1 = [4,5,3,2,7,19,6,11,23,17,8,1,20,10,22,24,14,16,0,21,12,25,13,9,18,15] #4
        wheel_2 = [25,22,19,9,13,0,3,7,10,5,14,17,24,15,23,20,12,1,11,21,16,18,2,6,4,8] #25
        wheel_3 = [12,21,18,23,16,11,9,19,17,0,13,25,3,7,1,6,5,8,20,14,15,22,24,2,10,4] #12
        wheel_4 = [1,24,3,17,21,23,13,0,22,14,12,10,11,6,25,4,15,8,18,9,2,20,19,7,5,16] #1
        wheel_5 = [0,15,3,18,20,14,2,21,11,7,23,13,5,6,12,24,22,21,10,1,8,17,16,25,4,9] #0
        while True:
            wheel_choice = 0
            try:
                wheel_choice =  int(input("Wheel #" + str(i + 1) + ": " ))
                if wheel_choice == 1:
                    wheel_choice = wheel_1
                elif wheel_choice == 2:
                    wheel_choice = wheel_2
                elif wheel_choice == 3:
                    wheel_choice = wheel_3
                elif wheel_choice == 4: 
                    wheel_choice = wheel_4
                elif wheel_choice == 5:
                    wheel_choice = wheel_5
                elif wheel_choice == 0:
                    wheel_choice = wheel_0
                    
                else:
                    print ("The wheel # has to be 0-5, you entered " + str(wheel_choice) + ".")
                    continue
                return wheel_choice
                
            except:
                print("//error//")
                print("Your selection caused an error,")
                print("Make sure to enter a number between 0 and 5")
                print(" ")
            
    @staticmethod
    def set_plugboard():
        """
        return {
            "a" : input("a:"),
            "b" : input("b:"),
            "c" : input("c:"),
            "d" : input("d:"),
            "e" : input("e:"),
            "f" : input("f:"),
            "g" : input("g:"),
            "h" : input("h:"),
            "i" : input("i:"),
            "j" : input("j:"),
            "k" : input("k:"),
            "l" : input("l:"),
            "m" : input("m:"),
            "n" : input("n:"),
            "o" : input("o:"),
            "p" : input("p:"),
            "q" : input("q:"),
            "r" : input("r:"),
            "s" : input("s:"),
            "t" : input("t:"),
            "u" : input("u:"),
            "v" : input("v:"),
            "w" : input("w:"),
            "x" : input("x:"),
            "y" : input("y:"),
            "z" : input("z:")
            """           
        return {
            "a" : "",
            "b" : "",
            "c" : "",
            "d" : "",
            "e" : "",
            "f" : "",
            "g" : "",
            "h" : "",
            "i" : "",
            "j" : "",
            "k" : "",
            "l" : "",
            "m" : "",
            "n" : "",
            "o" : "",
            "p" : "",
            "q" : "",
            "r" : "",
            "s" : "",
            "t" : "",
            "u" : "",
            "v" : "",
            "w" : "",
            "x" : "",
            "y" : "",
            "z" : ""}

    @staticmethod
    def set_wheel(i):
        while True:
            try:
                return int(input("Shift #" + str(i + 1) + ": " ))
            
            except: 
                print("//error//")
                print("Your selection caused an error,")
                print("Make sure to enter a number between 0 and 25")
                print(" ")


    def __init__(self):
        #print ("Enigma Machine (Version 3)")
        self.shifts = []
        self.wheels = []
        self.switchboard = enigma_machine.set_plugboard()
        
            
        self.num_gears = 3 #int(input("How many gears for this encryption? "))
        print ("Enter the wheels to use as the " + str(self.num_gears) + " gears")
        print ("Then enter the encryption for " + str(self.num_gears) + " gears")
        for i in range(self.num_gears):
            self.wheels.append(enigma_machine.set_wheel_choices(i))
            self.shifts.append(enigma_machine.set_wheel(i))
            print (" ")

        self.constants = ["empty"]
        self.constants = self.constants + self.shifts
            
    def encrypt (self, message):
        message_list = []
        self.shifts = self.constants[1:4]
        for i in range(len(message)):
            
            if ord(message[i]) in range(65,91) or ord(message[i]) in range(97,123):
                message_list.append(check_plug_board(message[i], self.switchboard))
                message_list[i] = ord(message_list[i])
            else:                      
                message_list.append(ord(message[i]))
                
           
        for i in range(len(message_list)):
            if ord(message[i]) in range(65,91) or  ord(message[i]) in range(97,123):
                
                if self.shifts[0] == 26:
                    self.shifts[0] = self.shifts[0] - 26
                    self.shifts[1] = self.shifts[1] + 1
                
                if self.shifts[1] == 26:
                    self.shifts[1] = self.shifts[1] - 26
                    self.shifts[2] = self.shifts[2] + 1
                    
                if self.shifts[2] == 26:
                    self.shifts[2] = self.shifts[2] - 1
            
                the_change = self.wheels[0][self.shifts[0]] + self.wheels[1][self.shifts[1]] + self.wheels[2][self.shifts[2]]

                message_list[i] = message_list [i] + the_change
                
                if ord(message[i]) in range(65,91):
                    while message_list[i] < 65:
                        message_list[i] = message_list[i] + 26
                    
                    while message_list[i] > 90:
                        message_list[i] = message_list[i] - 26
                        
                if ord(message[i]) in range(97,123):
                    while message_list[i] < 97:
                        message_list[i] = message_list[i] + 26
                    
                    while message_list[i] > 122:
                        message_list[i] = message_list[i] - 26
                                          
                message_list[i] = chr(message_list[i])
                self.shifts[0] = self.shifts[0] + 1
            
            else:
                ######for other characters#######
                if self.shifts[0] == 26:
                    self.shifts[0] = self.shifts[0] - 26
                    self.shifts[1] = self.shifts[1] + 1
                
                if self.shifts[1] == 26:
                    self.shifts[1] = self.shifts[1] - 26
                    self.shifts[2] = self.shifts[2] + 1
                    
                if self.shifts[2] == 26:
                    self.shifts[2] = self.shifts[2] - 1
            
                the_change = self.wheels[0][self.shifts[0]] + self.wheels[1][self.shifts[1]] + self.wheels[2][self.shifts[2]]
                
                message_list[i] = message_list [i] + the_change
                
                if ord(message[i]) in range(32,65):
                    while message_list[i] < 32:
                        message_list[i] = message_list[i] + 33
                    
                    while message_list[i] > 64:
                        message_list[i] = message_list[i] - 33
                        
                if ord(message[i]) in range(91,97):
                    while message_list[i] < 91:
                        message_list[i] = message_list[i] + 6
                    
                    while message_list[i] > 96:
                        message_list[i] = message_list[i] - 6
                        
                if ord(message[i]) in range(123,127):
                    while message_list[i] < 123:
                        message_list[i] = message_list[i] + 4
                    
                    while message_list[i] > 126:
                        message_list[i] = message_list[i] - 4
                        
                                          
                message_list[i] = chr(message_list[i])
                self.shifts[0] = self.shifts[0] + 1
                               
        for i in range(len(message_list)):
            if  ord(message[i]) in range(65,91) or ord(message[i]) in range(97,123):
                message_list [i] = check_plug_board(message_list[i], self.switchboard)
            
        return "".join (message_list)
    

    def decrypt(self, message):
        self.shifts = self.constants[1:4]
        message_list = []

        
        for i in range(len(message)):
            if  ord(message[i]) in range(65,91) or ord(message[i]) in range(97,123):
                message_list.append(check_plug_board(message[i], self.switchboard))
                message_list[i] = ord(message_list[i])
            else:
                message_list.append(ord(message[i]))
                
        for i in range(len(message_list)):
            if ord(message[i]) in range(65,91) or ord(message[i]) in range(97,123):
                if self.shifts[0] == 26:
                    self.shifts[0] = self.shifts[0] - 26
                    self.shifts[1] = self.shifts[1] + 1
                
                if self.shifts[1] == 26:
                    self.shifts[1] = self.shifts[1] - 26
                    self.shifts[2] = self.shifts[2] + 1
                    
                if self.shifts[2] == 26:
                    self.shifts[2] = self.shifts[2] - 1
            
                the_change = self.wheels[0][self.shifts[0]] + self.wheels[1][self.shifts[1]] + self.wheels[2][self.shifts[2]]
                   
                message_list[i] = message_list [i] - the_change
                
                if ord(message[i]) in range(65,91):
                    while message_list[i] < 65:
                        message_list[i] = message_list[i] + 26
                    
                    while message_list[i] > 91:
                        message_list[i] = message_list[i] - 26
                        
                if ord(message[i]) in range(97,123):
                    while message_list[i] < 97:
                        message_list[i] = message_list[i] + 26
                    
                    while message_list[i] > 122:
                        message_list[i] = message_list[i] - 26
           
                message_list[i] = chr(message_list[i])
                self.shifts[0] = self.shifts[0] + 1


            elif ord(message[i]) in range(32,65) or ord(message[i]) in range(123,127) or ord(message[i]) in range(91,97):
                ######for other characters#######
                if self.shifts[0] == 26:
                    self.shifts[0] = self.shifts[0] - 26
                    self.shifts[1] = self.shifts[1] + 1
                
                if self.shifts[1] == 26:
                    self.shifts[1] = self.shifts[1] - 26
                    self.shifts[2] = self.shifts[2] + 1
                    
                if self.shifts[2] == 26:
                    self.shifts[2] = self.shifts[2] - 1
            
                the_change = self.wheels[0][self.shifts[0]] + self.wheels[1][self.shifts[1]] + self.wheels[2][self.shifts[2]]
                
                message_list[i] = message_list [i] - the_change
                
                if ord(message[i]) in range(32,65):
                    while message_list[i] < 32:
                        message_list[i] = message_list[i] + 33
                    
                    while message_list[i] > 64:
                        message_list[i] = message_list[i] - 33
                        
                if ord(message[i]) in range(91,97):
                    while message_list[i] < 91:
                        message_list[i] = message_list[i] + 6
                    
                    while message_list[i] > 96:
                        message_list[i] = message_list[i] - 6
                        
                if ord(message[i]) in range(123,127):
                    while message_list[i] < 123:
                        message_list[i] = message_list[i] + 4
                    
                    while message_list[i] > 126:
                        message_list[i] = message_list[i] - 4
                                                                
                message_list[i] = chr(message_list[i])
                self.shifts[0] = self.shifts[0] + 1
        
            
        for i in range(len(message_list)):
            if  ord(message[i]) in range(65,91) or ord(message[i]) in range(97,123):
                message_list [i] = check_plug_board(message_list[i], self.switchboard)
        print (message_list)
        return "".join (message_list)



"""
my_enigma = enigma_machine()

to_be_encrypted = "Winter break is in less than 4 weeks! Hopefully there is no homework." #str(input("message?"))
encrypted =  my_enigma.encrypt(to_be_encrypted)
print(encrypted)
print (my_enigma.decrypt(encrypted))
"""


