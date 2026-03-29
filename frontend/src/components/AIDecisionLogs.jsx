import React from 'react'

function AIDecisionLogs({ logs }) {
  if (!logs || logs.length === 0) {
    return null
  }

  const getPhaseIcon = (phase) => {
    switch (phase) {
      case 'PLANNING':
        return '📋'
      case 'EXECUTION':
        return '⚙️'
      case 'VALIDATION':
        return '✓'
      case 'MONITORING':
        return '🔍'
      case 'ERROR':
        return '❌'
      default:
        return 'ℹ️'
    }
  }

  const getActionColor = (action) => {
    if (action.includes('STARTED')) return '#3b82f6'
    if (action.includes('COMPLETED') || action.includes('GENERATED')) return '#10b981'
    if (action.includes('FAILED') || action.includes('FAILURE')) return '#ef4444'
    if (action.includes('RETRY')) return '#f59e0b'
    if (action.includes('ISSUE')) return '#f97316'
    return '#6b7280'
  }

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      fractionalSecondDigits: 3
    })
  }

  // Group logs by phase
  const logsByPhase = logs.reduce((acc, log) => {
    const phase = log.phase || 'GENERAL'
    if (!acc[phase]) acc[phase] = []
    acc[phase].push(log)
    return acc
  }, {})

  return (
    <div className="result-section">
      <h3>🧠 AI Decision Logs</h3>
      <div className="logs-container">
        <p className="section-description">
          Real-time timeline of AI agent decisions and workflow execution:
        </p>
        
        <div className="logs-timeline">
          {Object.entries(logsByPhase).map(([phase, phaseLogs], index) => (
            <div key={index} className="timeline-phase">
              <div className="phase-header">
                <span className="phase-icon">{getPhaseIcon(phase)}</span>
                <span className="phase-name">{phase}</span>
                <span className="phase-count">{phaseLogs.length} events</span>
              </div>
              
              <div className="phase-logs">
                {phaseLogs.map((log, logIndex) => (
                  <div key={logIndex} className="log-entry">
                    <div className="log-timestamp">
                      {formatTimestamp(log.timestamp)}
                    </div>
                    <div className="log-content">
                      <div 
                        className="log-action-badge"
                        style={{ borderLeftColor: getActionColor(log.action) }}
                      >
                        {log.action}
                      </div>
                      <div className="log-message">
                        {log.message || log.description || log.output}
                      </div>
                      
                      {/* Additional details for specific log types */}
                      {log.step_number !== undefined && (
                        <div className="log-detail">
                          <strong>Step:</strong> {log.step_number}
                        </div>
                      )}
                      
                      {log.retry_count !== undefined && (
                        <div className="log-detail retry-info">
                          <strong>Retry Count:</strong> {log.retry_count}
                        </div>
                      )}
                      
                      {log.error && (
                        <div className="log-detail error-info">
                          <strong>Error:</strong> {log.error}
                        </div>
                      )}
                      
                      {log.severity && (
                        <div className={`log-detail severity-${log.severity.toLowerCase()}`}>
                          <strong>Severity:</strong> {log.severity}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default AIDecisionLogs
