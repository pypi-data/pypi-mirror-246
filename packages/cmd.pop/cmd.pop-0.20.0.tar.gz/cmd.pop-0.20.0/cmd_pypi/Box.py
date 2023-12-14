# V1=bottPY( "83" , lambda BB:HTML_init("83")  )
# V1=bottPY( "83" , lambda BB:HTML_init(BB)  )
# button1.on_click( lambda BB: CMD( eval( name ) ) )  ##### 這裡BB is 
######## 注意第二個函數是 使用 lambda BB
#########################################
def bottPY(name="port 5000" , CMD="" ):
    # %%file HTML.py
    import ipywidgets as widgets
    from IPython.display import display, Javascript
    # 創建一個按鈕
    ##################################################################
    ##### 因為這邊name物件 是傳給外部HTML2當標題 (動作)
    ##### 當沒設置 參考HTML2 傳入當標題 (由這往HTML2外傳)
    # print(f"@## {name} ##@",CMD,type(CMD),"##@") 
    button1 = widgets.Button(description= f"{name}" ) ## 放棄使用
 
    ##################################################
    ########### 這裡說明 餐入和參數是分離的
    ########### lambda BB:HTML_init(89)  
    ########### None 阻斷上面 name.description方式
    ########### 直接參考 HTML 函數設置
    ########## button1.on_click 類似 return
    name="None" 
    # print("@++ name ++@",name,CMD,type(CMD),"##@") 
    # if name.count(":")==1: 
    button1.on_click( lambda BB: CMD( eval( name ) ) )  
    #####################################################
    # button1.on_click( lambda BB: CMD( eval(BB.description) ) ) 錯誤的失敗

    
    return button1



def bottCMD(name="port 5000",CMD=""):
    #################################################
    import ipywidgets as widgets
    from IPython.display import display
    ################################################
    import os
    # button1.on_click(lambda BB:print(os.popen( fun(BB.description) ).read()))   ## BB直接使用 #################### lambda BB:print(BB) 

    # 創建按鈕1
    button1 = widgets.Button(description=f"{name}")
    ##################################################################
    ##################################################################
    import os
    if CMD=="":
        button1.on_click(lambda BB:print(os.popen(str(BB.description)).read()))
    else:
        button1.on_click(lambda BB:print(os.popen(str(CMD)).read()))
    return button1
    ##################################################################
    ##################################################################
# bottCMD(f"ls -al"),
# bottCMD(f"位置","pwd"),





# R=[ str(type(buttons_row1)) , str(type(buttons_row2)) ] 
# return len([i for i in R if "<class 'ipywidgets.widgets.widget_box.VBox'>"!=i ])==0
def VBox(R=[] ):
    import ipywidgets as widgets
    from IPython.display import display
    butt1 = widgets.VBox( R )

    # print([ str(type(i)) for i in R] )
    if len([i for i in R if "<class 'ipywidgets.widgets.widget_box.HBox'>"!=str(type(i)) ])==0:
        print("@ VBox(HBox) 合格 @")
        # 顯示按鈕
        display( butt1 )
    elif len([i for i in R if "<class 'ipywidgets.widgets.widget_box.VBox'>"!=str(type(i)) ])==0:
        print("@ VBox(VBox) 顯示 @")
        # 顯示按鈕
        display( butt1 )
    else:
        return butt1

def HBox(R=[] ):
    import ipywidgets as widgets
    from IPython.display import display
    butt1 = widgets.HBox( R )

    # print([ str(type(i)) for i in R] )
    if len([i for i in R if "<class 'ipywidgets.widgets.widget_box.VBox'>"!=str(type(i)) ])==0:
        print("@ HBox(VBox) 顯示 @")
        # 顯示按鈕
        display( butt1 )
    elif len([i for i in R if "<class 'ipywidgets.widgets.widget_box.HBox'>"!=str(type(i)) ])==0:
        print("@ HBox(HBox) 顯示 @")
        # 顯示按鈕
        display( butt1 )
    else:
        return butt1 