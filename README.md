Serial2API
====================

### 协议

Header

| 版本 | Token | CMD | 数据长度 | TAG | 分片顺序 | 数据 |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 01 | FFFF | 00 | FFFF | 00 | FFFF | 123456789ABCDEF

CMD

| CMD | 信息 | 
| ---- | ---- | 
| 00 | ACK | 
| 01 | Message | 
| 02 | Image | 
| FF | RST | 

TAG

| TAG | 信息 | 
| ---- | ---- | 
| 00 | 无下一分片 | 
| 01 | 有下一分片 |