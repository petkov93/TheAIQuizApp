from customtkinter import CTkLabel

from helpers.utils import load_gif_frames
from ui.base.base_frame import BaseFrame


class LoadingFrame(BaseFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CTkLabel(self, text='Generating the quiz...', font=('Aerial', 28, 'bold'))
        self.gif_label = CTkLabel(self, text=' ')
        self.frames = load_gif_frames('assets/gif_images/loading.gif')

        self.load_widgets()
        self.animate_gif()

    def is_frame_on_top(self) -> bool:
        return self == self.master.winfo_children()[-1]

    def load_widgets(self):
        for children in self.winfo_children():
            children.pack(anchor='center', fill='x', expand=True)

    def animate_gif(self, delay=30) -> None:
        def update(idx=0):
            self.gif_label.configure(image=self.frames[idx])
            next_idx = (idx + 1) % len(self.frames)
            self.gif_label.after(delay, update, next_idx)

        if self.is_frame_on_top():
            update()
