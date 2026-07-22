# Import python packages
import os
import snowflake.connector as sc
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be: ", name_on_order)

private_key_file = 'rsa_key.p8'

conn_params = {
    'account': 'LARAJJK-AHB36729',
    'user': 'CraigRobertson',
    'authenticator': 'SNOWFLAKE_JWT',
    'private_key_file': private_key_file,
    'private_key_file_pwd': 'SnowFlake',
    'warehouse': 'COMPUTE_WH',
    'database': 'SMOOTHIES',
    'schema': 'PUBLIC'
}

ctx = sc.connect(**conn_params)
cs = ctx.cursor()

#cnx = st.connection("snowflake")
#session = cnx.session()
cnx = ctx.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string +"""','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' +name_on_order+ '!', icon="✅")
