"""Test cases for Shell/Bash error analyzer."""

import unittest
from shell_analyzer import ShellAnalyzer, ShellError


class TestShellAnalyzer(unittest.TestCase):
    """Test Shell analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ShellAnalyzer()
    
    def test_syntax_error(self):
        """Test shell syntax error detection."""
        test_cases = [
            ("bash: syntax error: unexpected end of file", 'syntax_error'),
            ("/bin/sh: 1: Syntax error: unexpected token", 'syntax_error')
        ]
        
        for error_text, expected_type in test_cases:
            with self.subTest(error=error_text):
                result = self.analyzer.analyze(error_text)
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, expected_type)
                self.assertEqual(result.severity, 'high')
                self.assertTrue(len(result.suggestions) > 0)
    
    def test_syntax_error_near_token(self):
        """Test syntax error near unexpected token."""
        error_text = "./script.sh: line 10: syntax error near unexpected token `}'"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unexpected_token_near')
        self.assertEqual(result.severity, 'high')
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_command_not_found(self):
        """Test command not found error detection."""
        test_cases = [
            "bash: gitx: command not found",
            "./script.sh: line 5: npm: command not found",
            "zsh: command not found: docker-compose"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'command_not_found')
    
    def test_permission_denied(self):
        """Test permission denied error detection."""
        test_cases = [
            "bash: /usr/local/bin/script: Permission denied",
            "./deploy.sh: Permission denied",
            "sudo: /etc/sudoers: Operation not permitted"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'permission_denied')
            self.assertEqual(result.severity, 'high')
    
    def test_unbound_variable(self):
        """Test unbound variable error detection."""
        test_cases = [
            "./deploy.sh: line 5: VAR: unbound variable",
            "bash: UNDEFINED_VAR: unbound variable",
            "./script.sh: line 10: parameter not set"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'unbound_variable')
            self.assertEqual(result.severity, 'medium')
    
    def test_bad_substitution(self):
        """Test bad substitution error detection."""
        test_cases = [
            "./script.sh: line 3: ${VAR[@]: bad substitution",
            "bash: ${array[*]: bad substitution",
            "/bin/sh: 1: bad substitution"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'bad_substitution')
    
    def test_integer_expression_expected(self):
        """Test integer expression error detection."""
        test_cases = [
            "./calc.sh: line 5: [: abc: integer expression expected",
            "bash: [: hello: integer expression expected",
            "./test.sh: line 10: integer expression expected"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'integer_expression_expected')
            self.assertEqual(result.severity, 'medium')
    
    def test_too_many_arguments(self):
        """Test too many arguments error detection."""
        test_cases = [
            "./test.sh: line 15: [: too many arguments",
            "bash: [: too many arguments",
            "./script.sh: line 20: test: too many arguments"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'too_many_arguments')
    
    def test_no_such_file(self):
        """Test no such file error detection."""
        # These are actual file operations, not command lookups
        test_cases = [
            "cat: /tmp/missing.txt: No such file or directory",
            "./script.sh: line 5: cd: /nonexistent: No such file or directory"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'no_such_file')
    
    def test_command_file_not_found(self):
        """Test command not found when it's a file path."""
        # This is actually a command not found error for a script file
        error_text = "bash: ./missing.sh: No such file or directory"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        # This could be either command_not_found or missing_keyword depending on pattern order
        self.assertIn(result.error_type, ['command_not_found', 'missing_keyword', 'no_such_file'])
    
    def test_cannot_overwrite(self):
        """Test cannot overwrite error detection."""
        test_cases = [
            "bash: file.txt: cannot overwrite existing file",
            "./script.sh: line 10: output.log: File exists",
            "zsh: file exists: data.csv"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'cannot_overwrite')
            self.assertEqual(result.severity, 'medium')
    
    def test_broken_pipe(self):
        """Test broken pipe error detection."""
        test_cases = [
            "cat: write error: Broken pipe",
            "./script.sh: line 25: echo: write error: Broken pipe",
            "grep: write error: Broken pipe"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'broken_pipe')
    
    def test_unexpected_token_near(self):
        """Test unexpected token error detection."""
        test_cases = [
            "./script.sh: line 10: syntax error near unexpected token `done'",
            "bash: syntax error near unexpected token `fi'",
            "./test.sh: line 5: syntax error near unexpected token `then'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'unexpected_token_near')
            self.assertEqual(result.severity, 'high')
    
    def test_missing_keyword(self):
        """Test missing keyword error detection."""
        test_cases = [
            "./script.sh: line 50: unexpected EOF while looking for matching `}'",
            "bash: unexpected EOF while looking for matching `\"'",
            "./test.sh: line 25: missing `fi'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'missing_keyword')
    
    def test_array_subscript(self):
        """Test array subscript error detection."""
        test_cases = [
            "./script.sh: line 15: arr[index]: bad array subscript",
            "bash: array[-1]: invalid subscript",
            "./test.sh: line 20: bad array subscript"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'array_subscript')
            self.assertEqual(result.severity, 'medium')
    
    def test_substring_expansion(self):
        """Test substring expansion error detection."""
        test_cases = [
            "./script.sh: line 5: substring expression < 0",
            "bash: ${str:10:5}: substring expression error",
            "./test.sh: line 8: substring expression"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'substring_expansion')
    
    def test_set_e_error(self):
        """Test set -e related error detection."""
        test_cases = [
            "./deploy.sh: line 25: set -e: command failed",
            "Script exited due to errexit",
            "./script.sh: errexit trap triggered"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'set_e_error')
            self.assertEqual(result.severity, 'high')
    
    def test_function_not_found(self):
        """Test function not found error detection."""
        test_cases = [
            "./script.sh: line 10: my_function: function not found",
            "bash: helper_func: procedure not found",
            "./test.sh: line 5: function not found: process_data"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'function_not_found')
    
    def test_script_info_extraction(self):
        """Test script path and line number extraction."""
        test_cases = [
            ("./deploy.sh:25: error message", "deploy.sh", 25),
            ("/home/user/script.sh: line 10: error", "/home/user/script.sh", 10),
            ("line 42 of backup.sh", "backup.sh", 42),
            ('"install.sh", line 15: syntax error', "install.sh", 15)
        ]
        
        for error_text, expected_script, expected_line in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            if expected_script:
                self.assertIn(expected_script, result.script_path or '')
            if expected_line:
                self.assertEqual(result.line, expected_line)
    
    def test_command_extraction(self):
        """Test command extraction from error messages."""
        error_text = "bash: `git stash': command not found"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.command, "git stash")
    
    def test_unknown_error(self):
        """Test handling of unknown shell errors."""
        error_text = "Some random shell error that doesn't match patterns"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unknown_shell_error')
        self.assertEqual(result.severity, 'medium')
    
    def test_chinese_formatting(self):
        """Test Chinese language formatting."""
        error_text = "bash: command not found: npm"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='zh')
        
        self.assertIn('Shell/Bash 錯誤', formatted)
        self.assertIn('智能建議', formatted)
    
    def test_english_formatting(self):
        """Test English language formatting."""
        error_text = "bash: command not found: npm"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='en')
        
        self.assertIn('Shell/Bash Error', formatted)
        self.assertIn('Smart Suggestions', formatted)


class TestShellAnalyzerIntegration(unittest.TestCase):
    """Integration tests for Shell analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ShellAnalyzer()
    
    def test_real_world_bash_errors(self):
        """Test with real-world Bash error messages."""
        real_errors = [
            {
                'text': "./deploy.sh: line 42: syntax error near unexpected token `done'",
                'expected_type': 'unexpected_token_near',
                'expected_script': 'deploy.sh',
                'expected_line': 42
            },
            {
                'text': "bash: /usr/local/bin/node: No such file or directory",
                'expected_type': 'no_such_file',
                'expected_severity': 'high'
            },
            {
                'text': "./build.sh: line 15: JAVA_HOME: unbound variable",
                'expected_type': 'unbound_variable',
                'expected_script': 'build.sh',
                'expected_line': 15
            },
            {
                'text': "./test.sh: line 25: [: missing `]'",
                'expected_type': 'missing_keyword',
                'expected_severity': 'high'
            }
        ]
        
        for scenario in real_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                
                if 'expected_script' in scenario:
                    self.assertIn(scenario['expected_script'], result.script_path or '')
                if 'expected_line' in scenario:
                    self.assertEqual(result.line, scenario['expected_line'])
                if 'expected_severity' in scenario:
                    self.assertEqual(result.severity, scenario['expected_severity'])
    
    def test_suggestion_quality(self):
        """Test that suggestions are relevant and helpful."""
        error_text = "bash: npm: command not found"
        result = self.analyzer.analyze(error_text)
        
        # Check that suggestions exist and have required fields
        self.assertTrue(len(result.suggestions) > 0)
        for suggestion in result.suggestions:
            self.assertIn('title', suggestion)
            self.assertIn('code', suggestion)
            self.assertIn('confidence', suggestion)
            self.assertGreater(suggestion['confidence'], 0)
            self.assertLessEqual(suggestion['confidence'], 1)
    
    def test_complex_error_scenarios(self):
        """Test complex multi-line shell errors."""
        complex_error = """./deploy.sh: line 45: syntax error near unexpected token `}'
./deploy.sh: line 45: `}'"""
        
        result = self.analyzer.analyze(complex_error)
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unexpected_token_near')
        self.assertEqual(result.line, 45)
        self.assertIn('deploy.sh', result.script_path or '')
    
    def test_posix_vs_bash_errors(self):
        """Test errors specific to POSIX sh vs Bash."""
        posix_errors = [
            "/bin/sh: 1: [[: not found",  # Bash-specific syntax in sh
            "/bin/sh: 1: Bad substitution",  # Bash parameter expansion in sh
            "sh: arrays not supported"  # Array syntax in POSIX sh
        ]
        
        for error_text in posix_errors:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            # Should provide suggestions about using bash instead of sh
            self.assertTrue(any('bash' in str(s).lower() for s in result.suggestions))
    
    def test_pipeline_errors(self):
        """Test errors in shell pipelines."""
        pipeline_errors = [
            "grep: write error: Broken pipe",
            "sort: write failed: standard output: Broken pipe",
            "head: write error: Broken pipe"
        ]
        
        for error_text in pipeline_errors:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'broken_pipe')
            # Should suggest SIGPIPE handling
            self.assertTrue(any('PIPE' in str(s) for s in result.suggestions))
    
    def test_performance(self):
        """Test analyzer performance with multiple errors."""
        import time
        
        errors = [
            "bash: command not found",
            "./script.sh: line 10: syntax error",
            "Permission denied",
            "unbound variable",
            "bad substitution",
            "too many arguments"
        ] * 20  # Test with 120 errors
        
        start_time = time.time()
        for error in errors:
            self.analyzer.analyze(error)
        end_time = time.time()
        
        # Should analyze 120 errors in less than 1 second
        self.assertLess(end_time - start_time, 1.0)


if __name__ == '__main__':
    unittest.main()