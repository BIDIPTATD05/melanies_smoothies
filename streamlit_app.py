# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session ,only for SiS
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie"""
)


name_on_order = st.text_input("Name of the Smoothie")
st.write("The name of your Smoothie will be:", name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    'Choose upto 5 ingredients: '
    , my_dataframe, 
    max_selections=5
)

if ingredients_List:
    ingredients_string=''

    for fruit_chosen in ingredients_List:
        ingredients_string+=fruit_chosen+ ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width= True)
   

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
            values('""" + ingredients_string + """','""" +name_on_order+"""') """
   
    st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie  is ordered ", icon="✅")





