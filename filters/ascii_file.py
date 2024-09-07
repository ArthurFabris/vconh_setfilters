import cv2
import time
fps = 1/60
metalicset = '''█WMQ8D0O@&#%=o*^~           '''
ascii_char_list = " `'\"-^_:,.~+<>!*il=\\{}[]7?rt1()c/vzxunJYTI3fjLCAoZayXU2Ve5s4wbEd9S8FhPGKpOqkdNHmMBWQ#R0%g$D&6@"


ASCII_CHARS = metalicset



def resize_image(image, new_width=500):
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

def ascii_filter(video_path):
    cap = cv2.VideoCapture(video_path)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart the video
            continue
        
        gray_image = grayscale_image(frame)
        resized_image = resize_image(gray_image)
        ascii_str = image_to_ascii(resized_image)
        
        img_width = resized_image.shape[1]
        ascii_img = "\n".join([ascii_str[i:(i + img_width)] for i in range(0, len(ascii_str), img_width)])
        
        print(f"\033[1;32;40m {ascii_img}")
        time.sleep(fps)
        
        # Clear the console
        print("\033c", end="")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Call the function with the path to your video file
ascii_filter('VCONHTAG_L.mp4')



def main():
    ascii_filter('VCONHTAG_L.mp4')


if __name__ == "__main__":
    main()
