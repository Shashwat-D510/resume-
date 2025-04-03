import json
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))  # Use GOOGLE_API_KEY environment variable
model = genai.GenerativeModel('gemini-pro')

def handler(event, context):
    try:
        data = json.loads(event['body'])

        name = data.get('name')
        skills = data.get('skills')
        jobDescription = data.get('jobDescription')

        if not all([name, skills, jobDescription]):
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Missing fields"})
            }

        prompt = f"Generate a resume for {name}. Skills: {skills}. Job Description: {jobDescription}."

        response = model.generate_content(prompt)
        resume = response.text.strip()

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"resume": resume})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }