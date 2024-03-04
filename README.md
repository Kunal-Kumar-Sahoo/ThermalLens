# Thermal Camera Connected Component Detection

## Overview

This project aims to detect 4-connected components in thermal camera footage within a specified frequency range. It utilizes computer vision techniques to process the video frames, identify connected components, and filter them based on their frequency characteristics.

## Algorithm

The algorithm consists of the following steps:

1. **Video Processing**: Read the thermal camera footage frame by frame.

2. **Image Processing**: Convert each frame to grayscale, apply Gaussian blur to reduce noise, and threshold the image to create a binary representation.

3. **Connected Component Labeling**: Label connected components in the binary image using 4-connectivity. This step identifies regions of pixels that are connected to each other.

4. **Frequency Filtering**: Calculate the frequency of each connected component based on its equivalent diameter and the frame rate of the video. Filter out the connected components that fall within the specified frequency range.

5. **Visualization**: Draw bounding boxes around the filtered connected components on the original video frames.

6. **Display**: Display the processed frames with the detected connected components.

## Working of the Code

The code is written in Python and utilizes the OpenCV, scikit-image, and NumPy libraries.

1. **find_connected_components(video_path, frequency_range, threshold, fps)**:
   - Reads the thermal camera video and processes each frame to identify 4-connected components within the specified frequency range.
   - Returns a list of lists, where each inner list contains the connected components for a frame.

2. **find_frequency_peaks(connected_components, fps)**:
   - Analyzes the connected components data to find frequency peaks.
   - Returns an array containing the frequencies of the peaks.

3. **Main Script**:
   - Parses command-line arguments to specify the video path and frequency range.
   - Calls the above functions to detect connected components and frequency peaks.
   - Displays the frequency peaks.

## How to Run

To run the code, follow these steps:

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/your_username/thermal-camera-connected-component-detection.git
   ```

2. Navigate to the project directory:

   ```
   cd thermal-camera-connected-component-detection
   ```

3. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

4. Run the script:

   ```
   python script.py video_path.mp4 --frequency_range 0 1
   ```

   Replace `video_path.mp4` with the path to your thermal camera footage and adjust the frequency range as needed.