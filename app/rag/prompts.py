PLANNER_PROMPT = """You are an expert research planner. Break down the user query into a search plan.
Query: {query}
Respond ONLY with a valid JSON object matching this schema:
{{
  "query": "original query",
  "search_keywords": ["keyword1", "keyword2", "keyword3"],
  "intent": "brief explanation of what the user is looking for"
}}"""

NOVELTY_SCORER_PROMPT = """Evaluate the novelty or significance of this research abstract on a scale from 0.0 to 1.0.
Abstract: {abstract}
Respond ONLY with a float number (e.g., 0.85). Do not include any other text."""

SUMMARIZE_PAPER_PROMPT = """You are a research analyst. Provide a structured summary of this research paper.

Paper Text:
{text}

You MUST respond in this exact format:

**Abstract Overview:** <2-3 sentence overview of the paper's core contribution>

**Methodology:** <detailed description of the research methodology, tools, datasets, and experimental setup used>

**Key Findings:** <bullet points of the main results, metrics, and conclusions>

**Contributions:** <what this paper contributes to the field>
"""

COMBINED_SUMMARY_PROMPT = """Synthesize the following research abstracts into a cohesive combined summary.
For each paper, briefly note the methodology and key findings.
Then provide an overall synthesis of common themes and divergent approaches.

Abstracts:
{text}

Combined Research Synthesis:"""

RESEARCH_GAPS_PROMPT = """Based on the following research context, identify and analyze research gaps and future directions.
Ensure your response is highly structured, insightful, and formatted cleanly.

Context:
{text}

You MUST provide your analysis in this exact format:

## Critical Research Gaps

1. **<Gap title>**
   <Detailed description of the gap, why it exists, and why it matters to the field>

2. **<Gap title>**
   <Detailed description>

3. **<Gap title>**
   <Detailed description>

4. **<Gap title>**
   <Detailed description>

5. **<Gap title>**
   <Detailed description>

## Methodological Limitations
- <Limitation 1>
- <Limitation 2>
- <Limitation 3>

## Future Research Directions
- **<Direction 1>:** <Brief explanation>
- **<Direction 2>:** <Brief explanation>
- **<Direction 3>:** <Brief explanation>
- **<Direction 4>:** <Brief explanation>
"""

METHODOLOGY_EXTRACT_PROMPT = """Extract and summarize the methodology from this research paper abstract/text.
Focus on: research design, data collection methods, tools/frameworks used, evaluation metrics, and experimental setup.

Text: {text}

Methodology Summary:"""

MERMAID_WORKFLOW_PROMPT = """You are an expert at creating Mermaid JS diagrams.
Based on the following research methodology or synthesis text, generate a Mermaid Top-Down (TD) graph that strictly maps out the functional workflow, architecture, or research process.
Do NOT include any markdown code blocks, backticks, comments, or explanations.
Output ONLY the raw mermaid syntax starting with `graph TD;`.
Keep node text concise and avoid special characters in node labels.

Text: {text}

Mermaid Graph:"""
