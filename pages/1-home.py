import streamlit as st

st.set_page_config(layout="wide")
# Custom HTML/CSS for the banner
custom_html = """
<div class="banner">
    <img src="https://github.com/user-attachments/assets/aa4f6b8b-aae1-4b9f-a37a-b98c471a7d46" alt="Banner Image">
</div>
<style>
    .banner {
        width: 100%;
        height: 900px;
        overflow: hidden;
    }
    .banner img {
        width: 100%;
        object-fit: cover;
    }
</style>
"""
# Display the custom HTML
st.components.v1.html(custom_html)

# Sidebar content
st.sidebar.header("우리FISA TA")
st.sidebar.subheader("Subheading")
st.sidebar.text("Sidebar content goes here.")

# Main content
st.title("Main Content")
st.write("Welcome to my Streamlit app!")
st.write("This is the main content area.")