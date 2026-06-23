"""
Eligibility Module
This module handles loan eligibility and campaign eligibility decisions.
Features:
- Loan eligibility checker with approval/rejection/manual review decisions
- Campaign eligibility assignment based on customer profile
"""

from src.utils import (
    LOAN_MIN_AGE, LOAN_MAX_AGE, LOAN_MIN_INCOME,
    LOAN_EMI_TO_INCOME_MAX, LOAN_MIN_CREDIT_SCORE,
    LOAN_MIN_SAVINGS_PERCENTAGE, CAMPAIGN_SAVINGS_THRESHOLD_HIGH,
    CAMPAIGN_SAVINGS_THRESHOLD_MEDIUM
)


def check_loan_eligibility(customer, financial_summary, requested_loan_amount):
    """
    Check loan eligibility based on customer profile and financial metrics.
    
    Decision Rules:
    
    APPROVED:
    - Age between 21 and 65
    - Monthly income >= 25,000
    - EMI-to-income ratio < 60%
    - Credit score >= 650
    - Savings percentage >= 10%
    - All above conditions must be met
    
    REJECTED:
    - Age < 21 or Age > 65
    - Monthly income < 25,000
    - Credit score < 600
    - EMI-to-income ratio > 60%
    - Savings percentage < 5%
    
    MANUAL REVIEW REQUIRED:
    - Conditions between approved and rejected (ambiguous cases)
    - Risk category is High Risk but other factors are favorable
    - Credit score between 600-650
    - EMI-to-income ratio between 50-60%
    
    Args:
        customer (dict): Customer details
        financial_summary (dict): Financial summary calculated
        requested_loan_amount (float): Requested loan amount
    
    Returns:
        dict: Decision and reason
    """
    
    decision = None
    reason = ""
    
    age = customer['age']
    monthly_income = customer['monthly_income']
    credit_score = customer['credit_score']
    emi_to_income = financial_summary['emi_to_income_ratio']
    savings_percentage = financial_summary['savings_percentage']
    
    # Check for outright rejection conditions
    if age < LOAN_MIN_AGE or age > LOAN_MAX_AGE:
        decision = "Rejected"
        reason = f"Age {age} is outside the eligible range (21-65 years)."
        return {'decision': decision, 'reason': reason}
    
    if monthly_income < LOAN_MIN_INCOME:
        decision = "Rejected"
        reason = f"Monthly income ₹{monthly_income:.2f} is below minimum ₹25,000."
        return {'decision': decision, 'reason': reason}
    
    if credit_score < 600:
        decision = "Rejected"
        reason = f"Credit score {credit_score} is critically low (< 600)."
        return {'decision': decision, 'reason': reason}
    
    # Check for approval conditions
    if (age >= LOAN_MIN_AGE and age <= LOAN_MAX_AGE and
        monthly_income >= LOAN_MIN_INCOME and
        emi_to_income < LOAN_EMI_TO_INCOME_MAX and
        credit_score >= LOAN_MIN_CREDIT_SCORE and
        savings_percentage >= LOAN_MIN_SAVINGS_PERCENTAGE):
        decision = "Approved"
        reason = "All eligibility criteria met. Customer qualifies for the loan."
        return {'decision': decision, 'reason': reason}
    
    # Check for manual review cases
    if credit_score >= 600 and credit_score < LOAN_MIN_CREDIT_SCORE:
        decision = "Manual Review Required"
        reason = f"Credit score {credit_score} is acceptable but below ideal threshold. Manual verification needed."
        return {'decision': decision, 'reason': reason}
    
    if emi_to_income >= 50 and emi_to_income <= LOAN_EMI_TO_INCOME_MAX:
        decision = "Manual Review Required"
        reason = f"EMI-to-income ratio {emi_to_income:.2f}% is high. Manual review recommended."
        return {'decision': decision, 'reason': reason}
    
    if savings_percentage >= 5 and savings_percentage < LOAN_MIN_SAVINGS_PERCENTAGE:
        decision = "Manual Review Required"
        reason = f"Savings percentage {savings_percentage:.2f}% is low. Manual review needed."
        return {'decision': decision, 'reason': reason}
    
    # Default to manual review if not clearly approved or rejected
    if decision is None:
        decision = "Manual Review Required"
        reason = "Customer profile requires manual review for final decision."
    
    return {'decision': decision, 'reason': reason}


def check_campaign_eligibility(customer, financial_summary):
    """
    Assign customer to a marketing campaign based on profile.
    
    Campaign Assignment Rules:
    
    PREMIUM UPSELL CAMPAIGN:
    - Segment = Premium or Enterprise
    - Savings percentage > 30%
    - Customer value = High Value
    
    LOAN OFFER CAMPAIGN:
    - Segment = Standard or Premium
    - Savings percentage between 15-30%
    - Risk category = Low Risk or Medium Risk
    - Credit score >= 650
    
    CASHBACK CAMPAIGN:
    - Segment = Standard
    - Savings percentage between 10-25%
    - City in metro areas (Mumbai, Delhi, Bangalore, Hyderabad, Chennai)
    - Customer value = Medium Value or Low Value
    
    NO CAMPAIGN:
    - High risk customers
    - Savings percentage < 10%
    - Customer value = Low Value and Enterprise segment
    
    Args:
        customer (dict): Customer details
        financial_summary (dict): Financial summary
    
    Returns:
        dict: Campaign assignment and reason
    """
    
    segment = customer['segment']
    city = customer['city']
    savings_percentage = financial_summary['savings_percentage']
    risk_category = financial_summary['risk_category']
    value_category = financial_summary['customer_value_category']
    credit_score = customer['credit_score']
    
    metro_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai"]
    
    # Premium Upsell Campaign
    if (segment in ["Premium", "Enterprise"] and
        savings_percentage > CAMPAIGN_SAVINGS_THRESHOLD_HIGH and
        value_category == "High Value"):
        return {
            'campaign': "Premium Upsell Campaign",
            'reason': f"Premium segment with high savings ({savings_percentage:.2f}%) and high value profile."
        }
    
    # Loan Offer Campaign
    if (segment in ["Standard", "Premium"] and
        CAMPAIGN_SAVINGS_THRESHOLD_MEDIUM <= savings_percentage <= CAMPAIGN_SAVINGS_THRESHOLD_HIGH and
        risk_category in ["Low Risk", "Medium Risk"] and
        credit_score >= 650):
        return {
            'campaign': "Loan Offer Campaign",
            'reason': f"Good credit profile ({credit_score}) with moderate savings and low-medium risk."
        }
    
    # Cashback Campaign
    if (segment == "Standard" and
        10 <= savings_percentage <= 25 and
        city in metro_cities and
        value_category in ["Medium Value", "Low Value"]):
        return {
            'campaign': "Cashback Campaign",
            'reason': f"Standard segment customer in {city} with moderate savings. Cashback incentive recommended."
        }
    
    # No Campaign (Default)
    return {
        'campaign': "No Campaign",
        'reason': f"Customer profile does not qualify for active campaigns. Risk: {risk_category}, Savings: {savings_percentage:.2f}%."
    }
