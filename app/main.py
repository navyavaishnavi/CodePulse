import streamlit as st
from complexity_analyzer import ComplexityAnalyzer


st.set_page_config(
    page_title="CodePulse",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ CodePulse")
st.subheader("AI-Powered Code Complexity Analyzer")

code_input = st.text_area(
    "Paste Your Python Code Here",
    height=300
)

if st.button("Analyze Code"):

    analyzer = ComplexityAnalyzer(code_input)

    result = analyzer.analyze()

    st.success("Analysis Complete")

    st.write("### Analysis Results")

    st.write(f"🔁 Total Loops Detected: {result['loops']}")

    st.write(f"🔄 Nested Loops Present: {result['nested_loops']}")

    st.write(f"📈 Estimated Time Complexity: {result['estimated_complexity']}")
