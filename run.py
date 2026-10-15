"""One-command setup and launch for Windows, macOS and Linux."""
import argparse
from pathlib import Path
import subprocess
import sys
import threading
import venv
import webbrowser

ROOT = Path(__file__).resolve().parent


def main():
    if sys.version_info < (3, 10):
        raise SystemExit('Please install Python 3.10 or newer (3.12 or 3.13 recommended).')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--setup-only', action='store_true')
    args = parser.parse_args()
    environment = ROOT / '.venv'
    python = environment / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    if not python.exists():
        print('Creating a project virtual environment...', flush=True)
        venv.EnvBuilder(with_pip=True).create(environment)
    requirements = ROOT / 'requirements.txt'
    stamp = environment / '.requirements-installed'
    if not stamp.exists() or stamp.read_bytes() != requirements.read_bytes():
        print('Installing project dependencies (internet needed on first run)...', flush=True)
        subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(requirements)], check=True)
        stamp.write_bytes(requirements.read_bytes())
    if args.setup_only:
        print('Setup complete.')
        return
    # Import the server inside the project's interpreter, without nested child processes.
    code = "import sys; sys.path.insert(0, sys.argv.pop(1)); import dashboard; dashboard.main()"
    if not args.no_browser:
        threading.Timer(1.5, lambda: webbrowser.open(f'http://127.0.0.1:{args.port}')).start()
    try:
        subprocess.run([str(python), '-c', code, str(ROOT), '--port', str(args.port)], check=True)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f'Could not start: {exc}\nCheck Python, internet access and the selected port.')
