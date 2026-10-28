import streamlit as st
from modules import(
    objetivo,
    datos,
)

st.set_page_config(page_title='Proyecto', page_icon='', initial_sidebar_state='collapsed')

def main():
    st.title('Proyecto -  Propuesta para mitigar el acoso cibernético en entornos de educación superior')
    st.sidebar.title('Navegación')
    menu = ['Objetivo', 'Datos recopilados']
    option = st.sidebar.selectbox("Menu", menu)
    if option.lower() == 'objetivo':
        objetivo.mostrar_info()
    elif option.lower() == 'datos recopilados':
        datos.grafica()


if __name__ == '__main__':
    main()