#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced SQL Code Understanding window features
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from ai_interface import AIInterface
    from ai_config import AIConfig
    import tkinter as tk
    
    def test_understanding_window():
        """Test the enhanced Understanding window"""
        print("🎯 Testing Enhanced SQL Code Understanding Window")
        print("=" * 50)
        
        # Create test window
        root = tk.Tk()
        root.withdraw()  # Hide main window
        
        # Initialize AI components
        ai_config = AIConfig()
        
        def get_sample_sql():
            return """
            SELECT c.customer_id, c.customer_name, o.order_date, p.product_name
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id  
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_date >= '2024-01-01'
            ORDER BY o.order_date DESC
            """
        
        ai_interface = AIInterface(ai_config, get_sample_sql)
        
        # Sample AI response
        sample_response = """
🎯 **SQL Analysis Results:**

**Query Purpose:** 
This query retrieves customer order details with product information for orders placed since January 1st, 2024.

**Tables Used:**
- `customers` (c) - Customer information
- `orders` (o) - Order records  
- `order_items` (oi) - Items within orders
- `products` (p) - Product catalog

**Joins Explained:**
1. `customers` ↔ `orders`: Links customers to their orders
2. `orders` ↔ `order_items`: Gets items for each order
3. `order_items` ↔ `products`: Retrieves product details

**Key Features:**
- Date filter: Only orders from 2024 onwards
- Sorted by order date (newest first)
- Combines data from 4 related tables

**Optimization Suggestions:**
1. Ensure indexes on join columns (customer_id, order_id, product_id)
2. Consider date index on orders.order_date
3. Use LIMIT if only top N results needed
        """
        
        # Show the enhanced understanding window
        window = ai_interface.show_understand_result(
            "SQL Code Understanding - Enhanced Demo", 
            sample_response,
            get_sample_sql()
        )
        
        # Instructions for user
        print("\n✅ Enhanced Understanding Window Features:")
        print("🔍 ZOOM CONTROLS:")
        print("  • Global Zoom: Top-right buttons affect ALL sections")
        print("  • Section Zoom: Individual zoom for each section")
        print("  • Keyboard: Ctrl+Plus/Minus to zoom, Ctrl+0 to reset")
        print("\n📏 SIZING:")
        print("  • Drag the horizontal bars to resize sections")
        print("  • Each section is now 20-50% larger by default")
        print("  • Window is 1200x900 (20% bigger than before)")
        print("\n🎯 QUICK QUESTIONS:")
        print("  • Meaningful button labels instead of Q1, Q2, etc.")
        print("  • Hover for tooltips with full question text")
        print("  • Color-coded zoom controls per section")
        print("\n⌨️  KEYBOARD SHORTCUTS:")
        print("  • Ctrl+Enter: Submit question")
        print("  • Ctrl+Plus: Zoom in all sections")
        print("  • Ctrl+Minus: Zoom out all sections") 
        print("  • Ctrl+0: Reset all zoom levels")
        print("\n💡 TIP: Try the different zoom controls and resize the sections!")
        print("🎉 The interface is now much more readable and professional!")
        
        root.mainloop()
    
    if __name__ == "__main__":
        test_understanding_window()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all modules are available")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Failed to create test window")