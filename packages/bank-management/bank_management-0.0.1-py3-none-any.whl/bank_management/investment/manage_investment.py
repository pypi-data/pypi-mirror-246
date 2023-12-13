# import sys
# import os

# # Add the project's root directory to the Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .investment import investment,mortgage,zero_coupon_bond,government_bond




def edit_rate(inv,new_rate):
    """
    Edit the interest rate of an investment.

    Parameters:
    - inv (investment): An investment object.
    - new_rate (float): The new interest rate to be set for the investment.
    """
    inv.rate=new_rate

def edit_risk(inv,new_risk):
    """
    Edit the risk level of an investment.

    Parameters:
    - inv (investment): An investment object.
    - new_risk (str): The new risk level to be set for the investment.
    """
    inv.risk=new_risk

def show_all_investment(dict_mort,dict_zcb,dict_gov):
    """
    Display detailed information about all investments (mortgages, zero-coupon bonds, government bonds).

    Parameters:
    - dict_mort (dict): Dictionary containing mortgage objects.
    - dict_zcb (dict): Dictionary containing zero-coupon bond objects.
    - dict_gov (dict): Dictionary containing government bond objects.
    """
    print("All mortgage details")
    for key, value in dict_mort.items():
        print("Mortgage type: ",key,"Mortgage details: ",value.show_details()) #the mortgage dict should be key:representing the mortgage type and value: being a mortgage class
    print("All zero-coupon-bond details")
    for key, value in dict_zcb.items():
        print("Zero-coupon-bond type: ",key,"Zero-coupon-bond details: ",value.show_details())
    print("All government bond details")
    for key, value in dict_gov.items():
        print("Government bond type: ",key,"Government bond details: ",value.show_details())

def recommendation_bond(user_risk,user_rate,choose_type,dict_mort,dict_zcb,dict_gov):#choose_type being 1/2/3, representing mort/zcb/gov
    """
    Provide investment recommendations based on user risk and return rate preferences.

    Parameters:
    - user_risk (str): User's risk preference.
    - user_rate (float): User's desired return rate.
    - choose_type (int): 1 for mortgage, 2 for zero-coupon bond, 3 for government bond.
    - dict_mort (dict): Dictionary containing mortgage objects.
    - dict_zcb (dict): Dictionary containing zero-coupon bond objects.
    - dict_gov (dict): Dictionary containing government bond objects.
    """
    print("We will give you recommendation based on your risk and return rate preference.")
    print("The final investment recommendation we give you will best match the rate and risk you provided.")
    if choose_type==1:
        dict_use=dict_mort
    elif choose_type==2:
        dict_use=dict_zcb
    elif choose_type==3:
        dict_use=dict_gov
    
    min_sum=200000
    value_store=[]
    

    for value in dict_use.values():# to get the min tempsum
        temp_sum=abs(value.rate-user_rate)+abs(value.risk-user_risk)
        if temp_sum<min_sum:
            min_sum=temp_sum
    for value in dict_use.values():# to store the key of min tempsum
        temp_sum=abs(value.rate-user_rate)+abs(value.risk-user_risk)
        if temp_sum==min_sum:
            value_store.append(value)
    
    print("the final recommendation is: ")
    for value in value_store:
        value.show_details()

    
#initialization
def mortgage_initialization():
    """
    Initialize mortgage objects.

    Returns:
    - dict: Dictionary containing mortgage objects.
    """
    # initialize 
    mortgage1 = mortgage(0.03,5,5,2000)
    mortgage2 = mortgage(0.04,7,5,3000)
    mortgage3 = mortgage(0.05,8,10,4000)
    mortgage_dict = {
        1: mortgage1,
        2: mortgage2,
        3: mortgage3
    }
    return mortgage_dict

def zcb_initialization():
    """
    Initialize zero-coupon bond objects.

    Returns:
    - dict: Dictionary containing zero-coupon bond objects.
    """
    # initialize 
    zcb1 = zero_coupon_bond(0.03,5,2000,5)
    zcb2 = zero_coupon_bond(0.06,10,3000,8)
    zcb_dict = {
        1: zcb1,
        2: zcb2
    }
    return zcb_dict

def gov_initialization():
    """
    Initialize government bond objects.

    Returns:
    - dict: Dictionary containing government bond objects.
    """
    # initialize 
    gov1 = government_bond(0.03,5,2000,4,1)
    gov2 = government_bond(0.05,5,3000,5,1)
    gov3 = government_bond(0.05,6,2000,3,2)
    gov_dict = {
        1: gov1,
        2: gov2,
        3: gov3

    }
    return gov_dict



