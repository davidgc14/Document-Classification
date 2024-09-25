import joblib
import numpy as np
from io import BytesIO
from pdfminer.high_level import extract_text 
from pdfminer.layout import LAParams 
import re
import unidecode
import os
from pytesseract import image_to_string # para leer imágenes
import fitz # para leer archivos pdf
from PIL import Image # para convertir imágenes a texto

from log import create_logger

logger = create_logger(__name__)



# Import model

model = joblib.load('./model/model.pkl')
vectorizer = joblib.load('./model/vectorizer.pkl')


def predict_model(path):
    text = extraction(path)
    if text == None:
        return None, [0,0]
    
    vectorized = vectorizer.transform([text])
    result = model.predict(vectorized)[0]
    prob = model.predict_proba(vectorized)[0]

    logger.debug(f'Prob: {prob}')
    logger.debug(f'Result: {result}')
    return result, prob



def extraction(file):

    text = np.array([])

    try:
        text = extract_digital_pdf(file)
        logger.debug('File extracted using digital process.')
    except Exception as e:
        logger.warning(str(e))
        logger.debug('Trying with OCR.')
        try:
            text = extract_scanned_pdf(file)
            logger.debug('File extracted using OCR.')
        except Exception as e:
            logger.error(str(e))
            raise Exception('Imposible to extract text from the document.')
    
    return clean_text(text)


def extract_scanned_pdf(file):
    pdf_text = ''

    if not file.readable():
        raise Exception('Document encripted or damaged. Please review the doc status.')
    
    file.seek(0)
    pdf_document = fitz.open(stream=file.read(), filetype="pdf")

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num) 

        zoom = 2.0 # Zoom para mejorar la resolución de la imagen
        mat = fitz.Matrix(zoom, zoom)
        pixmap = page.get_pixmap(matrix=mat)

        # Convertir la página en imagen
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples) #.convert("L")
        page_text = image_to_string(img)

        pdf_text += ' ' + page_text
    return pdf_text


def extract_digital_pdf(file):
    # Config
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    
    file_stream = BytesIO(file.read())

    # extract the text from file
    try:
        pdf_text = extract_text(file_stream, laparams=laparams)
    except Exception as e:
        logger.error(e)
        return None

    len_pdf_text = len(clean_text(pdf_text))
    if len_pdf_text < 20:
        logger.warning('PDF seems to be scanned. No digital information found.')
        raise Exception('PDF seems to be scanned. No digital information found.')
    else:
        return pdf_text
    




def clean_text(text, smallest=4, largest=20):
    if text is None:
        return None
    
    if type(text) != str: # in case of beeing a vector
        text = ' '.join(text)

    cleaned = text.lower()

    cleaned = cleaned.replace('\n', ' ')
    cleaned = cleaned.replace('\t', ' ')
    cleaned = cleaned.replace('\x0c', ' ')

    # remove accents
    cleaned = unidecode.unidecode(cleaned)

    # remove punctuation
    cleaned = re.sub(r'[^\w\s]', ' ', cleaned)

    # remove numbers
    cleaned = re.sub(r'\d+', ' ', cleaned)

    # remove non alphanumeric characters
    cleaned = re.sub(r'[^a-zA-Z0-9]', ' ', cleaned)

    # remove short words
    cleaned = ' '.join([word for word in cleaned.split() if smallest <= len(word) <= largest])

    # remove multiple spaces
    while '  ' in cleaned:
        cleaned = cleaned.replace('  ', ' ')

    cleaned = cleaned.strip()

    logger.debug('Text cleaned.')
    return cleaned