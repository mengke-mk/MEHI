.. __utils:

实用工具
========
这里介绍项目中的一些辅助函数。


tool
----
这个包下面放着一些logging，测定时间，显示信息，通知报错的方法。


exeTime(func)
^^^^^^^^^^^^^
一个装饰器，放在需要测时间的函数前面就能在函数调用的时候得到其运行时间，由于spark的lazy机制，无法测定用到rdd的函数的运行时间。

.. code-block:: python

    @exeTime
    def func():
        pass


showsize(obj, name = '')
^^^^^^^^^^^^^^^^^^^^^^^^
显示一个对象的大小，会自动转单位。

.. code-block:: python

    showsize(img_stack, 'L side images')


bar(level)(msg, i ,end)
^^^^^^^^^^^^^^^^^^^^^^^
一个curry化的log函数，使用了特别的染色技巧，会输出一个进度条一样的东西，只在串行的时候使用，并行采用spark自带的进度条。用在循环里。

log(level)(msg)
^^^^^^^^^^^^^^^
一个curry化的log函数，使用了特别的染色技巧,会根据level显示不同的颜色，loglevel = ['debug','info','time','error','warn']。用这个函数来输出信息。另外如果需要把日志写到文件中，则推荐使用python自带的 `logging` 模块，这个模块没有染色。但是格式化功能很强大。

.. code-block:: python

    log('info')('fusion start ....')

send_mail(sub, content)
^^^^^^^^^^^^^^^^^^^^^^^
一个反人类的函数，一般把它放到try-catch块里，用于报错，程序出错后会发邮件。使用时请更改函数里面的 `main_to` ，不然就会给我发邮件了。


mha2tiff
--------
一个用来实现mha和tiff互相转换的工具，如果报错大部分可能都是格式的问题，参见 `FAQ` 这一章

read_mha(fn)
^^^^^^^^^^^^
以numpy中的 `ndarray` 形式，根据fn文件名读取一个文件到内存中。

write_mha (data, fn)
^^^^^^^^^^^^^^^^^^^^
把内存中一个 `ndarray` 的对象，以fn的名字保存

visualization
-------------
上一个版本的可视化脚本，需要pyVTK的支持，甚至还能把图像输出成.avi格式的视频，然而使用需要能修改脚本，因为读取的细胞文件名是写死了的，见该文件的28～29行。

.. code-block:: python

    vis = Visualization()
    vis.debug()




configuration
-------------
没什么用处，上个版本的遗留产物，本来准备写成根据配置来运行的，但是没有时间搞这个。忽略它但不要删除它。
