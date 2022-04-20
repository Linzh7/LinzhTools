# LinzhTools
## 常用数据集处理工具
包含如下功能：
- 转移成对的文件（数据与标记）
- 删除符合某个pattern的东西
- 批量剪切文件（DEBUG是用来测试的，免得弄错了）
- 批量复制文件（DEBUG是用来测试的，免得弄错了）
- 打印不属于指定的东西
- 获得文件列表
- 获得文件夹列表
- 获得文件内容
[LinzhUtil.py](https://github.com/Linzh7/LinzhTools/blob/master/LinzhUtil.py)

## 图像数据集格式转换
比如语义识别，大部分数据集给的是RGB标定，然后再给一个map。

而为了模型处理方便，很多需要转换成x级灰度（往往是256级），每个类型是一个灰度级。

还有比如二值化然后再输入等等很多种很麻烦的转换，这是综合工具。

如果存在多对一的映射，比如几个标定都代表行人，记得使用revers方法。

[ImgDatasetProcess.py](https://github.com/Linzh7/LinzhTools/blob/master/ImgDatasetProcess.py)

## Wordpress的XML备份转换成Hugo等使用的Markdown
字面意思

## 引用编码自动顺序排列
[CitesIndexRearrange.py](https://github.com/Linzh7/LinzhTools/blob/master/DocumentTools/CitesIndexRearrange.py)
如果撰写文章的时候，Word中的引用不按顺序，但又被要求按顺序引用，则可以使用此工具。功能如下：

[x] 自动替换文内引用序号

[x] 自动替换文末引用序号

[x] 自动识别文内引用分隔符`,`与连续引用标记`-`

[x] 写入文内引用时，自动添加引用分隔符`,`

[ ] 写入文内引用时，自动添加连续引用标记`-`

[ ] 自动对文末引用排序

[ ] 保留文中的图片、公式等内容

因而，目前来说还有功能不太完善，但可以手动对着无图片的版本修改。且大段的文字可以直接替换，如intro, related work，都可以减轻工作量。

## 引用格式转换（主要针对GB）
[CitesTransform.py](https://github.com/Linzh7/LinzhTools/blob/master/DocumentTools/CitesTransform.py)
目前仅支持少数格式（而且不一定对）
