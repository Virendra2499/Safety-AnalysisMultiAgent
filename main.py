from sentence_transformers import SentenceTransformer
import faiss
import google.generativeai as genai
from config import GEMINI_API_KEY
from dummy_data import safety_requirements, system_descriptions

embedder = SentenceTransformer("all-MiniLM-L6-v2")
requirement_embeddings = embedder.encode(safety_requirements)

dimension = requirement_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(requirement_embeddings)

genai.configure(api_key=GEMINI_API_KEY)
llm = genai.GenerativeModel("gemini-2.0-flash")

def retrieve_reqs(doc_text, k=2):
    query_vec = embedder.encode([doc_text])
    _, I = index.search(query_vec, k)
    return [safety_requirements[i] for i in I[0]]

def agent_analyze_compliance(requirement, doc_snippet):
    """Use Gemini to assess compliance"""
    prompt = f"""
You are a safety compliance expert.
Evaluate if the following system design satisfies the requirement.

Requirement:
{requirement}

System Description:
{doc_snippet}

Respond with:

COMPLIANT or NON-COMPLIANT

Explanation

Suggested Recommendation (if any)"""
    response = llm.generate_content(prompt)
    return response.text.strip()

def agent_generate_report(all_analyses):
    """Generate a structured compliance report using Gemini"""
    joined = "\n\n".join(all_analyses)
    prompt = f"""
You are a technical documentation expert.
Based on the following compliance evaluations, write a clear, structured safety analysis report.

Format:

Requirement

Compliance: COMPLIANT / NON-COMPLIANT

Explanation

Recommendation (if non-compliant)

Analyses:
{joined}
"""
    response = llm.generate_content(prompt)
    return response.text.strip()

def run_pipeline():
    for doc in system_descriptions:
        relevant_reqs = retrieve_reqs(doc)
        analysis_results = []
        for req in relevant_reqs:
            result = agent_analyze_compliance(req, doc)
            analysis_results.append(f"Requirement: {req}\nSystem: {doc}\nResult: {result}")
        report = agent_generate_report(analysis_results)
        print(report)
    return report

if __name__ == "__main__":
    report = run_pipeline()
    print("Compliance analysis completed.")
    print("Generated report:")
    print(report)
    print("You can now review the compliance analysis and recommendations.")