"""Raw async finite wait and unchanged installer from repair1; live-only caller."""
import asyncio

async def bounded(awaitable, seconds, cancel_grace=2):
    """wait_for/gather can wait indefinitely when cancellation is suppressed."""
    task = asyncio.create_task(awaitable)
    done, _ = await asyncio.wait({task}, timeout=max(0, seconds))
    if done:
        return task.result()
    task.cancel()
    done, _ = await asyncio.wait({task}, timeout=max(0, cancel_grace))
    if done:
        # Retrieve cancellation/error without replacing the primary timeout.
        try:
            task.result()
        except BaseException:
            pass
    raise TimeoutError("Operation deadline; cancellation completion not assumed")


def install_pins(requirements, absolute_deadline):
    import json
    from pathlib import Path
    import subprocess
    import sys
    import time
    if sys.version_info[:3] != (3, 13, 14):
        raise RuntimeError('Pinned Python unavailable')
    pins = Path('/a040-requirements.txt')
    pins.write_text(requirements)
    seconds = min(600, int(absolute_deadline-time.time())-30)
    if seconds <= 0:
        raise TimeoutError('Preparation deadline before installer')
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir',
                    '--only-binary=:all:', '--extra-index-url',
                    'https://download.pytorch.org/whl/cu126', '-r', str(pins),
                    '--report', '/a040-install-report.json'], check=True, timeout=seconds)
    inventory = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze', '--all'], text=True)
    Path('/a040-linux-requirements.lock.txt').write_text(inventory)
    print('A040_LINUX_PINS='+json.dumps(inventory), flush=True)

