import os
from dotenv import load_dotenv
from src.resume_parser import ResumeParser
from src.job_discovery import JobDiscoveryTool

load_dotenv()


if __name__ == "__main__":
    # List of resumes you want to parse
    resumes = [
        #r"D:\smart-job-agent\data\kiruba 7th sem resume.pdf",
        r"D:\smart-job-agent\data\Tumulavakarteek_resume.pdf"
    ]

    # Loop through each resume
    for idx, resume_path in enumerate(resumes, start=1):
        parser = ResumeParser(resume_path)
        parser.extract_text()
        parser.parse_resume()
        parser.suggested_jobs()

        # Save each profile with a unique name
        output_path = r"D:\smart-job-agent\profile.json"
        parser.save_details(output_path)
        print(f"✅ Resume parsed and profile saved to {output_path}")
    print("\n🔍 Testing Job Discovery Tool with random role...")
    print("=== DEBUG THEIRSTACK API ===")
    
    # Check if API key is loaded
    api_key = os.getenv("THEIRSTACK_API_KEY")
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    
    # for the theirstack jobs
     
    
    jobs_tool = JobDiscoveryTool()
    
    # Test with easy_apply filter
    jobs = jobs_tool.fetch_theirstack_jobs(country_code="IN", limit=3)
    
    print(f"✅ Found {len(jobs)} easy apply jobs in India")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job.get('job_title', 'N/A')}")
        print(f"   Company: {job.get('company_object', {}).get('name', 'N/A')}")
        
        # Fixed location line
        locations = job.get('locations', [])
        location_name = locations[0].get('name', 'N/A') if locations else 'N/A'
        print(f"   Location: {location_name}")
        
        print(f"   Apply: {job.get('url', 'N/A')}")
        description = job.get('description', 'No description available')
        print(f"   Description: {description[:200]}...")
        print()
        print()
        
    # for the scrapping dog
    """
    jobs_tool = JobDiscoveryTool(cache_file=r"D:\smart-job-agent\jobs.json")

    try:
        jobs = jobs_tool.fetch_linkedin_jobs(
        field="Software Engineer",
        geoid="102713980",  # LinkedIn GeoID for India
        location="India",
        page=1,
        sort_by="day"
    )


        print("✅ Job discovery API call successful. Top 3 jobs:\n")
        for job in jobs[:3]:
            print(f"- {job.get('job_position')} @ {job.get('company_name')} ({job.get('job_location')})")
            print(f"  Link: {job.get('job_link')}\n")


    except Exception as e:
        print(f"❌ Job discovery failed: {e}")
        
    """