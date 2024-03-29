import pathlib
import textwrap

import google.generativeai as genai

from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

def LLM_Response(news):
    try:
        system_prompt = 'With respect to the news provided respond with a reasons for whether you should buy or sell Tesla stock and give a confidence ranging from 0 (sell) to 9 (buy). Only respond in JSON format and nothing else. the following format should be followed {reason: string, confidence: integer}'
        ARTICLE = news

        response = model.generate_content(
        f'''
        SYSTEM PROMPT: {system_prompt}
        NEWS: {remove_quotes(ARTICLE)}''', 
        stream=True)

        output = ''
        for chunk in response:
            output += chunk.text

        return output
    except Exception as e:
        print(f"An error occurred: {e}\nfor news: {news}")
        return '{reason: error, confidence: 5}' # Return None if an error occurs