import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class GUI:
    def __init__(self, root):
        self.root = root
        self.video = None
        self.paused = False
        self.frame_count = 0
        self.current_frame = 0
        self.photo = None

        self.canvas_width = 640
        self.canvas_height = 480

        self.btn_open_video = tk.Button(root, text="영상 찾기", command=self.open_video)
        self.btn_open_video.pack(pady=10)

        self.btn_play_pause = tk.Button(root, text="재생/일시정지", command=self.play_pause)
        self.btn_play_pause.pack(pady=10)

        self.label_frame = tk.Label(root, text="시점(frame): ")
        self.label_frame.pack(pady=10)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

    def open_video(self):
        self.video_path = filedialog.askopenfilename(title="영상 선택", filetypes=(("Video files", "*.mp4"), ("All files", "*.*")))
        self.play_video()

    def play_video(self):
        self.video = cv2.VideoCapture(self.video_path)  # 선택한 영상 로드
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))  # 전체 프레임 수 가져오기
        self.play_frame()

    def play_frame(self):
        if not self.paused:
            ret, frame = self.video.read()  # 프레임 읽기
            if not ret:
                self.video.release()
                self.label_frame.config(text="시점(frame): ")  # 레이블 초기화
                return

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV의 BGR 형식을 RGB로 변환
            image = Image.fromarray(frame)  # 이미지 객체로 변환

            # 영상의 크기를 GUI의 크기에 맞게 조정
            resized_image = image.resize((self.canvas_width, self.canvas_height))

            self.photo = ImageTk.PhotoImage(resized_image)  # Tkinter에서 사용할 수 있는 형식으로 변환
            self.canvas.delete("all")  # 기존 캔버스 삭제
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)  # 캔버스에 이미지 추가

            self.current_frame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))  # 현재 프레임 가져오기
            self.label_frame.config(text="시점(frame): {}".format(self.current_frame))  # 레이블에 시점(frame) 출력

        self.root.after(10, self.play_frame)  # 10ms 후에 play_frame 함수를 다시 호출하여 연속적으로 프레임을 업데이트

    def play_pause(self):
        self.paused = not self.paused

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x600")  # GUI 크기를 가로 640, 세로 600으로 고정
    gui = GUI(root)
    root.mainloop()
