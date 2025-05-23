#! python
import os
import boto3
from dotenv import load_dotenv

load_dotenv()


def get_handwritten_text_from_image_aws(file_path):
    textract = boto3.client(
        "textract",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCES_KEY"),
        region_name=os.getenv("REGION_NAME"),
    )

    # Load local document
    with open(file_path, "rb") as img:
        document_bytes = img.read()

    response = textract.analyze_document(
        Document={"Bytes": document_bytes}, FeatureTypes=["FORMS", "TABLES"]
    )

    # Print text
    text = ""
    print("Extracted text:")
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            text += block["Text"] + "\n"
            print(block["Text"])

    return text
