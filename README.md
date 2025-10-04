# Mini Job Application Agent (v1)

This is the **first version** of the Job Application Agent.  
It focuses only on:
1. Extracting text from a resume (PDF)
2. Sending the extracted data to an LLM
3. Generating a job application summary
4. Sending an approval email to the user

---

## Features (Mini Version)

- Read PDF resumes using **PyMuPDF**
- (Optional) Use **spaCy** to extract name, email, phone
- Use **OpenAI** LLM to generate application text
- Send an approval email using **SMTP**

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mini-job-agent.git
   cd mini-job-agent
