def extract_context_sentences(text, keywords, context_size=2):
    # Split the text into sentences
    sentences = text.split('. ')

    # Initialize a list to store sentences with context around keywords
    relevant_sentences = []

    # Iterate over each sentence
    for i, sentence in enumerate(sentences):
        # Check if the sentence contains any of the keywords
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            # Determine the range of sentences to include around the keyword
            start_index = max(0, i - context_size)
            end_index = min(len(sentences), i + context_size + 1)

            # Extract relevant sentences with context
            relevant_sentences.extend(sentences[start_index:end_index])

    # Join the relevant sentences into a single text block
    relevant_text = '. '.join(relevant_sentences)

    return relevant_text



# Example big text
big_text = """
Loading... Loading...

This whale alert can help traders discover the next big trading opportunities.

Whales are entities with large sums of money and we track their transactions here at Benzinga on our options activity scanner.

Traders often look for circumstances when the market estimation of an option diverges away from its normal worth. Abnormal amounts of trading activity could push option prices to hyperbolic or underperforming levels.

Here's the list of options activity happening in today's session:

Symbol PUT/CALL Trade Type Sentiment Exp. Date Strike Price Total Trade Price Open Interest Volume TSLA PUT SWEEP BEARISH 06/09/23 $230.00 $47.0K 6.4K 52.9K CVNA CALL TRADE BULLISH 06/09/23 $21.00 $46.3K 902 7.8K VFC CALL SWEEP BEARISH 01/19/24 $20.00 $310.9K 3.3K 1.1K GM PUT SWEEP BULLISH 06/16/23 $35.00 $50.8K 19.1K 1.1K ABNB CALL TRADE BULLISH 06/16/23 $115.00 $69.0K 7.5K 493 WYNN CALL SWEEP BULLISH 06/16/23 $102.00 $50.7K 617 317 DHI PUT SWEEP BEARISH 07/21/23 $115.00 $61.9K 166 179 W PUT SWEEP BEARISH 07/21/23 $65.00 $193.5K 0 145 EXPE PUT SWEEP BEARISH 06/21/24 $100.00 $45.9K 5 69 PVH PUT TRADE BULLISH 12/15/23 $75.00 $25.1K 43 45

Explanation

These bullet-by-bullet explanations have been constructed using the accompanying table.

• For TSLA TSLA, we notice a put option sweep that happens to be bearish, expiring in 1 day(s) on June 9, 2023. This event was a transfer of 212 contract(s) at a $230.00 strike. This particular put needed to be split into 8 different trades to become filled. The total cost received by the writing party (or parties) was $47.0K, with a price of $222.0 per contract. There were 6496 open contracts at this strike prior to today, and today 52999 contract(s) were bought and sold.

• Regarding CVNA CVNA, we observe a call option trade with bullish sentiment. It expires in 1 day(s) on June 9, 2023. Parties traded 200 contract(s) at a $21.00 strike. The total cost received by the writing party (or parties) was $46.3K, with a price of $232.0 per contract. There were 902 open contracts at this strike prior to today, and today 7847 contract(s) were bought and sold.

• For VFC VFC, we notice a call option sweep that happens to be bearish, expiring in 225 day(s) on January 19, 2024. This event was a transfer of 1149 contract(s) at a $20.00 strike. This particular call needed to be split into 9 different trades to become filled. The total cost received by the writing party (or parties) was $310.9K, with a price of $270.0 per contract. There were 3374 open contracts at this strike prior to today, and today 1185 contract(s) were bought and sold.

• Regarding GM GM, we observe a put option sweep with bullish sentiment. It expires in 8 day(s) on June 16, 2023. Parties traded 1541 contract(s) at a $35.00 strike. This particular put needed to be split into 24 different trades to become filled. The total cost received by the writing party (or parties) was $50.8K, with a price of $33.0 per contract. There were 19101 open contracts at this strike prior to today, and today 1157 contract(s) were bought and sold.

• Regarding ABNB ABNB, we observe a call option trade with bullish sentiment. It expires in 8 day(s) on June 16, 2023. Parties traded 200 contract(s) at a $115.00 strike. The total cost received by the writing party (or parties) was $69.0K, with a price of $345.0 per contract. There were 7509 open contracts at this strike prior to today, and today 493 contract(s) were bought and sold.

• Regarding WYNN WYNN, we observe a call option sweep with bullish sentiment. It expires in 8 day(s) on June 16, 2023. Parties traded 199 contract(s) at a $102.00 strike. This particular call needed to be split into 191 different trades to become filled. The total cost received by the writing party (or parties) was $50.7K, with a price of $255.0 per contract. There were 617 open contracts at this strike prior to today, and today 317 contract(s) were bought and sold.

• For DHI DHI, we notice a put option sweep that happens to be bearish, expiring in 43 day(s) on July 21, 2023. This event was a transfer of 144 contract(s) at a $115.00 strike. This particular put needed to be split into 28 different trades to become filled. The total cost received by the writing party (or parties) was $61.9K, with a price of $430.0 per contract. There were 166 open contracts at this strike prior to today, and today 179 contract(s) were bought and sold.

Loading... Loading...

• For W W, we notice a put option sweep that happens to be bearish, expiring in 43 day(s) on July 21, 2023. This event was a transfer of 145 contract(s) at a $65.00 strike. This particular put needed to be split into 9 different trades to become filled. The total cost received by the writing party (or parties) was $193.5K, with a price of $1335.0 per contract. There were 0 open contracts at this strike prior to today, and today 145 contract(s) were bought and sold.

• For EXPE EXPE, we notice a put option sweep that happens to be bearish, expiring in 379 day(s) on June 21, 2024. This event was a transfer of 41 contract(s) at a $100.00 strike. This particular put needed to be split into 3 different trades to become filled. The total cost received by the writing party (or parties) was $45.9K, with a price of $1120.0 per contract. There were 5 open contracts at this strike prior to today, and today 69 contract(s) were bought and sold.

• Regarding PVH PVH, we observe a put option trade with bullish sentiment. It expires in 190 day(s) on December 15, 2023. Parties traded 45 contract(s) at a $75.00 strike. The total cost received by the writing party (or parties) was $25.1K, with a price of $560.0 per contract. There were 43 open contracts at this strike prior to today, and today 45 contract(s) were bought and sold.

Options Alert Terminology

- Call Contracts: The right to buy shares as indicated in the contract.

- Put Contracts: The right to sell shares as indicated in the contract.

- Expiration Date: When the contract expires. One must act on the contract by this date if one wants to use it.

- Premium/Option Price: The price of the contract.

For more information, visit our Guide to Understanding Options Alerts or read more about unusual options activity.

This article was generated by Benzinga's automated content engine and reviewed by an editor.
"""

# Keywords to look for
keywords = ['Tesla', 'Elon Musk', 'Twitter', 'TSLA', 'electric cars']


# Extract relevant sentences with context
relevant_text = extract_context_sentences(big_text, keywords)
print(relevant_text)