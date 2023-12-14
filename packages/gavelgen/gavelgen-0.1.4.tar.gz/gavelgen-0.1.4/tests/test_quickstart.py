from gavelgen import Gavel

# Initialise Gavel API
api_key = "YOUR_API_KEY
gavel = Gavel(api_key)

existing_session_id = None

# Create Session. If session_id = None, we will create a new session
session = gavel.session("ANY_MODEL_NAME", session_id=None)

# Create Interaction
interaction = session.interact()

model_input = "What is the Pythagoras Theorem?"
def my_model(input):
    # Your model logic here
    return "A^2 + B^2 = C^2"

# Add model input to interaction
interaction.input(model_input)

# Add model output to interaction
model_output = my_model(model_input)
interaction.output(model_output)

# When user gives it a thumbs down
interaction.score("USER_FEEDBACK", -100)

# When domain expert scores the output based on a rubrics
interaction.score("RUBRICS_A", 100)

# submit the interaction and receive session_id
interaction_id, session_id = interaction.submit()
print(f"Interaction {interaction_id} in Session {session_id} submitted successfully.")
