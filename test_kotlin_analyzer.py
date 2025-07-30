"""Test cases for Kotlin error analyzer."""

import unittest
from kotlin_analyzer import KotlinAnalyzer, KotlinError


class TestKotlinAnalyzer(unittest.TestCase):
    """Test Kotlin analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = KotlinAnalyzer()
    
    def test_null_pointer_error(self):
        """Test null pointer exception detection."""
        error_text = "java.lang.NullPointerException at MainActivity.kt:45"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'null_pointer')
        self.assertEqual(result.severity, 'critical')
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_kotlin_null_pointer(self):
        """Test Kotlin-specific NPE detection."""
        error_text = "kotlin.KotlinNullPointerException"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'null_pointer')
    
    def test_type_mismatch_error(self):
        """Test type mismatch error detection."""
        error_text = "Type mismatch: inferred type is String but Int was expected"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'type_mismatch')
        self.assertEqual(result.severity, 'high')
    
    def test_unresolved_reference(self):
        """Test unresolved reference error."""
        error_text = "Unresolved reference: findViewById"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unresolved_reference')
    
    def test_class_cast_exception(self):
        """Test class cast exception."""
        error_text = "java.lang.ClassCastException: String cannot be cast to Integer"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'class_cast')
        self.assertEqual(result.severity, 'critical')
    
    def test_coroutine_exception(self):
        """Test coroutine exception detection."""
        error_text = "kotlinx.coroutines.JobCancellationException: Job was cancelled"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'coroutine_exception')
    
    def test_lateinit_not_initialized(self):
        """Test lateinit property access error."""
        error_text = "kotlin.UninitializedPropertyAccessException: lateinit property binding has not been initialized"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'lateinit_not_initialized')
    
    def test_no_such_element(self):
        """Test NoSuchElementException."""
        error_text = "java.util.NoSuchElementException: List is empty."
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'no_such_element')
    
    def test_illegal_argument(self):
        """Test IllegalArgumentException."""
        error_text = "java.lang.IllegalArgumentException: Parameter must be positive"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'illegal_argument')
    
    def test_android_activity_not_found(self):
        """Test Android ActivityNotFoundException."""
        error_text = "android.content.ActivityNotFoundException: Unable to find explicit activity class"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'activity_not_found')
    
    def test_network_on_main_thread(self):
        """Test NetworkOnMainThreadException."""
        error_text = "android.os.NetworkOnMainThreadException"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'network_on_main_thread')
        self.assertEqual(result.severity, 'critical')
    
    def test_gradle_unresolved_dependency(self):
        """Test Gradle dependency resolution error."""
        error_text = "Could not resolve com.example:library:1.0.0"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unresolved_dependency')
    
    def test_duplicate_class_error(self):
        """Test duplicate class error."""
        error_text = "Duplicate class com.example.MyClass found in modules"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'duplicate_class')
    
    def test_file_info_extraction(self):
        """Test file path and line number extraction."""
        error_text = "MainActivity.kt:123:45: error: Unresolved reference: binding"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.file_path, 'MainActivity.kt')
        self.assertEqual(result.line, 123)
    
    def test_unknown_error(self):
        """Test handling of unknown Kotlin errors."""
        error_text = "Some random Kotlin error that doesn't match patterns"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unknown_kotlin_error')
        self.assertEqual(result.severity, 'medium')
    
    def test_chinese_formatting(self):
        """Test Chinese language formatting."""
        error_text = "NullPointerException"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='zh')
        
        self.assertIn('Kotlin 錯誤', formatted)
        self.assertIn('智能建議', formatted)
    
    def test_english_formatting(self):
        """Test English language formatting."""
        error_text = "NullPointerException"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='en')
        
        self.assertIn('Kotlin Error', formatted)
        self.assertIn('Smart Suggestions', formatted)


class TestKotlinAnalyzerIntegration(unittest.TestCase):
    """Integration tests for Kotlin analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = KotlinAnalyzer()
    
    def test_real_world_error_scenarios(self):
        """Test with real-world Kotlin error messages."""
        real_errors = [
            {
                'text': "E/AndroidRuntime: FATAL EXCEPTION: main\n    Process: com.example.app, PID: 12345\n    java.lang.NullPointerException\n        at com.example.app.MainActivity.onCreate(MainActivity.kt:45)",
                'expected_type': 'null_pointer',
                'expected_file': 'MainActivity.kt',
                'expected_line': 45
            },
            {
                'text': "e: /Users/dev/project/app/src/main/java/com/example/UserViewModel.kt: (25, 35): Type mismatch: inferred type is String? but String was expected",
                'expected_type': 'type_mismatch',
                'expected_file': 'UserViewModel.kt',
                'expected_line': 25
            },
            {
                'text': "Caused by: kotlin.UninitializedPropertyAccessException: lateinit property viewModel has not been initialized\n    at com.example.app.ui.MainFragment.onViewCreated(MainFragment.kt:67)",
                'expected_type': 'lateinit_not_initialized',
                'expected_file': 'MainFragment.kt',
                'expected_line': 67
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
        error_text = "NullPointerException"
        result = self.analyzer.analyze(error_text)
        
        # Check that suggestions exist and have required fields
        self.assertTrue(len(result.suggestions) > 0)
        for suggestion in result.suggestions:
            self.assertIn('title', suggestion)
            self.assertIn('code', suggestion)
            self.assertIn('confidence', suggestion)
            self.assertGreater(suggestion['confidence'], 0)
            self.assertLessEqual(suggestion['confidence'], 1)
    
    def test_android_specific_errors(self):
        """Test Android-specific error handling."""
        android_errors = [
            "android.os.NetworkOnMainThreadException",
            "android.content.ActivityNotFoundException: Unable to find explicit activity class {com.example/.MainActivity}",
            "java.lang.RuntimeException: Unable to start activity ComponentInfo{com.example/com.example.MainActivity}: kotlin.UninitializedPropertyAccessException: lateinit property binding has not been initialized"
        ]
        
        for error_text in android_errors:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertNotEqual(result.error_type, 'unknown_kotlin_error')
    
    def test_performance(self):
        """Test analyzer performance with multiple errors."""
        import time
        
        errors = [
            "NullPointerException",
            "Type mismatch: inferred type is String but Int was expected",
            "Unresolved reference: findViewById",
            "ClassCastException: String cannot be cast to Int",
            "NetworkOnMainThreadException"
        ] * 20  # Test with 100 errors
        
        start_time = time.time()
        for error in errors:
            self.analyzer.analyze(error)
        end_time = time.time()
        
        # Should analyze 100 errors in less than 1 second
        self.assertLess(end_time - start_time, 1.0)


if __name__ == '__main__':
    unittest.main()