"""
LLM integration to convert scraped text into a JSON quiz.
Tries to use LangChain + Google Gemini if configured; otherwise falls back to a deterministic generator.
"""
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")


def _fallback_generate(title: str, text: str, question_count: int = 10) -> Dict[str, Any]:
    """Enhanced generator for content-relevant quiz creation.

    Creates questions based on actual webpage content with detailed study summary.
    """
    # Enhanced summary: multiple paragraphs for comprehensive overview
    paras = [p.strip() for p in text.split("\n\n") if p.strip() and len(p.strip()) > 50]
    
    # Create comprehensive summary
    summary_parts = []
    if paras:
        # Main overview from first paragraph
        summary_parts.append(f"**Overview**: {paras[0][:400]}...")
        
        # Key points from other paragraphs
        if len(paras) > 1:
            key_points = []
            for para in paras[1:4]:  # Use up to 3 more paragraphs
                if len(para) > 100:
                    # Extract first sentence as key point
                    first_sentence = para.split('.')[0].strip()
                    if len(first_sentence) > 20:
                        key_points.append(first_sentence)
            
            if key_points:
                summary_parts.append(f"**Key Points**: " + " | ".join(key_points[:3]))
    
    # Create study summary
    study_summary = "\n\n".join(summary_parts) if summary_parts else f"This article provides comprehensive information about {title}."

    # Enhanced question generation with content analysis
    questions = []
    qcount = question_count
    
    # Extract meaningful sentences and key terms
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20 and len(s.strip()) < 200]
    
    # Extract key terms (nouns, important words)
    import re
    key_terms = []
    for sentence in sentences[:8]:
        # Simple keyword extraction - look for capitalized words and important terms
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', sentence)
        key_terms.extend([w for w in words if len(w) > 3 and w.lower() != title.lower()])
    
    # Remove duplicates and limit
    key_terms = list(dict.fromkeys(key_terms))[:15]
    
    # Question templates for variety and speed - expanded for 15+ questions
    templates = [
        "What is a key characteristic of {title}?",
        "According to the article, {title} is primarily known for what?", 
        "Which statement best describes {title}?",
        "What important aspect of {title} is mentioned?",
        "How is {title} typically defined or characterized?",
        "What significant feature of {title} does the article highlight?",
        "Which of the following is associated with {title}?",
        "What notable information about {title} is provided?",
        "According to the content, {title} can be described as what?",
        "What key point about {title} is emphasized in the article?",
        "What fundamental principle underlies {title}?",
        "Which aspect makes {title} particularly important?",
        "How does {title} relate to its field of study?",
        "What distinguishes {title} from similar concepts?",
        "What practical application of {title} is discussed?"
    ]
    
    for i in range(qcount):
        # Create content-specific questions
        if i < len(sentences):
            sentence = sentences[i]
            
            # Extract content-based question
            if any(word in sentence.lower() for word in ['is', 'was', 'are', 'were']):
                # Definition/description type question
                q_text = f"According to the article, what is true about {title}?"
            elif any(word in sentence.lower() for word in ['used', 'apply', 'application']):
                # Usage/application type question  
                q_text = f"How is {title} typically used or applied?"
            elif any(word in sentence.lower() for word in ['develop', 'create', 'invent']):
                # Development/history type question
                q_text = f"Regarding the development of {title}, what does the article mention?"
            else:
                # General knowledge question
                template_index = i % len(templates)
                q_text = templates[template_index].format(title=title)
            
            # Create realistic answer options based on actual content
            # Correct answer from actual content
            correct_parts = sentence.split()[:12]  # First part of sentence
            correct_answer = " ".join(correct_parts) + ("..." if len(sentence.split()) > 12 else "")
            
            # Generate plausible distractors
            if i < len(key_terms) and len(key_terms) > 3:
                # Use key terms to create plausible wrong answers
                wrong_options = [
                    f"It primarily focuses on {key_terms[i % len(key_terms)]} and related technologies",
                    f"It is mainly associated with {key_terms[(i+1) % len(key_terms)]} research",
                    f"It represents advances in {key_terms[(i+2) % len(key_terms)]} methodology"
                ]
            else:
                # Generic but topic-relevant wrong answers
                wrong_options = [
                    f"It is an outdated approach to {title.lower()} implementation",
                    f"It represents theoretical concepts not yet practically applied",
                    f"It focuses solely on commercial applications of {title.lower()}"
                ]
            
            # Combine correct and wrong answers
            options = [correct_answer] + wrong_options
            answer = correct_answer
            
        else:
            # Fallback to template-based questions for remaining slots
            template_index = i % len(templates)
            q_text = templates[template_index].format(title=title)
            
            # Use key terms if available for better options
            if key_terms:
                options = [
                    f"It involves {key_terms[0]} and related processes",
                    f"It focuses on {key_terms[1] if len(key_terms) > 1 else 'technical aspects'}",
                    f"It emphasizes {key_terms[2] if len(key_terms) > 2 else 'practical applications'}",
                    f"It represents {key_terms[3] if len(key_terms) > 3 else 'innovative approaches'}"
                ]
            else:
                # Generic options as last resort
                options = [
                    f"A fundamental aspect of {title}",
                    f"An advanced feature of {title}",
                    f"A basic component of {title}",
                    f"A specialized area of {title}"
                ]
            
            answer = options[0]
        
        questions.append({"question": q_text, "options": options, "answer": answer})

    return {
        "title": title, 
        "summary": summary_parts[0] if summary_parts else f"Information about {title}",
        "study_summary": study_summary,
        "questions": questions
    }


def generate_quiz_with_llm(title: str, text: str, question_count: int = 10) -> Dict[str, Any]:
    """Attempt to generate a quiz using LangChain + Gemini. Falls back to deterministic generator.

    Returns a dict matching the schema in the spec.
    """
    # Try to import LangChain and call Gemini
    try:
        if not GEMINI_API_KEY:
            return _fallback_generate(title, text, question_count)
            
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import JsonOutputParser
        from langchain_core.pydantic_v1 import BaseModel, Field
        from typing import List

        # Define the expected structure
        class QuizQuestion(BaseModel):
            question: str = Field(description="The quiz question")
            options: List[str] = Field(description="Four answer options")
            answer: str = Field(description="The correct answer from options")

        class QuizOutput(BaseModel):
            title: str = Field(description="Article title")
            summary: str = Field(description="Brief summary of the article")
            study_summary: str = Field(description="Detailed study summary for learning")
            questions: List[QuizQuestion] = Field(description="List of quiz questions")

        parser = JsonOutputParser(pydantic_object=QuizOutput)

        prompt = ChatPromptTemplate.from_template(
            """You are an educational AI that converts Wikipedia content into a JSON-structured quiz.
            
            Create a quiz from the following article about "{title}":
            
            {article_text}
            
            Generate exactly {question_count} multiple choice questions with 4 options each (A, B, C, D).
            Make sure the questions test understanding of key concepts from the article.
            Make questions challenging but fair, covering different aspects of the topic.
            
            Also provide a comprehensive study_summary that includes:
            - Key concepts and definitions
            - Important facts and figures
            - Main points to remember for studying
            - Context and background information
            
            {format_instructions}
            """
        )

        llm = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=0.7
        )

        chain = prompt | llm | parser

        result = chain.invoke({
            "title": title,
            "article_text": text[:1500],  # Shorter text for faster processing
            "question_count": question_count,
            "format_instructions": parser.get_format_instructions()
        })

        return result

    except Exception as e:
        # If any import/configuration error happens, fall back to deterministic generator
        print(f"LLM generation failed: {e}, using fallback")
        return _fallback_generate(title, text, question_count)


def _generate_study_summary_with_ai(title: str, text: str) -> str:
    """Generate enhanced study summary using Gemini AI based on topic name."""
    print(f"Generating study summary for: {title}")
    print(f"API Key available: {bool(GEMINI_API_KEY)}")
    
    if not GEMINI_API_KEY:
        return f"**Study Material**: This article provides comprehensive information about {title}."
    
    genai.configure(api_key=GEMINI_API_KEY)
    
    prompt = f"""
    Create a comprehensive study summary about "{title}". Generate educational content based on your knowledge of this topic.

    IMPORTANT: DO NOT use any ** asterisks, markdown formatting, or special characters. Use only plain text.

    Write a clean study summary with these sections (use plain text headers only):
    
    Overview: Key concepts and main ideas (2-3 sentences)
    Important Facts: Key dates, figures, and historical information  
    Key Points: Main aspects students should understand
    Context: Background information and significance

    Use simple bullet points with - (dash) not * (asterisk).
    No bold text, no ** formatting, no markdown at all.
    Keep it concise but informative (300-500 words).
    Make it completely clean and readable as plain text only.
    """

    # Initialize the model
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")

    # Generate content
    response = model.generate_content(prompt)
    
    # Clean up the response to remove ALL ** formatting and unwanted characters
    clean_text = response.text
    
    # Remove all ** (double asterisks) formatting
    clean_text = clean_text.replace('**', '')
    
    # Remove single * at start of lines (bullet points)
    lines = clean_text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('* '):
            line = '- ' + line[2:]  # Replace * with -
        cleaned_lines.append(line)
    
    clean_text = '\n'.join(cleaned_lines)
    
    print(f"Generated summary length: {len(clean_text)}")
    
    # Return the cleaned text
    return clean_text


def generate_quiz(title: str, text: str, extra_questions: bool = False) -> Dict[str, Any]:
    """Main entrypoint used by the API.
    Returns a JSON-serializable dict.
    
    Args:
        title: Article title
        text: Article content
        extra_questions: If True, generates 15 questions instead of 10
    """
    # Determine question count
    question_count = 15 if extra_questions else 10
    
    quiz = generate_quiz_with_llm(title, text, question_count)

    # Ensure minimal schema
    if "title" not in quiz:
        quiz["title"] = title
    if "summary" not in quiz:
        quiz["summary"] = (text.split("\n\n")[0][:400]) if text else ""
    # Always generate enhanced study summary using AI (override any existing one)
    quiz["study_summary"] = _generate_study_summary_with_ai(title, text)
    if "questions" not in quiz or not isinstance(quiz["questions"], list):
        quiz["questions"] = []

    return quiz