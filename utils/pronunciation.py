# import openai
#
# openai.api_key = "your-openai-key"
#
# def get_pronunciation_feedback(user_text, expected_text):
#     prompt = f"""Evaluate the pronunciation based on this:
#     - Expected: "{expected_text}"
#     - Heard: "{user_text}"
#     Give feedback in 1 sentence."""
#
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()
#
def get_pronunciation_feedback(transcript, expected):
    # Dummy logic – replace with MFA or GPT feedback
    for word in expected.split():
        if word.lower() not in transcript.lower():
            return f"Try saying '{word}' more clearly!"
    return "Good job!"
