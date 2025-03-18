# Conversational Agent

## Overview
This project implements a chatbot that retrieves weather data, performs calculations, and searches for information using different reasoning methods:
- **Basic Agent**: Provides direct responses using tools.
- **Chain of Thought (CoT) Agent**: Breaks down complex queries step by step.
- **ReAct Agent**: Thinks before retrieving relevant information.

## Setup

### 1. Install Dependencies
```bash
pip install openai requests python-dotenv
```

### 2. Set Up API Keys
- [OpenAI](https://platform.openai.com/)
- [WeatherAPI](https://www.weatherapi.com/)

Create a `.env` file:
```ini
API_KEY=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
BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4
WEATHER_API_KEY=55c14b3518524caa9cc195430251803
```

### 3. Run the Chatbot
```bash
python conversational_agent.py
```
Select an agent:
- **1**: Basic
- **2**: Chain of Thought
- **3**: ReAct
- **4**: Compare all agents

## Example Conversations
**Basic Agent:**
```
User: What's the weather in New York?
Assistant: 12°C, clear skies.
```

**CoT Agent:**
```
User: Temperature difference between Cairo and Paris?
Assistant: Cairo: 30°C, Paris: 18°C → Difference: 12°C
```

**ReAct Agent:**
```
User: Chance of rain in Tokyo tomorrow?
Assistant: Checking forecast... 60% chance of rain.
```

## Conclusion
This chatbot demonstrates different reasoning approaches for better responses. The **Basic Agent** is fast, **CoT** improves clarity, and **ReAct** enhances problem-solving. Future improvements could include real-time web search and advanced NLP.


