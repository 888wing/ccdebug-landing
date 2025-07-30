"""Shell/Bash language error analyzer for CCDebugger."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ShellError:
    """Represents a Shell/Bash error with analysis."""
    error_type: str
    message: str
    script_path: Optional[str] = None
    line: Optional[int] = None
    command: Optional[str] = None
    severity: str = "high"
    suggestions: List[Dict[str, any]] = None
    explanation: Optional[str] = None
    

class ShellAnalyzer:
    """Analyzer for Shell/Bash script errors."""
    
    # Common Shell/Bash syntax error patterns
    SYNTAX_PATTERNS = {
        'syntax_error': {
            'pattern': r"(?:syntax error|unexpected token|unexpected end of file)",
            'severity': 'high',
            'explanation': "Shell syntax error detected. Check for missing quotes, brackets, or keywords.",
            'suggestions': [
                {
                    'title': 'Check syntax structure',
                    'code': '#!/bin/bash\n# Correct syntax examples\nif [ "$var" = "value" ]; then\n    echo "Match"\nfi',
                    'confidence': 0.85
                },
                {
                    'title': 'Verify quotes and brackets',
                    'code': '# Use proper quoting\nvar="value with spaces"\n# Always quote variables\nif [ "$var" = "test" ]; then',
                    'confidence': 0.80
                }
            ]
        },
        'command_not_found': {
            'pattern': r"(?:command not found|No such file or directory)",
            'severity': 'high',
            'explanation': "The specified command or file was not found.",
            'suggestions': [
                {
                    'title': 'Check if command is installed',
                    'code': '# Check if command exists\nwhich command_name\n# Or use command -v\ncommand -v command_name',
                    'confidence': 0.90
                },
                {
                    'title': 'Check PATH variable',
                    'code': '# View current PATH\necho $PATH\n# Add directory to PATH\nexport PATH="$PATH:/new/directory"',
                    'confidence': 0.85
                },
                {
                    'title': 'Use full path to command',
                    'code': '# Use absolute path\n/usr/bin/command\n# Or find command location\nwhich command',
                    'confidence': 0.80
                }
            ]
        },
        'permission_denied': {
            'pattern': r"(?:Permission denied|Operation not permitted)",
            'severity': 'high',
            'explanation': "Insufficient permissions to execute the command or access the file.",
            'suggestions': [
                {
                    'title': 'Check file permissions',
                    'code': '# View permissions\nls -la file.sh\n# Make script executable\nchmod +x script.sh',
                    'confidence': 0.95
                },
                {
                    'title': 'Use sudo if needed',
                    'code': '# Run with elevated privileges\nsudo command\n# Or change ownership\nsudo chown user:group file',
                    'confidence': 0.85
                }
            ]
        },
        'unbound_variable': {
            'pattern': r"(?:unbound variable|parameter not set)",
            'severity': 'medium',
            'explanation': "Attempting to use an undefined variable. This often happens with 'set -u' enabled.",
            'suggestions': [
                {
                    'title': 'Initialize variable',
                    'code': '# Set default value\nvar="${VAR:-default}"\n# Or check if set\nif [ -z "${VAR+x}" ]; then\n    VAR="default"\nfi',
                    'confidence': 0.90
                },
                {
                    'title': 'Use parameter expansion',
                    'code': '# Default value if unset\n${var:-default}\n# Default and assign if unset\n${var:=default}',
                    'confidence': 0.85
                }
            ]
        },
        'bad_substitution': {
            'pattern': r"bad substitution",
            'severity': 'high',
            'explanation': "Invalid variable substitution syntax.",
            'suggestions': [
                {
                    'title': 'Check variable syntax',
                    'code': '# Correct syntax\n${variable}\n${array[index]}\n${variable:-default}',
                    'confidence': 0.85
                },
                {
                    'title': 'Use compatible shell',
                    'code': '#!/bin/bash\n# Some features require bash\n# Not available in sh',
                    'confidence': 0.80
                }
            ]
        },
        'integer_expression_expected': {
            'pattern': r"integer expression expected",
            'severity': 'medium',
            'explanation': "A non-integer value was provided where an integer was expected.",
            'suggestions': [
                {
                    'title': 'Use arithmetic expansion',
                    'code': '# For arithmetic operations\nresult=$((num1 + num2))\n# Or use let\nlet "result = num1 + num2"',
                    'confidence': 0.90
                },
                {
                    'title': 'Validate numeric input',
                    'code': '# Check if variable is numeric\nif [[ "$var" =~ ^[0-9]+$ ]]; then\n    echo "Valid number"\nfi',
                    'confidence': 0.85
                }
            ]
        },
        'too_many_arguments': {
            'pattern': r"too many arguments",
            'severity': 'medium',
            'explanation': "Too many arguments provided to a command or test expression.",
            'suggestions': [
                {
                    'title': 'Quote variables properly',
                    'code': '# Always quote variables in tests\nif [ "$var" = "value with spaces" ]; then\n    echo "Match"\nfi',
                    'confidence': 0.95
                },
                {
                    'title': 'Use [[ ]] for complex tests',
                    'code': '# Bash extended test\nif [[ $var == pattern* ]]; then\n    echo "Pattern match"\nfi',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    # File and I/O error patterns
    IO_PATTERNS = {
        'no_such_file': {
            'pattern': r"No such file or directory",
            'severity': 'high',
            'explanation': "The specified file or directory does not exist.",
            'suggestions': [
                {
                    'title': 'Check file existence',
                    'code': '# Test if file exists\nif [ -f "file.txt" ]; then\n    cat file.txt\nfi',
                    'confidence': 0.90
                },
                {
                    'title': 'Create missing directory',
                    'code': '# Create directory if missing\nmkdir -p /path/to/directory',
                    'confidence': 0.85
                }
            ]
        },
        'cannot_overwrite': {
            'pattern': r"(?:cannot overwrite|File exists)",
            'severity': 'medium',
            'explanation': "Cannot overwrite existing file.",
            'suggestions': [
                {
                    'title': 'Use noclobber option',
                    'code': '# Enable noclobber\nset -C\n# Force overwrite\ncommand >| file.txt',
                    'confidence': 0.85
                },
                {
                    'title': 'Check before writing',
                    'code': '# Backup existing file\nif [ -f "file.txt" ]; then\n    mv file.txt file.txt.bak\nfi',
                    'confidence': 0.80
                }
            ]
        },
        'broken_pipe': {
            'pattern': r"Broken pipe",
            'severity': 'medium',
            'explanation': "The process reading from the pipe terminated before reading all data.",
            'suggestions': [
                {
                    'title': 'Handle SIGPIPE',
                    'code': '# Ignore broken pipe\ntrap "" PIPE\n# Or handle gracefully\ntrap "echo Pipeline broken" PIPE',
                    'confidence': 0.85
                },
                {
                    'title': 'Check pipeline components',
                    'code': '# Use pipefail option\nset -o pipefail\n# Check pipeline status\ncommand1 | command2\necho ${PIPESTATUS[@]}',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # Loop and control flow patterns
    CONTROL_PATTERNS = {
        'unexpected_token_near': {
            'pattern': r"syntax error near unexpected token",
            'severity': 'high',
            'explanation': "Syntax error in control structure (if, for, while, etc).",
            'suggestions': [
                {
                    'title': 'Check control structure syntax',
                    'code': '# Correct if statement\nif [ condition ]; then\n    commands\nelif [ condition ]; then\n    commands\nelse\n    commands\nfi',
                    'confidence': 0.90
                },
                {
                    'title': 'Verify loop syntax',
                    'code': '# For loop\nfor i in {1..10}; do\n    echo $i\ndone\n\n# While loop\nwhile [ condition ]; do\n    commands\ndone',
                    'confidence': 0.85
                }
            ]
        },
        'missing_keyword': {
            'pattern': r"(?:unexpected EOF while looking for matching|missing [`'\"])",
            'severity': 'high',
            'explanation': "Missing closing keyword or bracket in control structure.",
            'suggestions': [
                {
                    'title': 'Check matching keywords',
                    'code': '# Every if needs fi\nif [ test ]; then\n    echo "test"\nfi\n\n# Every case needs esac\ncase $var in\n    pattern) commands ;;\nesac',
                    'confidence': 0.95
                },
                {
                    'title': 'Verify bracket matching',
                    'code': '# Match all brackets\n{ command1; command2; }\n( subshell commands )\n[[ test expression ]]',
                    'confidence': 0.90
                }
            ]
        }
    }
    
    # Array and string manipulation patterns
    ARRAY_PATTERNS = {
        'array_subscript': {
            'pattern': r"(?:bad array subscript|invalid subscript)",
            'severity': 'medium',
            'explanation': "Invalid array index or subscript.",
            'suggestions': [
                {
                    'title': 'Use proper array syntax',
                    'code': '# Declare array\narr=(element1 element2 element3)\n# Access elements\necho ${arr[0]}\n# Get all elements\necho ${arr[@]}',
                    'confidence': 0.90
                },
                {
                    'title': 'Check array bounds',
                    'code': '# Get array length\nlength=${#arr[@]}\n# Safe access\nif [ $index -lt $length ]; then\n    echo ${arr[$index]}\nfi',
                    'confidence': 0.85
                }
            ]
        },
        'substring_expansion': {
            'pattern': r"substring expression",
            'severity': 'medium',
            'explanation': "Error in substring expansion syntax.",
            'suggestions': [
                {
                    'title': 'Use correct substring syntax',
                    'code': '# Substring expansion\nstr="Hello World"\n# From position 6\necho ${str:6}\n# From position 0, length 5\necho ${str:0:5}',
                    'confidence': 0.85
                },
                {
                    'title': 'String manipulation',
                    'code': '# Remove prefix\n${var#prefix}\n# Remove suffix\n${var%suffix}\n# Replace\n${var/old/new}',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # Special shell features
    SPECIAL_PATTERNS = {
        'set_e_error': {
            'pattern': r"(?:set -e|errexit)",
            'severity': 'high',
            'explanation': "Script exited due to 'set -e' (exit on error) being enabled.",
            'suggestions': [
                {
                    'title': 'Handle expected failures',
                    'code': '# Allow specific command to fail\ncommand_that_might_fail || true\n# Or check return code\nif ! command; then\n    handle_error\nfi',
                    'confidence': 0.90
                },
                {
                    'title': 'Use error handling',
                    'code': '# Trap errors\ntrap \'echo "Error on line $LINENO"\' ERR\n# Custom error handler\nerror_handler() {\n    echo "Error: $1"\n    exit 1\n}',
                    'confidence': 0.85
                }
            ]
        },
        'function_not_found': {
            'pattern': r"(?:function|procedure) not found",
            'severity': 'high',
            'explanation': "Attempting to call an undefined function.",
            'suggestions': [
                {
                    'title': 'Define function before use',
                    'code': '# Function definition\nmy_function() {\n    echo "Function called"\n}\n# Call function\nmy_function',
                    'confidence': 0.95
                },
                {
                    'title': 'Source function file',
                    'code': '# Source external functions\nsource functions.sh\n# Or use dot notation\n. ./functions.sh',
                    'confidence': 0.90
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize the Shell analyzer."""
        # Order matters - more specific patterns should be checked first
        self.all_patterns = {
            **self.CONTROL_PATTERNS,  # Check control patterns first (more specific)
            **self.IO_PATTERNS,       # Then IO patterns
            **self.ARRAY_PATTERNS,    # Then array patterns
            **self.SPECIAL_PATTERNS,  # Then special patterns
            **self.SYNTAX_PATTERNS    # Finally general syntax patterns
        }
    
    def analyze(self, error_text: str) -> Optional[ShellError]:
        """Analyze Shell/Bash error text and return structured analysis."""
        if not error_text:
            return None
            
        # Extract script and line information if present
        script_info = self._extract_script_info(error_text)
        
        # Extract command if present
        command = self._extract_command(error_text)
        
        # Try to match against known patterns
        for error_type, config in self.all_patterns.items():
            pattern = config['pattern']
            match = re.search(pattern, error_text, re.MULTILINE | re.IGNORECASE)
            
            if match:
                return ShellError(
                    error_type=error_type,
                    message=error_text,
                    script_path=script_info.get('script'),
                    line=script_info.get('line'),
                    command=command,
                    severity=config['severity'],
                    suggestions=config['suggestions'],
                    explanation=config['explanation']
                )
        
        # Generic Shell error if no pattern matches
        return ShellError(
            error_type='unknown_shell_error',
            message=error_text,
            script_path=script_info.get('script'),
            line=script_info.get('line'),
            command=command,
            severity='medium',
            explanation="This appears to be a Shell/Bash error, but doesn't match common patterns.",
            suggestions=[
                {
                    'title': 'Check shell syntax',
                    'code': '# Verify script syntax\nbash -n script.sh\n# Or use shellcheck\nshellcheck script.sh',
                    'confidence': 0.5
                },
                {
                    'title': 'Enable debug mode',
                    'code': '# Run with debug output\nbash -x script.sh\n# Or add to script\nset -x',
                    'confidence': 0.5
                }
            ]
        )
    
    def _extract_script_info(self, error_text: str) -> Dict[str, any]:
        """Extract script path and line number from error text."""
        info = {}
        
        # Common patterns for script:line format
        patterns = [
            r'([^:]+\.sh):(\d+):',  # script.sh:42:
            r'([^:]+): line (\d+):',  # script: line 42:
            r'line (\d+) of ([^:]+)',  # line 42 of script.sh
            r'"([^"]+)", line (\d+)'  # "script.sh", line 42
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_text)
            if match:
                if 'line' in pattern and 'of' in pattern:
                    info['line'] = int(match.group(1))
                    info['script'] = match.group(2)
                elif '"' in pattern:
                    info['script'] = match.group(1)
                    info['line'] = int(match.group(2))
                else:
                    info['script'] = match.group(1)
                    info['line'] = int(match.group(2))
                break
        
        return info
    
    def _extract_command(self, error_text: str) -> Optional[str]:
        """Extract the command that caused the error."""
        # Look for command in quotes or after colon
        patterns = [
            r"[`']([^`']+)[`']",  # Command in backticks or quotes
            r": ([^:]+)$",  # After last colon
            r"^([^:]+):",  # Before first colon
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_text, re.MULTILINE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def format_suggestions(self, error: ShellError, language: str = 'en') -> str:
        """Format error analysis for display."""
        if language == 'zh':
            output = f"🚨 Shell/Bash 錯誤 - {error.severity.upper()} 優先級\n\n"
            output += f"錯誤類型: {error.error_type}\n"
            if error.script_path:
                output += f"腳本: {error.script_path}"
                if error.line:
                    output += f" (第 {error.line} 行)"
                output += "\n"
            if error.command:
                output += f"命令: {error.command}\n"
            output += f"\n說明: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 智能建議:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (信心度: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```bash\n{suggestion['code']}\n```\n"
        else:
            output = f"🚨 Shell/Bash Error - {error.severity.upper()} Priority\n\n"
            output += f"Error Type: {error.error_type}\n"
            if error.script_path:
                output += f"Script: {error.script_path}"
                if error.line:
                    output += f" (Line {error.line})"
                output += "\n"
            if error.command:
                output += f"Command: {error.command}\n"
            output += f"\nExplanation: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 Smart Suggestions:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (Confidence: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```bash\n{suggestion['code']}\n```\n"
        
        return output


# Example usage
if __name__ == "__main__":
    analyzer = ShellAnalyzer()
    
    # Test cases
    test_errors = [
        "./script.sh: line 10: syntax error near unexpected token `}'",
        "bash: command not found: gitx",
        "Permission denied: /usr/local/bin/script",
        "./deploy.sh: line 5: VAR: unbound variable",
        "bad substitution",
        "./test.sh: line 15: [: too many arguments"
    ]
    
    for error_text in test_errors:
        result = analyzer.analyze(error_text)
        if result:
            print(analyzer.format_suggestions(result))
            print("-" * 80)