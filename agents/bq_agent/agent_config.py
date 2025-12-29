from google.genai import types

CONFIG_1 = types.GenerateContentConfig(
    temperature=0.2,
    max_output_tokens=700,
    safety_settings=[
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT", threshold="OFF"
        ),
    ]
)