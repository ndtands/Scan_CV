import json
from utils import *
from PIL import Image
from tqdm import tqdm

f = open('Label.json')
data = json.load(f)

PATH_SOURCE = '/home/administrator/Documents/Label_Tools/pwd/my_data/'
FILE_JSON_OUT = 'D_Tan.json'
DIR_IMAGE = 'Image/'

out = []
gg = []
# Kiểm tra xem kích thước của word có bằng số box và có bằng số label không
for page in tqdm(data, desc ='run'):
    temp = dict()
    id = page['id']
    annotators =  page['annotations'][0]['result']
    try:
      boxes, words, lables = get_anotators(annotators)
      temp['id'] = id
    except:
        print("ERR: ", id)

# Lưu ảnh 
for page in tqdm(data, desc ='run'):
    path_original = page['data']['ocr']
    path_original = path_original.split('/data/')[-1]
    img = Image.open(PATH_SOURCE+'media/'+path_original)
    temp = dict()
    path = page['data']['ocr'].split('-')[-1]
    path= DIR_IMAGE + path
    page['data']['ocr'] = path
    img.save(path)

ctx = json.dumps(data)
with open(FILE_JSON_OUT,'w') as f:
    f.write(ctx)

