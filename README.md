# Stock Price Prediction using LLM Reasoning and Knowledge Graphs

Predicting stock prices accurately is a paramount objective for investors, financial analysts, and traders alike, as it enables informed decision-making, risk mitigation, and potential profit maximization. Traditional methods often rely solely on historical data and technical indicators,
overlooking the valuable insights embedded in real-time news and social media sentiments. In response, this project introduces an innovative approach leveraging knowledge graphs and Language Model (LLM) reasoning to enhance stock price prediction accuracy. The proposed
system employs automated bots equipped with news APIs and social media APIs to gather real-time textual data. These data sources are then subjected to sentiment analysis and LLM Reasoning to gauge market sentiment accurately. Furthermore, the integration of knowledge
graphs provides contextual understanding, allowing the LLM to determine the relevance and impact of various events on stock prices. 8 selected tech stocks were used to evaluate the three
strategies discussed. LLM KG Reasoning demonstrates the highest performance for 5 out of the 8 stocks however, this strategy also yields negative results for 2 stocks. 

![image](https://github.com/dr4g0n7ly/Stock-Price-Prediction-using-LLM-Reasoning-and-Knowledge-Graphs/assets/82759046/6dc3a03c-ad05-464c-a2c2-733794971609)

## Modules

#### Module 1 - Backtesting
Backtesting serves as the conclusive testing phase for our system. Leveraging the Lumibot Python library, we meticulously evaluate our strategies, integrating insights derived from sentiment analysis and/or LLM prompt engineering. Additionally, we implement advanced quant finance techniques, including but not limited to, take profit prices, stop loss prices, cash risks, and dynamic purchase quantities. This component not only facilitates the selection of specific stocks but also enables a comprehensive performance comparison with the strategies we meticulously develop.

#### Module 2 - News Extraction Model
The system employs MarketAux APIs to procure stock-specific news, categorized by dates, which are subsequently stored in the database for testing. As the system approaches its final stages, these APIs will be instrumental in accessing real-time news data, thereby enhancing the system's capability to promptly respond to evolving market conditions. Currently we are only restricting the system to Amazon, AMD, Apple, Google, JP Morgan, Microsoft, Nvidia and Tesla related news articles for testing purposes. 

#### Module 3 - Sentiment Analysis
Sentiment analysis using FinBERT harnesses a specialized adaptation of the BERT (Bidirectional Encoder Representations from Transformers) model, tailored to discern sentiment nuances within financial texts. This methodology empowers the classification of sentiments—be it positive, negative, or neutral—embedded in various financial sources such as news articles, social media posts, or corporate reports. This capability renders invaluable insights for traders, investors, and financial analysts, enabling them to make well-informed decisions rooted in the prevailing sentiment landscape.

#### Module 4 - Knowledge Triplet Extraction
The system utilizes Google's Gemini Pro API to generate KG triplets from unstructured text while reasoning out why the triplets have been deemed to be the most detrimental to the price movement of the specific stock. Parsing techniques are applied to identify and extract relationships between entities, attributes, and values (head, relation and tail) within the text. These triplets provide structured data in the JSON format, facilitating a key task in the creation of this project - knowledge graph construction. Leveraging Google's ongoing advancements in NLP ensures the system remains adept at handling diverse text sources and ever evolving linguistic patterns.

#### Module 5 - LLM reasoning with prompt engineering
The reasoning method involves utilizing a large language model to provide a confidence score regarding the direction of movement for a financial stock. This process entails formulating a prompt or query tailored to elicit confidence scores from the LLM about the future performance of the stock, while at the same time generating reasons for the confidence scores. The LLM then evaluates various factors such as market trends, company news, and historical data to generate a confidence score indicating the likelihood of the stock's price increasing or decreasing. The LLM used in the system is Google's Gemini Pro API and this LLM has been preferred due to the large amount of free GPU compute units available. The confidence score serves as a quantitative measure of the model's certainty in its prediction, enabling backtesting modules to perform decision making on whether a stock should be bought or sold.

#### Module 6 - Embedding Generation and Semantic Search
The system uses Google’s Embedding-001 API to generate vector embeddings from the extracted triplets. Semantic search is performed over these embeddings to find the K most relevant triplets from the past week and K most relevant triplets in general with respect to the given day's news. These extracted triplets are injected as context into the prompt, this is then used to guide the decision-making and reasoning process of the LLM.
