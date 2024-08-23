from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from waitress import serve
from io import BytesIO

NotoSansJP = "NotoSansJP-Regular.ttf"

app = Flask(__name__)

templates = {
    "test1": {"size": 72, "x": 0, "y": 0, "file": "templates/test1.png", "fill": "black",
              "font": NotoSansJP, "desc": "テスト用に使った1919x810pxの画像、意味はない。"},

    "exit": {"size": 52, "x": 50, "y": 255, "size2": 48, "x2": 120, "y2": 220, "file": "templates/exit.png",
             "fill": "#29d600", "fill2": "white", "font": NotoSansJP,
             "desc": "高速道路の出口看板テンプレート。提供：@tetsuota221"}
}


@app.route('/', methods=['GET'])
def index():
    return templates


@app.route('/test1', methods=['GET'])
def gtest1():
    templatename = "test1"
    text1 = request.args.get('v', '')

    with open(templates[templatename]["file"], 'rb') as f:
        img = f.read()
    image = Image.open(BytesIO(img))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(templates[templatename]["font"], templates[templatename]["size"])
    draw.text((templates[templatename]["x"], templates[templatename]["y"]),
              text1, font=font, fill=templates[templatename]["fill"])

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')


@app.route('/exit', methods=['GET'])
def gexit():
    templatename = "exit"
    text1 = request.args.get('v', '')
    text2 = request.args.get('v2', '')

    with open(templates[templatename]["file"], 'rb') as f:
        img = f.read()
    image = Image.open(BytesIO(img))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(templates[templatename]["font"], templates[templatename]["size"])
    font2 = ImageFont.truetype(templates[templatename]["font"], templates[templatename]["size2"])
    draw.text((templates[templatename]["x"], templates[templatename]["y"]),
              text1, font=font, fill=templates[templatename]["fill"], anchor='mm')
    draw.text((templates[templatename]["x2"], templates[templatename]["y2"]),
              text2, font=font2, fill=templates[templatename]["fill2"])

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)

    return send_file(output, mimetype='image/png')


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3000)
