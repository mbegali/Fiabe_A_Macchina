from docx import Document

# Load the document
doc = Document("student_essay.docx")

# Modify the first paragraph to include a comment
first_paragraph = doc.paragraphs[0]
first_paragraph.text += " [Attento qui: This sentence has a grammar mistake.]"

# Save the document
doc.save("student_essay.docx")
print("Inline comment added successfully!")
