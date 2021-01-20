#### Qt
1. **ASSERT: "!"No style available without QApplication!**
- 解决方法
  .pro文件添加 QT += charts qml quick
  将 QGuiApplication app(argc, argv); 修改为QApplication app(argc, argv); **记得修改头文件引用**
- 原因
  QApplication 继承自QGuiApplication ，对于有继承基本Qt widgets的 需要用QApplication，而ChartView来自于Qt widgets

2. **如何实现动态曲线**
  - 定义一个变量来保存时间, x轴的min/max值根据这个变量生成
    ```
      property int timer: 0
    ```

    ```
    ValueAxis{
        id: id_axis_x
        min: timer - 5000
        max: timer + 500
        tickCount: 100
        tickInterval: 1000
    }
    ```
    ```
    Timer{
        id: id_timer
        interval: 50
        repeat: true
        running: true
        onTriggered: {
            timer += 500
            draw_curve(timer, Math.random())
        }
    }
    ```
    **qml绘图cpu占用极高, 待解决**

3. **如何从C++向QML中添加曲线**
   
4. **QML绘图卡顿问题**
 - 定时器放在C++中
  
5. **Qt 定时器**
