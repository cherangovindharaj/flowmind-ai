import { useState } from 'react'
import axios from 'axios'
import WorkflowInput from './components/WorkflowInput'
import PlanDisplay from './components/PlanDisplay'
import ExecutionResults from './components/ExecutionResults'
import ValidationResult from './components/ValidationResult'
import MonitoringIssues from './components/MonitoringIssues'
import AIDecisionLogs from './components/AIDecisionLogs'
import ImpactMetrics from './components/ImpactMetrics'
import './styles.css'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [task, setTask] = useState('')
  const [workflowData, setWorkflowData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const runWorkflow = async () => {
    if (!task.trim()) {
      setError('Please enter a task description')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_BASE_URL}/run-workflow`, {
        task: task,
        max_retries: 2,
      })

      setWorkflowData(response.data)
    } catch (err) {
      console.error('Workflow execution failed:', err)
      setError(err.response?.data?.detail || 'Failed to execute workflow. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const clearResults = () => {
    setWorkflowData(null)
    setTask('')
    setError(null)
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 FlowMind AI</h1>
        <p className="subtitle">Autonomous Workflow Agent System</p>
        <p className="tagline">Autonomously executes enterprise workflows using multi-agent AI with self-correction and validation.</p>
        {workflowData?.metadata?.demo_mode && (
          <div className="demo-mode-badge" title="Running in demo mode - no API costs">
            🎭 Demo Mode
          </div>
        )}
      </header>

      <main className="main-content">
        <WorkflowInput
          task={task}
          onTaskChange={setTask}
          onRun={runWorkflow}
          loading={loading}
          disabled={loading}
        />

        {error && (
          <div className="error-container">
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          </div>
        )}

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Executing workflow... This may take a moment.</p>
          </div>
        )}

        {workflowData && !loading && (
          <div className="results-container">
            <div className="results-header">
              <h2>🚀 Autonomous Execution Report</h2>
              <button className="clear-btn" onClick={clearResults}>
                Clear Results
              </button>
            </div>

            <div className="result-section">
              <h3>📋 Task</h3>
              <div className="task-display">{workflowData.task}</div>
            </div>

            <PlanDisplay plan={workflowData.plan} />

            {/* Enhanced Execution Summary */}
            {workflowData.execution?.summary && (
              <div className="result-section">
                <h3>🧠 Execution Intelligence Dashboard</h3>
                <div className="execution-metrics">
                  <div className="metric-card">
                    <div className="metric-value">{workflowData.execution.summary.total_steps}</div>
                    <div className="metric-label">Total Steps</div>
                  </div>
                  <div className="metric-card success">
                    <div className="metric-value">{workflowData.execution.summary.successful}</div>
                    <div className="metric-label">Successful</div>
                  </div>
                  <div className="metric-card failed">
                    <div className="metric-value">{workflowData.execution.summary.failed}</div>
                    <div className="metric-label">Failed</div>
                  </div>
                  <div className="metric-card retried">
                    <div className="metric-value">{workflowData.execution.summary.retried}</div>
                    <div className="metric-label">Retried</div>
                  </div>
                </div>
              </div>
            )}

            {/* Business Impact Metrics */}
            <ImpactMetrics />

            <ExecutionResults results={workflowData.execution?.results || workflowData.execution_results} />

            <ValidationResult validation={workflowData.validation} />

            <MonitoringIssues issues={workflowData.monitoring_issues} />

            <AIDecisionLogs logs={workflowData.logs} />

            <div className="execution-info">
              <div className="info-item">
                <strong>Execution ID:</strong> {workflowData.metadata?.execution_id || workflowData.execution_id}
              </div>
              <div className="info-item">
                <strong>Duration:</strong> {(workflowData.metadata?.total_duration_seconds || workflowData.total_duration_seconds || 0).toFixed(2)}s
              </div>
              <div className="info-item">
                <strong>Workflow Type:</strong> {workflowData.metadata?.workflow_type || 'Unknown'}
              </div>
              <div className="info-item">
                <strong>Mode:</strong> {workflowData.metadata?.demo_mode ? '🎭 Demo' : '🤖 Live'}
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>FlowMind AI </p>
      </footer>
    </div>
  )
}

export default App
