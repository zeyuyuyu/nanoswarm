# 🦠 NanoSwarm

<div align="center">
  <p><strong>The world's first ultra-lightweight personal swarm intelligence sandbox.</strong></p>
  <p><strong>Make life decisions with 100 AI advisors right on your laptop.</strong></p>
</div>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)

Inspired by the massive simulations of [MiroFish](https://github.com/666ghj/MiroFish) but custom-built for an individual's personal life, NanoSwarm brings the power of **Swarm Intelligence** directly to your local machine (or lightweight API). 

Instead of asking just one AI to solve your problem, what if you asked a **Micro-Society** of experts? 

NanoSwarm takes your question (e.g., "Should I quit my job to build an open-source startup?"), automatically generates a diverse panel of AI agents (The Critic, The Optimist, The Data Scientist, The Philosopher), lets them debate it out, and synthesizes a final verdict natively in your terminal.

## 🚀 Why NanoSwarm?

*   **🧠 Swarm Intelligence for the Individual:** Not just for governments or mega-corps. For *you*.
*   **⚡ Ultra-Lightweight:** Designed to run entirely locally (via Ollama/Llama.cpp) or via cheap fast APIs (using `litellm`). No heavy orchestration frameworks needed.
*   **🎭 Dynamic Personas:** Automatically spawns the perfect mix of experts based on *your specific prompt*.
*   **💻 Beautiful Terminal UI:** Built with `rich` for a stunning, color-coded debate experience right in your CLI.

## 🛠️ Quick Start

```bash
git clone https://github.com/zeyuyuyu/nanoswarm.git
cd nanoswarm
pip install .

# Set your API key (if using LiteLLM/OpenAI/Anthropic/Gemini etc.)
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."

# Run the CLI
nanoswarm "Should I invest in early-stage AI startups right now?"

# Or specify a different model entirely (via LiteLLM router)
nanoswarm "What is the meaning of life?" --model gemini/gemini-pro
```

## 🏗️ How it Works

1.  **Ingestion:** You ask a question.
2.  **Casting:** NanoSwarm analyzes the question and dynamically generates distinct personas (e.g., Financial Advisor, Skeptic, Risk Taker).
3.  **Ideation (The Swarm):** Each persona generates an independent analysis based on their specific worldview.
4.  **Debate (The Crucible):** The tools run inside a fast async gather loop. 
5.  **Synthesis:** A master "Synthesizer" reads the entire debate log and outputs a cohesive, balanced, final recommendation.

## 🤝 Contributing

PRs are welcome! We want more local model tooling, alternative debate strategies (e.g., recursive cross-examination), and even more lightweight core logic.

## 📜 License

MIT License.
