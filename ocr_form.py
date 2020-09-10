import align_images
from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image that we'll assign to template")
ap.add_argument("-t", "--template", required=True,
    help="path to input template image")
args = vars(ap.parse_args())

OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

OCR_Locations = [
    OCRLocation("first_name", (58, 48, 150, 20),                # (265, 237, 751, 106)
        ["first", "middle", "initial", "name"]),
    OCRLocation("last_name", (208, 48, 170, 20),                # (1020, 237, 835, 106)
		["last", "name"]),
	OCRLocation("address", (58, 68, 320, 20),                   # (265, 336, 1588, 106),
		["address"]),
	OCRLocation("city_state_zip", (58, 88, 320, 20),            # (265, 436, 1588, 106),
		["city", "zip", "town", "state"]),
	OCRLocation("employee_signature", (68, 503, 298, 33),       # (319, 2516, 1487, 156),
		["employee", "signature", "form", "valid", "unless", "you", "sign"]),
	OCRLocation("date", (366, 503, 96, 33),                     # (1804, 2516, 504, 156),
        ["date"]),
	OCRLocation("employee_name_address", (58, 542, 244, 37),    # (265, 2706, 1224, 180),
		["employer", "name", "address"]),
	OCRLocation("employee_ein", (371, 542, 92, 38),             # (1831, 2706, 448, 180),
		["employer", "identification", "number", "ein"]),
]

print("[Info] loading images...")
image = cv2.imread(args["image"])
template = cv2.imread(args["template"])

print("[Info] aligning images...")
aligned = align_images.align_images(image, template)

print("[Info] OCR'ing document...")
parsingResults = []

for loc in OCR_Locations:
    (x, y, w, h) = loc.bbox
    roi = aligned[y:y+h, x:x+w]
    cv2.imshow(loc.id, roi)
    cv2.waitKey(0)
    
    rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb)
    
    for line in text.split("\n"):
        if len(line) == 0:
            continue

        lower = line.lower()
        count = sum([lower.count(x) for x in loc.filter_keywords])

        if count == 0:
            parsingResults.append((loc, line))

results = {}

for (loc, line) in parsingResults:
    r = results.get(loc.id, None)

    if r is None:
        results[loc.id] = (line, loc._asdict())
    
    else:
        (existingText, loc) = r
        text = "{}\n{}".format(existingText, line)

        results[loc["id"]] = (text, loc)

for (locID, result) in results.items():
    (text, loc) = result

    print(loc["id"])
    print("=" * len(loc["id"]))
    print("{}\n\n".format(text))

    (x, y, w, h) = loc["bbox"]
    clean = cleanup_text(text)

    cv2.rectangle(aligned, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for (i, line) in enumerate(clean.split("\n")):
        startY = y + (i * 70) + 40
        cv2.putText(aligned, line, (x, startY), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)

cv2.imshow("Input", imutils.resize(image))
cv2.imshow("Output", imutils.resize(aligned))
cv2.waitKey(0)