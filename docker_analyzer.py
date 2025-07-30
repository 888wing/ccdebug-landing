"""Docker/Dockerfile language error analyzer for CCDebugger."""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DockerError:
    """Represents a Docker/Dockerfile error with analysis."""
    error_type: str
    message: str
    dockerfile_path: Optional[str] = None
    line: Optional[int] = None
    instruction: Optional[str] = None
    severity: str = "high"
    suggestions: List[Dict[str, any]] = None
    explanation: Optional[str] = None
    

class DockerAnalyzer:
    """Analyzer for Docker and Dockerfile errors."""
    
    # Dockerfile syntax error patterns
    DOCKERFILE_PATTERNS = {
        'invalid_instruction': {
            'pattern': r"(?:Unknown instruction|Invalid instruction|unknown flag)",
            'severity': 'high',
            'explanation': "Invalid or misspelled Dockerfile instruction.",
            'suggestions': [
                {
                    'title': 'Check Dockerfile syntax',
                    'code': '# Valid Dockerfile instructions\nFROM image:tag\nRUN command\nCOPY source dest\nWORKDIR /path\nEXPOSE port\nCMD ["executable"]',
                    'confidence': 0.90
                },
                {
                    'title': 'Use uppercase for instructions',
                    'code': '# Instructions must be uppercase\nFROM ubuntu:latest  # Correct\nfrom ubuntu:latest  # Incorrect',
                    'confidence': 0.85
                }
            ]
        },
        'missing_argument': {
            'pattern': r"(?:requires at least \d+ argument|COPY requires at least|not enough arguments in call)",
            'severity': 'high',
            'explanation': "Dockerfile instruction is missing required arguments.",
            'suggestions': [
                {
                    'title': 'Provide required arguments',
                    'code': '# Examples of correct usage\nFROM ubuntu:20.04\nCOPY source.txt /dest/\nRUN apt-get update\nEXPOSE 8080',
                    'confidence': 0.90
                },
                {
                    'title': 'Check instruction syntax',
                    'code': '# Common instruction formats\nCOPY <src> <dest>\nADD <src> <dest>\nENV <key>=<value>\nLABEL <key>=<value>',
                    'confidence': 0.85
                }
            ]
        },
        'invalid_from': {
            'pattern': r"(?:invalid reference format|repository name must be lowercase|FROM requires (?:one|exactly one) argument)",
            'severity': 'high',
            'explanation': "Invalid FROM instruction or image reference.",
            'suggestions': [
                {
                    'title': 'Use valid image reference',
                    'code': '# Valid FROM formats\nFROM ubuntu:20.04\nFROM node:16-alpine\nFROM registry.com/namespace/image:tag',
                    'confidence': 0.95
                },
                {
                    'title': 'Use lowercase for image names',
                    'code': '# Image names must be lowercase\nFROM ubuntu:latest     # Correct\nFROM Ubuntu:latest     # Incorrect',
                    'confidence': 0.90
                }
            ]
        },
        'copy_failed': {
            'pattern': r"(?:COPY failed|failed to compute cache key|no such file or directory)",
            'severity': 'high',
            'explanation': "COPY or ADD instruction failed, usually due to missing source files.",
            'suggestions': [
                {
                    'title': 'Check source file exists',
                    'code': '# Ensure files exist in build context\n# Build context is usually current directory\ndocker build -t myimage .\n\n# Files must be within build context',
                    'confidence': 0.90
                },
                {
                    'title': 'Use .dockerignore',
                    'code': '# Create .dockerignore to exclude files\nnode_modules/\n.git/\n*.log\n.env',
                    'confidence': 0.85
                },
                {
                    'title': 'Check file paths',
                    'code': '# Use relative paths from build context\nCOPY ./src /app/src\n# Not absolute paths\nCOPY /home/user/src /app/src  # Wrong',
                    'confidence': 0.80
                }
            ]
        },
        'run_failed': {
            'pattern': r"(?:The command .+ returned a non-zero code|executor failed running)",
            'severity': 'high',
            'explanation': "RUN instruction failed during build.",
            'suggestions': [
                {
                    'title': 'Check command syntax',
                    'code': '# Combine commands to reduce layers\nRUN apt-get update && \\\n    apt-get install -y package && \\\n    apt-get clean',
                    'confidence': 0.85
                },
                {
                    'title': 'Handle non-interactive mode',
                    'code': '# Set non-interactive for apt\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update && apt-get install -y package',
                    'confidence': 0.80
                },
                {
                    'title': 'Check package availability',
                    'code': '# Update package lists first\nRUN apt-get update && apt-get install -y package\n# For Alpine\nRUN apk update && apk add package',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    # Docker runtime error patterns
    RUNTIME_PATTERNS = {
        'container_not_found': {
            'pattern': r"(?:No such container|container .+ not found|Could not find container)",
            'severity': 'medium',
            'explanation': "The specified container does not exist.",
            'suggestions': [
                {
                    'title': 'List running containers',
                    'code': '# List all running containers\ndocker ps\n\n# List all containers (including stopped)\ndocker ps -a',
                    'confidence': 0.90
                },
                {
                    'title': 'Use container name or ID',
                    'code': '# Use container name\ndocker exec -it container_name bash\n\n# Or use container ID\ndocker exec -it abc123def456 bash',
                    'confidence': 0.85
                }
            ]
        },
        'image_not_found': {
            'pattern': r"(?:Unable to find image|pull access denied|repository does not exist|repository .+ not found)",
            'severity': 'high',
            'explanation': "Docker cannot find or pull the specified image.",
            'suggestions': [
                {
                    'title': 'Check image name',
                    'code': '# Verify image name and tag\ndocker pull ubuntu:20.04\n\n# List local images\ndocker images',
                    'confidence': 0.90
                },
                {
                    'title': 'Login to registry',
                    'code': '# Login if using private registry\ndocker login registry.example.com\n\n# For Docker Hub\ndocker login',
                    'confidence': 0.85
                }
            ]
        },
        'port_already_allocated': {
            'pattern': r"(?:bind: address already in use|port is already allocated)",
            'severity': 'medium',
            'explanation': "The specified port is already in use by another process.",
            'suggestions': [
                {
                    'title': 'Use different port',
                    'code': '# Map to different host port\ndocker run -p 8081:80 image\n\n# Or let Docker choose\ndocker run -P image',
                    'confidence': 0.95
                },
                {
                    'title': 'Find process using port',
                    'code': '# Find what\'s using the port\nlsof -i :8080\n# Or\nnetstat -tulpn | grep 8080',
                    'confidence': 0.85
                }
            ]
        },
        'permission_denied': {
            'pattern': r"(?:Permission denied|Got permission denied|access denied)",
            'severity': 'high',
            'explanation': "Permission denied error, often related to Docker daemon access.",
            'suggestions': [
                {
                    'title': 'Add user to docker group',
                    'code': '# Add current user to docker group\nsudo usermod -aG docker $USER\n\n# Then logout and login again',
                    'confidence': 0.90
                },
                {
                    'title': 'Use sudo (temporary)',
                    'code': '# Run with sudo\nsudo docker ps\n\n# Not recommended for regular use',
                    'confidence': 0.70
                }
            ]
        },
        'out_of_space': {
            'pattern': r"(?:no space left on device|disk quota exceeded)",
            'severity': 'critical',
            'explanation': "Docker has run out of disk space.",
            'suggestions': [
                {
                    'title': 'Clean up Docker resources',
                    'code': '# Remove unused containers, images, volumes\ndocker system prune -a\n\n# Remove volumes too\ndocker system prune -a --volumes',
                    'confidence': 0.95
                },
                {
                    'title': 'Check disk usage',
                    'code': '# Check Docker disk usage\ndocker system df\n\n# Check overall disk space\ndf -h',
                    'confidence': 0.90
                }
            ]
        }
    }
    
    # Docker compose error patterns
    COMPOSE_PATTERNS = {
        'invalid_compose_file': {
            'pattern': r"(?:yaml|yml|ERROR: yaml).*(?:scanner|parser|found character|mapping values|did not find expected)",
            'severity': 'high',
            'explanation': "Invalid YAML syntax in docker-compose file.",
            'suggestions': [
                {
                    'title': 'Check YAML syntax',
                    'code': '# Validate docker-compose file\ndocker-compose config\n\n# Common YAML rules:\n# - Use spaces, not tabs\n# - Consistent indentation\n# - Proper quoting',
                    'confidence': 0.90
                },
                {
                    'title': 'Fix indentation',
                    'code': 'version: "3.8"\nservices:\n  web:              # 2 spaces\n    image: nginx    # 4 spaces\n    ports:\n      - "80:80"     # 6 spaces',
                    'confidence': 0.85
                }
            ]
        },
        'service_not_found': {
            'pattern': r"(?:No such service|Service .+ was not found)",
            'severity': 'medium',
            'explanation': "The specified service is not defined in docker-compose.yml.",
            'suggestions': [
                {
                    'title': 'List available services',
                    'code': '# List all services\ndocker-compose ps\n\n# Check service names in compose file\ndocker-compose config --services',
                    'confidence': 0.90
                },
                {
                    'title': 'Use correct service name',
                    'code': '# Execute command in service\ndocker-compose exec service_name command\n\n# View logs for service\ndocker-compose logs service_name',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    # Network and volume patterns
    NETWORK_PATTERNS = {
        'network_not_found': {
            'pattern': r"(?:network .+ not found|Error response from daemon: network)",
            'severity': 'medium',
            'explanation': "The specified Docker network does not exist.",
            'suggestions': [
                {
                    'title': 'Create network',
                    'code': '# Create a network\ndocker network create mynetwork\n\n# List networks\ndocker network ls',
                    'confidence': 0.90
                },
                {
                    'title': 'Use existing network',
                    'code': '# Connect container to network\ndocker run --network mynetwork image\n\n# Or use default bridge\ndocker run image',
                    'confidence': 0.85
                }
            ]
        },
        'volume_not_found': {
            'pattern': r"(?:volume .+ not found|no such volume)",
            'severity': 'medium',
            'explanation': "The specified Docker volume does not exist.",
            'suggestions': [
                {
                    'title': 'Create volume',
                    'code': '# Create a volume\ndocker volume create myvolume\n\n# List volumes\ndocker volume ls',
                    'confidence': 0.90
                },
                {
                    'title': 'Use bind mount instead',
                    'code': '# Use bind mount\ndocker run -v /host/path:/container/path image\n\n# Or anonymous volume\ndocker run -v /container/path image',
                    'confidence': 0.85
                }
            ]
        }
    }
    
    def __init__(self):
        """Initialize the Docker analyzer."""
        # Order matters for pattern matching - check more specific patterns first
        # Rearrange DOCKERFILE_PATTERNS to check invalid_from before missing_argument
        dockerfile_patterns_ordered = {
            'invalid_instruction': self.DOCKERFILE_PATTERNS['invalid_instruction'],
            'invalid_from': self.DOCKERFILE_PATTERNS['invalid_from'],
            'copy_failed': self.DOCKERFILE_PATTERNS['copy_failed'],
            'run_failed': self.DOCKERFILE_PATTERNS['run_failed'],
            'missing_argument': self.DOCKERFILE_PATTERNS['missing_argument'],
        }
        
        self.all_patterns = {
            **dockerfile_patterns_ordered,
            **self.COMPOSE_PATTERNS,
            **self.NETWORK_PATTERNS,
            **self.RUNTIME_PATTERNS
        }
    
    def analyze(self, error_text: str) -> Optional[DockerError]:
        """Analyze Docker error text and return structured analysis."""
        if not error_text:
            return None
            
        # Extract Dockerfile and line information if present
        file_info = self._extract_file_info(error_text)
        
        # Extract instruction if present
        instruction = self._extract_instruction(error_text)
        
        # Try to match against known patterns
        for error_type, config in self.all_patterns.items():
            pattern = config['pattern']
            match = re.search(pattern, error_text, re.MULTILINE | re.IGNORECASE)
            
            if match:
                return DockerError(
                    error_type=error_type,
                    message=error_text,
                    dockerfile_path=file_info.get('file'),
                    line=file_info.get('line'),
                    instruction=instruction,
                    severity=config['severity'],
                    suggestions=config['suggestions'],
                    explanation=config['explanation']
                )
        
        # Generic Docker error if no pattern matches
        return DockerError(
            error_type='unknown_docker_error',
            message=error_text,
            dockerfile_path=file_info.get('file'),
            line=file_info.get('line'),
            instruction=instruction,
            severity='medium',
            explanation="This appears to be a Docker error, but doesn't match common patterns.",
            suggestions=[
                {
                    'title': 'Check Docker documentation',
                    'code': '# Verify Docker command syntax\ndocker --help\ndocker COMMAND --help',
                    'confidence': 0.5
                },
                {
                    'title': 'Enable debug logging',
                    'code': '# Run with debug output\ndocker --debug COMMAND\n\n# Or set environment variable\nexport DOCKER_BUILDKIT=1',
                    'confidence': 0.5
                }
            ]
        )
    
    def _extract_file_info(self, error_text: str) -> Dict[str, any]:
        """Extract Dockerfile path and line number from error text."""
        info = {}
        
        # Common patterns for Dockerfile:line
        patterns = [
            r'(?:Dockerfile|dockerfile):(\d+)',  # Dockerfile:42
            r'line (\d+): .+ \(Dockerfile\)',    # line 42: error (Dockerfile)
            r'"([^"]+Dockerfile[^"]*)" at line (\d+)',  # "path/Dockerfile" at line 42
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_text, re.IGNORECASE)
            if match:
                if '"' in pattern:
                    info['file'] = match.group(1)
                    info['line'] = int(match.group(2))
                elif 'line' in pattern and 'Dockerfile' in pattern:
                    info['line'] = int(match.group(1))
                    info['file'] = 'Dockerfile'
                else:
                    info['file'] = 'Dockerfile'
                    info['line'] = int(match.group(1))
                break
        
        return info
    
    def _extract_instruction(self, error_text: str) -> Optional[str]:
        """Extract the Dockerfile instruction from error text."""
        # Look for uppercase words that might be instructions
        instruction_pattern = r'\b(FROM|RUN|CMD|LABEL|MAINTAINER|EXPOSE|ENV|ADD|COPY|ENTRYPOINT|VOLUME|USER|WORKDIR|ARG|ONBUILD|STOPSIGNAL|HEALTHCHECK|SHELL)\b'
        match = re.search(instruction_pattern, error_text, re.IGNORECASE)
        
        if match:
            return match.group(1).upper()
        
        return None
    
    def format_suggestions(self, error: DockerError, language: str = 'en') -> str:
        """Format error analysis for display."""
        if language == 'zh':
            output = f"🚨 Docker 錯誤 - {error.severity.upper()} 優先級\n\n"
            output += f"錯誤類型: {error.error_type}\n"
            if error.dockerfile_path:
                output += f"Dockerfile: {error.dockerfile_path}"
                if error.line:
                    output += f" (第 {error.line} 行)"
                output += "\n"
            if error.instruction:
                output += f"指令: {error.instruction}\n"
            output += f"\n說明: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 智能建議:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (信心度: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```dockerfile\n{suggestion['code']}\n```\n"
        else:
            output = f"🚨 Docker Error - {error.severity.upper()} Priority\n\n"
            output += f"Error Type: {error.error_type}\n"
            if error.dockerfile_path:
                output += f"Dockerfile: {error.dockerfile_path}"
                if error.line:
                    output += f" (Line {error.line})"
                output += "\n"
            if error.instruction:
                output += f"Instruction: {error.instruction}\n"
            output += f"\nExplanation: {error.explanation}\n"
            
            if error.suggestions:
                output += "\n🎯 Smart Suggestions:\n"
                for i, suggestion in enumerate(error.suggestions, 1):
                    output += f"\n{i}. {suggestion['title']} (Confidence: {suggestion['confidence']*100:.0f}%)\n"
                    if 'code' in suggestion:
                        output += f"```dockerfile\n{suggestion['code']}\n```\n"
        
        return output


# Example usage
if __name__ == "__main__":
    analyzer = DockerAnalyzer()
    
    # Test cases
    test_errors = [
        "Unknown instruction: FRON",
        "COPY failed: file not found: package.json",
        "The command '/bin/sh -c npm install' returned a non-zero code: 1",
        "docker: Error response from daemon: pull access denied for myimage",
        "bind: address already in use",
        "ERROR: Service 'web' was not found"
    ]
    
    for error_text in test_errors:
        result = analyzer.analyze(error_text)
        if result:
            print(analyzer.format_suggestions(result))
            print("-" * 80)