# 数据表结构说明文档



## 微博数据表
    该表保存的是获取到的微博相关数据
    
    
|名称|类型|长度|允许为空|备注|
|:---|:---|:---|:---|:---|
|id|bigint|20|不允许|主键ID(自增)|
|msg_id|bigint|20|允许|微博ID 唯一索引|
|address|varchar|255|允许|微博发布地址|
|content|mediumtext|0|允许|文章的内容|
|msg_time|varchar|255|允许|微博发布时间|
|msg_timestamp|timestamp|0|允许|微博发布时间戳|
|tools|varchar|255|允许|微博发布工具|
|transmi_count|int|10|允许|转发数|
|comment_count|int|10|允许|评论数|
|praise_count|int|10|允许|点赞数|
|lng|float|0|允许|经度|
|lat|float|0|允许|纬度|
|created_at|timestamp|0|允许|数据创建时间|
|updated_at|timestamp|0|允许|数据更新时间|
    
 

### 建表语句

````
    DROP TABLE IF EXISTS `weibogis`;
    CREATE TABLE `weiboGis` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `msg_id` bigint(20) DEFAULT NULL,
      `address` varchar(255) DEFAULT NULL,
      `content` mediumtext,
      `msg_time` varchar(255) DEFAULT NULL,
      `msg_timestamp` datetime DEFAULT NULL,
      `tools` varchar(255) DEFAULT NULL,
      `transmi_count` int(10) DEFAULT NULL,
      `comment_count` int(10) DEFAULT NULL,
      `praise_count` int(10) DEFAULT NULL,
      `lng` float(64) DEFAULT NULL,
      `lat` float(64) DEFAULT NULL,
      `real_lng` float(64) DEFAULT NULL,
      `real_lat` float(64) DEFAULT NULL,
      `created_at` datetime DEFAULT NULL,
      `updated_at` datetime DEFAULT NULL,
      PRIMARY KEY (`id`) USING BTREE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    
    SET FOREIGN_KEY_CHECKS = 1;
```