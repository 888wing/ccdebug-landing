"""Swift language error analyzer for CCDebugger."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SwiftError:
    """Represents a Swift error with analysis."""
    error_type: str
    message: str
    file_path: Optional[str] = None
    line: Optional[int] = None
    severity: str = "high"
    suggestions: List[Dict[str, any]] = None
    explanation: Optional[str] = None
    

class SwiftAnalyzer:
    """Analyzer for Swift language errors."""
    
    # Common Swift error patterns
    ERROR_PATTERNS = {
        'nil_unwrap': {
            'pattern': r"Fatal error: Unexpectedly found nil while (?:implicitly )?unwrapping an Optional value",
            'severity': 'critical',
            'explanation': "You're trying to force unwrap an optional that contains nil. This is one of the most common Swift runtime errors.",
            'suggestions': [
                {
                    'title': 'Use optional binding (if let)',
                    'code': 'if let value = optionalValue {\n    // Use value safely\n}',
                    'confidence': 0.95
                },
                {
                    'title': 'Use nil-coalescing operator (??)',
                    'code': 'let value = optionalValue ?? defaultValue',
                    'confidence': 0.90
                },
                {
                    'title': 'Use guard statement',
                    'code': 'guard let value = optionalValue else { return }',
                    'confidence': 0.85
                }
            ]
        },
        'type_mismatch': {
            'pattern': r"Cannot convert value of type '(.+)' to expected argument type '(.+)'",
            'severity': 'high',
            'explanation': "Type mismatch error. Swift's type system is strict and doesn't allow implicit conversions.",
            'suggestions': [
                {
                    'title': 'Explicit type casting',
                    'code': 'as? TargetType // Safe casting\nas! TargetType // Force casting (use carefully)',
                    'confidence': 0.85
                },
                {
                    'title': 'Check type compatibility',
                    'code': 'if let converted = value as? TargetType {\n    // Use converted value\n}',
                    'confidence': 0.80
                }
            ]
        },
        'array_bounds': {
            'pattern': r"Fatal error: Index out of range",
            'severity': 'critical',
            'explanation': "Attempting to access an array element at an index that doesn't exist.",
            'suggestions': [
                {
                    'title': 'Check array bounds',
                    'code': 'if index < array.count {\n    let element = array[index]\n}',
                    'confidence': 0.95
                },
                {
                    'title': 'Use safe subscript',
                    'code': 'array.indices.contains(index) ? array[index] : nil',
                    'confidence': 0.90
                },
                {
                    'title': 'Use first/last properties',
                    'code': 'array.first // Safe access to first element\narray.last  // Safe access to last element',
                    'confidence': 0.85
                }
            ]
        },
        'protocol_conformance': {
            'pattern': r"Type '(.+)' does not conform to protocol '(.+)'",
            'severity': 'high',
            'explanation': "The type doesn't implement all required methods/properties of the protocol.",
            'suggestions': [
                {
                    'title': 'Implement required protocol methods',
                    'code': 'extension YourType: ProtocolName {\n    // Implement required methods\n}',
                    'confidence': 0.90
                },
                {
                    'title': 'Check protocol requirements',
                    'code': '// Add missing methods/properties required by the protocol',
                    'confidence': 0.85
                }
            ]
        },
        'memory_access': {
            'pattern': r"Simultaneous accesses to .+, but modification requires exclusive access",
            'severity': 'critical',
            'explanation': "Swift's memory safety prevents simultaneous access to the same memory location.",
            'suggestions': [
                {
                    'title': 'Use temporary variable',
                    'code': 'let temp = value\n// Modify temp instead of original',
                    'confidence': 0.85
                },
                {
                    'title': 'Restructure code to avoid simultaneous access',
                    'code': '// Separate read and write operations',
                    'confidence': 0.80
                }
            ]
        },
        'swiftui_state': {
            'pattern': r"Accessing State's value outside of being installed on a View",
            'severity': 'high',
            'explanation': "SwiftUI @State can only be accessed within the view's body or methods called from body.",
            'suggestions': [
                {
                    'title': 'Access @State in View body',
                    'code': 'var body: some View {\n    Text(stateVariable) // Access here\n}',
                    'confidence': 0.90
                },
                {
                    'title': 'Use @Binding for child views',
                    'code': '@Binding var value: String // In child view',
                    'confidence': 0.85
                }
            ]
        },
        'async_await': {
            'pattern': r"'async' call in a function that does not support concurrency",
            'severity': 'high',
            'explanation': "Async functions must be called from async contexts.",
            'suggestions': [
                {
                    'title': 'Use Task to call async function',
                    'code': 'Task {\n    await asyncFunction()\n}',
                    'confidence': 0.95
                },
                {
                    'title': 'Make calling function async',
                    'code': 'func yourFunction() async {\n    await asyncFunction()\n}',
                    'confidence': 0.90
                }
            ]
        }
    }
    
    # Xcode-specific error patterns
    XCODE_PATTERNS = {
        'module_not_found': {
            'pattern': r"No such module '(.+)'",
            'severity': 'high',
            'explanation': "The specified module/framework cannot be found.",
            'suggestions': [
                {
                    'title': 'Check package dependencies',
                    'code': '// In Package.swift or Xcode project settings',
                    'confidence': 0.85
                },
                {
                    'title': 'Import correct module name',
                    'code': 'import ModuleName // Check spelling and case',
                    'confidence': 0.80
                }
            ]
        },
        'linker_error': {
            'pattern': r"Undefined symbols for architecture",
            'severity': 'critical',
            'explanation': "Linker cannot find the implementation of referenced symbols.",
            'suggestions': [
                {
                    'title': 'Add missing framework',
                    'code': '// Add framework in Build Phases > Link Binary With Libraries',
                    'confidence': 0.85
                },
                {
                    'title': 'Check target membership',
                    'code': '// Ensure files are included in correct target',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize the Swift analyzer."""
        self.all_patterns = {**self.ERROR_PATTERNS, **self.XCODE_PATTERNS}
    
    def analyze(self, error_text: str) -> Optional[SwiftError]:
        """Analyze Swift error text and return structured analysis."""
        if not error_text:
            return None
            
        # Extract file and line information if present
        file_info = self._extract_file_info(error_text)
        
        # Try to match against known patterns
        for error_type, config in self.all_patterns.items():
            pattern = config['pattern']
            match = re.search(pattern, error_text, re.MULTILINE | re.IGNORECASE)
            
            if match:
                return SwiftError(
                    error_type=error_type,
                    message=error_text,
                    file_path=file_info.get('file'),
                    line=file_info.get('line'),
                    severity=config['severity'],
                    suggestions=config['suggestions'],
                    explanation=config['explanation']
                )
        
        # Generic Swift error if no pattern matches
        return SwiftError(
            error_type='unknown_swift_error',
            message=error_text,
            file_path=file_info.get('file'),
            line=file_info.get('line'),
            severity='medium',
            explanation="This appears to be a Swift error, but doesn't match common patterns."
        )
    
    def _extract_file_info(self, error_text: str) -> Dict[str, any]:
        """Extract file path and line number from error text."""
        info = {}
        
        # Common Swift error format: "File.swift:42:10: error:"
        file_pattern = r'([^\s]+\.swift):(\d+):'
        match = re.search(file_pattern, error_text)
        
        if match:
            info['file'] = match.group(1)
            info['line'] = int(match.group(2))
        
        return info
    
    def format_suggestions(self, error: SwiftError, language: str = 'en') -> str:
        """Format error analysis for display."""
        if language == 'zh':
            output = f"🚨 Swift 錯誤 - {error.severity.upper()} 優先級\n\n"
            output += f"錯誤類型: {error.error_type}\n"
            if error.file_path:
                output += f"文件: {error.file_path}"
                if error.line:
                    output += f" (第 {error.line} 行)"
                output += "\n"
            output += f"\n說明: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 智能建議:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (信心度: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```swift\n{suggestion['code']}\n```\n"
        else:
            output = f"🚨 Swift Error - {error.severity.upper()} Priority\n\n"
            output += f"Error Type: {error.error_type}\n"
            if error.file_path:
                output += f"File: {error.file_path}"
                if error.line:
                    output += f" (Line {error.line})"
                output += "\n"
            output += f"\nExplanation: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 Smart Suggestions:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (Confidence: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```swift\n{suggestion['code']}\n```\n"
        
        return output


# Example usage
if __name__ == "__main__":
    analyzer = SwiftAnalyzer()
    
    # Test cases
    test_errors = [
        "Fatal error: Unexpectedly found nil while unwrapping an Optional value",
        "Cannot convert value of type 'String' to expected argument type 'Int'",
        "Fatal error: Index out of range",
        "Type 'MyClass' does not conform to protocol 'Codable'"
    ]
    
    for error_text in test_errors:
        result = analyzer.analyze(error_text)
        if result:
            print(analyzer.format_suggestions(result))
            print("-" * 80)