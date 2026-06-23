"""
Billing Module
This module handles product billing calculations.
Features:
- Accept product details
- Calculate gross amount, discounts, GST
- Apply delivery charges based on amount threshold
- Calculate final payable amount
"""

from src.utils import (
    get_valid_input, validate_quantity, validate_unit_price,
    validate_discount, validate_gst, validate_category,
    STANDARD_DELIVERY_CHARGE, DELIVERY_CHARGE_THRESHOLD,
    VALID_CATEGORIES
)


def get_product_details():
    """
    Accept product details from user with validation.
    
    Returns:
        dict: Dictionary containing product details
    """
    print("\n" + "-"*60)
    print("ENTER PRODUCT DETAILS")
    print("-"*60)
    
    # Get product name
    product_name = input("Enter product name: ").strip()
    while not product_name:
        print("Error: Product name cannot be empty")
        product_name = input("Enter product name: ").strip()
    
    # Get and validate product category
    print(f"\nAvailable categories: {', '.join(VALID_CATEGORIES)}")
    category = input("Enter product category: ").strip()
    while not validate_category(category):
        print(f"Error: Category must be one of {VALID_CATEGORIES}")
        category = input("Enter product category: ").strip()
    
    # Get and validate quantity
    quantity = get_valid_input(
        "Enter quantity (units): ",
        int,
        validate_quantity,
        "Quantity must be greater than 0"
    )
    
    # Get and validate unit price
    unit_price = get_valid_input(
        "Enter unit price (₹): ",
        float,
        validate_unit_price,
        "Unit price cannot be negative"
    )
    
    # Get and validate discount percentage
    discount_percentage = get_valid_input(
        "Enter discount percentage (0-100): ",
        float,
        validate_discount,
        "Discount percentage must be between 0 and 100"
    )
    
    # Get and validate GST percentage
    gst_percentage = get_valid_input(
        "Enter GST percentage: ",
        float,
        validate_gst,
        "GST percentage cannot be negative"
    )
    
    # Get and validate delivery charge
    delivery_charge = get_valid_input(
        "Enter delivery charge (₹): ",
        float,
        lambda x: x >= 0,
        "Delivery charge cannot be negative"
    )
    
    return {
        'name': product_name,
        'category': category,
        'quantity': quantity,
        'unit_price': unit_price,
        'discount_percentage': discount_percentage,
        'gst_percentage': gst_percentage,
        'delivery_charge': delivery_charge
    }


def calculate_billing(product):
    """
    Calculate billing amount with discounts, GST, and delivery charges.
    
    Business Rule:
    - If the amount after discount and GST is above threshold (₹5000),
      delivery charge is waived (set to 0).
    
    Calculation Steps:
    1. Gross Amount = Quantity × Unit Price
    2. Discount Amount = Gross Amount × (Discount % / 100)
    3. Amount After Discount = Gross Amount - Discount Amount
    4. GST Amount = Amount After Discount × (GST % / 100)
    5. Amount Before Delivery = Amount After Discount + GST Amount
    6. If Amount Before Delivery > Threshold, Delivery = 0, else Delivery = Provided Value
    7. Final Payable = Amount Before Delivery + Delivery
    
    Args:
        product (dict): Product details dictionary
    
    Returns:
        dict: Dictionary containing billing details
    """
    
    # Step 1: Calculate gross amount
    gross_amount = product['quantity'] * product['unit_price']
    
    # Step 2: Calculate discount amount
    discount_amount = gross_amount * (product['discount_percentage'] / 100)
    
    # Step 3: Amount after discount
    amount_after_discount = gross_amount - discount_amount
    
    # Step 4: Calculate GST amount
    gst_amount = amount_after_discount * (product['gst_percentage'] / 100)
    
    # Step 5: Calculate amount before delivery
    amount_before_delivery = amount_after_discount + gst_amount
    
    # Step 6: Check if delivery should be waived
    if amount_before_delivery > DELIVERY_CHARGE_THRESHOLD:
        delivery_charge = 0  # Waive delivery charge
        delivery_waived = True
    else:
        delivery_charge = product['delivery_charge']
        delivery_waived = False
    
    # Step 7: Calculate final payable amount
    final_payable_amount = amount_before_delivery + delivery_charge
    
    return {
        'gross_amount': gross_amount,
        'discount_amount': discount_amount,
        'amount_after_discount': amount_after_discount,
        'gst_amount': gst_amount,
        'delivery_charge': delivery_charge,
        'delivery_waived': delivery_waived,
        'final_payable_amount': final_payable_amount
    }
