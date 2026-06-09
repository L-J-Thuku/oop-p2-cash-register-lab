# test_cash_register.py

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cash_register import CashRegister

class TestCashRegister(unittest.TestCase):
    
    def setUp(self):
        """Create a fresh cash register before each test"""
        self.register = CashRegister()
    
    def test_init_default_discount(self):
        """Test that discount defaults to 0"""
        self.assertEqual(self.register.discount, 0)
    
    def test_init_with_discount(self):
        """Test that discount can be set"""
        register = CashRegister(20)
        self.assertEqual(register.discount, 20)
    
    def test_discount_validation_integer(self):
        """Test that discount must be an integer"""
        register = CashRegister("20")
        self.assertEqual(register.discount, 0)  # Should default to 0
    
    def test_discount_validation_range(self):
        """Test that discount must be between 0-100"""
        register = CashRegister(150)
        self.assertEqual(register.discount, 0)
        
        register = CashRegister(-10)
        self.assertEqual(register.discount, 0)
    
    def test_add_item_updates_total(self):
        """Test that add_item correctly updates total"""
        self.register.add_item("Apple", 1.50, 2)
        self.assertEqual(self.register.total, 3.00)
    
    def test_add_item_updates_items_list(self):
        """Test that add_item correctly updates items list"""
        self.register.add_item("Banana", 0.75, 3)
        self.assertEqual(len(self.register.items), 3)
        self.assertEqual(self.register.items, ["Banana", "Banana", "Banana"])
    
    def test_add_item_records_transaction(self):
        """Test that add_item records transaction"""
        self.register.add_item("Orange", 2.00, 1)
        self.assertEqual(len(self.register.previous_transactions), 1)
        self.assertEqual(self.register.previous_transactions[0]['item'], "Orange")
    
    def test_apply_discount_with_valid_discount(self):
        """Test that apply_discount reduces total correctly"""
        register = CashRegister(20)
        register.add_item("Shirt", 50.00, 1)
        register.apply_discount()
        self.assertEqual(register.total, 40.00)  # 20% off $50 = $40
    
    def test_apply_discount_success_message(self):
        """Test that apply_discount returns the expected success message"""
        register = CashRegister(20)
        register.add_item("Shirt", 50.00, 1)
        message = register.apply_discount()
        self.assertEqual(message, "After the discount, the total comes to $40.")
    
    def test_apply_discount_with_no_discount(self):
        """Test that apply_discount prints message when no discount"""
        self.register.add_item("Hat", 25.00, 1)
        self.register.apply_discount()
        # Total should remain unchanged
        self.assertEqual(self.register.total, 25.00)
    
    def test_void_last_transaction(self):
        """Test that void_last_transaction removes last transaction"""
        self.register.add_item("Shoes", 60.00, 1)
        self.register.add_item("Socks", 10.00, 2)
        
        initial_total = self.register.total
        initial_items_count = len(self.register.items)
        
        self.register.void_last_transaction()
        
        # Should remove the socks transaction (2 pairs for $20)
        self.assertEqual(self.register.total, initial_total - 20.00)
        self.assertEqual(len(self.register.items), initial_items_count - 2)
    
    def test_void_empty_transaction(self):
        """Test voiding when no transactions exist"""
        self.register.void_last_transaction()  # Should not error
    
    def test_multiple_items_same_name(self):
        """Test adding multiple items with same name"""
        self.register.add_item("Apple", 1.00, 5)
        self.assertEqual(len(self.register.items), 5)
        self.assertEqual(self.register.total, 5.00)

if __name__ == "__main__":
    unittest.main()