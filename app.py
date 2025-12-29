import streamlit as st
from chat.processor import EKGProcessor

st.title("EKG Neo4j Query Generator")

processor = EKGProcessor()

question = st.text_input("Enter your question about the EKG graph:")

if question:
    try:
        cypher = processor.generate_cypher(question)
        st.subheader("Generated Cypher Query")
        st.code(cypher, language="cypher")
    except Exception as e:
        st.error(str(e))
