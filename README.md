---
title: Tri-Model LLM Arena
emoji: 🥊
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
tags:
- llm-benchmarking
- openai
- claude
- gemini
- comparison
---

# Tri-Model LLM Arena 🥊 

A unified, asynchronous chat interface designed to compare the "Big Three" AI providers—Anthropic, Google, and OpenAI—simultaneously within a single, responsive dashboard.

## 🚀 Overview
Tri-Model LLM Arena allows developers and researchers to send a single prompt and receive three parallel responses. It provides a "Replit-inspired" UI that adapts between desktop and mobile, offering deep insights into the performance and economics of each model through real-time telemetry.

## ✨ Key Features
* **Asynchronous Execution:** Queries Claude, Gemini, and GPT APIs in parallel to minimize wait times and ensure simultaneous streaming.
* **Flexible UI (Replit-Style):**
    * **Desktop:** 3-pane side-by-side layout with an option to stack windows vertically.
    * **Mobile:** Vertical stack with two panes closed by default (toggleable).
* **Model Tier Presets:** Quickly switch between comparison sets:
    * **Flash:** GPT-4o-mini, Gemini 1.5 Flash, Claude 3.5 Haiku.
    * **Pro/Mid:** GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet.
    * **SOTA:** o1-preview, Gemini 2.0 Ultra, Claude 3 Opus.
* **Real-time Analytics (Hovering Report):**
    * **Latency:** Average response time in seconds.
    * **Tokens:** Total cumulative prompt and completion tokens.
    * **Cost:** Estimated USD spend based on current provider pricing.
* **Session Reporting:** Option to download a full session report (PDF/HTML) before closing, featuring series charts and an AI-generated performance summary.

## 🛠️ Tech Stack
* **Framework:** [Gradio](https://gradio.app/)
* **Backend:** Python (with `asyncio` for non-blocking API calls)
* **Hosting:** Hugging Face Spaces
* **Version Control:** GitHub

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/jaswanth-surabattula/tri-model-arena.git](https://github.com/jaswanth-surabattula/tri-model-arena.git)
    cd tri-model-arena
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_key_here
    ANTHROPIC_API_KEY=your_key_here
    GEMINI_API_KEY=your_key_here
    ```

4.  **Run the app locally:**
    ```bash
    python app.py
    ```

## 📊 Analytics Logic
The application calculates session metrics using the following logic:
* **Latency ($L$):** $L = T_{response} - T_{request}$
* **Cost Calculation:** $$Cost = \sum (Tokens_{in} \cdot Rate_{in}) + (Tokens_{out} \cdot Rate_{out})$$
## 🔄 Keeping Models Up to Date

Model IDs and pricing are hardcoded in `src/three_way/core/config.py`.
When providers release new models or retire old ones, update that file manually.

See **[docs/how_to_update_models.md](docs/how_to_update_models.md)** for step-by-step instructions,
including where to find model IDs, how to convert pricing to the format the code expects,
and which deprecation pages to watch.

## 📝 License
This project is licensed under the **MIT License**. This allows for open contribution and modification while keeping the tool accessible to the community. See the [LICENSE](LICENSE) file for more details.
