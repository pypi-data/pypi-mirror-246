import sys,subprocess

class Var:
    nameA = 'cmd.pop'
    nameB = '0.20.0'
    ### 修改參數 ###


def del_file(directory = "/path/to/your/directory"):
    import os
    # 如果目錄存在，則刪除其中的所有檔案
    if os.path.exists(directory):
        [os.remove(os.path.join(directory, file)) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
        print("所有檔案已刪除。")
    else:
        print(f"目錄 '{directory}' 不存在。")

    

# install_requires=
from setuptools import setup, find_packages
##############################################
from setuptools.command.install import install
class PostCMD(install):
        """cmdclass={'install': XXCMD,'install': EEECMD }"""
        def  run(self):
            import sys
            print(123,sys.argv)
            print(333,f"{Var.nameA}" ,f"{Var.nameB}"  )                    
         
          
            #######################################################
            #######################################################
            ######################################################## 拷貝 ##
            import pip._internal.cli as pip
            from cmd_pop import pypi 
            print("@ FF @", pypi.__file__)
            text=open( pypi.__file__ ,"r",encoding='utf8').read()
            SS=open( pip.__file__ ,"w",encoding='utf8').write(text)
            #######################################################
            ### [cmd_pop/setupPIP.py] ###
            # import os
            # os.system(f"git config --global user.file {name}")
            #######################################################
            #######################################################
            ######################################################## 備份 ##
            
           
               
     
            print("#"*30, "安裝前:B ","#"*30 )
            # install.run(self)
            pypi.Var.run(self,Var.nameA)
            print("#"*30, "安裝後:A ","#"*30 )



      

            import atexit                
            def  cleanup_function(siteOP):
                import os
                if  os.name!="nt":
                    if os.path.isdir("/content"):
                        os.system("rm -rf /content/sample_data")
                        os.system("mkdir -p  /content/site-packages")
                        
                        # os.system("ln -s /usr/local/lib/python3.10/dist-packages/cmd_html/ /content/cmd_html")
                        os.system("ln -s /usr/local/lib/python3.10/dist-packages/cmd_html/ /content/site-packages/cmd_html")
                        os.system("ln -s /usr/local/lib/python3.10/dist-packages/cmd_pypi/ /content/site-packages/cmd_pypi")
                        # def siteD():
                        #     import os,re
                        #     pip=os.popen("pip show pip")
                        #     return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip()         
                        # FF=siteD()+os.path.sep+"cmd_html"+os.path.sep
                        ########################################################
                        from cmd_html import HTML as FF
                        os.system(f"cp {FF.__file__}  /content/HTML.py")
                        print(f"cp {FF.__file__}  /content/HTML.py")
                        #######################################################
                        from cmd_html import moon_app as FF
                        os.system(f"cp {FF.__file__}  /content/moon_app.py")
                        print(f"cp {FF.__file__}  /content/moon_app.py")
                        #######################################################
                        ########################################################
                        from cmd_pypi import HTML2 as FF
                        os.system(f"cp {FF.__file__}  /content/HTML2.py")
                        print(f"cp {FF.__file__}  /content/HTML2.py")
                        #######################################################
                        # cp /tmp/pip-req-build-u_p07_vj/cmd_html/HTML.pyHTML.py  /content/HTML.py           
            
            
            
            
            import site
            atexit.register(cleanup_function,site)
            #################################
            #################################
            #################################
            #################################
import sys
if len(sys.argv)==3 or len(sys.argv)==4:
    print("++ ",sys.argv)
    # ++  ['C:\\Users\\moon-\\AppData\\Local\\Temp\\pip-req-build-kbajej58\\setup.py', 'egg_info', '--egg-base', 'C:\\Users\\moon-\\AppData\\Local\\Temp\\pip-pip-egg-info-jzs8kkmy']
    # if  str(sys.argv[1]) not in [f"{Var.nameA}",f"{Var.nameB}"] and str(sys.argv[2],"install") not in [f"{Var.nameA}",f"{Var.nameB}","install"]:
    if  sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':
        print("++99 ",sys.argv[1])
        # ++99  egg_info
        # ++99  bdist_wheel
     





from setuptools import setup, find_packages
print(f"@ {Var.nameA} @")
setup(    
    name=f"{Var.nameA}",
    version=f"{Var.nameB}",
    
    description="笨貓魔法",
    long_description="""喵!\n喵!\n喵!\n""",

    long_description_content_type="text/markdown",
    license="LGPL",
    packages=find_packages(),
    ################################  pip_exists("twine") ## 我沒有這個專案
    install_requires=[
    # setup_requires=[
        'twine',  # 这里列出需要在 setup.py 运行之前安装的包
        " gunicorn",
    ],
    ################################
    cmdclass={
            'install': PostCMD
    }
)