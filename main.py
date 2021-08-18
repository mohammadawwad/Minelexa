from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
import intents


# Register the intents with the SkillBuilder. Intents are defined in intents.py.
# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers in intents.py. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()
sb.add_request_handler(intents.LaunchRequestHandler())
sb.add_request_handler(intents.HelpIntentHandler())
sb.add_request_handler(intents.CancelOrStopIntentHandler())
sb.add_request_handler(intents.HelloWorldIntentHandler())
sb.add_request_handler(intents.SessionEndedRequestHandler())
sb.add_request_handler(intents.MinecraftHelperIntentHandler())
sb.add_request_handler(intents.GetBlogIntentHandler())
sb.add_request_handler(intents.IntentReflectorHandler()) # Register this intent last!

app = Flask(__name__)
skill_id = 'amzn1.ask.skill.1e8f4e00-16c4-49a5-aad1-ad07c235ee5e'

skill_adapter = SkillAdapter(
  skill=sb.create(), 
  skill_id=skill_id, app=app
)

@app.route("/", methods=["GET", "POST"])
def invoke_skill():
    return skill_adapter.dispatch_request()

app.run('0.0.0.0', port=443)