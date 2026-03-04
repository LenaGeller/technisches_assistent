
import streamlit as st
from pipeline import frage_stellen

st.set_page_config(layout="wide")

st.markdown("""
<style>

.block-container {
    max-width: 900px;
    padding-top: 2rem;
}

h1 {
    font-size: 2rem;
}

.stTextInput input {
    font-size: 1.1rem;
    padding: 0.6rem;
}

div.stButton > button {
    width: 100%;
    font-weight: 600;
    border-radius: 6px;
}

.answer-box {
    padding: 1.4rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: #fafafa;
}

</style>
""", unsafe_allow_html=True)

st.title("Technischer Assistent")

st.caption(
"Demonstrator für strukturierte Analyse technischer Regelwerke "
"(RAG + technische Normtexte)"
)

st.markdown("#### Frage stellen")

frage = st.text_input("")

if st.button("Antwort generieren"):

    if not frage.strip():
        st.warning("Bitte Fragestellung eingeben.")
    else:
        with st.spinner("Analyse läuft …"):
            antwort = frage_stellen(frage)

        st.markdown('<div class="answer-box">', unsafe_allow_html=True)
        st.markdown(result["answer"])
        st.markdown('</div>', unsafe_allow_html=True)
        

        if antwort["images"]:
            st.markdown("---")
            st.subheader("Relevante Abbildungen")

            cols = st.columns(len(antwort["images"]))

            for col, img in zip(cols, antwort["images"]):
                with col:
                    st.image(img, use_container_width=True)
