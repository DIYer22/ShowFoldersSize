# -*- coding: gbk -*-
"""
Created on Wed Dec 30 22:49:43 2015

@author: ylxx@live.com

�����ҳ�ѧPyhtonʱ�㿪ʼ����Ŀ
������ṹ������
Ҳû���ձ�̹淶
�������汾�����ع�,����

"""
#from __future__ import unicode_literals

import os
import pickle
import copy
import webbrowser

#==============================================================================
# #�����ຯ��
#==============================================================================


def turn_path(Path):#ת��ת���·��

    return Path.replace('\\','/')


def stand_path(Path):#��Ŀ¼·����׼��
    Path = turn_path(Path)
    if Path[-1] == '/':
        Path = Path[0:len(Path)-1]

    if Path[-1] == ':' and len(Path)<= 3:
        Path = Path+'/'
    return Path


def stand_path2(Path):#·����׼��
    Path = turn_path(Path)
    if Path[-1] == '/':
        Path = Path[0:-1]
    return Path


def path_to_cmd(Path):#·��ת��cmd����
    Path = Path.replace('/','\\')
    Path = '"'+Path+'"'
    return Path


def split_path(Path): #��·��������ļ�������
    list = Path.split("/")
    if list[-1] == '':
        list = list[:-1]
    return list

def change_list(d):      #����list˳��
    len2 = len(d)
    for i in range(len2/2):
        temp = d[len2-1-i]
        d[len2-1-i] = d[i]
        d[i] = temp


def path_to_list(Path): #��·��һ��һ��ķֽ�Ϊ���·��
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
    '''��·��ת��Ϊ�ṹ���ж�Ӧ���ļ���'''
    '''���棺��Ҫ�ڵ�����PC�еĺ����ٵ��ô˺���,��ֱ�Ӽ�PC����'''
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
# �ļ����ֵ�����ຯ��
#==============================================================================

def file_to_struct(Path,PC): #����ļ��������
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
    for i in PathList :  #ÿ��·��+size
        p['size']+= size
        p = p['file'][i]
    p['size']+= size
    p['file'][name] = {'size':size}


def dir_to_struct(Path,PC): #��ӿ��ļ��е������

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


def creat_root_struct(Path,PC):#���ݳ�ʼ������������ṹ
    list = path_to_list(Path)
    #print '����·��',list
    if not ('file' in PC):
        PC['file'] = {}

        PC['size'] = 0
    for dir in list:
        dir_to_struct(dir,PC)


def add_path_to_file(Path,PC):#�������ļ������ļ��У�ִ����Ӧ�ĺ���
    if os.path.isdir(Path):

        dir_to_struct(Path,PC)
    else:
        file_to_struct(Path,PC)

def walk_root(Root,PC,do): #ǰ�����Root·���µ������ļ����ļ��в�ִ��do����
    try:    #�е��ļ���û��Ȩ�޽��룬����WindowsError�������¼���ǣ�����������
        for lists in os.listdir(Root): #��ñ���·����һ����ļ���

            Path  =  os.path.join(Root,lists) #������ת��Ϊ·��
            Path = turn_path(Path)  #��·����׼��
            do(Path,PC)  #����ÿ���ļ�ִ��do������������ṹ�壩
            if os.path.isdir(Path):   #������ļ���������������ļ���
                walk_root(Path,PC,do)

    except WindowsError,error:
        global ErrorTime
        ErrorTime+= 1  #���û��Ȩ�ޣ�����WindowsError���¼����
        global ErrorPath
        ErrorPath+= [(error,Root)]
        return


def init_struct(Root,PC):#����Root��Ҫ�������ļ��е�ַ�� ��ʼ�����ݽṹ
    Root = stand_path(Root)  #��·����׼��
    creat_root_struct(Root,PC)  #��Ҫ�������ļ��е�ĸ�ļ����Լ��Լ� ����ṹ��


    print '    (1/2) ���ڱ����ļ���:',Root,'�������ļ��нṹ�壬���Եȡ�����\n'
    walk_root(Root,PC,add_path_to_file)
    #��Ҫ�������ļ����µ������ļ��������ִ��add_path_to_file
    #add_path_to_file�ǽ��ļ����ļ��м���ṹ��ĺ���

    change_now_sort(Root,PC) #��ת�˹���·����Ҫ��sort��Ÿ���

    global Roots
    Roots+= [Root]  #���±�������·����¼����
    print '    (2/2) �ļ��нṹ���Ѵ����ɹ����ɹ�����',Root,'·���µ��ļ�\n'

    global ErrorTime  #�����޷��������ļ�����������У�֪ͨ�û��ж��ٸ�
    if ErrorTime != 0:
        print '\n  ע�⣺����ϵͳȨ��ԭ��һ����',ErrorTime,'��ϵͳ�ļ����ļ���δ������\n'


def del_thing(top):#ɾ�������ϵͳ������ļ�
    if os.path.isfile(top): #������ļ���ɾ��
        os.remove(top)
        return
    for Root, dirs, files in os.walk(top, topdown = False):
        for name in files:
            os.remove(os.path.join(Root, name))
        for name in dirs:
            os.rmdir(os.path.join(Root, name))

    os.rmdir(top)


def del_file_or_dir(Path,PC):#ɾ������
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
    for i in PathList :  #ÿ��·��-size
        p['size']-= size
        p = p['file'][i]
    p['size']-= size
    del p['file'][name]



#==============================================================================
# #���ӻ��ຯ��
#==============================================================================

def b_to_mb(b):  #���ݵ�λת������ʾ
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


def sort_by_size(dir):#�����ļ��������ļ�������
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


def change_now_sort(Path,PC):#�ı�NowSort
    list = split_path(Path)
    p = PC

    for dir in list:
        p = p['file'][dir]
    sort = sort_by_size(p)
    global NowSort
    global NowPath
    NowPath = Path
    NowSort = copy.deepcopy(sort)


def cout_dir(Path,PC):#�������Ӳ鿴�ļ��в����մ�С������ʾ��С
    list = split_path(Path)
    p = PC

    for dir in list:
        p = p['file'][dir]
    sort = sort_by_size(p)
    global NowSort
    NowSort = copy.deepcopy(sort)
    if len(Path)<= 3:
        print '\n','\n','����:'+Path,
        print '����',len(sort),'���ļ������ÿռ�:'+b_to_mb(p['size']),'\n'
    else:
        print '\n','\n','�ļ���:'+Path,
        print '����',len(sort),'���ļ���ռ�ÿռ�:'+b_to_mb(p['size']),'\n'

    MaxNameLen = 25 #�������ֵ������
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
            print '��'*(20*i[0]/sort[0][0]),
        print '\n'


def tree_for_pc_with_level(dir,deep,name = 'X.DIR',Tree_Level = 1):#tree�ͽṹ�����������Ȱ�



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

            print (Tree_Level-1)*' |   '+' '+'��'*26 #�����и��ϻ��� �޷���ʾ


def tree(Path,PC,deep):
    list = split_path(Path)
    p = PC

    for dir in list:
        p = p['file'][dir]
    if len(Path)<3:
        print '\n','\n','����:'+Path,
        print '���ÿռ�Ϊ:'+b_to_mb(p['size']),
    else:
        print '\n','\n','�ļ���:'+os.path.basename(Path), '·��:'+Path,
        print 'ռ�ÿռ�Ϊ:'+b_to_mb(p['size']),
    if deep!= 0:
        print '����ʾ�����Ϊ:',deep,
    else:
        print '�Ѽ���ȫ���ļ�',
    print '\n',' | '
    tree_for_pc_with_level(p,deep)



#==============================================================================
# #�����뺯���Խ���
#==============================================================================




def CD(Path,PC): #������
    if os.path.isfile(Path):
        print '����Ϊ�����ļ�:',os.path.basename(Path)
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
    print '�ɹ������ļ�',name,'�ļ�λ��',Path


def add_dir(name,Path,PC):
    Pathd = Path+'/'+name
    os.mkdir(Pathd)
    dir_to_struct(Pathd,PC)
    print '�ɹ������ļ���',name,'��·����',Pathd


def rename(Path,NewPath,PC):#������
    if os.path.exists(NewPath):
        print os.path.basename(NewPath),'�Ѵ��ڣ��뻻һ������,��������ָ��!'
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


def del_path(Path,PC): #ɾ������
    if os.path.isfile(Path):
        print '��ȷ��Ҫɾ���ļ�:',os.path.basename(Path),'��\n������yȷ��ɾ��������nȡ����'
        yorn = raw_input('\n>>>')
        if yorn  ==  'y':
            del_file_or_dir(Path,PC)
            print '�ɹ�ɾ��',os.path.basename(Path),'��'
        else:
            print 'ɾ��',os.path.basename(Path),'�Ĳ�����ȡ����'
    else:
        print '��ȷ��Ҫɾ���ļ���:',os.path.basename(Path),'���������',
        i = 0
        for lists in os.listdir(Path):
            if i<5:
                print lists,
            i+= 1
        if i<= 5:
            print "��",i,
        else:
            print "...��",i,
        print '���ļ���\n������yȷ��ɾ��������nȡ����'
        yorn = raw_input('\n>>>')
        if yorn  ==  'y':
            del_file_or_dir(Path,PC)
            print '�ɹ�ɾ��',os.path.basename(Path),'��'
        else:
            print 'ɾ��',os.path.basename(Path),'�Ĳ�����ȡ����'


def for_help():
    print '''


������

UCE�ļ��д�С�鿴�� V0.40

		By  BUCT-UCEС��
  
  
�����У�

    1. �鿴�ļ��д�С
    2. ��ʾ�ļ��е����νṹ
    3. �ӱ��������ļ����ҳ����ļ����ļ�
    4. �������ļ�����ռ�ÿռ�
    5. ���ñ�Ŵ����ļ������в���
    6. ��ֱ���ڹ������д��ļ�
    7. �ɱ�������͹�������
    8. ������CMD�ļ�����


    ����      	 ����

    dir          �鿴��ǰ�ļ��б�
    �س�         ����ͬdir�������ӷ���
    cd NAME      ��NAME�ļ����ļ���
    cd ..        ������һ���ļ���
    del NAME     ����ɾ���ļ��л��ļ�(ע��:�����ƶ�������վ)
    goto PATH    ����PATH·��,���л���PATH·��
    top NUM      ��ʾ����NUM���ļ�
                 �ɲ���NUM��Ĭ����10(NUMΪ������ʾȫ�ֵ���˼)
                 
    tree DEEP    ��ͼ�ν�����ʾ��ǰ�ļ��еĽṹ,�����DEEP
                 ��ֻ��ʾ��Ӧ����
                 DEEP�и��ţ����νṹ������������������ļ�
                 ����Ϊ����ֵ��|DEEP|��-0����ȫ������

    CMD.no No    ������CMD��� .no �ͻ������ӦNO��ŵ��ļ�
                 ����:cd.no 01 �򿪵ڱ��Ϊ01���ļ���
                 
    save         ������ȣ��洢�ڵ�ǰ�ļ���
                 ������Ϊ��UCE�ļ��д�С�鿴��_�洢���ݡ�
                 
    load         ����洢�Ľ��ȣ�����ڱ������Ĺ����������ļ������ݽ��᲻׼ȷ
    refresh      ������Ѿ��ڹ���������������������ļ�����ʹ�ô��������±���
    allpc        �������д���
    ana NUM      ����ռ�ÿռ�ΪǰNUM��ĸ����ļ�����
                 NUMĬ��Ϊ20(NUMΪ������ʾȫ�ֵ���˼)
                 
    md NAME      ����ļ��У�����ΪNAME
    mf NAME      ����ļ�������ΪNAME

    ren NAME>NEW ������NAMEΪNEW
    git          ��ø��£��鿴PythonԴ����
    q            ��������


��Ŀ��飺

  Ϊ�˷����˽�Ӳ����Դ�ķֲ����鿴�ļ��д�С��������Ӳ�̿ռ䣬��
  ������UCE�ļ��д�С�鿴����Ϊ����ѧϰ�ɱ���UCE�ļ��д�С�鿴��
  ��Ҫ����DOS�����Pyhton���
  (UCE�Ǳ���������ѧ�ļ�������ţ������为����)
  
  ���ף��ʹ�����!


    		��ϵ���ߣ�ylxx@live.com
      
    		�������ŷ�չ��������gitָ��
      
    		������2016/03/31      



'''


def enlarge_root(Path,PC):#�������·��
    print '������ʵ������Ѿ��������ļ�����������ϣ�����ļ�������������',Path,'·�����𣿣��������Ҫ����һ��ʱ�䣩'
    print '������yȷ����������nȡ����'
    yorn = raw_input('\n>>>')
    if yorn  ==  'y':
        print '\n\n���ڽ��ļ�������������',Path,'·����:\n'
        global Root
        global NowPath
        init_struct(Path,PC)
        Root = Path
        NowPath = Path
        print '�ļ��������ѳɹ�������',Path,'·����'
    else:
        print '��ȡ���ļ�������������',Path,'·���£�'


def refresh():#Roots·��ˢ��
    global ErrorTime
    global ErrorPath
    global NowPath
    global NowSort
    global Root
    global Roots
    i = 0
    RootsCopy = Roots[:]
    ErrorTime = 0  #����bug��¼
    ErrorPath = []
    ns = copy.deepcopy(NowSort)
    np = NowPath        #���浱ǰ·��
    for Path in RootsCopy:

        print str(i)+'/'+str(len(Roots)-i),'�������±����ļ���:',Path
        init_struct(Path,PC)
        i+= 1
    NowSort = copy.deepcopy(ns)
    NowPath = np
    Roots = RootsCopy[:]
    print '\nˢ�����б�������ɹ���'
    

class Top_box(object):
    '''top������'''
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
    ��������ļ����б�
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
        for_print =  '�ѱ������ļ��У�����' + str(top) + '���ļ���'
    else:
        global NowPath
        path = NowPath
        list = split_path(path)
        for dir in list:
            dirr = dirr['file'][dir]
        path += '/'
        for_print =  '��ǰ�ļ�����"' + path + '"�£�����' + str(top) + '���ļ���'
            
    box = Top_box(top)
                
    walk_root(dirr,path)     
    print for_print       
    print box
    print '\nTips:ѡ��·���������Ҽ��㸴�Ƴɹ��ˣ�'


class Anysis(object):
    '''�����������͵�ռ�ÿռ�'''
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
    '''�����������͵�ռ�ÿռ�'''
    global PC  
    dirr = PC
    if max_type < 0:
        max_type = -max_type
        for_print = '�����ѱ������ļ��У����ļ����͵�ռ�������'
    else:
        global NowPath
        list = split_path(NowPath)
        for_print = '��ǰ�ļ���"' + NowPath + '"�£����ļ����͵�ռ�������'
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
    

def save_data():  #�������
    global NowPath
    global NowSort
    global Root
    global Roots
    global ErrorTime
    global PC
    global ErrorPath
    File_Data  =  open("UCE�ļ��д�С�鿴��_�洢����","wb")

    data = {}

    data['ErrorTime'] = ErrorTime
    data['ErrorPath'] = ErrorPath
    data['PC'] = PC
    data['NowSort'] = NowSort
    data['NowPath'] = NowPath
    data['Root'] = Root
    data['Roots'] = Roots
    print '���ڽ�����д��',os.path.abspath('.'),'�µ��ļ�:��UCE�ļ��д�С�鿴��_�洢���ݡ������Եȡ�����'
    pickle.dump(data,File_Data)
    File_Data.close()
    print '\n�ļ���UCE�ļ��д�С�鿴��_�洢���ݡ���',
    print '������',os.path.abspath('.'),'·����'


def load_data():  #��������
    global NowPath
    global NowSort
    global Root
    global Roots
    global ErrorTime
    global PC
    global ErrorPath
    if not os.path.isfile("UCE�ļ��д�С�鿴��_�洢����"):
        print '�ڵ�ǰ·����',os.path.abspath('.'),'��','�ļ������ڣ�����ʧ�ܣ�'
        return
    print '���ڶ�ȡ',os.path.abspath('.'),'·���µ��ļ�:UCE�ļ��д�С�鿴��_�洢����\n���Եȡ�����'
    if 'size' in PC:
        del PC['file']
        del PC['size']
    File_Data  =  open("UCE�ļ��д�С�鿴��_�洢����","rb")
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
    print '�Ѵ��ļ�:��UCE�ļ��д�С�鿴��_�洢���ݡ��гɹ��ָ����ȣ�'



#==============================================================================
# #����̨������
#==============================================================================


def CMD_to_Fun(string):  #����ת��Ϊ��Ӧ����
    global NowPath
    global NowSort
    global Root
    global Roots
    global PC
    if string == '':  #�س�Ϊ dir
        cout_dir(NowPath,PC)
        return
    stringlist = string.split()  #�����ж��Ƿ�Ϊ.no������
    if '.' in stringlist[0]:
        if stringlist[0][-3:] == '.no':#ת��.no������
            numoder = string[len(stringlist[0]):].strip()#��ȡ���
            newname = '<' # '<' �Ǹ��Ǻ�
            if '>' in numoder:
                newname = numoder.split('>')[1].strip()
                numoder = numoder.split('>')[0].strip() #�����ren�Ļ� ��ȡ.on

            for i in NowSort:  #���ͨ�������ת��Ϊ����
                if numoder == i[3]:  #i����Ԫ��Ϊ[numoder,name,Path]
                    string = stringlist[0][:-3]+' '+i[1]
                    if newname!= '<':#������������������
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
        print '    ���Եȡ�������\n\n'
        the_top(top)
        return
    elif string[:3] == 'ana':
        num = 20
        if len(string) > 4:
            num = int(string.split()[1])
        print '    ���Եȡ�������\n\n'
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
        for i in range(65,91): #��ȡ����Ӳ���̷�
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
    elif string[0:3] == 'cd ':  #��
        dir = string[3:].strip()
        if dir == "..":
            Path = os.path.dirname(NowPath)
            if len(Path)<len(Root):
                if len(Path)<3:
                    cout_dir('',PC)
                    NowPath = Root
                    print 'ֻ�ǿ�һ����������ЩӲ�̣���ǰ·��û�б�'
                    print '�������ؼ���:tree+���������νṹ����������������ļ�'
                    print '����Ϊ����ֵ��|����|��-0����ȫ������'
                    return
                else:
                    tag = 0
                    for i in Roots:
                        if i in Path: #�ж���һ���Ƿ������
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
    elif string[0:3] == 'md ':  #�����ļ���
        name = string[3:].strip()
        add_dir(name,NowPath,PC)
        return
    elif string[0:3] == 'mf ':  #�����ļ�
        name = string[3:].strip()
        add_file(name,NowPath,PC)
        return
    elif string[0:4] == 'del ':  #�����ļ���
        Path = NowPath+'/'+string[4:].strip()
        del_path(Path,PC)
        return
    elif string[0:4] == 'tree':  #��
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
        print '\n�ѽ�',os.path.basename(Path),'������Ϊ',os.path.basename(NewPath),'\n'
        return

    elif string[0:5] == 'goto ':  #�л�Ŀ¼
        Path = string[5:].strip()
        if not os.path.isdir(Path):
            print '  ·�������ڣ�����������ָ�'
            return
        Pathn = Path
        Path = stand_path(Path)
        tag = 0
        for i in Roots:
            if i in Path:
                tag = 1
                print Path,'�Ѿ�����������·�����л�'
        if tag  ==  0:
            print '���ڱ����µ��ļ���:',Path
            init_struct(Path,PC)
        NowPath = Pathn
        Root = Pathn
        return
    else:
        print 'ָ��������������룬Ҳ������ help�鿴����'


def cin_cmd(PC):  #����ָ��ĺ���
    global NowPath
    cout_dir(NowPath,PC)
    while 1:
        #cout_dir(NowPath,PC)
        print ''
        print '��'*40
        #print '��'*40
        print '\n��ǰ·��Ϊ\"'+NowPath+'\"������ָ��(����help,�鿴����):'
        string = raw_input('\n>>>')
        print ''
        string = string.strip()
        if string  == 'q':
            break
        
        try:
            CMD_to_Fun(string)
        except :
            print '\n\n���������������ļ�������ָ��û����ԣ�����һ�ΰ�(��������help,�鿴����)\n\n'

def lunch():#��ʼ����
    global Path
    global PC
    print '''

    ��ӭʹ��UCE�ļ��д�С�鿴�� V0.40



    ֱ�ӻس������򽫱�����ǰ·�� ���� ���������·�� ���� C:\\ 

    ����ʱ������Ҫ���Ե�Ƭ�̣�����ȴ�ʱ��ͱ���·���µ��ļ������й�

    ��Ҳ���Լ���help���Բ鿴����

    ע�⣺��Сд���У�����Ҫ������

'''
    if os.path.isfile('UCE�ļ��д�С�鿴��_�洢����'):
        print '\nTips:�Ѽ�⵽�п�����Ľ���,���� load �������롣\n'
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
            print '������������д��������ǰ����ĵ��������ο�\n'
        if not os.path.isdir(Path) and Path!= ':' and ':' in Path:
            print '�ļ��в����ڣ����������룡\n'
        print '��'*40
        print '\n��ֱ�ӻس� �� �����������·��(���� C:\\):'
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


#ȫ������

PC = {}  #�����ݽṹ
NowPath = '' #��ǰ����·��
NowSort = []  #��¼��ǰ����·�����ļ��ı��

Root = '' #��ǰ�������ĵط�
Roots = []  #��¼���������ĵط���Root��list

ErrorTime = 0  #ͳ���޷������ļ��ĸ���
ErrorPath = []  #��¼�޷������ĵ�ַ


lunch()

