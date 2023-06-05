import os
import subprocess
from time import sleep


def start_project():
    print("Welcome to Quivr! Press Enter to start.")
    input()  # Wait for user to press Enter

    # Change directory to project
    os.chdir('/Users/richardjohns/projects/ai/quivr')

    # Start backend
    print("Starting backend...")
    backend_cmd = ['uvicorn', 'api:app', '--reload', '--host', '0.0.0.0', '--port', '5050']
    backend_process = subprocess.Popen(backend_cmd, cwd='backend')
    sleep(5)  # Allow backend to start

    # Start frontend
    print("Starting frontend...")
    frontend_cmd = ['yarn', 'dev']
    frontend_process = subprocess.Popen(frontend_cmd, cwd='frontend')
    
    try:
        # Open browser
        print("Opening browser...")
        import webbrowser
        webbrowser.open('http://localhost:3000/upload')
        webbrowser.open('http://localhost:3000/chat')

        # Wait for processes to complete
        print("Applications are running...")
        backend_process.wait()
        frontend_process.wait()

    except KeyboardInterrupt:
        print("\nThanks for using Quivr - goodbye!")
        backend_process.terminate()
        frontend_process.terminate()


if __name__ == '__main__':
    start_project()
