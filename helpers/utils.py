from PIL import Image
from customtkinter import CTkImage


def load_gif_frames(path: str) -> list[CTkImage]:
    """
    Load all frames of a GIF file and convert them into CTkImage objects.

    This function opens a GIF located at the given file path and iterates
    through each frame until the end of the animation.

    Each frame is copied and wrapped in a `CTkImage` with a fixed display size of 300×300 pixels.

    The resulting list of frames can be used for displaying animated GIFs
    inside a CustomTkinter application.
    :param path:
    :return: A list of `CTkImage` objects, one for each frame of the GIF.
    """
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


def wrap_length(text: str, wrap_count: int = 50) -> str:
    """
    Wraps long text so it doesn't go outside the widget
    :param text: the text to be wrapped
    :param wrap_count: char count for each line of text, default is 50 chars
    :return: the formatted text as str.
    """
    count = 0
    formatted = []
    for word in text.split():
        if count + len(word) <= wrap_count:
            formatted.append(word)
            count += len(word)
        else:
            formatted.append(f'\n{word}')
            count = 0
    return ' '.join(formatted)

# def clean_gif_halo(input_path, output_path, threshold=200):
#     frames = []
#     img = Image.open(input_path)
#
#     for frame in ImageSequence.Iterator(img):
#         frame = frame.convert('RGBA')
#         pixels = frame.getdata()
#         new_pixels = []
#
#         for r, g, b, a in pixels:
#             if r > threshold and g > threshold and b > threshold:
#                 new_pixels.append((255, 255, 255, 0))
#             else:
#                 new_pixels.append((r, g, b, a))
#
#         new_frame = Image.new('RGBA', frame.size)
#         new_frame.putdata(new_pixels)
#         frames.append(new_frame)
#
#     frames[0].save(
#         output_path,
#         save_all=True,
#         append_images=frames[1:],
#         loop=0,
#         disposal=2,
#         transparency=0
#     )
