import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')


class TaskAssistant:
    def __init__(self, role, goal):
        self.role = role
        self.goal = goal

    def audit_with_ai(self, product_data):
        title = product_data.get('title')
        description = product_data.get('description')
        prompt = f"""
        Role: {self.role}
        Goal: {self.goal}

        Product Title: {title}
        Product Description: {description}

        Task: Analyze this Shopify product from the perspective of an AI Shopping Agent.
        1. Identify specific information gaps that would cause an AI to hallucinate or skip this product.
        2. Assign an 'AI Readiness Score' (0-100).
        3. Provide a 'Ranked Action Plan' for the merchant.

        Format the output as JSON:
        {{
          "score": int,
          "gaps": ["gap 1", "gap 2"],
          "action_plan": ["action 1", "action 2"],
          "perception_summary": "How AI sees this product"
        }}
        """

        response = model.generate_content(prompt)
        cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
        return cleaned_response


auditor = TaskAssistant(
    role="AI Representation Auditor",
    goal="Ensure accurate AI discovery and zero-hallucination commerce."
)


def audit_batch(self, products_list):
    prompt = f"""
    Analyze the following Shopify products for AI Readiness.
    Products: {products_list}

    Return a JSON list of objects, one for each product, following this schema:
    [{{ "title": str, "score": int, "gaps": [], "action_plan": [], "perception_summary": str }}]
    """
    response = model.generate_content(prompt)
    return response.text