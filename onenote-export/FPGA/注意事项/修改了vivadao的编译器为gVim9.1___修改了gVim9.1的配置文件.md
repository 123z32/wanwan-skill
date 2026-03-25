# 修改了vivadao的编译器为gVim9.1???修改了gVim9.1的配置文件

> 来源: OneNote > FPGA > 注意事项
> 修改: 2026-01-10T10:28:39Z

修改了vivadao的编译器为gVim9.1￼￼￼修改了gVim9.1的配置文件

 

 
" ================= 基础人性化设置 =================

 
set nocompatible " 关闭兼容模式

 
source $VIMRUNTIME/mswin.vim " 开启 Windows 快捷键 (Ctrl+C/V/X/S/Z 可用了!)

 
behave mswin " 像 Windows 程序一样行为

 

 
" ================= 界面美化 =================

 
syntax on " 开启代码颜色高亮

 
colorscheme desert " 设置为深色背景（护眼）

 
set guifont=Consolas:h12 " 设置字体为 Consolas，字号 12 (看着舒服)

 
set number " 显示行号

 
set nowrap " 代码太长不自动换行（FPGA代码通常很长）

 
set guioptions-=T " 隐藏顶部那个丑陋的工具栏

 

 
" ================= 编程辅助 =================

 
set autoindent " 换行时自动对齐

 
set tabstop=4 " Tab 键宽度设为 4 个空格

 
set shiftwidth=4 " 自动缩进宽度设为 4

 
set expandtab " 把 Tab 转为空格 (避免不同软件打开乱码)

 
filetype plugin indent on " 识别文件类型

 

 
" ================= 解决乱码 =================

 
set encoding=utf-8

 
set fileencodings=utf-8,chinese,latin-1

 
language messages zh_CN.utf-8 " 菜单中文显示

 

 
- 
想打字/写代码时：

 
 
- 按一下 i 键（Insert 模式）。
 
- 此时左下角会显示 -- INSERT --，这时候它就和记事本一模一样了。
 

 
 
- 
想保存/或者发呆时：

 
 
- 按一下 Esc 键（Normal 模式）。
 
- 此时你不能打字，键盘变成了遥控器。
 

 
 
- 
最常用的命令（在 Esc 模式下输入）：

 
 
- :w -> 保存 (Write)
 
- :q -> 退出 (Quit)
 
- :wq -> 保存并退出
 
- u -> 撤销 (Undo)