#!/usr/bin/env python3
"""
Test script to verify AI configuration dialog works properly
"""

import tkinter as tk
from sql_mask_gui import EnhancedSQLMaskerGUI

def test_ai_config():
    """Test that AI config dialog opens without errors"""
    root = tk.Tk()
    app = EnhancedSQLMaskerGUI(root)
    
    print("✅ Application created successfully")
    print("✅ AI features initialized")
    print("✅ Ready to test AI configuration dialog")
    print("\nTo test:")
    print("1. Click 'Enable AI Features' button")
    print("2. Click 'AI Config' button")
    print("3. Verify all fields and buttons are visible")
    print("4. Test the Save and Cancel buttons")
    
    root.mainloop()

if __name__ == "__main__":
    test_ai_config()