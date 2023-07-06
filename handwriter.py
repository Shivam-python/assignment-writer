# from PIL import Image, ImageDraw, ImageFont
#
# # Load the handwriting font
# font_path = "Paty.ttf"
# font_size = 36
# font = ImageFont.truetype(font_path, font_size)
#
# # Create a blank image
# image_width = 400
# image_height = 200
# image = Image.new("RGB", (image_width, image_height), (255, 255, 255))
# draw = ImageDraw.Draw(image)
#
# # Define the text to render
# text = "Hello, World!"
#
# # Calculate the position to center the text
# text_width, text_height = draw.textsize(text, font=font)
# x = (image_width - text_width) // 2
# y = (image_height - text_height) // 2
#
# # Render the text on the image
# draw.text((x, y), text, font=font, fill=(0, 0, 0))
#
# # Save or display the image
# image.save("handwritten_text.png")
# image.show()

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register the custom TTF font
font_path = "ttf_files/Paty.ttf"
font_name = "CustomFont"
pdfmetrics.registerFont(TTFont(font_name, font_path))


# Create a new PDF document
pdf_path = "samples/handwritten_text.pdf"
pdf = canvas.Canvas(pdf_path, pagesize=A4)

# Define the text to render
# text = ''
with open('sample_test_txt_files/essay-anime.txt', 'r') as file:
    text = file.read().rstrip()

# Calculate the position to start writing
margin = 20 * mm  # Adjust the margin as needed
line_height = 10 * mm  # Adjust the line height as needed
max_width = A4[0] - 2 * margin
x = margin
y = A4[1] - margin - line_height

# Set the custom font
pdf.setFont(font_name, 13)

# Split the text into lines
lines = []
current_line = ""
words = text.split()
for word in words:
    if pdf.stringWidth(current_line + " " + word) <= max_width:
        current_line += " " + word
    else:
        lines.append(current_line.strip())
        current_line = word

if current_line:
    lines.append(current_line.strip())

# Calculate the total height required for the text
total_height = len(lines) * line_height

# Draw lines on the page
line_start = margin
line_end = A4[0] - margin
for i in range(len(lines)):
    line_y = y - i * line_height
    pdf.line(line_start, line_y, line_end, line_y)

# Render the text on the page
for i, line in enumerate(lines[::-1]):
    line_y = y - (total_height - (i+1) * line_height)
    pdf.drawString(x, line_y, line)

# Save and close the PDF document
pdf.save()