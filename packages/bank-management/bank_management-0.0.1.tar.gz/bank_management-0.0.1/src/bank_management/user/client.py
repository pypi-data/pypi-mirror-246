from datetime import datetime

class client:
    def __init__(self,name,email,phoneNumber,balance,password):
        """
        Initializes a new client instance.

        Parameters:
        - name (str): The name of the client.
        - email (str): The email of the client.
        - phoneNumber (str): The phone number of the client.
        - balance (float): The initial balance of the client.
        - password (int): The password of the client.
        """
        self.name = name
        self.email = email
        self.phoneNumber = phoneNumber
        self._balance = balance
        self._password = password
        self.create_time = datetime.now()
    
    def save_money(self,amount):
        """
        Increases the client's balance by the specified amount.

        Parameters:
        - amount (float): The amount to be saved by the client.

        Prints:
        - Success message after saving money.
        """
        self._balance += amount
        print(self.name,"Successfully saved!")
    
    def withdraw_money(self,amount):
        """
        Decreases the client's balance by the specified amount if sufficient funds are available.

        Parameters:
        - amount (float): The amount to be withdrawn by the client.

        Prints:
        - Success message after a successful withdrawal or an error message if the balance is insufficient.
        """
        if self._balance<amount:
            print("Not enough balance")
        else:
            self._balance-=amount
            print(self.name,"Successfully withdrew")

    def transfer(self,amount,receiver):
        """
        Transfers money from the client to another client.

        Parameters:
        - amount (float): The amount to be transferred.
        - receiver (client): The receiving client instance.

        Prints:
        - Success message after a successful transfer or an error message if the balance is insufficient.
        """
        if(self._balance<amount):
            print("Not enough money")
        else:
            receiver.save_money(amount)
            print("Successfully transfer to",receiver.name)
            self.withdraw_money(amount)

    def show_information(self):
        """
        Retrieves and returns information about the client.

        Returns:
        - list: A list containing the client's name, email, phone number, creation time, and balance.
        """
        information = [self.name,self.email,self.phoneNumber,self.create_time,self._balance]
        return information
    
    def edit_password(self,new_password):
        """
        Edits the client's password.

        Parameters:
        - new_password (int): The new password for the client.
        """
        self._password = int(new_password)
        

    def get_password(self):
        """
        Retrieves the client's password.

        Returns:
        - int: The client's password.
        """
        return self._password

def new_user_registration():
    """
    Registers a new client with user input for name, phone number, initial balance, email, and password.

    Returns:
    - client: The newly registered client instance.
    """
    name = input("Plz input your name: ")
    phone = input("Plz input your phone number: ")
    initial_balance = float(input("Plz save your money: "))
    
    email = input("Plz input your email: ")
    password = int(input("plz input your password: "))

    c_new = client(name,email,phone,initial_balance,password)

    
    print("Welcome to be the member of this big family!")
    return c_new

def existing_user_login(clients_dict):
    """
    Logs in an existing client with user input for the client's name and password.

    Parameters:
    - clients_dict (dict): Dictionary containing client names as keys and client instances as values.

    Returns:
    - client: The logged-in client instance.
    """
    # existing_user_login
    client_name = input("plz enter your name:\n")
    client_current = clients_dict.get(client_name)

    if client_current is not None:
        password = int(input("plz enter your password\n"))
        #password = int(input("plz enter your password\n"))
        if password != client_current.get_password():
            print("wrong password")
            existing_user_login()
        else:
            print("Welcome",client_current.name)
            return client_current
    else:
        print("Not existing")