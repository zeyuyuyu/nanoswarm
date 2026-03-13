# 🦠 NanoSwarm

<div align="center">
  <p><strong>The world's first ultra-lightweight personal swarm intelligence sandbox.</strong></p>
  <p><strong>Make life decisions with 100 AI advisors on your laptop.</strong></p>
</div>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)

Inspired by the massive simulations of [MiroFish](https://github.com/666ghj/MiroFish) but built for your personal life, NanoSwarm brings the power of **Swarm Intelligence** directly to your local machine (or lightweight API). 

Instead of asking one AI to solve your problem, what if you asked a **Micro-Society** of experts? 

NanoSwarm takes your question (e.g., "Should I quit my job to build an open-source startup?"), automatically generates a diverse panel of AI agents (The Critic, The Optimist, The Data Scientist, The Philosopher), lets them debate it out, and synthesizes a final verdict.

## 🚀 Why NanoSwarm?

*   **🧠 Swarm Intelligence for the Individual:** Not for governments or mega-corps. For *you*.
*   **⚡ Ultra-Lightweight:** Designed to run entirely locally (via Ollama/Llama.cpp) or via cheap fast APIs (Gemini Flash, GPT-4o-mini). No heavy orchestration frameworks needed.
*   **🎭 Dynamic Personas:** Automatically spawns the perfect mix of experts based on *your specific prompt*.
*   **💻 Beautiful Terminal UI:** Built with `rich` for a stunning, color-coded debate experience right in your CLI.

## 🛠️ Quick Start

```bash
git clone https://github.com/zeyuyuyu/nanoswarm.git
cd nanoswarm
pip install -r requirements.txt

# Set your API key (if using LiteLLM/OpenAI/Gemini etc.)
export OPENAI_API_KEY="sk-..."

# Or just use local Ollama! (Set model in config)
python -m nanoswarm.cli "Should I invest in early-stage AI startups right now?"
```

## 🏗️ How it Works

1.  **Ingestion:** You ask a question.
2.  **Casting:** NanoSwarm analyzes the question and dynamically generates 5-20 distinct personas (e.g., Financial Advisor, Skeptic, Risk Taker).
3.  **Ideation (The Swarm):** Each persona generates an independent analysis based on their worldview.
4.  **Debate (The Crucible):** The agents see each other's points and provide critiques and counter-arguments.
5.  **Synthesis:** A master "Synthesizer" reads the entire debate and outputs a cohesive, balanced, final recommendation.

## 🤝 Contributing

PRs are welcome! We want more models, more debate strategies, and even more lightweight core logic.

## 📜 License

MIT License.
