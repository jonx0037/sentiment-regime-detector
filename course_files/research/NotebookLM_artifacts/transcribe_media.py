import os
import sys
import whisper
import torch
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def print_flushed(msg):
    print(msg, flush=True)

def get_device():
    if torch.cuda.is_available():
        return "cuda"
    elif torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

def transcribe_directory(directory=".", model_size="turbo"):
    device = get_device()
    print_flushed(f"Loading Whisper model '{model_size}' on device: {device}...")
    
    try:
        model = whisper.load_model(model_size, device=device)
    except Exception as e:
        print_flushed(f"Error loading model on {device}: {e}")
        print_flushed("Falling back to CPU...")
        model = whisper.load_model(model_size, device="cpu")

    supported_extensions = ('.mp4', '.m4a', '.mp3', '.wav')
    files = [f for f in os.listdir(directory) if f.lower().endswith(supported_extensions)]
    
    if not files:
        print_flushed("No media files found to transcribe.")
        return

    print_flushed(f"Found {len(files)} media files.")

    report = {
        "processed": [],
        "renamed": [],
        "skipped": [],
        "errors": []
    }

    import re
    timestamp_pattern = re.compile(r"\[\d{2}:\d{2}\]")

    for i, filename in enumerate(files):
        file_path = os.path.join(directory, filename)
        base_name = os.path.splitext(filename)[0]
        
        # Define old and new output filenames
        old_output_filename = f"{base_name}.md"
        new_output_filename = f"{base_name}_transcript.md"
        
        old_output_path = os.path.join(directory, old_output_filename)
        new_output_path = os.path.join(directory, new_output_filename)

        should_transcribe = True

        # Check if new style file exists
        if os.path.exists(new_output_path):
            with open(new_output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if timestamp_pattern.search(content):
                    print_flushed(f"[{i+1}/{len(files)}] Skipping {filename} (Valid transcript exists: {new_output_filename})")
                    report["skipped"].append(filename)
                    should_transcribe = False
                else:
                    print_flushed(f"[{i+1}/{len(files)}] Re-transcribing {filename} (Existing transcript missing timestamps)")
        
        # Check if old style file exists and we haven't decided to skip yet
        elif os.path.exists(old_output_path):
            with open(old_output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if timestamp_pattern.search(content):
                # Old file has timestamps, just rename it
                try:
                    os.rename(old_output_path, new_output_path)
                    print_flushed(f"[{i+1}/{len(files)}] Renamed {old_output_filename} -> {new_output_filename}")
                    report["renamed"].append(filename)
                    should_transcribe = False
                except OSError as e:
                     print_flushed(f"   -> Error renaming {old_output_filename}: {e}")
                     report["errors"].append(f"{filename} (Rename failed)")
            else:
                # Old file lacks timestamps, remove it and let transcription happen
                print_flushed(f"[{i+1}/{len(files)}] Removing old transcript {old_output_filename} (Missing timestamps)")
                try:
                    os.remove(old_output_path)
                except OSError as e:
                    print_flushed(f"   -> Warning: Could not remove {old_output_filename}: {e}")

        if should_transcribe:
            print_flushed(f"[{i+1}/{len(files)}] Transcribing {filename}...")
            
            try:
                result = model.transcribe(file_path, verbose=False)
                
                with open(new_output_path, "w", encoding="utf-8") as f:
                    f.write(f"# Transcript: {filename}\n\n")
                    for segment in result['segments']:
                        start = segment['start']
                        start_min = int(start // 60)
                        start_sec = int(start % 60)
                        timestamp = f"[{start_min:02d}:{start_sec:02d}]"
                        text = segment['text'].strip()
                        f.write(f"{timestamp} {text}\n")
                
                # Verify integrity
                if os.path.exists(new_output_path) and os.path.getsize(new_output_path) > 0:
                    print_flushed(f"   -> Saved to {new_output_filename}")
                    report["processed"].append(filename)
                else:
                     print_flushed(f"   -> Error: Output file empty or missing for {filename}")
                     report["errors"].append(f"{filename} (File creation failed)")
                
            except Exception as e:
                print_flushed(f"   -> Error transcribing {filename}: {e}")
                report["errors"].append(f"{filename} ({str(e)})")

    # Summary Report
    print_flushed("\n" + "="*40)
    print_flushed("       TRANSCRIPTION SUMMARY")
    print_flushed("="*40)
    print_flushed(f"Total Files Found: {len(files)}")
    print_flushed(f"Processed (New):   {len(report['processed'])}")
    print_flushed(f"Renamed (kept):    {len(report['renamed'])}")
    print_flushed(f"Skipped (Already Done): {len(report['skipped'])}")
    print_flushed(f"Errors:            {len(report['errors'])}")
    
    if report['errors']:
        print_flushed("\nError Details:")
        for err in report['errors']:
            print_flushed(f" - {err}")
    print_flushed("="*40 + "\n")

if __name__ == "__main__":
    print_flushed("Script starting...")
    transcribe_directory()
