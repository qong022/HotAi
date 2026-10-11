# Hot Ai (v3.1)

A high-performance, hybrid desktop AI workspace engineered with Python, `pywebview`, and `litellm`. Hot Ai bridges real-time cloud language models with local offline neural runtimes through a single unified glassmorphic interface.

**Developer:** [Your Name] ([@qong022](https://github.com/qong022))  
**Platform:** Windows 10 / 11 (x64)  
**Distribution:** Standalone Single-File Binary / Windows Installer  

---

## ⚡ Architecture & Supported Engines

Hot Ai dynamically orchestrates multiple foundation models depending on network state and workload requirements:

* **Google Gemini (Cloud Hub):** High-capacity contextual analysis leveraging Gemini 1.5/2.0 Flash for multi-turn conversational reasoning.
* **Groq Engine (Ultra-Low Latency):** Near-instantaneous cloud inference powering open-weights reasoning (Llama 3.3 / DeepSeek).
* **Ollama (Local Offline Hub):** Zero-telemetry, fully private local execution using `llama3.1` over `localhost:11434` without an internet connection.
* **Hyper Cluster (Multi-Model Synthesis):** Simultaneous tri-engine query pipeline with built-in cloud-to-local failover if cloud APIs experience 503 capacity throttling.

---

## 📥 Installation

Download the official installer directly from the [Releases](https://github.com/qong022/HotAi/releases) tab:

1. Download **`HotAi_Setup.exe`**.
2. Run the wizard to install Hot Ai and automatically generate your desktop shortcut.
3. Open the installed application:
   * **For Cloud Modes:** Provide free API keys for Gemini and Groq inside your `.env` configuration file.
   * **For Offline Mode:** Select the Ollama prompt during setup or ensure [Ollama](https://ollama.com) is installed with `llama3.1`.

---

## 🛠️ Built With

* **GUI:** HTML5, CSS3 Glassmorphism, PyWebView
* **Inference Orchestration:** LiteLLM & Tiktoken
* **Packaging:** PyInstaller & Inno Setup Compiler