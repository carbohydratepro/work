import cv2
import numpy as np
import os
import shutil
import pytesseract

from pytesseract import Output
from PIL import Image, ImageEnhance, ImageFilter


def find_largest_rectangle(image, temp_ocr_path):
    '''最大長方形の抽出'''
    # 画像を読み込み、前処理
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # 輪郭の検出
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 最大長方形の検出
    largest_area = 0
    largest_rectangle = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            if area > largest_area:
                largest_area = area
                largest_rectangle = approx

    if largest_rectangle is not None:

        # マスクの作成
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [largest_rectangle], -1, (255, 255, 255), -1) # 白色で塗りつぶす

        # マスクを適用
        result = cv2.bitwise_and(image, mask)

        # 切り取り範囲を計算
        x, y, w, h = cv2.boundingRect(largest_rectangle)
        cropped_result = result[y:y+h, x:x+w]

  
        # 切り取った画像を保存
        cv2.imwrite(f'{temp_ocr_path}/cropped_image.jpg', cropped_result)
        print("最大の長方形の部分を切り取り、保存しました。")
    else:
        print("長方形が見つかりませんでした。")

def crop_right_percentage(image_path, percentage, temp_ocr_path):
    # 画像を読み込む
    img = cv2.imread(image_path)

    # 画像の幅と高さを取得
    height, width = img.shape[:2]

    # 右側のn%を計算
    new_width = int(width * (1 - percentage / 100))

    # 右側のn%を削除
    cropped_img = img[:, :new_width]

    # 切り取った画像を保存
    cv2.imwrite(f'{temp_ocr_path}/cropped_image_del.jpg', cropped_img)



def crop_and_save(image, rectangles, ranges_directories, temp_ocr_path):
    """ 四角形に基づいて画像を切り抜き、保存（幅の条件付き） """
    img_width = image.shape[1]

    for i, rect in enumerate(rectangles):
        x, y, w, h = cv2.boundingRect(rect)
        rect_width_percent = (w / img_width) * 100

        for (min_percent, max_percent, width_percent_range, output_dir) in ranges_directories:
            min_x = int(img_width * min_percent / 100)
            max_x = int(img_width * max_percent / 100)
            
            # 四角形の幅が指定されたパーセント範囲内にあるかチェック
            if width_percent_range[0] <= rect_width_percent <= width_percent_range[1]:
                if x >= min_x and x + w <= max_x:
                    if not os.path.exists(f"{temp_ocr_path}/{output_dir}"):
                        os.makedirs(f"{temp_ocr_path}/{output_dir}")

                    cropped = image[y:y+h, x:x+w]
                    cv2.imwrite(f'{temp_ocr_path}/{output_dir}/rectangle_{i+1}.jpg', cropped)

def save_rectangles(rectangles, img_width, ranges_directories, temp_ocr_path):
    """ 四角形の座標をファイルに保存（幅の条件付き） """
    for (min_percent, max_percent, width_percent_range, output_dir) in ranges_directories:
        min_x = int(img_width * min_percent / 100)
        max_x = int(img_width * max_percent / 100)

        with open(f'{temp_ocr_path}/{output_dir}/rectangles.txt', 'w') as f:
            for i, rect in enumerate(rectangles):
                x, y, w, h = cv2.boundingRect(rect)
                rect_width_percent = (w / img_width) * 100

                if x >= min_x and x + w <= max_x and width_percent_range[0] <= rect_width_percent <= width_percent_range[1]:
                    coordinates = ' '.join([f'({cx},{cy})' for cx, cy in rect])
                    f.write(f'{coordinates}{i+1}\n')


def findSquares(bin_image, image, cond_area=1000):
    squares = []
    contours, _ = cv2.findContours(bin_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        arclen = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, arclen*0.02, True)

        area = abs(cv2.contourArea(approx))
        if approx.shape[0] == 4 and area > cond_area and cv2.isContourConvex(approx):
            rcnt = approx.reshape(-1, 2)
            squares.append(rcnt)
    return squares

def contains_text(image):
    """画像内のテキストを検出して、テキストが存在するかどうかを返す"""
    extracted_text = pytesseract.image_to_string(image)
    return len(extracted_text.strip()) > 0

def crop_save_and_check_text_with_coordinates(image, rectangles, ranges_directories, temp_ocr_path):
    """矩形に基づいて画像を切り抜き、保存（幅の条件付き）、テキストが含まれているか判定し、座標を保存"""
    img_width = image.shape[1]

    for (min_percent, max_percent, width_percent_range, output_dir) in ranges_directories:
        min_x = int(img_width * min_percent / 100)
        max_x = int(img_width * max_percent / 100)
        if not os.path.exists(f"{temp_ocr_path}/{output_dir}"):
            os.makedirs(f"{temp_ocr_path}/{output_dir}")
        coordinates_file_path = f'{temp_ocr_path}/{output_dir}/rectangles.txt'
        with open(coordinates_file_path, 'w') as f:
            for i, rect in enumerate(rectangles):
                x, y, w, h = cv2.boundingRect(rect)
                rect_width_percent = (w / img_width) * 100

                if width_percent_range[0] <= rect_width_percent <= width_percent_range[1] and x >= min_x and x + w <= max_x:
                    cropped_image = image[y:y+h, x:x+w]
                    cropped_pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                    
                    if contains_text(cropped_pil_image):
                        filename = f'rectangle_{i+1}.jpg'
                        cv2.imwrite(os.path.join(temp_ocr_path, output_dir, filename), cropped_image)
                        coordinates = ' '.join([f'({cx},{cy})' for cx, cy in rect])
                        f.write(f'{coordinates} - {filename}\n')

def extract_text(dirs, temp_ocr_path):
    '''OCRを行う関数(多分精度重視)'''
    texts = ""
    for dir in dirs:
        for file_path in os.listdir(f"{temp_ocr_path}/{dir}"):
            if file_path == "rectangles.txt":
                continue
            
            # 画像の前処理
            image = Image.open(f"{temp_ocr_path}/{dir}/{file_path}").convert('L')
            image = image.filter(ImageFilter.MedianFilter())
            # enhancer = ImageEnhance.Contrast(image)
            # image = enhancer.enhance(2)
            image = image.point(lambda x: 0 if x < 140 else 255)

            # Tesseractの設定
            custom_config = r'--oem 3 --psm 7'
            text = pytesseract.image_to_string(image, lang='jpn', config=custom_config)
            texts += f"{text}\n"
    
    return texts
    
# ===========================================================================

def read_coordinates(file_path):
    """テキストファイルから座標データを読み込み、Y座標の小さい順にソートした後、ファイル名をキーとする辞書を返す"""
    coordinates = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            coords_part = parts[0]
            file_name = parts[1]
            # Y座標に基づいて各座標をソート
            coords = sorted([tuple(map(int, coord.strip('()').split(','))) for coord in coords_part.split()], key=lambda x: x[1])
            coordinates[file_name] = coords
    return coordinates



def extract_text_test(dir, temp_ocr_path):
    """指定されたディレクトリから画像のテキストを抽出する"""
    texts = {}
    for file_path in os.listdir(f"{temp_ocr_path}/{dir}"):
        if file_path.endswith(".jpg"):  # 'rectangles.txt'を除外
            image = Image.open(f"{temp_ocr_path}/{dir}/{file_path}").convert('L')
            image = image.filter(ImageFilter.MedianFilter())
            image = image.point(lambda x: 0 if x < 140 else 255)
            custom_config = r'--oem 3 --psm 7'
            text = pytesseract.image_to_string(image, lang='jpn', config=custom_config)
            texts[file_path] = text.strip()
    return texts

def associate_texts(texts_img1, texts_img2, coordinates_img1, coordinates_img2):
    """テキストデータと座標データを関連付けて、Y軸でソートする"""
    associations = []
    for file_path1, text1 in texts_img1.items():
        closest_match = None
        closest_distance = float('inf')  # 初期値を無限大に設定
        y_coordinate = None  # Y座標の値を保持する変数
        for file_path2, text2 in texts_img2.items():
            distance = calculate_distance(coordinates_img1[file_path1], coordinates_img2[file_path2])
            if distance < closest_distance:
                closest_distance = distance
                closest_match = (file_path2, text2)
                y_coordinate = min(coordinates_img2[file_path2], key=lambda x: x[1])[1]  # Y軸の最小値を使用
        if closest_match:
            associations.append((text1, closest_match[1], y_coordinate))
        else:
            associations.append((text1, None, y_coordinate))
    
    # Y軸の値に基づいてソート
    associations.sort(key=lambda x: x[2])
    
    # Y座標を結果から削除して返す（必要に応じて）
    return [(text1, text2) for text1, text2, _ in associations]


def calculate_distance(coords1, coords2):
    """座標間の距離を計算する簡単な例（中心点の距離を使用）"""
    center1 = ((coords1[0][0] + coords1[2][0]) / 2, (coords1[0][1] + coords1[2][1]) / 2)
    center2 = ((coords2[0][0] + coords2[2][0]) / 2, (coords2[0][1] + coords2[2][1]) / 2)
    return ((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2) ** 0.5


# ============================================================================

def ocr_carbon(image):
    temp_ocr_path = "temp_ocr"
    if not os.path.exists(temp_ocr_path):
        os.mkdir(temp_ocr_path)
    else:
        shutil.rmtree(temp_ocr_path)
        os.mkdir(temp_ocr_path)
    
    # 画像から最大の矩形を見つけ、corpped_image.jpgとして保存
    find_largest_rectangle(image, temp_ocr_path)

    # 画像ファイルのパスと削除するパーセントを指定
    image_path = f'{temp_ocr_path}/cropped_image.jpg'
    percentage = 73  # 右側73%を削除

    # 画像から指定したパーセント分右側を削除し、cropped_image_del.jpgとして保存
    crop_right_percentage(image_path, percentage, temp_ocr_path)
    
    image = cv2.imread(f'{temp_ocr_path}/cropped_image_del.jpg', cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    squares = findSquares(bw, image)

    img_width = image.shape[1]
    
    # 範囲と保存ディレクトリのリスト
    # 例: [(0, 50, 'img1'), (50, 100, 'img2')] は、最初の50%をimg1に、次の50%をimg2に保存
    ranges_directories = [
        (15, 50, (22, 28), 'img1'),    # 画像の0%から50%まで、幅が10%から20%の四角形を img1 ディレクトリに保存
        (60, 90, (20, 25), 'img2')    # 画像の50%から100%まで、幅が5%から15%の四角形を img2 ディレクトリに保存
    ]
    
    dirs = ['img1', 'img2']

    # 四角形に基づいて画像を切り抜き、保存 & 情報をテキストファイルに保存
    crop_save_and_check_text_with_coordinates(image, squares, ranges_directories, temp_ocr_path)
    
    
    # 以下の関数を使用してデータを処理
    texts_img1 = extract_text_test("img1", temp_ocr_path)
    texts_img2 = extract_text_test("img2", temp_ocr_path)
    coordinates_img1 = read_coordinates(os.path.join(temp_ocr_path, "img1", "rectangles.txt"))
    coordinates_img2 = read_coordinates(os.path.join(temp_ocr_path, "img2", "rectangles.txt"))
    associations = associate_texts(texts_img1, texts_img2, coordinates_img1, coordinates_img2)

    
    return associations
