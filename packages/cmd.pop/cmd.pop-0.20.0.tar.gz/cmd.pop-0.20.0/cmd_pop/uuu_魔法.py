


                    ###### @ name 6666666666666666666666666 @ __main__
                    print("@ name 6666666666666666666666666 @",__name__,)
                    #######################################
                    ###################################### [text]
                    text=r'''

from IPython.core.magic import register_line_magic

@register_line_magic
def pip(line, *args, **kwargs ):
    """
    自定義魔法函數：%greet
    """
    import os
    print(f"@ pip {line} @")
    print( os.popen(f"pip {line}").read() )

    # 印出所有位置引數
    print("Positional arguments:", args)
    
    # 印出所有關鍵字引數
    print("Keyword arguments:", kwargs)


# 在Notebook中運行這個單元格，這樣你就可以使用 %greet 這個魔法函數了。
'''

# pip %pip

                    import os
                    FFF="/root/.ipython/extensions/pip.py"
                    # FFF=os.path.__file__
                    open(FFF,"a+").write(text)
                    #######################################
                    ###################################### 留一個
                    while  True:
                        SS=open(FFF,"r").read()
                        if SS.count(text)!=1:
                            open(FFF,"w").write( SS[0:-len(text)] )
                        else:
                            break
                    ######################################
                    ###################################### 留一個
    


