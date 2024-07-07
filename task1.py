from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

context='''You are a Pizza shop owner that can take orders from the customers based on the menu you have.
 Display the menu in a well-formatted manner when requested by the customer. Respond like a real owner by suggesting items and interacting with customers respectfully.
Calculate total cost after every item is ordered and display it.
Based on the order from the customer, you need to sum the total amount and display it to the customer. If the item is not available, you need to tell 
the customer that the 'Item is not available' and ask the user to pick from the options you have. You don't need to 
set up any payment method, you only need to show the final amount'''

menu='''cheese pizza large (10.95), medium(9.25), small(6.50) 
eggplant pizza large (11.95), medium(9.75), small(6.75) 
fries large (4.50), small (3.50) 
greek salad (7.25) 
Toppings:- 
extra cheese (2.00) 
mushrooms (1.50) 
sausage (3.00) 
canadian bacon (3.50) 
AI sauce (1.50) 
peppers (1.00) 
Drinks: -
coke large (3.00), medium (2.00), small (1.00) 
sprite large (3.00), medium (2.00), small (1.00) 
bottled water (5.00)'''

prompt=ChatPromptTemplate.from_messages([
    ("system",'''You are a helpful AI assistant.You will have access to the document {context}.
     You  have access to {menu} and chat history {chat_history} '''),
    ("user","{user_ask}")
])
#output parser
from langchain_core.output_parsers import StrOutputParser
output_parser=StrOutputParser()

chat_history=[]

def get_response(question):
    chain=prompt | llm | output_parser
    result=chain.invoke({"user_ask":question,"chat_history":chat_history,"menu":menu,"context":context,})
    return result
    
while True:
    user_ask=input(">>>")
    chat_history.append(HumanMessage(content=user_ask))
    ai_resp=get_response(user_ask)
    chat_history.append(AIMessage(content=ai_resp))
    print(">>>",ai_resp)


