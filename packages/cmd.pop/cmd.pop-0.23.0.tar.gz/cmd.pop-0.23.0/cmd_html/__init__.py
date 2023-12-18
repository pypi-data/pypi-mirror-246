

# import os
# open(os.path.__file__,"a").write("print(123)") ## 第 1 順位
# import site
# open(site.__file__,"a").write("print(123999)")  ## 第 2 順位



# @ name @ cmd_html.HTML    ####### pip install 時候
# @ name @ __main__          ####### %run HTML   時候



# import os
# if  os.path.isdir("sample_data"):
#     import os
#     # os.system("rm -rf /content/*")
#     os.system("rm -rf /content/sample_data")
#     ########################################






# ########## HTML :: import 時候 此模組不會是 __main__
# import sys
# if __name__!="cmd_html":
#         # "cmd_html"  in sys.modules["cmd_html"]
#         print("@ __init__.py @",__name__,"cmd_html"  in sys.modules , "cmds"  in sys.modules)
#         # __init__.py ############################## 設定
#         from  cmd_html.HTML_init import *
#         from  cmd_html.HTML_del import *
#         # bott("A",lambda BB :print( BB.description ) )
#         # sys.modules["cmd_html"].__dict__=globals()
#         # sys.modules["cmd_html"].__dict__=globals()

#         sys.modules["__main__"].__dict__["cmds"] =  sys.modules["cmds"] = sys.modules["cmd_html"]
#         del sys.modules["cmd_html"]
        
#         print("@ __init__.py @ add ...",__name__,"cmd_html"  in sys.modules , "cmds"  in sys.modules)



# from  cmd_html.HTML_init import HTML_init,bott
# from  cmd_html.HTML_del import *



# @ name @ cmd_html.HTML    ####### pip install 時候
# @ name @ __main__          ####### %run HTML   時候
# if __name__=="__main__": ################################ 




# ### [更新] 和 [替換方法]
# def reload_module(module_name):
#     import sys,importlib
#     if module_name in sys.modules:
#         print("@ 1 @")
#         del sys.modules[module_name]
#         # print(module_name)
#         # if module_nam.split(".")
#         if module_name.count(".")>0:
#           NN = module_name.rsplit(".")[1]
#           sys.modules[module_name] = getattr(__import__(module_name),NN)
#     else:
#         print("@ 2 @")
#         sys.modules[module_name]= importlib.import_module(module_name)
#     return sys.modules[module_name]
# ### reload ############################## [更新]
# reload_module(module_name)
















# 多餘!!
# import os,site
# os.environ["PYTHONPATH"]=site.getsitepackages()[0]+":"+os.environ["PYTHONPATH"] ### 這個不能亂改 會嚴重錯誤
# os.environ["PATH"]=site.getsitepackages()[0]+":"+os.environ["PATH"]             ### 這個不能亂改 會嚴重錯誤
# import os
# os.chdir("/usr/local/lib/python3.10/dist-packages")
# %run cmd_html/HTML_init  ####### 他是用當前路徑去計算
