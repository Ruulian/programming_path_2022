FILE_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/
PORT=16770

/bin/chmod +x ${FILE_PATH}app.py
/usr/bin/socat TCP-LISTEN:${PORT},fork,reuseaddr EXEC:${FILE_PATH}app.py,stderr &