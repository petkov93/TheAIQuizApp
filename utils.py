from PIL import Image, ImageSequence
from customtkinter import CTkImage


def load_gif_frames(path) -> list[CTkImage]:
    image = Image.open(path)
    frames = []
    try:
        while True:
            frame = CTkImage(image.copy(), size=(300, 300))
            frames.append(frame)
            image.seek(len(frames))
    except EOFError:
        pass
    return frames


def wraplength(text: str, wrap_count: int = 50) -> str:
    words = text.split()
    count = 0
    output_lst = []
    for word in words:
        if count + len(word) <= wrap_count:
            output_lst.append(word)
            count += len(word)
        else:
            output_lst.append(f'\n{word}')
            count = 0
    return ' '.join(output_lst)

def clean_gif_halo(input_path, output_path, threshold=200):
    frames = []
    img = Image.open(input_path)

    for frame in ImageSequence.Iterator(img):
        frame = frame.convert('RGBA')
        pixels = frame.getdata()
        new_pixels = []

        for r, g, b ,a in pixels:
            if r > threshold and g > threshold and b > threshold:
                new_pixels.append((255, 255, 255, 0))
            else:
                new_pixels.append((r, g, b, a))

        new_frame = Image.new('RGBA', frame.size)
        new_frame.putdata(new_pixels)
        frames.append(new_frame)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        disposal=2,
        transparency=0
    )
