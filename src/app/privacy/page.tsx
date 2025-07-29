export default function PrivacyPolicy() {
  return (
    <div className="container mx-auto px-4 py-16 max-w-4xl">
      <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
      
      <div className="prose prose-neutral dark:prose-invert max-w-none">
        <p className="text-muted-foreground mb-8">
          Last updated: January 1, 2025
        </p>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Introduction</h2>
          <p>
            CCDebugger ("we," "our," or "us") is committed to protecting your privacy. 
            This Privacy Policy explains how we collect, use, and safeguard your information 
            when you use our AI-powered debugging tool for Claude Code.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Information We Collect</h2>
          
          <h3 className="text-xl font-semibold mb-3">1. Error Data</h3>
          <p className="mb-4">
            When you use CCDebugger, we may process:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Error messages and stack traces you submit for analysis</li>
            <li>Code snippets related to debugging context</li>
            <li>Command usage patterns (anonymized)</li>
          </ul>

          <h3 className="text-xl font-semibold mb-3">2. Usage Information</h3>
          <p className="mb-4">
            We automatically collect:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>CLI version information</li>
            <li>Operating system and environment details</li>
            <li>Feature usage statistics (anonymized)</li>
          </ul>

          <h3 className="text-xl font-semibold mb-3">3. VS Code Extension Data</h3>
          <p className="mb-4">
            If you use our VS Code extension:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Extension settings and preferences</li>
            <li>Error analysis requests</li>
            <li>Performance metrics (optional)</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">How We Use Your Information</h2>
          <p className="mb-4">
            We use the collected information to:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Provide AI-powered error analysis and debugging suggestions</li>
            <li>Improve our debugging algorithms and templates</li>
            <li>Develop new features based on usage patterns</li>
            <li>Ensure service reliability and performance</li>
            <li>Provide technical support when requested</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Data Storage and Security</h2>
          <p className="mb-4">
            <strong>Local Processing:</strong> CCDebugger processes data locally on your machine 
            whenever possible. Error analysis happens in your Claude Code environment.
          </p>
          <p className="mb-4">
            <strong>Temporary Storage:</strong> Any data sent for AI analysis is processed 
            in real-time and not permanently stored on our servers.
          </p>
          <p className="mb-4">
            <strong>Security Measures:</strong> We implement industry-standard security measures 
            to protect your data during transmission and processing.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Third-Party Services</h2>
          <p className="mb-4">
            CCDebugger may integrate with:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li><strong>Claude AI:</strong> For advanced error analysis (see Anthropic's privacy policy)</li>
            <li><strong>GitHub:</strong> For version control integration (optional)</li>
            <li><strong>Analytics Services:</strong> For anonymous usage statistics</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Your Rights and Choices</h2>
          <p className="mb-4">
            You have the right to:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Use CCDebugger offline without any data collection</li>
            <li>Opt-out of anonymous usage statistics</li>
            <li>Request deletion of any personal data</li>
            <li>Access information we have about you</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Data Retention</h2>
          <p>
            We retain error analysis data only for the duration of your debugging session. 
            Anonymous usage statistics are aggregated and retained for up to 12 months 
            to improve our service.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Children's Privacy</h2>
          <p>
            CCDebugger is not intended for use by children under 13 years of age. 
            We do not knowingly collect personal information from children.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Changes to This Policy</h2>
          <p>
            We may update this Privacy Policy from time to time. We will notify you 
            of any changes by updating the "Last updated" date at the top of this policy.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Contact Us</h2>
          <p>
            If you have questions about this Privacy Policy or our data practices, 
            please contact us at:
          </p>
          <ul className="list-none mt-4">
            <li>Email: privacy@ccdebugger.com</li>
            <li>GitHub: github.com/888wing/ccdebugger/issues</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Open Source Commitment</h2>
          <p>
            CCDebugger is open source software. You can review our code and data 
            handling practices on our GitHub repository. We believe in transparency 
            and welcome community contributions to improve privacy and security.
          </p>
        </section>
      </div>
    </div>
  )
}