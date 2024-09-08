import random
import os
import cv2
import time
import numpy as np

metalicset = '''          ~*=%#&^@oO0D8QMW█'''
#metalicset = '''█WMQ8D0O@&#%=o*^~           '''

ASCII_CHARS = metalicset

def lsd_webcamtoy():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Parameters for effect
    buffer_size = 10  # Number of frames to buffer for motion delay
    frame_buffer = []  # Buffer to store previous frames

    # Variables for color map and sharpening
    night_vision_map = None  # Initialize the night vision color map
    sharpness_factor =3.5  # Default sharpness factor
    blend_alpha = 2.0  # Default blend alpha factor

    # STATE VARIABLES
    alpha_ON        = 1 # usa a variavel blend_alpha como o brilho da imagem
    sharpness_ON    = 1 # filtro de sharpen
    nightvision_ON  = 1 # filtro da visão noturna
    lsd_effect_ON   = 1 # efeito lsd do webcamtoy
    invertaxis_ON   = 1 # inverte a orientação da webcam tipo se olhar no espelho sla

    def create_night_vision_map():
        lut = np.zeros((256, 1, 3), dtype=np.uint8)
        
        for i in range(256):
            lut[i] = (0, i, 0)  # Set red and blue channels to intensity, keep green at 0
            
        return lut

    def create_default_map():
        lut = np.zeros((256, 1, 3), dtype=np.uint8)
        
        for i in range(256):
            lut[i] = (i, i, i)  
            
        return lut

    def apply_sharpening(image, factor):
        kernel = np.array([[-1, -1, -1],
                        [-1, 9 * factor, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)



    # Create the night vision color map
    night_vision_map = create_night_vision_map()
    # Create the default color map
    default_map = create_default_map()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Add the current frame to the buffer
        frame_buffer.append(frame.copy())
        if len(frame_buffer) > buffer_size:
            frame_buffer.pop(0)


        if alpha_ON == 1:
            if lsd_effect_ON == 1:
                # Blend frames in the buffer
                blended_frame = np.zeros_like(frame, dtype=np.float32)
                alpha = blend_alpha / len(frame_buffer)
                for f in frame_buffer:
                    blended_frame += f * alpha
            else:
                blended_frame = frame
        else:
            if lsd_effect_ON == 1:
                # Blend frames in the buffer
                blended_frame = np.zeros_like(frame, dtype=np.float32)
                alpha = blend_alpha / len(frame_buffer)
                for f in frame_buffer:
                    blended_frame += f * alpha
            else:
                blended_frame = frame

        # Apply a color distortion effect (night vision)
        if nightvision_ON == 1:

            distorted_frame = cv2.convertScaleAbs(blended_frame)
            night_vision_frame = cv2.LUT(distorted_frame, night_vision_map)
        else:
            distorted_frame = cv2.convertScaleAbs(blended_frame)
            night_vision_frame = cv2.LUT(distorted_frame,default_map)

        # Apply sharpening
        if sharpness_ON == 1:
            sharpened_frame = apply_sharpening(night_vision_frame, sharpness_factor)
        else:
            sharpened_frame = night_vision_frame

        if invertaxis_ON == 1:
            flipped_image_vertical = cv2.flip(night_vision_frame, 1)
        else:
            flipped_image_vertical = night_vision_frame
        # Display the resulting frame
        cv2.imshow('Color Night Vision Effect', flipped_image_vertical)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


def resize_image(image, new_width=100):

    height, width = image.shape
    ratio = height / width / 2  # Adjust aspect ratio as needed
    new_height = int(new_width * ratio)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def grayscale_image(image):

    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def image_to_ascii(image):

    pixels = image.flatten()
    max_pixel_value = max(pixels)
    if max_pixel_value == 0:
        max_pixel_value = 1  # Avoid division by zero or infinity
    normalized_pixels = [int(pixel / max_pixel_value * (len(ASCII_CHARS) - 1)) for pixel in pixels]
    ascii_str = ''.join([ASCII_CHARS[pixel] for pixel in normalized_pixels])
    return ascii_str

def ascii_filter():
    # ASCII characters in descending order of density

    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray_image = grayscale_image(frame)
        resized_image = resize_image(gray_image)
        ascii_str = image_to_ascii(resized_image)
        
        img_width = resized_image.shape[1]
        ascii_img = "\n".join([ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)])
        
        print(ascii_img)
        
        # Clear the console
        print("\033c", end="")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
def draw_dripping_text(text):
    """Draws a dripping effect for the given text in ASCII art."""
    frames = 10  # Number of frames to animate
    
    for frame in range(frames):
        clear_screen()
        for line in text.splitlines():
            # Randomly replace characters with '~' to simulate dripping
            dripping_line = ''.join(char if char == ' ' or random.random() > 0.2 else '░' for char in line)
            print(dripping_line)
        
        time.sleep(0.1)  # Adjust the speed of animation by changing the sleep duration
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    
    tag = '''
 ██▒   █▓ ▄████▄   ▒█████   ███▄    █  ██░ ██ 
▓██░   █▒▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █ ▓██░ ██▒
 ▓██  █▒░▒▓█    ▄ ▒██░  ██▒▓██  ▀█ ██▒▒██▀▀██░
  ▒██ █░░▒▓▓▄ ▄██▒▒██   ██░▓██▒  ▐▌██▒░▓█ ░██ 
   ▒▀█░  ▒ ▓███▀ ░░ ████▓▒░▒██░   ▓██░░▓█▒░██▓
   ░ ▐░  ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒  ▒ ░░▒░▒
   ░ ░░    ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒░ ▒ ░▒░ ░
     ░░  ░        ░ ░ ░ ▒     ░   ░ ░  ░  ░░ ░
      ░  ░ ░          ░ ░           ░  ░  ░  ░
     ░   ░                                    
    '''
    while True:
        os.system("clear")
        print(tag)
        draw_dripping_text(tag)
        print()
        print("1 = Filtro lsd do webcamtoy com cor de visao noturna")
        print("2 = Filtro ascii")
        print("Para parar o filtro ascii vc aperta cntrl+c e para parar a visao noturna apenas aperque 'q'.")
        selec_filtro = input('Que filtro deseja usar (1/2) >')
    
        if int(selec_filtro) == 1:
            lsd_webcamtoy()
        elif int(selec_filtro) == 2:
            ascii_filter()
