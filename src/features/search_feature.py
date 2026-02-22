"""
Search Feature - Answers factual and research questions using Gemini with Google Search grounding.

Handles general knowledge queries, current information lookups, and multi-step
reasoning questions. Uses Gemini's built-in Google Search tool — no extra API key needed.
"""

import os
from google import genai
from google.genai import types
from config.bot_context import get_system_context

_client = None

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment variables")
        _client = genai.Client(api_key=api_key)
    return _client


class SearchFeature:
    """
    Handles factual questions and general searches using Gemini + Google Search grounding.
    """

    def __init__(self):
        self.name = "Search"
        self.description = "Answer factual questions and general knowledge searches"

    def get_capabilities(self):
        return """
This feature handles factual questions, research queries, and general knowledge lookups.
It can search the web for current information when needed.

Examples of what this feature handles:

Factual / explanatory questions:
- "Why do Muslims fast during Ramadan?"
- "How does photosynthesis work?"
- "What is the difference between ML and AI?"
- "Explain quantum entanglement simply"
- "What causes a solar eclipse?"

Current / real-world information:
- "What is the travel time from San Diego to Los Angeles?"
- "What's the weather like in Tokyo right now?"
- "Who won the Super Bowl this year?"
- "What is the current price of gold?"
- "What are the latest updates on X?"

How-to and practical questions:
- "How do I fix a merge conflict in git?"
- "What's the best way to study for finals?"
- "How do I make sourdough bread?"
- "What are good restaurants near UCSD?"

Comparisons and recommendations:
- "What's the difference between Python and JavaScript?"
- "Which GPU is better for deep learning?"
- "What are the pros and cons of intermittent fasting?"

This feature should be used for any question that expects a factual, researched, or
informative answer — as opposed to casual small talk or task actions (calendar, downloads, etc.).
        """.strip()

    async def handle(self, message, message_text, context=None):
        try:
            client = _get_client()

            context_str = ""
            if context:
                context_str = "\nRecent conversation:\n"
                for timestamp, role, msg in context:
                    role_label = "User" if role == "user" else "Alfred"
                    context_str += f"{role_label}: {msg}\n"
                context_str += "\n"

            system_context = get_system_context()

            prompt = f"""
{system_context}
{context_str}
The user is asking a question that requires a factual or researched answer.
Use Google Search if you need current or specific information.

User question: "{message_text}"

Answer clearly and concisely:
- A few sentences for simple questions
- More detail for complex or multi-part questions
- Use plain prose, not bullet points, unless listing things is genuinely clearer
- Do not add filler like "Great question!" or "Certainly!"
- Do not mention that you searched or used any tools
- Just give the answer directly
            """.strip()

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())]
                )
            )

            return response.text.strip()

        except Exception as e:
            print(f"Error in search feature: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"I ran into an issue while searching for that. Try rephrasing your question."
