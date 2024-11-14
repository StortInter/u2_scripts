# U2 Scripts

### 脚本列表

- auto_del.py

  deluge 客户端自动删种

- auto_magic_seeds.py

  给有上传速度的种子放魔法(支持各种 bt 客户端)
  
- catch_magic.py
  
  追魔/搭桥(不限客户端)
  
- download_new_torrents.py
  
  自动下载新种
  
- find_torrent.py
  
  根据文件名反查种子并添加到 qb 客户端
  
- give_sugar.py
  
  发糖
  
- my_bencoder.py
  
  自用 bencode 格式编码与解码
  
- qb_del.py
  
  从 qb 客户端删除赚分效率不高的种子
  
- rename_torrents.py
  
  按种子标题重命名种子文件(仅支持 qb)
  
- u2_auxseed.py
  
  u2辅种(仅支持 qb)
  
- u2_magic.py
  
  放魔法/限速(支持客户端 qb 和 de)

### 环境配置

使用 conda 配置环境

```bash
conda create -n tools python pytz requests bs4 loguru pymongo
```

