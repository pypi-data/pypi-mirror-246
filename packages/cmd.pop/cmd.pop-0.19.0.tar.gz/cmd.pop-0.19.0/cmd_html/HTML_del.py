# %%file /usr/local/lib/python3.10/dist-packages/HTML_del.py

def find_pid(port=5000):
    import subprocess
    try:
        # 使用subprocess運行lsof -i :<port>命令
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)

        # 檢查命令是否成功執行
        if result.returncode == 0:
            # 分析命令輸出，獲取PID
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                # 第二行是進程信息，取第一列（PID）
                pid = lines[1].split()[1]
                # return int(pid)
                pid = int(pid)
                ################################################################
                import  psutil
                if pid:
                    try:
                        # 通過 PID 獲取進程對象
                        process = psutil.Process(pid)  ## 終止無效:所以改上面ppid
                        # 獲取目標進程的上級 (ppid)
                        # ppid = process.ppid()
                        # process = psutil.Process(ppid) ############################################## 取消 PPID 避免 關閉自己
                        # 終止進程，你也可以使用 process.kill() 來發送 SIGKILL 信號
                        process.terminate()
                        print(f"已終止 PID 為 {pid} 的進程。")
                    except psutil.NoSuchProcess:
                        print(f"未找到 PID 為 {pid} 的進程。")
                else:
                    print(f"未找到使用端口 {port} 的進程。")
    except Exception as e:
        print(f"Error: {e}")
    return None


# !ps aux | grep gunicorn
def find_web( user_port=5000, user_name = 'gunicorn' ):
    import psutil
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == user_port:
            pid = conn.pid
            # print("@ pid :",pid)
            # return conn.pid
            try:
                process = psutil.Process(pid)
                if process.name() == user_name:
                    print(f"@ 找到端口 { user_port } 上由 '{ user_name }' 启动的进程 PID: {pid} @")
                    return pid

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        # if pid:
        #   print(f"@ 找到端口 { user_port } 上由 '{ user_name }' 启动的进程 PID: {pid} @")
        # else:
    print(f"@ 未找到端口 { user_port } 上由 '{ user_name }' 启动的进程 @")
    return False
################################################################
# def kill_port(port=5000):
def HTML_del(port=5000):
    import psutil
    # 通過指定的端口找到進程的 PID
    pid = find_web(port)
    # if  not pid:
    #     pid = Fpid(port)
    #     print("@!",  Fpid(port) )
    
    if pid:
        try:
            # 通過 PID 獲取進程對象
            process = psutil.Process(pid)  ## 終止無效:所以改上面ppid
            # 獲取目標進程的上級 (ppid)
            ppid = process.ppid()
            process = psutil.Process(ppid)
            # 終止進程，你也可以使用 process.kill() 來發送 SIGKILL 信號
            process.terminate()
            print(f"已終止 PID 為 {pid} 的進程。")
        except psutil.NoSuchProcess:
            print(f"未找到 PID 為 {pid} 的進程。")
    else:
        print(f"未找到使用端口 {port} 的進程。")


# kill_port(5000)
