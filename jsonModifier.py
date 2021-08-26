import json


a_file = open("test.json", "r")
json_object = json.load(a_file)
a_file.close()
print(json_object)


def jsonWriter(item, text, img):
  json_object["mainTemplate"]["items"][0]["items"][1]["headerSubtitle"] = item
  json_object["mainTemplate"]["items"][0]["items"][2]["text"] = text
  json_object["mainTemplate"]["items"][0]["items"][3]["imageSource"] = img

jsonWriter("text", "textiinggn", "text.pmg")

a_file = open("test.json", "w")
json.dump(json_object, a_file, indent=2)
print(json_object)
a_file.close()
