# BlackScholes
This program creates a black scholes model with an HTML front-end to allow for usability. Incorporated dark mode as well. 

Within this ReadMe, we will discuss the inputs required, the utilization of HTML, and the purpose behind this project. 

## Purpose
Overall, the reason for this project was primarily due to the fact that I am interested in the intersection between finance and computer science. As such, this felt like a great first step into the said-intersection between the two. It provides great basics on a simple back-end (taking inputs and outputting a result given a specified formula), and creating an HTML front-end (that can take in inputs and acknowledges when we do not have enough inputs provided). Simply put, this program could be analogized to a Pythagorean Theorem just with an added front-end, but slightly more complex on the back-end. This project took approximately two hours, and most of the time was spent figuring out HTML code and how to create a Dark Mode. It was a fun and challenging experience. 

## Inputs
There are five main inputs: spot price, strike price, time to maturity, volatility, and interest rate. These are all integral in the basic Black Scholes model, and each impacts the formula in a different manner. 

### Spot Price
The spot price can be considered the current market price of the underlying stock/index. For example, if the price of TSLA is $100/share, then the spot price will be $100. 

### Strike Price
The strike price is the determined price in which the option holder can buy or sell the underlying stock. For example, a call or put option at $95 for TSLA. 

### Time to Maturity
Time to maturity will be the remaining time until the option expires. The longer the time to maturity, the higher the option premium. This makes sense, and a higher time to maturity indicates more time for the underlying stock to [potentially] go up or down to the respective call or put strike price. Suppose that the time to maturity for our TSLA example will be 0.5 years, or half a year. 

### Volatility
Volatility is measuring the asset's price risk, or variability. Since TSLA is a relatively volatile stock (to, say SPY or GOOGL), it will have higher option prices, as there is a higher probability for the option being ITM (in-the-money) by the date of expiration. For our example, we will have volatility set to around 0.3. 

### Interest Rate
Interest rate is the risk-free interest rate, or the short-term interest rate. This is important as it serves as another measure for time to maturity, in a sense. Higher interest rates typically indicate higher call and lower put prices. In our example, we will have interest rate set to around 0.1.

### Sample Output
Suppose I put in the following details into the Black Scholes model I have created. Spot price is $100, strike price is $95, time to maturity is 0.5 years, volatility is 0.3 and interest rate is 0.1. 

As a result, our code prints out a call and put price. The call price would be 13.75, and the put price would be 4.12. 
