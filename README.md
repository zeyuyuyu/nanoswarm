# 🦠 NanoSwarm

<div align="center">
  <p><strong>The world's first ultra-lightweight personal swarm intelligence sandbox.</strong></p>
  <p><strong>Make life decisions with 100 AI advisors right on your laptop.</strong></p>
</div>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)

Inspired by the massive agent simulations of [MiroFish](https://github.com/666ghj/MiroFish) and the multi-agent context loops of [BetterFish](https://github.com/betterfish), NanoSwarm brings the power of **Swarm Intelligence** directly to your terminal.

Instead of asking just one AI a generic question, what if you asked a **Micro-Society** of experts? 

NanoSwarm takes your prompt (e.g., "Should I quit my job to build an open-source startup?"), automatically generates a diverse panel of AI agents (The Critic, The Optimist, The Data Scientist, The Philanthropist), injects live search context, lets them debate it out, and synthesizes a final verdict natively in your CLI.

## 🚀 Why NanoSwarm?

*   **🧠 Swarm Intelligence for Individuals:** Not just for governments or macro-finance predictions. For *your* decisions.
*   **⚡ Ultra-Lightweight (like PicoClaw):** Designed to run entirely locally (via Ollama/Llama.cpp) or via cheap fast APIs. No heavy orchestration frameworks needed. Just Python.
*   **🎭 Dynamic Personas:** Automatically spawns the perfect mix of experts based on *your specific prompt*. 
*   **🌐 Live Web Context:** Pass `--search` to silently scrape DuckDuckGo for the latest context before the debate begins so agents aren't hallucinating on old data.

## 🛠️ Quick Start

```bash
git clone https://github.com/zeyuyuyu/nanoswarm.git
cd nanoswarm
pip install .

# Set your API key (if using LiteLLM/OpenAI/Anthropic/Gemini etc.)
export OPENAI_API_KEY="sk-..."

# Run the CLI
nanoswarm "Should I invest in early-stage AI startups right now?"

# Enable Live Search Context
nanoswarm "What are the key takeaways from the MiroFish GitHub launch?" --search

# Use a completely local model via Ollama!
nanoswarm "Should I buy a house in 2026?" --model ollama/llama3
```

## 🏗️ Architecture

1.  **Ingestion & Search:** You ask a question. If `--search` is enabled, a lightweight query is generated and DuckDuckGo is scraped for immediate global context.
2.  **Casting:** NanoSwarm analyzes the question and dynamically generates a personalized JSON array of distinct personas.
3.  **Ideation (The Swarm):** Each persona generates an independent analysis simultaneously using `asyncio.gather`.
4.  **Debate (The Crucible):** The tools run inside a fast async gather loop, streaming the results back to a beautiful `rich` terminal UI wrapper.
5.  **Synthesis:** A master "Synthesizer" reads the entire debate log and outputs a cohesive, balanced, final recommendation.

## 🤝 Roadmap / Contributing
PRs are welcome! 
- [ ] Add Agent Memory across multiple turn debates
- [ ] Swarm Visualizer output (HTML/JS)
- [ ] Connect internal CLI commands to Local MCP endpoints 

## 📜 License
MIT License.
