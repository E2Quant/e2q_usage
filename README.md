# 一个可正式运行的案例


## 准备的资料

- 基本
    - 系统 debian 12 (bookworm)
    - 报价 python 代码: [TickForPy](https://github.com/E2Quant/e2q_ticket/tree/main/TickForPy)
    - 数据库([postgresql](https://www.postgresql.org/download/))
    - [kafka](https://kafka.apache.org/downloads)
    - [Apache ZooKeeper](https://zookeeper.apache.org/releases.html)
    - 当前目录[backtest] 回测的 E2L 语言案例代码
    - 当前目录[e2q_log] Python 写的查看日志代码
- 安装配置
    - E2Q 系统安装 请 [参考](https://github.com/E2Quant/e2q_doc/blob/main/docs/Installation.md)
    - kafka topic 的创建, 会在 e2l 语言中自动创建
- 运行
    - 回测
    - 在线
- 数据查看
    - 数据库
    - 日志

### 安装配置 

- postgresql 配置 
    - 创建相对应的权限
    - 创建数据库 [SQL 文件](https://github.com/E2Quant/e2q/blob/main/cfg/e2q_postgresql.sql)
- 运行 kafka
    ```shell
    ## apache-zookeeper
    sudo ./bin/zkServer.sh --config ./conf start

    ## kafka
    sudo ./bin/kafka-server-start.sh -daemon config/server.properties
    ```

### 运行

- 单 symbol 的模式

    * E2Q 端，以下是在编译好的目录中
        ``` shell
            ./e2q -p ../cfg/db.properties -e  /opt/e2q_usage/backtest/ea/Enter/Single/ma_es.e2 -s /opt/e2q_usage/backtest/oms/main.e2 -r 0 -f logs
        ```
    
    * Tick 报价端, 最近 200 交易日的报价

        ``` shell
            python TickFromHdf5.py backtest day -200 0

        ```

- 多 symbol 的模式

    * E2Q 端，以下是在编译好的目录中
        ``` shell
            ./e2q -p ../cfg/db.properties -e  /opt/e2q_usage/backtest/ea/Enter/MvoRisk/ma_mr.e2  -s /opt/e2q_usage/backtest/oms/main.e2 -r 0 -f logs
        ```
    
    * Tick 报价端, 最近 200 交易日的报价

        ``` shell
            python TickFromHdf5.py btall  day -200 0

        ```

- 在线模式，可参考 python 中的 market 函数

### 数据查看

- 数据库

```SQL

E2Q=> \x on
Expanded display is on.
E2Q=> select * from e2q_history limit 2;
-[ RECORD 1 ]+-----------------------
sid          | 2
verid        | 1
symobl       | 179593
stock        | 600519
buy_price    | 1811.24
buy_time     | 2023-11-03 00:00:00+08
stop_price   | 1812
stop_time    | 2023-11-06 00:00:00+08
sell_adjpx   | 11131.702
buy_adjpx    | 11127.425
profit       | 0.038
closetck     | 1032451500
LossOrProfit | StopLoss
cash         | 0
share        | 0
quantid      | 1032451500
bticket      | 1032451500
sticket      | 1032451502
position     | 0.9
amount       | 304
qty          | 4
-[ RECORD 2 ]+-----------------------
sid          | 7
verid        | 1
symobl       | 179593
stock        | 600519
buy_price    | 1791.17
buy_time     | 2023-11-07 00:00:00+08
stop_price   | 1798.34
stop_time    | 2023-11-08 00:00:00+08
sell_adjpx   | 11054.827
buy_adjpx    | 11014.476
profit       | 0.366
closetck     | 1032451506
LossOrProfit | StopLoss
cash         | 0
share        | 0
quantid      | 1032451500
bticket      | 1032451506
sticket      | 1032451508
position     | 0.9
amount       | 717
qty          | 1


```

- 查看日志

```shell
[e2q_usage/e2q_log]$ python log_bin.py /opt/e2q/build/logs/3967251_0_.log 0 10
2025-06-24 11:15:46.813 | INFO     | __main__:read_log:50 - row: 45
  logt numt          value  deci  loc                ticket_now      pid      vname                                               path       func
0    T    P  1721232000000     0  303 2024-07-19 00:00:00+08:00  3967251      ptime  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintTime
1    P    P         188600     3  304 2024-07-19 00:00:00+08:00  3967251   now_open  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
2    P    P         186400     3  305 2024-07-19 00:00:00+08:00  3967251    now_low  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
3    P    P         190000     3  306 2024-07-19 00:00:00+08:00  3967251   now_high  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
4    P    P         189700     3  307 2024-07-19 00:00:00+08:00  3967251  now_close  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
5    T    P  1721318400000     0  303 2024-07-22 00:00:00+08:00  3967251      ptime  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintTime
6    P    P         189600     3  304 2024-07-22 00:00:00+08:00  3967251   now_open  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
7    P    P         189200     3  305 2024-07-22 00:00:00+08:00  3967251    now_low  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
8    P    P         194400     3  306 2024-07-22 00:00:00+08:00  3967251   now_high  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci
9    P    P         193900     3  307 2024-07-22 00:00:00+08:00  3967251  now_close  /opt/e2q_usage/backtest/ea/Physical/ModeGuide/...  PrintDeci

```