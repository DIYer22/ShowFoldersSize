# -*- coding: gbk -*-
"""
Created on Wed Dec 30 22:49:43 2015

@author: ylxx@live.com

这是我初学Pyhton时便开始的项目
许多代码结构不合适
也没按照编程规范
待后续版本进行重构,修整

"""
#from __future__ import unicode_literals

import os
import pickle
import copy
import webbrowser

#==============================================================================
# #工具类函数
#==============================================================================


def turn_path(Path):#转换转义符路径

    return Path.replace('\\','/')


def stand_path(Path):#根目录路径标准化
    Path = turn_path(Path)
    if Path[-1] == '/':
        Path = Path[0:len(Path)-1]

    if Path[-1] == ':' and len(Path)<= 3:
        Path = Path+'/'
    return Path


def stand_path2(Path):#路径标准化
    Path = turn_path(Path)
    if Path[-1] == '/':
        Path = Path[0:-1]
    return Path


def path_to_cmd(Path):#路径转向cmd命令
    Path = Path.replace('/','\\')
    Path = '"'+Path+'"'
    return Path


def split_path(Path): #将路径分离成文件夹名字
    list = Path.split("/")
    if list[-1] == '':
        list = list[:-1]
    return list

def change_list(d):      #交换list顺序
    len2 = len(d)
    for i in range(len2/2):
        temp = d[len2-1-i]
        d[len2-1-i] = d[i]
        d[i] = temp


def path_to_list(Path): #将路径一层一层的分解为多个路径
    PathList  = []
    while 1:
        PathList += [Path]
        Pathsp  =  os.path.split(Path)
        Path  = Pathsp[0]
        if Pathsp[1] == '':
            break
    change_list(PathList )
    if PathList [0][-1] == '/' or PathList [0][-1] == '\\':
        PathList [0] = PathList [0][0:len(PathList [0])-1]
    return PathList


def path_to_dir(path, dirr=None):
    '''将路径转换为结构体中对应的文件夹'''
    '''警告：不要在调用了PC中的函数再调用此函数,得直接加PC参数'''
    if dirr is None:
        global PC
        p = PC
    else:
        p = dirr        
    list = split_path(Path)
    
    for dir in list:
        p = p['file'][dir]
    return p
    


#==============================================================================
# 文件及字典操作类函数
#==============================================================================

def file_to_struct(Path,PC): #添加文件到广义表
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

    PathList  = split_path(Pathdir)

    p = PC
    for i in PathList :  #每个路径+size
        p['size']+= size
        p = p['file'][i]
    p['size']+= size
    p['file'][name] = {'size':size}


def dir_to_struct(Path,PC): #添加空文件夹到广义表

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
    PathList  = split_path(Pathdir)
    p = PC
    for i in PathList :
        p = p['file'][i]
    p['file'][name] = {'file':{},'size':0}


def creat_root_struct(Path,PC):#根据初始条件创造广义表结构
    list = path_to_list(Path)
    #print '所有路径',list
    if not ('file' in PC):
        PC['file'] = {}

        PC['size'] = 0
    for dir in list:
        dir_to_struct(dir,PC)


def add_path_to_file(Path,PC):#分析是文件还是文件夹，执行相应的函数
    if os.path.isdir(Path):

        dir_to_struct(Path,PC)
    else:
        file_to_struct(Path,PC)

def walk_root(Root,PC,do): #前序遍历Root路径下的所有文件及文件夹并执行do函数
    try:    #有的文件夹没有权限进入，产生WindowsError错误，则记录他们，并跳过他们
        for lists in os.listdir(Root): #获得遍历路径下一层的文件名

            Path  =  os.path.join(Root,lists) #将名字转换为路径
            Path = turn_path(Path)  #将路径标准化
            do(Path,PC)  #并对每个文件执行do函数（即加入结构体）
            if os.path.isdir(Path):   #如果是文件夹则继续遍历该文件夹
                walk_root(Path,PC,do)

    except WindowsError,error:
        global ErrorTime
        ErrorTime+= 1  #如果没有权限，报错WindowsError则记录下来
        global ErrorPath
        ErrorPath+= [(error,Root)]
        return


def init_struct(Root,PC):#输入Root（要遍历的文件夹地址） 初始化数据结构
    Root = stand_path(Root)  #将路径标准化
    creat_root_struct(Root,PC)  #将要遍历的文件夹的母文件夹以及自己 加入结构体


    print '    (1/2) 正在遍历文件夹:',Root,'并创建文件夹结构体，请稍等。。。\n'
    walk_root(Root,PC,add_path_to_file)
    #将要遍历的文件夹下的所有文件先序遍历执行add_path_to_file
    #add_path_to_file是将文件或文件夹加入结构体的函数

    change_now_sort(Root,PC) #跳转了工作路径后要将sort编号更新

    global Roots
    Roots+= [Root]  #将新遍历过的路径记录下来
    print '    (2/2) 文件夹结构体已创建成功！可管理在',Root,'路径下的文件\n'

    global ErrorTime  #引入无法遍历的文件数量，如果有，通知用户有多少个
    if ErrorTime != 0:
        print '\n  注意：由于系统权限原因，一共有',ErrorTime,'个系统文件或文件夹未索引！\n'


def del_thing(top):#删除计算机系统里面的文件
    if os.path.isfile(top): #如果是文件，删除
        os.remove(top)
        return
    for Root, dirs, files in os.walk(top, topdown = False):
        for name in files:
            os.remove(os.path.join(Root, name))
        for name in dirs:
            os.rmdir(os.path.join(Root, name))

    os.rmdir(top)


def del_file_or_dir(Path,PC):#删除操作
    del_thing(Path)
    Pathdir = os.path.dirname(Path)
    if Pathdir[len(Pathdir)-1] == '/':
        Pathdir = Pathdir[:len(Pathdir)-1]
    name = os.path.basename(Path)
    PathList  = split_path(Pathdir)
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



#==============================================================================
# #可视化类函数
#==============================================================================

def b_to_mb(b):  #数据单位转换并显示
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


def sort_by_size(dir):#创建文件夹下子文件的排序
    list = []
    size = 0

    for th in dir['file']:

        list +=  [[dir['file'][th]['size'],th,'']]
    list = sorted(list,reverse = True)
    nolen = len(str(len(list)))
    i = 0
    for x in list:
        nostr = (nolen-len(str(i)))*'0'+str(i)
        x+= [nostr]
        i+= 1
    return list


def change_now_sort(Path,PC):#改变NowSort
    list = split_path(Path)
    p = PC

    for dir in list:
        p = p['file'][dir]
    sort = sort_by_size(p)
    global NowSort
    global NowPath
    NowPath = Path
    NowSort = copy.deepcopy(sort)


def cout_dir(Path,PC):#输入链接查看文件夹并按照大小排序，显示大小
    list = split_path(Path)
    p = PC

    for dir in list:
        p = p['file'][dir]
    sort = sort_by_size(p)
    global NowSort
    NowSort = copy.deepcopy(sort)
    if len(Path)<= 3:
        print '\n','\n','磁盘:'+Path,
        print '下有',len(sort),'个文件，已用空间:'+b_to_mb(p['size']),'\n'
    else:
        print '\n','\n','文件夹:'+Path,
        print '下有',len(sort),'个文件，占用空间:'+b_to_mb(p['size']),'\n'

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

        print (('size:'+b_to_mb(i[0])).ljust(13,' '))[:13],
        if(sort[0][0]!= 0):
            print '■'*(20*i[0]/sort[0][0]),
        print '\n'


def tree_for_pc_with_level(dir,deep,name = 'X.DIR',Tree_Level = 1):#tree型结构输出，带有深度版



    if Tree_Level!= 1:
        if 'file' in dir:
            print '\btype:DIR   ',
        else:
            print 'type:'+(os.path.splitext(name)[1].ljust(10,' '))[1:6],

        print (('size:'+b_to_mb(dir['size'])).ljust(13,' '))[:13],
        print ''
    if Tree_Level>deep and deep!= 0:
        return
    if 'file' in dir:
        sort = sort_by_size(dir)
        for i in sort:
            print Tree_Level*' |   ',(i[1].ljust(25,'-'))[:25],
            Tree_Level+= 1
            tree_for_pc_with_level(dir['file'][i[1]],deep,i[1],Tree_Level)
            Tree_Level-= 1
        if len(dir['file'])!= 0:

            print (Tree_Level-1)*' |   '+' '+'￣'*26 #这里有个上划线 无法显示


def tree(Path,PC,deep):
    list = split_path(Path)
    p = PC

    for dir in list:
        p = p['file'][dir]
    if len(Path)<3:
        print '\n','\n','磁盘:'+Path,
        print '已用空间为:'+b_to_mb(p['size']),
    else:
        print '\n','\n','文件夹:'+os.path.basename(Path), '路径:'+Path,
        print '占用空间为:'+b_to_mb(p['size']),
    if deep!= 0:
        print '所显示的深度为:',deep,
    else:
        print '已检索全部文件',
    print '\n',' | '
    tree_for_pc_with_level(p,deep)



#==============================================================================
# #命令与函数对接区
#==============================================================================




def CD(Path,PC): #打开命令
    if os.path.isfile(Path):
        print '正在为您打开文件:',os.path.basename(Path)
        os.system(path_to_cmd(Path))
        return
    global NowPath
    cout_dir(Path,PC)
    NowPath = Path

def add_file(name,Path,PC):
    Pathf = Path+'/'+name
    f = open(Pathf,'w')
    f.close()
    file_to_struct(Pathf,PC)
    print '成功创建文件',name,'文件位于',Path


def add_dir(name,Path,PC):
    Pathd = Path+'/'+name
    os.mkdir(Pathd)
    dir_to_struct(Pathd,PC)
    print '成功创建文件夹',name,'其路径是',Pathd


def rename(Path,NewPath,PC):#重命名
    if os.path.exists(NewPath):
        print os.path.basename(NewPath),'已存在，请换一个名字,重新输入指令!'
    else:
        os.rename(Path,NewPath)
        list = split_path(Path)
        p = PC
        for dir in list:
            q = p
            p = p['file'][dir]
        newname = os.path.basename(NewPath)
        q['file'][newname] = p

        del q['file'][os.path.basename(Path)]


def del_path(Path,PC): #删除命令
    if os.path.isfile(Path):
        print '你确定要删除文件:',os.path.basename(Path),'吗？\n（输入y确定删除，输入n取消）'
        yorn = raw_input('\n>>>')
        if yorn  ==  'y':
            del_file_or_dir(Path,PC)
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
        yorn = raw_input('\n>>>')
        if yorn  ==  'y':
            del_file_or_dir(Path,PC)
            print '成功删除',os.path.basename(Path),'！'
        else:
            print '删除',os.path.basename(Path),'的操作已取消！'


def for_help():
    print '''


帮助：

UCE文件夹大小查看器 V0.40

		By  BUCT-UCE小磊
  
  
功能有：

    1. 查看文件夹大小
    2. 显示文件夹的树形结构
    3. 从遍历过的文件中找出最大的几个文件
    4. 分析各文件类型占用空间
    5. 可用编号代替文件名进行操作
    6. 可直接在管理器中打开文件
    7. 可保存检索和工作进度
    8. 基本的CMD文件操作


    命令      	 功能

    dir          查看当前文件列表
    回车         功能同dir，但更加方便
    cd NAME      打开NAME文件或文件夹
    cd ..        返回上一层文件夹
    del NAME     彻底删除文件夹或文件(注意:不是移动到回收站)
    goto PATH    遍历PATH路径,并切换至PATH路径
    top NUM      显示最大的NUM个文件
                 可不填NUM，默认是10(NUM为负数表示全局的意思)
                 
    tree DEEP    以图形界面显示当前文件夹的结构,如果有DEEP
                 则只显示对应层数
                 DEEP有负号，树形结构将输出遍历过的所有文件
                 层数为绝对值的|DEEP|，-0便是全部层数

    CMD.no No    在命令CMD后加 .no 就会操作对应NO编号的文件
                 例如:cd.no 01 打开第编号为01的文件夹
                 
    save         保存进度，存储在当前文件夹
                 并命名为“UCE文件夹大小查看器_存储数据”
                 
    load         载入存储的进度，如果在保存后更改过遍历过的文件，数据将会不准确
    refresh      如果你已经在管理器外操作过遍历过的文件，请使用此命令重新遍历
    allpc        遍历所有磁盘
    ana NUM      分析占用空间为前NUM大的各类文件类型
                 NUM默认为20(NUM为负数表示全局的意思)
                 
    md NAME      添加文件夹，名字为NAME
    mf NAME      添加文件，名字为NAME

    ren NAME>NEW 重命名NAME为NEW
    git          获得更新，查看Python源代码
    q            结束程序


项目简介：

  为了方便了解硬盘资源的分布，查看文件夹大小，并管理硬盘空间，而
  开发出UCE文件夹大小查看器，为降低学习成本，UCE文件夹大小查看器
  主要仿照DOS命令，和Pyhton风格
  (UCE是北京化工大学的计算机社团，我是其负责人)
  
  最后，祝您使用愉快!


    		联系作者：ylxx@live.com
      
    		帮助社团发展：请输入git指令
      
    		更新于2016/03/31      



'''


def enlarge_root(Path,PC):#扩大检索路径
    print '您想访问的区域已经超出了文件遍历区，您希望将文件遍历区扩大至',Path,'路径下吗？（这可能需要花费一点时间）'
    print '（输入y确定扩大，输入n取消）'
    yorn = raw_input('\n>>>')
    if yorn  ==  'y':
        print '\n\n正在将文件遍历区扩大至',Path,'路径下:\n'
        global Root
        global NowPath
        init_struct(Path,PC)
        Root = Path
        NowPath = Path
        print '文件遍历区已成功扩大至',Path,'路径下'
    else:
        print '已取消文件遍历区扩大至',Path,'路径下！'


def refresh():#Roots路径刷新
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

        print str(i)+'/'+str(len(Roots)-i),'正在重新遍历文件夹:',Path
        init_struct(Path,PC)
        i+= 1
    NowSort = copy.deepcopy(ns)
    NowPath = np
    Roots = RootsCopy[:]
    print '\n刷新所有遍历区域成功！'
    

class Top_box(object):
    '''top的容器'''
    def __init__(self,top=10):
        self.top = top
        self.box = []
        self.full = top
    def add(self,mix):
        size, name = mix
        l = self.box
        if l == []:
            self.box += [mix]
            return self.box[-1]
            
        lenn = len(l)
        i = 0
        while size < l[i][0]:
            i += 1
            if i == lenn:
                break
        self.box = l[:i] + [mix] + l[i:]
        self.box = self.box[:self.top]
#        return self.box[-1][0]
    
    def cmpp(self,mix):
        if self.box == []:
            self.add(mix)
            return 
        size, name = mix
        if self.full:
            minn = 0
            self.full -= 1
        else :
            minn = self.box[-1][0]
            
        if size > minn:
            self.add(mix)
    
    def __str__(self):
        strr = '\n'
        for i in self.box:
            strr += b_to_mb(i[0]).ljust(8,' ')[:8] + i[1] + '\n'
        
        return strr
            
    __repr__ = __str__


def the_top(top=10):
    '''
    获得最大的文件的列表
    '''
    
    def walk_root(dirr, strr=''):
        for things in dirr['file']:
            if 'file' in dirr['file'][things]:
                strr2 = strr + things + '/'
                walk_root(dirr['file'][things], strr2)
            else:
                strr2 = things + '\n        @' + strr + '\n'
                box.cmpp((dirr['file'][things]['size'],strr2))
                
    global PC  
    dirr = PC
    if top < 0:
        top = -top
        path = ''
        for_print =  '已遍历的文件中，最大的' + str(top) + '个文件：'
    else:
        global NowPath
        path = NowPath
        list = split_path(path)
        for dir in list:
            dirr = dirr['file'][dir]
        path += '/'
        for_print =  '当前文件夹下"' + path + '"下，最大的' + str(top) + '个文件：'
            
    box = Top_box(top)
                
    walk_root(dirr,path)     
    print for_print       
    print box
    print '\nTips:选中路径，单击右键便复制成功了！'


class Anysis(object):
    '''分析数据类型的占用空间'''
    def __init__(self, max_type=15):
        self.dic = {}
        self.max_type = max_type
    
    def add(self, size, key):
        key = key.lower()
        if key in self.dic:
            self.dic[key] += size
        else:
            self.dic[key] = size
        
    def get_type(self, size, name):
        index = name.rfind('.')
        if index < 0:
            self.add(size, 'None_Type')
        else:
            self.add(size, name[index+1:])

    def __str__(self):

        def dic_to_list(dic):
            listt = []
            for i in dic:
                listt += [(i,dic[i])]
            return listt
            
        listt = dic_to_list(self.dic)

        listt.sort(lambda x, y:-1 if x[1] > y[1] else 1)
        strr = '\n'
        for i in listt[:self.max_type]:
            strr += i[0].ljust(9,' ')[:9] + '  ' + b_to_mb(i[1]).ljust(8,' ')[:8] + '\n'
        
        return strr
            
    __repr__ = __str__        


def anysis(max_type=15):
    '''分析数据类型的占用空间'''
    global PC  
    dirr = PC
    if max_type < 0:
        max_type = -max_type
        for_print = '所有已遍历的文件中，各文件类型的占用情况：'
    else:
        global NowPath
        list = split_path(NowPath)
        for_print = '当前文件夹"' + NowPath + '"下，各文件类型的占用情况：'
        for dir in list:
            dirr = dirr['file'][dir]
        
    box = Anysis(max_type)
    
    def walk_root(dirr):
        for things in dirr['file']:
            if 'file' in dirr['file'][things]:
                walk_root(dirr['file'][things])
            else:
                box.get_type(dirr['file'][things]['size'], things)
    walk_root(dirr)
    print for_print
    print box
    

def save_data():  #保存进度
    global NowPath
    global NowSort
    global Root
    global Roots
    global ErrorTime
    global PC
    global ErrorPath
    File_Data  =  open("UCE文件夹大小查看器_存储数据","wb")

    data = {}

    data['ErrorTime'] = ErrorTime
    data['ErrorPath'] = ErrorPath
    data['PC'] = PC
    data['NowSort'] = NowSort
    data['NowPath'] = NowPath
    data['Root'] = Root
    data['Roots'] = Roots
    print '正在将数据写入',os.path.abspath('.'),'下的文件:“UCE文件夹大小查看器_存储数据”，请稍等。。。'
    pickle.dump(data,File_Data)
    File_Data.close()
    print '\n文件“UCE文件夹大小查看器_存储数据”已',
    print '保存在',os.path.abspath('.'),'路径下'


def load_data():  #载入数据
    global NowPath
    global NowSort
    global Root
    global Roots
    global ErrorTime
    global PC
    global ErrorPath
    if not os.path.isfile("UCE文件夹大小查看器_存储数据"):
        print '在当前路径：',os.path.abspath('.'),'下','文件不存在，操作失败！'
        return
    print '正在读取',os.path.abspath('.'),'路径下的文件:UCE文件夹大小查看器_存储数据\n请稍等。。。'
    if 'size' in PC:
        del PC['file']
        del PC['size']
    File_Data  =  open("UCE文件夹大小查看器_存储数据","rb")
    data = pickle.load(File_Data)
    ErrorTime = data['ErrorTime']
    ErrorPath = data['ErrorPath']
    PC = data['PC']
    NowSort = data['NowSort']
    NowPath = data['NowPath']
    Root = data['Root']
    Roots = data['Roots']
    File_Data.close()
    cout_dir(NowPath,PC)
    print '已从文件:“UCE文件夹大小查看器_存储数据”中成功恢复进度！'



#==============================================================================
# #控制台函数区
#==============================================================================


def CMD_to_Fun(string):  #命令转换为对应函数
    global NowPath
    global NowSort
    global Root
    global Roots
    global PC
    if string == '':  #回车为 dir
        cout_dir(NowPath,PC)
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
    NowPath = stand_path2(NowPath)
    if '\"' in string:
        string = string.replace('\"',' ')

    if "\\" in string or "/" in string:
        string = stand_path(string)



    if string == 'dir':
        cout_dir(NowPath,PC)
        return
    if string == 'ls':
        cout_dir(NowPath,PC)
        return
    elif string == 'git':
        webbrowser.open('https://github.com/DIYer22/ShowFoldersSize')
        return
    elif string[:3] == 'top':
        top = 10
        if len(string) > 4:
            top = int(string.split()[1])
        print '    请稍等。。。。\n\n'
        the_top(top)
        return
    elif string[:3] == 'ana':
        num = 20
        if len(string) > 4:
            num = int(string.split()[1])
        print '    请稍等。。。。\n\n'
        anysis(num)
        return
    elif string == 'help':
        for_help()
        return
    elif string == 'save':
        save_data()
        return
    elif string == 'load':
        load_data()
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
        refresh()
        return
    elif string == 'refresh':
        refresh()
        return
    elif string[0:3] == 'cd ':  #打开
        dir = string[3:].strip()
        if dir == "..":
            Path = os.path.dirname(NowPath)
            if len(Path)<len(Root):
                if len(Path)<3:
                    cout_dir('',PC)
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
                            cout_dir(Path,PC)
                            NowPath = Path
                            Root = Path
                            return
                    if tag == 0:
                        enlarge_root(Path,PC)

            else:
                cout_dir(Path,PC)
                NowPath = Path
        elif dir == ".":
            CD(NowPath,PC)
        else:
            Path = NowPath+'/'+dir
            CD(Path,PC)
        return
    elif string[0:3] == 'md ':  #创建文件夹
        name = string[3:].strip()
        add_dir(name,NowPath,PC)
        return
    elif string[0:3] == 'mf ':  #创建文件
        name = string[3:].strip()
        add_file(name,NowPath,PC)
        return
    elif string[0:4] == 'del ':  #创建文件夹
        Path = NowPath+'/'+string[4:].strip()
        del_path(Path,PC)
        return
    elif string[0:4] == 'tree':  #打开
        if string == 'tree':
            tree(NowPath,PC,0)
        else:
            deep = int(string[4:].strip())
            Path = NowPath
            if '-' in string:
                Path = ''
                deep = -deep
            tree(Path,PC,deep)
        return

    elif string[0:4] == 'ren ':

        Path = NowPath+'/'+string[4:].split('>')[0].strip()
        NewPath = NowPath+'/'+string[4:].split('>')[1].strip()
        rename(Path,NewPath,PC)
        cout_dir(NowPath,PC)
        print '\n已将',os.path.basename(Path),'重命名为',os.path.basename(NewPath),'\n'
        return

    elif string[0:5] == 'goto ':  #切换目录
        Path = string[5:].strip()
        if not os.path.isdir(Path):
            print '  路径不存在！请重新输入指令。'
            return
        Pathn = Path
        Path = stand_path(Path)
        tag = 0
        for i in Roots:
            if i in Path:
                tag = 1
                print Path,'已经被遍历过！路径已切换'
        if tag  ==  0:
            print '正在遍历新的文件夹:',Path
            init_struct(Path,PC)
        NowPath = Pathn
        Root = Pathn
        return
    else:
        print '指令错误，请重新输入，也可输入 help查看帮助'


def cin_cmd(PC):  #输入指令的函数
    global NowPath
    cout_dir(NowPath,PC)
    while 1:
        #cout_dir(NowPath,PC)
        print ''
        print '≡'*40
        #print '￣'*40
        print '\n当前路径为\"'+NowPath+'\"请输入指令(输入help,查看帮助):'
        string = raw_input('\n>>>')
        print ''
        string = string.strip()
        if string  == 'q':
            break
        
        try:
            CMD_to_Fun(string)
        except :
            print '\n\n出错啦！可能是文件名或者指令没输入对！再试一次吧(或者输入help,查看帮助)\n\n'

def lunch():#起始函数
    global Path
    global PC
    print '''

    欢迎使用UCE文件夹大小查看器 V0.40



    直接回车，程序将遍历当前路径 或者 输入待遍历路径 例如 C:\\ 

    遍历时可能需要您稍等片刻，具体等待时间和遍历路径下的文件总数有关

    您也可以键入help，以查看帮助

    注意：大小写敏感，不需要加引号

'''
    if os.path.isfile('UCE文件夹大小查看器_存储数据'):
        print '\nTips:已检测到有可载入的进度,输入 load 进行载入。\n'
    tag = 0
    Path  =  ':'

    while not os.path.isdir(Path):
        if Path == 'q':
            return
        if Path == '':
            Path = os.path.abspath(".")
            break
        if tag == 0 and Path.strip() == 'load':
            load_data()
            tag = 1
            break
        if not(':' in Path):
            for_help()
            print '您输入的命令有错误，以上是帮助文档，供您参考\n'
        if not os.path.isdir(Path) and Path!= ':' and ':' in Path:
            print '文件夹不存在，请重新输入！\n'
        print '≡'*40
        print '\n请直接回车 或 输入想遍历的路径(例如 C:\\):'
        Path = raw_input('\n>>>')

    if tag == 1:
        cin_cmd(PC)
    else:
        global NowPath
        global Root
        Path = stand_path(Path)
        NowPath = Path
        Root = Path
        init_struct(Path,PC)
        cin_cmd(PC)


#全局数据

PC = {}  #主数据结构
NowPath = '' #当前操作路径
NowSort = []  #记录当前工作路径下文件的编号

Root = '' #当前被索引的地方
Roots = []  #记录被遍历过的地方即Root的list

ErrorTime = 0  #统计无法索引文件的个数
ErrorPath = []  #记录无法索引的地址


lunch()

