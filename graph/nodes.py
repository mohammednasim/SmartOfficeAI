import re
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY, MODEL_NAME
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.safety_prompt import SAFETY_PROMPT

from rag.retriever import get_retriever
from tools.calculator_tool import calculator
from tools.sql_tool import execute_sql
from tools.email_tool import send_email
from tools.calendar_tool import create_calendar_event

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)


def get_pdf_context(question):
    """Get relevant context from uploaded PDF."""
    try:
        retriever = get_retriever()
        docs = retriever.invoke(question)
        if not docs:
            return ""
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception:
        return ""


def router_node(state):
    """Decide which tool to use based on user input."""

    user_input = state["user_input"].lower()
    
    # Check for calculation
    if re.fullmatch(r"[0-9\+\-*/%\(\)\.\s]+", user_input.strip()):
        return {"next": "calculator"}
    
    # Check for email (prioritize over calendar)
    if "send email" in user_input or "send mail" in user_input or "@" in user_input:
        return {"next": "email"}
    
    # Check for calendar (only if not about email)
    if any(word in user_input for word in ["meeting", "calendar", "appointment", "schedule"]):
        return {"next": "calendar"}
    
    # Check for SQL/database
    if any(word in user_input for word in ["employee", "salary", "department", "database", "manager"]):
        return {"next": "sql"}
    
    # Default: use RAG + Memory + General chat
    return {"next": "chatbot"}



def calculator_node(state):
    """Handle mathematical calculations."""
    user_input = state["user_input"]
    result = calculator(user_input)
    return {"response": result}


def sql_node(state):
    """Generate and execute SQL query using AI."""
    user_input = state["user_input"]
    
    # Use AI to generate SQL query
    sql_prompt = f"""Generate a SQL query for the following user request about an employees table.
The table has columns: id, name, department, salary.

User request: {user_input}

Rules:
- Return ONLY the SQL query, no explanation
- Use SELECT * FROM employees for general employee queries
- Use WHERE department = 'DepartmentName' for specific department queries
- Use SELECT name, salary FROM employees for salary queries
- Use SELECT department, COUNT(*) FROM employees GROUP BY department for department counts
- Keep queries simple and safe"""

    try:
        response = llm.invoke(sql_prompt)
        sql = response.content.strip()
        
        # Clean up the response - remove markdown code blocks if present
        sql = sql.replace('```sql', '').replace('```', '').strip()
        
        # Basic safety check - only allow SELECT queries
        if not sql.upper().startswith('SELECT'):
            sql = "SELECT * FROM employees LIMIT 10"
    except Exception:
        sql = "SELECT * FROM employees LIMIT 10"
    
    result = execute_sql(sql)
    return {"response": result}


def email_node(state):
    """Extract email details and send email using AI-generated content from PDF."""
    user_input = state["user_input"]
    user_input_lower = user_input.lower()
    
    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_input_lower)
    to_email = email_match.group(0) if email_match else ""
    
    if not to_email:
        return {"response": "Please provide recipient email address (e.g., user@example.com)."}
    
    # Get PDF context
    pdf_context = get_pdf_context(user_input)
    
    # Generate structured email using AI
    if pdf_context:
        email_prompt = f"""Based on the following pdf content, generate a professional email to HR with candidate analysis feedback.

pdf Content:
{pdf_context}

User Request: {user_input}

Generate a structured professional email with:
1. Clear subject line
2. Professional greeting
3. Candidate analysis summary
4. Key skills and qualifications
5. Recommendation
6. Professional closing

Format the response as:
Subject: [subject line]

[Email body]"""
        
        response = llm.invoke(email_prompt)
        email_content = response.content
        
        # Parse subject and body
        lines = email_content.split('\n')
        subject = "Candidate Analysis - PDF Review"
        message_lines = []
        
        for line in lines:
            if line.lower().startswith('subject:'):
                subject = line.replace('Subject:', '').replace('subject:', '').strip()
            elif line.strip():
                message_lines.append(line)
        
        message = '\n'.join(message_lines).strip()
    else:
        # Fallback if no PDF content
        subject = "Work Update"
        message = f"""Dear Team,

{user_input}

No document content available for analysis.

Thank you.

Best regards,
Mohammed Nasim"""
    
    result = send_email(to_email, subject, message)
    return {"response": f"Email sent successfully to {to_email} with subject: '{subject}'"}


def calendar_node(state):
    """Extract calendar details and create event using simple parsing."""
    user_input = state["user_input"].lower()
    
    # Simple extraction - ask user for details if not clear
    title = "Meeting"
    date = ""
    time = ""
    
    try:
        # Try to extract date (format: dd-mm-yyyy, yyyy-mm-dd, or similar)
        date_match = re.search(r'(\d{1,4}[\-\/]\d{1,2}[\-\/]\d{1,4})', user_input)
        if date_match:
            date_str = date_match.group(1)
            # Convert to yyyy-mm-dd
            parts = date_str.replace("/", "-").split("-")
            if len(parts[0]) == 4:  # yyyy-mm-dd or yyyy-m-d
                year = parts[0]
                month = parts[1].zfill(2)
                day = parts[2].zfill(2)
                date = f"{year}-{month}-{day}"
            else:  # dd-mm-yyyy or d-m-yyyy
                year = parts[2]
                month = parts[1].zfill(2)
                day = parts[0].zfill(2)
                date = f"{year}-{month}-{day}"
        
        # Try to extract time (format: hh:mm or h pm/am or hh:mm pm/am)
        time_match = re.search(r'(\d{1,2}:\d{2}\s*(pm|am)?)|(\d{1,2}\s*(pm|am))', user_input)
        if time_match:
            time_str = time_match.group(0).replace(" ", "").upper()
            # Handle hh:mm format
            if ":" in time_str:
                parts = time_str.split(":")
                hour = int(parts[0])
                minute = parts[1].replace("PM", "").replace("AM", "")
                if "PM" in time_str and hour != 12:
                    hour += 12
                elif "AM" in time_str and hour == 12:
                    hour = 0
                time = f"{hour}:{minute}"
            # Handle h pm/am format
            else:
                if "PM" in time_str:
                    hour = int(time_str.replace("PM", ""))
                    if hour != 12:
                        hour += 12
                    time = f"{hour}:00"
                elif "AM" in time_str:
                    hour = int(time_str.replace("AM", ""))
                    if hour == 12:
                        hour = 0
                    time = f"{hour:02d}:00"
    except Exception:
        return {"response": "Error parsing date/time. Please use format: dd-mm-yyyy and time like 1pm or 13:00"}
    
    if not date or not time:
        return {"response": "Please provide date (dd-mm-yyyy) and time (hh:mm or 1pm) for the event."}
    
    result = create_calendar_event(title, date, time)
    return {"response": result}


def chatbot_node(state):
    """General chatbot with RAG."""
    user_input = state["user_input"]
    
    # Get context from PDF (with error handling)
    try:
        pdf_context = get_pdf_context(user_input)
    except Exception:
        pdf_context = ""
    
    # Build prompt
    context_parts = [SYSTEM_PROMPT, SAFETY_PROMPT]
    if pdf_context:
        context_parts.append(f"PDF Context:\n{pdf_context}")
    context_parts.append(f"User Question: {user_input}")
    
    full_prompt = "\n\n".join(context_parts)
    
    response = llm.invoke(full_prompt)
    
    return {"response": response.content}