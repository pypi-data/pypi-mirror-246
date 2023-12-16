
class CustomerService:
    def __init__(self):
        
        self.messages_storage = []

    def save_message(self):
        
        user_message=input("Please leave your message:")
        self.messages_storage.append(user_message)
        print("you message has been sent")
    def customer_service(self):
        customer_choice=input("""Please choose the following options: 'email' if you would like to learn about our app functions" 
                               or 'contact_NO' if you would like to contact our human serive""")
        
        if customer_choice=="email":
            print("Our email address is: xxxxxxxx@bankapp.com")
        if customer_choice=="contact_NO":
            print("Our contact number is xxx-xxx-xxxx")
        else:
            print("Your answer is not clear, please enter the correct option")
    
    

    def calculate_loan_repayment(self, loan_amount, loan_term, annual_interest_rate=0.05):
        
        self.annual_interest_rate=annual_interest_rate
        monthly_interest_rate = self.annual_interest_rate / 12

        
        numerator = loan_amount * monthly_interest_rate

        
        denominator = 1 - (1 + monthly_interest_rate) ** (-loan_term)

    
        monthly_repayment = numerator / denominator

        
        total_repayment = monthly_repayment * loan_term

        return {
            'monthly_repayment': round(monthly_repayment, 2),
            'total_repayment': round(total_repayment, 2)
        }