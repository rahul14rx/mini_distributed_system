import time
import requests
import sys
import os
from .config import API_URL, WORKER_ID, HOSTNAME
from .executor import run_command

def register():
    """Tell the server we exist."""
    print(f"👋 Registering Worker: {WORKER_ID} ({HOSTNAME})")
    try:
        requests.post(f"{API_URL}/workers/register", json={
            "id": WORKER_ID,
            "hostname": HOSTNAME
        })
        print("✅ Registered successfully!")
    except Exception as e:
        print(f"❌ Could not register: {e}")
        sys.exit(1) 

def poll_for_work():
    """Ask for a job and execute it."""
    try:
        # 1. Ask for a job
        response = requests.post(f"{API_URL}/jobs/poll", params={"worker_id": WORKER_ID})
        
        if response.status_code == 200:
            job = response.json()
            print(f"🚀 Received Job #{job['id']}: {job['command']}")
            
            # 2. Run the job
            is_success, logs = run_command(job['command'])
            status = "SUCCESS" if is_success else "FAILED"
            
            # --- NEW: ARTIFACT UPLOAD LOGIC ---
            # If the user created a file named 'output.txt', we upload it.
            artifact_file = "output.txt"
            if os.path.exists(artifact_file):
                print(f"📦 Found artifact '{artifact_file}', uploading...")
                with open(artifact_file, "rb") as f:
                    files = {'file': (artifact_file, f, 'text/plain')}
                    upload_res = requests.post(f"{API_URL}/jobs/{job['id']}/upload", files=files)
                    print(f"✅ Upload Status: {upload_res.status_code}")
                
                # Clean up local file
                os.remove(artifact_file)
            # ----------------------------------

            # 3. Report back completion
            print(f"📤 Reporting Job #{job['id']} as {status}...")
            requests.put(f"{API_URL}/jobs/{job['id']}/complete", params={
                "status": status,
                "log_path": logs 
            })
            print("Done.")
            
        else:
            pass # No jobs

    except requests.exceptions.ConnectionError:
        print("⚠️ Server down? Retrying...")
    except Exception as e:
        print(f"❌ Error: {e}")

def heartbeat():
    try:
        requests.post(f"{API_URL}/workers/heartbeat", json={
            "id": WORKER_ID,
            "status": "IDLE"
        })
    except:
        pass

if __name__ == "__main__":
    register()
    while True:
        poll_for_work()
        heartbeat()
        time.sleep(2)