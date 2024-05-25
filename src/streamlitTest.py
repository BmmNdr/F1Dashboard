import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("My Dashboard")
st.write("This is a simple dashboard created with Streamlit.")

# Create a sample DataFrame
data = pd.DataFrame({
    'A': np.random.randn(100),
    'B': np.random.randn(100),
    'C': np.random.randn(100),
    'D': np.random.randn(100)
})

# Display the DataFrame
st.write(data)

# Line chart
st.line_chart(data)

# Histogram
fig, ax = plt.subplots()
ax.hist(data['A'], bins=20)
st.pyplot(fig)

# Slider
slider_value = st.slider("Select a value", 0, 100, 50)
st.write(f"Selected value: {slider_value}")

# Select box
select_option = st.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
st.write(f"Selected option: {select_option}")

# Button
if st.button("Click Me"):
    st.write("Button clicked!")
