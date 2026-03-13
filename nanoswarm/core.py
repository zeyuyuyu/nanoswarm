import asyncio
from typing import List, Dict
import litellm
import json

litellm.drop_params = True

class SwarmAgent:
    def __init__(self, name: str, persona: str, model: str = "gpt-4o-mini"):
        self.name = name
        self.persona = persona
        self.model = model

    async def generate_thought(self, prompt: str) -> str:
        system_msg = f"You are {self.name}. Your persona is: {self.persona}. You must answer from this strict perspective."
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
        response = await litellm.acompletion(model=self.model, messages=messages)
        return response.choices[0].message.content

class NanoSwarm:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.agents: List[SwarmAgent] = []

    async def _cast_agents(self, topic: str, count: int = 5) -> List[SwarmAgent]:
        prompt = f"I have a topic: '{topic}'. Give me a JSON array of {count} distinct personas/experts who should debate this topic. Each item should have a 'name' and a 'persona_description'. Provide raw JSON array only."
        messages = [{"role": "user", "content": prompt}]
        
        response = litellm.completion(model=self.model, messages=messages, temperature=0.7)
        raw_content = response.choices[0].message.content
        
        try:
            # Basic parsing cleanup
            if raw_content.startswith("```json"):
                raw_content = raw_content.split("```json")[1].split("```")[0].strip()
            elif raw_content.startswith("```"):
                raw_content = raw_content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(raw_content)
            for item in data:
                self.agents.append(SwarmAgent(name=item['name'], persona=item['persona_description'], model=self.model))
        except Exception as e:
            # Fallback identities
            self.agents = [
                SwarmAgent("The Optimist", "Sees only the positive potential.", self.model),
                SwarmAgent("The Critic", "Sees only the flaws and risks.", self.model),
                SwarmAgent("The Pragmatist", "Focuses on realistic execution and next steps.", self.model)
            ]
        return self.agents


    async def debate(self, topic: str) -> Dict[str, str]:
        if not self.agents:
            await self._cast_agents(topic)
        
        tasks = []
        for agent in self.agents:
            tasks.append(agent.generate_thought(f"Analyze this topic from your unique perspective: {topic}"))
        
        results = await asyncio.gather(*tasks)
        
        debate_log = {}
        for agent, thought in zip(self.agents, results):
            debate_log[agent.name] = thought
            
        return debate_log

    async def synthesize(self, topic: str, debate_log: Dict[str, str]) -> str:
        context = "\n".join([f"[{name}]: {thought}" for name, thought in debate_log.items()])
        prompt = f"Topic: {topic}\n\nHere are opinions from different experts:\n{context}\n\nAct as the Master Synthesizer. Read all perspectives, weigh the pros and cons, and provide a final, actionable verdict."
        
        messages = [{"role": "user", "content": prompt}]
        response = await litellm.acompletion(model=self.model, messages=messages)
        return response.choices[0].message.content
