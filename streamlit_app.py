# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

# Write directly to the app
st.title("Customize your Smoothies:")
st.write(
    """Choose fruits you want in your customer smoothies.
    """
)

name_on_order = st.text_input('Name on Smoothies')
st.write('The name on your smoothie will be', name_on_order)

cnx= st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select((col('FRUIT_NAME')))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('choose upto 5 ingrediets:', my_dataframe, max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string =''

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen +' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')    
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('your smoothie is ordered ' + name_on_order)
    #st.write(my_insert_stmt)

