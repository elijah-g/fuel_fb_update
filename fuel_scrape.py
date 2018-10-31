import feedparser
import facebook
import datetime



#Function that takes a message as as a parameter and posts it to facebook page specified by
#the access token.
def facebook_post(post_message):
    #Create facebook GRAPH API object.
    graph = facebook.GraphAPI(access_token="EAAdi2SF1ba0BADHOZA0uz85XKaYRF7WZCn8bGCjqZBPePIm1asNNg3dS4ci7gTpZBY1PJnaZChBZCbMAZAmxjX7ZC4ZCGgDxmRq3HE4Ar9B6rPCGWlwiFZCcm6ZASzuZBzOBcdK93RB0dNCXFyferKXhvTnulDdorm57U05346pytXHxciA87WaPMv6ERDChxNZCFqIat9Csh6xcTVAZDZD", version="2.12")
    
    #Post the input message to facebook
    post = graph.put_object(parent_object='me', connection_name='feed', message=post_message)
    
    print(post)


#Function to get the current fuel prices for bunbury and return it in a dicitonary
def get_lowest_fuel_prices():
    
    fuel_dictionary = {}
    
    #Get the cheapest ULP price and name from fuelwatch gov rss feed
    NewsFeed_ULP = feedparser.parse("https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1&Suburb=Bunbury")#&Day=tomorrow")
    cheapest_ULP = NewsFeed_ULP['entries'][0]
    ULP_name = cheapest_ULP["trading-name"]
    ULP_price = cheapest_ULP["price"]
    fuel_dictionary["Unleaded"] = [ULP_name,ULP_price]
    
    #Get cheapest Premium Unleaded Prices
    NewsFeed_PU = feedparser.parse("https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=2&Suburb=Bunbury")#&Day=tomorrow")
    cheapest_PU = NewsFeed_PU['entries'][0]
    PU_name = cheapest_PU["trading-name"]
    PU_price = cheapest_PU["price"]
    fuel_dictionary["Premium Unleaded"] = [PU_name,PU_price]
    
    
    #Get Cheapest Diesel Prices
    NewsFeed_D = feedparser.parse("https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=4&Suburb=Bunbury")#&Day=tomorrow")
    cheapest_D = NewsFeed_D['entries'][0]
    D_name = cheapest_D["trading-name"]
    D_price = cheapest_D["price"]
    fuel_dictionary["Diesel"] = [D_name,D_price]
    
    
    #Return the resultant dictionary
    return (fuel_dictionary)
    
    
tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime("%A %e %B")
fuel_dictionary = get_lowest_fuel_prices()
fuel_dictionary_keys = sorted(fuel_dictionary.keys(), reverse=True)

fb_message = "****Fuel Prices for " + str(tomorrow) + "****\n\n"
for fuel in fuel_dictionary_keys:
    fb_message = fb_message + fuel + ": " + fuel_dictionary[fuel][1] + "c at " + fuel_dictionary[fuel][0] + "\n"


facebook_post(fb_message)
