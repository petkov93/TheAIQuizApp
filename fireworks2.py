import tkinter as tk
import random
import math

class Fireworks(tk.Canvas):
    def __init__(self, master, width=600, height=600, **kwargs):
        super().__init__(master, width=width, height=height, bg='black', highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.rockets = []
        self.particles = []
        self.after(500, self.launch_rocket)

    def launch_rocket(self):
        # Rocket starts at bottom, shoots upward
        x = random.randint(100, self.width - 100)
        y = self.height
        target_y = random.randint(self.height // 3, self.height // 2)
        color = random.choice(["red", "orange", "yellow", "white", "cyan", "purple", "pink", "green"])
        rocket = {"x": x, "y": y, "target_y": target_y, "color": color, "exploded": False}
        self.rockets.append(rocket)
        self.animate()
        self.after(random.randint(800, 1500), self.launch_rocket)

    def explode(self, rocket):
        num_particles = random.randint(50, 100)
        color = rocket["color"]
        x = rocket["x"]
        y = rocket["y"]
        for i in range(num_particles):
            angle = (2 * math.pi / num_particles) * i
            speed = random.uniform(3, 7)
            dx = math.cos(angle) * speed * random.uniform(0.5, 1.5)
            dy = math.sin(angle) * speed * random.uniform(0.5, 1.5)
            life = random.randint(50, 100)
            self.particles.append({
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "life": life,
                "color": color,
                "size": random.randint(2, 5),
                "secondary_explosion": life > 40 and random.random() < 0.15
            })

    def animate(self):
        self.delete("all")

        # Animate rockets (shooting up)
        new_rockets = []
        for rocket in self.rockets:
            if not rocket["exploded"]:
                rocket["y"] -= 10  # speed upward
                # Draw rocket as small circle
                self.create_oval(rocket["x"]-3, rocket["y"]-3, rocket["x"]+3, rocket["y"]+3, fill=rocket["color"], outline="")
                if rocket["y"] <= rocket["target_y"]:
                    rocket["exploded"] = True
                    self.explode(rocket)
                else:
                    new_rockets.append(rocket)
        self.rockets = new_rockets

        # Animate particles (explosion)
        new_particles = []
        for p in self.particles:
            if p["life"] > 0:
                p["x"] += p["dx"]
                p["y"] += p["dy"]
                p["dy"] += 0.15  # gravity
                p["life"] -= 1
                size = max(1, p["size"] * (p["life"] / 50))
                alpha = int(255 * (p["life"] / 50))
                color = p["color"]
                # Draw particle
                self.create_oval(p["x"], p["y"], p["x"]+size, p["y"]+size, fill=color, outline="")

                # Secondary explosion triggers when life halfway done
                if p["secondary_explosion"] and p["life"] == int(p["life"] / 2):
                    self.secondary_explode(p)

                new_particles.append(p)
        self.particles = new_particles

        # Continue animation if there are rockets or particles
        if self.rockets or self.particles:
            self.after(30, self.animate)

    def secondary_explode(self, parent_particle):
        num_particles = random.randint(5, 10)
        x = parent_particle["x"]
        y = parent_particle["y"]
        color = parent_particle["color"]
        for i in range(num_particles):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(1, 3)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            life = random.randint(10, 20)
            self.particles.append({
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "life": life,
                "color": color,
                "size": random.randint(1, 3),
                "secondary_explosion": False
            })

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Multi-Stage Fireworks")
    fw = Fireworks(root)
    fw.pack(fill="both", expand=True)
    root.mainloop()
