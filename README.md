# Stock Price Prediction using LLM Reasoning and Knowledge Graphs

Predicting stock prices accurately is a paramount objective for investors, financial analysts, and traders alike, as it enables informed decision-making, risk mitigation, and potential profit maximization. Traditional methods often rely solely on historical data and technical indicators,
overlooking the valuable insights embedded in real-time news and social media sentiments. In response, this project introduces an innovative approach leveraging knowledge graphs and Language Model (LLM) reasoning to enhance stock price prediction accuracy. The proposed
system employs automated bots equipped with news APIs and social media APIs to gather real-time textual data. These data sources are then subjected to sentiment analysis and LLM Reasoning to gauge market sentiment accurately. Furthermore, the integration of knowledge
graphs provides contextual understanding, allowing the LLM to determine the relevance and impact of various events on stock prices. 8 selected tech stocks were used to evaluate the three
strategies discussed. LLM KG Reasoning demonstrates the highest performance for 5 out of the 8 stocks however, this strategy also yields negative results for 2 stocks. 

![image](https://github.com/dr4g0n7ly/Stock-Price-Prediction-using-LLM-Reasoning-and-Knowledge-Graphs/assets/82759046/fc2c4ca7-b494-4b68-8be1-f611c5488145)


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


## Results & Discussion

#### Consistency
Before we begin comparing results between Sentiment Strategy, LLM Reasoning Strategy and LLM Reasoning with KG strategy, it is essential to determine whether the models we are using perform consistently. To perform this check, news sentiments using ‘ProsusAI/finbert’ as well as confidence scores using ‘google/geminipro’ (temperature = 0.6) were generated on retrieved Tesla stock news three times each. These sentiments and confidence scores are used to predict Tesla stock prices and the outputs are compared against each other.
The sentiment analysis model using FinBERT performs very consistently, resulting in the same output every time the model is run on the same news. However, slight inconsistencies were noticed during price prediction using LLM Reasoning.
LLM Reasoning is purely a text-generation task hence being highly probabilistic in nature while Sentiment Analysis is a classification task and hence has a very consistent output. The change in cumulative return has a variation of 3.08%. Nonetheless, since only three LLM Reasoning outputs have been generated to test consistency of the model, the variation in cumulative return can be approximated to about 10%. This can be considered as a consistent model due to LLM’s
black box nature and their subjectivity to hallucination. Therefore, both models performed consistently without drastic change. Now, we can compare the performance of the 3 strategies.

![image](https://github.com/dr4g0n7ly/Stock-Price-Prediction-using-LLM-Reasoning-and-Knowledge-Graphs/assets/82759046/01db28cb-396d-49f5-a7bc-84867fccc9fe)

![image](https://github.com/dr4g0n7ly/Stock-Price-Prediction-using-LLM-Reasoning-and-Knowledge-Graphs/assets/82759046/f3c9f3dd-ee4d-4a06-9b67-59e9bbb96538)


#### Performance
Due to the vast amount of finance news available on the top tech stocks, we have considered the following eight stocks for our evaluation: AMZN (Amazon), AMD (Advanced Micro Devices), AAPL (Apple), GOOG (Alphabet Class C), JPM (JPMorgan Chase & Co), MSFT (MicroSoft), NVDA (Nvidia), TSLA (Tesla). The process of evaluation involved collecting the stock-wise news from MarketAux. The collected news is then used to perform sentiment analysis as well as extract LLM reasoning confidence scores. To extract LLM reasoning with KG confidence scores, the news is used to generate triplets and their respective embeddings. Semantic search is performed on the embeddings using the news per day as the query. Top K triplets are retrieved based on whether the triplet was generated within the past week of the news being analyzed and is injected as Last Week Context. Top K triplets in general are also extracted and injected as General Context. These contexts provide the LLM with necessary information to base its reasoning as to whether one should buy or sell a particular stock, along with its reasoning. The confidence scores generated are the LLM-KG reasoning confidence scores. These confidence scores are used to perform back-testing on the selected stocks and their cumulative return was tested.

![image](https://github.com/dr4g0n7ly/Stock-Price-Prediction-using-LLM-Reasoning-and-Knowledge-Graphs/assets/82759046/0acdc295-bb73-4475-b148-7183c6320af7)

#### Limitations
The project heavily depends on the news provided and this is a major bottleneck to this research as the performance depends solely on the news. The news must be verified for its accuracy as well as its popularity must be taken into consideration which this project does not consider as of now. LLM Reasoning as well as triplet generation depend on the quality of the news provided and the news sources taken into consideration, which in-turn affect the decision making process of whether to buy or sell a certain stock. The outputs of the project are also limited to google’s Gemini Pro LLM. Any update, fine-tuning of the LLM or using a different LLM may vastly change the results. LLMs in general are subject to a black-box nature and hence hallucination. Adding financial market news as context helps resolve hallucination to some degree but as mentioned above consistency with LLMs is a challenging drawback. Moreover, Stock market prediction in general is inherently unpredictable due to the complex interplay of countless variables, including economic indicators, geopolitical events, and investor psychology. The market's inherent volatility amplifies this unpredictability, making it challenging to accurately forecast future trends. The project only accounts for news sources as of now, and does not take into consideration other variables. An integration with hard data, company fundamentals and different sources of news with the LLM KG Strategy may result in further improvements.
