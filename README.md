#在线词典
1. 确定好技术方案（套接字，并发，确定细节）

    * 数据传输：TCP
    * 多进程并发：由于Python线程GIL原因且IO操作较多，故此使用进程

2. 数据表进行建立（dict：words）
    * words单词表：单词id 单词word 释义explanation
    * userinfo用户信息表：id 账号account 密码password 用户名username
    * history历史记录表：用户id（用于查询用户的查询记录） 查询内容record 查询时间time

3. 结构设计：几个模块 封装设计
    * 服务端：
        * 通信模块TCPServer
            1. 主进程循环接受来自客户端的连接
            2. 收到连接创建新进程处理客户端事件

        * 逻辑处理模块
        * 数据库管理模块
    * 客户端：
        * 通信模块--TCP
        * 图形交互模块
        * 逻辑处理模块

4. 功能分析 和 通信搭建
    * 一级界面(登录界面)：
         * 登录/注册--输入账号密码
         * 成功则进入查询界面，失败返回返回界面 账号不能重复
         * 输入*exit退出登录
    * 二级界面(查询界面)：
         * 查单词 正确得到释义，错误/没有得到“抱歉，没有找到，臣妾会努力完善的”
         * 输入#n号查询历史记录 n为查询个数 ##查询全部记录
         * 输入*号退出查询，返回登录界面

    * 通信协议：
         *登录： LOGIN account password
         *注册： LOGON account password username
         *查询： SEARCH word
         *历史： HISTORY number
         *退出： EXIT

5. 罗列功能逻辑（每个功能确定服务端和客户端该做什么，编写代码测试）
    * 服务端：
         * 循环等待连接
         * 为连接创建新进程
         * 循环接收客户端登录信息
         * 校对信息，错误返回上一步，成功进入查询
         * 循环接收客户端查询内容
         * 从本地数据库搜索需求信息
         * 返回查询结果
    * 客户端：
         * 循环输入用户信息
         * 待服务端校对成功进入查询，否则返回上一步
         * 循环输入查询内容
         * 接收查询结果
         * 打印结果