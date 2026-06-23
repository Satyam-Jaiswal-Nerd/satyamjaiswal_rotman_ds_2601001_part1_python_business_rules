"""
Customer Module
This module handles customer profile information and financial summary calculations.
Features:
- Accept customer details
- Calculate financial metrics
- Determine risk and value categories
"""

from src.utils import (
    get_valid_input, validate_age, validate_income, validate_expenses,
    validate_emi, validate_credit_score, validate_segment, validate_city,
    calculate_percentage, VALID_SEGMENTS, VALID_CITIES,
    RISK_EMI_TO_INCOME_THRESHOLD_LOW, RISK_EMI_TO_INCOME_THRESHOLD_MEDIUM,
    RISK_SAVINGS_THRESHOLD_LOW, RISK_AGE_THRESHOLD,
    VALUE_SAVINGS_THRESHOLD_HIGH, VALUE_SAVINGS_THRESHOLD_MEDIUM,
    VALUE_INCOME_THRESHOLD_HIGH, VALUE_INCOME_THRESHOLD_MEDIUM
)


def get_customer_details():
    """
    Accept customer details from user with validation.
    
    Returns:
        dict: Dictionary containing customer details
    """
    print("\n" + "-"*60)
    print("ENTER CUSTOMER DETAILS")
    print("-"*60)
    
    # Get customer name
    name = input("Enter customer name: ").strip()
    while not name:
        print("Error: Name cannot be empty")
        name = input("Enter customer name: ").strip()
    
    # Get and validate age
    age = get_valid_input(
        "Enter age (years): ",
        int,
        validate_age,
        "Age cannot be negative"
    )
    
    # Get and validate city
    print(f"\nAvailable cities: {', '.join(VALID_CITIES)}")
    city = input("Enter city: ").strip()
    while not validate_city(city):
        print(f"Error: City not in the list. Please enter from: {', '.join(VALID_CITIES)}")
        city = input("Enter city: ").strip()
    
    # Get and validate monthly income
    monthly_income = get_valid_input(
        "Enter monthly income (₹): ",
        float,
        validate_income,
        "Monthly income cannot be negative"
    )
    
    # Get and validate monthly expenses
    monthly_expenses = get_valid_input(
        "Enter monthly expenses (₹): ",
        float,
        validate_expenses,
        "Monthly expenses cannot be negative"
    )
    
    # Get and validate existing EMI
    existing_emi = get_valid_input(
        "Enter existing EMI amount (₹): ",
        float,
        validate_emi,
        "EMI cannot be negative"
    )
    
    # Get and validate credit score
    credit_score = get_valid_input(
        "Enter credit score (300-900): ",
        int,
        validate_credit_score,
        "Credit score must be between 300 and 900"
    )
    
    # Get and validate customer segment
    print(f"\nAvailable segments: {', '.join(VALID_SEGMENTS)}")
    segment = input("Enter customer segment (Standard/Premium/Enterprise): ").strip()
    while not validate_segment(segment):
        print(f"Error: Segment must be one of {VALID_SEGMENTS}")
        segment = input("Enter customer segment: ").strip()
    
    return {
        'name': name,
        'age': age,
        'city': city,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'existing_emi': existing_emi,
        'credit_score': credit_score,
        'segment': segment
    }


def calculate_financial_summary(customer):
    """
    Calculate financial metrics and categorizations.
    
    Business Rules:
    
    RISK CATEGORIES:
    - Low Risk: EMI-to-Income < 30% AND Savings % >= 20% AND Age < 65 AND Credit Score >= 700
    - High Risk: EMI-to-Income > 50% OR Savings % < 10% OR Age >= 65 OR Credit Score < 600
    - Medium Risk: Everything else
    
    CUSTOMER VALUE CATEGORIES:
    - High Value: Savings % > 35% AND Monthly Income > 100,000 AND Credit Score >= 750
    - Low Value: Savings % < 15% OR Monthly Income < 50,000 AND Credit Score < 650
    - Medium Value: Everything else
    
    Args:
        customer (dict): Customer details dictionary
    
    Returns:
        dict: Dictionary containing financial summary and categorizations
    """
    
    # Calculate financial metrics
    monthly_savings = customer['monthly_income'] - customer['monthly_expenses']
    savings_percentage = calculate_percentage(monthly_savings, customer['monthly_income'])
    emi_to_income_ratio = calculate_percentage(customer['existing_emi'], customer['monthly_income'])
    
    # Determine risk category
    if (emi_to_income_ratio < RISK_EMI_TO_INCOME_THRESHOLD_LOW and 
        savings_percentage >= RISK_SAVINGS_THRESHOLD_LOW and 
        customer['age'] < RISK_AGE_THRESHOLD and 
        customer['credit_score'] >= 700):
        risk_category = "Low Risk"
    elif (emi_to_income_ratio > RISK_EMI_TO_INCOME_THRESHOLD_MEDIUM or 
          savings_percentage < 10 or 
          customer['age'] >= RISK_AGE_THRESHOLD or 
          customer['credit_score'] < 600):
        risk_category = "High Risk"
    else:
        risk_category = "Medium Risk"
    
    # Determine customer value category
    if (savings_percentage > VALUE_SAVINGS_THRESHOLD_HIGH and 
        customer['monthly_income'] > VALUE_INCOME_THRESHOLD_HIGH and 
        customer['credit_score'] >= 750):
        customer_value_category = "High Value"
    elif (savings_percentage < VALUE_SAVINGS_THRESHOLD_MEDIUM or 
          customer['monthly_income'] < VALUE_INCOME_THRESHOLD_MEDIUM or 
          customer['credit_score'] < 650):
        customer_value_category = "Low Value"
    else:
        customer_value_category = "Medium Value"
    
    return {
        'monthly_savings': monthly_savings,
        'savings_percentage': savings_percentage,
        'emi_to_income_ratio': emi_to_income_ratio,
        'risk_category': risk_category,
        'customer_value_category': customer_value_category
    }
