import streamlit as st
from paddleocr import PaddleOCR
import cv2
import logging
import json
from pymongo import MongoClient
import google.generativeai as genai
logging.getLogger("ppocr").setLevel(logging.WARNING)

class DatabaseHandler:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['Student']
        self.collection = self.db['test']

    def insert_document(self, document):
        self.collection.insert_one(document)

    def find_document(self, prime_num):
        return self.collection.find_one({'prime_num': prime_num})

    def update_document(self, prime_num, update_data):
        finding = self.collection.find_one({'prime_num': prime_num})
        if finding:
            up_doc = self.collection.update_one({'prime_num': prime_num}, {'$set':update_data})
            return up_doc.modified_count > 0
        return False

    def delete_document(self, prime_num):
        doc_delete = self.collection.delete_many({'prime_num': prime_num})
        return doc_delete.deleted_count > 0

    def delete_field(self, prime_num, field):
        field_delete = self.collection.update_one({'prime_num': prime_num}, {'$unset': {field: ""}})
        return field_delete.modified_count > 0

class CertificateInfoRetrieval:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def ocr_paddle(self, img):
        final_text = ''
        try:
            ocr = PaddleOCR(lang='en', use_angle_cls=True)
            result = ocr.ocr(img)
            for i in range(len(result[0])):
                text = result[0][i][1][0]
                final_text += ' ' + text
        except Exception as e:
            final_text = f"Error: {e}"
        return final_text

    def run_query(self, image_path, prime_number, document_type):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result_text = self.ocr_paddle(image)
        
        genai.configure(api_key='')  # Replace with your API key
        model = genai.GenerativeModel(model_name="gemini-1.0-pro")

        if document_type == "School":
            prompt = [result_text + '''This text is an extract from a school mark sheet. From this extract particular details of
Register number, School Name, Subject with marks and total marks. Also provide which class 10, +1, +2.Provide the details in the form of dictionary. Avoid using triple backticks. ''']
        elif document_type == "College":
            prompt = [result_text + '''This text is an extract from a college mark sheet. From this extract marks and semester details.Provide the details in the form of dictionary. Avoid using triple backticks. ''']

        response = model.generate_content(prompt)
        r1 = response.text
        data = json.loads(r1)
        document = {'prime_num': prime_number}
        data_doc = {**document,**data}
        self.db_handler.insert_document(data_doc)
        st.success("Data inserted successfully.")

    def get_document(self, prime_num):
        document = self.db_handler.find_document(prime_num)
        return document

    def update_document(self, prime_num, field, value):
        update_data = {field: value}
        if self.db_handler.update_document(prime_num, update_data):
            st.success("Document updated successfully!")
        else:
            st.error("Failed to update document.")

    def delete_document(self, prime_num):
        if self.db_handler.delete_document(prime_num):
            st.success("Document deleted successfully")
        else:
            st.error("No document was deleted. Please enter valid information")

    def delete_field(self, prime_num, field):
        if self.db_handler.delete_field(prime_num, field):
            st.success("Field deleted successfully")
        else:
            st.error("No field was deleted. Please enter valid information")

def main():
    cert_info_retrieval = CertificateInfoRetrieval()

    st.title("Certificate Information Retrieval Portal")
    st.caption("A Generative AI assisted system for details extraction from images")

    prime_number = st.text_input("Create Prime Number for a new student")

    uploaded_file = st.file_uploader("Upload a good quality image", type=["jpg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        
        document_type = st.radio("Document Type", ("School", "College"))
        
        if st.button('Submit'):
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_file.getbuffer())
            cert_info_retrieval.run_query("temp_image.jpg", prime_number, document_type)

    st.title("Document View")
    prime_num = st.text_input("Existing student prime number")
    if st.button('Retrieve Document'):
        document = cert_info_retrieval.get_document(prime_num)
        if document:
            st.write("Document found")
            st.json(document)
        else:
            st.write('Document not found')

    st.title("Document Updater")
    st.caption("Update new fields and values in the existing document")

    prime_num_update = st.text_input("Student prime number")
    field = st.text_input("Field")
    value = st.text_input("Value")
    if st.button("Update Document"):
        cert_info_retrieval.update_document(prime_num_update, field, value)

    st.title('Delete Document')
    prime_delete = st.text_input("Enter prime number to delete document")
    if st.button("Delete Document"):
        cert_info_retrieval.delete_document(prime_delete)

    st.title('Delete Field')
    prime_delete_field = st.text_input("Enter prime number")
    field_to_delete = st.text_input("Enter field to delete")
    if st.button("Delete Field"):
        cert_info_retrieval.delete_field(prime_delete_field, field_to_delete)

if __name__ == "__main__":
    main()
