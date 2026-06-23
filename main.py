"""
Business Rules Engine - Main Entry Point
This module serves as the command-line interface for the business rules engine.
It provides a menu-driven interface for users to access different features.
"""

from src.customer import get_customer_details, calculate_financial_summary
from src.billing import get_product_details, calculate_billing
from src.eligibility import check_loan_eligibility, check_campaign_eligibility
from src.utils import display_menu, get_valid_input

def display_customer_summary():
    """Feature 1: Display customer profile and financial summary."""
    print("\n" + "="*60)
    print("FEATURE 1: CUSTOMER PROFILE AND FINANCIAL SUMMARY")
    print("="*60)
    
    customer = get_customer_details()
    summary = calculate_financial_summary(customer)
    
    print("\n--- CUSTOMER DETAILS ---")
    print(f"Name: {customer['name']}")
    print(f"Age: {customer['age']}")
    print(f"City: {customer['city']}")
    print(f"Monthly Income: ₹{customer['monthly_income']:.2f}")
    print(f"Monthly Expenses: ₹{customer['monthly_expenses']:.2f}")
    print(f"Existing EMI: ₹{customer['existing_emi']:.2f}")
    print(f"Credit Score: {customer['credit_score']}")
    print(f"Customer Segment: {customer['segment']}")
    
    print("\n--- FINANCIAL SUMMARY ---")
    print(f"Monthly Savings: ₹{summary['monthly_savings']:.2f}")
    print(f"Savings Percentage: {summary['savings_percentage']:.2f}%")
    print(f"EMI-to-Income Ratio: {summary['emi_to_income_ratio']:.2f}%")
    print(f"Risk Category: {summary['risk_category']}")
    print(f"Customer Value Category: {summary['customer_value_category']}")
    print("="*60)


def display_billing():
    """Feature 2: Display product billing calculation."""
    print("\n" + "="*60)
    print("FEATURE 2: PRODUCT BILLING CALCULATOR")
    print("="*60)
    
    product = get_product_details()
    billing = calculate_billing(product)
    
    print("\n--- PRODUCT DETAILS ---")
    print(f"Product Name: {product['name']}")
    print(f"Category: {product['category']}")
    print(f"Quantity: {product['quantity']}")
    print(f"Unit Price: ₹{product['unit_price']:.2f}")
    
    print("\n--- BILLING CALCULATION ---")
    print(f"Gross Amount: ₹{billing['gross_amount']:.2f}")
    print(f"Discount ({product['discount_percentage']}%): ₹{billing['discount_amount']:.2f}")
    print(f"Amount After Discount: ₹{billing['amount_after_discount']:.2f}")
    print(f"GST ({product['gst_percentage']}%): ₹{billing['gst_amount']:.2f}")
    print(f"Delivery Charge: ₹{billing['delivery_charge']:.2f}")
    print(f"Final Payable Amount: ₹{billing['final_payable_amount']:.2f}")
    print("="*60)


def display_loan_eligibility():
    """Feature 3: Display loan eligibility decision."""
    print("\n" + "="*60)
    print("FEATURE 3: LOAN ELIGIBILITY DECISION")
    print("="*60)
    
    customer = get_customer_details()
    loan_amount = get_valid_input(
        "Enter requested loan amount (₹): ",
        float,
        lambda x: x > 0,
        "Loan amount must be positive"
    )
    
    summary = calculate_financial_summary(customer)
    decision = check_loan_eligibility(customer, summary, loan_amount)
    
    print("\n--- LOAN ELIGIBILITY RESULT ---")
    print(f"Customer: {customer['name']}")
    print(f"Requested Loan Amount: ₹{loan_amount:.2f}")
    print(f"Decision: {decision['decision']}")
    print(f"Reason: {decision['reason']}")
    print("="*60)


def display_campaign_eligibility():
    """Feature 4: Display campaign eligibility."""
    print("\n" + "="*60)
    print("FEATURE 4: CAMPAIGN ELIGIBILITY CHECKER")
    print("="*60)
    
    customer = get_customer_details()
    summary = calculate_financial_summary(customer)
    campaign = check_campaign_eligibility(customer, summary)
    
    print("\n--- CAMPAIGN ASSIGNMENT ---")
    print(f"Customer: {customer['name']}")
    print(f"Segment: {customer['segment']}")
    print(f"City: {customer['city']}")
    print(f"Savings Percentage: {summary['savings_percentage']:.2f}%")
    print(f"Customer Value: {summary['customer_value_category']}")
    print(f"\nAssigned Campaign: {campaign['campaign']}")
    print(f"Reason: {campaign['reason']}")
    print("="*60)


def main():
    """Main function to run the menu-driven application."""
    print("\n" + "="*60)
    print("WELCOME TO BUSINESS RULES ENGINE")
    print("="*60)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            try:
                display_customer_summary()
            except Exception as e:
                print(f"\nError: {e}")
        
        elif choice == '2':
            try:
                display_billing()
            except Exception as e:
                print(f"\nError: {e}")
        
        elif choice == '3':
            try:
                display_loan_eligibility()
            except Exception as e:
                print(f"\nError: {e}")
        
        elif choice == '4':
            try:
                display_campaign_eligibility()
            except Exception as e:
                print(f"\nError: {e}")
        
        elif choice == '5':
            print("\n" + "="*60)
            print("Thank you for using Business Rules Engine!")
            print("="*60 + "\n")
            break
        
        else:
            print("\nInvalid choice! Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
