export interface ErrorData {
  id: string;
  type: 'runtime' | 'network' | 'promise' | 'syntax' | 'resource';
  message: string;
  stack?: string;
  timestamp: number;
  url: string;
  line?: number;
  column?: number;
  source?: string;
  framework?: string;
  analysis?: ErrorAnalysis;
}

export interface ErrorAnalysis {
  analysisId: string;
  errorType: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  category: string;
  explanation: string;
  suggestions: Suggestion[];
  relatedErrors?: RelatedError[];
  documentation?: Documentation[];
  confidence: number;
  tags: string[];
}

export interface Suggestion {
  id: string;
  title: string;
  description: string;
  codeExample?: string;
  confidence: number;
  type: string;
  documentationUrl?: string;
  applicability: number;
}

export interface RelatedError {
  errorType: string;
  similarity: number;
}

export interface Documentation {
  title: string;
  url: string;
}

export interface AppState {
  errors: ErrorData[];
  isLoading: boolean;
  isMonitoring: boolean;
  currentUrl: string;
}

export interface ChromeTab {
  id?: number;
  url?: string;
  title?: string;
}