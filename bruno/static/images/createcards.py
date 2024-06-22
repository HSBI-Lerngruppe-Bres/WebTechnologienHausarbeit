import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import io


# Pfade zu den Hundebildern
dog_images = {
    "red": "bruno/static/images/dog1.jpg",
    "yellow": "bruno/static/images/dog2.webp",
    "blue": "bruno/static/images/buddy.jpeg",
    "green": "bruno/static/images/dog4.jpg"
}

# Farbe für jeden Kartentyp
color_map = {
    "red": (206, 17, 38),       # Rot
    "yellow": (255, 225, 53),   # Gelb
    "blue": (0, 70, 173),       # Blau
    "green": (0, 155, 72)       # Grün
}

def create_uno_card(dog_image_path, card_number, output_path, border_color):
    # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Transparenz
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # Füge die Kartennummer in jede Ecke hinzu
    font_size = 100  # Anpassen der Schriftgröße
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    number_text = str(card_number)
    number_shift_x = 20  # Anzahl der Pixel, um die die Zahlen nach rechts verschoben werden
    number_shift_y = 10
    number_positions = [
        (10 + number_shift_x, 10 + number_shift_y),  # oben links
        (card_width - font_size - 10 + number_shift_x, 10 + number_shift_y),  # oben rechts
        (10 + number_shift_x, card_height - font_size - 10 - number_shift_y),  # unten links
        (card_width - font_size - 10 + number_shift_x, card_height - font_size - 10 - number_shift_y)  # unten rechts
    ]
    
    for pos in number_positions:
        # Zeichne die schwarze Umrandung um die Zahlen
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    draw.text((pos[0] + i, pos[1] + j), number_text, fill="black", font=font)
        # Zeichne den farbigen Text über der schwarzen Umrandung
        draw.text(pos, number_text, fill=border_color, font=font)

    # Füge einen farbigen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline=border_color, width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karten
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPEG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte gespeichert: {output_path}")

def create_uno_card_no_number(dog_image_path, output_path, border_color):
    # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8) 
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # Füge einen farbigen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline=border_color, width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karte
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte ohne Nummer gespeichert: {output_path}")

def uno_reverse_symbol_matplotlib(color):
    fig, ax = plt.subplots(figsize=(2, 2), dpi=100)  # Vergrößere die Figur auf 2x2 Zoll

    left_arrow = '\u21C4'  # ⇄ Left-Right Arrow
    
    # Hinzufügen von Text mit Umrandung
    def add_text_with_outline(ax, x, y, text, fontsize, fontcolor, outlinecolor):
        # Zeichne die Umrandung
        for dx, dy in [(-0.5, -0.5), (-0.5, 0.5), (0.5, -0.5), (0.5, 0.5), (0, -0.5), (-0.5, 0), (0.5, 0), (0, 0.5)]:
            ax.text(x + dx/100, y + dy/100, text, fontsize=fontsize, ha='center', va='center', color=outlinecolor, weight='bold')
        # Zeichne den Text
        ax.text(x, y, text, fontsize=fontsize, ha='center', va='center', color=fontcolor)

    add_text_with_outline(ax, 0.25, 0.5, left_arrow, fontsize=60, fontcolor=color, outlinecolor='black')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)
    
    buf.seek(0)
    arrow_image = Image.open(buf)
    return arrow_image



def reverse(dog_image_path, output_path, border_color):
    # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    number_shift_x = 20
    number_shift_y = 10

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Transparenz
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # RGB-Werte in Bereich 0-1 umrechnen
    border_color_normalized = tuple(c / 255 for c in border_color)
    
    # Erstelle die Pfeilsymbole
    arrow_image = uno_reverse_symbol_matplotlib(border_color_normalized)

    # Füge das Pfeilsymbol in die linke obere Ecke ein
    card.paste(arrow_image, (10 + number_shift_x, 10 + number_shift_y), arrow_image)

    # Erstelle ein weiteres Pfeilsymbol für die gegenüberliegende Ecke
    arrow_image_rotated = arrow_image.rotate(180)

    # Füge das Pfeilsymbol in die rechte untere Ecke ein
    card.paste(arrow_image_rotated, (card_width - arrow_image.size[0] - 10 - number_shift_x, card_height - arrow_image.size[1] - 10 - number_shift_y), arrow_image_rotated)

    # Füge einen farbigen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline=border_color, width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karten
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPEG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte gespeichert: {output_path}")

def zweiziehen(dog_image_path, output_path, border_color):
        # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Transparenz
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # Füge die Kartennummer in jede Ecke hinzu
    font_size = 100  # Anpassen der Schriftgröße
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Text für Nummer +2
    number_text = "+2"
    number_shift_x = 20  # Anzahl der Pixel, um die die Zahlen nach rechts verschoben werden
    number_shift_y = 10
    number_positions = [
        (10 + number_shift_x, 10 + number_shift_y),  # oben links               
        (card_width - font_size - 65 + number_shift_x, card_height - font_size - 20 - number_shift_y)  # unten rechts
    ]
    
    for pos in number_positions:
        # Zeichne die schwarze Umrandung um die Zahlen
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    draw.text((pos[0] + i, pos[1] + j), number_text, fill="black", font=font)
        # Zeichne den farbigen Text über der schwarzen Umrandung
        draw.text(pos, number_text, fill=border_color, font=font)

    # Füge einen farbigen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline=border_color, width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karten
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPEG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte gespeichert: {output_path}")


def create_image_collage(images, output_path):
    # Überprüfe, ob die Anzahl der Bilder korrekt ist
    if len(images) != 4:
        print("Fehler: Die Funktion create_image_collage erwartet genau vier Bilder.")
        return
    
    # Öffne die vier Bilder
    image1 = Image.open(images[0])
    image2 = Image.open(images[1])
    image3 = Image.open(images[2])
    image4 = Image.open(images[3])
    
    # Bestimme die Größe der Collage
    width1, height1 = image1.size
    width2, height2 = image2.size
    width3, height3 = image3.size
    width4, height4 = image4.size
    
    max_width = max(width1, width2, width3, width4)
    max_height = max(height1, height2, height3, height4)
    
    # Erstelle eine leere Collage
    collage_width = max_width * 2
    collage_height = max_height * 2
    collage = Image.new('RGB', (collage_width, collage_height), 'white')
    
    # Füge die Bilder in die Collage ein
    collage.paste(image1, (0, 0))
    collage.paste(image2, (max_width, 0))
    collage.paste(image3, (0, max_height))
    collage.paste(image4, (max_width, max_height))
    
    # Füge einen schwarzen Rand um die Collage hinzu
    border_thickness = 10
    draw = ImageDraw.Draw(collage)
    draw.rectangle([0, 0, collage_width - 1, collage_height - 1], outline="black", width=border_thickness)
    
    # Speichere die Collage
    collage.save(output_path)
    print(f"Collage gespeichert: {output_path}")


def vierziehen(dog_image_path, output_path, border_color):
    # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Transparenz
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # Füge die Kartennummer in jede Ecke hinzu
    font_size = 100  # Anpassen der Schriftgröße
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Nummer +4
    number_text = "+4"
    number_shift_x = 20  # Anzahl der Pixel, um die die Zahlen nach rechts verschoben werden
    number_shift_y = 10
    number_positions = [
        (10 + number_shift_x, 10 + number_shift_y),  # oben links               
        (card_width - font_size - 65 + number_shift_x, card_height - font_size - 20 - number_shift_y)  # unten rechts
    ]
    
    for pos in number_positions:
        # Zeichne die schwarze Umrandung um die Zahlen
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    draw.text((pos[0] + i, pos[1] + j), number_text, fill="black", font=font)
        # Zeichne den farbigen Text über der schwarzen Umrandung
        draw.text(pos, number_text, fill="black", font=font)

    # Füge einen schwarzen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karte
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPEG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte gespeichert: {output_path}")



def generate_skip_symbol(line_color):
    fig, ax = plt.subplots()

    # Zeichnen eines Kreises als Basis für das Symbol
    circle = plt.Circle((0.5, 0.5), 0.4, edgecolor=line_color, facecolor='none', linewidth=10)
    ax.add_patch(circle)

    # Berechnen der Endpunkte des Strichs, sodass er am Rand des Kreises endet
    radius = 0.4
    offset = radius / np.sqrt(2)  # Offset für die Diagonale

    x = np.array([0.5 - offset, 0.5 + offset])
    y = np.array([0.5 - offset, 0.5 + offset])

    # Zeichnen des dickeren Schrägstrichs
    line_width = 10  # Dicke des Strichs in der Mitte
    ax.plot(x, y, color=line_color, linewidth=line_width)

    # Entfernen der Achsen
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Speichern des Symbols in ein BytesIO-Objekt
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    buf.seek(0)
    plt.close(fig)

    # Laden des Bildes aus dem BytesIO-Objekt
    symbol_image = Image.open(buf)
    return symbol_image


def skip(dog_image_path, output_path, border_color):
    # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    number_shift_x = 20
    number_shift_y = 10

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Transparenz
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # RGB-Werte in Bereich 0-1 umrechnen
    border_color_normalized = tuple(c / 255 for c in border_color)
    
    # Erstelle das Aussetzen-Symbol
    skip_symbol = generate_skip_symbol(border_color_normalized)
    skip_symbol = skip_symbol.resize((100, 100), Image.LANCZOS)  # Größe des Symbols anpassen

    # Füge das Aussetzen-Symbol in die linke obere Ecke ein
    card.paste(skip_symbol, (10 + number_shift_x, 10 + number_shift_y), skip_symbol)

    # Erstelle ein weiteres Aussetzen-Symbol für die gegenüberliegende Ecke
    skip_symbol_rotated = skip_symbol.rotate(180)

    # Füge das Aussetzen-Symbol in die rechte untere Ecke ein
    card.paste(skip_symbol_rotated, (card_width - skip_symbol.size[0] - 10 - number_shift_x, card_height - skip_symbol.size[1] - 10 - number_shift_y), skip_symbol_rotated)

    # Füge einen farbigen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline=border_color, width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karte
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPEG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte gespeichert: {output_path}")


def vierziehen_color(dog_image_path, output_path, border_color):
        # Prüfe, ob die Bilddatei existiert
    if not os.path.exists(dog_image_path):
        print(f"Fehler: Die Datei {dog_image_path} wurde nicht gefunden.")
        return
    
    # Öffne das Hundebild
    dog_image = Image.open(dog_image_path).convert("RGBA")

    # Erstelle eine neue weiße Karte
    card_width, card_height = 420, 680
    card = Image.new('RGBA', (card_width, card_height), 'white')
    draw = ImageDraw.Draw(card)

    # Passe das Hundebild an die Kartengröße an und mache es etwas transparenter
    dog_image = dog_image.resize((card_width, card_height), Image.LANCZOS)
    alpha = dog_image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)  # Transparenz
    dog_image.putalpha(alpha)

    # Platziere das transparente Hundebild auf der Karte
    card.paste(dog_image, (0, 0), dog_image)

    # Füge die Kartennummer in jede Ecke hinzu
    font_size = 100  # Anpassen der Schriftgröße
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Text für Nummer +2
    number_text = "+4"
    number_shift_x = 20  # Anzahl der Pixel, um die die Zahlen nach rechts verschoben werden
    number_shift_y = 10
    number_positions = [
        (10 + number_shift_x, 10 + number_shift_y),  # oben links               
        (card_width - font_size - 65 + number_shift_x, card_height - font_size - 20 - number_shift_y)  # unten rechts
    ]
    
    for pos in number_positions:
        # Zeichne die schwarze Umrandung um die Zahlen
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (0, 0):
                    draw.text((pos[0] + i, pos[1] + j), number_text, fill="black", font=font)
        # Zeichne den farbigen Text über der schwarzen Umrandung
        draw.text(pos, number_text, fill=border_color, font=font)

    # Füge einen farbigen Rand um die Karte hinzu
    border_thickness = 10
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline="black", width=border_thickness + 2)

    # Füge einen Rand um die Karte hinzu
    draw.rectangle([border_thickness // 2, border_thickness // 2, card_width - border_thickness // 2, card_height - border_thickness // 2], outline=border_color, width=border_thickness)
    # Zeichne einen zusätzlichen schwarzen Rand
    draw.rectangle([0, 0, card_width - 1, card_height - 1], outline="black", width=border_thickness - 5)

    # Speichere die UNO-Karten
    card = card.convert("RGB")  # Konvertiere zurück zu RGB zum Speichern als JPEG
    card.save(output_path, quality=95)  # Speichern mit hoher Qualität
    print(f"UNO-Karte gespeichert: {output_path}")


# Verzeichnis für die Ausgabedateien
output_dir = "output_cards"
os.makedirs(output_dir, exist_ok=True)

# Erstelle UNO-Karten für alle Farben und speichere sie
base_path = "C:/Users/sophi/Documents/HSBI/4_Semester 4/WebTechnologien/test"
for color, dog_image_name in dog_images.items():
    dog_image_path = os.path.join(base_path, dog_image_name)
    border_color = color_map[color]
    for number in range(0, 10):  # Erstelle Karten mit den Nummern 1 bis 9
        output_path = os.path.join(output_dir, f"{color}_{number}_normal.jpg")
        create_uno_card(dog_image_path, number, output_path, border_color)
    ## Karte ohne Nummer
    output_path_no_number = os.path.join(output_dir, f"{color}_null_wild.jpg")
    create_uno_card_no_number(dog_image_path, output_path_no_number, border_color)
    ## Reverse Karte
    output_path_reverse = os.path.join(output_dir, f"{color}_null_reverse.jpg")
    reverse(dog_image_path, output_path_reverse, border_color)
    ##Zwei-Ziehen Karte
    output_path_zweiziehen = os.path.join(output_dir, f"{color}_2_draw.jpg")
    zweiziehen(dog_image_path, output_path_zweiziehen, border_color)
    ##Vier-Ziehen Karte
    output_path_vierziehen = os.path.join(output_dir, f"wild_4_draw.jpg")
    vierziehen("images/vierziehen.webp", output_path_vierziehen, "black")
    ##Skip-Karte
    output_path_skip = os.path.join(output_dir, f"{color}_null_skip.jpg")
    skip(dog_image_path, output_path_skip, border_color)
    ##Zwei-Ziehen Karte
    output_path_vierziehen_color = os.path.join(output_dir, f"{color}_4_draw.jpg")
    vierziehen_color(dog_image_path, output_path_vierziehen_color, border_color)

##Wild Karte
images = ["output_cards/red_no_number.jpg", "output_cards/green_no_number.jpg", "output_cards/blue_no_number.jpg", "output_cards/yellow_no_number.jpg"]
output_path = "output_cards/wild_null_null.jpg"
create_image_collage(images, output_path)
