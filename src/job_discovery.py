import os
import json
import requests
from datetime import datetime, timedelta
from src.config import SCRAPINGDOG_URL, LINKEDIN_API_KEY,THEIRSTACK_API_KEY

class JobDiscoveryTool:
    def __init__(self, cache_file=r"D:\smart-job-agent\jobs.json"):
        self.base_url = SCRAPINGDOG_URL
        self.cache_file = cache_file

        # make sure parent folder exists
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

    def is_cache_valid(self):
        if not os.path.exists(self.cache_file):
            return False
        file_time = datetime.fromtimestamp(os.path.getmtime(self.cache_file))
        return datetime.now() - file_time < timedelta(days=30)

    def load_from_cache(self):
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_to_cache(self, data):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def fetch_linkedin_jobs(
        self,
        field,
        api_key=LINKEDIN_API_KEY,
        geoid="92000000",
        location=None,
        page=1,
        sort_by=None,
        job_type=None,
        exp_level=None,
        work_type=None,
        filter_by_company=None,
        **kwargs
    ):
        if self.is_cache_valid():
            print("✅ Using cached jobs.json data (less than 30 days old).")
            return self.load_from_cache()

        print("🔄 Cache expired or missing, fetching fresh jobs from API...")

        params = {
            "api_key": api_key,
            "field": field,
            "geoid": geoid,
            "location": location,
            "page": page,
            "sort_by": sort_by,
            "job_type": job_type,
            "exp_level": exp_level,
            "work_type": work_type,
            "filter_by_company": filter_by_company,
        }
        params = {k: v for k, v in params.items() if v is not None}
        params.update(kwargs)

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()

        self.save_to_cache(data)
        print(f"✅ Fresh data saved to {self.cache_file}")

        return data
    
    
    def fetch_theirstack_jobs(
    self,
    # Essential job seeker filters
    roles=None,
    country_code="IN", 
    limit=25,
    
    # Job type & location preferences
    remote=None,           # True=remote only, False=onsite only, None=both
    location_pattern=None, # e.g., "Bangalore", "Hyderabad"
    
    # Job details
    employment_type=None,  # "full_time", "part_time", "contract", "internship"
    experience_level=None, # "junior", "mid_level", "senior", "c_level"
    easy_apply=None,       # True=quick apply jobs only
    
    # Salary expectations
    min_salary_usd=None,
    
    # Job freshness
    posted_in_last_days=7
):
        """Fetch jobs from TheirStack API with job-seeker focused filters"""
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {THEIRSTACK_API_KEY}"
        }
        
        payload = {
            "page": 0,
            "limit": limit,
            "posted_at_max_age_days": posted_in_last_days
        }
        
        # Required country filter
        if country_code:
            payload["job_country_code_or"] = [country_code]
        
        # Job title/role - most important for job seekers
        if roles:
            payload["job_title_or"] = [roles] if isinstance(roles, str) else roles
        
        # Remote work preference
        if remote is not None:
            payload["remote"] = remote
        
        # Specific location within country
        if location_pattern:
            payload["job_location_pattern_or"] = [location_pattern]
        
        # Employment type (full-time, part-time, etc.)
        if employment_type:
            payload["employment_statuses_or"] = [employment_type] if isinstance(employment_type, str) else employment_type
        
        # Experience level
        if experience_level:
            payload["job_seniority_or"] = [experience_level] if isinstance(experience_level, str) else experience_level
        
        # Quick apply jobs
        if easy_apply is not None:
            payload["easy_apply"] = easy_apply
        
        # Salary expectations
        if min_salary_usd:
            payload["min_salary_usd"] = min_salary_usd
        
        try:
            response = requests.post(
                "https://api.theirstack.com/v1/jobs/search",
                json=payload,
                headers=headers
            )
            
            print(f"API Response Status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
            
        except Exception as e:
            print(f"TheirStack error: {e}")
            if hasattr(e, 'response'):
                print(f"Error response: {e.response.text}")
            return []






        """
        def fetch_theirstack_jobs(self, country_code="IN", limit=3, roles=None):
            
            headers = {
                'Content-Type': "application/json",
                'Authorization': f"Bearer {THEIRSTACK_API_KEY}"
            }
            
            payload = {
                "page": 0,
                "limit": limit,
                "job_country_code_or": [country_code],
                "posted_at_max_age_days": 7  # REQUIRED: Jobs from last 7 days
            }
            
            # Add role filtering if provided
            if roles:
                if isinstance(roles, str):
                    roles = [roles]
                payload["job_title_or"] = roles
            
            try:
                response = requests.post(
                    "https://api.theirstack.com/v1/jobs/search",
                    json=payload,
                    headers=headers
                )
                
                print(f"API Response Status: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                return data.get('data', [])  # Note: jobs are in 'data' field, not 'jobs'
                
            except Exception as e:
                print(f"TheirStack error: {e}")
                if hasattr(e, 'response'):
                    print(f"Error response: {e.response.text}")
                return []
            """
        