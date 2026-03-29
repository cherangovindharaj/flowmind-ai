# FlowMind AI – Autonomous Workflow Agent System
Enterprise-grade autonomous workflow execution using multi-agent AI with self-correction and real-time monitoring.

A multi-agent AI system that takes a user task, breaks it into steps, executes them, validates results, and monitors for issues. Built for the "Agentic AI for Autonomous Enterprise Workflows" hackathon.

![FlowMind AI](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![React](https://img.shields.io/badge/react-18.3+-blue)
![FastAPI](https://img.shields.io/badge/fastapi-0.115-green)

## 🎯 Project Overview

FlowMind AI is an end-to-end autonomous workflow execution system that leverages multiple specialized AI agents to complete enterprise tasks:

- **Planner Agent**: Uses LLM (Groq LLM API) to break down tasks into actionable steps
- **Executor Agent**: Simulates execution of each step with automatic retry on failure
- **Validator Agent**: Uses LLM to assess correctness of execution results
- **Monitor Agent**: Detects failures, anomalies, and issues throughout the workflow

## 🏗️ System Architecture

```
┌─────────────────┐
│   User Input    │
│  (Task String)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Planner Agent  │──► Creates workflow plan (4-8 steps)
│    (LLM-based)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Executor Agent  │──► Executes steps with retry logic
│  (Simulation)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Validator Agent │──► Validates execution results
│    (LLM-based)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Monitor Agent  │──► Detects issues & anomalies
│   (Rule-based)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Results  │
│  (JSON Response)│
└─────────────────┘
```

## ✨ Features

### Core Features
- ✅ **Multi-Agent Architecture**: Four specialized agents working in sequence
- ✅ **LLM Integration**: Groq LLM API-4o-mini for planning and validation
- ✅ **Automatic Retry**: Executor retries failed steps (configurable, default: 2 retries)
- ✅ **Comprehensive Logging**: File and console logging for debugging
- ✅ **Real-time Monitoring**: Issue detection with severity classification
- ✅ **Clean REST API**: FastAPI backend with CORS support
- ✅ **Modern UI**: React-based frontend with intuitive display

### Additional Features
- Modular agent design for easy extension
- Structured JSON prompts for reliable LLM responses
- Graceful error handling
- Execution time tracking
- Confidence scoring for validation

## 📁 Project Structure

```
flowmind-ai/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── agents/
│   │   ├── base_agent.py       # Abstract base class
│   │   ├── planner_agent.py    # Task breakdown
│   │   ├── executor_agent.py   # Step execution
│   │   ├── validator_agent.py  # Result validation
│   │   └── monitor_agent.py    # Issue detection
│   ├── services/
│   │   ├── llm_service.py      # Groq LLM API wrapper
│   │   └── workflow_service.py # Agent orchestration
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── utils/
│   │   └── logger.py           # Logging setup
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx             # Main app component
│       ├── main.jsx            # React entry point
│       ├── styles.css          # Global styles
│       └── components/
│           ├── WorkflowInput.jsx
│           ├── PlanDisplay.jsx
│           ├── ExecutionResults.jsx
│           ├── ValidationResult.jsx
│           └── MonitoringIssues.jsx
└── README.md
```

## 🔒 Security & Environment Variables

### Managing API Keys Securely

**⚠️ IMPORTANT:** Never commit sensitive credentials to Git!

> Sensitive credentials are managed using environment variables and are not included in the repository.

The project uses a `.env` file for local configuration, which is excluded from version control via `.gitignore`.

### Setup Instructions

1. **Copy the example environment file:**
   ```bash
   cd backend
   copy .env.example .env
   ```

2. **Edit `.env` and add your actual API key:**
   ```
   Groq LLM API_API_KEY=sk-your-actual-api-key-here
   Groq LLM API_MODEL=gpt-4o-mini
   HOST=0.0.0.0
   PORT=8000
   LOG_LEVEL=INFO
   ```

3. **Verify `.env` is ignored by Git:**
   ```bash
   git status
   ```
   
   The `.env` file should NOT appear in the list of tracked files.

### What's Protected

The following are automatically ignored by `.gitignore`:
- ✅ `.env` files (all environments)
- ✅ `venv/` directories
- ✅ `node_modules/` directories
- ✅ Log files
- ✅ Python cache (`__pycache__/`)
- ✅ IDE settings

### For Production Deployment

Use proper secrets management:
- Environment variables from your hosting provider
- AWS Secrets Manager / Azure Key Vault
- Kubernetes Secrets
- Docker secrets

**NEVER** hardcode API keys in source code!

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Groq LLM API API Key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables:**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your Groq LLM API API key:
   ```
   Groq LLM API_API_KEY=sk-your-actual-api-key-here
   Groq LLM API_MODEL=gpt-4o-mini
   ```

6. **Run the backend server:**
   ```bash
   python main.py
   ```
   
   The server will start at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will start at `http://localhost:5173`

## 🧪 Usage

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5173`
2. Enter a task description in the input box (e.g., "Onboard a new employee")
3. Click "Run Workflow"
4. Wait for the workflow to execute (may take 10-30 seconds)
5. Review the results:
   - **Plan**: Sequential steps generated by the AI
   - **Execution Results**: Status of each step (success/failure)
   - **Validation**: AI assessment of overall workflow success
   - **Monitoring Issues**: Any detected problems or anomalies

### API Usage

**Endpoint:** `POST /run-workflow`

**Request Body:**
```json
{
  "task": "Onboard a new employee",
  "max_retries": 2
}
```

**Response:**
```json
{
  "task": "Onboard a new employee",
  "plan": [
    {
      "step_number": 1,
      "description": "Collect employee personal information and documents",
      "status": "completed"
    },
    {
      "step_number": 2,
      "description": "Create company email account",
      "status": "completed"
    },
    {
      "step_number": 3,
      "description": "Set up workspace and equipment",
      "status": "completed"
    },
    {
      "step_number": 4,
      "description": "Add employee to payroll system",
      "status": "completed"
    },
    {
      "step_number": 5,
      "description": "Schedule orientation and training sessions",
      "status": "completed"
    },
    {
      "step_number": 6,
      "description": "Grant system access permissions",
      "status": "completed"
    }
  ],
  "execution_results": [
    {
      "step_number": 1,
      "description": "Collect employee personal information and documents",
      "status": "success",
      "output": "Successfully collected all required information for step 1",
      "retry_count": 0,
      "execution_time": 0.85
    }
    // ... more results
  ],
  "validation_result": {
    "is_valid": true,
    "confidence_score": 0.95,
    "reasoning": "All critical steps completed successfully. The workflow achieved 100% completion rate with no failed steps.",
    "failed_steps": []
  },
  "monitoring_issues": [],
  "execution_id": "abc123-def456-ghi789",
  "started_at": "2026-03-26T10:30:00Z",
  "completed_at": "2026-03-26T10:30:15Z",
  "total_duration_seconds": 15.23
}
```

### Example Tasks

Try these example tasks:
- "Onboard a new employee"
- "Process customer refund request"
- "Schedule team building event"
- "Set up new client account"
- "Organize company meeting"
- "Create marketing campaign"

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `Groq LLM API_API_KEY` | Your Groq LLM API API key | Required |
| `Groq LLM API_MODEL` | Groq LLM API model to use | `gpt-4o-mini` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Frontend Configuration

The frontend is pre-configured to connect to `http://localhost:8000`. To change this:

1. Edit `frontend/src/App.jsx`
2. Modify the `API_BASE_URL` constant

## 🧠 How It Works

### 1. Planning Phase
The Planner Agent receives the task and uses the LLM to generate a structured plan with 4-8 sequential steps. The LLM is prompted to return clean JSON output.

### 2. Execution Phase
The Executor Agent processes each step:
- Simulates realistic execution with random delays (0.5-1.5s)
- 90% success rate simulation (for demo purposes)
- Automatically retries failed steps up to 2 times
- Generates context-aware success/error messages

### 3. Validation Phase
The Validator Agent analyzes execution results using the LLM:
- Reviews all step outcomes
- Considers success rate and critical failures
- Returns pass/fail judgment with confidence score
- Provides detailed reasoning

### 4. Monitoring Phase
The Monitor Agent applies rule-based analysis:
- Detects failed steps (critical/high severity)
- Identifies retry patterns (medium/high severity)
- Flags slow executions (low severity)
- Checks for incomplete workflows (critical)

## 🛠️ Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is available

### Frontend won't connect to backend
- Verify backend is running at `http://localhost:8000`
- Check CORS settings in `backend/main.py`
- Ensure frontend proxy configuration in `vite.config.js`

### LLM errors
- Verify `Groq LLM API_API_KEY` is set in `.env`
- Check API key validity on Groq LLM API dashboard
- Ensure internet connectivity

### Import errors
- Make sure you're running from the correct directory
- Verify Python path includes the backend folder
- Reinstall dependencies if needed

## 📊 Demo Flow

**Input Task:** "Onboard a new employee"

**Expected Output:**
1. **Plan Generation**: 6 steps for employee onboarding
2. **Execution**: Each step executed with simulated success/failure
3. **Validation**: LLM confirms successful onboarding process
4. **Monitoring**: Flags any incomplete setups or access issues

**Typical Execution Time:** 10-20 seconds

## 🎨 Customization

### Adding New Agents
1. Create new agent class inheriting from `BaseAgent`
2. Implement the `execute()` method
3. Register in `workflow_service.py`

### Changing LLM Model
Edit `backend/.env`:
```
Groq LLM API_MODEL=gpt-4o  # or gpt-3.5-turbo
```

### Adjusting Retry Logic
Edit `backend/services/workflow_service.py`:
```python
workflow_service = WorkflowService(max_retries=3)  # Change from default 2
```

## 📝 License

This project is created for hackathon purposes. Feel free to use and modify.

## 👥 Credits

**Built with:**
- FastAPI - Modern Python web framework
- React - JavaScript UI library
- Vite - Next generation frontend tooling
- Groq LLM API - Language model provider

**Hackathon:** Agentic AI for Autonomous Enterprise Workflows

## 🚀 Future Enhancements

Potential features for future versions:
- Real API integrations (email, HR systems, etc.)
- Persistent workflow history
- Advanced analytics dashboard
- Custom workflow templates
- Multi-tenant support
- WebSocket support for real-time updates
- Human-in-the-loop approval steps

---

**Ready to build autonomous workflows with FlowMind AI! 🚀**
