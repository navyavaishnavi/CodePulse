import streamlit as st

from modules.complexity_analyzer import ComplexityAnalyzer
from modules.performance_tracker import PerformanceTracker
from modules.version_comparator import VersionComparator


st.set_page_config(
    page_title="CodePulse",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ CodePulse")

# SIDEBAR MODULES
module = st.sidebar.selectbox(
    "Choose Module",
    [
        "Complexity Analyzer",
        "Version Comparator"
    ]
)

# -------------------------------
# COMPLEXITY ANALYZER MODULE
# -------------------------------

if module == "Complexity Analyzer":

    st.subheader("AI-Powered Code Complexity Analyzer")

    code_input = st.text_area(
        "Paste Your Python Code Here",
        height=300
    )

    if st.button("Analyze Code"):

        analyzer = ComplexityAnalyzer(code_input)

        result = analyzer.analyze()

        performance = PerformanceTracker(code_input)

        performance_result = performance.analyze_performance()

        st.success("Analysis Complete")

        st.write("### Analysis Results")

        st.write(f"🔁 Total Loops Detected: {result['loops']}")

        st.write(f"🔄 Nested Loops Present: {result['nested_loops']}")

        st.write(
            f"📈 Estimated Time Complexity: "
            f"{result['estimated_complexity']}"
        )

        st.write(
            f"⏱ Execution Time: "
            f"{performance_result['execution_time']} seconds"
        )

        st.write(
            f"💾 Memory Usage: "
            f"{performance_result['memory_usage_kb']} KB"
        )

# -------------------------------
# VERSION COMPARATOR MODULE
# -------------------------------

elif module == "Version Comparator":

    st.subheader("Dependency Version Comparator")

    comparator = VersionComparator()

    st.write("Upload two requirements.txt files")

    old_file = st.file_uploader(
        "Upload OLD requirements.txt",
        type=["txt"],
        key="old"
    )

    new_file = st.file_uploader(
        "Upload NEW requirements.txt",
        type=["txt"],
        key="new"
    )

    if old_file and new_file:

        old_deps = comparator.read_requirements(old_file)

        new_deps = comparator.read_requirements(new_file)

        changes = comparator.compare_dependencies(
            old_deps,
            new_deps
        )

        if changes:

            st.success("Comparison Complete")

            st.table(changes)

        else:

            st.info("No dependency changes detected")
