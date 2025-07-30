"""Test cases for Docker/Dockerfile error analyzer."""

import unittest
from docker_analyzer import DockerAnalyzer, DockerError


class TestDockerAnalyzer(unittest.TestCase):
    """Test Docker analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = DockerAnalyzer()
    
    def test_invalid_instruction(self):
        """Test invalid Dockerfile instruction detection."""
        test_cases = [
            "Unknown instruction: FRON",
            "Invalid instruction: COPPY",
            "unknown flag: --chow"
        ]
        
        for error_text in test_cases:
            with self.subTest(error=error_text):
                result = self.analyzer.analyze(error_text)
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, 'invalid_instruction')
                self.assertEqual(result.severity, 'high')
                self.assertTrue(len(result.suggestions) > 0)
    
    def test_missing_argument(self):
        """Test missing argument error detection."""
        test_cases = [
            "COPY requires at least 2 arguments",
            "not enough arguments in call to EXPOSE"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'missing_argument')
    
    def test_from_argument_error(self):
        """Test FROM specific argument error."""
        error_text = "FROM requires exactly one argument"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        # This is correctly caught by invalid_from pattern
        self.assertEqual(result.error_type, 'invalid_from')
    
    def test_invalid_from(self):
        """Test invalid FROM instruction detection."""
        test_cases = [
            "invalid reference format",
            "repository name must be lowercase",
            "FROM requires one argument"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'invalid_from')
            self.assertEqual(result.severity, 'high')
    
    def test_copy_failed(self):
        """Test COPY/ADD failure detection."""
        test_cases = [
            "COPY failed: file not found: package.json",
            "failed to compute cache key: not found: app.py",
            "ADD failed: stat /var/lib/docker/tmp/docker-builder123/src: no such file or directory"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'copy_failed')
            self.assertEqual(result.severity, 'high')
    
    def test_run_failed(self):
        """Test RUN instruction failure detection."""
        test_cases = [
            "The command '/bin/sh -c apt-get install vim' returned a non-zero code: 1",
            "executor failed running [/bin/sh -c npm install]: exit code: 1",
            "The command 'npm install' returned a non-zero code: 127"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'run_failed')
    
    def test_container_not_found(self):
        """Test container not found error detection."""
        test_cases = [
            "Error: No such container: myapp",
            "Error response from daemon: Container myapp not found",
            "Could not find container with name or id: web"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'container_not_found')
            self.assertEqual(result.severity, 'medium')
    
    def test_image_not_found(self):
        """Test image not found error detection."""
        test_cases = [
            "Unable to find image 'myapp:latest' locally",
            "pull access denied for myimage, repository does not exist",
            "Error response from daemon: repository myrepo/myimage not found"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'image_not_found')
    
    def test_port_already_allocated(self):
        """Test port allocation error detection."""
        test_cases = [
            "bind: address already in use",
            "Error starting userland proxy: listen tcp4 0.0.0.0:8080: bind: address already in use",
            "port is already allocated"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'port_already_allocated')
            self.assertEqual(result.severity, 'medium')
    
    def test_permission_denied(self):
        """Test permission denied error detection."""
        test_cases = [
            "Got permission denied while trying to connect to the Docker daemon socket",
            "docker: Permission denied",
            "access denied: you do not have permission"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'permission_denied')
            self.assertEqual(result.severity, 'high')
    
    def test_out_of_space(self):
        """Test out of space error detection."""
        test_cases = [
            "no space left on device",
            "Error processing tar file: write /app: disk quota exceeded",
            "failed to register layer: no space left on device"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'out_of_space')
            self.assertEqual(result.severity, 'critical')
    
    def test_invalid_compose_file(self):
        """Test docker-compose YAML error detection."""
        test_cases = [
            "yaml: line 15: did not find expected key",
            "ERROR: yaml.scanner.ScannerError: mapping values are not allowed here",
            "yaml.parser.ParserError: expected '<document start>', but found '<block mapping start>'"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'invalid_compose_file')
    
    def test_service_not_found(self):
        """Test docker-compose service not found error."""
        test_cases = [
            "ERROR: No such service: webapp",
            "ERROR: Service 'database' was not found in docker-compose.yml",
            "No such service: redis"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'service_not_found')
            self.assertEqual(result.severity, 'medium')
    
    def test_network_not_found(self):
        """Test network not found error detection."""
        test_cases = [
            "Error response from daemon: network mynet not found",
            "network custom_network not found",
            "Error response from daemon: network bridge not found"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'network_not_found')
    
    def test_volume_not_found(self):
        """Test volume not found error detection."""
        test_cases = [
            "Error response from daemon: get myvolume: no such volume",
            "volume data_volume not found",
            "Error: No such volume: postgres_data"
        ]
        
        for error_text in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            self.assertEqual(result.error_type, 'volume_not_found')
    
    def test_file_info_extraction(self):
        """Test Dockerfile path and line extraction."""
        test_cases = [
            ("Dockerfile:15: Unknown instruction: FRON", "Dockerfile", 15),
            ("line 42: COPY failed (Dockerfile)", "Dockerfile", 42),
            ('"/app/Dockerfile" at line 10: syntax error', "/app/Dockerfile", 10)
        ]
        
        for error_text, expected_file, expected_line in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            if expected_file:
                self.assertEqual(result.dockerfile_path, expected_file)
            if expected_line:
                self.assertEqual(result.line, expected_line)
    
    def test_instruction_extraction(self):
        """Test Dockerfile instruction extraction."""
        test_cases = [
            ("Unknown instruction: FRON", None),  # FRON is not valid
            ("COPY failed: file not found", "COPY"),
            ("RUN npm install failed", "RUN"),
            ("FROM requires exactly one argument", "FROM")
        ]
        
        for error_text, expected_instruction in test_cases:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            if expected_instruction:
                self.assertEqual(result.instruction, expected_instruction)
    
    def test_unknown_error(self):
        """Test handling of unknown Docker errors."""
        error_text = "Some random Docker error that doesn't match patterns"
        result = self.analyzer.analyze(error_text)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'unknown_docker_error')
        self.assertEqual(result.severity, 'medium')
        self.assertTrue(len(result.suggestions) > 0)
    
    def test_chinese_formatting(self):
        """Test Chinese language formatting."""
        error_text = "COPY failed: file not found: app.js"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='zh')
        
        self.assertIn('Docker 錯誤', formatted)
        self.assertIn('智能建議', formatted)
    
    def test_english_formatting(self):
        """Test English language formatting."""
        error_text = "COPY failed: file not found: app.js"
        result = self.analyzer.analyze(error_text)
        formatted = self.analyzer.format_suggestions(result, language='en')
        
        self.assertIn('Docker Error', formatted)
        self.assertIn('Smart Suggestions', formatted)


class TestDockerAnalyzerIntegration(unittest.TestCase):
    """Integration tests for Docker analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = DockerAnalyzer()
    
    def test_real_world_dockerfile_errors(self):
        """Test with real-world Dockerfile build errors."""
        real_errors = [
            {
                'text': "Step 5/10 : COPY package.json /app/\nCOPY failed: file not found in build context or excluded by .dockerignore: stat package.json: file does not exist",
                'expected_type': 'copy_failed',
                'expected_instruction': 'COPY'
            },
            {
                'text': "Step 7/12 : RUN npm install\n ---> Running in abc123def456\nnpm ERR! code ENOENT\nThe command '/bin/sh -c npm install' returned a non-zero code: 1",
                'expected_type': 'run_failed',
                'expected_instruction': 'RUN'
            },
            {
                'text': "Dockerfile:15: Unknown instruction: FRON",
                'expected_type': 'invalid_instruction',
                'expected_line': 15
            }
        ]
        
        for scenario in real_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                
                if 'expected_instruction' in scenario:
                    self.assertEqual(result.instruction, scenario['expected_instruction'])
                if 'expected_line' in scenario:
                    self.assertEqual(result.line, scenario['expected_line'])
    
    def test_real_world_runtime_errors(self):
        """Test with real-world Docker runtime errors."""
        runtime_errors = [
            {
                'text': "docker: Error response from daemon: driver failed programming external connectivity on endpoint webapp (abc123): Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use.",
                'expected_type': 'port_already_allocated',
                'expected_severity': 'medium'
            },
            {
                'text': "Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get \"http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json\": dial unix /var/run/docker.sock: connect: permission denied",
                'expected_type': 'permission_denied',
                'expected_severity': 'high'
            },
            {
                'text': "Unable to find image 'node:18-alpine' locally\ndocker: Error response from daemon: pull access denied for node, repository does not exist or may require 'docker login': denied: requested access to the resource is denied.",
                'expected_type': 'image_not_found'
            }
        ]
        
        for scenario in runtime_errors:
            with self.subTest(error=scenario['text']):
                result = self.analyzer.analyze(scenario['text'])
                self.assertIsNotNone(result)
                self.assertEqual(result.error_type, scenario['expected_type'])
                
                if 'expected_severity' in scenario:
                    self.assertEqual(result.severity, scenario['expected_severity'])
    
    def test_suggestion_quality(self):
        """Test that suggestions are relevant and helpful."""
        error_text = "COPY failed: file not found: package.json"
        result = self.analyzer.analyze(error_text)
        
        # Check that suggestions exist and have required fields
        self.assertTrue(len(result.suggestions) > 0)
        for suggestion in result.suggestions:
            self.assertIn('title', suggestion)
            self.assertIn('code', suggestion)
            self.assertIn('confidence', suggestion)
            self.assertGreater(suggestion['confidence'], 0)
            self.assertLessEqual(suggestion['confidence'], 1)
    
    def test_multi_stage_build_errors(self):
        """Test errors in multi-stage Docker builds."""
        error_text = """Step 8/15 : COPY --from=builder /app/dist /usr/share/nginx/html
COPY failed: stat /var/lib/docker/overlay2/abc123/merged/app/dist: no such file or directory"""
        
        result = self.analyzer.analyze(error_text)
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'copy_failed')
        self.assertEqual(result.instruction, 'COPY')
        # Should provide suggestions about multi-stage builds
        self.assertTrue(any('build context' in str(s).lower() for s in result.suggestions))
    
    def test_docker_compose_errors(self):
        """Test docker-compose specific errors."""
        compose_errors = [
            "ERROR: yaml.scanner.ScannerError: while scanning a simple key\n  in \"./docker-compose.yml\", line 15, column 1",
            "ERROR: Service 'frontend' depends on service 'backend' which is undefined.",
            "ERROR: The Compose file './docker-compose.yml' is invalid because:\nservices.web.ports contains an invalid type, it should be an array"
        ]
        
        for error_text in compose_errors:
            result = self.analyzer.analyze(error_text)
            self.assertIsNotNone(result)
            # Should recognize as compose-related error
            self.assertIn(result.error_type, ['invalid_compose_file', 'service_not_found', 'unknown_docker_error'])
    
    def test_buildkit_errors(self):
        """Test Docker BuildKit specific errors."""
        buildkit_error = "#12 ERROR: failed to solve: failed to compute cache key: failed to walk /var/lib/docker/tmp/buildkit-mount123456/src: lstat /var/lib/docker/tmp/buildkit-mount123456/src: no such file or directory"
        
        result = self.analyzer.analyze(buildkit_error)
        self.assertIsNotNone(result)
        self.assertEqual(result.error_type, 'copy_failed')
    
    def test_performance(self):
        """Test analyzer performance with multiple errors."""
        import time
        
        errors = [
            "Unknown instruction: FRON",
            "COPY failed: file not found",
            "Permission denied",
            "port is already allocated",
            "no space left on device",
            "Service 'web' not found"
        ] * 20  # Test with 120 errors
        
        start_time = time.time()
        for error in errors:
            self.analyzer.analyze(error)
        end_time = time.time()
        
        # Should analyze 120 errors in less than 1 second
        self.assertLess(end_time - start_time, 1.0)


if __name__ == '__main__':
    unittest.main()