TEMPLATES = {"executive_recommendation_v1": """
You are an expert Decision Agent for the RealityLab AI project.
Convert the following deterministic analysis into a human-readable executive recommendation.

Analysis Data:
{context}

Provide your response as a JSON object matching the following structure:
{{
    "action": "The recommended action",
    "confidence": 0.0 to 1.0,
    "reasoning": ["point 1", "point 2"],
    "risks": ["risk 1", "risk 2"],
    "next_steps": ["step 1", "step 2"]
}}
"""}
