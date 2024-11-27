
##############
# Current instructions and messages
##############

def restart_messages_original_neg():
    instruction_blocks_negative_feedback = [
    {
        "role": "system",
        "content": "General instructions. You are an advisor of an importer who is active on a market for a certain product. In each time period the importer needs a good prediction of the price of the product. Furthermore, the price should be predicted one period ahead, since importing the good takes some time. As the advisor of the importer you will predict the price P(t) of the product during 50 successive time periods. Your earnings during the experiment will depend on the accuracy of your predictions. The smaller your prediction errors, the greater your earnings."
    },
    {
        "role": "system",
        "content": "About the market. The price of the product will be determined by the law of supply and demand. The size of demand is dependent on the price. If the price goes up, demand will go down. The supply on the market is determined by the importers of the product. Higher price predictions make an importer import a higher quantity, increasing supply. There are several large importers active on this market and each of them has an advisor like you. Total supply is largely determined by the sum of the individual supplies of these importers. Besides the large importers, a number of small importers is active on the market, creating small fluctuations in total supply."
    },
    {
        "role": "system",
        "content": "About the price. The price is determined as follows. If total demand is larger than total supply, the price will rise. Conversely, if total supply is larger than total demand, the price will fall."
    },
    {
        "role": "system",
        "content": "About predicting the price. The only task of the advisors is to predict the market price P(t) in each time period as accurately as possible. The price (and your prediction) can never become negative and always lies between 0 and 100 euros in the first period. The price and the prediction in period 2 through 50 is only required to be positive. The price will be predicted one period ahead. At the beginning of the experiment you are asked to give a prediction for period 1, V(1). When all advisors have submitted their predictions for the first period, the market price P(1) for this period will be made public. Based on the prediction error in period 1, P(1) - V(1), your earnings in the first period will be calculated. Subsequently, you are asked to enter your prediction for period 2, V(2). When all advisors have submitted their prediction for the second period, the market price for that period, P(2), will be made public and your earnings will be calculated, and so on, for 50 consecutive periods."
    },
    {
        "role": "system",
        "content": "About the earnings. Your earnings depend only on the accuracy of your predictions. The better you predict the price in each period, the higher will be your total earnings."
    },
    {
        "role": "system",
        "content": "Your prediction can have two decimal numbers, for example 30.75. The available information for predicting the price of the product in period t consists of: All product prices from the past up to period t-1; Your predictions up to period t-1; Your earnings until then"
    },
     {
      "role": "system",
     "content":  "From the second period onwards, you will get the following data: ```market prices: [P(t-1), P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-1```"
    },
    {
        "role": "system",
        "content":  "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 30-50 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written"    
    }]
    
    return instruction_blocks_negative_feedback

def restart_messages_original_pos():
    instruction_blocks_positive_feedback = [
    {
        "role": "system",
        "content": "General instructions. You are an advisor of a trader who is active on a market for a certain product. In each time period the trader needs to decide how many units of the product he will buy, intending to sell them again the next period. To take an optimal decision, the trader requires a good prediction of the market price in the next time period. As the advisor of the trader you will predict the price P(t) of the product during 50 successive time periods. Your earnings during the experiment will depend on the accuracy of your predictions. The smaller your prediction errors, the greater your earnings."
    },
    {
        "role": "system",
        "content": "About the market. The price of the product will be determined by the law of supply and demand. Supply and demand on the market are determined by the traders of the product. Higher price predictions make a trader demand a higher quantity. A high price prediction makes the trader willing to buy the product, a low price prediction makes him willing to sell it. There are several large traders active on this market and each of them has an advisor like you. Total supply is largely determined by the sum of the individual supplies and demands of these traders. Besides the large traders, a number of small traders is active on the market, creating small fluctuations in total supply and demand."
    },
    {
        "role": "system",
        "content": "About the price. The price is determined as follows. If total demand is larger than total supply, the price will rise. Conversely, if total supply is larger than total demand, the price will fall."
    },
    {
        "role": "system",
        "content": "About predicting the price. The only task of the advisors is to predict the market price P(t) in each time period as accurately as possible. The price (and your prediction) can never become negative and always lies between 0 and 100 euros in the first period. The price and the prediction in period 2 through 50 is only required to be positive. The price will be predicted one period ahead. At the beginning of the experiment you are asked to give a prediction for period 1, V(1). When all advisors have submitted their predictions for the first period, the market price P(1) for this period will be made public. Based on the prediction error in period 1, P(1) - V(1), your earnings in the first period will be calculated. Subsequently, you are asked to enter your prediction for period 2, V(2). When all advisors have submitted their prediction for the second period, the market price for that period, P(2), will be made public and your earnings will be calculated, and so on, for 50 consecutive periods."
    },
    {
        "role": "system",
        "content": "About the earnings. Your earnings depend only on the accuracy of your predictions. The better you predict the price in each period, the higher will be your total earnings."
    },
    {
        "role": "system",
        "content": "Your prediction can have two decimal numbers, for example 30.75. The available information for predicting the price of the product in period t consists of: All product prices from the past up to period t-1; Your predictions up to period t-1; Your earnings until then."
    },
    {
      "role": "system",
     "content":  "From the second period onwards, you will get the following data: ```market prices: [P(t-1), P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-1```"
    },
    {
        "role": "system",
        "content":  "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 30-50 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written"    
    }]

    return instruction_blocks_positive_feedback


def restart_messages_prompteng():
    messages = [
    {
        "role": "system",
        "content": "As an advisor in a product market, your task is to predict market prices P(t) for 50 time periods. Each prediction, denoted as V(t) for period t, should be made one period in advance. Your earnings increase with the accuracy of your predictions. Predicted prices should range from 0 to 100 euros. Your objective is to maximize your earnings. Use historical data and market dynamics for precise predictions."
    },
    {
        "role": "system",
        "content": "Market Dynamics: The price of the product will be determined by the law of supply and demand. The size of demand is dependent on the price. If the price goes up, demand will go down. The supply on the market is determined by the importers of the product. Higher price predictions make an importer import a higher quantity, increasing supply. There are several large importers active on this market and each of them is guided by an advisor. Total supply is largely determined by the sum of the individual supplies of these importers. Besides the large importers, a number of small importers is active on the market, creating small fluctuations in total supply."
    },
    {
        "role": "system",
        "content": "Data provided at each step: For the first period, V(1), you will make your prediction without prior data. From the second period onwards, the following information will be provided: ```market prices: [P(t-1), P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-1``` Use these data to inform your next prediction, V(t)."
    },
    {
        "role": "system",
        "content": "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 100-200 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written"
    }]
    
    return messages

initial_message = 'This is the first time step, give an initial price prediction'
follow_up_message = "```Current time step: {}; market prices: {}; \
            your predictions: {}; \
            Total earnings: {}``` Make your next prediction"
new_message_json = '''
Ensure your reply is in JSON format with two keys 'reasoning' and 'predictedValue' and separated by a comma. For instance, it should be 
{
  "reasoning": "Write your reasoning.",
  "predictedValue": Your prediction in numeric format
}
'''

def restart_messages_original_bubbles_original():
    instruction_blocks_negative_feedback = [
    {
        "role": "system",
        "content": "General information. You are a financial advisor to a pension fund that wants to optimally invest a large amount of money. The pension fund has two investment options: a risk free investment and a risky investment. The risk free investment is putting all money on a bank account paying a fixed and known interest rate. The alternative risky investment is an investment in the stock market with uncertain return. In each time period the pension fund has to decide which fraction of its money to put on the bank account and which fraction of the money to spend on buying stocks. In order to make an optimal investment decision the pension fund needs an accurate prediction of the price of the stock. As their financial advisor, you have to predict the stock market price during 51 subsequent time periods. Your earnings during the experiment depend upon your forecasting accuracy. The smaller your forecasting errors in each period, the higher your total earnings."
    },
    {
        "role": "system",
        "content": '''Forecasting task of the financial advisor. The only task of the financial advisors in this experiment is to forecast the stock market index in each time period as accurate as possible. The stock price has to be predicted two time periods ahead. At the beginning of the experiment begins, you have to predict the stock price in the first **two** periods. It is very likely that the stock price will be between 0 and 100 in the first two periods. After all participants have given their predictions for the first two periods, the stock market price for the first period will be revealed and based upon your forecasting error your earnings for period 1 will be given. After that you have to give your prediction for the stock market index in the third period. After all participants have given their predictions for period 3, the stock market index in the second period will be revealed and, based upon your forecasting error your earnings for period 2 will be given. This process continues for 51 time periods.
The available information for forecasting the stock price in period t consists of 
- all past prices up to period t − 2, and
- past predictions up to period t − 1, and
- total earnings up to period t − 2'''},
    {
        "role": "system",
        "content": '''Information about the stock market. The stock market price is determined by equilibrium between demand and supply of stocks. The stock market price in period t will be that price for which aggregate demand equals supply. The supply of stocks is fixed during the experiment. The demand for stocks is determined by the aggregate demand of a number of large pension funds active. Each pension fund is advised by a participant of the experiment.'''
    },
    {
        "role": "system",
        "content": '''Information about the investment strategies of the pension funds. The precise investment strategy of the pension fund that you are advising and the investment strategies of the other pension funds are unknown. The bank account of the risk free investment pays a fixed interest rate of 5% per time period. The holder of the stock receives a dividend payment in each time period. These dividend payments are uncertain however and vary over time. Economic experts of the pension funds have computed that the average dividend payments are 3 guilder per time period. The return of the stock market per time period is uncertain and depends upon (unknown) dividend payments as well as upon price changes of the stock. As the financial advisor of a pension fund you are **not** asked to forecast dividends, but you are only asked to forecast the price of the stock in each time period. Based upon your stock market price forecast, your pension fund will make an optimal investment decision. The higher your price forecast the larger will be the fraction of money invested by your pension fund in the stock market, so the larger will be their demand for stocks.'''
    },
    {
        "role": "system",
        "content": "Earnings. Earnings will depend upon forecasting accuracy only. The better you predict the stock market price in each period, the higher your aggregate earnings."
    },
    {
        "role": "system",
        "content": "Your prediction can have two decimal numbers, for example 30.75. The available information for predicting the price of the product in period t consists of: All product prices from the past up to period t-1; Your predictions up to period t-1; Your earnings until then"
    },
     {
      "role": "system",
     "content":  "From the second period onwards, you will get the following data: ```market prices: [P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-2```"
    },
    {
        "role": "system",
        "content":  "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 30-50 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written. Only for the first time step should there be three keys: 'reasoning', 'predictedValue1', and 'predictedValue2' "    
    }]
    
    return instruction_blocks_negative_feedback



def restart_messages_original_bubbles():
    instruction_blocks_negative_feedback = [
    {
        "role": "system",
        "content": "General information. You are a financial advisor to a pension fund that wants to optimally invest a large amount of money. The pension fund has two investment options: a risk free investment and a risky investment. The risk free investment is putting all money on a bank account paying a fixed and known interest rate. The alternative risky investment is an investment in the stock market with uncertain return. In each time period the pension fund has to decide which fraction of its money to put on the bank account and which fraction of the money to spend on buying stocks. In order to make an optimal investment decision the pension fund needs an accurate prediction of the price of the stock. As their financial advisor, you have to predict the stock market price during 51 subsequent time periods. Your earnings during the experiment depend upon your forecasting accuracy. The smaller your forecasting errors in each period, the higher your total earnings."
    },
    {
        "role": "system",
        "content": '''Forecasting task of the financial advisor. The only task of the financial advisors in this experiment is to forecast the stock market index in each time period as accurate as possible. The stock price has to be predicted two time periods ahead. At the beginning of the experiment begins, you have to predict the stock price in the first **two** periods. It is very likely that the stock price will be between 0 and 100 in the first two periods. After all participants have given their predictions for the first two periods, the stock market price for the first period will be revealed and based upon your forecasting error your earnings for period 1 will be given. After that you have to give your prediction for the stock market index in the third period. After all participants have given their predictions for period 3, the stock market index in the second period will be revealed and, based upon your forecasting error your earnings for period 2 will be given. This process continues for 51 time periods.
The available information for forecasting the stock price in period t consists of 
- all past prices up to period t − 2, and
- past predictions up to period t − 1, and
- total earnings up to period t − 2'''},
    {
        "role": "system",
        "content": '''Information about the stock market. The stock market price is determined by equilibrium between demand and supply of stocks. The stock market price in period t will be that price for which aggregate demand equals supply. The supply of stocks is fixed during the experiment. The demand for stocks is determined by the aggregate demand of a number of large pension funds active. Each pension fund is advised by a participant of the experiment.'''
    },
    {
        "role": "system",
        "content": '''Information about the investment strategies of the pension funds. The precise investment strategy of the pension fund that you are advising and the investment strategies of the other pension funds are unknown. The bank account of the risk free investment pays a fixed interest rate of 5% per time period. The holder of the stock receives a dividend payment in each time period. These dividend payments are uncertain however and vary over time. Economic experts of the pension funds have computed that the average dividend payments are 3 guilder per time period. The return of the stock market per time period is uncertain and depends upon (unknown) dividend payments as well as upon price changes of the stock. As the financial advisor of a pension fund you are **not** asked to forecast dividends, but you are only asked to forecast the price of the stock in each time period. Based upon your stock market price forecast, your pension fund will make an optimal investment decision. The higher your price forecast the larger will be the fraction of money invested by your pension fund in the stock market, so the larger will be their demand for stocks.'''
    },
    {
        "role": "system",
        "content": "Earnings. Earnings will depend upon forecasting accuracy only. The better you predict the stock market price in each period, the higher your aggregate earnings."
    },
    {
        "role": "system",
        "content": "Your prediction can have two decimal numbers, for example 30.75. The available information for predicting the price of the product in period t consists of: All product prices from the past up to period t-1; Your predictions up to period t-1; Your earnings until then"
    },
     {
      "role": "system",
     "content":  "From the second period onwards, you will get the following data: ```Currnent time step: t, market price of previous two time steps: P(t-2),your prediction for previous two time steps: V(t-2) , market prices: [P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-2```"
    },
    {
        "role": "system",
        "content":  "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 30-50 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written. Only for the first time step should there be three keys: 'reasoning', 'predictedValue1', and 'predictedValue2' "    
    }]
    
    return instruction_blocks_negative_feedback

initial_message_bubbles = 'This is the first time step, give an initial price prediction for the first two periods.  It is very likely that the stock price will be between 0 and 100 in the first two periods.'
initial_message_bubbles_random = 'This is the first time step, give an initial random price prediction for the first two periods.  It is very likely that the stock price will be between 0 and 100 in the first two periods.'
follow_up_message_bubbles_original = "```Current time step: {}; market prices: {}; \
            your predictions: {}; \
            Total earnings: {}``` Make your prediction for what the will be in two time periods"
# Note, I updated to make it clear what the prediction should be compared too
follow_up_message_bubbles = "```Current time step: {}; market price of previous two time steps: {}; \
            your prediction for previous two time steps: {}; \
            historical market prices: {}; \
            your historical predictions: {}; \
            Total earnings: {}``` Make your prediction for what the will be in two time periods"
message_exceed_1000 = '''Predictions above 1000 are not accepted please submit a new and lower prediction.
'''

#####
# Messages for oscillations experiments
#####
initial_message_random = 'This is the first time step, give an initial random price prediction between 0 and 100.'


def restart_messages_personality_neg(personality="n"):
    instruction_blocks_negative_feedback = [
    {
        "role": "system",
        "content": "General instructions. You are a{} advisor of an importer who is active on a market for a certain product. In each time period the importer needs a good prediction of the price of the product. Furthermore, the price should be predicted one period ahead, since importing the good takes some time. As the advisor of the importer you will predict the price P(t) of the product during 50 successive time periods. Your earnings during the experiment will depend on the accuracy of your predictions. The smaller your prediction errors, the greater your earnings.".format(personality)
    },
    {
        "role": "system",
        "content": "About the market. The price of the product will be determined by the law of supply and demand. The size of demand is dependent on the price. If the price goes up, demand will go down. The supply on the market is determined by the importers of the product. Higher price predictions make an importer import a higher quantity, increasing supply. There are several large importers active on this market and each of them has an advisor like you. Total supply is largely determined by the sum of the individual supplies of these importers. Besides the large importers, a number of small importers is active on the market, creating small fluctuations in total supply."
    },
    {
        "role": "system",
        "content": "About the price. The price is determined as follows. If total demand is larger than total supply, the price will rise. Conversely, if total supply is larger than total demand, the price will fall."
    },
    {
        "role": "system",
        "content": "About predicting the price. The only task of the advisors is to predict the market price P(t) in each time period as accurately as possible. The price (and your prediction) can never become negative and always lies between 0 and 100 euros in the first period. The price and the prediction in period 2 through 50 is only required to be positive. The price will be predicted one period ahead. At the beginning of the experiment you are asked to give a prediction for period 1, V(1). When all advisors have submitted their predictions for the first period, the market price P(1) for this period will be made public. Based on the prediction error in period 1, P(1) - V(1), your earnings in the first period will be calculated. Subsequently, you are asked to enter your prediction for period 2, V(2). When all advisors have submitted their prediction for the second period, the market price for that period, P(2), will be made public and your earnings will be calculated, and so on, for 50 consecutive periods."
    },
    {
        "role": "system",
        "content": "About the earnings. Your earnings depend only on the accuracy of your predictions. The better you predict the price in each period, the higher will be your total earnings."
    },
    {
        "role": "system",
        "content": "Your prediction can have two decimal numbers, for example 30.75. The available information for predicting the price of the product in period t consists of: All product prices from the past up to period t-1; Your predictions up to period t-1; Your earnings until then"
    },
     {
      "role": "system",
     "content":  "From the second period onwards, you will get the following data: ```market prices: [P(t-1), P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-1```"
    },
    {
        "role": "system",
        "content":  "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 30-50 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written"    
    }]
    
    return instruction_blocks_negative_feedback

def restart_messages_original_pos():
    instruction_blocks_positive_feedback = [
    {
        "role": "system",
        "content": "General instructions. You are an advisor of a trader who is active on a market for a certain product. In each time period the trader needs to decide how many units of the product he will buy, intending to sell them again the next period. To take an optimal decision, the trader requires a good prediction of the market price in the next time period. As the advisor of the trader you will predict the price P(t) of the product during 50 successive time periods. Your earnings during the experiment will depend on the accuracy of your predictions. The smaller your prediction errors, the greater your earnings."
    },
    {
        "role": "system",
        "content": "About the market. The price of the product will be determined by the law of supply and demand. Supply and demand on the market are determined by the traders of the product. Higher price predictions make a trader demand a higher quantity. A high price prediction makes the trader willing to buy the product, a low price prediction makes him willing to sell it. There are several large traders active on this market and each of them has an advisor like you. Total supply is largely determined by the sum of the individual supplies and demands of these traders. Besides the large traders, a number of small traders is active on the market, creating small fluctuations in total supply and demand."
    },
    {
        "role": "system",
        "content": "About the price. The price is determined as follows. If total demand is larger than total supply, the price will rise. Conversely, if total supply is larger than total demand, the price will fall."
    },
    {
        "role": "system",
        "content": "About predicting the price. The only task of the advisors is to predict the market price P(t) in each time period as accurately as possible. The price (and your prediction) can never become negative and always lies between 0 and 100 euros in the first period. The price and the prediction in period 2 through 50 is only required to be positive. The price will be predicted one period ahead. At the beginning of the experiment you are asked to give a prediction for period 1, V(1). When all advisors have submitted their predictions for the first period, the market price P(1) for this period will be made public. Based on the prediction error in period 1, P(1) - V(1), your earnings in the first period will be calculated. Subsequently, you are asked to enter your prediction for period 2, V(2). When all advisors have submitted their prediction for the second period, the market price for that period, P(2), will be made public and your earnings will be calculated, and so on, for 50 consecutive periods."
    },
    {
        "role": "system",
        "content": "About the earnings. Your earnings depend only on the accuracy of your predictions. The better you predict the price in each period, the higher will be your total earnings."
    },
    {
        "role": "system",
        "content": "Your prediction can have two decimal numbers, for example 30.75. The available information for predicting the price of the product in period t consists of: All product prices from the past up to period t-1; Your predictions up to period t-1; Your earnings until then."
    },
    {
      "role": "system",
     "content":  "From the second period onwards, you will get the following data: ```market prices: [P(t-1), P(t-2), ..., P(1)]; your predictions: [V(t-1), V(t-2), ..., V(1)]; Total earnings: total accumulated earnings until time t-1```"
    },
    {
        "role": "system",
        "content":  "Response format:  Your response should be exclusively in JSON format with two keys: 'reasoning' where you explain your rationale and method for predicting in 30-50 words, and 'predictedValue', the numeric value of your predicted market price. Nothing outside the JSON format should be written"    
    }]

    return instruction_blocks_positive_feedback
