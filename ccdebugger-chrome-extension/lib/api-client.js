/**
 * CCDebugger Chrome Extension - API Client
 * Handles communication with CCDebugger backend API
 */

class CCDebuggerAPI {
  constructor(endpoint = 'https://api.ccdebugger.com') {
    this.baseUrl = endpoint;
    this.apiKey = null;
    this.timeout = 10000; // 10 seconds
    this.retryAttempts = 3;
    this.retryDelay = 1000; // 1 second
  }

  /**
   * Set API configuration
   * @param {Object} config - API configuration
   */
  setConfig(config) {
    if (config.endpoint) {
      this.baseUrl = config.endpoint;
    }
    if (config.apiKey) {
      this.apiKey = config.apiKey;
    }
    if (config.timeout) {
      this.timeout = config.timeout;
    }
  }

  /**
   * Analyze error with CCDebugger API
   * @param {Object} errorData - Error information
   * @returns {Promise<Object>} Analysis results
   */
  async analyzeError(errorData) {
    const endpoint = `${this.baseUrl}/analyze`;
    
    const payload = {
      error_type: errorData.type || 'unknown',
      message: errorData.message || '',
      stack_trace: errorData.stack || '',
      error_context: {
        url: errorData.url || '',
        source_file: errorData.source || '',
        line_number: errorData.line || null,
        column_number: errorData.column || null,
        user_agent: navigator.userAgent,
        timestamp: errorData.timestamp || new Date().toISOString()
      },
      language: this.detectLanguage(errorData),
      framework: this.detectFramework(errorData),
      metadata: {
        extension_version: chrome.runtime.getManifest().version,
        chrome_version: this.getChromeVersion()
      }
    };

    try {
      const response = await this.makeRequest('POST', endpoint, payload);
      return this.processAnalysisResponse(response);
    } catch (error) {
      console.error('API analysis error:', error);
      // Return fallback analysis
      return this.getFallbackAnalysis(errorData);
    }
  }

  /**
   * Get error patterns from API
   * @param {string} language - Programming language
   * @returns {Promise<Array>} Error patterns
   */
  async getErrorPatterns(language) {
    const endpoint = `${this.baseUrl}/patterns/${language}`;
    
    try {
      const response = await this.makeRequest('GET', endpoint);
      return response.patterns || [];
    } catch (error) {
      console.error('Failed to fetch error patterns:', error);
      return [];
    }
  }

  /**
   * Submit feedback for an analysis
   * @param {string} analysisId - Analysis ID
   * @param {Object} feedback - User feedback
   * @returns {Promise<Object>} Feedback response
   */
  async submitFeedback(analysisId, feedback) {
    const endpoint = `${this.baseUrl}/feedback`;
    
    const payload = {
      analysis_id: analysisId,
      helpful: feedback.helpful,
      correct: feedback.correct,
      comment: feedback.comment || '',
      timestamp: new Date().toISOString()
    };

    try {
      return await this.makeRequest('POST', endpoint, payload);
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      throw error;
    }
  }

  /**
   * Make HTTP request with retry logic
   * @param {string} method - HTTP method
   * @param {string} url - Request URL
   * @param {Object} data - Request payload
   * @returns {Promise<Object>} Response data
   */
  async makeRequest(method, url, data = null) {
    const headers = {
      'Content-Type': 'application/json',
      'X-Extension-Version': chrome.runtime.getManifest().version,
      'X-Client-Type': 'chrome-extension'
    };

    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const options = {
      method,
      headers,
      signal: AbortSignal.timeout(this.timeout)
    };

    if (data && method !== 'GET') {
      options.body = JSON.stringify(data);
    }

    let lastError;
    for (let attempt = 0; attempt < this.retryAttempts; attempt++) {
      try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
          throw new APIError(
            `API request failed: ${response.status} ${response.statusText}`,
            response.status,
            await this.parseErrorResponse(response)
          );
        }

        return await response.json();
      } catch (error) {
        lastError = error;
        
        // Don't retry on client errors (4xx)
        if (error instanceof APIError && error.status >= 400 && error.status < 500) {
          throw error;
        }

        // Wait before retry
        if (attempt < this.retryAttempts - 1) {
          await this.delay(this.retryDelay * Math.pow(2, attempt));
        }
      }
    }

    throw lastError;
  }

  /**
   * Parse error response from API
   * @param {Response} response - Fetch response
   * @returns {Promise<Object>} Error details
   */
  async parseErrorResponse(response) {
    try {
      const data = await response.json();
      return data.error || data.message || 'Unknown error';
    } catch {
      return response.statusText || 'Unknown error';
    }
  }

  /**
   * Process analysis response
   * @param {Object} response - API response
   * @returns {Object} Processed analysis
   */
  processAnalysisResponse(response) {
    return {
      analysisId: response.analysis_id || null,
      errorType: response.error_type || 'unknown',
      severity: response.severity || 'medium',
      category: response.category || 'general',
      explanation: response.explanation || '',
      suggestions: this.processSuggestions(response.suggestions || []),
      relatedErrors: response.related_errors || [],
      documentation: response.documentation || [],
      confidence: response.confidence || 0.5,
      tags: response.tags || []
    };
  }

  /**
   * Process suggestions from API
   * @param {Array} suggestions - Raw suggestions
   * @returns {Array} Processed suggestions
   */
  processSuggestions(suggestions) {
    return suggestions.map(suggestion => ({
      id: suggestion.id || null,
      title: suggestion.title || suggestion.description || '',
      description: suggestion.description || '',
      code: suggestion.code_example || suggestion.code || '',
      confidence: suggestion.confidence || 0.5,
      type: suggestion.type || 'general',
      documentation: suggestion.documentation_url || null,
      applicability: suggestion.applicability || 1.0
    }));
  }

  /**
   * Get fallback analysis when API is unavailable
   * @param {Object} errorData - Error information
   * @returns {Object} Fallback analysis
   */
  getFallbackAnalysis(errorData) {
    const analysis = {
      analysisId: null,
      errorType: errorData.type || 'unknown',
      severity: 'medium',
      category: 'general',
      explanation: 'Analysis unavailable. Using local patterns.',
      suggestions: [],
      confidence: 0.3
    };

    // Add basic suggestions based on error type
    if (errorData.message) {
      const message = errorData.message.toLowerCase();
      
      if (message.includes('undefined') || message.includes('null')) {
        analysis.suggestions.push({
          title: 'Check for null/undefined values',
          description: 'Add null checks before accessing properties',
          code: 'if (object && object.property) { /* use property */ }',
          confidence: 0.7
        });
      }
      
      if (message.includes('is not a function')) {
        analysis.suggestions.push({
          title: 'Verify function exists',
          description: 'Check if the function is defined and imported correctly',
          confidence: 0.6
        });
      }
      
      if (message.includes('network') || message.includes('fetch')) {
        analysis.suggestions.push({
          title: 'Check network connectivity',
          description: 'Verify API endpoints and network status',
          confidence: 0.5
        });
      }
    }

    return analysis;
  }

  /**
   * Detect programming language from error
   * @param {Object} errorData - Error information
   * @returns {string} Detected language
   */
  detectLanguage(errorData) {
    // Check file extension
    if (errorData.source) {
      const ext = errorData.source.split('.').pop().toLowerCase();
      const languageMap = {
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'py': 'python',
        'rb': 'ruby',
        'java': 'java',
        'swift': 'swift',
        'kt': 'kotlin',
        'go': 'go',
        'rs': 'rust',
        'php': 'php'
      };
      
      if (languageMap[ext]) {
        return languageMap[ext];
      }
    }

    // Check error patterns
    if (errorData.message) {
      if (errorData.message.includes('SyntaxError') || errorData.message.includes('TypeError')) {
        return 'javascript';
      }
      if (errorData.message.includes('NameError') || errorData.message.includes('IndentationError')) {
        return 'python';
      }
    }

    // Check stack trace patterns
    if (errorData.stack) {
      if (errorData.stack.includes('.js:') || errorData.stack.includes('.jsx:')) {
        return 'javascript';
      }
      if (errorData.stack.includes('.py:')) {
        return 'python';
      }
    }

    return 'javascript'; // Default
  }

  /**
   * Detect framework from error
   * @param {Object} errorData - Error information
   * @returns {string|null} Detected framework
   */
  detectFramework(errorData) {
    const patterns = {
      'react': ['React', 'ReactDOM', 'useState', 'useEffect', 'Component'],
      'vue': ['Vue', 'v-model', 'v-for', '$emit', 'mounted'],
      'angular': ['Angular', 'ng-', '@Component', 'NgModule'],
      'svelte': ['Svelte', '$:', 'export let'],
      'next': ['Next', '_app', '_document', 'getServerSideProps'],
      'nuxt': ['Nuxt', 'asyncData', 'fetch', '$nuxt']
    };

    const searchText = `${errorData.message} ${errorData.stack || ''}`;
    
    for (const [framework, keywords] of Object.entries(patterns)) {
      if (keywords.some(keyword => searchText.includes(keyword))) {
        return framework;
      }
    }

    return null;
  }

  /**
   * Get Chrome version
   * @returns {string} Chrome version
   */
  getChromeVersion() {
    const match = navigator.userAgent.match(/Chrome\/(\d+\.\d+\.\d+\.\d+)/);
    return match ? match[1] : 'unknown';
  }

  /**
   * Delay helper for retry logic
   * @param {number} ms - Milliseconds to delay
   * @returns {Promise<void>}
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Custom error class for API errors
class APIError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

// Export for use in extension
window.CCDebuggerAPI = CCDebuggerAPI;