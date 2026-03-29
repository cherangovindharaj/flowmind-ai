import React from 'react'

function ValidationResult({ validation }) {
  if (!validation) {
    return null
  }

  const getStatusColor = () => {
    return validation.is_valid ? 'valid' : 'invalid'
  }

  const getStatusText = () => {
    return validation.is_valid ? 'PASSED' : 'FAILED'
  }

  return (
    <div className="result-section">
      <h3>⚖️ AI Audit & Compliance Check</h3>
      <div className={`validation-container ${getStatusColor()}`}>
        <div className="validation-header">
          <span className="validation-status">{getStatusText()}</span>
          <span className="confidence-score">
            Confidence: {(validation.confidence_score * 100).toFixed(0)}%
          </span>
        </div>
        <div className="validation-reasoning">
          <strong>Analysis:</strong>
          <p>{validation.reasoning}</p>
        </div>
        {validation.failed_steps && validation.failed_steps.length > 0 && (
          <div className="failed-steps">
            <strong>Failed Steps:</strong>
            <span>{validation.failed_steps.join(', ')}</span>
          </div>
        )}
      </div>
    </div>
  )
}

export default ValidationResult
