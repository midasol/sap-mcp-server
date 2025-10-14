# 🚀 AI Order Inquiry Chatbot - Setup Guide

Quick start guide to get the chatbot running in 5 minutes.

## ✅ Prerequisites Checklist

- [ ] Python 3.11 or higher installed
- [ ] Google Gemini API key (get from https://aistudio.google.com/app/apikey)
- [ ] SAP Gateway credentials (host, username, password)
- [ ] Terminal/command line access

## 📥 Installation Steps

### Step 1: Install Dependencies

```bash
# Install Google Gemini SDK
pip install google-genai

# Verify installation
python -c "from google import genai; print('✓ Gemini SDK installed')"
```

### Step 2: Set Environment Variables

**On macOS/Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"

# Verify
echo $GEMINI_API_KEY
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"

# Verify
echo $env:GEMINI_API_KEY
```

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here

# Verify
echo %GEMINI_API_KEY%
```

### Step 3: Configure SAP Settings

Edit `order_inquiry_chatbot.py` and update the SAP configuration (around line 320):

```python
sap_config = {
    "host": "your-sap-server.com",      # Your SAP server hostname
    "username": "your-username",         # Your SAP username
    "password": "your-password",         # Your SAP password
    "client": "100",                     # SAP client number
    "service": "Z_SALES_ORDER_GENAI_SRV",  # OData service name
    "entity_set": "zsd004Set",           # Entity set name
}
```

## 🎮 Running the Chatbot

### Interactive Mode (Recommended)

```bash
python order_inquiry_chatbot.py
```

**Expected output:**
```
============================================================
🤖 AI Order Inquiry Chatbot Started
============================================================

💡 Enter 'quit' or 'exit' to stop

👤 You: _
```

**Example conversation:**
```
👤 You: 주문 번호 91000092 정보 알려줘

🤔 Analyzing query: '주문 번호 91000092 정보 알려줘'
✅ Extracted Order ID: 91000092

📡 Retrieving order information from SAP...
✅ Order data retrieved successfully

🤖 Chatbot:

📦 주문 정보 (Order Information)
==================================================

🔢 주문 번호 (Order ID): 91000092
📝 고객 주문 번호 (Customer PO): 2410_110440_01
📋 주문 유형 (Order Type): ZEX
...
```

### Test Mode (Automated)

Run predefined test queries without manual input:

```bash
python test_chatbot.py
```

**What it does:**
- Tests 6 different query formats
- Korean and English variations
- Success and failure cases
- Displays all responses

## 🧪 Testing

### Test Query 1: Korean Formal
```
👤 You: 주문 번호 91000092에 대한 정보를 알려줘
```

### Test Query 2: English Formal
```
👤 You: Can you check order 91000092?
```

### Test Query 3: Korean Casual
```
👤 You: 91000092 주문 상태 확인해줘
```

### Test Query 4: Just the Number
```
👤 You: 91000092
```

### Test Query 5: No Order ID (Should Fail)
```
👤 You: 주문 정보 알려줘

Expected Response:
❌ 주문 번호를 찾을 수 없습니다.
다음과 같은 형식으로 질문해주세요:
- "주문 번호 91000092에 대한 정보 알려줘"
...
```

## 🔧 Troubleshooting

### Issue 1: "GEMINI_API_KEY environment variable not set"

**Symptoms:**
```
❌ Error: GEMINI_API_KEY environment variable not set
```

**Solution:**
```bash
# Check if variable is set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your-api-key-here"

# Add to .bashrc or .zshrc for persistence
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
```

### Issue 2: "SAP authentication failed"

**Symptoms:**
```
❌ SAP authentication failed
```

**Solutions:**
1. **Verify credentials** in `sap_config`
2. **Check SAP server connectivity**:
   ```bash
   ping your-sap-server.com
   ```
3. **Ensure MCP server is running**:
   ```bash
   python -m sap_mcp.stdio_server
   ```
4. **Check SAP user permissions** for OData service access

### Issue 3: "No order ID found in query"

**Symptoms:**
```
❌ No order ID found in query
```

**Solutions:**
- Include order number in your query
- Use 8-digit format: `91000092`
- Try explicit format: "주문 번호 91000092" or "order 91000092"

**Valid Examples:**
- ✅ "주문 번호 91000092 정보"
- ✅ "order 91000092"
- ✅ "91000092"
- ❌ "주문 정보" (no number)
- ❌ "order info" (no number)

### Issue 4: "Order data not found"

**Symptoms:**
```
❌ 주문 번호 91000092에 대한 정보를 찾을 수 없습니다.
```

**Solutions:**
1. **Verify order exists** in SAP system
2. **Check service configuration**:
   - `service`: "Z_SALES_ORDER_GENAI_SRV"
   - `entity_set`: "zsd004Set"
3. **Verify user has access** to the OData service
4. **Try a different order ID** that you know exists

### Issue 5: ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'google.genai'
```

**Solution:**
```bash
pip install google-genai

# Or with specific version
pip install google-genai==0.2.0
```

### Issue 6: SSL Certificate Errors

**Symptoms:**
```
SSLCertVerificationError: certificate verify failed
```

**Solution:**
Already handled in the SAP client with `verify_ssl=False` for development.

For production, install proper SSL certificates.

## 📚 Next Steps

Once the chatbot is working:

1. **Customize Response Format**
   - Edit `format_order_response()` in `order_inquiry_chatbot.py`
   - Add/remove fields
   - Change emoji indicators
   - Adjust language labels

2. **Add More Query Types**
   - Modify Gemini system instruction
   - Support date ranges
   - Support customer filters
   - Support status queries

3. **Integrate with Other Systems**
   - Add Slack bot interface
   - Create web UI
   - Add database for chat history
   - Implement caching

4. **Production Deployment**
   - Set up proper secret management
   - Configure monitoring
   - Add rate limiting
   - Implement logging

## 🎯 Quick Reference

### Start Interactive Chat
```bash
python order_inquiry_chatbot.py
```

### Run Tests
```bash
python test_chatbot.py
```

### Check Environment
```bash
# Check Python version
python --version

# Check Gemini API key
echo $GEMINI_API_KEY

# Test MCP server
python -m sap_mcp.stdio_server
```

### Stop Chatbot
```
Type: quit
Or press: Ctrl+C
```

## 💡 Tips

1. **Fast Testing**: Use `test_chatbot.py` for quick validation
2. **Interactive Mode**: Best for demonstrations and real usage
3. **Log Inspection**: Check console output for detailed debugging
4. **Order IDs**: Use 8-digit numbers for best results
5. **Multi-Language**: Mix Korean and English in same session

## 📞 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review [ORDER_CHATBOT_README.md](ORDER_CHATBOT_README.md)
3. Review [CHATBOT_ARCHITECTURE.md](CHATBOT_ARCHITECTURE.md)
4. Check SAP MCP server logs
5. Verify Gemini API quota and limits

## 🎉 Success Criteria

You should be able to:
- ✅ Start the chatbot without errors
- ✅ Extract order IDs from natural language
- ✅ Retrieve order data from SAP
- ✅ Display formatted order information
- ✅ Handle both Korean and English queries
- ✅ See proper error messages for invalid inputs

If all criteria are met, your chatbot is ready to use! 🚀
