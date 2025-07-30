"""SQL language error analyzer for CCDebugger."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SQLError:
    """Represents a SQL error with analysis."""
    error_type: str
    message: str
    sql_dialect: Optional[str] = None
    line: Optional[int] = None
    position: Optional[int] = None
    severity: str = "high"
    suggestions: List[Dict[str, any]] = None
    explanation: Optional[str] = None
    

class SQLAnalyzer:
    """Analyzer for SQL language errors."""
    
    # Common SQL syntax error patterns
    SYNTAX_PATTERNS = {
        'syntax_error': {
            'pattern': r"(?:syntax error|SQL syntax|parse error)",
            'severity': 'high',
            'explanation': "SQL syntax error detected. Check for typos, missing keywords, or incorrect syntax.",
            'suggestions': [
                {
                    'title': 'Check SQL syntax structure',
                    'code': 'SELECT column1, column2\nFROM table_name\nWHERE condition;',
                    'confidence': 0.85
                },
                {
                    'title': 'Verify quotes and delimiters',
                    'code': "-- Use single quotes for strings\nWHERE name = 'value'\n\n-- Use backticks/quotes for identifiers\nSELECT `column name` FROM table",
                    'confidence': 0.80
                }
            ]
        },
        'missing_column': {
            'pattern': r"(?:Unknown column|Column .+ (?:does not exist|doesn't exist)|no such column)",
            'severity': 'high',
            'explanation': "The specified column does not exist in the table.",
            'suggestions': [
                {
                    'title': 'List available columns',
                    'code': '-- MySQL/MariaDB\nSHOW COLUMNS FROM table_name;\n\n-- PostgreSQL\n\\d table_name',
                    'confidence': 0.90
                },
                {
                    'title': 'Check column name spelling',
                    'code': '-- Column names are case-sensitive in some databases',
                    'confidence': 0.85
                }
            ]
        },
        'missing_table': {
            'pattern': r"(?:Table .+ (?:does not exist|doesn't exist)|no such table|relation .+ does not exist)",
            'severity': 'high',
            'explanation': "The specified table does not exist in the database.",
            'suggestions': [
                {
                    'title': 'List available tables',
                    'code': '-- MySQL/MariaDB\nSHOW TABLES;\n\n-- PostgreSQL\n\\dt\n\n-- SQLite\n.tables',
                    'confidence': 0.90
                },
                {
                    'title': 'Check database/schema context',
                    'code': '-- Ensure correct database\nUSE database_name;\n\n-- Or use fully qualified name\nSELECT * FROM database.schema.table;',
                    'confidence': 0.85
                }
            ]
        },
        'type_mismatch': {
            'pattern': r"(?:type mismatch|invalid input syntax|cannot convert|data type mismatch)",
            'severity': 'high',
            'explanation': "Data type mismatch between provided value and expected column type.",
            'suggestions': [
                {
                    'title': 'Use proper type conversion',
                    'code': "-- Cast to correct type\nCAST(value AS INTEGER)\nCAST(value AS VARCHAR(255))\nTO_DATE('2025-01-29', 'YYYY-MM-DD')",
                    'confidence': 0.90
                },
                {
                    'title': 'Check column data types',
                    'code': '-- View table structure\nDESCRIBE table_name;\n\n-- PostgreSQL\n\\d+ table_name',
                    'confidence': 0.85
                }
            ]
        },
        'constraint_violation': {
            'pattern': r"(?:constraint|violation|duplicate (?:key|entry)|foreign key|unique constraint|check constraint)",
            'severity': 'high',
            'explanation': "Database constraint violation detected.",
            'suggestions': [
                {
                    'title': 'Handle duplicate key errors',
                    'code': '-- Use INSERT IGNORE (MySQL)\nINSERT IGNORE INTO table VALUES (...);\n\n-- Use ON CONFLICT (PostgreSQL)\nINSERT INTO table VALUES (...)\nON CONFLICT (id) DO NOTHING;',
                    'confidence': 0.85
                },
                {
                    'title': 'Check foreign key relationships',
                    'code': '-- Ensure parent record exists\nSELECT * FROM parent_table WHERE id = ?;\n\n-- Or disable checks temporarily\nSET foreign_key_checks = 0;',
                    'confidence': 0.80
                }
            ]
        },
        'permission_denied': {
            'pattern': r"(?:permission denied|insufficient privileges)",
            'severity': 'critical',
            'explanation': "User does not have required permissions for this operation.",
            'suggestions': [
                {
                    'title': 'Grant necessary permissions',
                    'code': "-- Grant specific permissions\nGRANT SELECT, INSERT ON database.table TO 'user'@'host';\n\n-- Grant all permissions\nGRANT ALL PRIVILEGES ON database.* TO 'user'@'host';",
                    'confidence': 0.90
                },
                {
                    'title': 'Check current permissions',
                    'code': "-- MySQL\nSHOW GRANTS FOR CURRENT_USER();\n\n-- PostgreSQL\n\\du",
                    'confidence': 0.85
                }
            ]
        },
        'deadlock': {
            'pattern': r"(?:deadlock|lock wait timeout|transaction.*aborted)",
            'severity': 'critical',
            'explanation': "Database deadlock or lock timeout occurred.",
            'suggestions': [
                {
                    'title': 'Retry transaction',
                    'code': '-- Implement retry logic\nBEGIN;\n-- Your queries here\nCOMMIT;\n-- On deadlock, wait and retry',
                    'confidence': 0.85
                },
                {
                    'title': 'Optimize transaction order',
                    'code': '-- Access tables in consistent order\n-- Keep transactions short\n-- Use appropriate isolation level\nSET TRANSACTION ISOLATION LEVEL READ COMMITTED;',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # Connection error patterns
    CONNECTION_PATTERNS = {
        'connection_refused': {
            'pattern': r"(?:Connection refused|could not connect|Can't connect to)",
            'severity': 'critical',
            'explanation': "Cannot establish connection to database server.",
            'suggestions': [
                {
                    'title': 'Check database server status',
                    'code': '# MySQL\nsudo systemctl status mysql\n\n# PostgreSQL\nsudo systemctl status postgresql',
                    'confidence': 0.90
                },
                {
                    'title': 'Verify connection parameters',
                    'code': "# Test connection\nmysql -h hostname -P port -u username -p\n\n# Or\npsql -h hostname -p port -U username -d database",
                    'confidence': 0.85
                }
            ]
        },
        'authentication_failed': {
            'pattern': r"(?:authentication failed|password authentication failed|Access denied for user|access denied.*using password)",
            'severity': 'critical',
            'explanation': "Authentication failed. Check username and password.",
            'suggestions': [
                {
                    'title': 'Reset user password',
                    'code': "-- MySQL\nALTER USER 'username'@'host' IDENTIFIED BY 'new_password';\n\n-- PostgreSQL\nALTER USER username PASSWORD 'new_password';",
                    'confidence': 0.85
                },
                {
                    'title': 'Check user host restrictions',
                    'code': "-- MySQL: Check allowed hosts\nSELECT user, host FROM mysql.user WHERE user = 'username';",
                    'confidence': 0.80
                }
            ]
        },
        'database_not_found': {
            'pattern': r"(?:database .+ does not exist|Unknown database|FATAL: database)",
            'severity': 'high',
            'explanation': "The specified database does not exist.",
            'suggestions': [
                {
                    'title': 'Create database',
                    'code': '-- Create database\nCREATE DATABASE database_name;\n\n-- With encoding (PostgreSQL)\nCREATE DATABASE database_name ENCODING \'UTF8\';',
                    'confidence': 0.90
                },
                {
                    'title': 'List available databases',
                    'code': '-- MySQL\nSHOW DATABASES;\n\n-- PostgreSQL\n\\l',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    # Query optimization patterns
    OPTIMIZATION_PATTERNS = {
        'slow_query': {
            'pattern': r"(?:Query execution was interrupted|maximum statement execution time|query timeout)",
            'severity': 'medium',
            'explanation': "Query is taking too long to execute.",
            'suggestions': [
                {
                    'title': 'Add indexes for WHERE/JOIN columns',
                    'code': '-- Create index\nCREATE INDEX idx_column ON table(column);\n\n-- Composite index\nCREATE INDEX idx_multi ON table(col1, col2);',
                    'confidence': 0.90
                },
                {
                    'title': 'Use EXPLAIN to analyze query',
                    'code': '-- MySQL\nEXPLAIN SELECT * FROM table WHERE condition;\n\n-- PostgreSQL\nEXPLAIN ANALYZE SELECT * FROM table WHERE condition;',
                    'confidence': 0.95
                }
            ]
        },
        'missing_index': {
            'pattern': r"(?:full table scan|using filesort|using temporary)",
            'severity': 'medium',
            'explanation': "Query performance could be improved with proper indexing.",
            'suggestions': [
                {
                    'title': 'Identify missing indexes',
                    'code': '-- Check slow query log\n-- Look for queries without index usage\n-- Use performance schema',
                    'confidence': 0.85
                },
                {
                    'title': 'Monitor index usage',
                    'code': '-- MySQL: Check index usage\nSELECT * FROM sys.schema_unused_indexes;',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # ORM-specific patterns
    ORM_PATTERNS = {
        'n_plus_one': {
            'pattern': r"(?:N\+1|multiple queries|lazy loading)",
            'severity': 'medium',
            'explanation': "N+1 query problem detected. Use eager loading to optimize.",
            'suggestions': [
                {
                    'title': 'Use JOIN to eager load',
                    'code': '-- Instead of multiple queries\nSELECT * FROM posts;\nSELECT * FROM comments WHERE post_id = ?;\n\n-- Use JOIN\nSELECT p.*, c.*\nFROM posts p\nLEFT JOIN comments c ON p.id = c.post_id;',
                    'confidence': 0.90
                },
                {
                    'title': 'ORM eager loading examples',
                    'code': '# Django\nPost.objects.prefetch_related(\'comments\')\n\n# SQLAlchemy\nsession.query(Post).options(joinedload(Post.comments))',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize the SQL analyzer."""
        # Order matters - more specific patterns should be checked first
        self.all_patterns = {
            **self.CONNECTION_PATTERNS,  # Check connection patterns first (includes auth)
            **self.SYNTAX_PATTERNS,
            **self.OPTIMIZATION_PATTERNS,
            **self.ORM_PATTERNS
        }
    
    def analyze(self, error_text: str) -> Optional[SQLError]:
        """Analyze SQL error text and return structured analysis."""
        if not error_text:
            return None
            
        # Detect SQL dialect if possible
        dialect = self._detect_dialect(error_text)
        
        # Extract line/position information if present
        line_info = self._extract_line_info(error_text)
        
        # Try to match against known patterns
        for error_type, config in self.all_patterns.items():
            pattern = config['pattern']
            match = re.search(pattern, error_text, re.MULTILINE | re.IGNORECASE)
            
            if match:
                return SQLError(
                    error_type=error_type,
                    message=error_text,
                    sql_dialect=dialect,
                    line=line_info.get('line'),
                    position=line_info.get('position'),
                    severity=config['severity'],
                    suggestions=config['suggestions'],
                    explanation=config['explanation']
                )
        
        # Generic SQL error if no pattern matches
        return SQLError(
            error_type='unknown_sql_error',
            message=error_text,
            sql_dialect=dialect,
            line=line_info.get('line'),
            position=line_info.get('position'),
            severity='medium',
            explanation="This appears to be a SQL error, but doesn't match common patterns."
        )
    
    def _detect_dialect(self, error_text: str) -> Optional[str]:
        """Detect SQL dialect from error message."""
        # Check for specific error code patterns first
        if re.search(r'ERROR \d{4}', error_text):  # MySQL error codes
            return 'mysql'
        if re.search(r'ERROR:', error_text) and 'LINE' in error_text:  # PostgreSQL format
            return 'postgresql'
        if re.search(r'FATAL:', error_text):  # PostgreSQL fatal errors
            return 'postgresql'
        
        dialect_indicators = {
            'mysql': ['MySQL', 'mysqld', 'MyISAM', 'InnoDB', 'ERROR 1'],
            'postgresql': ['PostgreSQL', 'psql', 'pg_', 'postgres', 'relation'],
            'sqlite': ['SQLite', 'sqlite3'],
            'mssql': ['SQL Server', 'MSSQL', 'Transact-SQL'],
            'oracle': ['Oracle', 'ORA-', 'PL/SQL']
        }
        
        error_lower = error_text.lower()
        for dialect, indicators in dialect_indicators.items():
            if any(ind.lower() in error_lower for ind in indicators):
                return dialect
        
        return None
    
    def _extract_line_info(self, error_text: str) -> Dict[str, any]:
        """Extract line and position information from error text."""
        info = {}
        
        # Common patterns for line numbers
        line_patterns = [
            r'line (\d+)',
            r'LINE (\d+)',
            r':(\d+):',
            r'at line (\d+)'
        ]
        
        for pattern in line_patterns:
            match = re.search(pattern, error_text)
            if match:
                info['line'] = int(match.group(1))
                break
        
        # Position/column patterns
        pos_patterns = [
            r'position (\d+)',
            r'column (\d+)',
            r':\d+:(\d+)'
        ]
        
        for pattern in pos_patterns:
            match = re.search(pattern, error_text)
            if match:
                info['position'] = int(match.group(1))
                break
        
        return info
    
    def format_suggestions(self, error: SQLError, language: str = 'en') -> str:
        """Format error analysis for display."""
        if language == 'zh':
            output = f"🚨 SQL 錯誤 - {error.severity.upper()} 優先級\n\n"
            output += f"錯誤類型: {error.error_type}\n"
            if error.sql_dialect:
                output += f"SQL 方言: {error.sql_dialect.upper()}\n"
            if error.line:
                output += f"行號: {error.line}"
                if error.position:
                    output += f", 位置: {error.position}"
                output += "\n"
            output += f"\n說明: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 智能建議:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (信心度: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```sql\n{suggestion['code']}\n```\n"
        else:
            output = f"🚨 SQL Error - {error.severity.upper()} Priority\n\n"
            output += f"Error Type: {error.error_type}\n"
            if error.sql_dialect:
                output += f"SQL Dialect: {error.sql_dialect.upper()}\n"
            if error.line:
                output += f"Line: {error.line}"
                if error.position:
                    output += f", Position: {error.position}"
                output += "\n"
            output += f"\nExplanation: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 Smart Suggestions:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (Confidence: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```sql\n{suggestion['code']}\n```\n"
        
        return output


# Example usage
if __name__ == "__main__":
    analyzer = SQLAnalyzer()
    
    # Test cases
    test_errors = [
        "You have an error in your SQL syntax near 'FORM users'",
        "ERROR 1054: Unknown column 'username' in 'field list'",
        "Table 'database.users' doesn't exist",
        "Duplicate entry 'john@example.com' for key 'email'",
        "ERROR 1045: Access denied for user 'root'@'localhost' (using password: YES)",
        "Query execution was interrupted, maximum statement execution time exceeded"
    ]
    
    for error_text in test_errors:
        result = analyzer.analyze(error_text)
        if result:
            print(analyzer.format_suggestions(result))
            print("-" * 80)