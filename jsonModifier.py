import json

#sepereated into seperate file for organization 
#rewrites the json values according to the scraped data based on the question asked
def jsonWriter(item, ingredients, text, img):
  a_file = open("aplDetails.json", "r")
  json_object = json.load(a_file)
  a_file.close()
  print(json_object)

  json_object["mainTemplate"]["items"][0]["items"][1]["headerSubtitle"] = item
  json_object["mainTemplate"]["items"][0]["items"][2]["text"] = ingredients
  json_object["mainTemplate"]["items"][0]["items"][3]["text"] = text
  json_object["mainTemplate"]["items"][0]["items"][4]["imageSource"] = img

  a_file = open("aplDetails.json", "w")
  json.dump(json_object, a_file, indent=2)
  print(json_object)
  a_file.close()
