import subprocess, json

result = subprocess.run(
    ['kaggle', 'kernels', 'logs', 'kingtechie/fako-online-download-latentsync-v3'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)

lines = result.stdout.split('\n')
stdout_lines = []
for line in lines:
    line = line.strip().rstrip(',')
    if not line:
        continue
    try:
        obj = json.loads(line)
        if obj.get('stream_name') == 'stdout':
            data = obj.get('data', '').rstrip()
            if data:
                stdout_lines.append(data)
    except json.JSONDecodeError:
        pass

for l in stdout_lines:
    print(l)
