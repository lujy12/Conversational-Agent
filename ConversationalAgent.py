import os
import json
import requests
import csv
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.environ.get("API_KEY", os.getenv('OPTOGPT_API_KEY'))
BASE_URL = os.environ.get("BASE_URL", os.getenv('BASE_URL'))
LLM_MODEL = os.environ.get("LLM_MODEL", os.getenv('OPTOGPT_MODEL'))
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# Weather Tools
def get_current_weather(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    weather_info = data["current"]
    return json.dumps({
        "location": data["location"]["name"],
        "temperature_c": weather_info["temp_c"],
        "condition": weather_info["condition"]["text"],
    })

def get_weather_forecast(location, days=3):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    forecast = [{
        "date": day["date"],
        "max_temp_c": day["day"]["maxtemp_c"],
        "condition": day["day"]["condition"]["text"]
    } for day in data["forecast"]["forecastday"]]
    return json.dumps({"location": data["location"]["name"], "forecast": forecast})

# Calculator Tool
def calculator(expression):
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# Web Search Tool
def web_search(query):
    search_db = {
        "weather forecast": "Weather forecasts predict atmospheric conditions.",
        "temperature conversion": "C to F: (C × 9/5) + 32, F to C: (F - 32) × 5/9",
    }
    return json.dumps({"query": query, "result": search_db.get(query.lower(), "No relevant info found.")})

# Define Tools
weather_tools = [{
    "type": "function",
    "function": {"name": "get_current_weather", "parameters": {"location": "string"}}
}, {
    "type": "function",
    "function": {"name": "get_weather_forecast", "parameters": {"location": "string", "days": "integer"}}
}]

calculator_tool = {"type": "function", "function": {"name": "calculator", "parameters": {"expression": "string"}}}
search_tool = {"type": "function", "function": {"name": "web_search", "parameters": {"query": "string"}}}

cot_tools = weather_tools + [calculator_tool]
react_tools = cot_tools + [search_tool]

available_functions = {
    "get_current_weather": get_current_weather,
    "get_weather_forecast": get_weather_forecast,
    "calculator": calculator,
    "web_search": web_search,
}

def process_messages(client, messages, tools=None):
    tools = tools or []
    response = client.chat.completions.create(model=LLM_MODEL, messages=messages, tools=tools)
    messages.append(response.choices[0].message)
    return messages

def run_conversation(client, system_message, tools):
    messages = [{"role": "system", "content": system_message}]
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        messages.append({"role": "user", "content": user_input})
        messages = process_messages(client, messages, tools)
        print(f"Assistant: {messages[-1]['content']}")

def run_comparison():
    user_input = input("Enter a query: ")
    agents = [
        ("Basic", "You are a helpful assistant.", weather_tools),
        ("Chain of Thought", "Use step-by-step reasoning.", cot_tools),
        ("ReAct", "Think before you act and retrieve relevant data.", react_tools),
    ]
    responses = {}
    for name, system_msg, tools in agents:
        messages = [{"role": "system", "content": system_msg}, {"role": "user", "content": user_input}]
        messages = process_messages(client, messages, tools)
        responses[name] = messages[-1]["content"]
        print(f"\n{name} Agent: {messages[-1]['content']}")
    
    ratings = {}
    for name in responses:
        rating = input(f"Rate response from {name} (1-5): ")
        ratings[name] = rating
    
    with open("agent_ratings.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Agent", "Response", "Rating"])
        for name, response in responses.items():
            writer.writerow([name, response, ratings[name]])
    print("Ratings saved to agent_ratings.csv")

if __name__ == "__main__":
    choice = input("Choose agent (1: Basic, 2: CoT, 3: ReAct, 4: Compare): ")
    if choice == "1":
        run_conversation(client, "You are a helpful weather assistant.", weather_tools)
    elif choice == "2":
        run_conversation(client, "Use step-by-step reasoning.", cot_tools)
    elif choice == "3":
        run_conversation(client, "Think before you act and retrieve relevant data.", react_tools)
    elif choice == "4":
        run_comparison()
    else:
        print("Invalid choice.")
