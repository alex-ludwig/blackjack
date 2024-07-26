class Banking:
    
    def __init__(self):
        pass
        
    def print_balance(self):
        print(f"Accounts of: {self.name}\tTotal Balance: {self.balance}")
    
    def deposit(self, value):
        
        self.balance += value
        #self.check_balance()
        #self.print_balance()
        
    def withdraw(self, value):

        if self.balance <= 0 or (self.balance - value)<0: 
            print("\n### YOU AIN'T GOT SH#T BRUVV!###\n")
            #print(f"Accounts of: {self.name}\tTotal Balance: {self.balance}")
            return 0
        else:
            self.balance -= value
            #self.print_balance()
            return value

class Account(Banking):
    
    def __init__(self, name="new account", balance=0):
        
        # setup Account
        self.name = name
        self.balance = balance
        
        # setup Banking
        Banking.__init__(self)
        
        #check balance
        #Banking.print_balance(self)
        
    def check_again(self):
        print(f"REAL BALANCE: {self.balance}")