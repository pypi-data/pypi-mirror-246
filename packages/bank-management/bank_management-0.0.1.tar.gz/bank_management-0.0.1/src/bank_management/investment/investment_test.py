import unittest
import sys
import os

# before run this test file, go to the 7th line manage_investment.py and delete a dot
# into this "from investment import investment,mortgage,zero_coupon_bond,government_bond"


# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from investment.investment import investment,mortgage
from investment import zero_coupon_bond,government_bond
from manage_investment import edit_rate, edit_risk, show_all_investment, recommendation_bond, mortgage_initialization, zcb_initialization, gov_initialization

class TestManageInvestmentModule(unittest.TestCase):

    

    def test_zero_coupon_bond_calculation(self):
        zero_coupon_bond_instance = zero_coupon_bond(0.03,1,1000,5)
        zero_coupon_bond_instance.calculate_fv()
        zero_coupon_bond_instance.calculate_YTM()

        # Add more assertions based on your expected results

    def test_government_bond_calculation(self):
        government_bond_instance = government_bond(0.04,2,5000,10,2)
        government_bond_instance.calculate_coupon()

    def setUp(self):
        self.mortgage_dict = mortgage_initialization()
        self.zcb_dict = zcb_initialization()
        self.gov_dict = gov_initialization()

    def test_edit_rate(self):
        mortgage_instance = self.mortgage_dict[1]
        edit_rate(mortgage_instance, 0.06)
        self.assertEqual(mortgage_instance.rate, 0.06)

    def test_edit_risk(self):
        zcb_instance = self.zcb_dict[1]
        edit_risk(zcb_instance, 1)
        self.assertEqual(zcb_instance.risk, 1)

    def test_show_all_investment(self):
        # You can capture the output of the print statements and assert against it
        # For simplicity, this test just checks if the method runs without errors
        show_all_investment(self.mortgage_dict, self.zcb_dict, self.gov_dict)

    def test_recommendation_bond(self):
        # You can capture the output of the print statements and assert against it
        # For simplicity, this test just checks if the method runs without errors
        recommendation_bond(1, 5, 1, self.mortgage_dict, self.zcb_dict,self.gov_dict)


if __name__ == '__main__':
    unittest.main()
