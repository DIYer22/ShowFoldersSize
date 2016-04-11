# ShowFoldersSize 0.40 文档

标签（空格分隔）： ShowFoldersSize

---

## 0.40更新

1. 增加top命令，以展示最大的文件
2. 增加ana命令，以分析各文件类型空间占用情况
3. 修改了help内容
4. 修改了部分提示
5. 打包成了exe文件，方便使用
6. 添加了图标
[![](http://7xs2rt.com1.z0.glb.clouddn.com/nullico_small.png)](https://codeload.github.com/DIYer22/ShowFoldersSize/zip/master)

---

## 使用帮助：
将`复制到要查看文件夹大小的地方.exe`文件复制到对应文件夹，打开，并按一下回车，便可以查看此文件夹下的所有文件夹大小

在软件中，输入`help`
获得如下帮助
```
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
```



