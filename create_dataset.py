import os
import subprocess

ROOT_DIR = 'datasets/KTH'
BASE_OUTPUT_DIR = 'KTH_slowed' 


SCALES_TO_PROCESS = [0.5, 0.75, 0.25]


print(f"Starting video processing for multiple scales...")
print(f"Source directory: {ROOT_DIR}")
print(f"Base output directory: {BASE_OUTPUT_DIR}")
print(f"Scales to be generated: {SCALES_TO_PROCESS}\n")

for subdir, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith('.avi'):
            input_path = os.path.join(subdir, file)
            print(f"Found source file: {input_path}")

            for scale in SCALES_TO_PROCESS:
                pts_multiplier = 1.0 / scale

                scale_folder_name = f"scale_{scale}"
                relative_subdir = os.path.relpath(subdir, ROOT_DIR)
                
              
                output_subdir = os.path.join(BASE_OUTPUT_DIR, scale_folder_name, relative_subdir)
                
                os.makedirs(output_subdir, exist_ok=True)
                
                output_path = os.path.join(output_subdir, file)

                print(f"  -> Processing for scale {scale}x (PTS multiplier: {pts_multiplier:.2f})")
                print(f"     Output: {output_path}")

                command = [
                    'ffmpeg',
                    '-i', input_path,
                    '-filter:v', f'setpts={pts_multiplier}*PTS',
                    '-an',       
                    '-y',        
                    output_path
                ]

                try:
                    subprocess.run(
                        command, 
                        check=True, 
                        capture_output=True, 
                        text=True
                    )
                except subprocess.CalledProcessError as e:
                    print(f"     ERROR processing {input_path} for scale {scale}!")
                    print(f"     FFmpeg stderr:\n{e.stderr}")
                except FileNotFoundError:
                    print("FATAL ERROR: 'ffmpeg' command not found.")
                    print("Please install FFmpeg and ensure it's in your system's PATH.")
                    exit()

            print("-" * 20) 

print("\nAll processing complete.")