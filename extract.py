import cv2
import os
import subprocess

video_path = "videoplayback.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    result = "Video couldn't be opened!"
else:
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    fps = cap.get(cv2.CAP_PROP_FPS)  
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  
    print(f"FPS: {fps}")
    print(f"Gesamtanzahl der Frames: {total_frames}")

    audio_output = "audio_output.mp3"
    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', audio_output], check=True)
        print(f"Audio extracted successfully: {audio_output}")
    except subprocess.CalledProcessError as e:
        print(f"Error while extraxting audio track: {e}")

    frames = []
    extracted = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = os.path.join(output_dir, f"frame_{extracted:03d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frames.append(frame_filename)
        extracted += 1

        print(f"Frame {extracted}/{total_frames} safed as {frame_filename}")

    cap.release()
    
    result = frames
    print(f"Successfully extracted frames: {extracted}/{total_frames}")

print(f"All Frames: {len(frames)}")
