
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

st.markdown("""
Demonstrator für die strukturierte Analyse technischer Regelwerke (RAG + technische Normtexte)  

### Dokumentbasis  

Dieser Assistent basiert aktuell **nur auf Kapitel 5** des folgenden Dokuments:   
[IVD-Merkblatt Nr. 3-1 - Konstruktive Ausführung und Abdichtung von Fugen in Sanitär- und Feuchträumen](https://www.abdichten.de/media/merkblaetter/03-1/ivd-merkblatt03-1.pdf)  
Er beantwortet daher **nur Fragen zu diesem Kapitel.**  

Der Prototyp demonstriert das Prinzip:  
Ein solches System kann problemlos auf **viele Dokumente oder ganze Normensammlungen** erweitert werden.
""")

example_questions = [
"Wie wird eine Anschlussfuge zwischen zwei Wänden abgedichtet?",
"Wie wird eine Boden-Wand-Fuge fachgerecht ausgeführt und abgedichtet?",
"Wie wird eine Dreiecksfuge mit Dreikantfase ausgeführt?",
"Wie wird eine Rechteckfuge konstruktiv ausgeführt?",
"Wie wird eine Fuge an Bade- oder Duschwannen fachgerecht abgedichtet?"
]

st.subheader("Beispielfragen")

if "frage" not in st.session_state:
    st.session_state.frage = ""

for q in example_questions:
    if st.button(q):
        st.session_state.frage = q

st.markdown("#### Frage stellen")

frage = st.text_input("", key="frage")

if st.button("Antwort generieren"):

    if not frage.strip():
        st.warning("Bitte Fragestellung eingeben.")
    else:
        with st.spinner("Dokumente werden analysiert…"):
            antwort = frage_stellen(frage)

        with st.container(border=True):
            st.markdown(antwort["answer"])
        

        if antwort["images"]:
            st.markdown("---")
            st.subheader("Relevante Abbildungen")

            cols = st.columns(len(antwort["images"]))

            for col, img in zip(cols, antwort["images"]):
                with col:
                    st.image(img, use_container_width=True)
