#!/usr/bin/env python3
"""
Test script for modular SQL Masker application
"""

import tkinter as tk

def test_modular_app():
    """Test that modular application starts without errors"""
    try:
        # Import the modular version
        from sql_mask_gui_modular import EnhancedSQLMaskerGUI
        
        print("✅ Successfully imported modular application")
        
        # Test core components
        from ai_config import AIConfig
        from ai_interface import AIInterface
        from sql_masker import SQLMasker, NameGenerator, SQLAnalyzer
        from syntax_highlighter import HighlightedText, SQLSyntaxHighlighter
        
        print("✅ Successfully imported all modules")
        
        # Test basic functionality
        ai_config = AIConfig()
        print(f"✅ AI Config initialized: {ai_config.config}")
        
        sql_masker = SQLMasker()
        print("✅ SQL Masker initialized")
        
        name_gen = NameGenerator()
        test_table = name_gen.generate_table_name("users")
        test_column = name_gen.generate_column_name("user_id")
        print(f"✅ Name Generator works: {test_table}, {test_column}")
        
        analyzer = SQLAnalyzer()
        test_sql = "SELECT user_id, name FROM users WHERE age > 25"
        entities = analyzer.extract_tables(test_sql)
        print(f"✅ SQL Analyzer works: found tables {entities}")
        
        print("\n🎉 All modular components working correctly!")
        print("\nTo test the GUI:")
        print("python sql_mask_gui_modular.py")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_modular_app()