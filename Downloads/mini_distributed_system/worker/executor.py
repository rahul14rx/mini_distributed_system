import subprocess
import os

def run_command(command: str):
    """
    Runs a shell command and returns the output (logs) and exit code.
    """
    print(f"⚡ Executing: {command}")
    
    try:
        # Run command, capture output (stdout) and errors (stderr)
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60 # Safety: Kill job if it takes > 60s
        )
        
        # Combine stdout and stderr
        logs = result.stdout + "\n" + result.stderr
        success = (result.returncode == 0)
        
        return success, logs

    except subprocess.TimeoutExpired:
        return False, "❌ Error: Job timed out (Limit: 60s)"
    except Exception as e:
        return False, f"❌ System Error: {str(e)}"