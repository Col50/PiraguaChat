import os
from dotenv import load_dotenv
from google.cloud import vision_v1p3beta1 as vision

load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)


def get_handwritten_text_from_image(file_path, y_threshold=15):
    try:
        print("Starting OCR process...")
        client = vision.ImageAnnotatorClient()
        with open(file_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        image_context = vision.ImageContext(language_hints=["es-t-i0-handwrit"])
        response = client.document_text_detection(
            image=image, image_context=image_context
        )
        if response.error.message:
            raise Exception(response.error.message)
        full_text = response.full_text_annotation
        word_list = []
        for page in full_text.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = "".join([symbol.text for symbol in word.symbols])
                        x = word.bounding_box.vertices[0].x
                        y = word.bounding_box.vertices[0].y
                        word_list.append({"text": word_text, "x": x, "y": y})
        lines = []
        for word in word_list:
            added = False
            for line in lines:
                if abs(line["y"] - word["y"]) < y_threshold:
                    line["words"].append(word)
                    added = True
                    break
            if not added:
                lines.append({"y": word["y"], "words": [word]})
        lines.sort(key=lambda l: l["y"])
        for line in lines:
            line["words"].sort(key=lambda w: w["x"])
        ordered_text = "\n".join(
            [" ".join([w["text"] for w in line["words"]]) for line in lines]
        )
        return ordered_text
    except Exception as e:
        print("Error:", e)
        return None
