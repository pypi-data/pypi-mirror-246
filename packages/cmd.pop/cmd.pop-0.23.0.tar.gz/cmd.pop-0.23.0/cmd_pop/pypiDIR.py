import sys,subprocess
# print("@ sys @",sys.argv)
class Var:
    # nameA = 'pip'
    # nameB = '0.2.0'
    ### 修改參數 ###
    @classmethod
    def update_names(cls, name=None, vvv=None):
        """
        更新
        """
        if name is not None and vvv is not None:
            cls.nameA = name
            cls.nameB = vvv
          
            print(f"已更新 nameA={cls.nameA}, nameB={cls.nameB}")
            print("-"*50)

            # 修改文件内容
            # filename = __file__   # 替换成你的脚本文件名
            with open( "setup.py" , 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if "### 修改參數 ###" in line:
                        lines[i-2] = f"    nameA = '{name}'\n"
                        lines[i-1] = f"    nameB = '{vvv}'\n"
                        break  # 找到后就退出循环
                f.seek(0)
                f.writelines(lines)
                f.truncate()
                # 刷新檔案緩衝區
                f.flush()
                f.close()
              
               ##  這邊會導致跑二次..............關掉一個
       
             
        else:
            print("未提供足够的参数")
    
    @classmethod
    def gitNAME(cls,name="name"):
        import subprocess
        # 讀取 Git 使用者名稱
        result = subprocess.run(['git', 'config', f'user.{name}'], capture_output=True, text=True)

        # 如果命令成功執行，則輸出使用者名稱
        if result.returncode == 0:
            git_user_name = result.stdout.strip()
            # print(f"Git 使用者名稱: {git_user_name}")
            return git_user_name
        else:
            # print("無法讀取 Git 使用者名稱")
            return False
    # name=gitNAME()
    # pypi=gitNAME('pypi')
    @classmethod
    def pip_MD(cls,name, passs):
        # if os.name == "nt":
        #     file_path = os.path.join(os.getcwd(), ".pypirc")
        # else:
        if os.name != "nt":
            file_path = "/root/.pypirc"
            with open(file_path, "w") as f:
                f.write("[pypi]\n")
                f.write("repository: https://upload.pypi.org/legacy/\n")
                f.write(f"username: {name}\n")
                f.write(f"password: {passs}\n")
    @classmethod
    def pip_exists(cls,package_name):
        import os,importlib
        if  os.name=="nt":
            print("條件必須[linux]環境")
        else:
            try:
                importlib.import_module(package_name)
            except ImportError:
                NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
                os.system(f"pip install {package_name} {NU}")
    @classmethod
    def pip_twine( cls,URL="https://gitlab.com/moon-0516/cmd.pop@0.11.0" ):
        import os
        if  os.name=="nt":
            print("條件必須[linux]環境")
        elif URL.count("@")==1:
            os.chdir("/content")
            A,B=URL.split("@")
            NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
            print(f"git clone -b {B} {A} {NU}")  
            
            name=os.path.basename(A)
            print("")
            if  os.system(f"git clone -b {B} {A}")==0:
                os.chdir(name)
                os.system(f"rm -rf /content/.git")
                os.system("python setup.py sdist")
                print(os.popen("twine upload --skip-existing  dist/*  --config-file /root/.pypirc").read())
                print("pause            ")
                input("pause")
                
            os.chdir("../")
            os.system(f"rm -rf /content/{name}")
        else:
            print("格式不對")
    @classmethod
    def  clear(cls):
            ###############################################################################
            import os
            if os.name!="nt":
                os.system("rm -rf ~/.cache/pip/*")
            else:
                os.system(f"rmdir /q /s %LOCALAPPDATA%\pip\cache")
            ################################################################################
    ############
    ############
    # pypi.Var.run(self,Var.nameA) ## del[cmd_pop]
    @classmethod
    def run(cls,  this=None , install=None ,nameA="cmd.pop" ):
        #####

        ###################################
        def del_file(directory = "/path/to/your/directory"):
            import os
            # 如果目錄存在，則刪除其中的所有檔案
            if os.path.exists(directory):
                [os.remove(os.path.join(directory, file)) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
                print("所有檔案已刪除。")
            else:
                print(f"目錄 '{directory}' 不存在。")
        ###################################
        ###################################
        # from setuptools.command.install import install
        import os
        data = {}    
        PWD=os.getcwd()
        ### 路徑   底下目錄  底下檔案
        for root , dirs , files in os.walk(PWD):
            print( os.path.basename(root) in [i for i in os.listdir( PWD )if i[0]!="."] )
            if  root.find(os.path.sep+".git")==-1:
                ######################################## 
                ######################################## 
                print(root , dirs , files)
                ################################################################### 
                ######################################## def 刪除路徑下的 所有檔案
                BB=nameA.split(".")               ### [nameA] ###
                if "_".join(BB)==os.path.basename(root):         
                    print( "@@## ",root )         
                    del_file( root )
                    # os.system(f"rmdir /q /s %LOCALAPPDATA%\pip\cache")
                print( "@@ ## "*10 )
        return install.run( this )
    
    @classmethod
    def import_file(cls,name):
        import importlib as L
        MDD = L.import_module(name)    
        # from cmd_html import setupPIP
        text=open( MDD.__file__ ,"r",encoding='utf8').read()
        os.system(f"git config --global file.{name} {text}")
        os._exit(0)
    @classmethod
    def open_file(cls,name):
        import os
        # print("@@", os.getcwd() + os.path.sep + "setup.py" )
        # SS=open( os.getcwd() + os.path.sep + "setup.py" ,"w",encoding='utf8').write("text")
        return os.popen(f"git config --global file.{name}").read().strip()
        # os._exit(0)
            
    
        
    
    
def pip_api(moon="moon-start",name=""):

    token=gitNAME('api').split(":")
    token=False if len(token)==1 else token[1]
    if not token:
        return token
    ###################################
    if  not token :
        print(f"@ token {token} 不存在 @")
        os._exit(0)
    # !curl --header "PRIVATE-TOKEN: KEY" "https://gitlab.com/api/v4/projects/moon-start%2FBAT."
    import requests
    url = f"https://gitlab.com/api/v4/projects/{moon}%2F{name}"
    headers = {"PRIVATE-TOKEN": token }
    # headers = {"PRIVATE-TOKEN": "KEY"}
    response = requests.get(url, headers=headers)
    # print(response.status_code==200)
    # print(response.json())
    return response.status_code==200

def pip_tag(moon="moon-start",name=""):
    token=gitNAME('api').split(":")
    token=False if len(token)==1 else token[1]
    if not token:
        return token
    # namespace = "moon-start"
    ###################################
    if  not token :
        print(f"@ token {token} 不存在 @")
        os._exit(0)
    # !curl --header "PRIVATE-TOKEN: KEY" "https://gitlab.com/api/v4/projects/moon-start%2FBAT."
    import requests
    # url = f"https://gitlab.com/api/v4/projects/moon-start%2F{name}"
    url_tag = f"https://gitlab.com/api/v4/projects/{moon}%2F{name}/repository/tags"
    headers = {"PRIVATE-TOKEN": token }
    # headers = {"PRIVATE-TOKEN": "KEY"}
    response = requests.get(url_tag, headers=headers)
    # print(response.status_code==200)
    # print(response.json())
    # return response.status_code==200
    RR=[]
    if response.status_code == 200:
        tags_info = response.json()
        # print("Project Versions:")
        for tag in tags_info:
            # print(tag.get("name"))
            RR.append(tag.get("name"))
    # else:
        # print(f"Error getting tags: {response.status_code}")
    ## 排序
    keyIF = lambda x: tuple(map(int, x.split('.')))
    TG=sorted(RR,key=keyIF)
    return TG

def gitNAME(name="name"):
    import subprocess
    # 讀取 Git 使用者名稱
    result = subprocess.run(['git', 'config', f'user.{name}'], capture_output=True, text=True)


    # 如果命令成功執行，則輸出使用者名稱
    if result.returncode == 0:
        git_user_name = result.stdout.strip()
        # print(f"Git 使用者名稱: {git_user_name}")
        return git_user_name
    else:
        # print("無法讀取 Git 使用者名稱")
        # returninput("@ [pip api] : ")
        return False
moon=gitNAME("moon")
# moon="moon-start"
name=gitNAME()
pypi=gitNAME('api')
##########################################################
import sys,os   
if len(sys.argv)==4:
    if   sys.argv[1]=="moon"  and sys.argv[3]=="ok":
        import os
        name=str(sys.argv[2])
        os.system(f"git config --global user.moon {name}")
        os._exit(0)
    if  sys.argv[1]=="del"  and sys.argv[2]=="ok":
        import shutil
        def rmdirDIR(path):
            try:
                shutil.rmtree(path)
                # print(f"成功刪除目錄: {directory_path}")
            except Exception as e:
                # print(f"刪除目錄時發生錯誤: {e}")
                pass
        home = os.getcwd()
        ########################################
        # 呼叫函數以刪除目錄
        rmdirDIR(f"{home}{os.path.sep}.git")
        input("[pause] 確定刪除?? ")
        rmdirDIR(f"{home}{os.path.sep}{sys.argv[3]}")
        os._exit(0)







if len(sys.argv)==3:
    if  sys.argv[1]=="MD":
        Var.pip_MD( "__token__",sys.argv[2].strip() )
        os._exit(0)
    if  sys.argv[1]=="twine":
        Var.pip_exists("twine")
        Var.pip_twine( sys.argv[2].strip()  )
        os._exit(0)

    if   sys.argv[1]=="name":
        import os
        name=str(sys.argv[2])
        os.system(f"git config --global user.name {name}")
        os.system(f"git config --global init.defaultBranch main")
        os._exit(0)
    elif sys.argv[1]=="api":
        import os
        KEY=str(sys.argv[2])
        ###################################################
        # if os.name=="nt":
        #     os.system("rmdir /s /q .git")
        # else:
        #     os.system("rm -rf .git")
        ###################################################
     
            # if not BBL:
            #     print("@ 重新執行 @")
            #     os._exit(0)
        if ".git"  in os.listdir(os.getcwd()):
            pypi = os.popen("git config --global user.api").read().strip()
            SA =  os.path.basename(os.popen("git remote get-url gitlab").read().strip())
            os.system(f"git remote  set-url gitlab https://{ pypi }@gitlab.com/{moon}/{SA}")
            print(f"@ [位置] @ git remote  set-url   https://{ pypi }@gitlab.com/{moon}/{SA} @")
   

        ###################################################
        os.system(f"git config --global  user.api {KEY}")
        os._exit(0)
    elif sys.argv[1]=="del":
        import os
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        os.system(f"pip cls {NU}") ## 缺一不可
        print(f"@ [使用] pip uninstall {sys.argv[2]} -y  @")
        print(os.popen(f"pip uninstall {sys.argv[2]} -y ").read())
        os._exit(0)

        
    elif sys.argv[2]=="get":
        import os
        if os.name=="nt": #### 在 win 11 使用
            ##########################################
            name = sys.argv[1]
            value = os.popen(f"git config user.{name}").read().strip()
            ##########################################
            print(f"## [user.{name}] {value}  ") 
            os._exit(0)

    elif sys.argv[1]=="save":
        import os
        if os.name=="nt": #### 在 win 11 使用
            ##########################################
            name = sys.argv[2]
            print(f"#1# [save-del-cmd.pop]",os.popen(f"pip del {name}").read().strip())
            # value = os.popen(f"pip setup.py cmd.pop  {name} && pip -u install cmd.pop=={name}").read().strip()
            value = os.popen(f"pip setup.py cmd.pop  {name} && pip install cmd.pop=={name}").read().strip()
            ##########################################
            print(f"#2# [save-setup.py-cmd.pop={name}]","##"*60,f"\n\n\n{value}") 
            os._exit(0)


    elif sys.argv[1]=="load" and sys.argv[2]=="pip":
        import os
        if os.name!="nt":
            ##########################################
            # from IPython import get_ipython
            # # 取得 IPython 實例
            # ip = get_ipython()
            # # 使用 os.system() 來執行 %load_ext pip
            # import os
            # os.system("jupyter nbextension enable --py widgetsnbextension")
            # # 或者使用 IPython 的 run_line_magic 方法
            # ip.run_line_magic("load_ext", "pip")
            # # ip.run_line_magic("load_ext", "PY檔名")
            ##########################################
            print(f"@ [使用] %load_ext  pip  @") 
            os._exit(0)


 
if len(sys.argv)==2:
    # print("!!")
    if  sys.argv[1]=="api":
        import os
        os.system("git config --global --unset user.api")
        print("@ git config --global --unset user.api 移除 @") 
        os._exit(0)
    elif  sys.argv[1]=="moon":
        import os
        os.system("git config --global --unset user.moon")
        print("@ git config --global --unset user.moon 移除 @") 
        os._exit(0)
    ########################
    ########################
    elif sys.argv[1]=="pop":
        import os
        dictQ={i.split("=")[0][5::] : i.split("=")[1] for i in os.popen("git config --global --list").read().split("\n")if i[0:4]=="user"}
        # if "name" in dictQ.keys():
        #   S=dictQ["name"]
        #   print(S)
        
        print(f"@ user: {dictQ} @")
        os._exit(0)
    elif sys.argv[1]=="init":
        import os
        home = os.path.basename(os.getcwd())
        NN   = home.split(".")
        if len(NN)==2:
            ###############################################################################
            if ".git" in os.listdir():
                print("# [提示] (git init) 已建立")
                print("# [提示] 停止 pip init 後面動作")
            else:
                # 创建目录
                os.makedirs( "_".join(NN) , exist_ok=True)
                # 在目录中创建 __init__.py 文件
                open( "."+os.path.sep+"_".join(NN)+os.path.sep+"__init__.py" , 'w').write(" ")
                ### [建檔] ###
                ######################################################## 拷貝 ##
                # from cmd_html import setupPIP 
                # text=open( setupPIP.__file__ ,"r",encoding='utf8').read()

                # import os
                # print("@@", os.getcwd() + os.path.sep + "setup.py" )
                # SS=open( os.getcwd() + os.path.sep + "setup.py" ,"w",encoding='utf8').write("text")
                #######################################################
                os.system("git init ")
                pwd=os.path.basename(os.path.dirname(os.getcwd()))
                os.system(f"git config user.moon {pwd}")
                os.system(f"git config user.home {home}")
              


                # print("@ git config --global --unset user.api 移除 @") 
        
            # print(f"@ pip moon @ {pwd}")
            # os.system(f"pip moon {pwd}")
            ############
            os._exit(0)
        else:
            print("# [提示] 專案名稱沒有[.] ")
            print("# [提示] 無法 (git init)")
            os._exit(0)

        # print( len(NN) )
        os._exit(0)
    elif sys.argv[1]=="cls":
        Var.clear()
        os._exit(0)
    elif sys.argv[1]=="MD":
        print("")
        print("https://colab.research.google.com/drive/1jl5xJiOqFz5Bcj7SdPsF1VmBVR_dCWb0")
        os._exit(0)
    if len(sys.argv)==2:
        # if  sys.argv[1][0]==r"%" and  len(sys.argv[1])!=1  :
        if  sys.argv[1]==r"%pip" and  len(sys.argv[1])!=1  :
            print(f"@ [使用] %load_ext  pip  @") 
            os._exit(0)


if len(sys.argv)==4:
    if  sys.argv[1]=="setup.py" and moon and pypi:
        SA,SB = sys.argv[2],sys.argv[3]
        ########################################################
        NU= ">nul 2>&1" if os.name=="nt" else  ">/dev/null 2>&1"
        if os.system(f'git remote get-url gitlab {NU}')!=0:
            os.system(f"git init")
            os.system(f"git remote add gitlab https://{ pypi }@gitlab.com/{moon}/{SA}")
            print(f"@ [位置] @ git remote add gitlab https://pypi:{ pypi }@gitlab.com/{moon}/{SA} @")
        else:
            import re
            URL = os.popen("git remote get-url gitlab").read().strip()
            KEY=re.findall(r'https://([^/^@]+)@gitlab\.com/[^/^@]+/[^/^@]+$',URL)
            if len(KEY)!=0:
               KEY=KEY[0]
               URL = re.sub( f"//{KEY}@", f"//{pypi}@" ,URL )
            else:
                os.system(f"git remote  set-url gitlab {URL}")
                print(f"@ [位置] @ git remote  set-url  {URL} @")
                print("-"*50)
                os._exit(0)

            # print("@!! URL ",KEY,pypi,URL)
            # print("@ URL ",URL)

     
        #####################################################
        Var.update_names( SA,SB )

        
        if  not pip_api(moon,SA):
            print(f"@ 專案不存在 @")
            os._exit(0)


        # # print("@ SA :",pip_tag(moon,SA),SB)
        # if  pip_tag(moon,SA)==[]:
        #     print("# ",os.popen(f"git add . ").read())
        #     print("# ",os.popen(f"git commit -m \"{ SB }\" ").read())
        #     print("# ",os.popen(f"git tag { SB } ").read())
        #     #########################################################
        #     print("# ",os.popen(f"git push -u gitlab main").read())
        #     print("# ",os.popen(f"git push --tags").read())
        # else:
        #     # print( "@ SB :" ,SB in pip_tag(moon,SA)  )
        #     if  SB in pip_tag(moon,SA):
        #         # 刪除本地標籤
        #         os.popen(f"git tag -d { SB }")
        #         # 推送新標籤到遠端
        #         os.popen(f"git push gitlab :refs/tags/{ SB }")
        #         ###################################################
        #         ###################################################
        #     #######################################################
        #     print("# ",os.popen(f"git add . ").read())
        #     print("# ",os.popen(f"git commit -m \"{ SB }\" ").read())
        #     print("# ",os.popen(f"git tag { SB } ").read())
        #     #########################################################
        #     print("# ",os.popen(f"git push -u gitlab main").read())
        #     print("# ",os.popen(f"git push --tags").read())


        if  SB in pip_tag(moon,SA):
            # 刪除本地標籤
            os.popen(f"git tag -d { SB }  {NU}")
            # 推送新標籤到遠端
            os.popen(f"git push gitlab :refs/tags/{ SB }  {NU}")
            ###################################################
            ###################################################
            import time
            time.sleep(1)
       
        #######################################################
        print("# ",os.popen(f"git add .  {NU}").read())
        print("# ",os.popen(f"git commit -m \"{ SB }\"  {NU}").read())
        print("# ",os.popen(f"git tag { SB }  {NU}").read())
        #########################################################
        print("# ",os.popen(f"git push -u gitlab main  {NU}").read())
        print("# ",os.popen(f"git push --tags").read())
        os.system(f"pip uninstall {SA} -y")
        os._exit(0)
    else:
        if (not moon)  or (not pypi):
            print("@ [缺少環境] api 或 moon @")
            #os._exit(0)
        



#####
##################################################################
# if len(sys.argv)>=2 and moon and pypi and  "uninstall"  not  in sys.argv and  "del"  not  in sys.argv  and  "setup.py" not  in sys.argv  and r"-install" in sys.argv:
if len(sys.argv)>=2 and moon and pypi and  "uninstall"  not  in sys.argv and  "del"  not  in sys.argv  and  "setup.py" not  in sys.argv :
    print("@ [使用] user.api 認證 @")
    # NAA=sys.argv.index('-install')
    # sys.argv.pop(NAA) ## [抽出][-u] pop即刪除
    # sys.argv.insert(NAA,"install") ## [插入]

    # print(f"@ {sys.argv} @",os.environ["username"])
    args = sys.argv[1:]
    # if args is None:
    #     args = sys.argv[1:]
    if  "install" in sys.argv:
        NN = args.index("install")+1
        # KEY= os.environ["KEY"]
        if  args[NN].find(r"==")!=-1:
            SA,SB=args[NN].split(r"==")
            # print(f"@1 {SA} {SB}")
            args[NN]=f"git+https://{pypi}@gitlab.com/{moon}/{SA}@{SB}"
            # print(f"@1 {args} {pypi}")
        else:
            SA=args[NN]
            # print(f"@2 {SA}")
            args[NN]=f"git+https://{pypi}@gitlab.com/{moon}/{SA}"
            # print(f"@2 {args} {pypi}")
        ################################################################
        
        # print("@!! ",not pip_api( moon ,SA)  ) 
        if not pip_api( moon ,SA):
            import re
            # 定義正規表達式模式
            pattern = re.compile(r'^git\+https://[^/^@]+@gitlab\.com/[^/^@]+/[^/^@]+[@]?[^/^@]?$')
            args = sys.argv[1:]              ## 條件需要::不要移動 
            if  not pattern.match( args[NN] ):
                print(f"@ 專案 {SA} 不存在 @")
                os._exit(0)
        else:
            # print("@ SB ",  'SB' in globals() )
            if 'SB' in globals():
                # print("存在名为 SB 的变量")
                if  SB not in pip_tag( moon ,SA):
                    print(f"@ 目前沒有 {SB} 版本 @")
                    os._exit(0)
        ##############################
        # print(f"@ 專案 {SA} 存在 @")
        sys.argv=[sys.argv[0]]
        sys.argv.extend( args )
        # print("@ argv @",sys.argv)
        ##############################
 



