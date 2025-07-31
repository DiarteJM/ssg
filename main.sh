chmod +x main.sh
echo "Running main.py..."
cd "$(dirname "$0")" # Go to directory containing this script
PYTHONPATH=$(pwd) python3 -c "from src.main import copy_static_to_public; copy_static_to_public()"
cd public && python3 -m http.server 8888