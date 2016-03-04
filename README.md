# Python文件管理器设计报告



----------


>项目名称：`Python文件管理器`

>开发者：`杨磊`

>班级：`计科1403`

>联系方式：`ylxx@live.com`



 1. 项目目的和介绍
======

 作为一个计算机重度使用者，硬盘空间经常处于紧张状态，特别是C:\盘，C:\盘在固态硬盘上，无法扩展，而且C:\盘下的文件结构多而混乱,通常我会定期清理磁盘，但有以下问题：


 > * Windows资源管理器并不能提供文件夹大小的显示和排序，让我管理不方便
 > * 我还经常使用CMD命令 “tree”来查看文件夹结构，然而，tree命令过于简陋，无法满足我的需求。
 > * 且CMD命令下输入文件名长的文件或文件夹是十分痛苦的（例如名字超长的电影文件），我也想解决这个输入体验的问题

综上，这次课设我打算开发一个有特色功能的Python版资源管理器,以满足以上需求


 2. 功能设计
====
> * 实现基本的CMD文件操作
> * 可以默认显示文件夹大小
> * 漂亮的展示文件夹的树形结构
> * 可用编号代替文件名进行操作
> * 可保存检索和工作进度
> * 可直接在管理器中打开文件
注\[1]：复制和剪切功能将在后续版本加入
注[2]：后续版本将添加图形界面

 3. 核心思路
=====
###1. 开发语言
>由于Python语言应用性强，数据处理方便，开发周期短等优点，以及此项目对性能要求不高，瓶颈多为I/O操作，所以最终选择了Pyhton 2.7来开发此项目

###2. 用户使用逻辑
```flow
st=>start: Start:>https://www.zybuluo.com

op=>operation: 初始界面
cond=>condition: 是否载入进度?
sub=>operation: 载入工作进度
e=>end
op1=>operation: 由路径创造结构体
io2=>operation: 输入新的指令

io=>inputoutput: 输入指令
cond2=>condition: 是否为q？
op3=>operation: 初始界面2
st->op->cond
cond(no)->op1
cond(yes)->sub->io
op1->io->cond2->

sub2=>subroutine: 执行对应指令

cond2(yes)->e
cond2(no)->sub2(right)->io

```

<p>    </p>
<p>    </p>
<p>    </p>
<h1>  </h1>
###3. 问题的抽象
>要想知道文件夹的大小，就必须要知道文件夹下所有文件的大小，再相加
>文件夹与其下的文件的关系为树形关系
>因此，抽象数据结构为树，将路径下文件的树形结构和数据结构的树要一一对应
>由于我们主要目的是查看大小，因此还应在结构体中加入大小的数据


###3. 数据结构

由于文件夹本来就是一种树形结构，因此我考虑的是使用Python中的字典数据类型来表示的广义表，来表示树

用键表示文件名，其值为一个字典，字典的内容是文件的属性

>如一个1KB的文件的节点表示为:
`'文件名':{'size':1024}`

>如一个空文件夹的节点则表示为：
`'文件夹名':{'file':{},'size':0}`（键'file'对应的是字典）

>如果根文件夹中有子文件和子文件夹则：
`'根文件夹名':{'file':{'子文件名':{}，'子文件夹名':{}},'size':1024}`
文件夹的子文件放在键'file'对应的字典里面

>当然，所有文件，文件夹都应该在一个字典中，我命名为PC，即：
`PC={'file':{'根文件夹名':{}},'size':1024}`

###4. 重要数据
```python
#全局数据

PC = {}  #主数据结构
NowPath = '' #当前操作路径
NowSort = []  #记录当前工作路径下文件的编号

Root = '' #当前被索引的地方
Roots = []  #记录被遍历过的地方即Root的list

ErrorTime = 0  #统计无法索引文件的个数
ErrorPath = []  #记录无法索引的地址
```
###5. 函数一览

```python
import os 
import pickle  #保存用
import copy  #深度复制用

def Lunch():  #起始函数


#文件及字典操作类函数
def File_to_Struct(Path,PC): #添加文件到广义表
def Dir_to_Struct(Path,PC): #添加空文件夹到广义表
def Creat_Root_Struct(Path,PC):  #根据初始条件创造广义表结构
def Add_Path_to_File(Path,PC):  #分析是文件还是文件夹，执行相应的函数
def Walk_Root(Root,PC,do): #前序遍历Root路径下的所有文件及文件夹并执行do函数
def Init_Struct(Root,PC):  #输入Root（要遍历的文件夹地址） 初始化数据结构
def Del_Thing(top):  #删除计算机系统里面的文件
def Del_File_or_Dir(Path,PC):  #删除操作



#控制台函数区
def Cin_CMD(PC):  #输入指令的函数
def CMD_to_Fun(string):  #指令转换为对应函数


#命令与操作函数对接的函数区
def CD(Path,PC): #打开命令
def Add_File(name,Path,PC):
def Add_Dir(name,Path,PC):
def ReName(Path,NewPath,PC):  #重命名
def Del_Path(Path,PC): #删除命令
def For_Help():
def Enlarge_Root(Path,PC):  #扩大检索路径
def Refresh():  #Roots路径刷新
def Save_Data():  #保存进度
def Load_Data():  #载入进度


#可视化类函数
def B_to_MB(b):  #数据单位转换并显示
def Sort_by_Size(dir):  #创建文件夹下子文件的排序
def Change_Now_Sort(Path,PC):  #改变NowSort
def Cout_Dir(Path,PC):  #输入链接查看文件夹并按照大小排序，显示大小
def Tree_For_PC_With_Level(dir,deep,name = 'X.DIR',Tree_Level = 1):  #传入文件夹的节点，带有深度版
def Tree(Path,PC,deep):  #输入路径


#工具类函数
def Path_to_List(Path): #将路径一层一层的分解为多个路径，用于Creat_Root_Struct()

#以及其他非核心的工具类函数
```
###6. 核心函数：
#####1. 先序遍历函数
```python
def Walk_Root(Root,PC,do): #前序遍历Root路径下的所有文件及文件夹并执行do函数
    try:    #有的文件夹没有权限进入，产生WindowsError错误，则记录他们，并跳过他们
        for lists in os.listdir(Root): #获得遍历路径下一层的文件名
     
            Path  =  os.path.join(Root,lists) #将名字转换为路径
            Path = Turn_Path(Path)  #将路径标准化
            do(Path,PC)  #并对每个文件执行do函数（即加入结构体）
            if os.path.isdir(Path):   #如果是文件夹则继续遍历该文件夹
    except WindowsError,error:
        global ErrorTime
        ErrorTime+= 1  #如果没有权限，报错WindowsError则记录下来
        global ErrorPath
        ErrorPath+= [(error,Root)]
        return

```


#####2. 构造结构体 PC的函数
```python
def Init_Struct(Root,PC):#输入Root（要遍历的文件夹地址） 初始化数据结构
    Root = Stand_Path(Root)  #将路径标准化    
    Creat_Root_Struct(Root,PC)  #将要遍历的文件夹的母文件夹以及自己 加入结构体
    
    print '    (1/2) 正在遍历索引区:',Root,'并创建目录结构体，请稍等。。。\n'
    Walk_Root(Root,PC,Add_Path_to_File) 
    #将要遍历的文件夹下的所有文件先序遍历执行Add_Path_to_File
    #Add_Path_to_File是将文件或文件夹加入结构体的函数
    
    Change_Now_Sort(Root,PC) #跳转了工作路径后要将sort编号更新
    
    global Roots 
    Roots+= [Root]  #将刚遍历过的路径记录下来
    print '    (2/2) 目录结构体已创建成功！可在目录',Root,'下管理文件\n'
    
    global ErrorTime  #引入无法遍历的文件数量，如果有，通知用户有多少个
    if ErrorTime != 0:
        print '\n  注意：由于系统权限原因，一共有',ErrorTime,'个系统文件或文件夹未索引！\n' 
    
```


4. 效果展示
====
##1. 初始界面
初始界面要求用户输入路径，或载入已保存工作进度（第14行）：
```
    欢迎使用Python资源管理器 V0.2 

    请输入文件索引路径，程序将在您输入完毕后对文件夹进行遍历
    
    例如 C:\ 或者直接回车（程序将遍历当前路径）

    遍历时可能需要您稍等片刻，具体等待时间和索引路径下的文件总数有关

    您也可以键入help，以查看帮助
    
    注意：大小写敏感，不需要加引号
    

Tips:已检测到有可载入的进度,输入 load 进行载入。

请输入文件索引路径(例如 C:\):
```

##2. help命令
用户可输入 help\n 查看以下帮助：
```python
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
```


##3. dir命令
一开始工作路径输入为`C:\` 盘时：
（由于内容太多，只展示前半部分的效果）
```
    (1/2) 正在遍历索引区: C:/ 并创建目录结构体，请稍等。。。

    (2/2) 目录结构体已创建成功！可在目录 C:/ 下管理文件


  注意：由于系统权限原因，一共有 320 个系统文件或文件夹未索引！
  
磁盘:C: 下有 44 个文件，已用空间:109GB 

  Users                     
     No.00 type:DIR   size:35.6GB   ■■■■■■■■■■■■■■■■■■■■ 

  Windows                   
     No.01 type:DIR   size:22.4GB   ■■■■■■■■■■■■ 

  Program Files (x86)       
     No.02 type:DIR   size:17.1GB   ■■■■■■■■■ 

  Program Files             
     No.03 type:DIR   size:9.2GB    ■■■■■ 

  pagefile.sys              
     No.04 type:      size:8.0GB    ■■■■ 

  hiberfil.sys              
     No.05 type:      size:6.3GB    ■■■ 

  D                         
     No.06 type:DIR   size:3.5GB    ■ 

  ProgramData               
     No.07 type:DIR   size:2.5GB    ■ 

  
```
##4. tree命令
工作路径为 ` I:\测试`   文件夹下时 
输入指令` tree`：
混乱的结构也一览无余！（浏览时，宽度应大于 标准的%80）
```python
文件夹:测试 路径:I:/测试 占用空间为:83.4MB 已检索全部文件 
 | 
 |    子文件------------------- type:DIR    size:41.6MB   
 |    |    kksd--------------------- type:DIR    size:41.6MB   
 |    |    |    6.mp4-------------------- type:mp4   size:41.6MB   
 |    |    |    新建文件夹--------------- type:DIR    size:12B      
 |    |    |    |    2.txt-------------------- type:txt   size:6B       
 |    |    |    |    1.txt-------------------- type:txt   size:6B       
 |    |    |    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
 |    |    |    2.txt-------------------- type:txt   size:6B       
 |    |    |    1.txt-------------------- type:txt   size:6B       
 |    |    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
 |    |    sd----------------------- type:DIR    size:12B      
 |    |    |    2.txt-------------------- type:txt   size:6B       
 |    |    |    1.txt-------------------- type:txt   size:6B       
 |    |    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
 |    |    2.txt-------------------- type:txt   size:6B       
 |    |    1.txt-------------------- type:txt   size:6B       
 |    |    kks---------------------- type:DIR    size:0B       
 |    ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
 |    6.mp4-------------------- type:mp4   size:41.6MB   
 |    2.jpg-------------------- type:jpg   size:122KB    
 |    1.txt-------------------- type:txt   size:289B     
 |    空子文件----------------- type:DIR    size:0B  
 ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
```
在使用`allpc`指令遍历过所以文件夹后
在任何工作路径下输入
输入`tree -1`（树形结构将输出遍历过的所有文件，层数为绝对值，即|-1|）
```python

磁盘: 已用空间为:671GB 所显示的深度为: 1 
 | 
 |    H:----------------------- type:DIR    size:310GB    
 |    G:----------------------- type:DIR    size:150GB    
 |    C:----------------------- type:DIR    size:109GB    
 |    F:----------------------- type:DIR    size:65.0GB   
 |    I:----------------------- type:DIR    size:35.9GB   
 ￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣
```
5. 总结
=====
###1. 引语：
>课程设计是一门培养学生综合运用所学知识,发现,提出,分析和解决实际问题的学科

###2. 收获：
> * 对 Windows 下计算机的文件系统有了深刻的了解

> * 对Python开发和树形数据结构更加熟练

> * 有了一个不错的文件管理工具

###3. 后续：
1. 实现复制，剪切，粘贴功能
2. 开发出图形界面，便于操作和推广
3. 兼容Linux
