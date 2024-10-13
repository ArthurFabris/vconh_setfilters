import cv2
import time
import os
metalicset_inverse = '''█WMQ8D0O@&#%=o*^~           '''
metalicset =         '''           ~*=%#&^@oO0D8QMW█'''
class AsciiFilter:
    def __init__(self, fps=1/60, ascii_chars=None):
        self.fps = fps
        self.ascii_frames_dict = {}
        self.frame_count = 0
        self.ascii_chars = ascii_chars if ascii_chars else f"{metalicset_inverse}"
    
    def list_accepted_files(self, file_pool):
        accepted_extensions = ('.mp4', '.jpg', '.jpeg', '.png')
        file_list = [file for file in os.listdir(file_pool) if file.lower().endswith(accepted_extensions)]
    
        for index, file in enumerate(file_list):
            print(f"{index + 1}: {file}")
        
        return file_list

    def resize_image(self, image, new_width):
        height, width = image.shape
        ratio = width / height  
        new_height = int(new_width / ratio) 
        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image


    def grayscale_image(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def image_to_ascii(self, image):
        pixels = image.flatten()
        max_pixel_value = max(pixels)
        if max_pixel_value == 0:
            max_pixel_value = 1 # nao podemos dividir por 0
        normalized_pixels = [int(pixel / max_pixel_value * (len(self.ascii_chars) - 1)) for pixel in pixels]
        
        ascii_str = ''.join([self.ascii_chars[pixel] for pixel in normalized_pixels])
        
        img_width = image.shape[1]
        ascii_lines = [ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)]
        
        return ascii_lines

    def process_frame(self, frame,new_width):
        gray_image = self.grayscale_image(frame)
        resized_image = self.resize_image(gray_image, new_width)
        ascii_lines = self.image_to_ascii(resized_image)
        
        self.ascii_frames_dict[self.frame_count] = ascii_lines
        self.frame_count += 1
        
        ascii_img = "\n".join(ascii_lines)

    def ascii_filter(self, video_path,new_width):
        cap = cv2.VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
                break
            else:
                self.process_frame(frame,new_width)

        cap.release()
        cv2.destroyAllWindows()
    
    def get_ascii_frames(self):
        return self.ascii_frames_dict

def main():
    path = os.getcwd()  
    file_pool = f"{path}/file-pool/"
    
   
    converter = AsciiFilter()

    accepted_files = converter.list_accepted_files(file_pool)

    print("Escolha o numero do arquivo na lista de arquivos ou digite o caminho inteiro do arquivo.\n")
    user_input = input("> ")

    try:
        file_index = int(user_input) - 1
        if 0 <= file_index < len(accepted_files):
            selected_file = os.path.join(file_pool, accepted_files[file_index])
            print(f"Selected file: {selected_file}")
            converter.ascii_filter(selected_file)
            print("ASCII frames stored in dictionary.")
            print(converter.get_ascii_frames())
        else:
            print("Invalid file number.")
    except ValueError:
        if os.path.isfile(user_input):
            print(f"Selected file: {user_input}")
            converter.ascii_filter(user_input)
            print("ASCII frames stored in dictionary.")
        else:
            print("Invalid file path.")

if __name__ == "__main__":
    main()
