# 📄 Resume Parser

A powerful Streamlit web application that transforms PDF resumes into structured JSON data and beautifully formatted Markdown profiles using AI-powered parsing.

## 🚀 Live Demo

[**Try the app here**](https://resume-parser-ilgm3dswtlvtpmn2irqebr.streamlit.app/)

## ✨ Features

- **📁 PDF Upload**: Simple drag-and-drop interface for PDF resume uploads
- **🤖 AI-Powered Parsing**: Uses Groq's LLaMA model to extract structured information
- **📊 JSON Output**: Converts resume data into organized JSON format
- **📝 Markdown Generation**: Creates professional profile summaries in Markdown
- **✏️ Edit & Preview**: Edit JSON data with real-time preview
- **💾 Download Options**: Export both JSON and Markdown files
- **🎨 Clean UI**: Minimal, responsive design with modern styling
- **⚡ Fast Processing**: Quick extraction and parsing workflow

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **PDF Processing**: pdfplumber
- **AI/ML**: Groq API (LLaMA 3 70B)
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud

## 📋 Extracted Information

The app extracts and structures the following resume sections:

- **Overview**: Name, current role, company
- **Contact Information**: Phone, email, profile links
- **Skills**: Technical skills and inferred capabilities
- **Work Experience**: Role, company, duration, responsibilities
- **Projects**: Title, guidance, duration, summary
- **Education**: Degree, institution, graduation year
- **Extra-curricular**: Activities and achievements

## 🚀 Quick Start

### Online Usage
1. Visit the [live demo](https://resume-parser-ilgm3dswtlvtpmn2irqebr.streamlit.app/)
2. Upload your PDF resume
3. View the generated markdown profile
4. Edit JSON data if needed
5. Download your structured data

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-parser.git
   cd resume-parser
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your-groq-api-key-here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🔑 API Key Setup

### Get Your Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Login to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key for use in the application

### Local Development
Add your API key to the `.env` file:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### Streamlit Cloud Deployment
1. Go to your app settings in Streamlit Cloud
2. Navigate to "Secrets"
3. Add the following:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```

## 📁 Project Structure

```
resume-parser/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (local only)
├── .gitignore           # Git ignore file
├── README.md            # Project documentation
└── .streamlit/          # Streamlit configuration (optional)
    └── secrets.toml     # Local secrets file
```

## 🔧 Dependencies

- `streamlit==1.28.0` - Web application framework
- `pdfplumber==0.10.3` - PDF text extraction
- `requests==2.31.0` - HTTP requests for API calls
- `python-dotenv==1.0.0` - Environment variable management
- `Pillow==10.0.1` - Image processing support
- `pdfminer.six==20221105` - PDF processing backend
- `cryptography==41.0.7` - Security and encryption

## 📖 Usage Guide

### Step 1: Upload Resume
- Click "Choose a PDF resume file"
- Select your resume (PDF format only)
- File size limit: Reasonable PDF sizes supported

### Step 2: View Results
- Extracted text preview (expandable)
- AI-generated markdown profile
- Success indicators and error handling

### Step 3: Edit (Optional)
- Click "Edit JSON Data" to modify extracted information
- Preview changes before saving
- Save or cancel modifications

### Step 4: Download
- **JSON File**: `resume_data.json` - Structured data
- **Markdown File**: `resume_summary.md` - Formatted profile

## 🎨 Sample Output

### JSON Structure
```json
{
  "overview": {
    "name": "John Doe",
    "current_role": "Software Engineer",
    "company": "Tech Corp"
  },
  "contact_info": {
    "phone": "+1-234-567-8900",
    "email": "john.doe@email.com",
    "profile_links": ["https://github.com/johndoe"]
  },
  "skills": {
    "technical": ["Python", "JavaScript", "React"],
    "inferred": ["Web Development", "API Design"]
  }
}
```

### Markdown Output
```markdown
# John Doe

**Current Role:** Software Engineer at Tech Corp

## 📞 Contact Information
- **Phone:** +1-234-567-8900
- **Email:** john.doe@email.com

## 💻 Skills
**Technical Skills:** Python, JavaScript, React
```

## 🚀 Deployment

### Streamlit Cloud
1. **Push code to GitHub**
2. **Connect to Streamlit Cloud**
3. **Set up secrets** (GROQ_API_KEY)
4. **Deploy** with one click

### Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY='your-api-key'

# Run the app
streamlit run app.py
```

## 🛡️ Security & Privacy

- **API Keys**: Stored securely in environment variables
- **File Processing**: Temporary files are automatically cleaned up
- **Data Privacy**: No resume data is stored permanently
- **HTTPS**: All API communications are encrypted

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for providing the powerful LLaMA API
- **Streamlit** for the excellent web framework
- **pdfplumber** for reliable PDF text extraction
- **Open Source Community** for the amazing tools and libraries

## 📞 Support

If you encounter any issues or have questions:

1. **Check the Issues**: [GitHub Issues](https://github.com/apurba-manna-amsc/resume-parser/issues)
2. **Create New Issue**: Provide detailed description and steps to reproduce
3. **Email**: 98apurbamanna@gmail.com

## 🔄 Updates & Changelog

### v1.0.0 (Current)
- Initial release with core functionality
- PDF upload and text extraction
- AI-powered parsing with Groq API
- JSON editing and markdown generation
- Download capabilities

---

⭐ **If you found this project helpful, please give it a star!** ⭐

**Made with ❤️ by [Apurba Manna](https://github.com/apurba-manna-amsc)**
