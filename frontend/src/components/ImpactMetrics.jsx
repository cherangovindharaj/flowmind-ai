import React from 'react'

function ImpactMetrics() {
  return (
    <div className="result-section">
      <h3>💼 Business Impact</h3>
      <p className="section-subtitle">Results based on simulated enterprise workflow execution with AI agents</p>
      <div className="impact-metrics">
        {/* Time Reduction */}
        <div className="impact-card time">
          <div className="impact-icon">⏱️</div>
          <div className="impact-value">2 hrs → 10 mins</div>
          <div className="impact-label">Execution Time Reduced</div>
          <div className="impact-subtitle">92% faster execution</div>
        </div>

        {/* Automation Level */}
        <div className="impact-card automation">
          <div className="impact-icon">🤖</div>
          <div className="impact-value">85%</div>
          <div className="impact-label">Workflow Automated</div>
          <div className="impact-subtitle">Minimal human intervention</div>
        </div>

        {/* Error Reduction */}
        <div className="impact-card error">
          <div className="impact-icon">🛡️</div>
          <div className="impact-value">15% → 2%</div>
          <div className="impact-label">Error Rate Reduced</div>
          <div className="impact-subtitle">87% fewer errors</div>
        </div>
      </div>
      <p className="impact-disclaimer">
        Estimated impact based on automated workflow execution
      </p>
    </div>
  )
}

export default ImpactMetrics
