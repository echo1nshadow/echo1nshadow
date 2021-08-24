- 下划线
  1. 使用```<u>下划线</u>```
<u>下划线</u>
  1. ```<span style="border-bottom:2px dashed yellow;">所添加的需要加下划线的行内文字</span>```
<span style="border-bottom:2px dashed yellow;">所添加的需要加下划线的行内文字</span>

- 删除线
  两个```~~```
  eg:
  ```
  ~~Q_INVOKABLE 定义的函数必须有参数~~
  ```
  ~~Q_INVOKABLE 定义的函数必须有参数~~

- 链接
  - 使用尖括号可以把URL或者email地址变成可点击的链接
    ```
    <echo1nshadow@qq.com>
    ```
    <echo1nshadow@qq.com> 
  - 引用图片
    ```
      ![图片](图片.url)
      ![测试](https://s3.bmp.ovh/imgs/2021/08/a85ae8245015ccaa.jpg)
    ```
    ![测试](https://s3.bmp.ovh/imgs/2021/08/a85ae8245015ccaa.jpg)

  - 引用网址, 链接文本放在中括号内，链接地址放在后面的括号中
    ```
      [echo1nshadow](https://github.com/echo1nshadow)
    ```
    [echo1nshadow](https://github.com/echo1nshadow)
- PDF分页
  ```
  <div STYLE="page-break-after: always;"></div>
  ```
  前后再添个空行

- pandoc
  安装pandoc
  ```
  sudo apt-get install pandoc pandoc-citeproc texlive
  ```