"""Kotlin language error analyzer for CCDebugger."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class KotlinError:
    """Represents a Kotlin error with analysis."""
    error_type: str
    message: str
    file_path: Optional[str] = None
    line: Optional[int] = None
    severity: str = "high"
    suggestions: List[Dict[str, any]] = None
    explanation: Optional[str] = None
    

class KotlinAnalyzer:
    """Analyzer for Kotlin language errors."""
    
    # Common Kotlin error patterns
    ERROR_PATTERNS = {
        'null_pointer': {
            'pattern': r"(?:NullPointerException|NPE|KotlinNullPointerException)",
            'severity': 'critical',
            'explanation': "Null pointer exception occurred. Despite Kotlin's null safety, this can happen with platform types or !! operator.",
            'suggestions': [
                {
                    'title': 'Use safe call operator (?.)',
                    'code': 'object?.method() // Returns null if object is null',
                    'confidence': 0.95
                },
                {
                    'title': 'Use Elvis operator (?:)',
                    'code': 'val result = nullable ?: defaultValue',
                    'confidence': 0.90
                },
                {
                    'title': 'Use let with safe call',
                    'code': 'object?.let { \n    // Use it safely here\n}',
                    'confidence': 0.85
                }
            ]
        },
        'type_mismatch': {
            'pattern': r"Type mismatch: inferred type is (.+) but (.+) was expected",
            'severity': 'high',
            'explanation': "Type mismatch error. Kotlin's type system is strict and doesn't allow implicit conversions.",
            'suggestions': [
                {
                    'title': 'Explicit type conversion',
                    'code': 'value.toInt() // Convert to Int\nvalue.toString() // Convert to String',
                    'confidence': 0.85
                },
                {
                    'title': 'Smart casting',
                    'code': 'if (value is String) {\n    // value is automatically cast to String here\n}',
                    'confidence': 0.80
                }
            ]
        },
        'unresolved_reference': {
            'pattern': r"Unresolved reference: (.+)",
            'severity': 'high',
            'explanation': "The referenced identifier cannot be found in the current scope.",
            'suggestions': [
                {
                    'title': 'Check imports',
                    'code': 'import package.name.ClassName',
                    'confidence': 0.85
                },
                {
                    'title': 'Check spelling and case',
                    'code': '// Kotlin is case-sensitive',
                    'confidence': 0.80
                },
                {
                    'title': 'Check scope and visibility',
                    'code': '// Ensure the member is public or internal',
                    'confidence': 0.75
                }
            ]
        },
        'class_cast': {
            'pattern': r"ClassCastException: .+ cannot be cast to (.+)",
            'severity': 'critical',
            'explanation': "Attempting to cast an object to an incompatible type.",
            'suggestions': [
                {
                    'title': 'Use safe cast (as?)',
                    'code': 'val result = value as? TargetType // Returns null if cast fails',
                    'confidence': 0.95
                },
                {
                    'title': 'Check type before casting',
                    'code': 'if (value is TargetType) {\n    val casted = value // Smart cast\n}',
                    'confidence': 0.90
                }
            ]
        },
        'coroutine_exception': {
            'pattern': r"(?:CoroutineException|Job was cancelled|coroutine)",
            'severity': 'high',
            'explanation': "Exception in Kotlin coroutine. This often happens with improper exception handling in async code.",
            'suggestions': [
                {
                    'title': 'Use CoroutineExceptionHandler',
                    'code': 'val handler = CoroutineExceptionHandler { _, exception ->\n    println("Caught $exception")\n}',
                    'confidence': 0.90
                },
                {
                    'title': 'Use try-catch in coroutine',
                    'code': 'launch {\n    try {\n        // Coroutine code\n    } catch (e: Exception) {\n        // Handle exception\n    }\n}',
                    'confidence': 0.85
                },
                {
                    'title': 'Use supervisorScope',
                    'code': 'supervisorScope {\n    // Child failure won\'t cancel parent\n}',
                    'confidence': 0.80
                }
            ]
        },
        'lateinit_not_initialized': {
            'pattern': r"UninitializedPropertyAccessException: lateinit property (.+) has not been initialized",
            'severity': 'high',
            'explanation': "Accessing a lateinit property before it has been initialized.",
            'suggestions': [
                {
                    'title': 'Check if initialized',
                    'code': 'if (::property.isInitialized) {\n    // Use property safely\n}',
                    'confidence': 0.95
                },
                {
                    'title': 'Initialize in init block',
                    'code': 'init {\n    property = InitialValue()\n}',
                    'confidence': 0.90
                },
                {
                    'title': 'Use nullable type instead',
                    'code': 'private var property: Type? = null',
                    'confidence': 0.85
                }
            ]
        },
        'no_such_element': {
            'pattern': r"NoSuchElementException",
            'severity': 'high',
            'explanation': "Attempting to access an element that doesn't exist in a collection.",
            'suggestions': [
                {
                    'title': 'Use safe access methods',
                    'code': 'list.firstOrNull() // Returns null if empty\nlist.getOrNull(index) // Returns null if out of bounds',
                    'confidence': 0.95
                },
                {
                    'title': 'Check collection before access',
                    'code': 'if (list.isNotEmpty()) {\n    val first = list.first()\n}',
                    'confidence': 0.90
                }
            ]
        },
        'illegal_argument': {
            'pattern': r"IllegalArgumentException: (.+)",
            'severity': 'high',
            'explanation': "Invalid argument passed to a function.",
            'suggestions': [
                {
                    'title': 'Use require() for validation',
                    'code': 'fun process(value: Int) {\n    require(value > 0) { "Value must be positive" }\n}',
                    'confidence': 0.90
                },
                {
                    'title': 'Use check() for state validation',
                    'code': 'check(isInitialized) { "Must be initialized first" }',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    # Android-specific error patterns
    ANDROID_PATTERNS = {
        'activity_not_found': {
            'pattern': r"ActivityNotFoundException",
            'severity': 'high',
            'explanation': "The specified Activity cannot be found. Check your AndroidManifest.xml.",
            'suggestions': [
                {
                    'title': 'Declare Activity in manifest',
                    'code': '<activity android:name=".YourActivity" />',
                    'confidence': 0.90
                },
                {
                    'title': 'Check Intent action',
                    'code': 'if (intent.resolveActivity(packageManager) != null) {\n    startActivity(intent)\n}',
                    'confidence': 0.85
                }
            ]
        },
        'network_on_main_thread': {
            'pattern': r"NetworkOnMainThreadException",
            'severity': 'critical',
            'explanation': "Network operations cannot be performed on the main thread in Android.",
            'suggestions': [
                {
                    'title': 'Use coroutines with IO dispatcher',
                    'code': 'lifecycleScope.launch(Dispatchers.IO) {\n    // Network operation\n}',
                    'confidence': 0.95
                },
                {
                    'title': 'Use suspend function',
                    'code': 'suspend fun fetchData() = withContext(Dispatchers.IO) {\n    // Network call\n}',
                    'confidence': 0.90
                }
            ]
        },
        'view_binding_null': {
            'pattern': r"(?:findViewById|binding\.) .+ must not be null",
            'severity': 'high',
            'explanation': "View binding returned null. The view might not be inflated yet.",
            'suggestions': [
                {
                    'title': 'Use View Binding correctly',
                    'code': 'private var _binding: FragmentBinding? = null\nprivate val binding get() = _binding!!',
                    'confidence': 0.90
                },
                {
                    'title': 'Access views after onViewCreated',
                    'code': 'override fun onViewCreated(view: View, savedInstanceState: Bundle?) {\n    // Safe to access views here\n}',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    # Gradle/build error patterns
    BUILD_PATTERNS = {
        'unresolved_dependency': {
            'pattern': r"Could not resolve (.+)",
            'severity': 'high',
            'explanation': "Gradle cannot resolve the specified dependency.",
            'suggestions': [
                {
                    'title': 'Check dependency notation',
                    'code': 'implementation "group:artifact:version"',
                    'confidence': 0.85
                },
                {
                    'title': 'Add repository',
                    'code': 'repositories {\n    mavenCentral()\n    google()\n}',
                    'confidence': 0.80
                }
            ]
        },
        'duplicate_class': {
            'pattern': r"Duplicate class (.+) found",
            'severity': 'high',
            'explanation': "Duplicate classes found in dependencies.",
            'suggestions': [
                {
                    'title': 'Exclude duplicate module',
                    'code': 'implementation("dependency") {\n    exclude group: "conflicting.group"\n}',
                    'confidence': 0.85
                },
                {
                    'title': 'Use resolution strategy',
                    'code': 'configurations.all {\n    resolutionStrategy {\n        force "group:artifact:version"\n    }\n}',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize the Kotlin analyzer."""
        self.all_patterns = {
            **self.ERROR_PATTERNS, 
            **self.ANDROID_PATTERNS,
            **self.BUILD_PATTERNS
        }
    
    def analyze(self, error_text: str) -> Optional[KotlinError]:
        """Analyze Kotlin error text and return structured analysis."""
        if not error_text:
            return None
            
        # Extract file and line information if present
        file_info = self._extract_file_info(error_text)
        
        # Try to match against known patterns
        for error_type, config in self.all_patterns.items():
            pattern = config['pattern']
            match = re.search(pattern, error_text, re.MULTILINE | re.IGNORECASE)
            
            if match:
                return KotlinError(
                    error_type=error_type,
                    message=error_text,
                    file_path=file_info.get('file'),
                    line=file_info.get('line'),
                    severity=config['severity'],
                    suggestions=config['suggestions'],
                    explanation=config['explanation']
                )
        
        # Generic Kotlin error if no pattern matches
        return KotlinError(
            error_type='unknown_kotlin_error',
            message=error_text,
            file_path=file_info.get('file'),
            line=file_info.get('line'),
            severity='medium',
            explanation="This appears to be a Kotlin error, but doesn't match common patterns."
        )
    
    def _extract_file_info(self, error_text: str) -> Dict[str, any]:
        """Extract file path and line number from error text."""
        info = {}
        
        # Common Kotlin error format: "File.kt:42:10: error:"
        file_pattern = r'([^\s]+\.kt):(\d+):'
        match = re.search(file_pattern, error_text)
        
        if match:
            info['file'] = match.group(1)
            info['line'] = int(match.group(2))
        
        return info
    
    def format_suggestions(self, error: KotlinError, language: str = 'en') -> str:
        """Format error analysis for display."""
        if language == 'zh':
            output = f"🚨 Kotlin 錯誤 - {error.severity.upper()} 優先級\n\n"
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
                        output += f"```kotlin\n{suggestion['code']}\n```\n"
        else:
            output = f"🚨 Kotlin Error - {error.severity.upper()} Priority\n\n"
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
                        output += f"```kotlin\n{suggestion['code']}\n```\n"
        
        return output


# Example usage
if __name__ == "__main__":
    analyzer = KotlinAnalyzer()
    
    # Test cases
    test_errors = [
        "NullPointerException at MainActivity.kt:45",
        "Type mismatch: inferred type is String but Int was expected",
        "Unresolved reference: findViewById",
        "UninitializedPropertyAccessException: lateinit property binding has not been initialized",
        "NetworkOnMainThreadException"
    ]
    
    for error_text in test_errors:
        result = analyzer.analyze(error_text)
        if result:
            print(analyzer.format_suggestions(result))
            print("-" * 80)