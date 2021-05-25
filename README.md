[toc]
# 怎么又搞起flask框架了
最近搞深度学习，想在网页上部署一个简单的在线demo，之前尝试了一下onnxjs，但是貌似现在还不则么成熟，解析网络模型直接给我报错了。。。。所以还是改成前后端的部署方案。之前学习过一点点javaweb，但是感觉javaweb太过于笨重了，对于一些轻量级的网页简直就是高射炮打蚊子。加上后算需要结合pytorch进行一些推理，所以就往python后端框架方向看了下，对比了下django和flask，flask更轻量级一些，故选择flask

这是在线的demo：[http://www.yhqiao.xyz:5000/index](http://www.yhqiao.xyz:5000/index "http://www.yhqiao.xyz:5000/index")
能不能能访问随缘，因为服务器性能太羸弱了，内存只有2GB，在并发时，即很多个人访问并且推理时内存很容易爆掉，不过平时应该没什么问题，只要我flask（5000端口)开着就行
所有代码的github[https://github.com/YhQIAO/web_SOD](https://github.com/YhQIAO/web_SOD "https://github.com/YhQIAO/web_SOD")

# 整体技术方案
## U2Net网络
这是一个很强大的显著性检测模型，2020年cvpr，效果很好，具体的网络实现是从GitHub git clone下来的，别人已经写好了

## flask
这几天用下来的感受就是flask很方便，十分轻量级，像这种功能十分简单的网页搭建轻轻松松就能搭建了，后端与还能喝Pytorch直接结合，十分方便，太方便了

flask项目的基本结构
- static
	存放静态文件，比如css，javascript，图片文件之类的数据
- templates
	存放网页模板文件，html
- python脚本以及其他文件


## ajax
之前学web技术学到ajax这里就没有继续深入了，当时以为是个比较复杂的技术，结果看下来在jquery里直接定义就行了，规定好数据类型和要发送的数据等就可以实现异步调用了，好处就是不用每发送一次消息就刷新一次网页，真正实现了动态网页的概念

这个项目要传送图片到后端，也就是传送文件。注意在封装为json时候要序列化

## 前端
这个没什么好讲的，主要就是flask里面用到了jinja2对网页进行渲染，类似jsp那种在网页里嵌入后端代码的形式。


