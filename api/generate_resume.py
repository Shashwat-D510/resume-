from http.server import BaseHTTPRequestHandler
import json
import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        name = data.get('name')
        skills = data.get('skills')
        jobDescription = data.get('jobDescription')

        if not all([name, skills, jobDescription]):
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing fields"}).encode('utf-8'))
            return

        prompt = f"Generate a resume for {name}. Skills: {skills}. Job Description: {jobDescription}."

        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200,
                temperature=0.7,
            )
            resume = response.choices[0].text.strip()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"resume": resume}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        return