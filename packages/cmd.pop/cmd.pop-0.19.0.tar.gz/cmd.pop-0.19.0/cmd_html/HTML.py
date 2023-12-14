
if __name__=="__main__":
    

    # import sys,site
    # sys.path.append(site.getsitepackages()[0])
    # ##########################
    # # from cmd_html import  *    ## 不要使用
    # import importlib,cmd_html 
    # cmds = importlib.reload(cmd_html)
    # #########################
    import sys
    print("@ HTML.py @",__name__,"cmd_html"  in sys.modules , "cmds"  in sys.modules)
    # __init__.py ############################## 設定
    # from  cmd_html.HTML_init import *
    # from  cmd_html.HTML_del import *
    # bott("A",lambda BB :print( BB.description ) )
    # sys.modules["cmd_html"].__dict__=globals()



   

    # bott("A",lambda BB :print( BB.description ) )
    # bott(" web :8080 ",lambda BB :print( BB.description ) )

    # cmds.HTML_init(5000)
    # input("")
    # cmds.HTML_del(5000)

    # import sys,cmd_html as cmds
    from  cmd_html.HTML_init import *
    from  cmd_html.HTML_del import *
    import importlib as L
    L.reload(L.import_module("cmd_html.HTML_init"))
    L.reload(L.import_module("cmd_html.HTML_del"))


    print("@ __init__.py @",__name__,"cmd_html"  in sys.modules , "cmds"  in sys.modules)
  

    if len(sys.argv)==2:
        PPT=eval(sys.argv[1])
        if type(PPT)==int:
            find_pid(PPT)
    else:
        PPT=80
        

    #### 這邊是一個 fun函數 先不要執行....BB是按鈕物件.....當按下才執行 HTML_init(5000) 
    bottBu(f" web  :{PPT} ",lambda BB :  HTML_init(PPT)  )
    bottBu(f" 狀態 :",lambda BB :   HTML_status(PPT) )
    bottBu(f" 關閉 :{PPT} ",lambda BB :  HTML_del(PPT)  )  ## find 會傳回 ## HTML 傳方法


import os
# os.system("git init")
# os.system("git remote add T https://gitlab.com/your-username/your-repo.git")
