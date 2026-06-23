"""
Utility Functions and Constants
This module contains constants and utility functions used across the application.
"""

# ==================== CONSTANTS ====================

# Credit score ranges
MIN_CREDIT_SCORE = 300
MAX_CREDIT_SCORE = 900

# Risk category thresholds
RISK_EMI_TO_INCOME_THRESHOLD_LOW = 30      # Less than 30% = Low Risk
RISK_EMI_TO_INCOME_THRESHOLD_MEDIUM = 50   # 30-50% = Medium Risk
RISK_SAVINGS_THRESHOLD_LOW = 20             # Less than 20% savings = High Risk
RISK_AGE_THRESHOLD = 65                      # Age above 65 = High Risk

# Customer value thresholds
VALUE_SAVINGS_THRESHOLD_HIGH = 35            # Greater than 35% savings = High Value
VALUE_SAVINGS_THRESHOLD_MEDIUM = 15          # 15-35% savings = Medium Value
VALUE_INCOME_THRESHOLD_HIGH = 100000         # Income above 100k = High Value factor
VALUE_INCOME_THRESHOLD_MEDIUM = 50000        # Income 50k-100k = Medium Value factor

# Loan eligibility thresholds
LOAN_MIN_AGE = 21
LOAN_MAX_AGE = 65
LOAN_MIN_INCOME = 25000
LOAN_EMI_TO_INCOME_MAX = 60                  # Maximum EMI-to-income ratio for approval
LOAN_MIN_CREDIT_SCORE = 650                  # Minimum credit score for approval
LOAN_MIN_SAVINGS_PERCENTAGE = 10             # Minimum savings percentage for approval

# Campaign eligibility rules
CAMPAIGN_SAVINGS_THRESHOLD_HIGH = 30
CAMPAIGN_SAVINGS_THRESHOLD_MEDIUM = 15

# Billing constants
DELIVERY_CHARGE_THRESHOLD = 5000  # If amount > 5000, delivery is free
STANDARD_DELIVERY_CHARGE = 100

# Valid customer segments
VALID_SEGMENTS = ["Standard", "Premium", "Enterprise"]
VALID_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Surat", "Indore", "Bhopal", "Visakhapatnam"
]
VALID_CATEGORIES = ["Electronics", "Clothing", "Food", "Home", "Sports", "Books", "Other"]


def display_menu():
    """Display the main menu options."""
    print("\n" + "-"*60)
    print("MAIN MENU")
    print("-"*60)
    print("1. Customer Profile & Financial Summary")
    print("2. Product Billing Calculator")
    print("3. Loan Eligibility Decision")
    print("4. Campaign Eligibility Checker")
    print("5. Exit")
    print("-"*60)


def get_valid_input(prompt, data_type, validation_func=None, error_msg="Invalid input"):
    """
    Get validated input from user.
    
    Args:
        prompt (str): The prompt to display to user
        data_type (type): The expected data type (int, float, str)
        validation_func (function): Optional validation function returning True/False
        error_msg (str): Error message to display if validation fails
    
    Returns:
        Converted and validated input value
    """
    while True:
        try:
            user_input = input(prompt).strip()
            converted = data_type(user_input)
            
            if validation_func and not validation_func(converted):
                print(f"Error: {error_msg}")
                continue
            
            return converted
        
        except ValueError:
            print(f"Error: Please enter a valid {data_type.__name__}")


def validate_age(age):
    """Validate age input."""
    return age >= 0


def validate_income(income):
    """Validate income input."""
    return income >= 0


def validate_expenses(expenses):
    """Validate expenses input."""
    return expenses >= 0


def validate_emi(emi):
    """Validate EMI input."""
    return emi >= 0


def validate_credit_score(score):
    """Validate credit score is within range."""
    return MIN_CREDIT_SCORE <= score <= MAX_CREDIT_SCORE


def validate_quantity(quantity):
    """Validate quantity is positive."""
    return quantity > 0


def validate_unit_price(price):
    """Validate unit price is non-negative."""
    return price >= 0


def validate_discount(discount):
    """Validate discount percentage is between 0 and 100."""
    return 0 <= discount <= 100


def validate_gst(gst):
    """Validate GST percentage is non-negative."""
    return gst >= 0


def validate_segment(segment):
    """Validate customer segment."""
    return segment in VALID_SEGMENTS


def validate_city(city):
    """Validate city name."""
    return city in VALID_CITIES


def validate_category(category):
    """Validate product category."""
    return category in VALID_CATEGORIES


def format_currency(amount):
    """Format amount as currency."""
    return f"₹{amount:,.2f}"


def calculate_percentage(part, whole):
    """Calculate percentage safely."""
    if whole == 0:
        return 0
    return (part / whole) * 100
