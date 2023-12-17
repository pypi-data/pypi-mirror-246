messages_with_translation_exist = []
def get_translated_text(language, value_to_be_translated, file_path=None):
    try:
        path = f"./locale/{language}/LC_MESSAGES/django.po"
        if file_path:
            path = file_path
        django_translation_file = open(path, "r")
        # To reduce the amount of time when we search look for the same value
        if value_to_be_translated in messages_with_translation_exist:
            value_to_be_translated_index = messages_with_translation_exist.index(value_to_be_translated)
            santized_translated_value = messages_with_translation_exist[value_to_be_translated_index+1]
            return santized_translated_value
        else:
            while True:
                line = django_translation_file.buffer.readline().decode()
                if f'msgid "{value_to_be_translated}"' in line.strip():
                    translated_value = django_translation_file.buffer.readline().decode()+"\n"
                    santized_translated_value = translated_value.replace("msgstr", "").replace('\"', '').strip()
                    messages_with_translation_exist.append(value_to_be_translated)
                    messages_with_translation_exist.append(santized_translated_value)
                    return santized_translated_value
                if not line:
                    break
        django_translation_file.close()
    except FileNotFoundError as e:
        raise Exception(f"File django.po is not exits")