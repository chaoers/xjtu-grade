# xjtu-grade

西安交通大学成绩查询排名计算爬虫

## V2.0 Preview

这个项目正在用utils重构中
项目进度: [@guitaoliu](https://github.com/guitaoliu/xjtu-grade)
`utils` 同步进度

## 项目简介

今年暑期学校教务处突然开启了成绩排名可查询，听说之前也开放过后来关了就想写个爬虫把数据记录下来

目前只对有意义的数据进行显示，但实际还爬到了一些很难处理的数据，如果有大佬想继续研究的话可以取消代码中某些注释(笑

目前表格中的项目有

- 学年学期
- 课程名
- 课程类别
- 课程性质
- 学分
- 学时
- 成绩
- GPA
- 及格
- 超过百分比
- 平时成绩
- 期末成绩
- 平均分
- 最低分
- 最高分

## 使用指北

### 项目依赖

本项目依赖

- python 3

python包依赖
- selenium（请确保能够正常运行，包括配置webdriver等
- xlwt

### Selenium教程

具体教程请移步我的博客[饭饭的Selenium+xlwt笔记](https://asterisk.plus/archives/188)

### 运行

打开`spider/spider.py`

在开头处填写`NetID`和密码（请放心该项目没有记录任何信息

运行文件

在运行目录下生成`Grade.xls`成绩表格

Enjoy it~

## 开源协议

本项目遵循`GPLV3.0`开源协议

**请注意遵循开源协议并不意味着可以随意使用，具体规范请具体查看`GPLV3`协议内容**


If you likes this repo, Please give me a star~