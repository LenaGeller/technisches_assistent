from llm import prompt, model, parser
from retrieval import retriever
from langchain_core.prompts import ChatPromptTemplate
import re

def frage_stellen(frage: str):

    # 1. Retrieval
    candidate_docs = retriever.invoke(frage)

    # 2️⃣ Chunks nummerieren
    chunk_texts = []
    for i, d in enumerate(candidate_docs):
        chunk_texts.append(f"[{i}]\n{d.page_content}")

    combined_chunks = "\n\n".join(chunk_texts)

    # 3️⃣ Ein einziger Re-Ranking Call
    rerank_prompt = ChatPromptTemplate.from_template("""
    Du erhältst eine Frage und mehrere Textabschnitte.
                                                     
    Ordne die Textabschnitte nach fachlicher Relevanz für die Beantwortung der Frage.

    Frage:
    {question}

    Textabschnitte:
    {chunks}

    Gib nur eine Liste der Indizes zurück,
    z.B.: 3, 1, 0, 4
    Keine Erklärung.
    """)

    chain_rerank = rerank_prompt | model | parser

    ranking_output = chain_rerank.invoke({
        "question": frage,
        "chunks": combined_chunks
    })

    # 4️⃣ Ranking interpretieren
    try:
        ranked_indices = [
            int(x.strip()) 
            for x in ranking_output.split(",") 
            if x.strip().isdigit()
        ]
    except:
        ranked_indices = []

    # 5️⃣ Top 4 übernehmen
    docs = [candidate_docs[i] for i in ranked_indices[:4] if i < len(candidate_docs)]

    context_parts = []
    image_ids = []
    quellen_liste = set()  # Nutzen ein Set, um Duplikate zu vermeiden

    for d in docs:   # Top 4
        titel = d.metadata.get("quelle") or d.metadata.get("source") or "Unbekannte Quelle"
        quellen_liste.add(titel)
        header = f"[QUELLE: {titel}]"
        context_parts.append(header + "\n" + d.page_content)

        imgs = d.metadata.get("linked_images", "")
        if imgs:
            image_ids.extend([x.strip() for x in imgs.split(",") if x.strip()])

    context = "\n\n".join(context_parts)
    image_ids = list(dict.fromkeys(image_ids))

    # 3. LLM Antwort
    chain = prompt | model | parser
    antwort = chain.invoke({
        "context": context,
        "question": frage
    })

    # --- Abbildungsnummern extrahieren ---
    mentioned = re.findall(
        r"(?:Abbildung|Abb\.)\s*[:\-]?\s*(\d+)",
        antwort,
        flags=re.IGNORECASE
    )

    def extract_id_number(image_id):
        m = re.search(r"abb_(\d+)$", image_id)
        return m.group(1) if m else None

    filtered_image_ids = []

    if mentioned:
        for img_id in image_ids:
            n = extract_id_number(img_id)
            if n and n in mentioned:
                filtered_image_ids.append(img_id)

    if not filtered_image_ids:
        filtered_image_ids = image_ids[:2]  # Max 2

    image_paths = [
        f"images/{img_id}.png"
        for img_id in filtered_image_ids
    ]

    # 5. Strukturierte Rückgabe
    return {
        "answer": antwort,
        "images": image_paths 
        "sources": list(quellen_liste)
    }
