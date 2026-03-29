import React from 'react'

function WorkflowInput({ task, onTaskChange, onRun, loading, disabled }) {
  const handleSubmit = (e) => {
    e.preventDefault()
    onRun()
  }

  return (
    <div className="workflow-input-section">
      <h2>🎯 Enter Your Task</h2>
      <form onSubmit={handleSubmit} className="task-form">
        <div className="input-group">
          <textarea
            value={task}
            onChange={(e) => onTaskChange(e.target.value)}
            placeholder="Enter a task to execute (e.g., 'Onboard a new employee')"
            rows={4}
            disabled={loading || disabled}
            className="task-textarea"
          />
        </div>
        <button
          type="submit"
          disabled={loading || disabled}
          className="run-btn"
        >
          {loading ? '⏳ Running Workflow...' : '▶️ Run Workflow'}
        </button>
      </form>

      <div className="example-tasks">
        <p className="example-label">Example tasks:</p>
        <ul className="example-list">
          <li>Onboard a new employee</li>
          <li>Process customer refund request</li>
          <li>Schedule team building event</li>
          <li>Set up new client account</li>
        </ul>
      </div>
    </div>
  )
}

export default WorkflowInput
