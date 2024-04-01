from config import GOOGLE_API_KEY
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

def LLM_Triplet(news):
    try:
        system_prompt = 'With respect to the entire news provided below, please generate 2 knowledge graph triplets containing {head, relation, tail} that contain the most relevant information that will cause Tesla stock price movement. Please be specific to the news provided. Please respond in json format: { triplets[{head, relation, tail}, {head, relation, tail}]} and nothing else as it needs to be used directly as json.'

        response = model.generate_content(
        f'''
        SYSTEM PROMPT: {system_prompt}
        NEWS: {remove_quotes(news)}''', 
        stream=True)

        output = ''
        for chunk in response:
            output += chunk.text

        return output
    except Exception as e:
        print(f"An error occurred: {e}\nfor news: {news}")
        return '{error: news blocked}'
    

output = LLM_Triplet("['Google has energy data on over 350 million buildings, according to documents CNBC viewed, and sees opportunity to sell the data to companies like Tesla Energy, Aurora Solar and Zillow. The tech giant hopes revenue can hit $100 million in the first year.\n\nDoomed hope on meme stock?', 'Elon Musk, Chief Executive Officer of SpaceX and Tesla and owner of Twitter, looks on as he attends the Viva Technology conference dedicated to innovation and startups at the Porte de Versailles exhibition centre in Paris, France, June 16, 2023.', ""Senate Majority Leader Chuck Schumer will host tech leaders including Tesla (NASDAQ: ) CEO Elon Musk, Meta Platforms (NASDAQ: ) CEO Mark Zuckerberg and Alphabet (NASDAQ: ) CEO Sundar Pichai at an artificial intelligence forum on Sept. 13, Schumer's office said on Monday."", 'Tesla (TSLA) Gains But Lags Market: What You Should Know']")
print(output)