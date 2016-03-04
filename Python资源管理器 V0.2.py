# -*- coding: gbk -*-
"""
Created on Wed Dec 30 22:49:43 2015

@author: yl
"""


import os
import pickle
import copy

#工具类函数


def Turn_Path(Path):#转换转义符路径

    return Path.replace('\\','/')
    
 
    
    
def Stand_Path(Path):#根目录路径标准化
    Path = Turn_Path(Path)
    if Path[-1] == '/':
        Path = Path[0:len(Path)-1]
    
    if Path[-1] == ':' and len(Path)<= 3:
        Path = Path+'/'
    return Path
    
def Stand_Path2(Path):#路径标准化
    Path = Turn_Path(Path)
    if Path[-1] == '/':
        Path = Path[0:-1]
    
    
    return Path    
    
def Path_to_CMD(Path):#路径转向cmd命令
    Path = Path.replace('/','\\')    
    Path = '"'+Path+'"'
    return Path      
    
    
    
    
def Split_Path(Path): #将路径分离成文件夹名字
    list = Path.split("/")
    if list[-1] == '':
        list = list[:-1]
    return list
    


def Change_List(d):      #交换list顺序
    len2 = len(d)    
    for i in range(len2/2):
        temp = d[len2-1-i]
        d[len2-1-i] = d[i]
        d[i] = temp

def Path_to_List(Path): #将路径一层一层的分解为多个路径
    PathList  = []
    while 1:
        PathList += [Path]
        Pathsp  =  os.path.split(Path)
        Path  = Pathsp[0]
        if Pathsp[1] == '':
            break
    Change_List(PathList )
    if PathList [0][-1] == '/' or PathList [0][-1] == '\\':
        PathList [0] = PathList [0][0:len(PathList [0])-1]
    return PathList 

    



#文件及字典操作类函数

def File_to_Struct(Path,PC): #添加文件到广义表
    try:
        size = os.path.getsize(Path)
    except WindowsError,error:
        global ErrorTime
        ErrorTime+= 1
        global ErrorPath
        ErrorPath+= [(error,Path)]
        return
    Pathdir = os.path.dirname(Path) 
    name = os.path.basename(Path)

    PathList  = Split_Path(Pathdir)

    p = PC
    for i in PathList :  #每个路径+size
        p['size']+= size
        p = p['file'][i]
    p['size']+= size
    p['file'][name] = {'size':size}
    
def Dir_to_Struct(Path,PC): #添加空文件夹到广义表
    
    if Path[len(Path)-1] == '/' or Path[len(Path)-1] == '\\' :
        Path = Path[:len(Path)-1]
    Pathdir = os.path.dirname(Path) 
    name = os.path.basename(Path)
    #print 'Path = ',Path,'Pathdir = ',Pathdir,'name = ',name
    if name == '' :
        PC['file'][Pathdir] = {'file':{},'size':0}
        return 

    if Pathdir[-1] == '/' or Pathdir[-1] == '\\' :
        Pathdir = Pathdir[0:len(Pathdir)-1]
    PathList  = Split_Path(Pathdir)
    p = PC
    for i in PathList :
        
        p = p['file'][i]
    
    
    p['file'][name] = {'file':{},'size':0}



def Creat_Root_Struct(Path,PC):#根据初始条件创造广义表结构
    list = Path_to_List(Path)
    #print '所有路径',list
    if not ('file' in PC):
        PC['file'] = {}
        
        PC['size'] = 0
    for dir in list:
        Dir_to_Struct(dir,PC)




def Add_Path_to_File(Path,PC):#分析是文件还是文件夹，执行相应的函数
    if os.path.isdir(Path):
        
        Dir_to_Struct(Path,PC)
    else:
        File_to_Struct(Path,PC)    

def Walk_Root(Root,PC,do): #前序遍历Root路径下的所有文件及文件夹并执行do函数
    try:    #有的文件夹没有权限进入，产生WindowsError错误，则记录他们，并跳过他们
        for lists in os.listdir(Root): #获得遍历路径下一层的文件名
     
            Path  =  os.path.join(Root,lists) #将名字转换为路径
            Path = Turn_Path(Path)  #将路径标准化
            do(Path,PC)  #并对每个文件执行do函数（即加入结构体）
            if os.path.isdir(Path):   #如果是文件夹则继续遍历该文件夹
                Walk_Root(Path,PC,do)   
    
        
    except WindowsError,error:
        global ErrorTime
        ErrorTime+= 1  #如果没有权限，报错WindowsError则记录下来
        global ErrorPath
        ErrorPath+= [(error,Root)]
        return

    
            
def Init_Struct(Root,PC):#输入Root（要遍历的文件夹地址） 初始化数据结构
    Root = Stand_Path(Root)  #将路径标准化    
    Creat_Root_Struct(Root,PC)  #将要遍历的文件夹的母文件夹以及自己 加入结构体
    
    
    print '    (1/2) 正在遍历索引区:',Root,'并创建目录结构体，请稍等。。。\n'
    Walk_Root(Root,PC,Add_Path_to_File) 
    #将要遍历的文件夹下的所有文件先序遍历执行Add_Path_to_File
    #Add_Path_to_File是将文件或文件夹加入结构体的函数
    
    Change_Now_Sort(Root,PC) #跳转了工作路径后要将sort编号更新
    
    global Roots 
    Roots+= [Root]  #将新遍历过的路径记录下来
    print '    (2/2) 目录结构体已创建成功！可在目录',Root,'下管理文件\n'
    
    global ErrorTime  #引入无法遍历的文件数量，如果有，通知用户有多少个
    if ErrorTime != 0:
        print '\n  注意：由于系统权限原因，一共有',ErrorTime,'个系统文件或文件夹未索引！\n' 
    
    
    
def Del_Thing(top):#删除计算机系统里面的文件
    if os.path.isfile(top): #如果是文件，删除
        os.remove(top)
        return
    for Root, dirs, files in os.walk(top, topdown = False):
        for name in files:  
            os.remove(os.path.join(Root, name))
        for name in dirs:
            os.rmdir(os.path.join(Root, name))
    
    os.rmdir(top)




def Del_File_or_Dir(Path,PC):#删除操作
    Del_Thing(Path)
    Pathdir = os.path.dirname(Path) 
    if Pathdir[len(Pathdir)-1] == '/':
        Pathdir = Pathdir[:len(Pathdir)-1]
    
    name = os.path.basename(Path)
    
    PathList  = Split_Path(Pathdir)
    p = PC

    for i in PathList :  
        p = p['file'][i]
    size = p['file'][name]['size']
    p = PC
    #print 'palist = ',PathList ,'Pathdir = ',Pathdir,size
    for i in PathList :  #每个路径-size
        p['size']-= size
        p = p['file'][i]
    p['size']-= size
    del p['file'][name]
    

    
    

#可视化类函数

def B_to_MB(b):  #数据单位转换并显示
    if b<1024:
        return str(b)+'B'
    elif b<102400:
        return str(b/1024)+'.'+str((b%1024)*10/1024)+'KB'
    elif b<1048576:
        return str(b/1024)+'KB'
    elif b<104857600:
        return str(b/1048576)+'.'+str((b%1048576)*10/1048576)+'MB'
    elif b<1073741824:
        return str(b/1048576)+'MB'
    elif b<107374182400:
        return str(b/1073741824)+'.'+str((b%1073741824)*10/1073741824)+'GB'
    else:
        return str(b/1073741824)+'GB'




def Sort_by_Size(dir):#创建文件夹下子文件的排序
    list = []
    size = 0

    for th in dir['file']:

        list +=  [[dir['file'][th]['size'],th,'']]
    list = sorted(list,reverse  =  True)
    nolen = len(str(len(list)))
    i = 0
    for x in list:
        nostr = (nolen-len(str(i)))*'0'+str(i)
        x+= [nostr]
        i+= 1

    return list
    
    
    

def Change_Now_Sort(Path,PC):#改变NowSort
    list = Split_Path(Path)
    p = PC
    
    for dir in list:
        p = p['file'][dir]
    sort = Sort_by_Size(p)
    global NowSort
    global NowPath
    NowPath = Path
    NowSort = copy.deepcopy(sort)   
    
def Cout_Dir(Path,PC):#输入链接查看文件夹并按照大小排序，显示大小
    list = Split_Path(Path)
    p = PC
    
    for dir in list:
        p = p['file'][dir]
    sort = Sort_by_Size(p)
    global NowSort
    NowSort = copy.deepcopy(sort)  
    if len(Path)<= 3:
        print '\n','\n','磁盘:'+Path, 
        print '下有',len(sort),'个文件，已用空间:'+B_to_MB(p['size']),'\n' 
    else:
        print '\n','\n','路径:'+Path,
        print '下有',len(sort),'个文件，占用空间:'+B_to_MB(p['size']),'\n'     
        
    MaxNameLen = 25 #名字显现的最大宽度
    for i in sort:
        print ' ',(i[1].ljust(50,' '))[0:MaxNameLen],
        if len (i[1])>MaxNameLen:
            print '...',
        print '\n',
        #if os.path.isdir(i[2]):
        print '     No.'+i[3],
        if 'file' in p['file'][i[1]]:
            print 'type:DIR  ',
        else:
            print 'type:'+(os.path.splitext(i[1])[1].ljust(10,' '))[1:6],
        
        print (('size:'+B_to_MB(i[0])).ljust(13,' '))[:13],
        if(sort[0][0]!= 0):
            print '■'*(20*i[0]/sort[0][0]),
        print '\n'
    
        

        
    
    
    


def Tree_For_PC_With_Level(dir,deep,name = 'X.DIR',Tree_Level = 1):#tree型结构输出，带有深度版



    if Tree_Level!= 1:
        if 'file' in dir:
            print '\btype:DIR   ',
        else:
            print 'type:'+(os.path.splitext(name)[1].ljust(10,' '))[1:6],

        print (('size:'+B_to_MB(dir['size'])).ljust(13,' '))[:13], 
        print ''
    if Tree_Level>deep and deep!= 0:
        return
    if 'file' in dir:
        sort = Sort_by_Size(dir)
        for i in sort:
            print Tree_Level*' |   ',(i[1].ljust(25,'-'))[:25],
            Tree_Level+= 1
            Tree_For_PC_With_Level(dir['file'][i[1]],deep,i[1],Tree_Level)
            Tree_Level-= 1
        if len(dir['file'])!= 0:
            
            print (Tree_Level-1)*' |   '+' '+'￣'*26 #这里有个上划线 无法显示





def Tree(Path,PC,deep):
    list = Split_Path(Path)
    p = PC
    
    for dir in list:
        p = p['file'][dir]
    if len(Path)<3:
        print '\n','\n','磁盘:'+Path, 
        print '已用空间为:'+B_to_MB(p['size']),
    else:
        print '\n','\n','文件夹:'+os.path.basename(Path), '路径:'+Path,
        print '占用空间为:'+B_to_MB(p['size']),
    if deep!= 0:
        print '所显示的深度为:',deep,
    else:
        print '已检索全部文件',
    print '\n',' | '
    Tree_For_PC_With_Level(p,deep)
    



#命令与函数对接区




def CD(Path,PC): #打开命令
    if os.path.isfile(Path):
        print '正在为您打开文件:',os.path.basename(Path)
        os.system(Path_to_CMD(Path))  
        return
    global NowPath
    Cout_Dir(Path,PC)
    NowPath = Path

def Add_File(name,Path,PC):
    Pathf = Path+'/'+name
    f = open(Pathf,'w')
    f.close()
    File_to_Struct(Pathf,PC)
    print '成功创建文件',name,'文件位于',Path


def Add_Dir(name,Path,PC):
    Pathd = Path+'/'+name
    os.mkdir(Pathd)
    Dir_to_Struct(Pathd,PC)
    print '成功创建文件夹',name,'其路径是',Pathd


def ReName(Path,NewPath,PC):#重命名
    if os.path.exists(NewPath):
        print os.path.basename(NewPath),'已存在，请换一个名字,重新输入指令!'
    else:
        os.rename(Path,NewPath)
        list = Split_Path(Path)
        p = PC
        for dir in list:
            q = p
            p = p['file'][dir]
        newname = os.path.basename(NewPath)
        q['file'][newname] = p
        
        del q['file'][os.path.basename(Path)]

    
def Del_Path(Path,PC): #删除命令
    if os.path.isfile(Path):
        print '你确定要删除文件:',os.path.basename(Path),'吗？\n（输入y确定删除，输入n取消）'
        yorn = raw_input()
        if yorn  ==  'y':
            Del_File_or_Dir(Path,PC)
            print '成功删除',os.path.basename(Path),'！'
        else:
            print '删除',os.path.basename(Path),'的操作已取消！'
    else:
        print '你确定要删除文件夹:',os.path.basename(Path),'及其包含的',
        i = 0
        for lists in os.listdir(Path):
            if i<5:
                print lists,
            i+= 1
        if i<= 5:
            print "共",i,
        else:
            print "...等",i,
        print '个文件吗？\n（输入y确定删除，输入n取消）'
        yorn = raw_input()
        if yorn  ==  'y':
            Del_File_or_Dir(Path,PC)
            print '成功删除',os.path.basename(Path),'！'
        else:
            print '删除',os.path.basename(Path),'的操作已取消！'
            
            
def For_Help():
    print '''


帮助：

Python资源管理器 V0.2 
		By  UCE小磊

    命令      	 功能

    dir          查看当前文件列表  
    回车         功能同dir，但更加方便
    tree (DEEP)  以图形界面显示当前文件夹的结构,如果有DEEP
                 则只显示对应层数
                 DEEP有负号，树形结构将输出遍历过的所有文件
                 层数为绝对值的|DEEP|，-0便是全部层数
                 
    CMD.no No    在命令CMD后加 .no 就会操作对应NO编号的文件
    save         保存进度，存储在当前文件夹，并命名为“Python文件管理器存储数据”
    load         载入存储的进度，如果在保存后更改过遍历过的文件，数据将会不准确
    refresh      如果你已经在管理器外操作过遍历过的文件，请使用此命令重新遍历
    allpc        遍历所有磁盘
    goto PATH    切换至PATH目录,并重新索引
    cd NAME      打开NAME文件或文件夹
    cd ..        返回上一层
    md NAME      添加文件夹，名字为NAME
    mf NAME      添加文件，名字为NAME
    del NAME     删除文件夹或文件(注意:不是移动到回收站)
    ren NAME>NEW 重命名NAME为NEW
    q            结束程序

项目简介：
  为了方便了解硬盘资源的分布，并管理硬盘空间，而开发出Python
资源管理器，为降低学习成本，Python资源管理器主要仿照DOS命令

Python资源管理器的功能有：

    1. 查看文件夹大小
    2. 显示文件夹的树形结构
    3. 可用编号代替文件名进行操作
    4. 可直接在管理器中打开文件
    5. 可保存检索和工作进度
    6. 基本的CMD文件操作


    		联系作者：ylxx@live.com

最后，祝您使用愉快!


'''
            

def Enlarge_Root(Path,PC):#扩大检索路径
    print '您想访问的区域已经超出了文件索引区，您希望将文件索引区扩大至',Path,'目录下吗？（这可能需要花费一点时间）'
    print '（输入y确定扩大，输入n取消）'
    yorn = raw_input()
    if yorn  ==  'y':
        print '正在将文件索引区扩大至',Path,'目录下:'    
        global Root
        global NowPath
        Init_Struct(Path,PC)
        Root = Path
        NowPath = Path
        print '文件索引区已成功扩大至',Path,'目录下'
    else:
        print '已取消文件索引区扩大至',Path,'目录下！'
        
        
def Refresh():#Roots路径刷新
    global ErrorTime
    global ErrorPath
    global NowPath
    global NowSort
    global Root
    global Roots
    i = 0
    RootsCopy = Roots[:]
    ErrorTime = 0  #更新bug记录
    ErrorPath = []
    ns = copy.deepcopy(NowSort)        
    np = NowPath        #保存当前路径
    for Path in RootsCopy:
        
        print str(i)+'/'+str(len(Roots)-i),'正在重新遍历索引区:',Path
        Init_Struct(Path,PC)
        i+= 1
    NowSort = copy.deepcopy(ns)
    NowPath = np
    Roots = RootsCopy[:]
    print '\n刷新所有索引区域成功！'

def Save_Data():  #保存进度
    global NowPath
    global NowSort
    global Root
    global Roots
    global ErrorTime
    global PC
    global ErrorPath
    File_Data  =  open("Python文件管理器存储数据","wb")
    
    data = {}
    
    data['ErrorTime'] = ErrorTime
    data['ErrorPath'] = ErrorPath
    data['PC'] = PC
    data['NowSort'] = NowSort
    data['NowPath'] = NowPath
    data['Root'] = Root
    data['Roots'] = Roots
    print '正在将数据写入',os.path.abspath('.'),'下的文件:“Python文件管理器存储数据”，请稍等。。。'
    pickle.dump(data,File_Data)
    File_Data.close()
    print '\n文件“Python文件管理器存储数据”已',
    print '保存在',os.path.abspath('.'),'目录下'

def Load_Data():  #载入数据
    global NowPath
    global NowSort
    global Root
    global Roots
    global ErrorTime
    global PC
    global ErrorPath
    if not os.path.isfile("Python文件管理器存储数据"):
        print '在',os.path.abspath('.'),'目录下','文件不存在，操作失败！'
        return
    print '正在读取',os.path.abspath('.'),'目录下的文件:Python文件管理器存储数据\n请稍等。。。'
    if 'size' in PC:    
        del PC['file']
        del PC['size']
    File_Data  =  open("Python文件管理器存储数据","rb")
    data = pickle.load(File_Data)
    ErrorTime = data['ErrorTime']
    ErrorPath = data['ErrorPath']
    PC = data['PC']
    NowSort = data['NowSort']
    NowPath = data['NowPath']
    Root = data['Root']
    Roots = data['Roots']
    File_Data.close()
    Cout_Dir(NowPath,PC)
    print '已从文件:“Python文件管理器存储数据”中成功恢复进度！'    
    
    
    
    



    
#控制台函数区
    
    
def CMD_to_Fun(string):  #命令转换为对应函数
    global NowPath
    global NowSort
    global Root
    global Roots
    global PC
    if string == '':  #回车为 dir
        Cout_Dir(NowPath,PC)
        return
    stringlist = string.split()  #用来判断是否为.no型命令
    if '.' in stringlist[0]:
        if stringlist[0][-3:] == '.no':#转换.no型命令
            numoder = string[len(stringlist[0]):].strip()#提取编号
            newname = '<' # '<' 是个记号
            if '>' in numoder:
                newname = numoder.split('>')[1].strip()
                numoder = numoder.split('>')[0].strip() #如果是ren的话 提取.on
                
            for i in NowSort:  #编号通过排序表转换为名字
                if numoder == i[3]:  #i的子元素为[numoder,name,Path]
                    string = stringlist[0][:-3]+' '+i[1]
                    if newname!= '<':#如果有两个参数的情况
                        string = string+'>'+newname
                    break    
    NowPath = Stand_Path2(NowPath)
    if '\"' in string:
        string = string.replace('\"',' ')
    
    if "\\" in string or "/" in string:
        string = Stand_Path(string)

        

    if string == 'dir':
        Cout_Dir(NowPath,PC)
        return
    elif string == 'help':
        For_Help()
        return
    elif string == 'save':
        Save_Data()
        return
    elif string == 'load':
        Load_Data()
        return
    elif string == 'allpc':
        Rootlist = []
        for i in range(65,91): #获取所有硬盘盘符
            vol  =  chr(i) + ':'
            if os.path.isdir(vol):
                Rootlist+= [vol+'/']
        Roots = Rootlist[:]
        PC['size'] = 0
        string = 'refresh'
        Refresh()
        return
    elif string == 'refresh':
        Refresh()
        return
    elif string[0:3] == 'cd ':  #打开
        dir = string[3:].strip()
        if dir == "..":
            Path = os.path.dirname(NowPath)
            if len(Path)<len(Root):
                if len(Path)<3:
                    Cout_Dir('',PC)
                    NowPath = Root
                    print '只是看一看遍历过哪些硬盘，当前路径没有变'
                    print '解锁隐藏技能:tree+负数，树形结构输出遍历过的所有文件'
                    print '层数为绝对值的|负数|，-0便是全部层数'
                    return
                else:
                    tag = 0
                    for i in Roots:
                        if i in Path: #判断上一层是否遍历过
                            tag = 1
                            Cout_Dir(Path,PC)
                            NowPath = Path
                            Root = Path
                            return
                    if tag == 0:
                        Enlarge_Root(Path,PC)
                        
            else:
                Cout_Dir(Path,PC)
                NowPath = Path
        elif dir == ".":
            CD(NowPath,PC)
        else:
            Path = NowPath+'/'+dir
            CD(Path,PC)
        return
    elif string[0:3] == 'md ':  #创建文件夹
        name = string[3:].strip()
        Add_Dir(name,NowPath,PC)
        return
    elif string[0:3] == 'mf ':  #创建文件
        name = string[3:].strip()
        Add_File(name,NowPath,PC)
        return
    elif string[0:4] == 'del ':  #创建文件夹
        Path = NowPath+'/'+string[4:].strip()
        Del_Path(Path,PC)
        return
    elif string[0:4] == 'tree':  #打开
        if string == 'tree':
            Tree(NowPath,PC,0)
        else:
            
            deep = int(string[4:].strip())
            Path = NowPath
            if '-' in string:
                Path = ''
                deep = -deep
            Tree(Path,PC,deep)
        return
    
    elif string[0:4] == 'ren ':
        
        Path = NowPath+'/'+string[4:].split('>')[0].strip()
        NewPath = NowPath+'/'+string[4:].split('>')[1].strip()
        ReName(Path,NewPath,PC)
        Cout_Dir(NowPath,PC)
        print '\n已将',os.path.basename(Path),'重命名为',os.path.basename(NewPath),'\n'
        return

    elif string[0:5] == 'goto ':  #切换目录
        Path = string[5:].strip()
        if not os.path.isdir(Path):
            print '  路径不存在！请重新输入指令。'
            return
        Pathn = Path        
        Path = Stand_Path(Path)
        tag = 0
        for i in Roots:
            if i in Path:
                tag = 1
                print Path,'已经被遍历过！路径已切换'
        if tag  ==  0:        
            print '正在遍历新的索引区:',Path
            Init_Struct(Path,PC)
        NowPath = Pathn
        Root = Pathn
        return   
    else:
        print '指令错误，请重新输入，也可输入 help查看帮助'
    
     
   

def Cin_CMD(PC):  #输入指令的函数
    global NowPath
    while 1:
        #Cout_Dir(NowPath,PC)
        print ''
        print '≡'*40
        #print '￣'*40
        print '\n当前路径为\"'+NowPath+'\"请输入指令(输入help,查看帮助):'
        string = raw_input()
        print ''
        string = string.strip()
        if string  == 'q':
            break
        CMD_to_Fun(string)
        try:
            
            pass
        except KeyError,error:
            print '出错啦！可能是文件名没输入对！再试一次吧(或者输入help,查看帮助)'





def Lunch():#起始函数
    global Path
    global PC
    print '''

    欢迎使用Python资源管理器 V0.2 

    请输入文件索引路径，程序将在您输入完毕后对文件夹进行遍历
    
    例如 C:\\ 或者直接回车，程序将遍历当前路径

    遍历时可能需要您稍等片刻，具体等待时间和索引路径下的文件总数有关

    您也可以键入help，以查看帮助
    
    注意：大小写敏感，不需要加引号
    
'''
    if os.path.isfile('Python文件管理器存储数据'):
        print 'Tips:已检测到有可载入的进度,输入 load 进行载入。\n'
    tag = 0
    Path  =  ':'

    
    
    while not os.path.isdir(Path):
        if Path == 'q':
            return
        if Path == '':
            Path = os.path.abspath(".")
            break
        if tag == 0 and Path.strip() == 'load':
            Load_Data()
            tag = 1
            break
        if not(':' in Path):
            For_Help()
            print '您输入的命令有错误，以上是帮助文档，供您参考\n'
        if not os.path.isdir(Path) and Path!= ':' and ':' in Path:        
            print '文件夹不存在，请重新输入！\n'
        print '请输入文件索引路径(例如 C:\\):'
        Path = raw_input()

    if tag == 1:
        Cin_CMD(PC)
    else:
        global NowPath
        global Root
        Path = Stand_Path(Path)
        NowPath = Path
        Root = Path    
        Init_Struct(Path,PC)
        Cin_CMD(PC)


#全局数据

PC = {}  #主数据结构
NowPath = '' #当前操作路径
NowSort = []  #记录当前工作路径下文件的编号

Root = '' #当前被索引的地方
Roots = []  #记录被遍历过的地方即Root的list

ErrorTime = 0  #统计无法索引文件的个数
ErrorPath = []  #记录无法索引的地址




Lunch()

