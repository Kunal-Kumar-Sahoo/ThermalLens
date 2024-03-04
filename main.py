import cv2
import numpy as np
from skimage.measure import label, regionprops
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
import argparse

def find_connected_components(video_path, frequency_range=(0, 1), threshold=100, fps=30):
    """
    Finds 4-connected components in a thermal camera video within a specified frequency range.

    Parameters:
    - video_path (str): Path to the thermal camera footage in .mp4 format.
    - frequency_range (tuple): Frequency range in Hz, within which to detect components.
    - threshold (int): Threshold for binary image segmentation.
    - fps (int): Frames per second of the video.

    Returns:
    - List of lists: Each inner list contains the connected components for a frame.
    """

    cap = cv2.VideoCapture(video_path)

    connected_components = []

    ret, frame = cap.read()

    while ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blurred = gaussian_filter(gray, sigma=1.5)

        _, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

        labeled_image, num_features = label(thresh, connectivity=1, return_num=True)

        # Filter connected components based on frequency range
        components_within_range = []
        for region in regionprops(labeled_image):
            frequency = region.equivalent_diameter / fps
            if frequency_range[0] <= frequency <= frequency_range[1]:
                components_within_range.append(region)

        connected_components.append(components_within_range)

        # Draw bounding boxes around connected components
        for region in components_within_range:
            minr, minc, maxr, maxc = region.bbox
            cv2.rectangle(frame, (minc, minr), (maxc, maxr), (0, 255, 0), 2)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        ret, frame = cap.read()

    cap.release()

    return connected_components

def find_frequency_peaks(connected_components, fps):
    """
    Finds frequency peaks in the connected components data.

    Parameters:
    - connected_components (list): List of lists containing connected components for each frame.
    - fps (int): Frames per second of the video.

    Returns:
    - numpy.ndarray: Array containing the frequencies of the peaks.
    """

    total_frames = len(connected_components)

    frequency_range = np.arange(1, fps / 2 + 1, 1)

    frequency_counts = np.zeros(len(frequency_range))

    for frame_components in connected_components:
        frequency_counts[len(frame_components)] += 1

    peaks, _ = find_peaks(frequency_counts, height=(None, None))

    frequencies = frequency_range[peaks]

    return frequencies

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect connected components in a thermal camera video.')
    parser.add_argument('video_path', type=str, help='Path to the thermal camera footage in .mp4 format')
    parser.add_argument('--frequency_range', nargs=2, type=float, default=[0, 1], help='Frequency range in Hz (e.g., 0 1)')
    args = parser.parse_args()

    frequency_range = tuple(args.frequency_range)

    fps = 30

    threshold = 100

    connected_components = find_connected_components(args.video_path, frequency_range, threshold, fps)

    frequencies = find_frequency_peaks(connected_components, fps)

    print("Frequency peaks (Hz):", frequencies)