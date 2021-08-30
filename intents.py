import json
import requests
import feedparser
from typing import Dict, Any
from bs4 import BeautifulSoup    
from jsonModifier import jsonWriter
import ask_sdk_core.utils as ask_utils
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import get_supported_interfaces
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler

# APL Document file paths for use in handlers
apl_details_path = "aplDetails.json"
# Tokens used when sending the APL directives
APL_DETAILS_TOKEN = "aplDetailsToken"
 

def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)


class MinecraftHelperIntentHandler(AbstractRequestHandler):
  """Handler for minecraft helper intent"""
  def can_handle(self, handler_input):
    return ask_utils.is_intent_name("MinecraftHelperIntent")(handler_input)

  
  def handle(self, handler_input):
    #reads the slot value you entered in the question
    slots = handler_input.request_envelope.request.intent.slots
    item = slots['Item'].resolutions.resolutions_per_authority[0].values[0].value.name

    itemStr = str(item);
    itemRename = itemStr.replace(" ", "-")

    #site url for webscraping
    URL = "https://www.minecraftcraftingguide.net"
    r = requests.get(URL)
    
    #using beautiful soup to scrape text and imgs
    soup = BeautifulSoup(r.content, 'html5lib')
    print(soup.prettify())

    name = soup.find(id = itemRename) 
    print(name)

    #since elements dont have id's we are looping through
    #the nested objects since there is a pattern
    for parent_row in name.parents:
        if parent_row.name == 'tr': 
            break

    for sibling_row in parent_row.next_siblings:
        if sibling_row.name == 'tr': 
            break

    content = list(sibling_row.stripped_strings)
    print(content)

    #creates the imgs link based on the item you are interested in
    imgStart = 'https://www.minecraftcraftingguide.net/img/crafting/'
    imgMid = itemRename +  '-crafting'
    imgEnd = '.png'
    imgLink = imgStart + imgMid + imgEnd
    print(imgLink)

    #checks to see if the link exists
    #changes between .png and .gif as links may vary
    response = requests.get(imgLink)
    if response.status_code == 200:
      print('imgUrl site exists')
    else:
      print('imgUrl site does not exist') 
      imgEnd = '.gif'
      imgLink = imgStart + imgMid + imgEnd
      print(imgLink)
      

    #speach and APL screen text and img
    item_ingredients = f'To craft that you will need the following Ingredients: {content[1]}'
    item_description = f'Item description: {content[0]}'
    speak_output = f'{item_ingredients}. {item_description}'

    #card text
    card_title = f"Crafting Guide for {item}"
    card_text = f'To craft that you will need the following Ingredients: {content[1]}.\n \nItem description, {content[0]}\n \nHere is a link to a crafting guide. {imgLink}'

    #Modifies json file which is used for APL
    jsonWriter(item, item_ingredients, item_description, imgLink)

    #Shows APL screen output if available
    response_builder = handler_input.response_builder
    if get_supported_interfaces(
            handler_input).alexa_presentation_apl is not None:
        response_builder.add_directive(
            RenderDocumentDirective(
                token = APL_DETAILS_TOKEN,
                document = _load_apl_document(apl_details_path)
            )
        )

    else:
        # User's device does not support APL, so tailor the speech to
        # this situation
        speak_output += (" This example would be more interesting on a "
                          "device with a screen, such as an Echo Show or "
                          "Fire TV. If you are using this in the developer"
                          "console make sure to enable APL in Build Tab -> Interfaces")


    #handles all our outputs
    return (
      handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard(card_title, card_text))
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
        speak_output = 'Welcome to the Minecraft Minelexa skil! What do you need help crafting?'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


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