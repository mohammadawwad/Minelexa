import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import StandardCard
import feedparser
import requests
from bs4 import BeautifulSoup                                                        

URL = "https://www.minecraftcraftingguide.net"
r = requests.get(URL)
   
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())

name = soup.find(id = 'boat') 
print(name)

class MinecraftHelperIntentHandler(AbstractRequestHandler):
  """Handler for minecraft helper intent"""
  def can_handle(self, handler_input):
    return ask_utils.is_intent_name("MinecraftHelperIntent")(handler_input)

    

  def handle(self, handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    item = slots['Item'].value
    itemStr = str(item);
    itemRename = itemStr.replace(" ", "-")

    imgStart = 'https://www.minecraftcraftingguide.net/img/crafting/'
    imgMid = itemRename
    imgEnd = '-crafting.png'
    imgLink = imgStart + imgMid + imgEnd
    print(imgLink)

    speak_output = f'To craft that you will need {itemRename} here is a link {imgLink}'
    card_title = "Img Card Test"
    card_text = "Should be displaying an image"

    imgObj = {
      "smallImageUrl": "https://www.minecraftcraftingguide.net/img/crafting/boat-crafting.png",
      "largeImageUrl": "https://www.minecraftcraftingguide.net/img/crafting/boat-crafting.png"
    }

    return (
      handler_input.response_builder
            .speak(speak_output)
            .set_card(StandardCard(card_title, card_text, imgObj))
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


class HelloWorldIntentHandler(AbstractRequestHandler):
  """Handler for Hello World Intent."""
  def can_handle(self, handler_input):
    print('checking if we can handle')
    return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

  def handle(self, handler_input):
    speak_output = "Hello World!"

    return (
      handler_input.response_builder
          .speak(speak_output)
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