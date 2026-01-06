# 🤖 AI Customer Support Email Automation

An intelligent email automation system that uses Google's Gemini AI to automatically process customer support emails, extract key information, and generate personalized responses.

## ✨ Features

- **Automated Email Monitoring**: Continuously monitors Gmail inbox for new unread emails via IMAP
- **AI-Powered Email Analysis**: Uses Gemini AI to extract structured information from customer emails:
  - Email category (complaint, refund request, product feedback, inquiry, etc.)
  - Products mentioned
  - Issue description
  - Customer name
- **Intelligent Response Generation**: Automatically generates contextual, friendly, and helpful responses
- **Email Whitelist**: Security feature to only process emails from approved senders
- **Async Processing**: Efficient asynchronous email handling for better performance
- **Auto-Reply**: Sends AI-generated responses back to customers via SMTP

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Customer Support                      │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Gmail      │    │  Gemini AI   │    │   Gmail      │ │
│  │   IMAP       │───▶│  Processing  │───▶│   SMTP       │ │
│  │  (Fetch)     │    │  (Analyze &  │    │  (Send)      │ │
│  │              │    │   Generate)  │    │              │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         ▼                    ▼                    ▼         │
│  extraction.py        support.py              main.py      │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose (for containerized setup)
  OR
- Python 3.8+
- Gmail account with IMAP enabled
- Google Gemini API key
- Gmail App Password (for IMAP/SMTP access)

## 🚀 Setup

You can run this project either using Docker (recommended) or locally with Python.

### Option 1: Using Docker (Recommended) 🐳

#### Pull from Docker Hub

```bash
docker pull abhayjha800/ai-customer-support:latest
```

#### Run the Container

```bash
docker run -d \
  --name ai-customer-support \
  -e IMAP_HOST=imap.gmail.com \
  -e SMTP_SERVER=smtp.gmail.com \
  -e EMAIL_USER=your_email@gmail.com \
  -e EMAIL_PASSWORD=your_16_char_app_password \
  -e GOOGLE_API_KEY=your_gemini_api_key_here \
  -v $(pwd)/whitelist.yaml:/app/whitelist.yaml \
  abhayjha800/ai-customer-support:latest
```

#### Using Docker Compose

```bash
# Create .env file with your credentials (see step 6 below)
docker-compose up -d
```

### Option 2: Local Python Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/abhayjha800/AI-Customer-Support.git
cd ai-customer-support
```

#### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure Gmail

1. **Enable IMAP**:
   - Go to [Gmail Settings → Forwarding and POP/IMAP](https://mail.google.com/mail/u/0/#settings/fwdandpop)
   - Enable IMAP access

2. **Generate App Password**:
   - Visit [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Create a new app password for "Mail"
   - Save the 16-character password

#### 5. Get Gemini API Key

- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Copy the key for the next step

#### 6. Create Environment File

Create a `.env` file in the project root:

```env
# Email Configuration
IMAP_HOST=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# Gemini AI Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
```

#### 7. Configure Whitelist

Edit `whitelist.yaml` to specify allowed sender emails:

```yaml
whitelist:
  - customer1@example.com
  - customer2@example.com
  - support@company.com
```

Or use an empty list to skip whitelist checking:

```yaml
whitelist: []
```

## 📂 Project Structure

```
ai-customer-support/
│
├── extraction.py          # Email fetching and sending (IMAP/SMTP)
├── support.py            # AI processing and response generation
├── main.py              # Main application orchestration
├── requirements.txt     # Python dependencies
├── whitelist.yaml      # Approved email senders
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose setup
├── .env               # Environment variables (create this)
└── README.md         # Project documentation
```

## 🎯 Usage

### Using Docker

```bash
# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

Or using Docker directly:

```bash
# Run the container
docker run -d \
  --name ai-customer-support \
  --env-file .env \
  -v $(pwd)/whitelist.yaml:/app/whitelist.yaml \
  abhayjha800/ai-customer-support:latest

# View logs
docker logs -f ai-customer-support

# Stop the container
docker stop ai-customer-support
```

### Running Locally

#### Run the Application

```bash
python main.py
```

The system will:
1. Connect to your Gmail inbox
2. Check for unread emails every 10 seconds
3. Process emails from whitelisted senders
4. Extract information using Gemini AI
5. Generate and send automated responses
6. Mark processed emails as read

### Sample Output

```
IMAP_HOST: imap.gmail.com
EMAIL_USER: support@company.com
Checking for new emails...
Connecting to imap.gmail.com...
Connected! Logging in...
Login successful! Selecting inbox...
Inbox selected!
Searching for unread emails...
Found 2 unread email(s)
Processing email from customer@example.com...
Reply sent successfully!
```

## 🔧 Configuration

### Email Check Interval

Modify the sleep duration in `main.py`:

```python
await asyncio.sleep(60)  # Check every 60 seconds
```

### AI Model Selection

Change the Gemini model in `main.py`:

```python
ai_support = AICustomerSupport(model="gemini-1.5-flash")
# Options: gemini-1.5-flash, gemini-1.5-pro, gemini-pro
```

### Email Categories

Customize categories in `support.py`:

```python
category: Literal[
    "complaint",
    "refund_request",
    "product_feedback",
    "customer_service_inquiry",
    "others",
]
```

## 🛠️ Technology Stack

- **Docker**: Containerization for easy deployment
- **Python 3.x**: Core programming language
- **LangChain**: LLM orchestration framework
- **Google Gemini AI**: Natural language processing and generation
- **IMAP/SMTP**: Email protocols for fetching and sending
- **Pydantic**: Data validation and structured outputs
- **asyncio**: Asynchronous processing
- **python-dotenv**: Environment variable management
- **PyYAML**: Configuration file parsing

## 📝 How It Works

1. **Email Fetching** (`extraction.py`):
   - Connects to Gmail via IMAP SSL
   - Searches for UNSEEN (unread) emails
   - Retrieves email content and sender information
   - Maintains whitelist for security

2. **AI Processing** (`support.py`):
   - Extracts text from email messages (handles multipart/plain text)
   - Uses Gemini AI to extract structured data (category, products, issue, name)
   - Generates personalized response using a prompt template
   - Returns both extracted data and generated reply

3. **Automation Loop** (`main.py`):
   - Orchestrates email fetching and AI processing
   - Validates senders against whitelist
   - Sends automated responses via SMTP
   - Runs continuously with configurable intervals

## 🔒 Security Considerations

- **Never commit `.env` file** - Add it to `.gitignore`
- **Use App Passwords** - Never use your actual Gmail password
- **Implement Whitelist** - Restrict processing to known senders
- **Monitor API Usage** - Track Gemini API costs and rate limits
- **Review Responses** - Consider adding human review for sensitive cases

## 🚨 Troubleshooting

### Authentication Errors
- Verify App Password is correct (no spaces)
- Ensure 2-Step Verification is enabled on Gmail
- Check that IMAP is enabled in Gmail settings

### API Key Issues
- Verify `GOOGLE_API_KEY` is set correctly in `.env`
- Check API key is valid at [Google AI Studio](https://makersuite.google.com)
- Ensure you have API quota remaining

### Connection Timeouts
- Check your internet connection
- Verify firewall isn't blocking IMAP (port 993) or SMTP (port 587)
- Try increasing timeout in `extraction.py`

### No Emails Detected
- Ensure emails are actually unread
- Check whitelist configuration
- Verify sender addresses match whitelist exactly

## 📊 Future Enhancements

- [ ] Add support for multiple email accounts
- [ ] Implement sentiment analysis for priority routing
- [ ] Add database for tracking email history
- [ ] Create web dashboard for monitoring
- [ ] Support for email attachments
- [ ] Multi-language support
- [ ] Integration with ticketing systems
- [ ] A/B testing for response templates

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Made with ❤️ using Google Gemini AI**