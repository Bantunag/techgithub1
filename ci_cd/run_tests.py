import subprocess

def run_tests():
    subprocess.run(["pytest", "tests/"], check=True)

if __name__ == "__main__":
    run_tests()
