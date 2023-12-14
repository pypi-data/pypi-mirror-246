
if __name__=="__main__":
    


    import sys
    # print("@ HTML.py @",__name__,"cmd_html"  in sys.modules , "cmds"  in sys.modules)
    ##################################################
    import importlib as L
    #################################################
    from  cmd_html.HTML_init import *
    from  cmd_html.HTML_del import *
    from  cmd_pypi.Box import *
    # L.reload(L.import_module("cmd_html.HTML_init"))  ## 發生找不到模組的 錯誤
    # L.reload(L.import_module("cmd_html.HTML_del"))
    # L.reload(L.import_module("cmd_pypi.Box"))
    L.reload(L.import_module("HTML2"))
    ####################################################
    # print("@ __init__.py @",__name__,"cmd_html"  in sys.modules , "cmds"  in sys.modules)
  

  

    if len(sys.argv)==2:
        PPT=eval(sys.argv[1])
        if type(PPT)==int:
            find_pid(PPT)
    else:
        PPT=80

    
    import os
    NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
    ##############################################################
    V1=bottPY(f" web  :{PPT} ",lambda BB :HTML_init(PPT)  )
    V2=bottPY(f" 狀態 :"      ,lambda BB :HTML_status(PPT) )
    V3=bottPY(f" 關閉 :{PPT} ",lambda BB :HTML_del(PPT)  )  

    # H1=VBox([V1,V1])
    # HBox([H1,H1])
    # ##############
    # print("@"*100)

    H1=VBox([V1,V2,V3])
    #### 這邊是一個 fun函數 先不要執行....BB是按鈕物件.....當按下才執行 HTML_init(5000) 
    V1=bottCMD(f"pwd")
    V2=bottCMD("安裝 cmd.pop 模組",f"echo 安裝中..稍後|| pip install cmd.pop {NU} | echo 安裝完畢!!")
    V3=bottCMD(f"pip show cmd.pop",)  ## find 會傳回 ## HTML 傳方法
    H2=VBox([V1,V2,V3])
    HBox([H1,H2])
    ################################
    #########################
    ##################

