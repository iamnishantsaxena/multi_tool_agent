from __future__ import annotations

from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field, conint

# --- Job Description Models (JD Extractor v2 Output) ---

class TechnicalSkillDetail(BaseModel):
    """Details of a specific technical skill required for a job."""
    name: str
    description: str
    requirement: Literal["Must Have", "Nice to Have", "Not Specified"]
    experienceLevelRequired: str = Field(..., description="e.g., Beginner | 3+ years | Not Specified")
    isKeySkill: bool

class NonTechnicalSkillDetail(BaseModel):
    """Details of a specific non-technical skill required for a job."""
    name: str
    description: str
    requirement: Literal["Must Have", "Nice to Have", "Not Specified"]
    experienceLevelRequired: str = Field(..., description="e.g., Proven | Not Specified")
    # isKeySkill is intentionally omitted for non-technical skills per prompt

class SkillsData(BaseModel):
    """Categorized skills required for the job."""
    Technical_Skills: List[TechnicalSkillDetail] = Field(..., alias="Technical Skills")
    Non_Technical_Skills: List[NonTechnicalSkillDetail] = Field(..., alias="Non Technical Skills")

class RequirementsData(BaseModel):
    """Formal prerequisites for the job."""
    Qualification: str = Field(..., description="e.g., Bachelor's Degree in CS | Not Specified")
    Work_Rights: str = Field(..., alias="Work Rights", description="e.g., Eligible to work in US | Not Specified")
    minYearsExperienceRequired: int = Field(..., description="e.g., 0 | 3 | 5")

class WorkFromHomeData(BaseModel):
    """Details about the work-from-home arrangement."""
    Available: Literal["YES", "NO", "Not Mentioned"]
    Days: conint(ge=0, le=5) # type: ignore

class FlexibleArrangementData(BaseModel):
    """Details about flexible work arrangements."""
    Work_From_Home: WorkFromHomeData = Field(..., alias="Work From Home")

class JobDescription(BaseModel):
    """Structured representation of an extracted Job Description."""
    jobTitle: str
    Responsibilities: List[str]
    Skills: SkillsData
    Requirements: RequirementsData
    Flexible_Arrangement: FlexibleArrangementData = Field(..., alias="Flexible Arrangement")
    Perks: List[str] = Field(default_factory=list)
    Extra_Details: Dict[str, str] = Field(default_factory=dict, alias="Extra Details", description="e.g., {'Location': '...', 'Salary Range': '...'}")


# --- Candidate Resume Models (CV Extractor v1 Output) ---

class CandidateProfileData(BaseModel):
    """Basic profile and contact information for the candidate."""
    Name: str
    Email: str
    Phone: str
    LinkedIn_URL: Optional[str] = Field(None, alias="LinkedIn URL")
    Portfolio_URL: Optional[str] = Field(None, alias="Portfolio URL")
    Location: Optional[str] = None

class WorkExperienceEntry(BaseModel):
    """Details of a single entry in the candidate's work history."""
    Job_Title: str = Field(..., alias="Job Title")
    Company: str
    Location: Optional[str] = None
    StartDate: Optional[str] = None
    EndDate: Optional[str] = None # e.g., YYYY-MM or Present
    Responsibilities: List[str] = Field(default_factory=list)

class CandidateSkillDetail(BaseModel):
    """Details of a skill identified in the candidate's resume."""
    name: str
    validated: bool = Field(..., description="True if evidence found in Work Experience or Projects")
    level: Literal["Beginner", "Intermediate", "Advanced", "Expert"]
    yearsExperience: int = Field(..., description="Approximate years of validated experience with the skill")
    evidence: List[str] = Field(default_factory=list, description="Sources of validation, e.g., 'Job: SE @ Acme'")

class CandidateSkillsData(BaseModel):
    """Categorized skills extracted from the candidate's resume."""
    Technical_Skills: List[CandidateSkillDetail] = Field(..., alias="Technical Skills")
    Non_Technical_Skills: List[CandidateSkillDetail] = Field(..., alias="Non Technical Skills")

class EducationEntry(BaseModel):
    """Details of a single entry in the candidate's education history."""
    Institution: str
    Degree: str
    Field_of_Study: str = Field(..., alias="Field of Study")
    StartDate: Optional[str] = None
    GraduationDate: Optional[str] = None
    Notes: Optional[str] = None

class ProjectEntry(BaseModel):
    """Details of a single project listed in the candidate's resume."""
    Project_Name: str = Field(..., alias="Project Name")
    Description: str
    Technologies_Used: List[str] = Field(default_factory=list, alias="Technologies Used")
    Link: Optional[str] = None
    Dates: Optional[str] = None

class CertificationEntry(BaseModel):
    """Details of a single certification or license listed."""
    Name: str
    Issuing_Body: Optional[str] = Field(None, alias="Issuing Body")
    Date_Earned: Optional[str] = Field(None, alias="Date Earned")
    Credential_ID: Optional[str] = Field(None, alias="Credential ID")

class PreferencesData(BaseModel):
    """Candidate's stated preferences and work authorization status."""
    Preferred_Locations: List[str] = Field(default_factory=list, alias="Preferred Locations")
    Remote_Work_Preference: Literal["Open to Remote", "Prefers Remote", "Prefers On-site", "Prefers Hybrid", "Not Mentioned"] = Field(..., alias="Remote Work Preference")
    Work_Authorization: Optional[str] = Field(None, alias="Work Authorization")

class LanguageEntry(BaseModel):
    """Details of a language spoken by the candidate."""
    Language: str
    Proficiency: Optional[str] = None

class CandidateResume(BaseModel):
    """Structured representation of an extracted Candidate Resume."""
    Candidate_Profile: CandidateProfileData = Field(..., alias="Candidate Profile")
    Summary: str
    Work_Experience: List[WorkExperienceEntry] = Field(..., alias="Work Experience")
    Skills: CandidateSkillsData
    Education: List[EducationEntry] = Field(default_factory=list)
    Projects: List[ProjectEntry] = Field(default_factory=list)
    Certifications_Licenses: List[CertificationEntry] = Field(default_factory=list, alias="Certifications & Licenses")
    Preferences_Authorizations: PreferencesData = Field(..., alias="Preferences & Authorizations")
    Languages: List[LanguageEntry] = Field(default_factory=list)


# --- Match Result Models (Matcher Engine v1 Output) ---

class MatchScoreBreakdownData(BaseModel):
    """Quantitative breakdown of match scores across categories."""
    skillsMatchRating: Literal["Excellent", "Good", "Fair", "Poor"]
    experienceMatchRating: Literal["Excellent", "Good", "Fair", "Poor"]
    qualificationsMatchRating: Literal["Meets", "Exceeds", "Partially Meets", "Does Not Meet", "Not Specified"]
    locationPreferenceMatchRating: Literal["Exact Match", "Compatible", "Potentially Compatible", "Mismatch", "Not Enough Info"]
    workRightsMatchRating: Literal["Confirmed Match", "Likely Match", "Sponsorship May Be Required", "Mismatch", "Cannot Determine", "Not Specified"]

class MatchSummaryData(BaseModel):
    """High-level summary of the JD-CV match."""
    overallRating: Literal["Excellent Match", "Good Match", "Fair Match", "Poor Match", "Mismatch"]
    keyStrengths: List[str] = Field(default_factory=list)
    keyWeaknesses: List[str] = Field(default_factory=list)
    matchScoreBreakdown: MatchScoreBreakdownData

class MatchedSkillDetail(BaseModel):
    """Details of how a specific JD skill requirement was met (or not) by the CV."""
    jdSkillName: str
    cvSkillName: str # Can be same as jdSkillName or a related skill
    matchType: Literal["Exact", "Related"]
    cvSkillLevel: str # Derived from CandidateSkillDetail.level
    cvYearsExperience: int
    cvValidated: bool
    matchStrength: Literal[
        "Strong Match (Validated)",
        "Moderate Match (Validated Related)",
        "Fair Match (Not Validated)",
        "Weak Match (Not Validated Related)",
        "Bonus (Validated)",
        "Minor Bonus (Not Validated)"
    ]

class CandidateSkillInfo(BaseModel):
    """Basic info about a candidate skill, often used for skills not required by JD."""
    cvSkillName: str
    cvSkillLevel: str # Derived from CandidateSkillDetail.level
    cvYearsExperience: int
    cvValidated: bool

class SkillCategoryAnalysisData(BaseModel):
    """Detailed analysis for a category of skills (Technical/Non-Technical)."""
    requiredMet: List[MatchedSkillDetail] = Field(default_factory=list)
    requiredMissing: List[str] = Field(default_factory=list)
    niceToHaveMet: List[MatchedSkillDetail] = Field(default_factory=list)
    niceToHaveMissing: List[str] = Field(default_factory=list)
    candidateSkillsNotRequired: List[CandidateSkillInfo] = Field(default_factory=list)

class SkillsAnalysisData(BaseModel):
    """Complete skills analysis comparing JD requirements to CV skills."""
    technicalSkills: SkillCategoryAnalysisData
    nonTechnicalSkills: SkillCategoryAnalysisData
    overallSkillComment: str

class RelevantRole(BaseModel):
    """Summary of a CV work experience role deemed relevant to the JD."""
    jobTitle: str
    company: str
    durationYears: float

class ExperienceAnalysisData(BaseModel):
    """Analysis of the candidate's experience against JD requirements."""
    jdMinYearsRequired: int
    cvTotalYearsExperience: float
    matchStatus: Literal["Exceeds", "Meets", "Below", "Significantly Below"]
    relevantRoles: List[RelevantRole] = Field(default_factory=list)
    comment: str

class CvEducationSummary(BaseModel):
    """Simplified education details used in the match summary."""
    degree: str
    fieldOfStudy: str
    institution: str

class QualificationAnalysisData(BaseModel):
    """Analysis of the candidate's educational qualifications against JD requirements."""
    jdQualification: str
    cvEducation: List[CvEducationSummary] = Field(default_factory=list)
    matchStatus: Literal["Meets", "Exceeds", "Partially Meets (Related Field/Equivalent Experience)", "Does Not Meet", "Not Specified"]
    comment: str

class JdRemotePolicy(BaseModel):
    """JD's remote work policy extracted for comparison."""
    available: Literal["YES", "NO", "Not Mentioned"]
    days: int

class LocationPreferenceAnalysisData(BaseModel):
    """Analysis of location and remote work preference compatibility."""
    jdLocation: Optional[str] = None
    jdRemotePolicy: JdRemotePolicy
    cvLocation: Optional[str] = None
    cvPreferredLocations: List[str] = Field(default_factory=list)
    cvRemotePreference: str # Literal from PreferencesData.Remote_Work_Preference
    compatibility: Literal["Exact Match", "Compatible", "Potentially Compatible (Relocation Required)", "Mismatch", "Not Enough Info"]
    comment: str

class WorkAuthorizationAnalysisData(BaseModel):
    """Analysis of work authorization compatibility."""
    jdRequirement: Optional[str] = None
    cvStatus: Optional[str] = None
    matchStatus: Literal["Confirmed Match", "Likely Match", "Sponsorship May Be Required", "Mismatch", "Cannot Determine", "Not Specified"]
    comment: str

class ResponsibilityOverlapData(BaseModel):
    """Analysis of keyword overlap between JD responsibilities and CV experience."""
    keywordsFound: List[str] = Field(default_factory=list)
    comment: str

class DetailedComparisonData(BaseModel):
    """Container for all detailed comparison analyses."""
    skillsAnalysis: SkillsAnalysisData
    experienceAnalysis: ExperienceAnalysisData
    qualificationAnalysis: QualificationAnalysisData
    locationAndPreferenceAnalysis: LocationPreferenceAnalysisData
    workAuthorizationAnalysis: WorkAuthorizationAnalysisData
    responsibilityKeywordOverlap: ResponsibilityOverlapData

class MatchResult(BaseModel):
    """The complete structured output of the JD-CV matching process."""
    matchSummary: MatchSummaryData
    detailedComparison: DetailedComparisonData

# Example Usage (Illustrative)
if __name__ == "__main__":
    # --- Example JD Data (Simplified) ---
    jd_data = {
        "jobTitle": "Senior Software Engineer",
        "Responsibilities": ["Develop features", "Mentor juniors"],
        "Skills": {
            "Technical Skills": [
                {"name": "Python", "description": "Backend dev", "requirement": "Must Have", "experienceLevelRequired": "5+ years", "isKeySkill": True},
                {"name": "AWS", "description": "Cloud services", "requirement": "Must Have", "experienceLevelRequired": "3+ years", "isKeySkill": True},
                {"name": "React", "description": "Frontend framework", "requirement": "Nice to Have", "experienceLevelRequired": "2+ years", "isKeySkill": False}
            ],
            "Non Technical Skills": [
                {"name": "Communication", "description": "Team collaboration", "requirement": "Must Have", "experienceLevelRequired": "Not Specified"},
            ]
        },
        "Requirements": {"Qualification": "Bachelor's in CS", "Work Rights": "Eligible to work in US", "minYearsExperienceRequired": 5},
        "Flexible Arrangement": {"Work From Home": {"Available": "YES", "Days": 3}},
        "Perks": ["Great culture", "Free snacks"],
        "Extra Details": {"Location": "New York, NY"}
    }
    jd_model = JobDescription(**jd_data)
    # print(jd_model.json(indent=2))

    # --- Example CV Data (Simplified) ---
    cv_data = {
        "Candidate Profile": {"Name": "Jane Doe", "Email": "jane@example.com", "Phone": "123-456-7890", "Location": "New York, NY"},
        "Summary": "Experienced engineer...",
        "Work Experience": [
            {"Job Title": "Software Engineer", "Company": "Tech Corp", "Location": "New York, NY", "StartDate": "2018-01", "EndDate": "Present", "Responsibilities": ["Developed Python services", "Used AWS daily"]}
        ],
        "Skills": {
            "Technical Skills": [
                {"name": "Python", "validated": True, "level": "Advanced", "yearsExperience": 6, "evidence": ["Job: Software Engineer @ Tech Corp"]},
                {"name": "AWS", "validated": True, "level": "Intermediate", "yearsExperience": 4, "evidence": ["Job: Software Engineer @ Tech Corp"]},
                {"name": "Docker", "validated": False, "level": "Beginner", "yearsExperience": 0, "evidence": []}
            ],
            "Non Technical Skills": [
                {"name": "Communication", "validated": True, "level": "Advanced", "yearsExperience": 6, "evidence": ["Job: Software Engineer @ Tech Corp"]}
            ]
        },
        "Education": [{"Institution": "State University", "Degree": "Bachelor of Science", "Field of Study": "Computer Science", "GraduationDate": "2017"}],
        "Projects": [],
        "Certifications & Licenses": [],
        "Preferences & Authorizations": {"Preferred Locations": ["New York, NY"], "Remote Work Preference": "Open to Remote", "Work Authorization": "US Citizen"},
        "Languages": [{"Language": "English", "Proficiency": "Native"}]
    }
    cv_model = CandidateResume(**cv_data)
    # print(cv_model.json(indent=2, by_alias=True)) # Use by_alias=True if using Field aliases

    # --- Example Match Result Data (Conceptual - Normally output by Matcher) ---
    match_data = {
        "matchSummary": {
            "overallRating": "Good Match",
            "keyStrengths": ["Strong Python match (Validated, 6 yrs)", "Meets AWS requirement (Validated, 4 yrs)", "Exceeds min experience", "Perfect location match"],
            "keyWeaknesses": ["Missing preferred React skill"],
            "matchScoreBreakdown": {
                "skillsMatchRating": "Good",
                "experienceMatchRating": "Excellent",
                "qualificationsMatchRating": "Meets",
                "locationPreferenceMatchRating": "Exact Match",
                "workRightsMatchRating": "Confirmed Match"
            }
        },
        "detailedComparison": {
             # ... (Extensive details mirroring the structure) ...
             # (Fill this based on a real match result)
             "skillsAnalysis": {
                "technicalSkills": {
                    "requiredMet": [
                        {"jdSkillName": "Python", "cvSkillName": "Python", "matchType": "Exact", "cvSkillLevel": "Advanced", "cvYearsExperience": 6, "cvValidated": True, "matchStrength": "Strong Match (Validated)"},
                        {"jdSkillName": "AWS", "cvSkillName": "AWS", "matchType": "Exact", "cvSkillLevel": "Intermediate", "cvYearsExperience": 4, "cvValidated": True, "matchStrength": "Strong Match (Validated)"}
                    ],
                    "requiredMissing": [],
                    "niceToHaveMet": [],
                    "niceToHaveMissing": ["React"],
                    "candidateSkillsNotRequired": [{"cvSkillName": "Docker", "cvSkillLevel": "Beginner", "cvYearsExperience": 0, "cvValidated": False}]
                 },
                 "nonTechnicalSkills": {
                     "requiredMet": [{"jdSkillName": "Communication", "cvSkillName": "Communication", "matchType": "Exact", "cvSkillLevel": "Advanced", "cvYearsExperience": 6, "cvValidated": True, "matchStrength": "Strong Match (Validated)"}],
                     "requiredMissing": [], "niceToHaveMet": [], "niceToHaveMissing": [], "candidateSkillsNotRequired": []
                 },
                 "overallSkillComment": "Candidate strongly matches required technical skills Python and AWS with validated experience. Missing preferred skill React."
             },
             "experienceAnalysis": {"jdMinYearsRequired": 5, "cvTotalYearsExperience": 6.5, "matchStatus": "Exceeds", "relevantRoles": [{"jobTitle": "Software Engineer", "company": "Tech Corp", "durationYears": 6.5}], "comment": "Candidate exceeds the minimum years of experience with relevant roles."},
             "qualificationAnalysis": {"jdQualification": "Bachelor's in CS", "cvEducation": [{"degree": "Bachelor of Science", "fieldOfStudy": "Computer Science", "institution": "State University"}], "matchStatus": "Meets", "comment": "Candidate meets the educational requirement."},
             "locationAndPreferenceAnalysis": {"jdLocation": "New York, NY", "jdRemotePolicy": {"available": "YES", "days": 3}, "cvLocation": "New York, NY", "cvPreferredLocations": ["New York, NY"], "cvRemotePreference": "Open to Remote", "compatibility": "Exact Match", "comment": "Perfect location match and candidate is open to remote/hybrid."},
             "workAuthorizationAnalysis": {"jdRequirement": "Eligible to work in US", "cvStatus": "US Citizen", "matchStatus": "Confirmed Match", "comment": "Candidate meets work authorization requirement."},
             "responsibilityKeywordOverlap": {"keywordsFound": ["Develop", "Python", "AWS"], "comment": "Keywords show good overlap with JD responsibilities."}
        }
    }
    match_model = MatchResult(**match_data)
    # print(match_model.json(indent=2))

    print("Pydantic models defined successfully.")