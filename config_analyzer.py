"""YAML/JSON configuration error analyzer for CCDebugger."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ConfigError:
    """Represents a YAML/JSON configuration error with analysis."""
    error_type: str
    message: str
    file_path: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    config_type: Optional[str] = None  # yaml, json, k8s, ci/cd
    severity: str = "high"
    suggestions: List[Dict[str, any]] = None
    explanation: Optional[str] = None
    

class ConfigAnalyzer:
    """Analyzer for YAML/JSON configuration errors."""
    
    # YAML syntax error patterns
    YAML_PATTERNS = {
        'yaml_indentation': {
            'pattern': r"(?:inconsistent indentation|bad indentation|found character .+ that cannot start any token|indentation|while scanning.*found character)",
            'severity': 'high',
            'explanation': "YAML indentation error. YAML requires consistent indentation with spaces.",
            'suggestions': [
                {
                    'title': 'Use consistent indentation',
                    'code': '# Use 2 spaces for each level\nparent:\n  child:\n    grandchild: value\n\n# NOT tabs or mixed spaces',
                    'confidence': 0.95
                },
                {
                    'title': 'Configure editor for YAML',
                    'code': '# .editorconfig\n[*.{yml,yaml}]\nindent_style = space\nindent_size = 2',
                    'confidence': 0.85
                }
            ]
        },
        'yaml_syntax_error': {
            'pattern': r"(?:yaml|yml).+(?:scanner|parser|could not find expected|mapping values|while scanning|while parsing|expected .+ but found)",
            'severity': 'high',
            'explanation': "YAML syntax error. Check for missing colons, quotes, or structural issues.",
            'suggestions': [
                {
                    'title': 'Check YAML syntax rules',
                    'code': '# Valid YAML syntax\nkey: value\nlist:\n  - item1\n  - item2\nmapping:\n  key1: value1\n  key2: value2',
                    'confidence': 0.90
                },
                {
                    'title': 'Quote special characters',
                    'code': '# Quote strings with special chars\nspecial: "value: with colon"\nversion: "1.0"  # Numbers as strings\nboolean: "yes"  # Not interpreted as bool',
                    'confidence': 0.85
                }
            ]
        },
        'yaml_duplicate_key': {
            'pattern': r"(?:duplicate key|found duplicate key|key .+ already defined)",
            'severity': 'high',
            'explanation': "Duplicate key found in YAML. Each key must be unique within its scope.",
            'suggestions': [
                {
                    'title': 'Remove or rename duplicate keys',
                    'code': '# Each key must be unique\nservices:\n  web: {...}\n  api: {...}  # Different name\n  # web: {...}  # Would be duplicate',
                    'confidence': 0.95
                },
                {
                    'title': 'Use arrays for multiple values',
                    'code': '# For multiple similar items\nservers:\n  - name: server1\n    host: host1\n  - name: server2\n    host: host2',
                    'confidence': 0.90
                }
            ]
        },
        'yaml_invalid_value': {
            'pattern': r"(?:expected .+ but found|invalid value|could not determine a constructor)",
            'severity': 'medium',
            'explanation': "Invalid value type or format in YAML.",
            'suggestions': [
                {
                    'title': 'Check value types',
                    'code': '# Common YAML values\nstring: "text"\nnumber: 123\nfloat: 12.34\nboolean: true\nnull_value: null\narray: [1, 2, 3]',
                    'confidence': 0.85
                },
                {
                    'title': 'Use proper boolean values',
                    'code': '# YAML booleans\nenabled: true   # or yes, on\ndisabled: false # or no, off\n# NOT "true" (string)',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # JSON syntax error patterns
    JSON_PATTERNS = {
        'json_parse_error': {
            'pattern': r"(?:JSON\.parse.*Unexpected token|SyntaxError.*JSON|Parse error.*JSON|JSON5:)",
            'severity': 'high',
            'explanation': "JSON parsing error. Check for syntax issues like missing commas or quotes.",
            'suggestions': [
                {
                    'title': 'Validate JSON syntax',
                    'code': '{\n  "key": "value",\n  "number": 123,\n  "array": [1, 2, 3],\n  "nested": {\n    "key": "value"\n  }\n}',
                    'confidence': 0.90
                },
                {
                    'title': 'Common JSON fixes',
                    'code': '// Check for:\n// - Missing commas between items\n// - Trailing commas (not allowed)\n// - Single quotes (use double)\n// - Unquoted keys',
                    'confidence': 0.85
                }
            ]
        },
        'json_trailing_comma': {
            'pattern': r"(?:trailing comma|Expecting 'EOF', got '}')",
            'severity': 'high',
            'explanation': "JSON does not allow trailing commas.",
            'suggestions': [
                {
                    'title': 'Remove trailing comma',
                    'code': '// Correct:\n{\n  "key1": "value1",\n  "key2": "value2"\n}\n\n// Incorrect:\n{\n  "key1": "value1",\n  "key2": "value2",  // <- trailing comma\n}',
                    'confidence': 0.95
                }
            ]
        },
        'json_single_quotes': {
            'pattern': r"(?:Unexpected token '|Single quotes not allowed|Expected double-quoted property)",
            'severity': 'high',
            'explanation': "JSON requires double quotes, not single quotes.",
            'suggestions': [
                {
                    'title': 'Use double quotes',
                    'code': '// Correct:\n{\n  "key": "value"\n}\n\n// Incorrect:\n{\n  \'key\': \'value\'\n}',
                    'confidence': 0.95
                }
            ]
        },
        'json_unquoted_key': {
            'pattern': r"(?:Expecting property name enclosed|Expected string but found identifier|Unquoted key)",
            'severity': 'high',
            'explanation': "JSON keys must be quoted strings.",
            'suggestions': [
                {
                    'title': 'Quote all keys',
                    'code': '// Correct:\n{\n  "name": "value",\n  "count": 123\n}\n\n// Incorrect:\n{\n  name: "value",\n  count: 123\n}',
                    'confidence': 0.95
                }
            ]
        }
    }
    
    # Kubernetes configuration patterns
    K8S_PATTERNS = {
        'k8s_api_version': {
            'pattern': r"(?:unknown api version|no matches for kind|could not find api|apiVersion .+ is not available)",
            'severity': 'high',
            'explanation': "Invalid or unsupported Kubernetes API version.",
            'suggestions': [
                {
                    'title': 'Use correct API version',
                    'code': '# Common API versions\napiVersion: v1  # Pod, Service, ConfigMap\napiVersion: apps/v1  # Deployment, StatefulSet\napiVersion: batch/v1  # Job\napiVersion: networking.k8s.io/v1  # Ingress',
                    'confidence': 0.90
                },
                {
                    'title': 'Check cluster version',
                    'code': '# Check available APIs\nkubectl api-versions\n\n# Check specific resource\nkubectl explain deployment.apiVersion',
                    'confidence': 0.85
                }
            ]
        },
        'k8s_missing_required': {
            'pattern': r"(?:missing required field|required key .+ not found|must specify|is required)",
            'severity': 'high',
            'explanation': "Required field missing in Kubernetes configuration.",
            'suggestions': [
                {
                    'title': 'Add required fields',
                    'code': '# Minimal required fields\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: my-app\nspec:\n  replicas: 1\n  selector:\n    matchLabels:\n      app: my-app\n  template:\n    metadata:\n      labels:\n        app: my-app\n    spec:\n      containers:\n      - name: app\n        image: myimage:latest',
                    'confidence': 0.90
                }
            ]
        },
        'k8s_invalid_resource': {
            'pattern': r"(?:unknown field|ValidationError|invalid type|cannot unmarshal)",
            'severity': 'medium',
            'explanation': "Invalid field or value in Kubernetes resource.",
            'suggestions': [
                {
                    'title': 'Validate resource schema',
                    'code': '# Validate before applying\nkubectl apply --dry-run=client -f config.yaml\n\n# Explain resource fields\nkubectl explain deployment.spec',
                    'confidence': 0.85
                },
                {
                    'title': 'Check field names',
                    'code': '# Common mistakes\n# replica: 3  # Wrong\nreplicas: 3  # Correct\n\n# container:  # Wrong  \ncontainers:  # Correct',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # CI/CD configuration patterns
    CICD_PATTERNS = {
        'github_actions_syntax': {
            'pattern': r"(?:workflow syntax|invalid workflow file|error in workflow|action.yml)",
            'severity': 'high',
            'explanation': "GitHub Actions workflow syntax error.",
            'suggestions': [
                {
                    'title': 'Check workflow syntax',
                    'code': 'name: CI\non:\n  push:\n    branches: [ main ]\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Run tests\n        run: npm test',
                    'confidence': 0.90
                },
                {
                    'title': 'Validate locally',
                    'code': '# Use act to test locally\nact -n  # Dry run\n\n# Or GitHub CLI\ngh workflow view',
                    'confidence': 0.80
                }
            ]
        },
        'gitlab_ci_syntax': {
            'pattern': r"(?:gitlab-ci\.yml|jobs:.+ config|Invalid configuration|yaml invalid|\.gitlab-ci)",
            'severity': 'high',
            'explanation': "GitLab CI configuration error.",
            'suggestions': [
                {
                    'title': 'Check .gitlab-ci.yml syntax',
                    'code': 'stages:\n  - build\n  - test\n  - deploy\n\nbuild-job:\n  stage: build\n  script:\n    - echo "Building..."\n    - npm install\n    - npm run build',
                    'confidence': 0.90
                },
                {
                    'title': 'Use CI Lint tool',
                    'code': '# Validate in GitLab UI:\n# Project > CI/CD > CI Lint\n\n# Or use GitLab API',
                    'confidence': 0.85
                }
            ]
        },
        'circleci_config': {
            'pattern': r"(?:\.circleci|circle\.yml|circleci.*config|Invalid config.*job|Schema error.*circle)",
            'severity': 'high',
            'explanation': "CircleCI configuration error.",
            'suggestions': [
                {
                    'title': 'Check CircleCI config',
                    'code': 'version: 2.1\njobs:\n  build:\n    docker:\n      - image: cimg/node:16.0\n    steps:\n      - checkout\n      - run: npm install\n      - run: npm test',
                    'confidence': 0.85
                },
                {
                    'title': 'Validate config',
                    'code': '# Use CircleCI CLI\ncircleci config validate\n\n# Pack and process\ncircleci config process .circleci/config.yml',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    # Schema validation patterns
    SCHEMA_PATTERNS = {
        'schema_validation_failed': {
            'pattern': r"(?:schema validation|does not match schema|ValidationError|schema error|Schema error)",
            'severity': 'high',
            'explanation': "Configuration does not match expected schema.",
            'suggestions': [
                {
                    'title': 'Check schema requirements',
                    'code': '# Validate against schema\n# For JSON Schema\najv validate -s schema.json -d config.json\n\n# For YAML\nyamllint config.yaml',
                    'confidence': 0.85
                },
                {
                    'title': 'Review schema documentation',
                    'code': '# Common schema issues:\n# - Missing required fields\n# - Wrong data types\n# - Invalid enum values\n# - Pattern mismatches',
                    'confidence': 0.80
                }
            ]
        },
        'invalid_reference': {
            'pattern': r"(?:reference .+ not found|cannot resolve|undefined reference|broken reference)",
            'severity': 'medium',
            'explanation': "Configuration contains invalid reference or link.",
            'suggestions': [
                {
                    'title': 'Check references',
                    'code': '# YAML anchors and aliases\ndefaults: &defaults\n  timeout: 30\n  retries: 3\n\njob1:\n  <<: *defaults\n  script: test.sh',
                    'confidence': 0.85
                },
                {
                    'title': 'Verify external references',
                    'code': '# Check file paths\ninclude: ./common/base.yaml\n\n# Check URLs\nimage: registry.com/namespace/image:tag',
                    'confidence': 0.80
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize the Config analyzer."""
        # Order patterns for better matching - more specific patterns first
        self.all_patterns = {}
        
        # Add patterns in order of specificity
        # Schema patterns first (very specific)
        self.all_patterns.update(self.SCHEMA_PATTERNS)
        
        # CI/CD patterns (domain-specific)
        self.all_patterns.update(self.CICD_PATTERNS)
        
        # K8s patterns (domain-specific)
        self.all_patterns.update(self.K8S_PATTERNS)
        
        # JSON patterns (more specific than YAML)
        # Reorder JSON patterns - more specific first
        json_ordered = {
            'json_trailing_comma': self.JSON_PATTERNS['json_trailing_comma'],
            'json_single_quotes': self.JSON_PATTERNS['json_single_quotes'],
            'json_unquoted_key': self.JSON_PATTERNS['json_unquoted_key'],
            'json_parse_error': self.JSON_PATTERNS['json_parse_error'],
        }
        self.all_patterns.update(json_ordered)
        
        # YAML patterns (general)
        self.all_patterns.update(self.YAML_PATTERNS)
    
    def analyze(self, error_text: str) -> Optional[ConfigError]:
        """Analyze configuration error text and return structured analysis."""
        if not error_text:
            return None
            
        # Detect configuration type
        config_type = self._detect_config_type(error_text)
        
        # Extract file and position information
        file_info = self._extract_file_info(error_text)
        
        # Try to match against known patterns
        for error_type, config in self.all_patterns.items():
            pattern = config['pattern']
            match = re.search(pattern, error_text, re.MULTILINE | re.IGNORECASE)
            
            if match:
                return ConfigError(
                    error_type=error_type,
                    message=error_text,
                    file_path=file_info.get('file'),
                    line=file_info.get('line'),
                    column=file_info.get('column'),
                    config_type=config_type,
                    severity=config['severity'],
                    suggestions=config['suggestions'],
                    explanation=config['explanation']
                )
        
        # Generic config error if no pattern matches
        return ConfigError(
            error_type='unknown_config_error',
            message=error_text,
            file_path=file_info.get('file'),
            line=file_info.get('line'),
            column=file_info.get('column'),
            config_type=config_type,
            severity='medium',
            explanation="This appears to be a configuration error, but doesn't match common patterns.",
            suggestions=[
                {
                    'title': 'Validate configuration syntax',
                    'code': '# For YAML\nyamllint config.yaml\n\n# For JSON\njq . config.json\n\n# Online validators also available',
                    'confidence': 0.5
                },
                {
                    'title': 'Check configuration documentation',
                    'code': '# Review the official documentation\n# for your specific tool/platform',
                    'confidence': 0.5
                }
            ]
        )
    
    def _detect_config_type(self, error_text: str) -> Optional[str]:
        """Detect the type of configuration from error text."""
        # Check more specific types before generic ones
        config_indicators = [
            ('k8s', ['kubernetes', 'k8s', 'kubectl', 'apiVersion', 'kind:', 'ValidationError', 'io.k8s']),
            ('github', ['github', 'workflow', 'actions/', '.github/workflows']),
            ('gitlab', ['gitlab', '.gitlab-ci', 'gitlab-ci.yml']),
            ('circleci', ['circleci', 'circle.yml', '.circleci']),
            ('docker-compose', ['docker-compose', 'compose.yml', 'compose.yaml']),
            ('json', ['json', 'JSON.parse', '.json', 'JSON5']),
            ('yaml', ['yaml', 'yml', '.yaml', '.yml'])
        ]
        
        error_lower = error_text.lower()
        for config_type, indicators in config_indicators:
            if any(ind.lower() in error_lower for ind in indicators):
                return config_type
        
        return None
    
    def _extract_file_info(self, error_text: str) -> Dict[str, any]:
        """Extract file path, line and column from error text."""
        info = {}
        
        # Common patterns for file:line:column
        patterns = [
            r'"([^"]+\.(?:ya?ml|json))".*?line (\d+)',  # "file.yaml" at line 10
            r'error in ([^:\s]+\.(?:ya?ml|json)) at line (\d+)',  # error in file.yaml at line 10 (check before generic)
            r'([^:\s]+\.(?:ya?ml|json)):(\d+):(\d+)',  # file.yaml:10:5 (simple)
            r'([^:\s]+\.(?:ya?ml|json)): line (\d+):(\d+)',  # file.yaml: line 10:5
            r'(?:in |at |from )"([^"]+\.(?:ya?ml|json))":(\d+):(\d+)',  # in "file.yaml":10:5
            r'(?:in |at |from )([^:\s]+\.(?:ya?ml|json)):(\d+):(\d+)',  # in file.yaml:10:5
            r'(?:in |at |from )"([^"]+\.(?:ya?ml|json))" at line (\d+)',  # in "file.yaml" at line 10
            r'line (\d+), column (\d+)',  # line 10, column 5
            r'line (\d+):(\d+)',  # line 10:5
            r':(\d+):(\d+)',  # :10:5
            r'at line (\d+)',  # at line 10
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_text, re.IGNORECASE | re.MULTILINE)
            if match:
                groups = match.groups()
                if len(groups) == 3 and '.' in groups[0]:  # file:line:column
                    info['file'] = groups[0]
                    info['line'] = int(groups[1])
                    info['column'] = int(groups[2])
                elif len(groups) == 2 and groups[0] and '.' in groups[0]:  # file at line
                    info['file'] = groups[0]
                    info['line'] = int(groups[1])
                elif len(groups) == 2 and groups[0].isdigit():  # line, column
                    info['line'] = int(groups[0])
                    info['column'] = int(groups[1])
                elif len(groups) == 1:  # just line
                    info['line'] = int(groups[0])
                break
        
        return info
    
    def format_suggestions(self, error: ConfigError, language: str = 'en') -> str:
        """Format error analysis for display."""
        if language == 'zh':
            output = f"🚨 配置錯誤 - {error.severity.upper()} 優先級\n\n"
            output += f"錯誤類型: {error.error_type}\n"
            if error.config_type:
                output += f"配置類型: {error.config_type.upper()}\n"
            if error.file_path:
                output += f"文件: {error.file_path}"
                if error.line:
                    output += f" (第 {error.line} 行"
                    if error.column:
                        output += f", 第 {error.column} 列"
                    output += ")"
                output += "\n"
            output += f"\n說明: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 智能建議:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (信心度: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```yaml\n{suggestion['code']}\n```\n"
        else:
            output = f"🚨 Configuration Error - {error.severity.upper()} Priority\n\n"
            output += f"Error Type: {error.error_type}\n"
            if error.config_type:
                output += f"Config Type: {error.config_type.upper()}\n"
            if error.file_path:
                output += f"File: {error.file_path}"
                if error.line:
                    output += f" (Line {error.line}"
                    if error.column:
                        output += f", Column {error.column}"
                    output += ")"
                output += "\n"
            output += f"\nExplanation: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 Smart Suggestions:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (Confidence: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```yaml\n{suggestion['code']}\n```\n"
        
        return output


# Example usage
if __name__ == "__main__":
    analyzer = ConfigAnalyzer()
    
    # Test cases
    test_errors = [
        "yaml: line 10: found character that cannot start any token",
        "JSON.parse: Unexpected token } at position 45",
        "Error from server: error validating data: ValidationError(Deployment.spec): missing required field 'selector'",
        "ERROR: Job failed: .gitlab-ci.yml: jobs:test config contains unknown keys: befor_script",
        "Schema validation failed: #/version: expected string, but got number",
        "CircleCI: Schema error: config.yml: jobs: build: steps: expected array"
    ]
    
    for error_text in test_errors:
        result = analyzer.analyze(error_text)
        if result:
            print(analyzer.format_suggestions(result))
            print("-" * 80)