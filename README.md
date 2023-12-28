# python_tool
使用python开发的一些插件和一些cmd命令行脚本

## checkSpine ##

**无任何环境依赖，使用者不用安装py环境**

**_对路径下的spine动效进行检查是否符合开发规则，减少对spine动效导出的json文件的阅读成本_**

-  window可将该插件写入 *右键* 注册表，方便在多文件夹下操作
-  输出信息：
   - 动效dc值 `(只做参考用，实际运行时的dc会根据动画播放波动<=该值)`
   - 用到的的图集尺寸 `(对尺寸超过2048x2048的图集 输出警告)`
   - 所有可以执行 **_替换插槽_**  逻辑的插槽名 `(对某些动画中存在影响替换插槽的 -附件帧- 输出警告 )`
   - 动画中存在的帧事件 `(本项目中存在普通帧事件、符合开发命名规则的帧事件，对不符合开发规则的事件 输出警告)`
   - 支持对指定文件的检测，支持文件夹下多文件检测
   
   - https://user-images.githubusercontent.com/32084033/220075140-aeccf210-6a64-4c1c-a5b5-c72f325708bf.mp4


## previewCurve ##

**无任何环境依赖，使用者不用安装py环境**

**_右键json文件快速预览spine动效_**
**_只展示spine的dc，无其他元素渲染影响_**
-  window可将该插件写入 *右键* 注册表，方便在多文件夹下操作
-  (preview) spine动效预览模式，实现控制spine播放进度（类似视频播放器进度条）
-  (curve) spine动效飞行曲线预览模式，实现可视化修改调整spine骨骼点，动效实现效果，程序调整骨骼坐标即可

   -  curveDemo：操作骨骼调整曲线动画demo

   -  https://user-images.githubusercontent.com/32084033/220071806-449d21a9-ecd9-41b2-96bd-2ca94502d84e.mp4

-  (replace) spine插槽替换预览模式，实现可视化替换资源到spine的插槽中（实现替换插槽和还原插槽）

   -  replaceDemo：替换插槽demo

   -  https://user-images.githubusercontent.com/32084033/220016493-d3e76cb4-a847-469f-a696-a0b0e6a0eff9.mp4

-  todo
   - (follow) 骨骼/插槽跟随模式，实现可视化生成节点到spine的骨骼/插槽位置，并根据骨骼/插槽的（坐标，缩放，旋转，透明度，颜色）属性变化而变化
   
## system ##

**_用py实现一些cmd命令行打包成exe文件，并将本文件夹配置到环境变量中，就可以在cmd下快捷调用实现的脚本_**
- 目前包括：

| 命令        | 介绍 |
| ---         | --- |
| close       | `1分钟后关机` |
| unclose     | `停止关机` |
| lock        | `锁屏` |
| restart     | `重启` |
| rmMeta      | `删除本文件夹下的所有meta文件` |
| sendemail   | `发送邮件` |
| updateLight | `修改屏幕亮度(对于不支持修改屏幕亮度电脑无法修改)` |
  
## tip ##  
- 发出神秘声音  from: (https://minecraft.fandom.com/zh/wiki/%E6%9D%91%E6%B0%91)

## linkCmd ##
- 本项目打包流程：构建astc文件->将astc文件复制到assets下指定目录->package工具打包成aab包->复制最终的resources资源到项目的入口服务器下
- linkcmd对原有打包流程的无侵入式整合，一键打包，没有中间步骤，可以自定义构建完成之后的命令 `如本工具组中的tip，system等命令`

## rmWindowSearch ##  
- 屏蔽window10系统中快捷搜索功能的 **_网页搜索_**，只搜索本系统中的文件

## util ##  
- 用python实现的工具类
- addWinPath.py可以将util工具类导入python库，就可以在其他路径下的python脚本中引用该util类
- 包含了发邮件，获取天气预报，修改显示屏亮度等功能的实现

## excel2ts ##  
- excel文件转声明文件
- 目前只测试了 *.csv, *.xls
   - cfg.json 配置表格的注释，类型，属性，数据的所在行
      - desc_line: 对应的ts中的属性的注释
      - type_line: 对应的ts中的属性的类型
      - param_line: 对应的ts中的属性名
      - data_line: excal的数据的开始行
```
XXXConfig.ts
export interface XXXConfig {
   /** 注释 */
   xxx: number;
}
```

## py2exe ##
- 将python脚本通过pyinstaller打包成exe文件，即可无py环境运行
   - 添加右键快捷（管理员运行）.bat 将py2exe加入 *.py 文件的右键列表中，方便在任意文件夹下一键 .py文件转.exe
   - 删除右键快捷（管理员运行）.bat  删除.py文件的py2exe删除掉

## cc ##

- py中解析ccc的预制体文件
   - 将prefab文件解析成对应的node、compoment的用法
   - 保证节点/组件的方法、属性用法同ts中写法一致和有代码提示
   - todo
      - [ ] prefabInfo解析，对应prefab引用外部prefab的情况
