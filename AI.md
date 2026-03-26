# AI Project Context & Architecture

## 🎯 Project Goals
- A real-time comparative chat interface for side-by-side benchmarking of Claude, Gemini, and OpenAI models. Features asynchronous API calls, Replit-style responsive UI, and detailed session performance analytics (latency, tokens, and cost).
- **Model Tiers:**
    - **Flash:** GPT-4o-mini, Gemini 1.5 Flash, Claude 3.5 Haiku.
    - **Pro/Mid:** GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet.
    - **SOTA:** o1-preview, Gemini 2.0 Ultra, Claude 3 Opus.

## 🛠 Tech Stack
- **Language:** Python (uv) / Gradio
- **AI Agents:** Gemini / Claude
- **Containers:** Docker (OrbStack)

## 📂 Folder Structure
- **src/three_way/core/**: Config & Constants (API keys, model rate mappings).
- **src/three_way/services/**: LLM logic & DB clients.
- **src/three_way/models/**: Data schemas.
- **src/three_way/utils/**: Helpers.

## 🤖 AI Instructions
- Use 'Ruff' for formatting.
- Keep logic in 'services' and config in 'core'.
- Implement asynchronous streaming for all three providers to ensure simultaneous UI updates.
- **Analytics Logic:**
    - Calculate Latency: $L = T_{response} - T_{request}$.
    - Calculate Cost: $Cost = \sum (Tokens_{in} \times Rate_{in}) + (Tokens_{out} \times Rate_{out})$.
- Ensure the UI is responsive: 3-pane side-by-side for desktop, vertical stack for mobile.
