def fetch_course_code(html_element):
    req_text = html_element
    course_code_found = False
    output_array = []
    for i in range(0, len(req_text)):
        char = req_text[i]
        if char == ' ':
            output_string = "".join(output_array)
            return output_string
        else:
            output_array.append(char)


