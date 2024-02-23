from openai import OpenAI
import os


class AI_Handler:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def send_request(self, request):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a nutritionist, helping a form of athlete to achieve there goals"},
                {"role": "user", "content": f"{request}"}
            ]
        )
        response = completion.choices[0].message.content
        return response
