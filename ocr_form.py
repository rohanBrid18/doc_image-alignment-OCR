from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2

OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

OCR_Locations = [
    OCRLocation("step1_first_name", (265, 237, 751, 106),   #(58, 50, 210, 70),
        ["middle", "initial", "first", "name"]),
    OCRLocation("step1_last_name", (1020, 237, 835, 106),
		["last", "name"]),
	OCRLocation("step1_address", (265, 336, 1588, 106),
		["address"]),
	OCRLocation("step1_city_state_zip", (265, 436, 1588, 106),
		["city", "zip", "town", "state"]),
	OCRLocation("step5_employee_signature", (319, 2516, 1487, 156),
		["employee", "signature", "form", "valid", "unless",
		 	"you", "sign"]),
	OCRLocation("step5_date", (1804, 2516, 504, 156),
        ["date"]),
	OCRLocation("employee_name_address", (265, 2706, 1224, 180),
		["employer", "name", "address"]),
	OCRLocation("employee_ein", (1831, 2706, 448, 180),
		["employer", "identification", "number", "ein"]),
]

