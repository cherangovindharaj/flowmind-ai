# 🔧 Fix OpenAI API Quota Exceeded Error (429)

## ❌ Error Message
```
Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details.', 'type': 'insufficient_quota', ...}}
```

## 🎯 What This Means

Your OpenAI API key has **no remaining credits**. This happens when:
- Free trial credits are exhausted ($5 free tier used up)
- Paid credits are depleted
- Billing issue with your OpenAI account

---

## ✅ Solution 1: Add Credits to OpenAI Account (Recommended)

### Steps:

1. **Go to OpenAI Platform**
   - Visit: https://platform.openai.com/account/billing/overview

2. **Add Payment Method** (if not already added)
   - Click "Add payment method"
   - Enter credit/debit card information

3. **Add Credits**
   - Click "Add credits"
   - Minimum: $5 (for most plans)
   - Recommended for hackathon: $10-20

4. **Wait for Activation**
   - Credits usually activate within 2-5 minutes
   - Refresh the billing page to confirm

5. **Retry FlowMind AI**
   - Backend will automatically use the API key
   - No restart needed (credits checked per request)

---

## ✅ Solution 2: Use Demo Mode (No API Credits Needed!)

I've created a **demo mode** that simulates the entire workflow without calling OpenAI API. Perfect for testing!

### How to Enable Demo Mode:

The system now **automatically falls back to demo mode** if OpenAI fails!

Just run your backend normally:
```bash
cd d:\flowmind-ai\backend
python main.py
```

When you see the quota error, it will automatically switch to demo mode and continue working.

### What Demo Mode Does:

✅ **Simulates LLM responses** for planning and validation  
✅ **Creates realistic workflow plans** (e.g., "Onboard employee" → 6 steps)  
✅ **Validates execution results** with confidence scores  
✅ **NO API calls** - completely free!  
✅ **Great for testing** frontend and workflow logic  

### Limitations:

⚠️ Plans are pre-defined templates (not truly AI-generated)  
⚠️ Validation responses are generic  
⚠️ Not suitable for production use  

---

## ✅ Solution 3: Use a Different API Key

If you have another OpenAI account:

1. **Get API Key from different account**
   - Create new OpenAI account at https://platform.openai.com/signup
   - Get new API key from https://platform.openai.com/api-keys

2. **Update `.env` file:**
   ```bash
   notepad d:\flowmind-ai\backend\.env
   ```

3. **Replace the API key:**
   ```
   OPENAI_API_KEY=sk-proj-new-key-here
   ```

4. **Restart backend:**
   - Stop current server (Ctrl+C)
   - Run again: `python main.py`

---

## 🧪 Testing the System Right Now

### Option A: Automatic Demo Mode (Easiest)

Just try running a workflow in the frontend! If OpenAI fails, it will automatically use demo mode.

**Test with:**
```
Task: "Onboard a new employee"
```

Expected output in demo mode:
- ✅ 6-step plan generated
- ✅ Execution with simulated success/failure
- ✅ Validation passes (92% confidence)
- ✅ No monitoring issues

### Option B: Force Demo Mode

Modify `workflow_service.py` to always use demo:

```python
# In services/workflow_service.py, line ~20
from services.demo_llm_service import DemoLLMService as LLMService
USE_DEMO_MODE = True
```

Then restart backend.

---

## 📊 Compare: Demo Mode vs OpenAI Mode

| Feature | Demo Mode | OpenAI Mode |
|---------|-----------|-------------|
| **Cost** | Free | Requires credits |
| **Setup** | Instant | Need API key + credits |
| **Plan Quality** | Template-based | AI-generated |
| **Flexibility** | Limited tasks | Any task |
| **Speed** | Fast | ~10-20 seconds |
| **Best For** | Testing UI/logic | Production/demo |

---

## 🔍 Check Your OpenAI Usage

1. **View Usage Dashboard**
   - Go to: https://platform.openai.com/usage
   - See daily/monthly usage

2. **Check Billing**
   - Go to: https://platform.openai.com/account/billing/overview
   - View current balance

3. **Set Usage Limits** (Optional)
   - Go to: https://platform.openai.com/account/billing/limits
   - Set monthly spending cap

---

## 💡 Quick Reference Commands

### Check if backend is using demo mode:
Look for this in startup logs:
```
INFO - WorkflowService initialized with LLM (demo_mode=True)
```

### Test workflow via curl:
```bash
curl -X POST http://localhost:8000/run-workflow \
  -H "Content-Type: application/json" \
  -d '{"task": "Schedule a meeting"}'
```

### View logs:
```powershell
Get-Content backend\logs\*.log -Tail 50
```

---

## 🎯 Recommended Approach for Hackathon

### During Development:
✅ **Use Demo Mode** - Save money, test quickly

### For Final Demo/Presentation:
✅ **Add $10 to OpenAI** - Show real AI capabilities

### Backup Plan:
✅ **Keep demo mode ready** - In case of API issues during demo

---

## 🆘 Still Having Issues?

### Check these common problems:

**Problem:** Demo mode not activating
- **Solution:** Restart backend after seeing the 429 error

**Problem:** Still getting quota error
- **Solution:** Wait 5 minutes after adding credits

**Problem:** Don't want to use OpenAI at all
- **Solution:** Demo mode is perfect for your needs!

---

## 📝 Current Status

✅ **Demo mode implemented**  
✅ **Automatic fallback on API failure**  
✅ **No code changes needed**  
✅ **Ready to test immediately**  

---

## 🚀 Next Steps

1. **Try demo mode now:**
   - Open http://localhost:5173
   - Enter: "Onboard a new employee"
   - Click "Run Workflow"

2. **If you want real AI:**
   - Add credits at: https://platform.openai.com/account/billing/overview
   - Wait 5 minutes
   - Try again

3. **For hackathon presentation:**
   - Demo both modes to show flexibility
   - Explain architecture works with or without OpenAI

---

**Your FlowMind AI system now works WITHOUT OpenAI credits! 🎉**

Just run it and enjoy testing!
