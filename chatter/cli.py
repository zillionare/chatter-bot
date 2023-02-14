"""Console script for backtest."""

import logging
import os
import re
import signal
import subprocess
import sys
import time

import cfg4py
import fire
import httpx
import psutil
from chatter.config import get_config_dir, endpoint

logger = logging.getLogger(__name__)

cfg = cfg4py.init(get_config_dir())


def help():
    print("chatter")
    print("=" * len("chatter"))
    print("chatter framework")


def find_chatter_process():
    """查找chatter进程

    chatter进程在ps -aux中显示应该包含 chatter.app 信息
    """
    for p in psutil.process_iter():
        try:
            cmd = " ".join(p.cmdline())
            if "chatter.app start" in cmd:
                return p.pid
        except psutil.AccessDenied:
            pass

    return None


def is_running(port=2130, endpoint="abcde"):
    url = f"http://localhost:{port}/{endpoint}/status"

    try:
        r = httpx.get(url)
        return r.status_code == 200
    except Exception:
        return False


def status(port=2130):
    """检查chatter server是否已经启动"""
    pid = find_chatter_process()
    if pid is None:
        print("chatter server未启动")
        return

    if is_running(port, endpoint()):
        print("\n=== chatter server is RUNNING ===")
        print("pid:", pid)
        print("port:", port)
        print("endpoint:", endpoint())
        print("\n")
    else:
        print("=== chatter server is DEAD ===")
        os.kill(pid, signal.SIGKILL)


def stop():
    print("停止 chatter server...")
    pid = find_chatter_process()
    if pid is None:
        print("chatter server未启动")
        return

    p = psutil.Process(pid)
    p.terminate()
    p.wait()
    print("chatter server已停止服务")


def start(port=2130):
    port = port or cfg.server.port

    if is_running(port, endpoint()):
        status()
        return

    print("启动chatter server")

    process = subprocess.Popen(
        [sys.executable, "-m", "chatter.app", "start", "--port", f"{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # for i in tqdm(range(100)):
    #     time.sleep(0.1)
    #     if is_running(port, endpoint()):
    #         status()
    #         return

    #     if process.poll() is not None:  # pragma: no cover
    #         # already exit, due to finish or fail
    #         out, err = process.communicate()
    #         logger.warning(
    #             "subprocess exited, %s: %s", process.pid, out.decode("utf-8")
    #         )
    #         raise subprocess.SubprocessError(err.decode("utf-8"))
    # else:
    #     print("chatter server启动超时或者失败。")


def main():
    fire.Fire({"help": help, "start": start, "stop": stop, "status": status})


if __name__ == "__main__":
    main()  # pragma: no cover
