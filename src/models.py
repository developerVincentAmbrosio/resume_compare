from typing import Dict, List, Any
from pydantic import BaseModel, Field

#CHECK THE PROMPTS

class GraphState(BaseModel):
    job_description: str
    resume_files: Dict[str, bytes]
    parsed_resumes: Dict[str, str] = Field(default_factory=dict)
    analysis_results: Dict[str, Any] = Field(default_factory=dict)

class ResumeFeedback(BaseModel):
    match_percentage: int = Field(
        description="Overall alignment score from 0 to 100"
        )
    matched_skills: List[str] = Field(
        description="Skills that match the job description"
        )
    missing_skills: List[str] = Field(
        description="Crucial skills mentioned in Job Description but missing from resume"
        )
    strengths: List[str] = Field(
        description="Key highlights where the candidate excels"
        )
    improvements: List[str] = Field(
        description="Actionable advice to better align resume"
        )
