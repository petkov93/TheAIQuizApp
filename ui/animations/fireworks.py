import math
import random
import tkinter as tk


# TODO add the fireworks if user get all questions correctly
class Fireworks(tk.Canvas):
    def __init__(self, master, width=600, height=600, **kwargs):
        super().__init__(master, width=width, height=height, bg="black", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.particles = []
        # noinspection PyTypeChecker
        self.after(500, self.launch)

    def launch(self):
        # Launch a new firework at a random position
        x = random.randint(50, int(self.width) - 50)
        y = random.randint(50, int(self.height) // 2)
        colors = ["red", "orange", "yellow", "white", "cyan", "purple", "pink", "green"]
        color = random.choice(colors)

        num_particles = random.randint(20, 40)
        for i in range(num_particles):
            angle = (2 * math.pi / num_particles) * i
            speed = random.uniform(2, 5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append({
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "life": random.randint(20, 40),
                "color": color
            })
        # noinspection PyTypeChecker
        self.after(1000, self.launch)  # launch another after a second
        self.animate()

    def animate(self):
        self.delete("all")
        new_particles = []
        for p in self.particles:
            if p["life"] > 0:
                p["x"] += p["dx"]
                p["y"] += p["dy"]
                p["dy"] += 0.05  # gravity effect
                p["life"] -= 1
                size = max(1, p["life"] // 3)
                self.create_oval(
                    p["x"], p["y"], p["x"] + size, p["y"] + size,
                    fill=p["color"], outline=""
                )
                new_particles.append(p)
        self.particles = new_particles
        if self.particles:
            # noinspection PyTypeChecker
            self.after(30, self.animate)


# Demo
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fireworks Animation")
    fw = Fireworks(root, width=800, height=600)
    fw.pack(fill="both", expand=True)
    root.mainloop()
