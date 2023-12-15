AIEarth Engine Python SDK

Visit the [AIEarth main page](https://engine-aiearth.aliyun.com/)
for more information.
    
# Quickstart

[快速入门](https://engine-aiearth.aliyun.com/docs/page/guide?d=c2989d)

## AIEarth Data 快速入门

> 重要：为了保障数据的传输速度，建议在平台托管Jupyter Notebook环境下使用

### 说明

AiEarth Data SDK可以使用户使用 `STAC` 标准接口访问我们的平台的公开数据和用户的私人数据。通过
指定数据唯一`STAC ID`并配合`offset + size`的办法，获取数据切片。

### 安装办法

1. 联系平台获取python模块安装包 `aiearth_data-1.0.0-py3-none-any.whl`
> 请联系钉钉用户群：32152986
2. 打开开发环境的终端（Terminal），安装Python模块

```shell
pip install '/path/to/aiearth_data-1.0.0-py3-none-any.whl'
```

3. 打开开发环境Notebook进行代码编写

### 使用案例

### 查询公开数据，并获取完整BGR波段数据

```python
# 初始化，并鉴权
import os

import numpy as np
from aiearth import core
import aiearth.data.search
from aiearth.data.search import PersonalQueryBuilder, personaldata_client, opendata_client
from aiearth.data.loader import DataLoader
from aiearth.data.stac_id import PersonalStacId, OpenStacId
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np

# 鉴权
core.Authenticate()
# 获取 STAC 客户端
client_opendata = opendata_client()
# 查询部分区域选定时间范围的Sentinel-2数据，并进行按云量从小到大排序
bbox = [116.30526075575888, 39.856226715750836, 116.45625485992359, 39.96534081463834]
search_req = client_opendata.search(collections=['SENTINEL_MSIL2A'], bbox=bbox,
                                    sortby=['+eo:cloud_cover'],
                                    datetime=(datetime(2022, 1, 1), datetime(2022, 3, 1)))

# 获取查询结果的第一个
item = list(search_req.items())[0]
print(item.id)

# 使用B4, B3, B2 查询所有数据
dataloader = DataLoader(OpenStacId(item.id))
dataloader.load()

shape = item.properties.get("proj:shape")
width, height = shape
print(width, height)

buffer_width, buffer_height = 2048, 2048
width_grid = int(width / buffer_width) + 1
height_grid = int(height / buffer_height) + 1

img = np.ndarray(shape=(width, height, 3))

for idx, band_name in enumerate(("B4", "B3", "B2")):
    channel = np.ndarray(shape=(width, height))
    for h in range(height_grid):
        for w in range(width_grid):
            x_offset = buffer_width * w
            y_offset = buffer_height * h
            this_buffer_width = buffer_width if x_offset + buffer_width <= width else width - x_offset
            this_buffer_height = buffer_height if y_offset + buffer_height <= height else height - y_offset
            block = dataloader.block(x_offset, y_offset, this_buffer_width, this_buffer_height, band_name)
            channel[x_offset: x_offset + this_buffer_width, y_offset: y_offset + this_buffer_height] = block
    img[:, :, idx] = channel


```

#### 查询个人数据，并获取完整B1波段数据

```python
# 引入aiearth基础包并进行鉴权
from aiearth import core

core.Authenticate()

# 引入 aiearth-data 及其他依赖
from aiearth.data.search import PersonalQueryBuilder, personaldata_client
from aiearth.data.loader import DataLoader
from aiearth.data.stac_id import PersonalStacId
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np

# 查询 2023-06-01 至 2023-06-15 上传/生产的，名字里含有 gaofen1_2m_5000 的个人数据
query = PersonalQueryBuilder()
    .and_name_contains("gaofen1_2m_5000")
    .and_upload_datetime_between(datetime(2023, 6, 1), datetime(2023, 6, 15))
    .build()
client = personaldata_client()
search_req = client.search(query=query)
items = list(search_req.items())

# 获取上一步结果第一幅影像的B1波段的全部数据
item = items[0]
item.properties

# properties 内容
{'meta:bandCount': 3,
 'meta:dataType': 'Byte',
 'description': '超分_gaofen1_2m_5000',
 'title': '超分_gaofen1_2m_5000',
 'proj:bbox': [113.14763797458761,
               29.51906661147954,
               113.24763840038761,
               29.619067037279542],
 'proj:epsg': -1,
 'datetime': '2023-06-14T16:38:27.056Z',
 'proj:shape': [13915, 13915],
 'proj:transform': [113.14763797458761,
                    7.18652e-06,
                    0.0,
                    29.619067037279542,
                    0.0,
                    -7.18652e-06],
 'meta:resX': 0.7999997333291894,
 'meta:resY': 0.799999733329161,
 'aie:band_names': ['B1', 'B2', 'B3'],
 'meta:uploadDatetime': '2023-06-14T16:38:27.056Z'}

# 循环获取B1波段全部数据
width, height = item.properties.get("proj:shape")
img = np.ndarray(shape=(width, height))

buffer_width, buffer_height = 2048, 2048
width_grid = int(width / buffer_width) + 1
height_grid = int(height / buffer_height) + 1

dataloader = DataLoader(PersonalStacId(item.id))
dataloader.load()

for h_idx in range(height_grid):
    for w_idx in range(width_grid):
        x_offset = buffer_width * w_idx
        y_offset = buffer_height * h_idx
        this_buffer_width = buffer_width if x_offset + buffer_width <= width else width - x_offset
        this_buffer_height = buffer_height if y_offset + buffer_height <= height else height - y_offset
        block = dataloader.block(x_offset, y_offset, this_buffer_width, this_buffer_height, "B1")
        img[x_offset: x_offset + this_buffer_width, y_offset: y_offset + this_buffer_height] = block

```