# 2019-nCov-data

简体中文 | [English](README.en.md)

本项目为2019新型冠状病毒（COVID-19/2019-nCoV）疫情状况的时间序列数据仓库，数据来源为[丁香园](https://ncov.dxy.cn/ncovh5/view/pneumonia)、[南都传媒](https://m.mp.oeeee.com/h5/pages/v20/nCovcase/guangdong.html)和[腾讯新闻](https://xw.qq.com/act/fytrace?from=singlemessage&isappinstalled=0&scene=1&clicktime=1581821123&enterid=1581821123)。
#
本项目数据包括：轨迹数据，同乘数据，新闻数据，谣言数据（后续会更新其他方面，尽量保持数据仓库完整）
#
希望用这些数据做科研之用，因此做了这个数据仓库，直接推送大部分统计软件可以直接打开的csv文件，希望能够减轻各位的负担。 
后期会部署服务器并提供API的使用和JSON数据接口，如有需要可以关注，后期我会进行数据清洗以后进行封装调用接口。

###   CSV文件列表     
*       新闻数据    covid_news.csv 
        轨迹数据    covid_patient_track.csv
        谣言数据    rumor.csv
        同乘数据    covid_virus_trip.csv

###   项目介绍
#
本项目每一小时钟访问并爬取一次数据(实际程序可以调控爬取时间，但为了减轻目标服务器负载建议10 - 60分钟一次)，储存在MySQL中，并且保存所有历史数据的更新，希望能够在未来回溯病情时能有所帮助。

### 数据表
```sql
CREATE TABLE `covid_news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `adoptType` int(255) DEFAULT NULL,
  `dataInfoOperator` varchar(255) DEFAULT NULL,
  `dataInfoState` int(255) DEFAULT NULL,
  `createTime` bigint(20) DEFAULT NULL,
  `dataInfoTime` bigint(20) DEFAULT NULL,
  `entryWay` int(255) DEFAULT NULL,
  `infoSource` varchar(255) DEFAULT NULL,
  `infoType` int(11) DEFAULT NULL,
  `modifyTime` bigint(20) DEFAULT NULL,
  `provinceId` int(11) DEFAULT NULL,
  `provinceName` varchar(255) DEFAULT NULL,
  `pubDate` bigint(20) DEFAULT NULL,
  `pubDateStr` text,
  `sourceUrl` text,
  `summary` text,
  `title` text,
  `new_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1401 DEFAULT CHARSET=utf8 COMMENT=']'


CREATE TABLE `covid_patient_track` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(255) DEFAULT NULL,
  `district` varchar(255) DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `is_today` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10960 DEFAULT CHARSET=utf8


CREATE TABLE `covid_rumor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text,
  `mainSummary` varchar(255) DEFAULT NULL,
  `rumorType` int(255) DEFAULT NULL,
  `score` int(255) DEFAULT NULL,
  `sourceUrl` varchar(255) DEFAULT NULL,
  `summary` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `rumor_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8


CREATE TABLE `covid_virus_trip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tripType` varchar(255) DEFAULT NULL,
  `tripDate` varchar(255) DEFAULT NULL,
  `tripNo` varchar(255) DEFAULT NULL,
  `tripDepname` varchar(255) DEFAULT NULL,
  `tripArrname` varchar(255) DEFAULT NULL,
  `tripDepcode` varchar(255) DEFAULT NULL,
  `tripArrcode` varchar(255) DEFAULT NULL,
  `tripDeptime` varchar(255) DEFAULT NULL,
  `tripArrtime` varchar(255) DEFAULT NULL,
  `carriage` varchar(255) DEFAULT NULL,
  `seatNo` varchar(255) DEFAULT NULL,
  `tripMemo` text,
  `link` text,
  `publisher` varchar(255) DEFAULT NULL,
  `publishtime` varchar(255) DEFAULT NULL,
  `verified` varchar(255) DEFAULT NULL,
  `codeList` varchar(255) DEFAULT NULL,
  `nameIndex` varchar(255) DEFAULT NULL,
  `createtime` varchar(255) DEFAULT NULL,
  `updatetime` varchar(255) DEFAULT NULL,
  `virus_trip_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2451 DEFAULT CHARSET=utf8


CREATE TABLE `covid_txnew_track` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `confid` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `county` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `user_num` varchar(255) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `other_info` varchar(255) DEFAULT NULL,
  `track` varchar(255) DEFAULT NULL,
  `target` varchar(255) DEFAULT NULL,
  `pub_time` varchar(255) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `source_url` varchar(255) DEFAULT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `contact_detail` varchar(255) DEFAULT NULL,
  `hashtag` varchar(255) DEFAULT NULL,
  `lasttime` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8


```
### 捐赠
#
本项目不需要任何捐赠。
全国各地的医疗资源都处于短缺的状态。如果希望捐赠的人，请移步各个红十字会或者官方认可的捐赠平台，他们能够更加妥善地运用这笔资金，帮助更有需要的人。
祝大家一切都好。

### 最后声明
#
1. 本项目完全出于公益目的，如果未来用作商业目的或产生任何不必要的版权纠纷，本项目不负任何责任；
2. 本项目仅获取丁香园和南都传媒的疫情数据并将其储存，数据所有权为丁香园和南都传媒，本人无法授权任何个人或团体在科研或商业项目中使用本数据，如有需要，希望您能够联系丁香园和南都传媒并取得许可；
3. 如有其它问题可留言
4. 感谢我的小伙伴帮我收集全国卫健委资料(该部分还没开始做，会尽快开始)

