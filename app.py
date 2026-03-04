
import streamlit as st
from pipeline import frage_stellen


st.set_page_config(
    page_title="Technischer Assistent",
    layout="centered"
)

st.markdown("""
<style>
h2 { margin-bottom: 0.3rem; }
div[data-testid="stTextInput"] { margin-top: -0.5rem; }
div.stButton > button {
    width: 100%;
    border-radius: 4px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h2>Technischer Assistent (Demo)</h2>
<p style="font-size:0.9rem; color:gray;">
Demonstrator für strukturierte Verarbeitung technischer Regelwerke.
</p>
""", unsafe_allow_html=True)

st.markdown("#### Frage stellen")

frage = st.text_input("")

if st.button("Antwort generieren"):

    if not frage.strip():
        st.warning("Bitte Fragestellung eingeben.")
    else:
        with st.spinner("Analyse läuft …"):
            antwort = frage_stellen(frage)

        st.markdown("---")
        st.markdown(antwort)

        if antwort["images"]:
            st.markdown("---")
            st.subheader("Relevante Abbildungen")

            for img in antwort["images"]:
                st.image(img, use_column_width=True)
