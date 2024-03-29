import pathlib
import textwrap

import google.generativeai as genai

from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

system_prompt = 'With respect to the news provided respond with a reasons for whether you should buy or sell Tesla stock and give a confidence ranging from 0 (sell) to 9 (buy). Only respond in JSON format and nothing else. the following format should be followed {reason: string, confidence: integer}'
ARTICLE = """ "['Amazon AMZN , Apple AAPL , Google GOOG , Meta, Microsoft MSFT and Tesla TSLA joined in the bullish fun but without making it all the way up or past their all-time highs.\n\nThe 7 stocks mentioned have gained by 44% since the beginning of the year while the other 493 stocks in the Standard & Poor’s 500 are up by just 1%.', ""I'm talking about the Tesla-Ford agreement. The deal will mean Tesla tech, specifically its charging port, will be integrated into Ford's second-generation EVs that are slated to come out in 2025."", 'The deal was announced by Ford CEO Jim Farley and Tesla CEO Elon Musk via, you guessed it, a Twitter Spaces — Musk’s latest push toward turning Twitter into an actual town square. No glitches for this one, at least.', 'This will give them access to 12,000 Tesla Superchargers in the U.S. and Canada, which is double the number Ford customers currently have access to. Ford’s BlueOval Charge Network has over 10,000 public DC fast-chargers.', 'Musk has applauded Ford in the past, noting on several occasions that only Tesla and Ford have avoided bankruptcy. As they chatted live with over 200,000 people listening in, Farley and Musk seemed to hint at future potential collaborations.', 'In response to Farley’s noting that making a “fully software updatable vehicle” is “super hard,” Musk responded that Tesla would be happy to “be helpful on the software front” and might “open source more code” to automakers.', ""Story continues\n\nBoth Ford and Tesla shares jumped over 7% in after-hours trading as a result of the news.\n\nSo you might have heard, but in case you didn't, TechCrunch is searching for 200 early-stage companies for Startup Battlefield at Disrupt this September. Comes with a chance to win a $100,000 in equity-free $$ and cool kid creds."", 'Tesla launched FSD Beta in Europe and Australia. It’s a small-scale launch, with one Model S in Belgium and another in Germany getting an update and a Model 3 in Australia receiving the beta software. For those who don’t know, FSD is already available in New Zealand, according to a Tesla salesperson who took me on a test drive the other day.', 'Many automakers, including Tesla, BMW, and Volkswagen, have said they plan to ditch AM radio because it interferes with electrical engines. So policymakers introduced a bill calling NHTSA to require AM radio in vehicles for public safety reasons. Ford CEO Jim Farley had a chat with some of them and apparently was convinced.', 'Tesla CEO Elon Musk hinted in a joint Twitter Spaces announcement with Ford that the automaker might “open up some of its automotive operating system code to other automakers.”\n\nUber is launching Uber Green in India, an effort to introduce more EVs to the platform.', 'German authorities are investigating a potential data leak by Tesla. The automaker reportedly failed to adequately protect data of customers, employees and business partners, according to local business newspaper Handelsblatt. The paper received 100 gigabytes of confidential leaked data.', ""Ford EVs will have Tesla DNA and Waymo's robotaxis are coming to Uber"", 'But the best way to make money from this disruption isn’t buying Tesla (NASDAQ:TSLA)… or other automakers going green.\n\nToday, I’ll share my top “backdoor” stock to profit from the coming EV boom.\n\nGlobal EV Sales\n\nTell me this isn’t one of the prettiest charts in the world…\n\nA record 10.5 million new EVs hit the roads last year.', 'For example, there are 180 lbs. of copper and 140 lbs. of lithium under the hood of a Tesla Model S.\n\nThese materials don’t grow on trees. You can’t make them in sterilized test tubes.\n\nYou have to pull them out of the ground. And that requires giant, rusty excavators… larger-than-life trucks… and lots of dirty, filthy mining.', 'Tesla, Ford (NYSE:F), and others are tearing the hinges off the door to get their hands on these materials.\n\nThe amount of money automakers spent on lithium surged 12X to $35 billion in the past two years alone. And we ain’t seen nothing yet.\n\nHumans mined a combined 700 million tons of copper over the past 5,000 years .', 'There are 180 lbs. of copper in a Tesla Model S. Copper’s used in the wires and cables that carry the electricity from the battery to the motor.\n\nBattery-powered cars need almost 3X as much copper as a regular gas guzzler.\n\nSurging EV sales are expected to double the demand for the “red metal” over the next decade, according to S&P Global.']" """

def remove_quotes(s):
    return s.replace("'", "").replace('"', '')

response = model.generate_content(
  f'''
  SYSTEM PROMPT: {system_prompt}
  NEWS: {remove_quotes(ARTICLE)}''', 
  stream=True)

output = ''
for chunk in response:
  output += chunk.text

print(output)