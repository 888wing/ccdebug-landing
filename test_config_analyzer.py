"""Test cases for YAML/JSON configuration error analyzer."""

import unittest
from config_analyzer import ConfigAnalyzer, ConfigError


class TestConfigAnalyzer(unittest.TestCase):
    """Test Config analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ConfigAnalyzer()
    
    def test_yaml_indentation(self):
        """Test YAML indentation error detection."""
        test_cases = [
            "YAML error: inconsistent indentation at line 10",
            "while scanning a simple key: found character that cannot start any token",
            "bad indentation of a mapping entry at line 5, column 7"
        ]
        
        for error_text in test_cases:
            with self.subTest(error=error_text):
                result = self.analyzer.analyze(error_text)
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, 'yaml_indentation')
                self.assertEqual(result.severity, 'high')
                self.assertTrue(len(result.suggestions) > 0)
    
    def test_yaml_syntax_error(self):
        """Test YAML syntax error detection."""
        test_cases = [
            "yaml.scanner.ScannerError: while scanning for the next token",
            "yaml.parser.ParserError: expected '<document start>', but found '<block mapping start>'",
            "YAML error: could not find expected ':' at line 15"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'yaml_syntax_error')
            self.assertEqual(result.severity, 'high')
    
    def test_yaml_duplicate_key(self):
        """Test YAML duplicate key error detection."""
        test_cases = [
            "YAML error: found duplicate key 'services' at line 20",
            "duplicate key error in config.yaml",
            "key 'name' already defined at line 10"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'yaml_duplicate_key')
            self.assertEqual(result.severity, 'high')
    
    def test_yaml_invalid_value(self):
        """Test YAML invalid value error detection."""
        test_cases = [
            "expected string but found boolean",
            "invalid value type at line 25",
            "could not determine a constructor for the tag '!!python/object'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'yaml_invalid_value')
            self.assertEqual(result.severity, 'medium')
    
    def test_json_parse_error(self):
        """Test JSON parse error detection."""
        test_cases = [
            "JSON.parse: Unexpected token } at position 45",
            "SyntaxError: Unexpected token < in JSON at position 0",
            "Expected property name but found '}'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'json_parse_error')
            self.assertEqual(result.severity, 'high')
    
    def test_json_trailing_comma(self):
        """Test JSON trailing comma error detection."""
        test_cases = [
            "Unexpected token } - trailing comma not allowed",
            "JSON error: trailing comma at line 15",
            "Expected string after comma but found '}'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'json_trailing_comma')
            self.assertEqual(result.severity, 'high')
    
    def test_json_single_quotes(self):
        """Test JSON single quotes error detection."""
        test_cases = [
            "Unexpected token ' at position 12",
            "Single quotes not allowed in JSON",
            "Expected double-quoted property name"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'json_single_quotes')
            self.assertEqual(result.severity, 'high')
    
    def test_json_unquoted_key(self):
        """Test JSON unquoted key error detection."""
        test_cases = [
            "Expecting property name enclosed in double quotes",
            "Expected string but found identifier",
            "Unquoted key 'name' at line 5"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'json_unquoted_key')
            self.assertEqual(result.severity, 'high')
    
    def test_k8s_api_version(self):
        """Test Kubernetes API version error detection."""
        test_cases = [
            "error validating data: unknown api version \"apps/v1beta1\"",
            "no matches for kind \"Deployment\" in version \"extensions/v1beta1\"",
            "could not find api version for Ingress",
            "apiVersion networking.k8s.io/v1beta1 is not available"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'k8s_api_version')
            self.assertEqual(result.severity, 'high')
    
    def test_k8s_missing_required(self):
        """Test Kubernetes missing required field error detection."""
        test_cases = [
            "error validating data: missing required field \"selector\" in io.k8s.api.apps.v1.DeploymentSpec",
            "required key 'metadata' not found",
            "Deployment.spec must specify replicas",
            "Container must specify image"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'k8s_missing_required')
            self.assertEqual(result.severity, 'high')
    
    def test_k8s_invalid_resource(self):
        """Test Kubernetes invalid resource error detection."""
        test_cases = [
            "error validating data: unknown field \"replicaCount\" in io.k8s.api.apps.v1.Deployment",
            "ValidationError(Deployment.spec): invalid type for io.k8s.api.apps.v1.DeploymentSpec",
            "cannot unmarshal string into Go value of type int32"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'k8s_invalid_resource')
            self.assertEqual(result.severity, 'medium')
    
    def test_github_actions_syntax(self):
        """Test GitHub Actions syntax error detection."""
        test_cases = [
            "workflow syntax error at line 10",
            "invalid workflow file: .github/workflows/ci.yml",
            "error in workflow: unexpected value 'ons'",
            "action.yml syntax error: invalid input"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'github_actions_syntax')
            self.assertEqual(result.severity, 'high')
    
    def test_gitlab_ci_syntax(self):
        """Test GitLab CI syntax error detection."""
        test_cases = [
            ".gitlab-ci.yml: jobs:test config should be a hash",
            "Invalid configuration format",
            "yaml invalid: mapping values are not allowed in this context"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'gitlab_ci_syntax')
            self.assertEqual(result.severity, 'high')
    
    def test_circleci_config(self):
        """Test CircleCI config error detection."""
        test_cases = [
            "Error in config file .circleci/config.yml",
            "Schema error in circle.yml: version not specified",
            "Invalid config: job 'build' must have a steps key"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'circleci_config')
            self.assertEqual(result.severity, 'high')
    
    def test_schema_validation_failed(self):
        """Test schema validation error detection."""
        test_cases = [
            "schema validation failed: #/version: expected string, but got number",
            "ValidationError: does not match schema",
            "schema error: required property 'name' not found"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'schema_validation_failed')
            self.assertEqual(result.severity, 'high')
    
    def test_invalid_reference(self):
        """Test invalid reference error detection."""
        test_cases = [
            "reference '*defaults' not found",
            "cannot resolve $ref: #/definitions/Service",
            "undefined reference to anchor 'base'",
            "broken reference: file not found"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'invalid_reference')
            self.assertEqual(result.severity, 'medium')
    
    def test_config_type_detection(self):
        """Test configuration type detection."""
        test_cases = [
            ("yaml: line 10: syntax error", "yaml"),
            ("JSON.parse error at position 45", "json"),
            ("kubectl apply: error validating data", "k8s"),
            ("github workflow syntax error", "github"),
            (".gitlab-ci.yml: invalid configuration", "gitlab"),
            ("circleci config validation failed", "circleci"),
            ("docker-compose.yml: services must be a mapping", "docker-compose")
        ]
        
        for error_text, expected_type in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.config_type, expected_type)
    
    def test_file_info_extraction(self):
        """Test file path, line and column extraction."""
        test_cases = [
            ("config.yaml:10:5: syntax error", "config.yaml", 10, 5),
            ("error in deployment.yml at line 25", "deployment.yml", 25, None),
            ("line 15, column 3: invalid indentation", None, 15, 3),
            ("app.json: line 42:8 - unexpected token", "app.json", 42, 8)
        ]
        
        for error_text, expected_file, expected_line, expected_column in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            if expected_file:
                self.assertEqual(result.file_path, expected_file)
            if expected_line:
                self.assertEqual(result.line, expected_line)
            if expected_column:
                self.assertEqual(result.column, expected_column)
    
    def test_unknown_error(self):
        """Test handling of unknown configuration errors."""
        error_text = "Some random config error that doesn't match patterns"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unknown_config_error')
        self.assertEqual(result.severity, 'medium')
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_chinese_formatting(self):
        """Test Chinese language formatting."""
        error_text = "yaml: line 10: found duplicate key 'services'"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='zh')
        
        self.assertIn('配置錯誤', formatted)
        self.assertIn('智能建議', formatted)
        self.assertIn('YAML', formatted)
    
    def test_english_formatting(self):
        """Test English language formatting."""
        error_text = "JSON.parse: Unexpected token }"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='en')
        
        self.assertIn('Configuration Error', formatted)
        self.assertIn('Smart Suggestions', formatted)
        self.assertIn('JSON', formatted)


class TestConfigAnalyzerIntegration(unittest.TestCase):
    """Integration tests for Config analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ConfigAnalyzer()
    
    def test_real_world_yaml_errors(self):
        """Test with real-world YAML configuration errors."""
        real_errors = [
            {
                'text': """while parsing a block mapping
  in "docker-compose.yml", line 3, column 1
expected <block end>, but found '<block mapping start>'
  in "docker-compose.yml", line 5, column 3""",
                'expected_type': 'yaml_syntax_error',
                'expected_file': 'docker-compose.yml',
                'expected_config_type': 'yaml'
            },
            {
                'text': "Error: YAML parse error on deployment.yaml: error converting YAML to JSON: yaml: line 25: found duplicate key \"replicas\"",
                'expected_type': 'yaml_duplicate_key',
                'expected_line': 25
            },
            {
                'text': "Error from server (BadRequest): error when creating \"service.yaml\": Service in version \"v1\" cannot be handled as a Service: v1.Service.Spec: v1.ServiceSpec.Ports: []v1.ServicePort: v1.ServicePort.TargetPort: Name: \"\", Port: 0",
                'expected_type': 'k8s_invalid_resource',
                'expected_config_type': 'k8s'
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
                if 'expected_config_type' in scenario:
                    self.assertEqual(result.config_type, scenario['expected_config_type'])
    
    def test_real_world_json_errors(self):
        """Test with real-world JSON configuration errors."""
        json_errors = [
            {
                'text': "Unexpected token } in JSON at position 156\n    at JSON.parse (<anonymous>)\n    at parse (index.js:10:15)",
                'expected_type': 'json_parse_error'
            },
            {
                'text': "Error: Parse error on line 10:\n...\"dependencies\": {},}\n---------------------^\nExpecting 'EOF', got '}'",
                'expected_type': 'json_trailing_comma',
                'expected_line': 10
            },
            {
                'text': "SyntaxError: JSON5: invalid character 'n' at 1:2",
                'expected_type': 'json_parse_error'
            }
        ]
        
        for scenario in json_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                
                if 'expected_line' in scenario:
                    self.assertEqual(result.line, scenario['expected_line'])
    
    def test_ci_cd_config_errors(self):
        """Test CI/CD configuration errors."""
        cicd_errors = [
            {
                'text': "Error: .github/workflows/ci.yml#L10: invalid workflow file: unexpected value 'ons'",
                'expected_type': 'github_actions_syntax',
                'expected_config_type': 'github'
            },
            {
                'text': "ERROR: Job failed: .gitlab-ci.yml: jobs:test config contains unknown keys: befor_script",
                'expected_type': 'gitlab_ci_syntax',
                'expected_config_type': 'gitlab'
            },
            {
                'text': "CircleCI: Schema error in config.yml: jobs: build: steps: expected array, got string",
                'expected_type': 'circleci_config',
                'expected_config_type': 'circleci'
            }
        ]
        
        for scenario in cicd_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                self.assertEqual(result.config_type, scenario['expected_config_type'])
    
    def test_suggestion_quality(self):
        """Test that suggestions are relevant and helpful."""
        error_text = "yaml: line 10: found duplicate key 'services'"
        result = self.analyzer.analyze(error_text)
        
        # Check that suggestions exist and have required fields
        self.assertTrue(len(result.suggestions) > 0)
        for suggestion in result.suggestions:
            self.assertIn('title', suggestion)
            self.assertIn('code', suggestion)
            self.assertIn('confidence', suggestion)
            self.assertGreater(suggestion['confidence'], 0)
            self.assertLessEqual(suggestion['confidence'], 1)
    
    def test_kubernetes_manifest_errors(self):
        """Test Kubernetes manifest specific errors."""
        k8s_error = """error validating data: [ValidationError(Deployment.spec): missing required field "selector" in io.k8s.api.apps.v1.DeploymentSpec, ValidationError(Deployment.spec.template.spec.containers[0]): missing required field "image" in io.k8s.api.core.v1.Container]"""
        
        result = self.analyzer.analyze(k8s_error)
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'k8s_missing_required')
        self.assertEqual(result.config_type, 'k8s')
        # Should provide suggestions about required fields
        self.assertTrue(any('required fields' in str(s).lower() for s in result.suggestions))
    
    def test_multi_line_yaml_errors(self):
        """Test multi-line YAML error messages."""
        yaml_error = """yaml.scanner.ScannerError: while scanning a simple key
  in "config.yaml", line 15, column 1
could not find expected ':'
  in "config.yaml", line 16, column 11"""
        
        result = self.analyzer.analyze(yaml_error)
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'yaml_syntax_error')
        self.assertEqual(result.file_path, 'config.yaml')
        self.assertEqual(result.line, 15)
        self.assertEqual(result.config_type, 'yaml')
    
    def test_performance(self):
        """Test analyzer performance with multiple errors."""
        import time
        
        errors = [
            "yaml: syntax error",
            "JSON.parse: unexpected token",
            "k8s: unknown api version",
            "gitlab-ci.yml: invalid",
            "schema validation failed",
            "reference not found"
        ] * 20  # Test with 120 errors
        
        start_time = time.time()
        for error in errors:
            self.analyzer.analyze(error)
        end_time = time.time()
        
        # Should analyze 120 errors in less than 1 second
        self.assertLess(end_time - start_time, 1.0)


if __name__ == '__main__':
    unittest.main()