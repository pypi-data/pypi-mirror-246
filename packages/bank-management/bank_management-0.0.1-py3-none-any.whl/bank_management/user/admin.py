from datetime import datetime

from .client import client

client1 = client("Billy","billy@gmail.com",123456,1000,123456)
class admin:
    def __init__(self,name,workNumber,password):
        """
        Initializes a new admin instance.

        Parameters:
        - name (str): The name of the admin.
        - workNumber (int): The work number of the admin.
        - password (int): The password of the admin.
        """
        self.name = name
        self.workNumber = workNumber
        self.password = password
        self.create_time = datetime.now()

    def show_client_detail(self,cl):
        """
        Displays detailed information about a given client.

        Parameters:
        - cl (client): The client instance.

        Prints:
        - Client details including name, email, phone number, creation date, and balance.
        """
        print("This is the information of",cl.name)
        information = cl.show_information()
        columns = ["name","email","PhoneNumber","created_date","balance"]
        for info, column in zip(information, columns):
            print(f"{column}: {info}")
        print("End")
        return information

    # 1: password 2: phoneNumber 3. email
    def edit_client_detail(self,cl,optionNumber,new_one):
        """
        Edits the details of a given client based on the specified option number.

        Parameters:
        - cl (client): The client instance.
        - optionNumber (int): The option number for editing (1: password, 2: phone number, 3: email).
        - new_one (str or int): The new value for the selected option.

        Prints:
        - Success message after editing.
        """

        if optionNumber == 1:
            cl.edit_password(new_one)
        elif optionNumber == 2:
            cl.phoneNumber = new_one
        elif optionNumber == 3:
            cl.email = new_one 

        print("Successfully Edited")
        return
    
def admin_login(admins_dict,clients_dict):
    """
    Authenticates an administrator and allows them to perform operations on clients.

    Parameters:
    - admins_dict (dict): Dictionary containing admin work numbers as keys and admin instances as values.
    - clients_dict (dict): Dictionary containing client names as keys and client instances as values.
    """
    workNumber = int(input("plz enter your Working Number: "))
    ad_temp = admins_dict.get(workNumber)
    #check password
    if ad_temp is not None:
        input_password = int(input("plz enter your password: "))
        if input_password == ad_temp.password:
            ad = admins_dict.get(workNumber)
            print(ad.name,"Successfully login")
            admin_operations(ad,clients_dict)
        else:
            print("Wrong password")
    else:
        print("Not existing")

def admin_operations(admin,clients_dict):
    """
    Provides a menu for administrators to perform various operations on clients.

    Parameters:
    - admin (admin): The admin instance.
    - clients_dict (dict): Dictionary containing client names as keys and client instances as values.
    """
    operation_num =int(input("plz enter your operation number:\n 1. check client's detail 2. edit client's detail 3. quit\n"))
    if operation_num == 3:
        print("bye, admin")
        return
    elif operation_num ==1 or operation_num==2:
        client_name = input("plz enter the client's name:\n ")
        client_target = clients_dict.get(client_name)
        if client_target is not None:
            if operation_num == 1:
                admin.show_client_detail(client_target)
                admin_operations(admin,clients_dict)
            elif operation_num ==2:
                editNumber = int(input("plz enter number:\n 1.edit password 2.edit phone number 3.edit email\n"))
                if editNumber not in (1,2,3):
                    print("Invalid number")
                else:
                    new_detail = input("plz enter your edited detail:\n")
                    admin.edit_client_detail(client_target,editNumber,new_detail)
                    admin_operations(admin,clients_dict)
        else:
            print("Not existing/Wrong name")
            admin_operations(admin,clients_dict)

    else:
        print("Wrong number")

if __name__ == "__main__":
    ad =admin(12,12,12)
    ad.show_client_detail(client1)
