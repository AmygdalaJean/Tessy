import cv2
# import pytesseract
import pandas as pd
# from pytesseract import Output
from PIL import Image

# Set the path to the tesseract executable
# Uncomment and set the path if Tesseract is not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

# Function to extract frames and perform OCR
def extract_numbers(video_path, interval):
    # Load the video
    cap = cv2.VideoCapture(video_path)

    frame_count = 1 # changed from 0 to 1 to start frame count at 1
    data = []
    while cap.isOpened():
        readOK, frame = cap.read(0)     # reads next available frame
        if not readOK:
            print("Reading frame ", frame_count, " failed.")
            break
        # Process frames at the specified interval
        if frame_count % interval == 0:
            height_max = len(frame[0,:])
            width_max = len(frame[0,:])
            offset_vert = -300
            offset_horiz = 0
            midline_horiz = round(width_max/2)
            midline_vert = round(height_max/2)
            width = 450
            height = 400
            crop_left = midline_horiz + offset_horiz
            crop_top = midline_vert + offset_vert
            frame_cropped = frame[crop_top:crop_top+height, crop_left:crop_left+width]

            # Optional: Convert frame to grayscale
            frame_gray = cv2.cvtColor(frame_cropped, cv2.COLOR_RGB2GRAY)  # flir videos use RGB (ITU-R B.709) according to VLC media player

            alpha = 1.5 # Contrast control (1.0-3.0)
            beta = 0 # Brightness control (0-100)

            #frame_adjusted = cv2.convertScaleAbs(frame_gray, alpha=alpha, beta=beta)
            adjOK, frame_adjusted = cv2.threshold(frame_gray, 240,255,cv2.THRESH_BINARY_INV)

            cv2.imshow('original', frame_cropped)
            cv2.imshow('Modified Frame', frame_adjusted)
            cv2.waitKey(0)  # wait an indefinite time for a user keystroke

            #convert OpenCV image to PIL image data format
            frame_pil = Image.fromarray(frame_adjusted)

            #frame_pil.show()

            # Use Tesseract to extract numbers
            custom_config = r'--oem 3 --psm 12 outputbase digits' # changed PSM from 6
            # ok results for 11, 12, 4
            # https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/
            # d = pytesseract.image_to_data(frame_pil, config=custom_config, output_type=Output.DICT)

            # Filter out numeric texts
            # n_boxes = len(d['text'])
            # for i in range(n_boxes):
            #     if d['text'][i].isdigit():
            #         data.append((frame_count, d['text'][i]))
            # data.append((frame_count, d['text']))

        frame_count += 1

    cap.release()
    return data

video_path = 'FLIR_20220504_101905.mp4'
# Path to your video file
results = extract_numbers(video_path, 10)

# Create a DataFrame and save to Excel
df = pd.DataFrame(results, columns=['Frame', 'Number'])
df.to_excel('extracted_numbers.xlsx', index=False)

print("Data extracted and saved to spreadsheet.")
