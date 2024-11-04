import tkinter as tk
from tkinter import Button, Entry, Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import time
import random

class PolyhedronViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Painter's Algorithm")

        self.fig = plt.Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect([1, 1, 1])

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Z")
        self.ax.set_zlabel("Y")

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label = Label(root, text="Количество случайных кубов:")
        self.label.pack(side=tk.LEFT)
        self.cube_count_entry = Entry(root)
        self.cube_count_entry.pack(side=tk.LEFT)

        self.sort_button = Button(root, text="Отрисовка", command=self.render_sorted_faces)
        self.sort_button.pack(side=tk.LEFT)

        self.initial_polyhedra = [
            np.array([[-1, -1, -1], [1, -1, -1], [1, -1, 1], [-1, -1, 1], [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1]]),
            np.array([[0, -2, 0], [1, -2, 0], [1, -2, 1], [0, -2, 1], [0, -3, 0], [1, -3, 0], [1, -3, 1], [0, -3, 1]])
        ]

        self.polyhedra = list(self.initial_polyhedra)
        self.faces = [
            [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]],
            [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]]
        ]

        self.first_run = True

    def calculate_face_center(self, polyhedron, face):
        vertices = polyhedron[face]
        center = vertices.mean(axis=0)
        return center[1]

    def generate_random_cubes(self, count):
        self.polyhedra = []
        self.faces = []
        for _ in range(count):
            size = random.uniform(0.5, 1.5)
            x, y, z = random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2)
            cube = np.array([
                [x - size, y - size, z - size],
                [x + size, y - size, z - size],
                [x + size, y - size, z + size],
                [x - size, y - size, z + size],
                [x - size, y + size, z - size],
                [x + size, y + size, z - size],
                [x + size, y + size, z + size],
                [x - size, y + size, z + size]
            ])
            self.polyhedra.append(cube)
            self.faces.append([[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 3, 7, 4], [1, 2, 6, 5]])

    def render_sorted_faces(self):
        self.ax.cla()
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Z")
        self.ax.set_zlabel("Y")

        if self.first_run:
            self.first_run = False
        else:
            try:
                count = int(self.cube_count_entry.get())
                if count > 0:
                    self.generate_random_cubes(count)
            except ValueError:
                print("Введите корректное число кубов")

        faces_with_depth = []
        for polyhedron, face_set in zip(self.polyhedra, self.faces):
            for face in face_set:
                y_center = self.calculate_face_center(polyhedron, face)
                faces_with_depth.append((y_center, polyhedron[face]))

        faces_with_depth.sort(key=lambda item: item[0], reverse=True)

        for y_center, vertices in faces_with_depth:
            face = Poly3DCollection([vertices], color="grey", edgecolor="k", alpha=1.0)
            self.ax.add_collection3d(face)
            self.canvas.draw()
            self.root.update()
            time.sleep(0.3)

        self.ax.set_xlim([-3, 3])
        self.ax.set_ylim([-3, 3])
        self.ax.set_zlim([-3, 3])
        self.canvas.draw()

root = tk.Tk()
app = PolyhedronViewer(root)
root.mainloop()
