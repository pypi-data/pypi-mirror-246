# %%file /usr/local/lib/python3.10/dist-packages/ABC/HTML.py
# %%file HTML.py
# import ipywidgets as widgets
# from IPython.display import display, Javascript


def bottBu(name="port 5000" , fun=lambda:"預設方法" ):
    # %%file HTML.py
    import ipywidgets as widgets
    from IPython.display import display, Javascript
    # 創建一個按鈕
    reset_button = widgets.Button(description= f"{name}" )
    # 將按鈕綁定到重製函數
    reset_button.on_click( lambda BB :fun( BB ) )  ##### 這裡BB is   .......def HTML_init(button): 按鈕::本身的物件  ........
    # 顯示按鈕
    display(reset_button)




def HTML_status(port):
    import subprocess
    command = f"lsof -i :{port}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"端口 {port} 已經啟動")
    else:
        print(f"目前端口 {port} 尚未使用")

# 調用方法，例如檢查 5000 端口
#  HTML_status(p8080)

# 先不管 bott是什麼..........如果想停止!!就不可以先帶入參數!!
# #### 這邊是一個 fun函數 先不要執行....BB是按鈕物件.....當按下才執行 HTML_init(5000) 
# bott(" web :8080 ",lambda BB :HTML_init(5000)  )
def HTML_init(port=5000):
# def HTML_init(button):
    # def reset_notebook(button):
        # import os
        # os.system("rm -rf /content/*")
        # print(button)


        import os
        # os.system("pip install gunicorn >/dev/null 2>&1 ")
        # port="5000" ## 禁止用80 port 會失敗
        # port= str(portN)   ## 禁止用80 port 會失敗
        from google.colab.output import eval_js
        url = eval_js( "google.colab.kernel.proxyPort(" + str(port) + ")" )
        print(url)
        # os.system(f"gunicorn -b 127.0.0.1:{port}  moon_app:app ")
        # !gunicorn -b 127.0.0.1:{port}  moon_app:app
        # !gunicorn -b 127.0.0.1:{port}  moon_app:app --daemon
        # !gunicorn -b 127.0.0.1:{port} moon_app:app -D --pid /content/moon_app.pid
        
        # os.system(f"gunicorn -b 127.0.0.1:{port} moon_app:app -D --pid /content/moon_app.pid")
        # os.system(f"echo {port} > /content/moon_app.port")
        os.system(f"gunicorn -b 127.0.0.1:{port} moon_app:app -D")
    # return reset_notebook



# # 創建一個按鈕
# reset_button = widgets.Button(description="port 5000")
# # 將按鈕綁定到重製函數
# reset_button.on_click(reset_notebook)
# # 顯示按鈕
# display(reset_button)

