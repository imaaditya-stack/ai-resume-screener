PROMPT = """
You are an expert recruiter with deep knowledge of technical hiring. Analyze this job description focusing solely on technical requirements:

1. Distilled Description for Semantic Matching:
Create a concise summary in 5-6 sentences of the essential technical requirements mentioned in the job description.

2. Keyword Extraction - BE VERY SELECTIVE AND FOLLOW THESE RULES:
- MANDATORY KEYWORDS: Include ONLY the core technologies without which a candidate would be automatically disqualified. For a React Developer, this might only include "React" and "JavaScript".
- OPTIONAL KEYWORDS: All other technical skills mentioned, grouped into relevant categories, with weights from 1-10.

IMPORTANT RULES FOR KEYWORD EXTRACTION:
1. List each technology as a separate item (e.g., "Jest", "Mocha", and "Jasmine" as three separate entries, not "Jest/Mocha/Jasmine" or "unit testing libraries")
2. Include only specific technologies and tools, not general phrases like "keeping up with ecosystem changes"
3. Break apart bundled technologies (e.g., instead of "Node.js (Relay+GraphQL)", list as separate items: "Node.js", "Relay", "GraphQL")
4. Only include concrete, specific technical skills that would appear on a resume (e.g., "React", "TypeScript", "Webpack")
5. Ensure all entries are single technologies/frameworks/languages, not descriptions or sentences

Job Description:
{JOB_DESCRIPTION}

Format your response as JSON:

{{
"distilled_description": "A concise paragraph with only essential technical requirements",
"mandatory_keywords": ["only absolute core technologies without which a candidate would be disqualified"],
"optional_keywords": [
  {{"name": "Category1", "weight": 8, "terms": ["term1", "term2", "term3"]}},
  {{"name": "Category2", "weight": 5, "terms": ["term4", "term5", "term6"]}}
],
"years_of_experience": 0.0
}}

Remember:
- Be extremely conservative with mandatory keywords
- List each technology as a separate entry
- Only include specific, concrete technologies
- Do not include full sentences or descriptions as keywords
"""
