# CodeCraft2022-charge
这是自己写的华为2022软挑的判题器，欢迎大家使用，替换data output运行即可。

目前实现的功能包括计算成本，判断流量分配是否符合qos限制，判断流量分配对于客户节点是否满足了需求，判断流量分配对于边缘站点是否满足带宽限制

如有疑问欢迎提出，也欢迎交流一些解题思路。

# 初赛成渝前四，欢迎联系

正式赛写的判题器也放进来了，当时比赛前半小时写的，不一定正确（至少从线上结果来看不一定）

######


复赛判题器实现画图功能，picture picute_T_Load是两种不同画图方法

修改了一个小bug，之前计费方式是四舍五入所有site的费用之后再相加，现在改成了求和之后再四舍五入

#4.1 
复赛判题器初版（charge2）已上传，欢迎大家使用，有问题请联系，马上修正。

################################################

初赛判题器增加了画图查看每个site负载的功能，新增了数据生成和分析的功能。

#3.19
之前demand我测试的时候修改过 ，将demand改成和线下调试数据一致了。


#3.16

修改，在一个时刻中的输入方案可以乱序，并且可以找到重复出现或者缺少某个方案的分配信息

有朋友反映没有考虑到是小于qos约束的问题，我确实没考虑到，已修改。


###################################################

#3.15

#新增了判断名字对不对，这种
Site_name:
空的solution的报错也解决了。

#新增了判断solution的数量对不对。

###################################################

