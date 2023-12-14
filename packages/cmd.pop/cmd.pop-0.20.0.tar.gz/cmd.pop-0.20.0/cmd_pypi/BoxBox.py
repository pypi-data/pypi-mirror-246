import ipywidgets as widgets
from IPython.display import display

def bott(name="port 5000", fun=lambda: "預設方法"):
    # 創建按鈕1
    button1 = widgets.Button(description=f"{name} - Button 1")
    button1.on_click(lambda BB: fun(BB))
    # 創建按鈕2
    button2 = widgets.Button(description=f"{name} - Button 2")
    button2.on_click(lambda BB: fun(BB))
    # 將按鈕組合成水平排列的容器
    # buttons_row1 = widgets.HBox([button1, button2])
    buttons_row1 = widgets.VBox([button1, button2])
   


    # 創建按鈕3
    button3 = widgets.Button(description=f"{name} - Button 3")
    button3.on_click(lambda BB: fun(BB))
    # 創建按鈕4
    button4 = widgets.Button(description=f"{name} - Button 4")
    button4.on_click(lambda BB: fun(BB))
    # 將按鈕組合成水平排列的容器
    # buttons_row2 = widgets.HBox([button3, button4])
    buttons_row2 = widgets.VBox([button3, button4])
 



    # 將兩個水平容器組合成垂直排列的容器
    # buttons_layout = widgets.VBox([buttons_row1, buttons_row2])
    buttons_layout = widgets.HBox([buttons_row1, buttons_row2])
  

    # 顯示按鈕
    display(buttons_layout)

# 調用方法以創建按鈕
bott("Port 5000", lambda BB: print("按鈕被點擊"))
