import asyncio
from typing import List, Dict, Optional
import litellm
import json

litellm.drop_params = True

class SwarmAgent:
    def __init__(self, name: str, persona: str, model: str = "gpt-4o-mini", tools_enabled: bool = False):
        self.name = name
        self.persona = persona
        self.model = model
        self.tools_enabled = tools_enabled

    async def generate_thought(self, prompt: str, global_context: str = "") -> str:
        system_msg = f"You are {self.name}. Your persona is: {self.persona}. You must answer from this strict perspective. Keep your response concise, sharp, and insightful."
        messages = [
            {"role": "system", "content": system_msg},
        ]
        
        if global_context:
            messages.append({"role": "system", "content": f"Here is some background context found from the web prior to the debate:\n{global_context}"})
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await litellm.acompletion(model=self.model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"[{self.name} encountered an error: {str(e)}]"

class NanoSwarm:
    def __init__(self, model: str = "gpt-4o-mini", enable_search: bool = False):
        self.model = model
        self.agents: List[SwarmAgent] = []
        self.enable_search = enable_search
        self.global_context = ""

    async def _gather_context(self, topic: str):
        if not self.enable_search:
            return
            
        from nanoswarm.tools import web_search
        # Ask an LLM to generate a search query based on the topic
        msg = [{"role": "user", "content": f"Given the topic '{topic}', what is a good 3-5 word search query to look up the latest context on the web? Reply with ONLY the query string, nothing else."}]
        try:
            resp = await litellm.acompletion(model=self.model, messages=msg)
            query = resp.choices[0].message.content.strip().strip("'\"")
            self.global_context = web_search(query, max_results=3)
        except Exception as e:
            self.global_context = f"Failed to gather context: {str(e)}"

    async def _cast_agents(self, topic: str, count: int = 4) -> List[SwarmAgent]:
        prompt = f"I have a topic: '{topic}'. Give me a JSON array of {count} distinct personas/experts who should debate this topic. Each item should have a 'name' and a 'persona_description'. Provide raw JSON array only."
        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = await litellm.acompletion(model=self.model, messages=messages, temperature=0.7)
            raw_content = response.choices[0].message.content
            
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
                SwarmAgent("The Optimist", "Sees only the positive potential and upside.", self.model),
                SwarmAgent("The Critic", "Sees only the flaws, risks, and worst-case scenarios.", self.model),
                SwarmAgent("The Pragmatist", "Focuses on realistic execution, timelines, and next steps.", self.model),
                SwarmAgent("The Lateral Thinker", "Approaches the problem from completely unrelated angles and fields.", self.model)
            ]
        return self.agents


    async def debate(self, topic: str) -> Dict[str, str]:
        if self.enable_search and not self.global_context:
             await self._gather_context(topic)
             
        if not self.agents:
            await self._cast_agents(topic)
        
        tasks = []
        for agent in self.agents:
            tasks.append(agent.generate_thought(f"Analyze this topic from your unique perspective: {topic}", self.global_context))
        
        results = await asyncio.gather(*tasks)
        
        debate_log = {}
        for agent, thought in zip(self.agents, results):
            debate_log[agent.name] = thought
            
        return debate_log

    async def synthesize(self, topic: str, debate_log: Dict[str, str]) -> str:
        context = "\n\n".join([f"### [{name}]\n{thought}" for name, thought in debate_log.items()])
        prompt = f"Topic: {topic}\n\nHere are opinions from different experts:\n{context}\n\nAct as the Master Synthesizer. Read all perspectives, weigh the pros and cons, and provide a final, actionable verdict. Format in clear Markdown."
        
        messages = [{"role": "user", "content": prompt}]
        try:
            response = await litellm.acompletion(model=self.model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to synthesize: {str(e)}"
