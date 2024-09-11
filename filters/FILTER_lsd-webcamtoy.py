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