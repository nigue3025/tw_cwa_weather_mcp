"""Minimal MCP stdio test client for app_mcp.py

Usage (PowerShell):
    & .\venv\Scripts\Activate.ps1; python .\app_mcp_test_client.py

It will:
 - start app_mcp.py as a subprocess
 - send an `initialize` message
 - call `mcp/listTools` and print the result
 - call `mcp/callTool` to invoke `check_available_location` and `get_weather` (examples)

Notes:
 - This client uses the same Content-Length framing that stdio MCP/LSP servers use.
 - If your `app_mcp.py` expects slightly different method names, adjust the method strings in the calls below.
"""

import subprocess
import sys
import json
import threading
import io
import os
import time

PY = sys.executable
SCRIPT = os.path.join(os.path.dirname(__file__), 'app_mcp.py')

# Helper: write a framed JSON message to the process stdin
def write_msg(proc, obj):
    b = json.dumps(obj, ensure_ascii=False).encode('utf-8')
    header = f"Content-Length: {len(b)}\r\n\r\n".encode('ascii')
    proc.stdin.write(header + b)
    proc.stdin.flush()

# Helper: read a framed JSON message from the process stdout
def read_msg(proc):
    # read headers
    headers = b''
    while True:
        line = proc.stdout.readline()
        if not line:
            raise EOFError('Server closed stdout')
        headers += line
        if headers.endswith(b'\r\n\r\n'):
            break
    # parse Content-Length
    headers_text = headers.decode('ascii', errors='ignore')
    for line in headers_text.split('\r\n'):
        if line.lower().startswith('content-length:'):
            length = int(line.split(':',1)[1].strip())
            break
    else:
        raise ValueError('No Content-Length header')
    # read payload
    payload = proc.stdout.read(length)
    return json.loads(payload.decode('utf-8'))


def main():
    print('Starting app_mcp.py subprocess...')
    proc = subprocess.Popen([PY, SCRIPT], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # send initialize
        init = {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
        write_msg(proc, init)
        res = read_msg(proc)
        print('\ninitialize response:')
        print(json.dumps(res, ensure_ascii=False, indent=2))

        # list tools
        req_id = 2
        list_tools = {"jsonrpc":"2.0","id":req_id,"method":"mcp/listTools","params":{}}
        write_msg(proc, list_tools)
        res = read_msg(proc)
        print('\nlistTools response:')
        print(json.dumps(res, ensure_ascii=False, indent=2))

        # call check_available_location
        req_id += 1
        call_check = {
            "jsonrpc":"2.0",
            "id":req_id,
            "method":"mcp/callTool",
            "params":{
                "name":"check_available_location",
                "arguments":{"location":"台北市"}
            }
        }
        write_msg(proc, call_check)
        res = read_msg(proc)
        print('\ncall check_available_location response:')
        print(json.dumps(res, ensure_ascii=False, indent=2))

        # call get_weather (may return large JSON)
        req_id += 1
        call_weather = {
            "jsonrpc":"2.0",
            "id":req_id,
            "method":"mcp/callTool",
            "params":{
                "name":"get_weather",
                "arguments":{"selected_county":"台北市"}
            }
        }
        write_msg(proc, call_weather)
        res = read_msg(proc)
        print('\ncall get_weather response: (truncated)')
        print(json.dumps(res, ensure_ascii=False)[:2000])

    except Exception as e:
        print('Error while testing:', e)
        # print stderr from the server for debugging
        try:
            err = proc.stderr.read().decode('utf-8')
            print('\n--- server stderr ---')
            print(err)
            print('--- end stderr ---')
        except Exception:
            pass
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()


if __name__ == '__main__':
    main()
