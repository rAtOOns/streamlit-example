# Import the streamlit library
import streamlit as st

# Use the write function to introduce the app
st.write("""
# Welcome to My Streamlit App!
This app receives two numbers as input, multiplies them, and displays the result.
""")

# Use the number_input function to get numbers from the user
num1 = st.number_input('Enter first number')
num2 = st.number_input('Enter second number')

# Use a button to handle the calculation
if st.button('Calculate'):
    result = num1 * num2

    # Use the write function to display the result
    st.write('The result is ', result)
