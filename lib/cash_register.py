# cash_register.py

class CashRegister:
    """A cash register for an e-commerce site"""
    
    def __init__(self, discount=0):
        """
        Initialize the cash register
        
        Args:
            discount: Discount percentage (0-100). Defaults to 0
        """
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []
    
    @property
    def discount(self):
        """Get the discount percentage"""
        return self._discount
    
    @discount.setter
    def discount(self, value):
        """
        Set discount with validation
        
        Args:
            value: Discount percentage (must be integer between 0-100)
        """
        # Check if discount is an integer
        if not isinstance(value, int):
            print("Not valid discount")
            self._discount = 0
            return
        
        # Check if discount is between 0 and 100
        if 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")
            self._discount = 0
    
    def add_item(self, item, price, quantity=1):
        """
        Add an item to the register
        
        Args:
            item: Name of the item
            price: Price per unit
            quantity: Number of items (defaults to 1)
        """
        # Calculate total cost for this item
        item_total = price * quantity
        
        # Add to overall total
        self.total += item_total
        
        # Add item to items list (quantity times)
        for _ in range(quantity):
            self.items.append(item)
        
        # Record transaction
        transaction = {
            'item': item,
            'price': price,
            'quantity': quantity,
            'item_total': item_total
        }
        self.previous_transactions.append(transaction)
    
    def apply_discount(self):
        """Apply the discount to the total price"""
        if not self.previous_transactions:
            message = "There is no discount to apply."
            print(message)
            return message

        if self.discount > 0:
            # Calculate discount amount
            discount_amount = self.total * (self.discount / 100)
            # Apply discount
            self.total -= discount_amount
            # Round to 2 decimal places
            self.total = round(self.total, 2)
            message = f"Discount of {self.discount}% applied. New total: ${self.total}"
            print(message)
            return message

        message = "There is no discount to apply."
        print(message)
        return message
    
    def void_last_transaction(self):
        """Remove the last transaction and update total and items"""
        if not self.previous_transactions:
            message = "There is no transaction to void."
            print(message)
            return message
        
        # Get the last transaction
        last_transaction = self.previous_transactions.pop()
        
        # Subtract from total
        self.total -= last_transaction['item_total']
        self.total = round(self.total, 2)
        
        # Remove items from items list
        for _ in range(last_transaction['quantity']):
            if last_transaction['item'] in self.items:
                self.items.remove(last_transaction['item'])
        
        message = f"Voided: {last_transaction['quantity']} x {last_transaction['item']}"
        print(message)
        return message
    
    def __str__(self):
        """String representation of the cash register"""
        return f"Cash Register - Total: ${self.total}, Items: {len(self.items)}, Discount: {self.discount}%"


# Example usage
if __name__ == "__main__":
    # Create a cash register with 20% discount
    register = CashRegister(20)
    
    # Add items
    register.add_item("Book", 15.99, 2)
    register.add_item("Pen", 2.50, 3)
    
    print(f"Total before discount: ${register.total}")
    
    # Apply discount
    register.apply_discount()
    
    # Void last transaction
    register.void_last_transaction()
    
    print(f"Final total: ${register.total}")
    print(f"Items left: {register.items}")