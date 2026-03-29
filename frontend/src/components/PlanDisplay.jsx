import React from 'react'

function PlanDisplay({ plan }) {
  if (!plan || plan.length === 0) {
    return null
  }

  return (
    <div className="result-section">
      <h3>🧠 AI Planning Phase</h3>
      <div className="plan-container">
        <p className="section-description">
          The AI planner broke down your task into {plan.length} sequential steps:
        </p>
        <ol className="plan-list">
          {plan.map((step, index) => (
            <li key={index} className="plan-step">
              <span className="step-number">{step.step_number}</span>
              <span className="step-description">{step.description}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  )
}

export default PlanDisplay
