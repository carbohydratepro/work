import os
from pathlib import Path
from pdf2image import convert_from_path

# poppler/binを環境変数PATHに追加する
poppler_dir = Path(__file__).parent.absolute() / "poppler/Library/bin"
os.environ["PATH"] += os.pathsep + str(poppler_dir)

# PDFファイルのパス
pdf_path = "./app/BRN3C2AF4D29ECC_002520.pdf"

# PDFをPNGに変換
images = convert_from_path(pdf_path)

# 各ページを個別のPNGファイルとして保存
for i, image in enumerate(images):
    image = image.rotate(270, expand=True)
    image.save(f'page_{i}.jpg', 'JPEG')
