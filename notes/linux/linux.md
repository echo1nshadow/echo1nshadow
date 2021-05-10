#### vim 相关
1. vim 编辑二进制文件
 - 格式转换为16进制
    ```:%!xxd```
 - 转换为二进制文件保存
    ```:$!xxd -r```


#### 可能有点用的程序
- ```file```
  file 命令用于分析文件的类型
  如果需要分析二进制文件, 可以首先使用 ```file``` 命令来切入, 在 Linux 下,一切皆文件，但并不是所有的文件都具有可执行性,可以先使用 file 命令来分析它们的类型
  ```
  echo@XiongJie:~/tools$ file calc_ftp_port
  calc_ftp_port: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=808488520c60bf877aa5d4ffb1d3035301c43bc3, not stripped
  ```

- ```ldd```
  ldd 命令可以用于分析可执行文件的依赖
  ```
  echo@XiongJie:~/tools$ ldd calc_ftp_port
        linux-vdso.so.1 (0x00007ffed83e9000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fb85cab9000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fb85d0ac000)
  ```

- ```ltrace```
  ltrace的功能是能够跟踪进程的库函数调用

- ```strace```
  strace 命令可以用于追踪程序运行过程中的系统调用及信号

- ```hexdump```
  hexdump 命令用来查看二进制文件的 16 进制编码,但实际它能查看任何文件,而不限于二进制文件

- ```strings```
  strings 命令可以用来打印二进制文件中可显示的字符
  ```
  echo@XiongJie:~/tools$ strings ./calc_ftp_port
  /lib64/ld-linux-x86-64.so.2
  libc.so.6
  printf
  atoi
  __cxa_finalize
  __libc_start_main
  GLIBC_2.2.5
  _ITM_deregisterTMCloneTable
  __gmon_start__
  _ITM_registerTMCloneTable
  AWAVI
  AUATL
  []A\A]A^A_
  port_first:%d
  port_later:%d
  port:%d
  ;*3$"
  ```

- ```readelf ```
  readelf 一般用于查看 ELF 格式的文件信息
  ```
  echo@XiongJie:~/tools$ readelf ./calc_ftp_port  -h
  ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x580
  Start of program headers:          64 (bytes into file)
  Start of section headers:          6488 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         9
  Size of section headers:           64 (bytes)
  Number of section headers:         29
  Section header string table index: 28
  ```