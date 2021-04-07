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


#### QML
- qml控制小数点位数 toFixed()

  eg: 两位小数使用 toFixed(2)
  ```
            TextField {
                id: id_cfg_value
                width: 200
                text: model.value.toFixed(2)
                font.pointSize: 12
                onTextEdited: {
                    model.value = parseFloat(id_cfg_value.text)
                }
            }
  ```

- 报qt_metacast 之类的错
  - 多继承只需要一个Q_OBJECT宏
  - 也可能是没有把文件加入到工程中
  
- QML 读写文件

  QML没有提供文件读写的接口, 需要使用C++来实现
  ```
  #ifndef FILE_OBJECT_H
  #define FILE_OBJECT_H
  #include <QObject>

  class FileObject : public QObject
  {
      Q_OBJECT
      Q_PROPERTY(QString source READ source WRITE setSource NOTIFY sourceChanged)
  public:
      explicit FileObject() {};
      ~FileObject() {};

      Q_INVOKABLE QString read();
      Q_INVOKABLE bool write(const QString& data);
      
    Q_INVOKABLE void setSource(const QString& source) { m_source = source; };
      QString source() { return m_source; }
      
  signals:
      void sourceChanged(const QString& source);

  private:
      QString m_source;
  };

  #endif // FILE_OBJECT_H
  ```

  ```
  #include "FileObject.h"

  #include <QFile>
  #include <QTextStream>

  /*
  FileObject::FileObject(QObject *parent) :
      QObject(parent)
  {

  }
  */

  QString FileObject::read()
  {
    QString content;
      QFile file(m_source);
      if ( file.open(QIODevice::ReadOnly) ) {
        content = file.readAll();
          file.close();
      } 
      
      return content;
  }

  bool FileObject::write(const QString& data)
  {
      QFile file(m_source);
      if ( file.open(QFile::WriteOnly | QFile::Truncate) ) {
          QTextStream out(&file);
        out<<data;
        file.close();
        return true;
      }
      else {
        return false;
      }
  }
  ```

  在 main.cpp 注册这个文件读写类
  ```
  qmlRegisterType<FileObject>("Coruitech.device",1,0,"FileObject")
  ```

  QML中导入并使用
  ```
  import Coruitech.device 1.0

  FileObject{
      id: fileObject
  }
  fileObject.setSource(id_folderlistmode.get(comboBox.currentIndex,"filePath"))
  var text = fileObject.read()
  ```  