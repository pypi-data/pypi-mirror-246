import requests
from typing import List, Optional
from pydantic import BaseModel
import json
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


BASE_URL = "https://cloud-add-interaction-s7cwzbgfoq-uc.a.run.app"
# BASE_URL = "http://127.0.0.1:5001/gavelgen-38c5b/us-central1/cloud_add_interaction"

class ScorePayload(BaseModel):
    """Pydantic model representing a score payload."""
    val: int
    name: str

class InteractionPayload(BaseModel):
    """Pydantic model representing an interaction payload."""
    input: str = ""
    output: str = ""
    scores: List[ScorePayload] = []
    model_name: str = ""
    session_id: Optional[str] = ""

class Gavel:
    """Gavel class for managing interactions with the API."""
    def __init__(self, api_key):
        """
        Initialize Gavel instance.

        Parameters:
        - api_key (str): The API key for authentication.
        """
        self.api_key = api_key

    def session(self, model_name, id=None):
        """
        Create a session for a specific model.

        Parameters:
        - model_name (str): The name of the model for the session.

        Returns:
        - Session: A Session instance for the specified model.
        """
        return Session(model_name, api_key=self.api_key, id=id)

class Session:
    """Session class representing a session with a specific model."""
    def __init__(self, model_name: str, api_key: str, id=None):
        """
        Initialize Session instance.

        Parameters:
        - model_name (str): The name of the model for the session.
        - api_key (str): The API key for authentication.
        - id (Optional[str]): The session ID (default is None).
        """
        self.model_name = model_name
        self.id = id
        self.api_key = api_key

    def interact(self):
        """
        Create an interaction within the session.

        Returns:
        - Interaction: An Interaction instance for the session.
        """
        return Interaction(api_key=self.api_key, session_id=self.id, model_name=self.model_name)

class Interaction:
    """Interaction class representing an interaction within a session."""
    def __init__(self, api_key: str, model_name: str, session_id=None):
        """
        Initialize Interaction instance.

        Parameters:
        - api_key (str): The API key for authentication.
        - model_name (str): The name of the model for the interaction.
        - session_id (Optional[str]): The session ID (default is None).
        """
        self.api_key = api_key
        self.payload = InteractionPayload(model_name=model_name, session_id=session_id)

    def input(self, model_input):
        """
        Set the input for the interaction.

        Parameters:
        - model_input (str): The input for the interaction.
        """
        self.payload.input = model_input

    def output(self, model_output):
        """
        Set the output for the interaction.

        Parameters:
        - model_output (str): The output for the interaction.
        """
        self.payload.output = model_output

    def score(self, name, value):
        """
        Add a score to the interaction.

        Parameters:
        - name (str): The name of the score.
        - value: The value of the score.
        """
        score = ScorePayload(name=name, val=value)
        self.payload.scores.append(score)

    def submit(self):
        """
        Submit the interaction to the API.

        Returns:
        - dict: The response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(BASE_URL, json=self.payload.dict(), headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to submit interaction. Status Code: {response.status_code}, Response: {response.text}")
