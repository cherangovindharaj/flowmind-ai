import React from 'react'

function MonitoringIssues({ issues }) {
  if (!issues || issues.length === 0) {
    return (
      <div className="result-section">
        <h3>🔍 Monitoring Issues</h3>
        <div className="monitoring-container clean">
          <p>✅ No issues detected during workflow execution.</p>
        </div>
      </div>
    )
  }

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return '🔴'
      case 'high':
        return '🟠'
      case 'medium':
        return '🟡'
      case 'low':
        return '🔵'
      default:
        return '⚪'
    }
  }

  const getSeverityClass = (severity) => {
    return `issue-${severity}`
  }

  return (
    <div className="result-section">
      <h3>🔍 Monitoring Issues</h3>
      <div className="monitoring-container">
        <p className="section-description">
          Detected {issues.length} issue{issues.length !== 1 ? 's' : ''} that require attention:
        </p>
        <div className="issues-list">
          {issues.map((issue, index) => (
            <div
              key={index}
              className={`issue-card ${getSeverityClass(issue.severity)}`}
            >
              <div className="issue-header">
                <span className="severity-icon">
                  {getSeverityIcon(issue.severity)}
                </span>
                <span className="severity-badge">{issue.severity.toUpperCase()}</span>
              </div>
              <div className="issue-body">
                <p className="issue-description">{issue.description}</p>
                {issue.affected_step && (
                  <p className="issue-step">Affected Step: {issue.affected_step}</p>
                )}
                <p className="issue-recommendation">
                  <strong>Recommendation:</strong> {issue.recommendation}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default MonitoringIssues
