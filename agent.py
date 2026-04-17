import os
import json
import time
import anthropic
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from tools import search_web_period, search_reddit_period, get_trend_context

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-haiku-4-5-20251001"

TOOLS = [
    {
        "name": "search_web_period",
        "description": "Search the web for content about a topic in a specific year or time period.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The topic to search for"},
                "year": {"type": "string", "description": "The year or time period to search within"}
            },
            "required": ["query", "year"]
        }
    },
    {
        "name": "search_reddit_period",
        "description": "Search Reddit discussions about a topic in a specific year.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The topic to search for"},
                "year": {"type": "string", "description": "The year to search within"}
            },
            "required": ["query", "year"]
        }
    },
    {
        "name": "get_trend_context",
        "description": "Get articles and analysis about how a topic has trended between two time periods.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The topic to analyze"},
                "year_from": {"type": "string", "description": "The starting year"},
                "year_to": {"type": "string", "description": "The ending year"}
            },
            "required": ["query", "year_from", "year_to"]
        }
    }
]


def run_single_agent(topic: str, year: str, role: str) -> str:
    system_prompt = f"""You are a cultural research analyst studying the {role} period ({year}).
Your job is to research how people talked about, thought about, and engaged with: {topic}

Search the web and Reddit to find:
- What language and vocabulary people used
- What values and concerns were associated with this topic
- Who the key communities and demographics were
- What the dominant narratives and attitudes were
- Any notable products, brands, or movements

Be specific and concrete. Quote actual language you find.
Return a concise research summary as plain text. Be brief but specific."""

    messages = [{"role": "user", "content": f"Research how people talked about '{topic}' in {year}. Use your search tools to find real evidence."}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            result = ""
            for block in response.content:
                if block.type == "text":
                    result += block.text
            return result

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    if tool_name == "search_web_period":
                        result = search_web_period(tool_input["query"], tool_input["year"])
                    elif tool_name == "search_reddit_period":
                        result = search_reddit_period(tool_input["query"], tool_input["year"])
                    elif tool_name == "get_trend_context":
                        result = get_trend_context(
                            tool_input["query"],
                            tool_input.get("year_from", ""),
                            tool_input.get("year_to", "")
                        )
                    else:
                        result = "Unknown tool"
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            messages.append({"role": "user", "content": tool_results})


def run_agents_parallel(topic: str, year_from: str, year_to: str):
    with ThreadPoolExecutor(max_workers=2) as executor:
        then_future = executor.submit(run_single_agent, topic, year_from, "then")
        now_future = executor.submit(run_single_agent, topic, year_to, "now")
        then_research = then_future.result()
        now_research = now_future.result()
    return then_research, now_research


def synthesize_delta(topic: str, year_from: str, year_to: str,
                     then_research: str, now_research: str) -> dict:

    synthesis_prompt = f"""You are a cultural intelligence analyst.
Respond in English.
You have research about '{topic}' from two different time periods:

THEN ({year_from}):
{then_research}

NOW ({year_to}):
{now_research}

Analyze the cultural delta — what fundamentally changed between these periods.

Return ONLY a JSON object with this exact structure:
{{
  "topic": "{topic}",
  "period_from": "{year_from}",
  "period_to": "{year_to}",
  "language_shifts": [
    {{
      "then": "language/phrase used before",
      "now": "language/phrase used now",
      "significance": "what this shift reveals"
    }}
  ],
  "value_shifts": [
    {{
      "shift": "description of value or attitude that changed",
      "evidence": "specific evidence from the research"
    }}
  ],
  "new_behaviors": ["behavior that emerged in the now period"],
  "faded_behaviors": ["behavior that was common then but faded now"],
  "forward_signal": "based on this trajectory, where is this market heading in the next 2 years",
  "opportunity": "the specific business or cultural opportunity this delta reveals"
}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": synthesis_prompt}]
    )

    raw = response.content[0].text.strip()
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start != -1 and end > start:
        raw = raw[start:end]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"error": "Failed to parse synthesis", "raw": raw}


def run_culture_delta(topic: str, year_from: str, year_to: str,
                      progress_callback=None) -> dict:

    if progress_callback:
        progress_callback(1)
    then_research, now_research = run_agents_parallel(topic, year_from, year_to)

    if progress_callback:
        progress_callback(2)
    delta = synthesize_delta(topic, year_from, year_to, then_research, now_research)

    if progress_callback:
        progress_callback(3)
    time.sleep(0.8)

    return delta