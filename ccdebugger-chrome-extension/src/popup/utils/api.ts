import { ErrorData, ErrorAnalysis } from '../types';

const API_BASE_URL = 'https://api.ccdebugger.com';
const API_TIMEOUT = 10000; // 10 seconds

export async function analyzeError(error: ErrorData): Promise<ErrorAnalysis> {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        error_type: error.type,
        message: error.message,
        stack_trace: error.stack,
        error_context: {
          url: error.url,
          source_file: error.source,
          line_number: error.line,
          column_number: error.column,
          user_agent: navigator.userAgent,
          timestamp: new Date(error.timestamp).toISOString()
        },
        language: 'javascript',
        framework: error.framework,
        metadata: {
          extension_version: chrome.runtime.getManifest().version,
          chrome_version: navigator.userAgent.match(/Chrome\/([0-9.]+)/)?.[1]
        }
      }),
      signal: AbortSignal.timeout(API_TIMEOUT)
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    return data as ErrorAnalysis;
  } catch (err) {
    console.error('Failed to analyze error:', err);
    
    // Return fallback analysis
    return {
      analysisId: `local-${Date.now()}`,
      errorType: error.type,
      severity: 'medium',
      category: 'runtime',
      explanation: 'Error analysis is currently unavailable. Please check your internet connection.',
      suggestions: [
        {
          id: 'fallback-1',
          title: 'Check console for more details',
          description: 'Open DevTools console to see the full error stack trace and context.',
          confidence: 0.5,
          type: 'debugging',
          applicability: 1.0
        }
      ],
      confidence: 0.3,
      tags: ['offline-analysis', error.type]
    };
  }
}