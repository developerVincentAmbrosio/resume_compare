import re
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

from models import GraphState, ResumeFeedback
from parsers import resume_text_extraction

model = ChatOpenAI(model="gpt-4o", 
                   temperature=0).with_structured_output(ResumeFeedback)

def cleaned_raw_text(text: str) -> str:

    srtips_ascii_pattern = r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]"
    strips_bullets_pattern = r"[•●■▪○◦➔➢✓✔❖▢\-‐‑‒–—―]+"
    strips_tabs_pattern = r"[ \t]+"
    reduces_line_break_pattern = r"\n{2,}"

    if not text:
        return""

    text = re.sub(srtips_ascii_pattern, "", text)
    text = re.sub(strips_bullets_pattern, "-", text)
    text = re.sub(strips_tabs_pattern, " ", text)
    text = re.sub(reduces_line_break_pattern, "\n", text)

    return text.strip()

def parse_resumes_node(state: GraphState) -> Dict[str, Any]:
    """Extracts text from all raw files"""
    parsed_dict = dict(state.parsed_resumes or {})
    for file_name, file_bytes in state.resume_files.items():
        raw_text = resume_text_extraction(file_name, file_bytes)

        if "Error" in raw_text:
            parsed_dict[file_name] = raw_text
        else:
            parsed_dict[file_name] = cleaned_raw_text(raw_text)
        
    return {"parsed_resumes": parsed_dict}

def compare_resumes_node(state: GraphState) -> Dict[str, Any]:
    """Matches resume text agains Job Description using Structured LLM output."""
    evalation_results = dict(state.analysis_results)
    jd = cleaned_raw_text(state.job_description)

    for file_name, resume_text in state.parsed_resumes.items():
        if "Error" in resume_text or not resume_text.strip():
            continue

        system_prompt = (
            """
            You are an expert HR Technical Recruiter. Analyze the provided resume
            against the Job Description. Provide objective, metrics-driven feedback
            strictly adhering to the requested JSON structure.
            """
        )

        user_content = (
            f"--- JOB DESCRIPTION ---\n{jd}\n\n" 
            f"--- RESUME ({file_name}) ---\n{resume_text}"
            )

        response = model.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content)
        ])
        evalation_results[file_name] = response.model_dump()
    
    return {"analysis_results": evalation_results}

workflow = StateGraph(GraphState)
workflow.add_node("parse_resumes", parse_resumes_node)
workflow.add_node("compare_resumes", compare_resumes_node)

workflow.add_edge(START, "parse_resumes")
workflow.add_edge("parse_resumes", "compare_resumes")
workflow.add_edge("compare_resumes", END)

resume_analyzer = workflow.compile()
