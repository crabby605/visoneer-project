import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageSaver:
    def __init__(self, root):
        self.root = root
        self.root.title("click image for auto lock")
        self.cap = cv2.VideoCapture(0)
        self.label = tk.Label(root)
        self.label.pack()
        self.capture_button = tk.Button(root, text="capture", command=self.capture_image)
        self.capture_button.pack(pady=20)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.root.after(10, self.update_frame)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite("known_face.jpg", frame)
            messagebox.showinfo("success", "image captured and saved as known_face.jpg")
            self.captured_image(frame)
        else:
            messagebox.showerror("error", "failed to capture image")

    def captured_image(self, frame):
        window = tk.Toplevel()
        window.title("captured Image")
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label = tk.Label(window, image=imgtk)
        label.image = imgtk
        label.pack()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = ImageSaver(root)
    root.mainloop()

if __name__ == "__main__":
    main()