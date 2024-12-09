import streamlit as st
from navigation.clark_wright_page import clark_wright_page
from navigation.dijkstra_page import dijkstra_page

# Main App
st.markdown("#### Algorithm Selection")
choice = st.selectbox("Choose an algorithm to start:", ["Home", "Clark-Wright Savings Algorithm", "Dijkstra's Algorithm"])

if choice == "Clark-Wright Savings Algorithm":
    clark_wright_page()
elif choice == "Dijkstra's Algorithm":
    dijkstra_page()


# Footer
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: green;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by Kai</p>
<p><a style='display: block; text-align: center;' href="https://www.edx.org/masters/micromasters/mitx-supply-chain-management" target="_blank">📚 Awesome learning ride with SCM MM @MITx! 🚀</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
