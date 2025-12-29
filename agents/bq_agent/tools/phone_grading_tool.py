from . import settings
from google import genai
from google.genai import types
from google.cloud import bigquery
from google.adk.tools import FunctionTool, ToolContext

import json
from typing import Optional


class PhoneGradingTool:
    def __init__(
        self,
    ):
        self._client: Optional[genai.Client] = None        
        self._bq_client: Optional[bigquery.Client] = None
        self._vertex_vision_response: Optional[dict] = None

    @property
    def bq_client(self) -> bigquery.Client:
        if self._bq_client is None:
            self._bq_client = bigquery.Client()
        return self._bq_client


    @property
    def client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_CLOUD_PROJECT,
                location=settings.GOOGLE_CLOUD_LOCATION,
            )
        return self._client
    
    
    def _get_images_from_context(self, tool_context: ToolContext):
        images = []
        if not tool_context or not tool_context.session:
            return images
            
        session = tool_context.session
        for event in reversed(session.events):
            if event.author == "user" and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        images.append(part.inline_data.data)
                        print(f"[DEBUG] IMAGE NAME: {part.inline_data.display_name}")
                if images:
                    break
                
        
        if len(images) < 7:
            return """
                Please provide the 7 images listed below:
                
                    1. A screenshot of the About page in your device's settings
                    2. Image of the phone's front
                    3. Image of the phone's back
                    4. Image of the phone's top edge
                    5. Image of the phone's bottom edge
                    6. Image of the phone's left side
                    7. Image of the phone's right side
                    
                Upload all of these images in the next message and the phone assessment will begin.
            """
                        
        return images


    def grade_phone_tool(self, tool_context: ToolContext, additional_description: str = None) -> str:
        
        """Grades the phone based on the given images.

        Args:
            tool_context: The tool context.
            additional_description (str): any additional description from user.

        Returns:
            str: The response containing the grading result
        """
        
        images = self._get_images_from_context(tool_context)
        
        if not isinstance(images, list):
            # tool_context.actions.skip_summarization = True
            return images
        
        bq_json_result = self._call_bigquery(images)
        
        if additional_description is None:
            additional_description = "Give a fair assesment"
        
        from agents.bq_agent.prompts.grader_prompt import grader_system_instruction 
        GRADER_SYSTEM_INSTRUCTION = grader_system_instruction(
            vertex_vision_response=self.vertex_vision_response,
            bq_json_result=bq_json_result
        )
        
        grader_response =  self.client.models.generate_content(
            model=settings.MODEL_ID,
            contents=[
                additional_description
            ],
            config=types.GenerateContentConfig(
                temperature=settings.MODEL_TEMPERATURE,
                system_instruction=GRADER_SYSTEM_INSTRUCTION,
            )
        )
        
        return grader_response.text
        
    
    def _call_bigquery(self, images) -> list:        
        model, storage, grade = self._call_vision(images=images)     
        query = f"""
            SELECT 
                id,
                type,
                storage,
                {grade} as price,
                category,
            FROM `{settings.BQ_TUKERINAJA_KNOWLEDGE}`
            WHERE
                type = @model
                AND storage = @storage
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("model", "STRING", model),
                bigquery.ScalarQueryParameter("storage", "STRING", storage),
            ]
        )

        return self.bq_client.query(query=query, job_config=job_config).to_dataframe().to_json(orient="records")
        

    def _call_vision(self, images) -> tuple[str, str, str]:
        
        from agents.bq_agent.prompts.vision_prompt import vision_instruction   
        
        contents = [
            [types.Part.from_bytes(data=i, mime_type="image/jpeg") for i in images],
            vision_instruction(),
        ]
        
        vision_response = self.client.models.generate_content(
            model=settings.MODEL_ID,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=settings.MODEL_TEMPERATURE,
                response_mime_type="application/json",
                response_schema=self._response_vision_schema(),
            )
        )
        
        vision_response_json = json.loads(vision_response.text)
        print("DEBUG VISION RESPONSE:", vision_response_json)
        
        # STORE JSON AS A CLASS PROP
        self.vertex_vision_response = vision_response_json
        
        model = vision_response_json["model"]
        storage = vision_response_json["storage"]
        grade = self._grade_mapper(vision_response_json["grade"])
        
        return (
            model,
            storage,
            grade,
        )


    def _grade_mapper(self, raw_grade):
        from agents.bq_agent.prompts.grader_prompt import grader_mapper
        
        return grader_mapper().get(raw_grade)


    def _response_vision_schema(self):
        return {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "storage": {"type": "string"},
                "grade": {
                    "type": "string",
                    "description": "Grade of the device written in 'Grade <the grade>'"
                },
                "reasoning": {"type": "string"}
            },
            "required": ["model", "storage", "grade", "reasoning"]
        }


    def _setup_vision_instruction(self):        
        pass


# FUNCTION INITIALIZATION
grade_phone_tool = FunctionTool(PhoneGradingTool().grade_phone_tool)