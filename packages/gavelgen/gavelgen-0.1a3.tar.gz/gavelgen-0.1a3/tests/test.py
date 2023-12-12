from faker import Faker
import requests
from pydantic import BaseModel
from typing import Optional, List
from gavelgen import Gavel

fake = Faker()

# Replace with the URL of your FastAPI server
base_url = "http://localhost:8000"  # Update this with your actual FastAPI server URL

class ScorePayload(BaseModel):
    val: int
    name: str

class InteractionPayload(BaseModel):
    input: str
    output: str
    scores: List[ScorePayload]
    model_name: str
    session_id: Optional[str]
    api_key: str

# Define a small set of predefined session IDs
fake_session_ids = [fake.uuid4() for _ in range(5)]
fake_model_names = [fake.word() for _ in range(5)]
fake_scores =[{"val": fake.random_int(min=-100, max=100), "name": fake.word()} for _ in range(5)]

# Create a bunch of interactions with multiple fake scores
for _ in range(10):
    # Generate a random number of fake scores for each interaction
    num_scores = fake.random_int(min=1, max=5)

    # Sample from the predefined set of fake session IDs
    sampled_session_id = fake.random.choice(fake_session_ids)

    # Generate a random list of fake scores
    scores = [fake.random.choice(fake_scores) for _ in range(num_scores)]

    model_name = fake.random.choice(fake_model_names)
    gavel = Gavel("2dafcaaf-8d96-4114-999e-2ec3776521af")

    interaction = gavel.session(model_name).interact()
    interaction.input = fake.sentence()
    interaction.output = fake.sentence()
    fake_score = fake.random.choice(fake_scores)
    interaction.score(fake_score["name"],fake_score["val"])
    print(interaction.submit())

    # interaction_payload = InteractionPayload(
    #     input=fake.sentence(),
    #     output=fake.sentence(),
    #     model_name=model_name,
    #     session_id=sampled_session_id,
    #     api_key="2dafcaaf-8d96-4114-999e-2ec3776521af",
    #     scores=scores
    # )

    # response = requests.post(f"{base_url}/interactions/", json=interaction_payload.dict())
    # print(f"Interaction created with ID: {response.json()}")

