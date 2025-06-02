import os
import json
import time
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from models.ai_answer_model import AIAnswerResponse, AnswerItem

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def generate_ai_answers(cleaned_text: str, job_position: str, questions: list) -> AIAnswerResponse:

    ai_payload = {
        "cleanedText": cleaned_text,
        "jobPosition": job_position,
        "questions": questions
    }
    system_prompt = (
        "You are a recruitment assistant AI. Analyze the candidate's resume content provided under \"cleanedText\". For each question, answer strictly based on the resume content. Use logical reasoning to combine relevant information even if it spans across different roles or titles. If the question is about work experience, do the following: - Identify all roles relevant to the job domain in the question. - For each relevant role, list: • Job title • Company name • Duration (start and end dates, and total time in months or years) - Then calculate and clearly state the total combined experience in that job domain (e.g., '1 year and 10 months'). - Make sure to include growth if the person has been promoted in the same company. If a question cannot be answered from the text, respond with \"N/A\". Respond in strict JSON format like this: { \"jobPosition\": \"<jobPosition>\", \"answered\": [ { \"id\": \"<question.id>\", \"question\": \"<question text>\", \"answer\": \"<detailed and logically structured answer>\" } ] }"
    )

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=json.dumps(ai_payload))
    ])

    messages = prompt.format_messages()

    llm = ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.3
    )

    start = time.time()
    response = llm(messages)
    end = time.time()

    print(f"⏱️ Time taken: {end - start:.2f} seconds")

    try:
        parsed = json.loads(response.content)

        return AIAnswerResponse(
            jobPosition=parsed["jobPosition"],
            answered=[AnswerItem(**a) for a in parsed["answered"]]
        )

    except Exception as e:
        raise ValueError(f"AI response parsing failed: {str(e)}")
