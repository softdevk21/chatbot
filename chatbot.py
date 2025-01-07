import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables
import streamlit as st


st.set_page_config(page_title="OrderArt Chatbot")
st.header("OrderArt Chatbot")

# Replace with your actual API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define model and generation parameters
model_name = "gemini-pro"
generation_config = {
    "temperature": 1,  # Adjust for more controlled responses
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,  # Limit output length
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name=model_name,
    generation_config=generation_config,
)

# Initialize chat history (optional)
chat_history = [
    {
        "role": "user",
        "parts": [{"text": "Hi"}]
    },
    {
        "role": "model",
        "parts": [{"text": "I'm here to help you with your Orderart inquiries. How can I assist you today?"}]
    },
    {
        "role": "user",
        "parts": [{"text": "How does the system handle table reservations?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "The system provides an interface to book tables, check availability, and receive confirmation for reservations."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Can customers order food for delivery or takeout?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, the system supports both delivery and takeout options, allowing customers to specify their preferences."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Does the system support multiple languages?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, the system is designed to support multiple languages to cater to a diverse customer base."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Can the system generate invoices for customers?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, after an order is placed, the system generates an invoice that can be downloaded or sent via email."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Can customers customize their orders?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, customers can customize orders by selecting toppings, portion sizes, or special requests like gluten-free or extra spicy."}]
    },
    {
        "role": "user",
        "parts": [{"text": "How are orders sent to the kitchen?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Once an order is placed, it is automatically routed to the kitchen's display system or printer for preparation."}]
    },
    {
        "role": "user",
        "parts": [{"text": "How does the system handle order cancellations?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Customers can cancel their orders within a specified time, and the system processes refunds automatically if applicable."}]
    },
    {
        "role": "user",
        "parts": [{"text": "What happens if there is a delay in the order?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "The system notifies customers of any delays and provides an updated ETA for delivery or preparation."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Can multiple orders be placed at once?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, customers can place multiple orders, and the system ensures each order is processed independently."}]
    },
    {
        "role": "user",
        "parts": [{"text": "What do we need to use the Orderart Platform?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "All you need is a domain name for your business and a copy of your menu. Our creative team will work the rest of the magic to take you live in the shortest time possible."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Do we pay commission to receive orders or table reservations?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "With Orderart, you own every dollar you earn. Our pricing model is transparent and affordable, and we charge based on a combination of services you deem important for your business. You can always start with our Basic Platform pack and add services when you feel the need."}]
    },
    {
        "role": "user",
        "parts": [{"text": "What form of payments can we accept with Orderart?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Cash on Delivery, Visa, Mastercard, and American Express payments are supported. Additionally, Apple Pay and Google Pay can be enabled for checkout."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Can I customize my site design and colors?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, all of the Orderart themes are uniquely designed and completely customizable to suit your brand."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Can I run my own marketing campaigns?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Yes, you can log in to your site admin interface and run SMS, email, social media, or browser notification campaigns. If life is already busy, ask your customer success manager to handle the marketing for you, including providing a detailed assessment of every campaign with a focus on return on investment."}]
    },
    {
        "role": "user",
        "parts": [{"text": "How am I billed for the additional services or marketing campaigns?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "If the business has subscribed to additional services like SEO or marketing, invoices are generated at the end of every month. You only pay for what you use."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Is the Orderart platform secure?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "Orderart is designed for secure online transactions with SSL encryption in place for your domain."}]
    },
    {
        "role": "user",
        "parts": [{"text": "Do my customers get routed to a 3rd party site for actual ordering?"}]
    },
    {
        "role": "model",
        "parts": [{"text": "No"},{"text":"we host your domain end-to-end, so not only do you save on hosting services, but your customers always stay on your website, significantly improving the Google ranking of your domain."}]
    }
]

response = requests.get('https://www.orderart.com.au')
response.raise_for_status()  # Raise an exception for bad status codes
soup = BeautifulSoup(response.content, "html.parser")

# Get all text content from the HTML
all_text = soup.get_text()
all_text = all_text.strip()  # Remove leading/trailing whitespace
all_text = ' '.join(all_text.split())  # Remove extra spaces
print(all_text)
chat_history.append({"role": "user", "parts": [{"text": all_text}]})


def chat(user_input):
    global chat_history
    chat_history.append({"role": "user", "parts": [{"text": "Only give answer based on give data only. \n"+user_input}]})

    try:
        chat_session = model.start_chat(history=chat_history)
        response = chat_session.send_message(user_input)
        chat_history.append({"role": "model", "parts": [{"text": response.text}]})
        return response.text

    except Exception as e:
        print(f"Error during chat: {e}")
        return "I'm having some trouble understanding. Can you please rephrase?"

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

# st.subheader("The Chat History is")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
if submit and input:
    input = input
    response_bot = chat(input)
    print("Bot:", response_bot)
    st.session_state['chat_history'].append(("You", input))
    st.session_state['chat_history'].append(("Bot", response_bot))

    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

    # st.write(f"You: {input}")
    # st.write(f"Bot: {response_bot}")



# Example usage
# while True:
#   user_input = input("You: ")
#   if user_input.lower() == "exit":
#     break
#   bot_response = chat(user_input)
#   print("Bot:", bot_response)