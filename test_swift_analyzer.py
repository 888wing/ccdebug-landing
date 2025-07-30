"""Test cases for Swift error analyzer."""

import unittest
from swift_analyzer import SwiftAnalyzer, SwiftError


class TestSwiftAnalyzer(unittest.TestCase):
    """Test Swift analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SwiftAnalyzer()
    
    def test_nil_unwrap_error(self):
        """Test nil unwrapping error detection."""
        error_text = "Fatal error: Unexpectedly found nil while unwrapping an Optional value"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'nil_unwrap')
        self.assertEqual(result.severity, 'critical')
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_type_mismatch_error(self):
        """Test type mismatch error detection."""
        error_text = "Cannot convert value of type 'String' to expected argument type 'Int'"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'type_mismatch')
        self.assertEqual(result.severity, 'high')
    
    def test_array_bounds_error(self):
        """Test array index out of range error."""
        error_text = "Fatal error: Index out of range"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'array_bounds')
        self.assertEqual(result.severity, 'critical')
    
    def test_protocol_conformance_error(self):
        """Test protocol conformance error."""
        error_text = "Type 'MyViewController' does not conform to protocol 'UITableViewDataSource'"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'protocol_conformance')
    
    def test_swiftui_state_error(self):
        """Test SwiftUI state access error."""
        error_text = "Accessing State's value outside of being installed on a View"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'swiftui_state')
    
    def test_async_await_error(self):
        """Test async/await error detection."""
        error_text = "'async' call in a function that does not support concurrency"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'async_await')
    
    def test_file_info_extraction(self):
        """Test file path and line number extraction."""
        error_text = "ProfileView.swift:42:10: Fatal error: Unexpectedly found nil while unwrapping an Optional value"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.file_path, 'ProfileView.swift')
        self.assertEqual(result.line, 42)
    
    def test_xcode_module_error(self):
        """Test Xcode module not found error."""
        error_text = "No such module 'Alamofire'"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'module_not_found')
    
    def test_unknown_error(self):
        """Test handling of unknown Swift errors."""
        error_text = "Some random Swift error that doesn't match patterns"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unknown_swift_error')
        self.assertEqual(result.severity, 'medium')
    
    def test_chinese_formatting(self):
        """Test Chinese language formatting."""
        error_text = "Fatal error: Index out of range"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='zh')
        
        self.assertIn('Swift 錯誤', formatted)
        self.assertIn('智能建議', formatted)
    
    def test_english_formatting(self):
        """Test English language formatting."""
        error_text = "Fatal error: Index out of range"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='en')
        
        self.assertIn('Swift Error', formatted)
        self.assertIn('Smart Suggestions', formatted)


class TestSwiftAnalyzerIntegration(unittest.TestCase):
    """Integration tests for Swift analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SwiftAnalyzer()
    
    def test_real_world_error_scenarios(self):
        """Test with real-world Swift error messages."""
        real_errors = [
            {
                'text': "ViewController.swift:23:15: Fatal error: Unexpectedly found nil while implicitly unwrapping an Optional value",
                'expected_type': 'nil_unwrap',
                'expected_file': 'ViewController.swift',
                'expected_line': 23
            },
            {
                'text': "error: cannot convert value of type '[String : Any]' to expected argument type 'Data'",
                'expected_type': 'type_mismatch'
            },
            {
                'text': "Thread 1: Fatal error: Index out of range",
                'expected_type': 'array_bounds'
            },
            {
                'text': "ContentView.swift:45:20: Accessing State's value outside of being installed on a View. This will result in a constant Binding of the initial value and will not update.",
                'expected_type': 'swiftui_state',
                'expected_file': 'ContentView.swift',
                'expected_line': 45
            }
        ]
        
        for scenario in real_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                
                if 'expected_file' in scenario:
                    self.assertEqual(result.file_path, scenario['expected_file'])
                if 'expected_line' in scenario:
                    self.assertEqual(result.line, scenario['expected_line'])
    
    def test_suggestion_quality(self):
        """Test that suggestions are relevant and helpful."""
        error_text = "Fatal error: Unexpectedly found nil while unwrapping an Optional value"
        result = self.analyzer.analyze(error_text)
        
        # Check that suggestions exist and have required fields
        self.assertTrue(len(result.suggestions) > 0)
        for suggestion in result.suggestions:
            self.assertIn('title', suggestion)
            self.assertIn('code', suggestion)
            self.assertIn('confidence', suggestion)
            self.assertGreater(suggestion['confidence'], 0)
            self.assertLessEqual(suggestion['confidence'], 1)
    
    def test_performance(self):
        """Test analyzer performance with multiple errors."""
        import time
        
        errors = [
            "Fatal error: Unexpectedly found nil while unwrapping an Optional value",
            "Cannot convert value of type 'String' to expected argument type 'Int'",
            "Fatal error: Index out of range",
            "Type 'MyClass' does not conform to protocol 'Codable'",
            "No such module 'SwiftUI'"
        ] * 20  # Test with 100 errors
        
        start_time = time.time()
        for error in errors:
            self.analyzer.analyze(error)
        end_time = time.time()
        
        # Should analyze 100 errors in less than 1 second
        self.assertLess(end_time - start_time, 1.0)


if __name__ == '__main__':
    unittest.main()