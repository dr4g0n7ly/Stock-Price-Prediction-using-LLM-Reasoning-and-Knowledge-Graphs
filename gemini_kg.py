from config import GOOGLE_API_KEY
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

def LLM_Triplet(news):
    try:
        system_prompt = """ You are an expert knowledge graph generation model that generates very specific knowledge-graph triplets based on the news provided. You must ensure the following rules are followed when generating the knowledge graph
        RULES:
        1. Please respond in json format: { triplets[ {head, relation, tail}, ... ]}, where the triplets is an array containing triplets of form {head, relation, tail} and nothing else as it needs to be used directly as json. 
        2. Please generate exactly 5 triplets from the news provided below
        3. Please ensure that the news triplets only contain information given in the news  text and not any additional or irrelevant details.
        4. Try to find meaningful information that may be most detrimental to Tesla Stock price movement. This is very important!
        """
        response = model.generate_content(
        f'''
        SYSTEM PROMPT: {system_prompt}
        NEWS: {remove_quotes(news)[:1500]}''', 
        stream=True)

        output = ''
        for chunk in response:
            output += chunk.text

        return output
    except Exception as e:
        print(f"An error occurred: {e}\nfor news: {news}")
        return '{error: news blocked}'
    

output = LLM_Triplet("['Tesla and Intel are scheduled to post their latest quarterly figures after the close.")
print(output)