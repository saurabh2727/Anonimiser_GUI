#!/usr/bin/env python3
"""
Test script for AI-enhanced masking functionality
Demonstrates the difference between traditional and AI-enhanced mapping generation
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from sql_masker import SQLMasker
from ai_config import AIConfig

def test_traditional_masking():
    """Test traditional random masking"""
    print("=" * 60)
    print("TRADITIONAL MASKING TEST")
    print("=" * 60)
    
    # Sample SQL from your test data
    sample_sql = """
    SELECT calc, billed_flag, dt, first_appeared_dt, offline_category, days_off_line, latest_traffic_dt
    FROM sys_offline_services 
    WHERE billed_flag = 'ASI000000000035' 
    AND offline_category LIKE 'Telstra - Consumer%'
    ORDER BY latest_traffic_dt DESC
    """
    
    masker = SQLMasker(naming_mode='business_like')
    
    print("Original SQL:")
    print(sample_sql)
    
    # Analyze and generate traditional mappings
    entities = masker.analyze_sql(sample_sql)
    masker.generate_mappings(entities)
    
    print("\nTraditional Mappings:")
    mappings = masker.get_all_mappings()
    for category, mapping in mappings.items():
        if mapping:
            print(f"\n{category.upper()}:")
            for original, masked in mapping.items():
                print(f"  {original} → {masked}")
    
    # Apply masking
    masked_sql = masker.mask_sql(sample_sql)
    print(f"\nMasked SQL:")
    print(masked_sql)

def test_ai_enhanced_masking():
    """Test AI-enhanced semantic masking"""
    print("\n" + "=" * 60)
    print("AI-ENHANCED MASKING TEST")
    print("=" * 60)
    
    # Check if AI is available
    ai_config = AIConfig()
    if not ai_config.is_configured():
        print("⚠️  AI not configured. Using local LLM defaults...")
        print("Make sure Ollama is running with deepseek-coder-v2:latest model")
        print("Or configure AI settings in the GUI first.")
        return
    
    # Sample SQL from your test data  
    sample_sql = """
    SELECT calc, billed_flag, dt, first_appeared_dt, offline_category, days_off_line, latest_traffic_dt
    FROM sys_offline_services 
    WHERE billed_flag = 'ASI000000000035' 
    AND offline_category LIKE 'Telstra - Consumer%'
    ORDER BY latest_traffic_dt DESC
    """
    
    masker = SQLMasker(naming_mode='ai_enhanced', ai_config=ai_config)
    
    print("Original SQL:")
    print(sample_sql)
    
    # Analyze and generate AI-enhanced mappings
    entities = masker.analyze_sql(sample_sql)
    print(f"\nDetected entities:")
    print(f"Tables: {entities['tables']}")
    print(f"Columns: {entities['columns']}")
    print(f"Strings: {entities['strings']}")
    
    print("\nGenerating AI-enhanced mappings...")
    masker.generate_mappings(entities)
    
    print("\nAI-Enhanced Mappings:")
    mappings = masker.get_all_mappings()
    for category, mapping in mappings.items():
        if mapping:
            print(f"\n{category.upper()}:")
            for original, masked in mapping.items():
                print(f"  {original} → {masked}")
    
    # Apply masking
    masked_sql = masker.mask_sql(sample_sql)
    print(f"\nMasked SQL:")
    print(masked_sql)

def compare_mapping_quality():
    """Compare traditional vs AI-enhanced mapping quality"""
    print("\n" + "=" * 60)
    print("MAPPING QUALITY COMPARISON")
    print("=" * 60)
    
    print("""
TRADITIONAL MAPPING CHARACTERISTICS:
• Random string generation
• No semantic preservation
• No business context awareness
• Example: 'customer_table' → 'tbl_order_master'

AI-ENHANCED MAPPING BENEFITS:
• Semantic meaning preservation
• Business domain awareness
• Consistent relationship mapping
• Example: 'customer_table' → 'client_data'
• Maintains field type hints ('created_date' → 'record_timestamp')
• Preserves string structure ('Company - Division' → 'Provider - Unit')

WHEN TO USE AI-ENHANCED MASKING:
✅ Sharing queries with external teams for review
✅ Documentation and training materials
✅ Code reviews where context matters
✅ Maintaining readability in masked queries

WHEN TRADITIONAL MASKING IS SUFFICIENT:
✅ Maximum anonymization requirements
✅ Simple internal testing
✅ When AI infrastructure is not available
✅ Performance-critical scenarios
    """)

def main():
    """Main test runner"""
    print("🎭 SQL Masking Comparison Test")
    print("Testing traditional vs AI-enhanced masking approaches\n")
    
    try:
        # Test traditional masking first
        test_traditional_masking()
        
        # Test AI-enhanced masking
        test_ai_enhanced_masking()
        
        # Show comparison
        compare_mapping_quality()
        
        print("\n" + "=" * 60)
        print("✅ Test completed!")
        print("Run the GUI application to try interactive AI masking.")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()