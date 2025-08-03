#Denvil


import re
import json
import logging
from typing import List, Dict, Tuple

class AdvancedReasoningEngine:
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.reasoning_patterns = {
            'mathematical': r'(\d+[\+\-\*\/\(\)\s]+\d+)|(\bsolve\b|\bcalculate\b)',
            'logical': r'(\bif\b.*\bthen\b)|(\bbecause\b)|(\btherefore\b)|(\bconclusion\b)',
            'analytical': r'(\banalyze\b)|(\bcompare\b)|(\bevaluate\b)|(\bassess\b)',
            'creative': r'(\bcreate\b)|(\bdesign\b)|(\bimagine\b)|(\binvent\b)'
        }
    
    async def process_with_reasoning(self, query: str, context: Dict) -> Dict:
        """Process query with advanced reasoning capabilities"""
        
        # Step 1: Analyze query type
        reasoning_type = self._identify_reasoning_type(query)
        
        # Step 2: Decompose complex problems
        if self._is_complex_query(query):
            return await self._solve_step_by_step(query, context, reasoning_type)
        else:
            return await self._direct_response(query, context, reasoning_type)
    
    def _identify_reasoning_type(self, query: str) -> str:
        """Identify the type of reasoning required"""
        query_lower = query.lower()
        
        for reasoning_type, pattern in self.reasoning_patterns.items():
            if re.search(pattern, query_lower):
                return reasoning_type
        
        return 'general'
    
    def _is_complex_query(self, query: str) -> bool:
        """Determine if query requires step-by-step reasoning"""
        complexity_indicators = [
            'step by step', 'explain how', 'break down', 'analyze',
            'multiple', 'various', 'different aspects', 'comprehensive'
        ]
        
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in complexity_indicators) or len(query.split()) > 50
    
    async def _solve_step_by_step(self, query: str, context: Dict, reasoning_type: str) -> Dict:
        """Solve complex queries using step-by-step reasoning"""
        
        # Step 1: Decompose the problem
        decomposition_prompt = f"""
        Break down this complex query into logical steps:
        Query: {query}
        
        Provide a numbered list of steps needed to fully address this query.
        Each step should be specific and actionable.
        """
        
        decomposition = await self.model_manager.generate_response(
            decomposition_prompt, 
            context, 
            {'urgent': False}
        )
        
        steps = self._extract_steps(decomposition['content'])
        
        # Step 2: Solve each step
        step_solutions = []
        accumulated_context = context.copy()
        
        for i, step in enumerate(steps):
            step_prompt = f"""
            Previous context: {json.dumps(accumulated_context, indent=2)}
            
            Current step to solve: {step}
            
            Provide a detailed solution for this specific step.
            """
            
            step_solution = await self.model_manager.generate_response(
                step_prompt,
                accumulated_context,
                {'urgent': False}
            )
            
            step_solutions.append({
                'step': i + 1,
                'question': step,
                'solution': step_solution['content']
            })
            
            # Update context with solution
            accumulated_context[f'step_{i+1}_solution'] = step_solution['content']
        
        # Step 3: Synthesize final response
        synthesis_prompt = f"""
        Original query: {query}
        
        Step-by-step solutions:
        {json.dumps(step_solutions, indent=2)}
        
        Provide a comprehensive final answer that synthesizes all the step solutions
        into a coherent response to the original query.
        """
        
        final_response = await self.model_manager.generate_response(
            synthesis_prompt,
            accumulated_context,
            {'urgent': False}
        )
        
        return {
            'response': final_response['content'],
            'reasoning_steps': step_solutions,
            'reasoning_type': reasoning_type,
            'total_tokens': sum([decomposition.get('tokens_used', 0), final_response.get('tokens_used', 0)]),
            'total_cost': sum([decomposition.get('cost', 0), final_response.get('cost', 0)])
        }
    
    async def _direct_response(self, query: str, context: Dict, reasoning_type: str) -> Dict:
        """Handle simple queries with direct response"""
        
        enhanced_prompt = f"""
        Query type identified: {reasoning_type}
        
        User query: {query}
        
        Provide a thoughtful response appropriate for this type of query.
        """
        
        response = await self.model_manager.generate_response(
            enhanced_prompt,
            context,
            {'urgent': True}
        )
        
        return {
            'response': response['content'],
            'reasoning_type': reasoning_type,
            'tokens_used': response['tokens_used'],
            'cost': response['cost']
        }
    
    def _extract_steps(self, decomposition_text: str) -> List[str]:
        """Extract numbered steps from decomposition response"""
        steps = []
        lines = decomposition_text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Match numbered steps (1., 2., 1), 2), etc.)
            if re.match(r'^\d+[\.\)]\s+', line):
                step = re.sub(r'^\d+[\.\)]\s+', '', line)
                if step:
                    steps.append(step)
        
        return steps if steps else [decomposition_text]
