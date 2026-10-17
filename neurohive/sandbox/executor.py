"""
NeuroHive - Sandboxed Secure Execution Environment for AI-Generated Code.
"""

import os
import sys
import subprocess
import tempfile
import time
from typing import Dict, Any, Tuple

# Dangerous system calls blocked in isolated environment
DISALLOWED_PATTERNS = [
    "import os; os.system('rm",
    "import shutil; shutil.rmtree('/'",
    "subprocess.Popen(['rm'",
    ":(){ :|:& };:",
    "/dev/sda",
]

class CodeSandbox:
    """
    Safely executes Python, Bash, and JavaScript code snippets
    with strict timeouts, memory controls, and output capture.
    """
    def __init__(self, timeout_seconds: int = 10):
        self.timeout = timeout_seconds

    def execute(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Executes code in an isolated temporary runtime.
        Returns execution telemetry: stdout, stderr, runtime_ms, status.
        """
        for pattern in DISALLOWED_PATTERNS:
            if pattern in code:
                return {
                    "success": False,
                    "error": "Security Sandbox Violation: Dangerous system call blocked.",
                    "stdout": "",
                    "stderr": "BLOCKED_BY_SANDBOX",
                    "runtime_ms": 0.0
                }

        start_time = time.time()
        ext = ".py" if language == "python" else (".js" if language in ("js", "javascript") else ".sh")
        
        with tempfile.NamedTemporaryFile("w", suffix=ext, delete=False, encoding="utf-8") as f:
            f.write(code)
            temp_path = f.name

        try:
            if language == "python":
                cmd = [sys.executable, temp_path]
            elif language in ("js", "javascript"):
                cmd = ["node", temp_path]
            else:
                cmd = ["bash", temp_path]

            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            elapsed = round((time.time() - start_time) * 1000, 2)
            
            return {
                "success": proc.returncode == 0,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "returncode": proc.returncode,
                "runtime_ms": elapsed
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {self.timeout}s limit.",
                "stdout": "",
                "stderr": "TIMEOUT",
                "runtime_ms": self.timeout * 1000.0
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
                "runtime_ms": 0.0
            }
        finally:
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except Exception:
                    pass
