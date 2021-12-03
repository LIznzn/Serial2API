Serial2API
====================
### Config
```
[TX]
device = /dev/tty.usbserial-1430
baudrate = 9600
bytesize = 8
parity = N
stopbits = 1
timeout = 5.0
attempt = 10

[RX]
device = /dev/tty.usbserial-1430
baudrate = 9600
bytesize = 8
parity = N
stopbits = 1
timeout = 5.0

[Server]
ip = 0.0.0.0
port = 5000
debug = True
```

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