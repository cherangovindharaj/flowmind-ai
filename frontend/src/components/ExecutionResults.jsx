import React from 'react'

function ExecutionResults({ results }) {
  if (!results || results.length === 0) {
    return null
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'SUCCESS':
        return '✅'
      case 'RETRIED_SUCCESS':
        return '🔄✅'
      case 'FAILED':
        return '❌'
      default:
        return '⏸️'
    }
  }

  const getStatusBadge = (status) => {
    if (status === 'RETRIED_SUCCESS') {
      return <span className="retry-badge">Retried Successfully</span>
    }
    if (status === 'FAILED') {
      return <span className="failed-badge">Failed</span>
    }
    return null
  }

  const getCriticalityIndicator = (criticality) => {
    const colors = {
      'HIGH': '#ef4444',
      'MEDIUM': '#f59e0b',
      'LOW': '#3b82f6'
    }
    return (
      <span 
        className="criticality-indicator"
        style={{ backgroundColor: colors[criticality] || colors['MEDIUM'] }}
        title={`${criticality} Priority`}
      >
        ●
      </span>
    )
  }

  const getRetryBadge = (retryCount) => {
    if (retryCount > 0) {
      return <span className="retry-badge">Retried {retryCount + 1}x</span>
    }
    return null
  }

  return (
    <div className="result-section">
      <h3>⚙️ Execution Results</h3>
      <div className="execution-container">
        <p className="section-description">
          Each step was executed with automatic retry on failure:
        </p>
        <div className="execution-grid">
          {results.map((result, index) => (
            <div
              key={index}
              className={`execution-card ${result.status}`}
            >
              <div className="execution-header">
                <span className="status-icon">
                  {getStatusIcon(result.status)}
                </span>
                {getCriticalityIndicator(result.criticality)}
                <span className="step-title">Step {result.step_number}</span>
                {getStatusBadge(result.status)}
                {result.retry_count > 0 && (
                  <span className="retry-badge">Retried {result.retry_count}x</span>
                )}
              </div>
              <div className="execution-body">
                <p className="execution-description">{result.description}</p>
                <p className="execution-output">{result.output}</p>
                {result.error_message && (
                  <p className="execution-error">{result.error_message}</p>
                )}
              </div>
              <div className="execution-footer">
                {result.execution_time && (
                  <span className="execution-time">
                    ⏱️ {result.execution_time.toFixed(2)}s
                  </span>
                )}
                {result.validation_checkpoint && (
                  <span className="checkpoint-badge" title="Validation Checkpoint">
                    ✓ Checkpoint
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ExecutionResults
