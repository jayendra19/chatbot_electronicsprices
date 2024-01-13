import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests



app = Flask(__name__)

@app.route('/')
def index():
    return "hello"





@app.route('/get_price/<product_name>', methods=['POST'])
def get_price(product_name):
    with app.app_context():
        load_dotenv()
        PRICEYUGE_API_KEY = os.getenv("API_KEY")
        SEARCH_API_URL = "https://price-api.datayuge.com/api/v1/compare/search"
        DETAIL_API_URL = "https://price-api.datayuge.com/api/v1/compare/detail"
        try:
            # Get product name from the Dialogflow intent
            # Get product name from the request data or set a default value
            #product_name = request.args.get('product_name', 'N/A')
            '''data = request.json
            #print(data)
            product_name = data.get('product_name')'''
            '''product_name = data['queryResult']['parameters']['product']'''

            # Make API call to fetch product details
            search_querystring = {
                "api_key": PRICEYUGE_API_KEY,
                "product": product_name,
                "page": "1"
            }
            search_response = requests.get(SEARCH_API_URL, params=search_querystring)
            search_data = search_response.json()
            

            # Check if 'data' is a list and not empty
            if isinstance(search_data.get('data'), list) and search_data['data']:
                product_info = search_data['data'][0]

                # Extract relevant information
                product_id = product_info.get('product_id', 'N/A')
                product_name_check = product_info.get('product_name', 'N/A')
                product_model_check = product_info.get('product_model', 'N/A')
                

                if product_name.lower() in product_name_check.lower() or product_name.lower() in product_model_check.lower():
                    return jsonify({'fulfillmentText': f"Sorry, no details found for {product_name}."})
                # Make API call to fetch detailed information (including prices for Amazon and Flipkart)
                detail_querystring = {
                    "api_key": PRICEYUGE_API_KEY,
                    "id": product_id}
                

                detail_response = requests.get(DETAIL_API_URL, params=detail_querystring)
                detail_data = detail_response.json()
                #print(detail_data)


                is_available = detail_data.get('data', {}).get('is_available', False)
                product_images = detail_data.get('data', {}).get('product_images', [])

                # Extract Amazon and Flipkart prices
                stores_data = detail_data.get('data',{}).get('stores', [])

                #print(stores_data)

                # Extract Amazon and Flipkart prices
                # Prepare response
                response_text = f"Detailed information for {product_name}:\n"
                for store in stores_data:
                    for store_name, store_info in store.items():
                        # Check if the store_info is not an empty list
                        if not store_info:
                            continue

                        response_text += f"- {store_name.capitalize()} Price: ₹{store_info.get('product_price', 'N/A')}\n"
                        response_text += f"- {store_name.capitalize()} Color: {store_info.get('product_color', 'N/A')}\n"
                        response_text += f"- {store_name.capitalize()} Offer: {store_info.get('product_offer', 'N/A')}\n"
                        response_text += f"- {store_name.capitalize()} Delivery Dates: {store_info.get('product_delivery', 'N/A')} Days\n"
                        response_text += f"- {store_name.capitalize()} Emi: {store_info.get('is_emi', 'No Emi')}\n"
                        response_text += f"- {store_name.capitalize()} Cod: {store_info.get('is_cod', 'Not Cod(Cash On Delivery)')}\n"
                        response_text += f"- {store_name.capitalize()} Return time: {store_info.get('return_time', 'N/A')}\n"
                

                response_text += f"-Product Images: {', '.join(product_images)} \n"
                #print(response_text)
                return jsonify({'fulfillmentText': response_text})


            else:
                
                return jsonify({'fulfillmentText': f"Sorry, no prices found for {product_name}."})

        except Exception as e:
            return jsonify({'fulfillmentText': f"Error: {str(e)}"})


    

#if __name__ == "__main__":
    #app.run()
