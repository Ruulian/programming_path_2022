FILE_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/
PORT=16777

/bin/chmod +x ${FILE_PATH}app.py
${FILE_PATH}app.py ${PORT} > /dev/null 2>&1 &