# CCDebugger API Documentation

## Overview

The CCDebugger API provides AI-powered error analysis for multiple programming languages. This RESTful API enables developers to integrate intelligent debugging capabilities into their applications.

## Base URL

```
Production: https://api.ccdebugger.com
Development: http://localhost:8000
```

## Authentication

### API Key Authentication (Optional)
For higher rate limits and premium features, include your API key in the Authorization header:

```http
Authorization: Bearer YOUR_API_KEY
```

## Rate Limiting

- **Without API Key**: 100 requests per hour
- **With API Key**: 1000 requests per hour
- **Enterprise**: Custom limits

Rate limit information is included in response headers:
- `X-RateLimit-Limit`: Maximum requests per hour
- `X-RateLimit-Remaining`: Remaining requests
- `X-RateLimit-Reset`: Unix timestamp when limit resets

## Endpoints

### 1. Analyze Error

Analyze an error with AI-powered suggestions.

**Endpoint**: `POST /analyze`

**Request Body**:
```json
{
  "error_type": "runtime_error",
  "message": "Cannot read property 'name' of undefined",
  "stack_trace": "TypeError: Cannot read property 'name' of undefined\n    at UserProfile.render (UserProfile.js:45:23)",
  "error_context": {
    "url": "https://example.com/profile",
    "source_file": "UserProfile.js",
    "line_number": 45,
    "column_number": 23,
    "user_agent": "Mozilla/5.0...",
    "timestamp": "2025-01-29T10:30:00Z"
  },
  "language": "javascript",
  "framework": "react",
  "metadata": {
    "extension_version": "1.0.0",
    "chrome_version": "120.0.0.0"
  }
}
```

**Response** (200 OK):
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "error_type": "null_reference",
  "severity": "high",
  "category": "runtime",
  "explanation": "You're trying to access the 'name' property of an object that is undefined. This typically happens when data hasn't loaded yet or when an expected object doesn't exist.",
  "suggestions": [
    {
      "id": "sugg_001",
      "title": "Add null check before accessing property",
      "description": "Check if the object exists before accessing its properties",
      "code_example": "if (user && user.name) {\n  return <div>{user.name}</div>;\n}",
      "confidence": 0.95,
      "type": "defensive_programming",
      "documentation_url": "https://docs.ccdebugger.com/null-checks",
      "applicability": 0.98
    },
    {
      "id": "sugg_002",
      "title": "Use optional chaining",
      "description": "Use the optional chaining operator for safe property access",
      "code_example": "return <div>{user?.name || 'Guest'}</div>;",
      "confidence": 0.92,
      "type": "modern_syntax",
      "applicability": 0.95
    }
  ],
  "related_errors": [
    {
      "error_type": "undefined_property",
      "similarity": 0.85
    }
  ],
  "documentation": [
    {
      "title": "Handling Null and Undefined in JavaScript",
      "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining"
    }
  ],
  "confidence": 0.94,
  "tags": ["null-safety", "react", "defensive-programming"]
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Missing required field: message",
    "details": {
      "field": "message",
      "requirement": "non-empty string"
    }
  }
}
```

### 2. Get Error Patterns

Retrieve common error patterns for a specific language.

**Endpoint**: `GET /patterns/{language}`

**Path Parameters**:
- `language`: Programming language (e.g., `javascript`, `python`, `swift`, `kotlin`)

**Query Parameters**:
- `framework` (optional): Specific framework (e.g., `react`, `django`)
- `category` (optional): Error category (e.g., `runtime`, `syntax`, `type`)

**Response** (200 OK):
```json
{
  "language": "javascript",
  "patterns": [
    {
      "pattern_id": "js_null_ref_001",
      "name": "null_reference_error",
      "regex": "Cannot read propert(?:y|ies) .+ of (?:null|undefined)",
      "description": "Attempting to access properties of null or undefined",
      "severity": "high",
      "common_causes": [
        "Accessing data before it's loaded",
        "Missing null checks",
        "Incorrect object initialization"
      ],
      "suggested_fixes": [
        "Add null/undefined checks",
        "Use optional chaining (?.)",
        "Provide default values"
      ]
    }
  ],
  "total": 42,
  "framework_specific": true
}
```

### 3. Submit Feedback

Submit feedback on an analysis to improve future suggestions.

**Endpoint**: `POST /feedback`

**Request Body**:
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "helpful": true,
  "correct": true,
  "applied_suggestion_id": "sugg_001",
  "comment": "The null check suggestion solved my issue perfectly",
  "timestamp": "2025-01-29T10:35:00Z"
}
```

**Response** (201 Created):
```json
{
  "feedback_id": "fb_123456",
  "status": "recorded",
  "message": "Thank you for your feedback"
}
```

### 4. Get Supported Languages

Get a list of all supported programming languages.

**Endpoint**: `GET /languages`

**Response** (200 OK):
```json
{
  "languages": [
    {
      "code": "javascript",
      "name": "JavaScript",
      "file_extensions": [".js", ".jsx", ".mjs"],
      "frameworks": ["react", "vue", "angular", "node"],
      "error_pattern_count": 156
    },
    {
      "code": "python",
      "name": "Python",
      "file_extensions": [".py"],
      "frameworks": ["django", "flask", "fastapi"],
      "error_pattern_count": 98
    },
    {
      "code": "swift",
      "name": "Swift",
      "file_extensions": [".swift"],
      "frameworks": ["swiftui", "uikit"],
      "error_pattern_count": 67
    },
    {
      "code": "kotlin",
      "name": "Kotlin",
      "file_extensions": [".kt", ".kts"],
      "frameworks": ["android", "spring"],
      "error_pattern_count": 73
    }
  ],
  "total": 14
}
```

### 5. Health Check

Check API service status.

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "version": "2.0.3",
  "timestamp": "2025-01-29T10:30:00Z",
  "services": {
    "api": "operational",
    "ai_engine": "operational",
    "database": "operational"
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request validation failed |
| `LANGUAGE_NOT_SUPPORTED` | Unsupported programming language |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `ANALYSIS_FAILED` | Error analysis failed |
| `INTERNAL_ERROR` | Server error |
| `UNAUTHORIZED` | Invalid or missing API key |

## WebSocket Support (Coming Soon)

Real-time error streaming for continuous monitoring:

```javascript
const ws = new WebSocket('wss://api.ccdebugger.com/stream');

ws.send(JSON.stringify({
  action: 'subscribe',
  api_key: 'YOUR_API_KEY',
  filters: {
    languages: ['javascript', 'typescript'],
    severity: ['high', 'critical']
  }
}));

ws.onmessage = (event) => {
  const analysis = JSON.parse(event.data);
  console.log('Real-time error analysis:', analysis);
};
```

## SDK Examples

### JavaScript/TypeScript
```javascript
import { CCDebuggerClient } from '@ccdebugger/sdk';

const client = new CCDebuggerClient({
  apiKey: 'YOUR_API_KEY'
});

try {
  const analysis = await client.analyzeError({
    type: 'runtime_error',
    message: error.message,
    stack: error.stack
  });
  
  console.log('Suggestions:', analysis.suggestions);
} catch (err) {
  console.error('Analysis failed:', err);
}
```

### Python
```python
from ccdebugger import CCDebuggerClient

client = CCDebuggerClient(api_key='YOUR_API_KEY')

try:
    analysis = client.analyze_error(
        error_type='runtime_error',
        message=str(error),
        stack_trace=traceback.format_exc()
    )
    
    for suggestion in analysis['suggestions']:
        print(f"- {suggestion['title']}: {suggestion['description']}")
        
except Exception as e:
    print(f"Analysis failed: {e}")
```

## Best Practices

1. **Include Stack Traces**: Always include full stack traces for better analysis
2. **Provide Context**: Include file paths, line numbers, and surrounding code
3. **Specify Language**: Explicitly set the programming language for accurate analysis
4. **Handle Errors**: Implement proper error handling for API failures
5. **Cache Results**: Cache analysis results to reduce API calls
6. **Batch Requests**: Group similar errors to optimize API usage

## Changelog

### v2.0.0 (2025-01-29)
- Added Swift language support
- Added Kotlin language support
- Improved AI analysis accuracy
- Enhanced suggestion confidence scoring

### v1.5.0 (2025-01-15)
- Added framework detection
- Improved error pattern matching
- Added related errors feature

## Support

- **Documentation**: https://docs.ccdebugger.com
- **GitHub Issues**: https://github.com/888wing/ccdebugger/issues
- **Email**: support@ccdebugger.com
- **Discord**: https://discord.gg/ccdebugger

---

*This API is actively maintained and updated. Check back regularly for new features and improvements.*