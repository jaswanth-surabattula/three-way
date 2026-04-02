# Project Guidelines for Claude Code

## What this app is
A web-based AI/LLM tool built with Python and Gradio. The UI should feel like a premium,
dark-mode-first developer tool — think Vercel dashboard, Raycast, or Linear.

---

## UI & Design Rules

### Aesthetic
- Dark mode only. Never use light backgrounds.
- Minimal, high-density layouts. No excessive padding or whitespace.
- Everything should feel intentional and precise — not decorative.
- Subtle borders and dividers over heavy shadows.

### Colors (apply via Gradio theme or custom CSS)
- Background: `#0a0a0a` (near-black)
- Surface / card: `#111111` or `#161616`
- Border: `#262626`
- Primary accent: `#ffffff` or a single color like `#6366f1` (indigo) — pick one and stick to it
- Muted text: `#737373`
- Body text: `#e5e5e5`
- Success: `#22c55e`, Error: `#ef4444`, Warning: `#f59e0b`

### Typography
- Prefer monospace for outputs, code, and model responses (e.g. `font-family: 'JetBrains Mono', monospace`)
- Use a clean sans-serif for labels and UI chrome (e.g. Inter)
- Keep font sizes tight: labels at 12–13px, body at 14px

### Components
- Use `gr.Blocks()` for all layouts — never `gr.Interface()` unless prototyping
- Prefer `gr.Row()` and `gr.Column()` for precise control
- Inputs on the left, outputs on the right (standard LLM tool layout)
- Chatbots: use `gr.Chatbot()` with `bubble_full_width=False`
- Buttons: keep them small and text-only unless it's a primary CTA
- Avoid Gradio's default colorful theme — always apply a custom dark theme

### Custom CSS pattern
Always inject CSS via `gr.Blocks(css=...)` or a `.css` file. Example overrides to always include:
```css
.gradio-container {
  background: #0a0a0a !important;
  font-family: 'Inter', sans-serif;
}
.gr-button {
  border-radius: 6px;
  font-size: 13px;
}
.gr-box, .gr-form {
  background: #111111;
  border: 1px solid #262626;
  border-radius: 8px;
}
textarea, input[type="text"] {
  background: #161616 !important;
  color: #e5e5e5 !important;
  border: 1px solid #262626 !important;
}
```

---

## Layout Patterns

### Standard LLM tool layout
```
[Header / App title row]
[Settings / config row — collapsible if complex]
[Left col: Input + controls] [Right col: Output / chat]
[Footer: status, token count, or metadata]
```

### For chat-style interfaces
- Full-width `gr.Chatbot()` at the top
- Input textbox + submit button pinned at bottom
- System prompt in a collapsible `gr.Accordion()`

---

## Gradio-specific Rules
- Always set `show_label=False` on textboxes when the context is obvious
- Use `gr.Markdown()` for section headers styled with HTML if needed
- Prefer `gr.Dropdown()` over radio buttons for options with 3+ items
- Set `scale=` parameters explicitly to control column widths
- Use `gr.State()` for any app state — never globals in multi-user context
- Always handle errors gracefully — show them in a visible `gr.Textbox(interactive=False)`

---

## What to avoid
- Do NOT use `gr.Interface()` for production layouts
- Do NOT leave Gradio's default orange/green theme — always override
- Do NOT use full-width buttons unless it's the single primary action
- Do NOT add unnecessary helper text or placeholder walls of text
- Do NOT use light backgrounds, ever
- Do NOT stack everything vertically — use rows and columns

---

## When I say "fix the UI", I mean:
1. Apply the dark color palette above
2. Tighten spacing and padding
3. Use the standard LLM layout (inputs left, outputs right)
4. Inject the base CSS overrides
5. Make it look like a tool a developer would actually want to use

## Reference apps for visual inspiration
- vercel.com/dashboard
- raycast.com
- linear.app