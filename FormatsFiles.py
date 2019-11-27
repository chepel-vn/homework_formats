"""Program describes work with json and xml format of files"""

# Function read file (json or xml)
def get_items_from_file(filename, stype="json"):
  """

  (string, string) -> list or xml object or None

  Function get iterable information from file (format json or xml)

  """
  try:
    if stype == "json":
      with open(filename, encoding="utf8") as file:
        import json
        json_file = json.load(file)
        items = json_file["rss"]["channel"]["items"]
        return items
    elif stype == "xml":
      import xml.etree.ElementTree as ET
      tree = ET.parse(filename)
      root = tree.getroot()
      items = root.findall("channel/item")
      return items
    else:
      print("Данный тип не поддерживается функцией чтения.")
  except FileNotFoundError:
    print(f"Файл \"{filename}\" не найден.")
  except KeyError:
    print(f"В процедуре чтения файла \"{filename}\" задан неверный ключ либо файл имеет другую структуру.")

def get_description(item, stype):
  """

  (list or xml object) -> string

  Function get text of field description

  """
  if stype == "json":
    return item["description"]
  elif stype == "xml":
    return item.find("description").text
  else:
    print("Данный тип файла не поддерживается функцией.")

def get_frequency_dictionary(items, stype, limit_length):
  """

  (list or xml object) -> dict

  Function accumulate all words from text to dictionary and calculate count of entries

  """

  words = {}
  for item in items:
    for word in get_description(item, stype).split():
      word = word.lower()
      if len(word) > limit_length:
        if words.get(word) != None:
          words[word] += 1
        else:
          words[word] = 1

  return words

def main():
  """

  (None) -> None

  Main function describe main functionality

  """

  # string type of file
  type_string = ("json", "xml")

  while True:
    while True:
      try:
        type = int(input("Введите тип файла (1=json 2=xml 3=exit): "))
        if type not in (1, 2, 3):
          print("Введено некорректное значение типа файла.")
        else:
          if type == 3:
            print("Выход из программы.")
            return
          stype = type_string[type-1]
          break
      except ValueError:
        print("Введено не числовое значение, необходимо ввести число.")

    # print(type)
    items = get_items_from_file("newsafr." + stype, stype)

    if items == None:
      print("Информация отсуствует.")
      continue

    # Accumulate all words (length > 6) to dictionary and calculate count of entries
    words = get_frequency_dictionary(items, stype, 6)

    # Sorting dictionary by value and return sorted list of tuple (key, value)
    words_sort = [(k, words[k]) for k in sorted(words.keys(), key=words.get, reverse=True)]

    # Print 10 first tuples
    count = 10
    print(f"Топ {count} самых часто встречающихся слов из \"{stype}\" файла: ")
    for i in range(0, count):
      print(f"Слово \"{words_sort[i][0]}\" встречается {words_sort[i][1]} раз.")
    print("")

main()