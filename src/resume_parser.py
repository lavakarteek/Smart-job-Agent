import fitz
import json
import re
import requests
from src.config import GROQ_API_KEY, GROQ_MODEL, GROQ_URL

class ResumeParser:
    def __init__(self,resume_path):
        self.resume_path=resume_path
        self.text_data=""
        self.parsed_profile={}

    def extract_text(self):
        content=fitz.open(self.resume_path)
        text= ""
        for i in content:
            text+=i.get_text()
        self.text_data=text
        #print(self.text_data)
    def llm_call(self, prompt):
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    def extract_json(self, text):
        """Extract JSON content from LLM output.
        Order of attempts:
        1) Fenced code block ```json ... ```
        2) Top-level JSON object {...}
        3) Top-level JSON array [...]
        4) Fallback to trimmed raw text
        """
        # Prefer fenced code block ```json ... ``` (case-insensitive)
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Try to capture a JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return match.group(0).strip()

        # Try to capture a JSON array
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return match.group(0).strip()
        return text.strip()
    def parse_resume(self):
        prompt = f"""
        You are an AI Resume Parser.
        Extract the following from the resume below as valid JSON:
        - name
        - email
        - phone
        - skills (list)
        - education (list)
        - experience (list of role, company, duration)
        - projects (list)
        - certifications (list)
        Resume Text:
        {self.text_data}
        """
        result = self.llm_call(prompt)
        cleaned = self.extract_json(result)
        try:
            self.parsed_profile = json.loads(cleaned)
            #print("✅ Parsed profile:", self.parsed_profile)
        except json.JSONDecodeError:
            self.parsed_profile={"raw_output" : result}
    def suggested_jobs(self):
        prompt = f"""
        Based on this profile:
        {json.dumps(self.parsed_profile, indent=2)}

        Suggest the top 3 job roles/domains that best fit this candidate.
        Return only a JSON array like:
        [
          {{"role": "Role 1"}},
          {{"role": "Role 2"}},
          {{"role": "Role 3"}}
        ]

        and dont add any filler in the top and bottom
        """
        result = self.llm_call(prompt)
        cleaned = self.extract_json(result)
        print(cleaned)
        try:
            roles_json = json.loads(cleaned)
            if isinstance(roles_json,list):
                self.parsed_profile["suggested_roles"]=roles_json
            else:
                self.parsed_profile["suggested_roles"]=[roles_json]
        except json.JSONDecodeError:
            roles = re.findall(r'"role"\s*:\s*"([^"]+)"', cleaned)
            if roles:
                self.parsed_profile["suggested_roles"] = [{"role": r} for r in roles]
            else:
                self.parsed_profile["suggested_roles"] = [{"role":cleaned}]
                    
        
    def save_details(self,output_path=r"D:\smart-job-agent\profile.json"):
        with open(output_path,'a+',encoding='utf-8') as f:
            #f.write(str(self.parsed_profile))
            json.dump(self.parsed_profile,f,indent=4,ensure_ascii=False)
            f.flush()

