import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import StandardCard
import feedparser
import requests
from bs4 import BeautifulSoup       
from ask_sdk_model import Response
import json
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective)
from typing import Dict, Any
from ask_sdk_core.utils import (
    is_request_type, is_intent_name, get_supported_interfaces)
from ask_sdk_model.interfaces.alexa.presentation.apl import UserEvent


#testing new stuff ahhhhhhhhh




# APL Document file paths for use in handlers
hello_world_doc_path = "helloworldDocument.json"
hello_world_button_doc_path = "helloworldWithButtonDocument.json"

# Tokens used when sending the APL directives
HELLO_WORLD_TOKEN = "helloworldToken"
HELLO_WORLD_WITH_BUTTON_TOKEN = "helloworldWithButtonToken"
 
 
def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)
 
 
class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
 
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # return is_intent_name("HelloWorldWithButtonIntent")(handler_input)
        return is_intent_name("HelloWorldIntent")(handler_input)
 
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"
        response_builder = handler_input.response_builder
 
        if get_supported_interfaces(
                handler_input).alexa_presentation_apl is not None:
            response_builder.add_directive(
                RenderDocumentDirective(
                    # token=HELLO_WORLD_TOKEN,
                    # document=_load_apl_document(hello_world_doc_path)
                    token=HELLO_WORLD_WITH_BUTTON_TOKEN,
                    document=_load_apl_document(hello_world_button_doc_path)
                )
            )
#             # Tailor the speech for a device with a screen
#             speak_output += (" Welcome to Alexa Presentation Language. "
#                              "Click the button to see what happens!")


        else:
            # User's device does not support APL, so tailor the speech to
            # this situation
            speak_output += (" This example would be more interesting on a "
                             "device with a screen, such as an Echo Show or "
                             "Fire TV.")
 
        return response_builder.speak(speak_output).response


 
 
class HelloWorldButtonEventHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        # Since an APL skill might have multiple buttons that generate
        # UserEvents, use the event source ID to determine the button press
        # that triggered this event and use the correct handler.
        # In this example, the string 'fadeHelloTextButton' is the ID we set
        # on the AlexaButton in the document.
 
        # The user_event.source is a dict object. We can retrieve the id
        # using the get method on the dictionary.
        if is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input):
            user_event = handler_input.request_envelope.request  # type: UserEvent
            return user_event.source.get("id") == "fadeHelloTextButton"
        else:
            return False
 
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ("Thank you for clicking the button! I imagine you "
                       "already noticed that the text faded away. Tell me to "
                       "start over to bring it back!")
 
        return handler_input.response_builder.speak(speech_text).ask(
            "Tell me to start over if you want me to bring the text back into "
            "view. Or, you can just say hello again.").response






























#Working code do not touch lol

class MinecraftHelperIntentHandler(AbstractRequestHandler):
  """Handler for minecraft helper intent"""
  def can_handle(self, handler_input):
    return ask_utils.is_intent_name("MinecraftHelperIntent")(handler_input)

  

  def handle(self, handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    item = slots['Item'].value
    itemStr = str(item);
    itemRename = itemStr.replace(" ", "-")

    URL = "https://www.minecraftcraftingguide.net"
    r = requests.get(URL)
      
    soup = BeautifulSoup(r.content, 'html5lib')
    print(soup.prettify())

    name = soup.find(id = itemRename) 
    print(name)

    for parent_row in name.parents:
        if parent_row.name == 'tr': 
            break

    for sibling_row in parent_row.next_siblings:
        if sibling_row.name == 'tr': 
            break

    content = list(sibling_row.stripped_strings)
    print(content)

    imgStart = 'https://www.minecraftcraftingguide.net/img/crafting/'
    imgMid = itemRename
    imgEnd = '-crafting.png'
    imgLink = imgStart + imgMid + imgEnd
    print(imgLink)

    speak_output = f'To craft that you will need the following Ingredients: {content[1]}... Item description, {content[0]}.. Here is a link to a crafting guide...   {imgLink}'

    card_title = f"Crafting Guide for {item}"
    card_text = f'To craft that you will need the following Ingredients: {content[1]}.\n \nItem description, {content[0]}\n \nHere is a link to a crafting guide. {imgLink}'

    imgObj = {
      "smallImageUrl": "https://www.minecraftcraftingguide.net/img/crafting/boat-crafting.png",
      "largeImageUrl": "https://www.minecraftcraftingguide.net/img/crafting/boat-crafting.png"
    }

    return (
      handler_input.response_builder
            .speak(speak_output)
            .set_card(StandardCard(card_title, card_text, imgObj))
            .ask(speak_output)
            .response
    )


class GetBlogIntentHandler(AbstractRequestHandler):
  """Handler for the get blog intent"""
  def can_handle(self, handler_input):
    return ask_utils.is_intent_name("GetBlogIntent")(handler_input)

  def handle(self, handler_input):
    feed = feedparser.parse('https://blog.replit.com/feed.xml')
    title = feed['entries'][0]['title']
    summary = feed['entries'][0]['summary']
    speak_output = f'The title of this blogpost is {title} {summary}'

    return (
      handler_input.response_builder
          .speak(speak_output)
          .response
    )

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = 'Welcome to the Replexa skil! What do you need help crafting?'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# class HelloWorldIntentHandler(AbstractRequestHandler):
#   """Handler for Hello World Intent."""
#   def can_handle(self, handler_input):
#     print('checking if we can handle')
#     return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

#   def handle(self, handler_input):
#     speak_output = "Hello World!"

#     return (
#       handler_input.response_builder
#           .speak(speak_output)
#           .response
#     )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "This intent handler is not finished yet!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )