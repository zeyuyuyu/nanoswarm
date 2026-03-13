# 🦠 NanoSwarm

<div align="center">
  <p><strong>The world's first ultra-lightweight personal swarm intelligence sandbox.</strong></p>
  <p><strong>Make decisions and predict the future with a micro-society of AI experts on your laptop.</strong></p>
</div>

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-green.svg)
![Stars](https://img.shields.io/github/stars/zeyuyuyu/nanoswarm)
![Downloads](https://img.shields.io/github/downloads/zeyuyuyu/nanoswarm/total)

Inspired by the massive multi-agent event prediction engines of [MiroFish](https://github.com/666ghj/MiroFish) and the extreme portable efficiency of [PicoClaw](https://github.com/sipeed/picoclaw), **NanoSwarm** brings true Swarm Intelligence directly to your terminal.

Instead of asking just one AI a generic question, what if you asked a **Micro-Society** of experts? 

NanoSwarm takes your real-world prompt (e.g., "Will AGI be achieved by 2027?" or "Should I quit my job?"), dynamically generates a panel of specialized AI agents, injects live web context, and lets them **debate** or run algorithmic **probability predictions**.

## 🚀 Why NanoSwarm?

*   **🔮 Predict Anything:** Use `--mode predict` to let the swarm compute the % probability of a real-world event occurring based on live data (a la MiroFish).
*   **🗣️ Multi-Round Debates:** Allow agents to counter-argue and criticize each other iteratively before reaching a verdict via `--rounds 3`.
*   **⚡ Ultra-Lightweight (The Nano Philosophy):** Designed to run entirely locally (via Ollama) or via cheap fast APIs. No heavy orchestration frameworks (`autogen`, `crewai`) needed. Just native Python `asyncio`.
*   **🌐 Live Reality Grounding:** Pass `--search` to silently scrape DuckDuckGo for the latest context before the debate starts.

## 🛠️ Quick Start

```bash
git clone https://github.com/zeyuyuyu/nanoswarm.git
cd nanoswarm
pip install .

export OPENAI_API_KEY="sk-..."  # Or GEMINI_API_KEY, ANTHROPIC_API_KEY...
```

### Mode 1: Swarm Debate (Life Decisions)
```bash
# Will cast a diverse group, pull live search data, and let them argue for 2 rounds
nanoswarm "Should I buy a house in a major city in 2026?" --search --rounds 2
```

### Mode 2: Swarm Prediction (Market/Tech Forecasts)
```bash
# Will ask the swarm to assign mathematical probabilities 
nanoswarm "Will OpenAI release GPT-5 before December 2026?" --mode predict --search
```

### Mode 3: Local Only (Ollama integration)
```bash
# Don't want to use OpenAI? Use Ollama!
nanoswarm "Should I learn Rust?" --model ollama/llama3
```

## 🏗️ Architecture

1.  **Ingestion & Intel:** If `--search` is enabled, NanoSwarm synthesizes a boolean search query and scrapes the web for zero-day context.
2.  **Casting:** The engine dynamically spawns a customized JSON roster of distinct personas (Skeptics, Analysts, Visionaries) based on the exact topic.
3.  **The Crucible (Async Gathering):** 
    *   *Debate Mode:* Agents read the context and each other's previous statements in an async execution loop.
    *   *Predict Mode:* Agents individually compute probabilities and reasoning, feeding into an aggregate swarm percentage.

## 🤝 Roadmap / Contributing
PRs are welcome! 
- [ ] Agent Memory (saving state locally to JSON/SQLite)
- [ ] HTML/JS visualizer for swarm breakdown
- [ ] Direct MCP integrations for agent tool-use

## 📜 License
MIT License.
