import requests
import json
import pandas as pd
import numpy as np
import streamlit as st


def read_csv(file):
    df = pd.read_csv(file)
    return df

# function to extract info from api

def bulk_pc_lookup(postcodes):
    # set up the api request
    url = "https://api.postcodes.io/postcodes"
    headers = {"Content-Type": "application/json"}
    
    # divide postcodes into batches of 100
    postcode_batches = [postcodes[i:i + 100] for i in range(0, len(postcodes), 100)]
    
    # to store the results
    postcode_data = []
    
    for batch in postcode_batches:
        # specify our input data and response, specifying that we are working with data in json format
        data = {"postcodes": batch}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # check for successful response
        if response.status_code == 200:
            results = response.json()["result"]
            
            for result in results:
                postcode = result["query"]
                
                if result["result"] is not None:
                    lsoa = result["result"]["codes"]["lsoa"]
                    latitude = result["result"]["latitude"]
                    longitude = result["result"]["longitude"]
                    region = result["result"]["region"]
                    postcode_data.append({"Charity Postcode": postcode, "Latitude": latitude, "Longitude": longitude, "LSOA Code": lsoa, "Region": region})
        else:
            # handle errors for each batch
            print(f"Error in batch: {response.status_code}")
    
    return postcode_data

def main():

    secret_key = st.text_input("Enter the password: ")

    if secret_key == 'TURBINE':

        st.title("Test App")

        uploaded_file = st.file_uploader("Upload your csv containing postcodes. Please make sure your postcode column is called 'Postcode'", type=["csv"])


        if uploaded_file is not None:

            st.write('See analysis:')

            df = read_csv(uploaded_file)

            st.write(df.head())

            postcodes = df['Postcodes'].tolist()

            output = bulk_pc_lookup(postcodes)

            output_df = pd.DataFrame(output)

            st.write(output_df)


if __name__ == '__main__':
    main()