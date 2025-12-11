def format_resume(resume):
    # Function to format the resume for better readability
    formatted_resume = f"Name: {resume.get('name')}\n"
    formatted_resume += f"Email: {resume.get('email')}\n"
    formatted_resume += f"Experience: {resume.get('experience')}\n"
    formatted_resume += f"Education: {resume.get('education')}\n"
    return formatted_resume

def validate_resume(resume):
    # Function to validate the resume data
    required_fields = ['name', 'email', 'experience', 'education']
    for field in required_fields:
        if field not in resume:
            return False
    return True