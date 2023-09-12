# 更新记录
- 2023-09-11的数据已上传；
- 2023-09-10的数据已上传；
- 2023-09-08的数据已上传；
- 2023-09-07的数据已上传；
- 2023-09-06的数据已上传；

# 使用说明
以下代码用来更新防治表的信息
```sql
UPDATE "2023_美国白蛾_3代_防治表"
SET "点位编号" = (
    SELECT "点位编号"
    FROM "2023_美国白蛾_3代_调查表"
    WHERE "点位名" = "2023_美国白蛾_3代_防治表"."点位名"
)
WHERE EXISTS (
    SELECT 1
    FROM "2023_美国白蛾_3代_调查表"
    WHERE "点位名" = "2023_美国白蛾_3代_防治表"."点位名"
);
```

## 数据录入说明
数据都是存在本地的`sqlite`数据库中，因此需要先录入数据，然后才能生成各种统计数据和后续的派单生成操作。

由于虫种的不同，各个数据表的字段也不完全一样，但是有一些是共有的，这些字段是必填项（**字必须完全一致且没有空格等符号**）。

**调查表**
- 「调查日期」：该字段用于和防治表的防治日期进行比较，以此来判断是否防治；
- 「点位编号」：点位编号是非常重要的核心字段，因为所有的次数计算和合格情况都依托于该字段聚合，因此对于那些没有明确编号的点位（例如蚜虫的调查点或者美国白蛾的乡镇点位）应该使用调查地的简要位置描述来填写，**不能使用空白代替**；
- 「乡镇/街道」：点位所属的区划；
- 「点位名」：一般而言是用于补充点位编号的信息，例如位置的描述；
- 「详细描述」：点位发生情况的详细描述，包括位置信息和受害情况，对于没有发生危害的点位可以为空；
- 「备注」：其他补充信息；
- 「调查结果」：合格/不合格，必须是这两者之一，用于对一个点位最终状态进行判断；

**防治表**
- 「防治日期」：如上文所述，必填项；
- 「点位编号」：同上调查表；



## 主页
暂时还没想好要实现的功能。

## 美国白蛾

## 国槐尺蠖

## 蚜虫


## 派单
对于有的虫种，有些字段是必须的，否则无法生成派单，因此对于其他虫种会进行一些自动计算的填充。
- 「网幕数」：这一个比较特殊，当前的模版中必须要求有数量，也就是说即使不是美国白蛾这一虫种，也需要填 0，目前我的处理方式是对于蚜虫类填 0，尺蠖类就填 5 个标准枝上的总虫口数量；
- 「地块类型」：美国白蛾的数据中会包含该字段，因此会直接填充，对于国槐尺蠖和春尺蠖，会填入「平原造林」，对于蚜虫会填入「行道树」；