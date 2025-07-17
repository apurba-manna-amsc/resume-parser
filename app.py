import streamlit as st
import pdfplumber
import requests
import json
import re
import os
from io import BytesIO
import tempfile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Page configuration
st.set_page_config(
    page_title="Resume Parser",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_file_path = tmp_file.name
        
        text = ""
        with pdfplumber.open(tmp_file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        os.unlink(tmp_file_path)  # Clean up temp file
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def get_resume_parsing_prompt(text):
    """Generate the prompt for resume parsing"""
    return f"""
You are a professional resume parsing assistant.

Your task is to extract structured information from a given resume text and return the result strictly in a valid JSON format, with no explanations or markdown.

Please extract the following fields:

1. overview:
   - name: Full name of the candidate
   - current_role: Latest job title
   - company: Latest company name

2. contact_info:
   - phone: Contact number
   - email: Email address
   - profile_links: List of URLs (LinkedIn, GitHub, portfolio)

3. skills:
   - technical: Skills explicitly listed in the "Skills" section
   - inferred: Skills mentioned in descriptions of experience or projects

4. work_experience:
   - Each entry must include role, company, duration, and a short description of responsibilities or contributions

5. projects:
   - Each entry must include title, under_guidance (if mentioned), duration, and a one-line summary

6. education:
   - Each entry must include degree, institution, and year of passing

7. extra_curricular:
   - List of extra-curricular activities or responsibilities mentioned

Here is the resume text:
{text}

Return only valid JSON. Do not include markdown or any extra explanation.

Example format:

{{
  "overview": {{
    "name": "John Doe",
    "current_role": "Software Engineer",
    "company": "Tech Corp"
  }},
  "contact_info": {{
    "phone": "+1-234-567-8900",
    "email": "john.doe@email.com",
    "profile_links": [
      "https://github.com/johndoe",
      "https://www.linkedin.com/in/johndoe/"
    ]
  }},
  "skills": {{
    "technical": [
      "Python",
      "JavaScript",
      "React",
      "Node.js"
    ],
    "inferred": [
      "Web Development",
      "API Design",
      "Database Management"
    ]
  }},
  "work_experience": [
    {{
      "role": "Software Engineer",
      "company": "Tech Corp",
      "duration": "Jan 2023 – Present",
      "description": "Developed and maintained web applications using modern technologies."
    }}
  ],
  "projects": [
    {{
      "title": "E-commerce Platform",
      "under_guidance": "Senior Developer",
      "duration": "Mar 2023",
      "summary": "Built a full-stack e-commerce solution with payment integration."
    }}
  ],
  "education": [
    {{
      "degree": "B.Tech, Computer Science",
      "institution": "University Name",
      "year": "2022"
    }}
  ],
  "extra_curricular": [
    "Member of Programming Club",
    "Volunteer at Tech Events"
  ]
}}
"""

def parse_resume_with_groq(text, api_key):
    """Parse resume text using Groq API"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": get_resume_parsing_prompt(text)}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error calling Groq API: {str(e)}")
        return None

def fix_llm_output_to_json(llm_output):
    """Fix common JSON formatting issues from LLM output"""
    try:
        # Try parsing directly first
        return json.loads(llm_output)
    except json.JSONDecodeError:
        try:
            # Try basic cleaning
            fixed = re.sub(r"(\w+):", r'"\1":', llm_output)  # Unquoted keys
            fixed = re.sub(r"'", r'"', fixed)  # Single to double quotes
            fixed = re.sub(r",\s*}", "}", fixed)  # Remove trailing commas
            fixed = re.sub(r",\s*]", "]", fixed)
            
            # Remove markdown code blocks if present
            fixed = re.sub(r"```json\n?", "", fixed)
            fixed = re.sub(r"```\n?", "", fixed)
            
            return json.loads(fixed)
        except Exception as e:
            st.error(f"Could not parse JSON: {str(e)}")
            return None

def json_to_markdown(data):
    """Convert JSON data to markdown format"""
    if not data:
        return ""
    
    markdown_content = []
    
    # Overview
    if 'overview' in data:
        overview = data['overview']
        markdown_content.append(f"# {overview.get('name', 'Unknown')}\n")
        if overview.get('current_role') and overview.get('company'):
            markdown_content.append(f"**Current Role:** {overview.get('current_role')} at {overview.get('company')}\n")
    
    # Contact Info
    if 'contact_info' in data:
        contact = data['contact_info']
        markdown_content.append("## 📞 Contact Information\n")
        if contact.get('phone'):
            markdown_content.append(f"- **Phone:** {contact['phone']}\n")
        if contact.get('email'):
            markdown_content.append(f"- **Email:** {contact['email']}\n")
        if contact.get('profile_links'):
            markdown_content.append("- **Profiles:**\n")
            for link in contact['profile_links']:
                markdown_content.append(f"  - {link}\n")
    
    # Skills
    if 'skills' in data:
        skills = data['skills']
        markdown_content.append("## 💻 Skills\n")
        if skills.get('technical'):
            markdown_content.append("**Technical Skills:**\n")
            markdown_content.append(", ".join(skills['technical']) + "\n\n")
        if skills.get('inferred'):
            markdown_content.append("**Inferred Skills:**\n")
            markdown_content.append(", ".join(skills['inferred']) + "\n\n")
    
    # Work Experience
    if 'work_experience' in data and data['work_experience']:
        markdown_content.append("## 🧑‍💼 Work Experience\n")
        for job in data['work_experience']:
            markdown_content.append(f"- **{job.get('role', 'Unknown Role')}**, *{job.get('company', 'Unknown Company')}* ({job.get('duration', 'Duration not specified')})\n")
            markdown_content.append(f"  - {job.get('description', 'No description provided')}\n")
    
    # Projects
    if 'projects' in data and data['projects']:
        markdown_content.append("## 📁 Projects\n")
        for project in data['projects']:
            markdown_content.append(f"- **{project.get('title', 'Untitled Project')}**\n")
            if project.get('under_guidance'):
                markdown_content.append(f"  - *Under Guidance:* {project['under_guidance']}\n")
            if project.get('duration'):
                markdown_content.append(f"  - *Duration:* {project['duration']}\n")
            if project.get('summary'):
                markdown_content.append(f"  - *Summary:* {project['summary']}\n")
    
    # Education
    if 'education' in data and data['education']:
        markdown_content.append("## 🎓 Education\n")
        for edu in data['education']:
            markdown_content.append(f"- **{edu.get('degree', 'Unknown Degree')}**, *{edu.get('institution', 'Unknown Institution')}* ({edu.get('year', 'Year not specified')})\n")
    
    # Extra Curricular
    if 'extra_curricular' in data and data['extra_curricular']:
        markdown_content.append("## 🌟 Extra Curricular\n")
        for item in data['extra_curricular']:
            markdown_content.append(f"- {item}\n")
    
    return "\n".join(markdown_content)

def create_download_link(content, filename, mime_type):
    """Create a download link for content"""
    b64 = BytesIO()
    b64.write(content.encode('utf-8'))
    b64.seek(0)
    return st.download_button(
        label=f"Download {filename}",
        data=b64.getvalue(),
        file_name=filename,
        mime=mime_type
    )

# Main Application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📄 Resume Parser</h1>
        <p>Upload your resume and get structured data in JSON and Markdown formats</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("🔑 GROQ_API_KEY environment variable is not set!")
        st.info("Please set your Groq API key in the environment variables to use this application.")
        st.code("export GROQ_API_KEY='your-api-key-here'")
        return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF resume file",
        type=['pdf'],
        help="Upload a PDF resume file to parse"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Extract text
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
        
        if extracted_text:
            # Show extracted text in expander
            with st.expander("📄 Extracted Text Preview"):
                st.text_area("Raw text from PDF:", extracted_text, height=200, disabled=True)
            
            # Parse with Groq
            with st.spinner("Parsing resume with AI..."):
                parsed_response = parse_resume_with_groq(extracted_text, api_key)
            
            if parsed_response:
                # Fix JSON format
                parsed_json = fix_llm_output_to_json(parsed_response)
                
                if parsed_json:
                    # Store in session state
                    st.session_state.parsed_data = parsed_json
                    
                    # Display success message
                    st.markdown('<div class="success-box">✅ Resume parsed successfully!</div>', unsafe_allow_html=True)
                    
                    # Generate and display markdown
                    markdown_content = json_to_markdown(parsed_json)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown("## 📋 Generated Profile Summary")
                        st.markdown(markdown_content)
                    
                    with col2:
                        st.markdown("## ⚙️ Actions")
                        
                        # Edit JSON option
                        if st.button("✏️ Edit JSON Data"):
                            st.session_state.edit_mode = True
                        
                        # Download buttons
                        st.markdown("### 📥 Download Options")
                        
                        # Download JSON
                        create_download_link(
                            json.dumps(parsed_json, indent=2),
                            "resume_data.json",
                            "application/json"
                        )
                        
                        # Download Markdown
                        create_download_link(
                            markdown_content,
                            "resume_summary.md",
                            "text/markdown"
                        )
                    
                    # Edit mode
                    if st.session_state.get('edit_mode', False):
                        st.markdown("## ✏️ Edit JSON Data")
                        
                        # JSON editor
                        edited_json_str = st.text_area(
                            "Edit the JSON data below:",
                            value=json.dumps(parsed_json, indent=2),
                            height=400,
                            key="json_editor"
                        )
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("💾 Save Changes"):
                                try:
                                    edited_json = json.loads(edited_json_str)
                                    st.session_state.parsed_data = edited_json
                                    st.session_state.edit_mode = False
                                    st.success("✅ Changes saved successfully!")
                                    st.rerun()
                                except json.JSONDecodeError as e:
                                    st.error(f"❌ Invalid JSON format: {str(e)}")
                        
                        with col2:
                            if st.button("🔄 Preview Changes"):
                                try:
                                    edited_json = json.loads(edited_json_str)
                                    preview_markdown = json_to_markdown(edited_json)
                                    st.markdown("### 👀 Preview:")
                                    st.markdown(preview_markdown)
                                except json.JSONDecodeError as e:
                                    st.error(f"❌ Invalid JSON format: {str(e)}")
                        
                        with col3:
                            if st.button("❌ Cancel"):
                                st.session_state.edit_mode = False
                                st.rerun()
                
                else:
                    st.error("❌ Failed to parse the resume. Please try again with a different file.")
            else:
                st.error("❌ Failed to process the resume with AI. Please check your API key and try again.")
        else:
            st.error("❌ Failed to extract text from the PDF. Please ensure the file is not corrupted.")

# App setup instructions
def show_setup_instructions():
    st.sidebar.markdown("## 🛠️ Setup Instructions")
    st.sidebar.markdown("""
    ### Environment Variables Required:
    ```bash
    export GROQ_API_KEY='your-groq-api-key-here'
    ```
    
    ### Dependencies:
    ```bash
    pip install streamlit pdfplumber requests
    ```
    
    ### How to run:
    ```bash
    streamlit run app.py
    ```
    """)

if __name__ == "__main__":
    # Initialize session state
    if 'parsed_data' not in st.session_state:
        st.session_state.parsed_data = None
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    
    # Show setup instructions in sidebar
    show_setup_instructions()
    
    # Run main app
    main()