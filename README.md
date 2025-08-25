# Twilio-Deepgram Voice Agent

A WebSocket server that bridges Twilio phone calls with Deepgram's Voice Agent API, enabling callers to interact with an AI-powered voice assistant through any phone number.

## Overview

This application creates a real-time voice agent that can:
- Answer phone calls through Twilio
- Convert speech to text using Deepgram's Nova-3 model
- Process conversations with OpenAI's GPT-4o-mini
- Respond with natural speech using Deepgram's Aura TTS
- Handle call interruptions and barge-in scenarios

## Prerequisites

### Required Accounts & Services
1. **Twilio Account**: [Sign up for free](https://www.twilio.com/try-twilio)
   - Active Twilio phone number (free tier works)
2. **Deepgram Account**: [Get API key](https://console.deepgram.com/signup?jump=keys)
3. **OpenAI Account**: API access for GPT-4o-mini model
4. **ngrok** (for local development): [Download here](https://ngrok.com/)

### System Requirements
- Python 3.7+
- Internet connection for API calls

## Installation

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/Daxrajsinh-holboxai/AI-voice-assistant-twilio-deegram-openai.git
cd twilio-deepgram-voice-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```bash
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

**Alternative**: Set environment variable directly
```bash
export DEEPGRAM_API_KEY="your_deepgram_api_key_here"
```



## Twilio Configuration

### 1. Create TwiML Bin
In your [Twilio Console](https://console.twilio.com/), create a TwiML Bin with:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="en">This call may be monitored or recorded.</Say>
    <Connect>
        <Stream url="wss://your-ngrok-domain.ngrok-free.app/twilio" />
    </Connect>
</Response>
```

**Note**: Replace `your-ngrok-domain.ngrok-free.app` with your actual ngrok static domain.

### 2. Configure Phone Number
1. Go to **Phone Numbers** → **Manage** → **Active numbers**
2. Select your Twilio phone number
3. In the **Voice Configuration** section:
   - Set "A call comes in" to "TwiML Bin"
   - Select the TwiML Bin you created above
4. Save the configuration

## Running the Application

### 1. Start the Server
```bash
python main.py
```

The server will start on `ws://localhost:5000`

### 2. Expose Server (for local development)
In a new terminal, start ngrok with your static domain:
```bash
ngrok http --domain=your-ngrok-domain.ngrok-free.app 5000
```

Update your TwiML Bin URL to use your static ngrok domain:
```
wss://your-ngrok-domain.ngrok-free.app/twilio
```

**Note**: Replace `your-ngrok-domain.ngrok-free.app` with your actual ngrok static domain.

### 3. Test the Integration
Call your Twilio phone number. You should:
1. Hear the monitoring message
2. Be connected to the voice agent
3. Hear the greeting: "Hello! How can I help you today?"
4. Be able to have a conversation with the AI assistant

## Configuration Options

### Voice Agent Settings
The agent configuration in `main.py` can be customized:

```python
config_message = {
    "agent": {
        "language": "en",
        "listen": {
            "provider": {
                "type": "deepgram",
                "model": "nova-3",  # Speech recognition model
                "keyterms": ["hello", "goodbye"]  # Important words to detect
            }
        },
        "think": {
            "provider": {
                "type": "open_ai",
                "model": "gpt-4o-mini",  # AI model for responses
                "temperature": 0.7  # Response creativity (0-1)
            },
            "prompt": "You are a helpful AI assistant focused on customer service."
        },
        "speak": {
            "provider": {
                "type": "deepgram",
                "model": "aura-2-thalia-en"  # Text-to-speech voice
            }
        },
        "greeting": "Hello! How can I help you today?"  # First message
    }
}
```

### Audio Settings
- **Input/Output**: µ-law encoding at 8kHz (Twilio standard)
- **Buffer Size**: 20 messages (0.4 seconds) for optimal performance

## Features

### Real-time Processing
- **Speech Recognition**: Deepgram Nova-3 model
- **AI Responses**: OpenAI GPT-4o-mini
- **Text-to-Speech**: Deepgram Aura TTS
- **Barge-in Support**: Interrupts AI when user starts speaking

### Call Management
- **Connection Handling**: Automatic WebSocket management
- **Audio Buffering**: Optimized for Twilio's 20ms audio chunks
- **Error Recovery**: Graceful handling of connection issues

## Troubleshooting

### Common Issues

**"DEEPGRAM_API_KEY environment variable is not set"**
- Ensure your `.env` file exists with the correct API key
- Or set the environment variable directly

**Connection refused on localhost:5000**
- Make sure the server is running with `python main.py`
- Check if port 5000 is available

**Twilio webhook errors**
- Verify your ngrok URL is correct in the TwiML Bin
- Ensure ngrok is running and forwarding to port 5000
- Check that the URL uses `wss://` (WebSocket Secure)

**No audio or response from agent**
- Verify your Deepgram API key has sufficient credits
- Check the console output for error messages
- Ensure your OpenAI API access is working

### Debug Mode
Monitor the console output for real-time conversation logs:
- 🟢 **User**: Messages from the caller
- 🔵 **Assistant**: AI responses

## Production Deployment

For production use:

1. **SSL Certificate**: Uncomment SSL configuration in `main.py`
2. **Domain**: Replace ngrok with a proper domain
3. **Environment Variables**: Use secure environment variable management
4. **Error Handling**: Add comprehensive logging and error recovery
5. **Load Balancing**: Consider multiple server instances for high traffic

## Support

- **Issues**: [Create an issue](https://github.com/your-repo/issues)
- **Deepgram Community**: [GitHub Discussions](https://github.com/orgs/deepgram/discussions)
- **Discord**: [Deepgram Discord](https://discord.gg/xWRaCDBtW4)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This integration requires active API keys and may incur charges based on usage. Monitor your API usage and billing in the respective dashboards.