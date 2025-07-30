"""Test cases for SQL error analyzer."""

import unittest
from sql_analyzer import SQLAnalyzer, SQLError


class TestSQLAnalyzer(unittest.TestCase):
    """Test SQL analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SQLAnalyzer()
    
    def test_syntax_error(self):
        """Test SQL syntax error detection."""
        error_text = "You have an error in your SQL syntax near 'FORM users' at line 1"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'syntax_error')
        self.assertEqual(result.severity, 'high')
        self.assertEqual(result.line, 1)
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_missing_column_error(self):
        """Test missing column error detection."""
        test_cases = [
            "ERROR 1054: Unknown column 'username' in 'field list'",
            "Column 'email' does not exist",
            "no such column: user_id"
        ]
        
        for error_text in test_cases:
            with self.subTest(error=error_text):
                result = self.analyzer.analyze(error_text)
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, 'missing_column')
    
    def test_missing_table_error(self):
        """Test missing table error detection."""
        test_cases = [
            "Table 'database.users' doesn't exist",
            "ERROR: relation \"products\" does not exist",
            "no such table: orders"
        ]
        
        for error_text in test_cases:
            with self.subTest(error=error_text):
                result = self.analyzer.analyze(error_text)
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, 'missing_table')
    
    def test_type_mismatch_error(self):
        """Test type mismatch error detection."""
        test_cases = [
            "Data type mismatch in criteria expression",
            "invalid input syntax for integer: \"abc\"",
            "Cannot convert varchar to int"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'type_mismatch')
    
    def test_constraint_violation(self):
        """Test constraint violation detection."""
        test_cases = [
            "Duplicate entry 'john@example.com' for key 'email'",
            "foreign key constraint fails",
            "unique constraint violation",
            "check constraint 'age_check' is violated"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'constraint_violation')
    
    def test_permission_denied(self):
        """Test permission denied error detection."""
        test_cases = [
            "permission denied for table users",
            "insufficient privileges to access database"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'permission_denied')
            self.assertEqual(result.severity, 'critical')
    
    def test_access_denied_as_auth_error(self):
        """Test that 'Access denied for user' is properly identified as authentication error."""
        error_text = "ERROR 1045: Access denied for user 'root'@'localhost'"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'authentication_failed')
        self.assertEqual(result.severity, 'critical')
    
    def test_deadlock_error(self):
        """Test deadlock error detection."""
        test_cases = [
            "Deadlock found when trying to get lock",
            "Lock wait timeout exceeded",
            "transaction was aborted due to deadlock"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'deadlock')
            self.assertEqual(result.severity, 'critical')
    
    def test_connection_refused(self):
        """Test connection refused error."""
        test_cases = [
            "Connection refused: connect",
            "could not connect to server: Connection refused",
            "Can't connect to MySQL server on 'localhost'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'connection_refused')
    
    def test_authentication_failed(self):
        """Test authentication failure detection."""
        test_cases = [
            "password authentication failed for user \"admin\"",
            "Access denied for user 'root'@'localhost' (using password: YES)",
            "authentication failed"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'authentication_failed')
    
    def test_database_not_found(self):
        """Test database not found error."""
        test_cases = [
            "database \"myapp\" does not exist",
            "Unknown database 'testdb'",
            "FATAL: database \"production\" does not exist"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'database_not_found')
    
    def test_slow_query(self):
        """Test slow query detection."""
        test_cases = [
            "Query execution was interrupted, maximum statement execution time exceeded",
            "query timeout after 30 seconds"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'slow_query')
            self.assertEqual(result.severity, 'medium')
    
    def test_dialect_detection(self):
        """Test SQL dialect detection."""
        test_cases = [
            ("MySQL server error", "mysql"),
            ("PostgreSQL: ERROR", "postgresql"),
            ("SQLite error: no such table", "sqlite"),
            ("SQL Server Native Client", "mssql"),
            ("ORA-01017: invalid username/password", "oracle")
        ]
        
        for error_text, expected_dialect in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.sql_dialect, expected_dialect)
    
    def test_line_info_extraction(self):
        """Test line and position extraction."""
        test_cases = [
            ("Error at line 42", 42, None),
            ("LINE 10: SELECT * FROM", 10, None),
            ("error:15:25: syntax error", 15, 25),
            ("at line 5, column 10", 5, 10)
        ]
        
        for error_text, expected_line, expected_pos in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            if expected_line:
                self.assertEqual(result.line, expected_line)
            if expected_pos:
                self.assertEqual(result.position, expected_pos)
    
    def test_unknown_error(self):
        """Test handling of unknown SQL errors."""
        error_text = "Some random SQL error that doesn't match patterns"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unknown_sql_error')
        self.assertEqual(result.severity, 'medium')
    
    def test_chinese_formatting(self):
        """Test Chinese language formatting."""
        error_text = "Syntax error near 'FORM'"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='zh')
        
        self.assertIn('SQL 錯誤', formatted)
        self.assertIn('智能建議', formatted)
    
    def test_english_formatting(self):
        """Test English language formatting."""
        error_text = "Syntax error near 'FORM'"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='en')
        
        self.assertIn('SQL Error', formatted)
        self.assertIn('Smart Suggestions', formatted)


class TestSQLAnalyzerIntegration(unittest.TestCase):
    """Integration tests for SQL analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SQLAnalyzer()
    
    def test_real_world_mysql_errors(self):
        """Test with real-world MySQL error messages."""
        real_errors = [
            {
                'text': "ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'FORM users WHERE id = 5' at line 1",
                'expected_type': 'syntax_error',
                'expected_dialect': 'mysql',
                'expected_line': 1
            },
            {
                'text': "ERROR 1146 (42S02): Table 'mydb.users' doesn't exist",
                'expected_type': 'missing_table',
                'expected_dialect': 'mysql'
            },
            {
                'text': "ERROR 1062 (23000): Duplicate entry 'john@example.com' for key 'users.email'",
                'expected_type': 'constraint_violation',
                'expected_dialect': 'mysql'
            }
        ]
        
        for scenario in real_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                
                if 'expected_dialect' in scenario:
                    self.assertEqual(result.sql_dialect, scenario['expected_dialect'])
                if 'expected_line' in scenario:
                    self.assertEqual(result.line, scenario['expected_line'])
    
    def test_real_world_postgresql_errors(self):
        """Test with real-world PostgreSQL error messages."""
        real_errors = [
            {
                'text': 'ERROR:  column "username" of relation "users" does not exist\nLINE 1: INSERT INTO users (username, email) VALUES ($1, $2)\n                           ^',
                'expected_type': 'missing_column',
                'expected_dialect': 'postgresql',
                'expected_line': 1
            },
            {
                'text': 'ERROR:  relation "products" does not exist at character 15',
                'expected_type': 'missing_table',
                'expected_dialect': 'postgresql'
            },
            {
                'text': 'FATAL:  password authentication failed for user "postgres"',
                'expected_type': 'authentication_failed',
                'expected_dialect': 'postgresql'
            }
        ]
        
        for scenario in real_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                self.assertEqual(result.sql_dialect, scenario['expected_dialect'])
                
                if 'expected_line' in scenario:
                    self.assertEqual(result.line, scenario['expected_line'])
    
    def test_suggestion_quality(self):
        """Test that suggestions are relevant and helpful."""
        error_text = "Table 'users' doesn't exist"
        result = self.analyzer.analyze(error_text)
        
        # Check that suggestions exist and have required fields
        self.assertTrue(len(result.suggestions) > 0)
        for suggestion in result.suggestions:
            self.assertIn('title', suggestion)
            self.assertIn('code', suggestion)
            self.assertIn('confidence', suggestion)
            self.assertGreater(suggestion['confidence'], 0)
            self.assertLessEqual(suggestion['confidence'], 1)
    
    def test_orm_error_patterns(self):
        """Test ORM-specific error patterns."""
        error_text = "N+1 query problem detected in User.posts relationship"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'n_plus_one')
        self.assertEqual(result.severity, 'medium')
        # Check that ORM-specific suggestions are provided
        self.assertTrue(any('eager' in str(s).lower() for s in result.suggestions))
    
    def test_performance(self):
        """Test analyzer performance with multiple errors."""
        import time
        
        errors = [
            "Syntax error near 'SELECT'",
            "Unknown column 'id' in field list",
            "Table 'users' doesn't exist",
            "Duplicate key violation",
            "Permission denied",
            "Connection refused",
            "Query timeout"
        ] * 20  # Test with 140 errors
        
        start_time = time.time()
        for error in errors:
            self.analyzer.analyze(error)
        end_time = time.time()
        
        # Should analyze 140 errors in less than 1 second
        self.assertLess(end_time - start_time, 1.0)
    
    def test_complex_multi_line_errors(self):
        """Test handling of complex multi-line error messages."""
        error_text = """ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that 
corresponds to your MySQL server version for the right syntax to use near 
'FORM users u 
  LEFT JOIN orders o ON u.id = o.user_id 
  WHERE u.status = 'active'' at line 3"""
        
        result = self.analyzer.analyze(error_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'syntax_error')
        self.assertEqual(result.line, 3)
        self.assertEqual(result.sql_dialect, 'mysql')


if __name__ == '__main__':
    unittest.main()