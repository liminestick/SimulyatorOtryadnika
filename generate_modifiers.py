from PIL import Image, ImageDraw, ImageFont
import os

# Пути к ресурсам
ICON_DIR = "Images/icon"
FONT_PATH = "fonts/EpilepsySansBold.ttf"
TEMP_DIR = "Images/temp"

# Настройки
SPACING_X = 20     # Отступ между иконкой и текстом
ROW_SPACING_Y = 20 # Отступ между строками
MAX_ICONS_PER_ROW = 2
ICON_SIZE = (48, 48)
TEXT_COLOR = (255, 255, 255)  # Белый цвет текста
FONT_SIZE = 36

# Соответствие слов -> иконок
ICON_MAP = {
    "голод": "hungry.png",
    "здоровье": "health.png",
    "настроение": "mood.png",
    "популярность": "popularity.png"
}

def create_text_with_icon(modifier_value, icon_path):
    """Создаёт маленькое изображение со значением и иконкой"""
    icon = Image.open(icon_path).convert("RGBA")
    icon = icon.resize(ICON_SIZE)

    # Расчёт ширины текста
    text_width = int(len(modifier_value) * FONT_SIZE * 0.5)
    total_width = icon.width + SPACING_X + text_width
    height = max(icon.height, FONT_SIZE)

    img = Image.new("RGBA", (total_width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Вставляем иконку
    img.paste(icon, (0, 0), icon)

    # Рисуем текст рядом
    text_x = icon.width + SPACING_X
    draw.text((text_x, 0), modifier_value, fill=TEXT_COLOR, font=font)

    return img


def get_modifier_image_path(modifiers_dict):
    """Генерирует имя файла на основе модификаторов из словаря"""
    filename_parts = []
    for key, value in modifiers_dict.items():
        keyword = key.lower()
        icon_file = ICON_MAP.get(keyword, None)
        if not icon_file:
            continue
        short_name = os.path.splitext(icon_file)[0]  # убираем .png
        filename_parts.append(f"{value}{short_name}")

    filename = ''.join(filename_parts) + ".png"
    return os.path.join(TEMP_DIR, filename)


def generate_or_get_modifier_image(modifiers_dict):
    """
    Генерирует или возвращает существующее изображение для словаря модификаторов
    :param modifiers_dict: Словарь вроде {'Голод': '+4', 'Деньги': '-8'}
    :return: Путь к изображению
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    output_path = get_modifier_image_path(modifiers_dict)

    if os.path.exists(output_path):
        return output_path

    images = []

    for key, value in modifiers_dict.items():
        keyword = key.lower()

        icon_file = ICON_MAP.get(keyword)
        if not icon_file:
            continue

        icon_path = os.path.join(ICON_DIR, icon_file)
        if not os.path.exists(icon_path):
            continue

        img = create_text_with_icon(value, icon_path)
        images.append(img)

    if not images:
        return None

    # Расчёт размеров сетки
    cols = min(MAX_ICONS_PER_ROW, len(images))
    rows = (len(images) + MAX_ICONS_PER_ROW - 1) // MAX_ICONS_PER_ROW

    row_heights = [0] * rows
    col_widths = [0] * cols

    for i, img in enumerate(images):
        col = i % MAX_ICONS_PER_ROW
        row = i // MAX_ICONS_PER_ROW
        col_widths[col] = max(col_widths[col], img.width)
        row_heights[row] = max(row_heights[row], img.height)

    total_width = sum(col_widths[:cols]) + SPACING_X * (cols - 1)
    total_height = sum(row_heights[:rows]) + ROW_SPACING_Y * (rows - 1)

    result = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))

    for i, img in enumerate(images):
        col = i % MAX_ICONS_PER_ROW
        row = i // MAX_ICONS_PER_ROW

        x = sum(col_widths[:col]) + SPACING_X * col
        y = sum(row_heights[:row]) + ROW_SPACING_Y * row

        result.paste(img, (x, y), img)

    result.save(output_path, "PNG")
    return output_path