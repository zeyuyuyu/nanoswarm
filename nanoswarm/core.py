import asyncio
from typing import List, Dict, Optional
import litellm
import json

litellm.drop_params = True

class SwarmAgent:
    def __init__(self, name: str, persona: str, model: str = "gpt-4o-mini"):
        self.name = name
        self.persona = persona
        self.model = model

    async def generate_thought(self, prompt: str, global_context: str = "", previous_rounds: str = "") -> str:
        system_msg = f"You are {self.name}. Your persona is: {self.persona}. You must answer from this strict perspective. Keep your response concise, sharp, and insightful."
        messages = [{"role": "system", "content": system_msg}]
        
        if global_context:
            messages.append({"role": "system", "content": f"Global Context found from the web:\n{global_context}"})
            
        if previous_rounds:
            messages.append({"role": "system", "content": f"Previous Debate History:\n{previous_rounds}"})
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await litellm.acompletion(model=self.model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"[{self.name} encountered an error: {str(e)}]"

    async def predict_probability(self, topic: str, context: str) -> dict:
        system_msg = f"You are {self.name}. Your persona is: {self.persona}. Based on the topic and context, what is the % probability of this occurring/being true? You MUST respond in pure JSON format: {{\"probability\": <0-100>, \"reasoning\": \"<short string>\"}}"
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Topic: {topic}\nContext: {context}"}
        ]
        try:
            response = await litellm.acompletion(model=self.model, messages=messages, temperature=0.2)
            raw = response.choices[0].message.content.strip()
            if raw.startswith("```json"): raw = raw.split("```json")[1].split("```")[0].strip()
            elif raw.startswith("```"): raw = raw.split("```")[1].split("```")[0].strip()
            return json.loads(raw)
        except Exception:
            return {"probability": 50, "reasoning": "Failed to compute. Defaulting to 50% uncertainty."}


class NanoSwarm:
    def __init__(self, model: str = "gpt-4o-mini", enable_search: bool = False):
        self.model = model
        self.agents: List[SwarmAgent] = []
        self.enable_search = enable_search
        self.global_context = ""
        self.debate_history = ""

    async def _gather_context(self, topic: str):
        if not self.enable_search:
            return
        from nanoswarm.tools import web_search
        msg = [{"role": "user", "content": f"Given the topic '{topic}', generate a highly specific 3-5 word search query for DuckDuckGo to find the latest news. Reply with ONLY the query string."}]
        try:
            resp = await litellm.acompletion(model=self.model, messages=msg)
            query = resp.choices[0].message.content.strip().strip("'\"")
            self.global_context = web_search(query, max_results=5)
        except Exception as e:
            self.global_context = f"Search failed: {str(e)}"

    async def _cast_agents(self, topic: str, count: int = 4) -> List[SwarmAgent]:
        prompt = f"I have a topic: '{topic}'. Give me a JSON array of {count} highly distinct, opinionated personas/experts who should debate this topic. Each item should have a 'name' and a 'persona_description'. Formats: JSON array only."
        messages = [{"role": "user", "content": prompt}]
        try:
            response = await litellm.acompletion(model=self.model, messages=messages, temperature=0.7)
            raw_content = response.choices[0].message.content
            if raw_content.startswith("```json"): raw_content = raw_content.split("```json")[1].split("```")[0].strip()
            elif raw_content.startswith("```"): raw_content = raw_content.split("```")[1].split("```")[0].strip()
            data = json.loads(raw_content)
            self.agents = [SwarmAgent(name=item['name'], persona=item['persona_description'], model=self.model) for item in data]
        except Exception:
            self.agents = [
                SwarmAgent("The Optimist", "Sees only positive potential and upside.", self.model),
                SwarmAgent("The Critic", "Sees only flaws, risks, and worst-case scenarios.", self.model),
                SwarmAgent("The Pragmatist", "Focuses on realistic execution and hard data.", self.model),
                SwarmAgent("The Lateral Thinker", "Approaches the problem from completely unexpected angles.", self.model)
            ]
        return self.agents

    async def debate(self, topic: str, rounds: int = 1) -> List[Dict[str, str]]:
        if self.enable_search and not self.global_context:
             await self._gather_context(topic)
        if not self.agents:
            await self._cast_agents(topic)
            
        all_rounds = []
        self.debate_history = ""
        
        for r in range(rounds):
            tasks = []
            round_prompt = f"Analyze this topic from your unique perspective: {topic}" if r == 0 else f"React to the previous round of debate regarding: {topic}. Critique others if necessary."
            
            for agent in self.agents:
                tasks.append(agent.generate_thought(round_prompt, self.global_context, self.debate_history))
            
            results = await asyncio.gather(*tasks)
            round_data = {agent.name: thought for agent, thought in zip(self.agents, results)}
            all_rounds.append(round_data)
            
            # Update history
            self.debate_history += f"--- Round {r+1} ---\n"
            for name, thought in round_data.items():
                self.debate_history += f"[{name}]: {thought}\n\n"
                
        return all_rounds

    async def predict(self, topic: str) -> dict:
        """Run a predictive swarm vote."""
        if self.enable_search and not self.global_context:
             await self._gather_context(topic)
        if not self.agents:
            await self._cast_agents(topic)
            
        tasks = [agent.predict_probability(topic, self.global_context) for agent in self.agents]
        results = await asyncio.gather(*tasks)
        
        predictions = {agent.name: res for agent, res in zip(self.agents, results)}
        
        try:
            avg_prob = sum([r.get("probability", 50) for r in results]) / len(results)
        except Exception:
            avg_prob = 50.0
            
        return {
            "average_probability": round(avg_prob, 2),
            "breakdown": predictions
        }

    async def synthesize(self, topic: str) -> str:
        prompt = f"Topic: {topic}\n\nDebate History:\n{self.debate_history}\n\nAct as the Master Synthesizer. Synthesize the debate. Provide a structured final verdict."
        messages = [{"role": "user", "content": prompt}]
        try:
            response = await litellm.acompletion(model=self.model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to synthesize: {str(e)}"
