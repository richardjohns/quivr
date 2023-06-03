import os
import subprocess
from time import sleep


def start_project():
    print("Welcome to Quivr!")
    print("Options:")
    print("1. Start the app without logging (default)")
    print("2. Start the app with logging")

    user_choice = input("Please enter your choice (1-2): ")
    if user_choice not in ['1', '2']:
        print("Invalid option selected. Starting the app without logging.")
    
    # Change directory to project
    os.chdir('/Users/richardjohns/projects/ai/quivr')

    # Start backend
    print("Starting backend...")
    backend_cmd = ['uvicorn', 'api:app', '--reload', '--host', '0.0.0.0', '--port', '5050']
    if user_choice == '2':
        with open("logs/backend.log", "w") as outfile:
            backend_process = subprocess.Popen(backend_cmd, cwd='backend', stdout=outfile)
    else:
        backend_process = subprocess.Popen(backend_cmd, cwd='backend')
    sleep(5)  # Allow backend to start

    # Start frontend
    print("Starting frontend...")
    frontend_cmd = ['yarn', 'dev']
    if user_choice == '2':
        with open("logs/frontend.log", "w") as outfile:
            frontend_process = subprocess.Popen(frontend_cmd, cwd='frontend', stdout=outfile)
    else:
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
