from customtkinter import CTkLabel

from helpers.utils import load_gif_frames
from ui.base.base_frame import BaseFrame
from ui.base_widgets.big_label import BigLabel


class LoadingFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gif_label = None
        self.gif_frames = load_gif_frames('assets/gif_images/loading.gif')

        self.load_widgets()

    def load_widgets(self):
        BigLabel(self, text='Generating the quiz...')
        self.gif_label = CTkLabel(self, text=' ')

        for children in self.winfo_children():
            children.pack(anchor='center', fill='x', expand=True)

        self.animate_gif()

    def animate_gif(self, delay=30) -> None:
        def update(idx=0):
            self.gif_label.configure(image=self.gif_frames[idx])
            next_idx = (idx + 1) % len(self.gif_frames)
            self.gif_label.after(delay, update, next_idx)

        if self.is_frame_on_top():
            update()

    def is_frame_on_top(self) -> bool:
        return self == self.master.winfo_children()[-1]
