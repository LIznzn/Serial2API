Serial2API
====================

### Protocol

#### Header

| Version | Token | CMD | Payload Length | TAG | Fragment Order | Payload Checksum | Payload |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
| 01 | FFFF | 00 | FFFF | 00 | FFFF | FFFF | 123456789ABCDEF

#### CMD

| Bit | Information | 
| ---- | ---- | 
| 00 | ACK | 
| 01 | Text Message | 
| 02 | Binary Message | 
| FF | RST | 

#### TAG

| Bit | Information | 
| ---- | ---- | 
| 00 | 无下一分片 | 
| 01 | 有下一分片 |

#### Payload Length

Maximum 65535 Bytes

#### Fragment Order

Maximum 65536 Fragments