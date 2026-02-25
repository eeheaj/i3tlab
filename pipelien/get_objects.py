import openai
import json

openai.api_key = "YOUR_API_KEY"

def get_required_objects(task: str):
    prompt = f"""
You are a perception-planning assistant.

Given a task description, list ONLY the physical objects that must be visually
detected by a YOLO-style object detector to complete the task.

Rules:
- Objects must be visually detectable in a camera image
- Use common object names compatible with YOLO labels
- Exclude abstract or internal items
- Output ONLY a JSON array of strings

Task:
"{task}"
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
