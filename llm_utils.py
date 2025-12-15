import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("api_key"))


def generate_user_response(rating, review):
    """
    Generates a polite AI response shown to the user
    """
    prompt = f"""
    You are a customer support assistant.
    Respond politely and empathetically to the customer review.

    Rating: {rating}
    Review: {review}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful customer support assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def generate_summary(review):
    """
    Generates a short summary for admin dashboard
    """
    prompt = f"Summarize the following customer review in one concise sentence:\n{review}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def generate_recommended_action(review):
    """
    Suggests a business action based on the review
    """
    prompt = f"""
    Based on the customer review below,
    suggest the most appropriate next action for the business.

    Review: {review}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
