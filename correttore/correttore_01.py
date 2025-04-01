
# questo usa la libreria dei python 

from docx import Document
import language_tool_python

# Load the document
doc = Document("student_essay.docx")

# Load the LanguageTool grammar checker (for Italian)
tool = language_tool_python.LanguageToolPublicAPI("it")  # "it" for Italian

# Process each paragraph
for para in doc.paragraphs:
    matches = tool.check(para.text)
    for match in matches:
        # Append the first detected error as an inline comment
        para.text += f" [Attento qui: {match.message}]"
        break  # Add only one comment per paragraph

# Save the document
doc.save("student_essay.docx")
print("Grammar mistakes detected and comments added!")
