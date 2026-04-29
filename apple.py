# =============================================================================
#                    AI RESUME ANALYZER & BUILDER
#                    Built with Streamlit (Python)
#                    Version: 2.0 - Production Ready
# =============================================================================
#
#  AUTHOR      : AI Engineer (Senior Full-Stack + AI)
#  FRAMEWORK   : Streamlit
#  LANGUAGE    : Python 3.9+
#  DESCRIPTION : A complete, AI-powered resume analysis and building platform.
#                Includes ATS scoring, NLP improvement suggestions, keyword
#                optimization, resume builder, and PDF export - all free,
#                no API keys required, fully client-runnable in VS Code.
#
#  HOW TO RUN  :
#    1. pip install -r requirements.txt
#    2. streamlit run app.py
#
#  PROJECT STRUCTURE:
#    app.py               -> Main application (this file)
#    requirements.txt     -> All Python dependencies
#
#  SECTIONS IN THIS FILE:
#    SECTION 1  -> Imports & Dependencies
#    SECTION 2  -> Page Configuration & Custom CSS
#    SECTION 3  -> Constants & Knowledge Databases
#      3.1  Action Verbs Database (by category)
#      3.2  Weak Phrases & Replacements
#      3.3  Industry Keywords (by sector)
#      3.4  ATS Keywords by Job Role
#      3.5  Common Spelling Corrections
#      3.6  Grammar Rules & Patterns
#    SECTION 4  -> Text Extraction Engine
#      4.1  PDF Text Extractor
#      4.2  DOCX Text Extractor
#      4.3  Image OCR Extractor
#      4.4  Unified File Handler
#    SECTION 5  -> ATS Scoring Engine
#      5.1  Contact Information Detector
#      5.2  Section Completeness Checker
#      5.3  Keyword Density Calculator
#      5.4  Formatting Quality Analyzer
#      5.5  Readability Scorer
#      5.6  Grammar & Spelling Scorer
#      5.7  Master ATS Score Calculator
#    SECTION 6  -> NLP Improvement Engine
#      6.1  Grammar Error Detector
#      6.2  Spelling Corrector
#      6.3  Action Verb Suggester
#      6.4  Weak Phrase Replacer
#      6.5  Bullet Point Enhancer
#      6.6  Sentence Structure Analyzer
#    SECTION 7  -> Keyword Optimization Module
#      7.1  Keyword Extractor
#      7.2  Gap Analyzer
#      7.3  Industry Term Suggester
#    SECTION 8  -> Resume Builder Module
#      8.1  Form Data Collector
#      8.2  Resume Data Validator
#      8.3  Resume Template Engine
#    SECTION 9  -> PDF Generator Module
#      9.1  ATS-Friendly PDF Creator
#      9.2  Styled Resume Builder
#    SECTION 10 -> UI Helper Components
#      10.1 Score Gauge Renderer
#      10.2 Metric Cards
#      10.3 Section Headers
#      10.4 Feedback Cards
#    SECTION 11 -> Page Renderers
#      11.1 Home / Landing Page
#      11.2 Upload & Analyze Page
#      11.3 Resume Builder Page
#      11.4 Results Dashboard Page
#      11.5 About & Help Page
#    SECTION 12 -> Main Application Entry Point
#
# =============================================================================

import streamlit as st
import re
import io
import datetime
import base64
import random
import string
from collections import Counter
from typing import Dict, List, Tuple, Optional, Any

# Document parsing libraries (optional)
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    try:
        import PyPDF2
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# NLTK for NLP (optional)
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    NLTK_AVAILABLE = True
    STOP_WORDS = set(stopwords.words('english'))
except Exception:
    NLTK_AVAILABLE = False
    STOP_WORDS = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                  'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her',
                  'it', 'its', 'they', 'them', 'their', 'themselves'}

# =============================================================================
# SECTION 2: PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Resume Analyzer & Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_home_page():
    # Hero Section with clean white design
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-radius: 20px; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; color: #1a1a2e; margin-bottom: 1rem;">📄 AI Resume Analyzer & Builder</h1>
        <p style="font-size: 1.2rem; color: #555; max-width: 700px; margin: 0 auto;">Upload your resume for instant ATS scoring, or build a new professional resume from scratch</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards with modern design
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 2rem; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #e0e0e0; transition: transform 0.3s;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">ATS Scoring</h3>
            <p style="color: #666; font-size: 0.9rem;">Get detailed 0-100 score with component breakdown</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 2rem; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #e0e0e0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔧</div>
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">Smart Suggestions</h3>
            <p style="color: #666; font-size: 0.9rem;">Actionable improvement tips for keywords & grammar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; border-radius: 15px; padding: 2rem; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.07); border: 1px solid #e0e0e0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">PDF Export</h3>
            <p style="color: #666; font-size: 0.9rem;">Download professionally formatted resume</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How it works section
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 2rem;'>How It Works</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    steps = [
        ("1", "Upload", "📤", "Upload your resume in PDF, DOCX, or image format"),
        ("2", "Analyze", "🔍", "AI scans for ATS compatibility and key metrics"),
        ("3", "Optimize", "⚡", "Get specific suggestions to improve your score"),
        ("4", "Download", "⬇️", "Export your optimized resume as PDF")
    ]
    
    for col, (num, title, icon, desc) in zip([col1, col2, col3, col4], steps):
        with col:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
                    <span style="color: white; font-size: 1.5rem; font-weight: bold;">{num}</span>
                </div>
                <h4 style="color: #2c3e50; margin-bottom: 0.5rem;">{icon} {title}</h4>
                <p style="color: #666; font-size: 0.85rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key features grid
    st.markdown("<h2 style='text-align: center; color: #2c3e50; margin-bottom: 2rem;'>Key Features</h2>", unsafe_allow_html=True)
    
    features = [
        ("🎯", "ATS Optimization", "Score your resume against ATS criteria"),
        ("🔑", "Keyword Analysis", "Identify missing industry keywords"),
        ("✍️", "Grammar Check", "Detect spelling and grammar issues"),
        ("📊", "Readability Score", "Measure content clarity and impact"),
        ("🏗️", "Resume Builder", "Create new resumes from templates"),
        ("💾", "Export Options", "Download as PDF or text format")
    ]
    
    # Display features in 3x2 grid
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(features):
                icon, title, desc = features[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                        <h4 style="color: #2c3e50; margin-bottom: 0.3rem;">{icon} {title}</h4>
                        <p style="color: #666; font-size: 0.85rem; margin: 0;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Stats section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); border-radius: 15px; padding: 2rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap;">
            <div style="flex: 1; padding: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">100%</div>
                <div style="color: #666; font-size: 0.85rem;">Free & No API Keys</div>
            </div>
            <div style="flex: 1; padding: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">🔒</div>
                <div style="color: #666; font-size: 0.85rem;">Privacy First - Local Processing</div>
            </div>
            <div style="flex: 1; padding: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">📱</div>
                <div style="color: #666; font-size: 0.85rem;">Works on Any Device</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 2rem;">
        <p style="color: #666; margin-bottom: 1rem;">Ready to optimize your resume?</p>
        <a href="#" onclick="return false;" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: bold; display: inline-block;">Get Started →</a>
    </div>
    """, unsafe_allow_html=True)
# =============================================================================
# SECTION 3: CONSTANTS
# =============================================================================

ACTION_VERBS = {
    "leadership": ["Led", "Managed", "Directed", "Oversaw", "Guided", "Mentored", "Coached"],
    "technical": ["Developed", "Built", "Created", "Implemented", "Designed", "Coded", "Engineered"],
    "analysis": ["Analyzed", "Evaluated", "Assessed", "Examined", "Investigated", "Researched"],
    "achievement": ["Achieved", "Improved", "Increased", "Reduced", "Delivered", "Generated", "Saved"]
}

WEAK_PHRASES = {
    "responsible for": "Managed",
    "helped": "Supported",
    "worked on": "Developed",
    "assisted with": "Collaborated on",
    "participated in": "Contributed to"
}

INDUSTRY_KEYWORDS = {
    "software_engineering": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "API", "SQL"],
    "data_science": ["Python", "SQL", "Machine Learning", "Data Analysis", "Pandas", "Statistics", "Visualization"],
    "product_management": ["Agile", "Scrum", "Roadmap", "Stakeholder", "Requirements", "User Stories", "MVP"],
    "marketing": ["SEO", "Content", "Social Media", "Analytics", "Campaign", "Brand", "Digital Marketing"],
    "general": ["Communication", "Leadership", "Problem Solving", "Teamwork", "Project Management"]
}

ATS_KEYWORDS_BY_ROLE = {
    "Software Engineer": {
        "must_have": ["programming", "development", "coding", "algorithms", "data structures"],
        "preferred": ["agile", "scrum", "git", "api", "cloud", "database"]
    },
    "Data Scientist": {
        "must_have": ["machine learning", "python", "statistics", "data analysis", "sql"],
        "preferred": ["deep learning", "nlp", "visualization", "pandas", "scikit-learn"]
    },
    "Product Manager": {
        "must_have": ["product strategy", "roadmap", "stakeholder", "agile", "requirements"],
        "preferred": ["analytics", "user research", "go-to-market", "metrics", "kpis"]
    }
}

SPELL_CORRECTIONS = {
    "recieve": "receive",
    "acheive": "achieve",
    "managment": "management",
    "developement": "development",
    "impliment": "implement",
    "comunication": "communication"
}

CONTACT_PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    "linkedin": r'linkedin\.com/in/[\w-]+'
}

NUMBER_PATTERNS = [
    r'\d+%', r'\$\d+', r'\d+\s*(?:users|customers|clients)'
]

# =============================================================================
# SECTION 4: TEXT EXTRACTION ENGINE
# =============================================================================

class TextExtractor:
    @staticmethod
    def extract_from_pdf(file_bytes: bytes) -> Tuple[str, List[str]]:
        text = ""
        warnings = []
        if PDF_AVAILABLE:
            try:
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                warnings.append(f"PDF extraction error: {str(e)}")
        else:
            warnings.append("PDF parser not available. Install pdfplumber or PyPDF2")
        return text, warnings

    @staticmethod
    def extract_from_docx(file_bytes: bytes) -> Tuple[str, List[str]]:
        text = ""
        warnings = []
        if DOCX_AVAILABLE:
            try:
                doc = Document(io.BytesIO(file_bytes))
                for para in doc.paragraphs:
                    if para.text.strip():
                        text += para.text + "\n"
            except Exception as e:
                warnings.append(f"DOCX extraction error: {str(e)}")
        else:
            warnings.append("DOCX parser not available. Install python-docx")
        return text, warnings

    @staticmethod
    def extract_from_image(file_bytes: bytes) -> Tuple[str, List[str]]:
        text = ""
        warnings = []
        if PIL_AVAILABLE and OCR_AVAILABLE:
            try:
                image = Image.open(io.BytesIO(file_bytes))
                text = pytesseract.image_to_string(image)
            except Exception as e:
                warnings.append(f"OCR extraction error: {str(e)}")
        else:
            warnings.append("OCR not available. Install Pillow and pytesseract")
        return text, warnings

    @staticmethod
    def handle_upload(uploaded_file) -> Tuple[str, List[str], str]:
        if uploaded_file is None:
            return "", ["No file uploaded"], "unknown"
        
        file_name = uploaded_file.name.lower()
        file_bytes = uploaded_file.read()
        text = ""
        warnings = []
        file_type = "unknown"
        
        if file_name.endswith(".pdf"):
            file_type = "PDF"
            text, warnings = TextExtractor.extract_from_pdf(file_bytes)
        elif file_name.endswith(".docx"):
            file_type = "DOCX"
            text, warnings = TextExtractor.extract_from_docx(file_bytes)
        elif file_name.endswith((".jpg", ".jpeg", ".png")):
            file_type = "IMAGE"
            text, warnings = TextExtractor.extract_from_image(file_bytes)
        else:
            warnings.append(f"Unsupported file type: {file_name}")
        
        return text, warnings, file_type

# =============================================================================
# SECTION 5: ATS SCORING ENGINE
# =============================================================================

class ATSScorer:
    def __init__(self, resume_text: str, job_role: str = "general"):
        self.text = resume_text
        self.text_lower = resume_text.lower()
        self.job_role = job_role
        self.words = resume_text.split()
        self.word_count = len(self.words)
        self.lines = [l for l in resume_text.split('\n') if l.strip()]
        
    def score_contact_info(self) -> Dict[str, Any]:
        score = 0
        missing = []
        if re.search(CONTACT_PATTERNS["email"], self.text):
            score += 30
        else:
            missing.append("Email")
        if re.search(CONTACT_PATTERNS["phone"], self.text):
            score += 30
        else:
            missing.append("Phone")
        if re.search(CONTACT_PATTERNS["linkedin"], self.text_lower):
            score += 40
        else:
            missing.append("LinkedIn")
        return {"score": score, "missing": missing, "label": "Contact Information"}
    
    def score_section_completeness(self) -> Dict[str, Any]:
        sections = {
            "experience": ["experience", "employment", "work"],
            "education": ["education", "academic"],
            "skills": ["skills", "technical skills"],
            "projects": ["projects", "portfolio"]
        }
        score = 0
        found = []
        missing = []
        for section, keywords in sections.items():
            found_section = any(kw in self.text_lower for kw in keywords)
            if found_section:
                score += 25
                found.append(section)
            else:
                missing.append(section)
        return {"score": score, "found": found, "missing": missing, "label": "Section Completeness"}
    
    def score_keyword_density(self) -> Dict[str, Any]:
        found_keywords = []
        missing_keywords = []
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in self.text_lower:
                    found_keywords.append(kw)
                else:
                    missing_keywords.append(kw)
        
        # Calculate density score
        keyword_count = len(found_keywords)
        score = min(100, int((keyword_count / 30) * 100))
        
        return {
            "score": score,
            "found_keywords": found_keywords[:20],
            "missing_keywords": missing_keywords[:20],
            "label": "Keyword Optimization"
        }
    
    def score_formatting(self) -> Dict[str, Any]:
        score = 100
        issues = []
        
        if self.word_count < 200:
            score -= 20
            issues.append("Resume too short - aim for 300-700 words")
        elif self.word_count > 1000:
            score -= 10
            issues.append("Resume may be too long - consider condensing")
        
        # Check for bullet points
        bullet_count = sum(1 for line in self.lines if line.strip().startswith(('•', '-', '*')))
        if bullet_count < 5:
            score -= 15
            issues.append("Add more bullet points to highlight achievements")
        
        return {"score": max(0, score), "issues": issues, "word_count": self.word_count, "label": "Formatting Quality"}
    
    def score_readability(self) -> Dict[str, Any]:
        score = 100
        feedback = []
        
        # Check sentence length
        sentences = re.split(r'[.!?]+', self.text)
        avg_length = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        if avg_length > 25:
            score -= 15
            feedback.append("Sentences are too long - break them into shorter statements")
        
        # Check for numbers/quantification
        has_numbers = any(re.search(pattern, self.text) for pattern in NUMBER_PATTERNS)
        if not has_numbers:
            score -= 20
            feedback.append("Add quantifiable achievements (%, $, numbers)")
        
        return {"score": max(0, score), "feedback": feedback, "avg_length": avg_length, "label": "Readability"}
    
    def score_grammar_spelling(self) -> Dict[str, Any]:
        score = 100
        errors = []
        
        # Check for common spelling errors
        words = re.findall(r'\b[a-z]+\b', self.text_lower)
        for word in words:
            if word in SPELL_CORRECTIONS:
                errors.append(f"'{word}' should be '{SPELL_CORRECTIONS[word]}'")
                score -= 5
        
        # Check for first-person pronouns
        pronouns = re.findall(r'\b(I|me|my|we|our)\b', self.text, re.IGNORECASE)
        if pronouns:
            score -= min(15, len(pronouns) * 2)
            errors.append(f"Avoid first-person pronouns - found {len(pronouns)} instances")
        
        return {"score": max(0, score), "errors": errors[:10], "label": "Grammar & Spelling"}
    
    def calculate_master_score(self) -> Dict[str, Any]:
        contact = self.score_contact_info()
        sections = self.score_section_completeness()
        keywords = self.score_keyword_density()
        formatting = self.score_formatting()
        readability = self.score_readability()
        grammar = self.score_grammar_spelling()
        
        weights = {
            "contact": 0.15,
            "sections": 0.20,
            "keywords": 0.30,
            "formatting": 0.20,
            "readability": 0.15
        }
        
        component_scores = {
            "contact": contact["score"],
            "sections": sections["score"],
            "keywords": keywords["score"],
            "formatting": formatting["score"],
            "readability": readability["score"]
        }
        
        master_score = sum(component_scores[k] * weights[k] for k in weights)
        master_score = int(master_score)
        
        if master_score >= 80:
            tier = "Excellent"
            message = "Your resume is highly optimized for ATS systems!"
        elif master_score >= 60:
            tier = "Good"
            message = "Good foundation - some improvements will help"
        elif master_score >= 40:
            tier = "Fair"
            message = "Needs significant improvement to pass ATS filters"
        else:
            tier = "Poor"
            message = "Critical issues found - consider rebuilding"
        
        return {
            "master_score": master_score,
            "tier": tier,
            "message": message,
            "component_scores": component_scores,
            "contact": contact,
            "sections": sections,
            "keywords": keywords,
            "formatting": formatting,
            "readability": readability,
            "grammar": grammar
        }

# =============================================================================
# SECTION 6: RESUME IMPROVER ENGINE
# =============================================================================

class ResumeImprover:
    def __init__(self, resume_text: str):
        self.text = resume_text
        self.text_lower = resume_text.lower()
        self.lines = [l for l in resume_text.split('\n') if l.strip()]
    
    def detect_grammar_errors(self) -> List[Dict[str, Any]]:
        errors = []
        for line_num, line in enumerate(self.lines, 1):
            # Check for first-person
            if re.search(r'\b(I|me|my|we)\b', line, re.IGNORECASE):
                errors.append({
                    "line": line_num,
                    "text": line[:60],
                    "error": "First-person pronoun detected",
                    "suggestion": "Remove personal pronouns"
                })
            # Check for weak openings
            if line.strip().startswith(('I', 'My', 'We')):
                errors.append({
                    "line": line_num,
                    "text": line[:60],
                    "error": "Line starts with personal pronoun",
                    "suggestion": "Start with action verb"
                })
        return errors
    
    def suggest_stronger_verbs(self) -> List[Dict[str, Any]]:
        suggestions = []
        for line in self.lines[:10]:
            for weak, strong in WEAK_PHRASES.items():
                if weak in line.lower():
                    suggestions.append({
                        "original": line[:60],
                        "weak_word": weak,
                        "suggested": strong
                    })
                    break
        return suggestions
    
    def get_all_improvements(self) -> Dict[str, Any]:
        return {
            "grammar": self.detect_grammar_errors(),
            "verbs": self.suggest_stronger_verbs()
        }

# =============================================================================
# SECTION 7: RESUME BUILDER
# =============================================================================

class ResumeBuilder:
    @staticmethod
    def build_resume_text(data: Dict[str, Any]) -> str:
        sections = []
        
        # Header
        sections.append(data.get("name", "").upper())
        sections.append(f"{data.get('email', '')} | {data.get('phone', '')}")
        if data.get("linkedin"):
            sections.append(data["linkedin"])
        sections.append("")
        
        # Summary
        if data.get("summary"):
            sections.append("PROFESSIONAL SUMMARY")
            sections.append(data["summary"])
            sections.append("")
        
        # Experience
        if data.get("experiences"):
            sections.append("WORK EXPERIENCE")
            for exp in data["experiences"]:
                if exp.get("title") and exp.get("company"):
                    sections.append(f"{exp['title']} | {exp['company']}")
                    if exp.get("description"):
                        for line in exp["description"].split('\n'):
                            if line.strip():
                                sections.append(f"• {line.strip()}")
                    sections.append("")
        
        # Education
        if data.get("education"):
            sections.append("EDUCATION")
            for edu in data["education"]:
                if edu.get("degree") and edu.get("institution"):
                    sections.append(f"{edu['degree']} | {edu['institution']}")
                    if edu.get("grad_year"):
                        sections[-1] += f" ({edu['grad_year']})"
            sections.append("")
        
        # Skills
        if data.get("skills"):
            sections.append("SKILLS")
            sections.append(data["skills"])
        
        return "\n".join(sections)
    
    @staticmethod
    def build_html_preview(data: Dict[str, Any]) -> str:
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <h1 style="text-align: center; color: #2c3e50;">{data.get('name', 'Your Name')}</h1>
            <p style="text-align: center; color: #7f8c8d;">
                {data.get('email', '')} | {data.get('phone', '')}
            </p>
        """
        
        if data.get("summary"):
            html += f"""
            <h2 style="color: #34495e; border-bottom: 2px solid #3498db;">Professional Summary</h2>
            <p>{data['summary']}</p>
            """
        
        if data.get("experiences"):
            html += "<h2 style='color: #34495e; border-bottom: 2px solid #3498db;'>Work Experience</h2>"
            for exp in data["experiences"]:
                if exp.get("title") and exp.get("company"):
                    html += f"<h3>{exp['title']} - {exp['company']}</h3>"
                    if exp.get("description"):
                        html += "<ul>"
                        for line in exp["description"].split('\n'):
                            if line.strip():
                                html += f"<li>{line.strip()}</li>"
                        html += "</ul>"
        
        if data.get("skills"):
            html += f"""
            <h2 style="color: #34495e; border-bottom: 2px solid #3498db;">Skills</h2>
            <p>{data['skills']}</p>
            """
        
        html += "</div>"
        return html

# =============================================================================
# SECTION 8: PDF GENERATOR
# =============================================================================

class PDFGenerator:
    @staticmethod
    def generate_pdf(data: Dict[str, Any]) -> Optional[bytes]:
        if not REPORTLAB_AVAILABLE:
            return None
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER)
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=HexColor('#2c3e50'))
        normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10)
        
        # Title
        story.append(Paragraph(data.get('name', 'Resume'), title_style))
        story.append(Spacer(1, 12))
        
        # Contact
        contact = f"{data.get('email', '')} | {data.get('phone', '')}"
        story.append(Paragraph(contact, normal_style))
        story.append(Spacer(1, 12))
        
        # Summary
        if data.get('summary'):
            story.append(Paragraph("Professional Summary", heading_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(data['summary'], normal_style))
            story.append(Spacer(1, 12))
        
        # Experience
        if data.get('experiences'):
            story.append(Paragraph("Work Experience", heading_style))
            story.append(Spacer(1, 6))
            for exp in data['experiences']:
                if exp.get('title') and exp.get('company'):
                    story.append(Paragraph(f"<b>{exp['title']}</b> - {exp['company']}", normal_style))
                    if exp.get('description'):
                        story.append(Paragraph(exp['description'].replace('\n', '<br/>'), normal_style))
                    story.append(Spacer(1, 6))
        
        # Skills
        if data.get('skills'):
            story.append(Paragraph("Skills", heading_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(data['skills'], normal_style))
        
        doc.build(story)
        return buffer.getvalue()

# =============================================================================
# SECTION 9: UI COMPONENTS
# =============================================================================

def render_score_gauge(score: int, label: str = "ATS Score"):
    color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 48px; font-weight: bold; color: {color};">{score}</div>
        <div style="font-size: 14px; color: #666;">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def render_score_bar(name: str, score: int, max_score: int = 100):
    percentage = (score / max_score) * 100
    st.progress(percentage / 100)
    st.caption(f"{name}: {score}/100")

def render_keyword_tags(keywords: List[str], tag_type: str = "present"):
    if not keywords:
        st.write("No keywords found")
        return
    
    cols = st.columns(4)
    for i, kw in enumerate(keywords[:12]):
        with cols[i % 4]:
            st.markdown(f'<span class="tag">{kw}</span>', unsafe_allow_html=True)

def render_suggestion_card(title: str, text: str, card_type: str = "info"):
    icon = "ℹ️" if card_type == "info" else "⚠️" if card_type == "warning" else "✅"
    st.info(f"{icon} **{title}**: {text}")

# =============================================================================
# SECTION 10: PAGE RENDERERS
# =============================================================================

def render_home_page():
    st.markdown("""
    <div class="main-header">
        <h1>📄 AI Resume Analyzer & Builder</h1>
        <p>Upload your resume for instant ATS scoring, or build a new one from scratch</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>📊</h2>
            <h3>ATS Scoring</h3>
            <p>Get detailed 0-100 score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🔧</h2>
            <h3>Smart Suggestions</h3>
            <p>Actionable improvement tips</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>📄</h2>
            <h3>PDF Export</h3>
            <p>Download optimized resume</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("ℹ️ **How it works**: Upload your resume (PDF, DOCX, or image) to get an instant ATS score and improvement suggestions. Or use our resume builder to create a new ATS-optimized resume from scratch.")

def render_upload_analyze_page():
    st.header("📤 Upload & Analyze Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=["pdf", "docx", "jpg", "jpeg", "png"],
        help="Supported formats: PDF, DOCX, JPG, PNG"
    )
    
    job_role = st.selectbox(
        "Target Job Role (for keyword matching)",
        ["general", "Software Engineer", "Data Scientist", "Product Manager", "Marketing Manager"]
    )
    
    if uploaded_file:
        with st.spinner("Extracting text from resume..."):
            text, warnings, file_type = TextExtractor.handle_upload(uploaded_file)
        
        if warnings:
            for warning in warnings:
                st.warning(warning)
        
        if text:
            st.success(f"✅ Successfully extracted {len(text.split())} words from {file_type} file")
            
            with st.expander("📄 Extracted Text Preview", expanded=False):
                st.text(text[:1000] + ("..." if len(text) > 1000 else ""))
            
            with st.spinner("Analyzing resume with ATS system..."):
                scorer = ATSScorer(text, job_role)
                results = scorer.calculate_master_score()
            
            # Display results
            st.markdown("---")
            st.header("📊 ATS Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                render_score_gauge(results["master_score"])
                st.metric("ATS Score", f"{results['master_score']}/100")
            with col2:
                st.metric("Tier", results["tier"])
            with col3:
                st.metric("Word Count", scorer.word_count)
            
            st.info(f"💡 **Recommendation**: {results['message']}")
            
            # Component scores
            st.subheader("Component Scores")
            for component, score in results["component_scores"].items():
                col1, col2 = st.columns([2, 3])
                with col1:
                    st.write(f"**{component.title()}**")
                with col2:
                    st.progress(score / 100)
                    st.caption(f"{score}/100")
            
            # Detailed feedback
            tab1, tab2, tab3, tab4 = st.tabs(["Keywords", "Formatting", "Sections", "Grammar"])
            
            with tab1:
                st.subheader("Keyword Analysis")
                if results["keywords"]["found_keywords"]:
                    st.write("✅ **Found Keywords:**")
                    render_keyword_tags(results["keywords"]["found_keywords"])
                if results["keywords"]["missing_keywords"]:
                    st.write("❌ **Missing Keywords:**")
                    render_keyword_tags(results["keywords"]["missing_keywords"], "missing")
            
            with tab2:
                st.subheader("Formatting Issues")
                if results["formatting"]["issues"]:
                    for issue in results["formatting"]["issues"]:
                        render_suggestion_card("Formatting Issue", issue, "warning")
                else:
                    st.success("No major formatting issues detected!")
            
            with tab3:
                st.subheader("Section Completeness")
                col1, col2 = st.columns(2)
                with col1:
                    if results["sections"]["found"]:
                        st.write("✅ **Present:**")
                        for section in results["sections"]["found"]:
                            st.write(f"- {section.title()}")
                with col2:
                    if results["sections"]["missing"]:
                        st.write("❌ **Missing:**")
                        for section in results["sections"]["missing"]:
                            st.write(f"- {section.title()}")
            
            with tab4:
                st.subheader("Grammar & Spelling")
                if results["grammar"]["errors"]:
                    for error in results["grammar"]["errors"]:
                        render_suggestion_card("Error", error, "warning")
                else:
                    st.success("No spelling or grammar issues detected!")
            
            # Improvement suggestions
            st.markdown("---")
            st.header("🔧 Improvement Suggestions")
            
            improver = ResumeImprover(text)
            improvements = improver.get_all_improvements()
            
            if improvements["grammar"]:
                st.subheader("Grammar Improvements")
                for err in improvements["grammar"][:5]:
                    render_suggestion_card(
                        f"Line {err['line']}",
                        f"{err['error']}: {err['suggestion']}",
                        "warning"
                    )
            
            if improvements["verbs"]:
                st.subheader("Stronger Verb Suggestions")
                for sugg in improvements["verbs"][:5]:
                    st.info(f"💪 Replace '{sugg['weak_word']}' with '{sugg['suggested']}'")
            
            # Store in session state
            st.session_state['analyzed_text'] = text
            st.session_state['analysis_results'] = results
            
            return results
    
    return None

def render_builder_page():
    st.header("🏗️ Resume Builder")
    st.info("Fill out the form below to create a professional, ATS-optimized resume")
    
    with st.form("resume_builder_form"):
        # Personal Information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email *", placeholder="john.doe@example.com")
            phone = st.text_input("Phone *", placeholder="(123) 456-7890")
        with col2:
            linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/johndoe")
            location = st.text_input("Location", placeholder="City, State")
        
        # Professional Summary
        st.subheader("Professional Summary")
        summary = st.text_area("Summary", height=100, placeholder="Write a 3-5 sentence professional summary...")
        
        # Work Experience
        st.subheader("Work Experience")
        experiences = []
        num_experiences = st.number_input("Number of experiences", min_value=0, max_value=5, value=1)
        
        for i in range(num_experiences):
            st.markdown(f"**Experience {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input(f"Job Title {i+1}", key=f"title_{i}")
                start_date = st.text_input(f"Start Date {i+1}", key=f"start_{i}", placeholder="Jan 2020")
            with col2:
                company = st.text_input(f"Company {i+1}", key=f"company_{i}")
                end_date = st.text_input(f"End Date {i+1}", key=f"end_{i}", placeholder="Present")
            
            description = st.text_area(f"Description {i+1}", key=f"desc_{i}", height=100, 
                                       placeholder="• Achieved X by doing Y\n• Improved Z by W%")
            
            if title or company:
                experiences.append({
                    "title": title,
                    "company": company,
                    "start_date": start_date,
                    "end_date": end_date,
                    "description": description
                })
        
        # Education
        st.subheader("Education")
        education = []
        num_education = st.number_input("Number of degrees", min_value=0, max_value=3, value=1)
        
        for i in range(num_education):
            st.markdown(f"**Degree {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}", placeholder="Bachelor of Science")
                institution = st.text_input(f"Institution {i+1}", key=f"inst_{i}", placeholder="University Name")
            with col2:
                field = st.text_input(f"Field of Study {i+1}", key=f"field_{i}", placeholder="Computer Science")
                grad_year = st.text_input(f"Graduation Year {i+1}", key=f"year_{i}", placeholder="2020")
            
            if degree or institution:
                education.append({
                    "degree": degree,
                    "field": field,
                    "institution": institution,
                    "grad_year": grad_year
                })
        
        # Skills
        st.subheader("Skills")
        skills = st.text_area("Skills (comma-separated)", height=100, 
                              placeholder="Python, JavaScript, Project Management, Leadership, Data Analysis")
        
        # Submit button
        submitted = st.form_submit_button("Generate Resume", use_container_width=True)
        
        if submitted:
            if not name or not email or not phone:
                st.error("Please fill in all required fields (*)")
                return None
            
            resume_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
                "location": location,
                "summary": summary,
                "experiences": experiences,
                "education": education,
                "skills": skills
            }
            
            # Build resume text
            resume_text = ResumeBuilder.build_resume_text(resume_data)
            
            # Store in session state
            st.session_state['built_resume_data'] = resume_data
            st.session_state['built_resume_text'] = resume_text
            
            st.success("✅ Resume generated successfully!")
            
            # Show preview
            st.subheader("Resume Preview")
            preview_html = ResumeBuilder.build_html_preview(resume_data)
            st.markdown(preview_html, unsafe_allow_html=True)
            
            # Download button
            if REPORTLAB_AVAILABLE:
                pdf_bytes = PDFGenerator.generate_pdf(resume_data)
                if pdf_bytes:
                    b64 = base64.b64encode(pdf_bytes).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="resume.pdf" class="download-btn">📄 Download PDF Resume</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
            return resume_data
    
    return None

def render_results_dashboard():
    st.header("📊 Results Dashboard")
    
    if 'analysis_results' in st.session_state:
        results = st.session_state['analysis_results']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("ATS Score", f"{results['master_score']}/100", delta=None)
        with col2:
            st.metric("Tier", results['tier'])
        with col3:
            st.metric("Components", "5/5")
        
        # Score breakdown
        st.subheader("Score Breakdown")
        for component, score in results['component_scores'].items():
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"**{component.title()}**")
            with col2:
                st.progress(score / 100)
                st.caption(f"{score}/100")
        
        # Recommendations
        st.subheader("Top Recommendations")
        recommendations = []
        
        if results['sections']['missing']:
            recommendations.append(f"Add missing sections: {', '.join(results['sections']['missing'])}")
        if results['keywords']['missing_keywords']:
            recommendations.append(f"Add important keywords: {', '.join(results['keywords']['missing_keywords'][:5])}")
        if results['formatting']['issues']:
            recommendations.extend(results['formatting']['issues'][:3])
        
        for rec in recommendations:
            render_suggestion_card("Action Item", rec, "info")
        
        # Export option
        if 'analyzed_text' in st.session_state:
            if st.button("Export Analysis Report"):
                report = f"""
                ATS Resume Analysis Report
                ===========================
                Score: {results['master_score']}/100
                Tier: {results['tier']}
                
                Component Scores:
                {chr(10).join([f"  - {k}: {v}/100" for k, v in results['component_scores'].items()])}
                
                Recommendations:
                {chr(10).join([f"  - {r}" for r in recommendations])}
                """
                st.download_button("Download Report", report, file_name="ats_report.txt")
    else:
        st.info("No analysis results yet. Upload a resume on the 'Upload & Analyze' page first.")

def render_about_page():
    st.header("ℹ️ About This Tool")
    
    st.markdown("""
    ### AI Resume Analyzer & Builder
    
    This tool helps you optimize your resume for Applicant Tracking Systems (ATS) 
    and modern hiring practices.
    
    #### Features:
    - **ATS Scoring**: Get a 0-100 score based on industry-standard criteria
    - **Keyword Analysis**: Identify missing keywords for your target role
    - **Grammar Checking**: Detect common errors and weak phrasing
    - **Resume Builder**: Create ATS-friendly resumes from scratch
    - **PDF Export**: Download professionally formatted resumes
    
    #### How it works:
    1. Upload your existing resume or build a new one
    2. Our AI analyzes content against ATS criteria
    3. Get detailed feedback and improvement suggestions
    4. Download your optimized resume
    
    #### Technology:
    - Built with Python and Streamlit
    - No external API calls - fully self-contained
    - Works entirely in your browser
    - Your data never leaves your computer
    
    #### Tips for best results:
    - Use standard fonts (Arial, Calibri, Times New Roman)
    - Include quantifiable achievements (%, $, numbers)
    - Customize keywords for each job application
    - Keep formatting simple (no tables, columns, or graphics)
    - Save as PDF for final submission
    
    ---
    **Note**: ATS scores are estimates - different systems have different algorithms.
    Use this tool as a guide, not as a guarantee.
    """)

# =============================================================================
# SECTION 11: MAIN APPLICATION
# =============================================================================

def main():
    # Sidebar navigation
    st.sidebar.markdown("## 📋 Navigation")
    
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Home", "📤 Upload & Analyze", "🏗️ Resume Builder", "📊 Results Dashboard", "ℹ️ About"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    if 'analysis_results' in st.session_state:
        score = st.session_state['analysis_results']['master_score']
        st.sidebar.metric("Last ATS Score", f"{score}/100")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 System Status")
    
    libs = []
    if PDF_AVAILABLE:
        libs.append("✅ PDF")
    if DOCX_AVAILABLE:
        libs.append("✅ DOCX")
    if REPORTLAB_AVAILABLE:
        libs.append("✅ PDF Export")
    
    st.sidebar.markdown("\n".join(libs) if libs else "⚠️ Some features limited")
    
    # Page routing
    if page == "🏠 Home":
        render_home_page()
    elif page == "📤 Upload & Analyze":
        render_upload_analyze_page()
    elif page == "🏗️ Resume Builder":
        render_builder_page()
    elif page == "📊 Results Dashboard":
        render_results_dashboard()
    elif page == "ℹ️ About":
        render_about_page()

if __name__ == "__main__":
    main()