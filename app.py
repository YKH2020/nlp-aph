import streamlit as st
import subprocess
import time
import os
import pandas as pd

# Page config
st.set_page_config(page_title="Autism Parent Helper", layout="wide")

# Chat and performance state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "performance_log" not in st.session_state:
    st.session_state.performance_log = []

# Title
st.title("🤝 Autism Parent Helper (APH)")

# Tab selector
tab_choice = st.radio("Choose pipeline:", ["🐍 Python", "🦀 Rust", "⚖️ Both"], horizontal=True)

# Input bar
query = st.chat_input("Ask a question about autism, parenting, or support...")

# --- Pipeline Runners ---
def run_python_pipeline(user_query: str):
    start = time.time()
    result = subprocess.run(["python", "./py_scripts/main.py", user_query], capture_output=True, text=True)
    duration = time.time() - start
    output = result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    return output, round(duration, 2)

def run_rust_pipeline(user_query: str):
    start = time.time()
    result = subprocess.run(["./rust_scripts/target/debug/rust_opt", user_query], capture_output=True, text=True)
    duration = time.time() - start
    output = result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    return output, round(duration, 2)

# --- Pipeline Execution ---
if query:
    if tab_choice == "🐍 Python":
        with st.spinner("Running Python pipeline..."):
            response, elapsed = run_python_pipeline(query)
        st.session_state.chat_history.append({
            "query": query,
            "response": response,
            "source": "Python",
            "time": elapsed
        })

    elif tab_choice == "🦀 Rust":
        with st.spinner("Running Rust pipeline..."):
            response, elapsed = run_rust_pipeline(query)
        st.session_state.chat_history.append({
            "query": query,
            "response": response,
            "source": "Rust",
            "time": elapsed
        })

    elif tab_choice == "⚖️ Both":
        with st.spinner("Running Rust pipeline..."):
            rust_response, rust_time = run_rust_pipeline(query)
        with st.spinner("Running Python pipeline..."):
            py_response, py_time = run_python_pipeline(query)

        st.session_state.chat_history.append({
            "query": query,
            "response": f"**🦀 Rust ({rust_time}s):**\n{rust_response}\n\n---\n\n**🐍 Python ({py_time}s):**\n{py_response}",
            "source": "Both",
            "time": round(rust_time + py_time, 2)
        })

        st.session_state.performance_log.append({
            "query": query,
            "rust_time": rust_time,
            "python_time": py_time
        })

    st.rerun()

# --- Chat Display ---
st.markdown("---")
for entry in st.session_state.chat_history:
    if (tab_choice == "🐍 Python" and entry["source"] != "Python") or \
       (tab_choice == "🦀 Rust" and entry["source"] != "Rust") or \
       (tab_choice == "⚖️ Both" and entry["source"] != "Both"):
        continue

    with st.chat_message("user", avatar="❓"):
        st.markdown(entry["query"])
    with st.chat_message("assistant", avatar="🤗"):
        st.markdown(entry["response"])
        st.caption(f"🕒 {entry['source']} response time: {entry['time']}s")

# --- Performance CSV (Both tab only) ---
if tab_choice == "⚖️ Both" and st.session_state.performance_log:
    st.markdown("### 📊 Performance Log")
    df = pd.DataFrame(st.session_state.performance_log)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Save Performance CSV", data=csv, file_name="performance_log.csv")

# --- Control Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔌 Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.performance_log = []
        st.rerun()

with col2:
    if st.button("🧠 Clear Memory", use_container_width=True):
        try:
            os.remove(".summary.txt")
            st.success("Memory (chat summary) cleared.")
        except FileNotFoundError:
            st.warning("No memory file to clear.")
        st.rerun()