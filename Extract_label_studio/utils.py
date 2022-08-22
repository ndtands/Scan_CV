import numpy as np
from PIL import Image, ImageDraw, ImageFont


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    
    def norm(self, x:float, y:float, w:float, h:float) -> tuple:
        x_norm = x*100/self.width
        y_norm = y*100/self.height
        w_norm = w*100/self.width
        h_norm = h*100/self.height
        return (x_norm, y_norm, w_norm, h_norm)

    def de_norm(self, x_norm: float, y_norm: float, w_norm: float, h_norm: float) -> tuple:
        x = x_norm*self.width/100
        y = y_norm*self.height/100
        w = w_norm*self.width/100
        h = h_norm*self.height/100
        return (x, y, x+w, y+h)


def fill_result(width, height, x, y, w, h,text, id = None):
    return [
        {"original_width":width,
          "original_height":height,
          "image_rotation":0,
          "value":{
            "x":x,
            "y":y,
            "width":w,
            "height":h,
            "rotation":0
          },
          "id":id,
          "from_name":"bbox",
          "to_name":"image",
          "type":"rectangle",
          "origin":"manual"
        },
        {"original_width":width,
          "original_height":height,
          "image_rotation":0,
          "value":{
            "x":x,
            "y":y,
            "width":w,
            "height":h,
            "rotation":0,
            "text":[
                text
            ]
          },
          "id":id,
          "from_name":"transcription",
          "to_name":"image",
          "type":"textarea",
          "origin":"manual"
        }
    ]


# def extract_pdf(path: str)-> tuple:

#     image = Image.open(path)
#     image = image.convert("RGB")
#     width, height = image.size
#     reg = Rectangle(width, height)
#     ocr_df = pytesseract.image_to_data(image, output_type='data.frame')
#     ocr_df = ocr_df.dropna().reset_index(drop=True)
#     float_cols = ocr_df.select_dtypes('float').columns
#     ocr_df[float_cols] = ocr_df[float_cols].round(0).astype(int)
#     ocr_df = ocr_df.replace(r'^\s*$', np.nan, regex=True)
#     coordinates = ocr_df[['left', 'top', 'width', 'height','text']]
#     actual_boxes = []
#     for _, row in coordinates.iterrows():
#         x, y, w, h = tuple(row[:4])
#         x, y, w, h = reg.norm(x, y, w, h)
#         t = row[4]
#         actual_boxes.append([x, y, w, h, str(t)])
#     return (actual_boxes, (width, height))


def get_data(dicct: dict):
    value = dicct['value']
    if dicct['type'] == 'rectangle':
        x = int(value['x']*10)
        y = int(value['y']*10)
        width = int(value['width']*10)
        height = int(value['height']*10)
        return "bbox", [x, y, x+width, y+height]
    elif dicct['type'] == 'textarea':
        return "text", value['text'][0]
    elif dicct['type'] == 'labels':
        return "label", value['labels'][0]

def get_anotators(annotators: list):
    boxes = []
    words = []
    labels = []
    for t in annotators:
        type_, value = get_data(t)
        if type_ == 'bbox':
            boxes.append(value)
        elif type_ == 'text':
            words.append(value)
        elif type_ == 'label':
            labels.append(value)
    assert len(boxes) == len(words), f'{len(boxes)}, {len(words)}'
    assert len(words) == len(labels),  f'{len(words)}, {len(labels)}'
    return boxes, words, labels