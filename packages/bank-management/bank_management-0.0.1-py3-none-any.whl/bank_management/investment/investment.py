class investment:
    def __init__(self,rate,risk):
        """
        Initialize an investment object with a given rate and risk.

        Parameters:
        - rate (float): The interest rate of the investment.
        - risk (str): The risk associated with the investment.
        """
        self.rate=rate
        self.risk=risk

class mortgage(investment):
    def __init__(self,rate,risk,year,initial_payment):
        investment.__init__(self,rate,risk)
        """
        Initialize a mortgage object with a given rate, risk, loan duration, and initial payment.

        Parameters:
        - rate (float): The interest rate of the mortgage.
        - risk (str): The risk associated with the mortgage.
        - year (int): The duration of the mortgage in years.
        - initial_payment (float): The initial payment of the mortgage.
        """
        self.P=initial_payment
        self.r=self.rate/12
        self.n=year

    def calculate_mortgage(self):
        """
        Calculate and print the monthly mortgage payment.
        """
        payment=self.P*(self.r*pow((1+self.r),self.n))/pow((1+self.r),self.n)
        print("the monthly payment should be: ",payment)
        return payment
    def show_details(self):
        """
        Print detailed information about the mortgage.
        """
        print("The information details are:")
        print("rate:",self.rate,", risk:",self.risk,", year:",self.n,", initial payment:",self.P)
        
    


class zero_coupon_bond(investment):
    def __init__(self,rate,risk,pv,year):
        """
        Initialize a zero-coupon bond object with a given rate, risk, present value, and duration.

        Parameters:
        - rate (float): The interest rate of the zero-coupon bond.
        - risk (str): The risk associated with the zero-coupon bond.
        - pv (float): The present value of the zero-coupon bond.
        - year (int): The duration of the zero-coupon bond in years.
        """
        investment.__init__(self,rate,risk)
        self.pv=pv
        self.n=year
    def calculate_fv(self):
        """
        Calculate and print the future value of the zero-coupon bond.
        """
        fv=pow((1+self.rate),self.n)*self.pv
        print("the fv of the zero-coupon bond is: ",fv)
        return fv

    def calculate_YTM(self):
        """
        Calculate and print the yield to maturity of the zero-coupon bond.
        """
        print("the YTM of the zero coupon bond is: ", self.risk)
    
    def show_details(self):
        """
        Print detailed information about the zero-coupon bond.
        """
        print("The information details are:")
        print("rate:",self.rate,", risk:",self.risk,", year:",self.n,", present value:",self.pv)


class government_bond(investment):
    def __init__(self,rate,risk,face_value,year,annual_semiannual):
        """
        Initialize a government bond object with a given rate, risk, face value, duration, and payment frequency.

        Parameters:
        - rate (float): The interest rate of the government bond.
        - risk (str): The risk associated with the government bond.
        - face_value (float): The face value of the government bond.
        - year (int): The duration of the government bond in years.
        - annual_semiannual (int): The frequency of payments (1 for annual, 2 for semi-annual).
        """
        investment.__init__(self,rate,risk)
        self.pv=face_value
        self.n=year
        self.f=annual_semiannual #annual is 1 and semi-annual is 2

    def calculate_coupon(self):
        """
        Calculate and print the coupon payment based on the payment frequency.
        """
        if(self.f==1):
            payment=self.pv*self. rate
            print("the bond will be paid annual. The payment each time is: ",payment)
            return payment
        elif(self.f==2):
            payment=self.pv*self.rate/2
            print("the bond will be paid semi-annual. The payment each time is: ",payment)
            return payment
        else:
            print("wrong input in the annual/ semi-annual section. Government bond will only be paid in one of the 2 ways.")
        
    def show_details(self): #change function
        """
        Print detailed information about the government bond.
        """
        print("The information details are:")
        print("rate:",self.rate,", risk:",self.risk,", year:",self.n,", face value:",self.pv,", how many times will you be paid in a year:",self.f)




    





