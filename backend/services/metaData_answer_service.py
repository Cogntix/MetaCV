import os
import json
from typing import List

from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

from models.meta_ai_model import AnswerItem


# Ensure GROQ_API_KEY is set, else raise error early
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")

os.environ["GROQ_API_KEY"] = API_KEY


# Step 0: Load base metadata format
def load_metadata_template() -> dict:
    with open("data/metadata_template.json", "r") as f:
        return json.load(f)


# Step 1: Convert extracted CV text into structured metadata (excluding QA)
def extract_metadata_from_text(extracted_text: str) -> dict:
    template = load_metadata_template()

    prompt = [
        SystemMessage(content=(
            "You are an AI that converts raw resume/CV text into structured metadata JSON. "
            "Return ONLY a valid JSON object in the following structure (exclude 'qa_results'):\n\n"
            f"{json.dumps(template, indent=2)}"
        )),
        HumanMessage(content=extracted_text)
    ]

    groq_chat = ChatGroq(model="llama3-70b-8192", temperature=0.3)

    response = groq_chat.invoke(prompt)

    try:
        metadata = json.loads(response.content)
    except json.JSONDecodeError:
        # Log full response for debugging, but raise safe error message
        raise ValueError("Groq returned invalid JSON response")

    return metadata


# Step 2: Add only answered questions to metadata
def merge_answers_into_metadata(metadata: dict, questions_with_answers: List[AnswerItem]) -> dict:
    qa_dict = {}
    for idx, qa in enumerate(questions_with_answers, 1):
        final_answer = qa.correct_answer or qa.auto_answer
        if final_answer:  # Only include if there's a valid answer
            qa_dict[f"q{idx}"] = {
                "question": qa.question,
                "answer": final_answer
            }
    metadata["qa_results"] = qa_dict
    return metadata


# Step 3: Combined operation
def generate_full_metadata(extracted_text: str, questions_with_answers: List[AnswerItem]) -> dict:
    metadata = extract_metadata_from_text(extracted_text)
    metadata_with_answers = merge_answers_into_metadata(metadata, questions_with_answers)
    return metadata_with_answers


# Optional: Save to file
def save_metadata_to_file(data: dict, path: str = "final_metadata.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
