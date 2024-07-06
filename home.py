import streamlit as st

def main():

    st.header('welcome to pylj online!')

    st.write("""
             This homepage uses streamlit to allow online access to pylj-powered simulations.
             For a code-free experience, the pages accessed through the sidebar will allow a user to create 
             Monte Carlo and Molecular Dynamics simulations directly on a streamlit page.
             For those looking to dive into the code itself, the button below will take you to the GitHub
             repository, containing the package base code as well as several exampe Jupyter notebooks.
             Alternatively, these notebooks can be accessed online through the pyodide-powered Jupyter 
             Lite examples, hosted on a GitHub page

             """)

    st.link_button(label = 'See the repository', url = 'https://github.com/arm61/pylj')
    st.link_button(label = 'jupyter lite', url = 'https://maximillian-dolan.github.io/pylj-online')

if __name__ == "__main__":
    main()