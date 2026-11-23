11f0b00 retf 0x3776
11f0b03 mov rsi, qword ptr [rbx + rcx*8]
11f0b07 test rsi, rsi
11f0b0a je 0x1411f0b3a
11f0b0c mov eax, dword ptr [rsi + 0x78]
11f0b0f sub rdi, rax
11f0b12 lea rcx, [rsi + 0x20]
11f0b16 mov rdx, rdi
11f0b19 call qword ptr [rip + 0x7560b9]
11f0b1f cmp byte ptr [rsi + 0x48], 0
11f0b23 je 0x1411f0be4
11f0b29 lock dec dword ptr [rsi + 0x40]
11f0b2d setne al
11f0b30 test al, al
11f0b32 je 0x1411f0bee
11f0b38 jmp 0x1411f0b49
11f0b3a mov eax, dword ptr [rax + 0x30]
11f0b3d sub rdi, rax
11f0b40 mov rcx, rdi
11f0b43 call qword ptr [rip + 0x757447]
11f0b49 mov bl, 1
11f0b4b mov eax, ebx
11f0b4d add rsp, 0x1878
11f0b54 pop rbx
11f0b55 pop rdi
11f0b56 pop rsi
11f0b57 pop r12
11f0b59 pop r13
11f0b5b pop r14
11f0b5d pop r15
11f0b5f pop rbp
11f0b60 ret 
11f0b61 cmp esi, 0x434c4160
11f0b67 jle 0x1411f0c8f
11f0b6d cmp esi, 0x43574364
11f0b73 jg 0x1411f0dde
11f0b79 cmp esi, 0x434c5272
11f0b7f jle 0x1411f0fac
11f0b85 lea eax, [rsi - 0x434f5063]
11f0b8b cmp eax, 0xd
11f0b8e jbe 0x1411f102a
11f0b94 lea eax, [rsi - 0x434f5363]
11f0b9a cmp eax, 0xd
11f0b9d ja 0x1411f29e7
11f0ba3 lea rcx, [rip + 0x3166]
11f0baa movsxd rax, dword ptr [rcx + rax*4]
11f0bae add rax, rcx
11f0bb1 jmp rax
11f0bb3 mov rcx, rdi
11f0bb6 mov dl, 0x1c
11f0bb8 mov r8d, 0x636f6d70
11f0bbe jmp 0x1411f2a60
11f0bc3 xor eax, eax
11f0bc5 test al, al
11f0bc7 jne 0x1411f0aaf
11f0bcd cmp byte ptr [rsi + 0x61], 0
11f0bd1 je 0x1411f0aaf
11f0bd7 mov rcx, rsi
11f0bda call 0x1412d29c0
11f0bdf jmp 0x1411f0aaf
11f0be4 xor eax, eax
11f0be6 test al, al
11f0be8 jne 0x1411f0b49
11f0bee cmp byte ptr [rsi + 0x61], 0
11f0bf2 je 0x1411f0b49
11f0bf8 mov rcx, rsi
11f0bfb call 0x1412d29c0
11f0c00 jmp 0x1411f0b49
11f0c05 cmp esi, 0x54566360
11f0c0b jle 0x1411f0d2c
11f0c11 cmp esi, 0x66696c73
11f0c17 jle 0x1411f0e95
11f0c1d cmp esi, 0x73756273
11f0c23 jle 0x1411f1309
11f0c29 cmp esi, 0x74635253
11f0c2f jle 0x1411f1711
11f0c35 cmp esi, 0x74635254
11f0c3b je 0x1411f206f
11f0c41 cmp esi, 0x74746277
11f0c47 je 0x1411f2141
11f0c4d cmp esi, 0x7474636c
11f0c53 jne 0x1411f2a95
11f0c59 lea rdx, [rbp - 0x48]
11f0c5d mov rcx, rdi
11f0c60 call 0x1411ddc80
11f0c65 call 0x141335560
11f0c6a mov qword ptr [rbp - 0x50], rax
11f0c6e lea rsi, [rbp - 0x50]
11f0c72 mov rcx, r14
11f0c75 mov rdx, rsi
11f0c78 call 0x14083d5a0
11f0c7d mov rcx, qword ptr [rbp - 0x50]
11f0c81 mov rax, qword ptr [rcx]
11f0c84 mov rdx, rsi
11f0c87 call qword ptr [rax + 0x10]
11f0c8a jmp 0x1411f0b49
11f0c8f cmp esi, 0x43474d62
11f0c95 jg 0x1411f0da0
11f0c9b cmp esi, 0x43464763
11f0ca1 jg 0x1411f0fdb
11f0ca7 lea eax, [rsi - 0x43424461]
11f0cad cmp eax, 0xe
11f0cb0 jbe 0x1411f104a
11f0cb6 lea eax, [rsi - 0x43425761]
11f0cbc cmp eax, 0xe
11f0cbf ja 0x1411f18d5
11f0cc5 lea rcx, [rip + 0x2ea4]
11f0ccc movsxd rax, dword ptr [rcx + rax*4]
11f0cd0 add rax, rcx
11f0cd3 jmp rax
11f0cd5 mov rcx, rdi
11f0cd8 mov dl, 8
11f0cda mov r8d, 0x6f676c73
11f0ce0 jmp 0x1411f2a60
11f0ce5 cmp esi, 0x43595362
11f0ceb jle 0x1411f0f3d
11f0cf1 cmp esi, 0x43616c73
11f0cf7 jg 0x1411f139a
11f0cfd lea eax, [rsi - 0x43595363]
11f0d03 cmp eax, 0xd
11f0d06 ja 0x1411f2a95
11f0d0c lea rcx, [rip + 0x306d]
11f0d13 movsxd rax, dword ptr [rcx + rax*4]
11f0d17 add rax, rcx
11f0d1a jmp rax
11f0d1c mov rcx, rdi
11f0d1f mov dl, 0x1b
11f0d21 mov r8d, 0x636f6d70
11f0d27 jmp 0x1411f2a60
11f0d2c cmp esi, 0x5443736d
11f0d32 jg 0x1411f0f08
11f0d38 cmp esi, 0x54436f68
11f0d3e jg 0x1411f1099
11f0d44 cmp esi, 0x54436e6d
11f0d4a jg 0x1411f1463
11f0d50 cmp esi, 0x54436d67
11f0d56 je 0x1411f1b01
11f0d5c cmp esi, 0x54436e67
11f0d62 jne 0x1411f2a95
11f0d68 movsx esi, byte ptr [rdi + 0xb8]
11f0d6f call 0x14083caf0
11f0d74 add rax, 0x28
11f0d78 mov dword ptr [rbp - 0x48], esi
11f0d7b mov qword ptr [rbp - 0x50], rax
11f0d7f lea rsi, [rbp - 0x50]
11f0d83 mov rcx, r14
11f0d86 mov rdx, rsi
11f0d89 call 0x14083d5a0
11f0d8e mov rcx, qword ptr [rbp - 0x50]
11f0d92 mov rax, qword ptr [rcx]
11f0d95 mov rdx, rsi
11f0d98 call qword ptr [rax + 0x10]
11f0d9b jmp 0x1411f0b49
11f0da0 lea eax, [rsi - 0x43474d63]
11f0da6 cmp eax, 0xd
11f0da9 jbe 0x1411f100a
11f0daf lea eax, [rsi - 0x43485361]
11f0db5 cmp eax, 0xe
11f0db8 ja 0x1411f106a
11f0dbe lea rcx, [rip + 0x2e9b]
11f0dc5 movsxd rax, dword ptr [rcx + rax*4]
11f0dc9 add rax, rcx
11f0dcc jmp rax
11f0dce mov rcx, rdi
11f0dd1 mov dl, 0x19
11f0dd3 mov r8d, 0x6f676c73
11f0dd9 jmp 0x1411f2a60
11f0dde cmp esi, 0x43575266
11f0de4 jg 0x1411f0f6c
11f0dea cmp esi, 0x43574c64
11f0df0 jle 0x1411f1332
11f0df6 cmp esi, 0x43574c72
11f0dfc jg 0x1411f1413
11f0e02 cmp esi, 0x43574c65
11f0e08 je 0x1411f1b8a
11f0e0e cmp esi, 0x43574c67
11f0e14 jne 0x1411f2a95
11f0e1a mov rcx, rdi
11f0e1d mov dl, 0xe
11f0e1f mov r8d, 0x67616d73
11f0e25 jmp 0x1411f2a60
11f0e2a cmp esi, 0x4e41666d
11f0e30 jg 0x1411f110c
11f0e36 cmp esi, 0x436e6b6d
11f0e3c jg 0x1411f14db
11f0e42 cmp esi, 0x436d6e61
11f0e48 je 0x1411f1b9a
11f0e4e cmp esi, 0x436d7861
11f0e54 jne 0x1411f2a95
11f0e5a mov rax, qword ptr [rdi + 0xb0]
11f0e61 mov esi, dword ptr [rax + 0x70]
11f0e64 call 0x14083caf0
11f0e69 add rax, 0x28
11f0e6d mov dword ptr [rbp - 0x48], esi
11f0e70 mov qword ptr [rbp - 0x50], rax
11f0e74 lea rsi, [rbp - 0x50]
11f0e78 mov rcx, r14
11f0e7b mov rdx, rsi
11f0e7e call 0x14083d5a0
11f0e83 mov rcx, qword ptr [rbp - 0x50]
11f0e87 mov rax, qword ptr [rcx]
11f0e8a mov rdx, rsi
11f0e8d call qword ptr [rax + 0x10]
11f0e90 jmp 0x1411f0b49
11f0e95 cmp esi, 0x5476636f
11f0e9b jg 0x1411f1135
11f0ea1 cmp esi, 0x54635372
11f0ea7 jg 0x1411f1530
11f0ead cmp esi, 0x54566361
11f0eb3 je 0x1411f16ec
11f0eb9 cmp esi, 0x54634672
11f0ebf jne 0x1411f2a95
11f0ec5 mov rcx, qword ptr [rip + 0x96e474]
11f0ecc mov rax, qword ptr [rcx]
11f0ecf mov rdx, rdi
11f0ed2 call qword ptr [rax + 0x48]
11f0ed5 mov bl, al
11f0ed7 call 0x14083caf0
11f0edc add rax, 0x18
11f0ee0 mov byte ptr [rbp - 0x48], bl
11f0ee3 mov qword ptr [rbp - 0x50], rax
11f0ee7 lea rsi, [rbp - 0x50]
11f0eeb mov rcx, r14
11f0eee mov rdx, rsi
11f0ef1 call 0x14083d5a0
11f0ef6 mov rcx, qword ptr [rbp - 0x50]
11f0efa mov rax, qword ptr [rcx]
11f0efd mov rdx, rsi
11f0f00 call qword ptr [rax + 0x10]
11f0f03 jmp 0x1411f0b49
11f0f08 cmp esi, 0x544b7040
11f0f0e jg 0x1411f1285
11f0f14 cmp esi, 0x54495342
11f0f1a jg 0x1411f1558
11f0f20 cmp esi, 0x5443736e
11f0f26 je 0x1411f1bd5
11f0f2c cmp esi, 0x5444674d
11f0f32 je 0x1411f16ec
11f0f38 jmp 0x1411f2a95
11f0f3d lea eax, [rsi - 0x43595063]
11f0f43 cmp eax, 0xd
11f0f46 ja 0x1411f18b9
11f0f4c lea rcx, [rip + 0x2df5]
11f0f53 movsxd rax, dword ptr [rcx + rax*4]
11f0f57 add rax, rcx
11f0f5a jmp rax
11f0f5c mov rcx, rdi
11f0f5f mov dl, 0xa
11f0f61 mov r8d, 0x636f6d70
11f0f67 jmp 0x1411f2a60
11f0f6c cmp esi, 0x43575366
11f0f72 jle 0x1411f1366
11f0f78 cmp esi, 0x43575764
11f0f7e jg 0x1411f143b
11f0f84 cmp esi, 0x43575367
11f0f8a je 0x1411f1c35
11f0f90 cmp esi, 0x43575373
11f0f96 jne 0x1411f2a95
11f0f9c mov rcx, rdi
11f0f9f mov dl, 0x13
11f0fa1 mov r8d, 0x73746474
11f0fa7 jmp 0x1411f2a60
11f0fac lea eax, [rsi - 0x434c4161]
11f0fb2 cmp eax, 0xe
11f0fb5 ja 0x1411f13eb
11f0fbb lea rcx, [rip + 0x2cda]
11f0fc2 movsxd rax, dword ptr [rcx + rax*4]
11f0fc6 add rax, rcx
11f0fc9 jmp rax
11f0fcb mov rcx, rdi
11f0fce mov dl, 0x1a
11f0fd0 mov r8d, 0x61747465
11f0fd6 jmp 0x1411f2a60
11f0fdb lea eax, [rsi - 0x43464764]
11f0fe1 cmp eax, 0xf
11f0fe4 ja 0x1411f2a95
11f0fea lea rcx, [rip + 0x2bbb]
11f0ff1 movsxd rax, dword ptr [rcx + rax*4]
11f0ff5 add rax, rcx
11f0ff8 jmp rax
11f0ffa mov rcx, rdi
11f0ffd mov dl, 0x18
11f0fff mov r8d, 0x73746474
11f1005 jmp 0x1411f2a60
11f100a lea rcx, [rip + 0x2bdb]
11f1011 movsxd rax, dword ptr [rcx + rax*4]
11f1015 add rax, rcx
11f1018 jmp rax
11f101a mov rcx, rdi
11f101d mov dl, 0x17
11f101f mov r8d, 0x636f6d70
11f1025 jmp 0x1411f2a60
11f102a lea rcx, [rip + 0x2ca7]
11f1031 movsxd rax, dword ptr [rcx + rax*4]
11f1035 add rax, rcx
11f1038 jmp rax
11f103a mov rcx, rdi
11f103d mov dl, 0xb
11f103f mov r8d, 0x636f6d70
11f1045 jmp 0x1411f2a60
11f104a lea rcx, [rip + 0x2ae3]
11f1051 movsxd rax, dword ptr [rcx + rax*4]
11f1055 add rax, rcx
11f1058 jmp rax
11f105a mov rcx, rdi
11f105d mov dl, 9
11f105f mov r8d, 0x6f676c73
11f1065 jmp 0x1411f2a60
11f106a lea eax, [rsi - 0x43484161]
11f1070 cmp eax, 0xe
11f1073 ja 0x1411f2a95
11f1079 lea rcx, [rip + 0x2ba4]
11f1080 movsxd rax, dword ptr [rcx + rax*4]
11f1084 add rax, rcx
11f1087 jmp rax
11f1089 mov rcx, rdi
11f108c mov dl, 7
11f108e mov r8d, 0x61747465
11f1094 jmp 0x1411f2a60
11f1099 cmp esi, 0x54437272
11f109f jg 0x1411f15ab
11f10a5 cmp esi, 0x54436f69
11f10ab je 0x1411f1c45
11f10b1 cmp esi, 0x54437270
11f10b7 jne 0x1411f2a95
11f10bd mov rax, qword ptr [rdi + 0x18]
11f10c1 mov esi, 0x5dc
11f10c6 cmp rax, qword ptr [rdi + 0x20]
11f10ca je 0x1411f10db
11f10cc mov rax, qword ptr [rax]
11f10cf test rax, rax
11f10d2 je 0x1411f10db
11f10d4 movsx esi, word ptr [rax + 0xa8]
11f10db call 0x14083caf0
11f10e0 add rax, 0x28
11f10e4 mov dword ptr [rbp - 0x48], esi
11f10e7 mov qword ptr [rbp - 0x50], rax
11f10eb lea rsi, [rbp - 0x50]
11f10ef mov rcx, r14
11f10f2 mov rdx, rsi
11f10f5 call 0x14083d5a0
11f10fa mov rcx, qword ptr [rbp - 0x50]
11f10fe mov rax, qword ptr [rcx]
11f1101 mov rdx, rsi
11f1104 call qword ptr [rax + 0x10]
11f1107 jmp 0x1411f0b49
11f110c cmp esi, 0x4e417064
11f1112 jg 0x1411f1605
11f1118 cmp esi, 0x4e41666e
11f111e je 0x1411f1773
11f1124 cmp esi, 0x4e41676c
11f112a je 0x1411f1773
11f1130 jmp 0x1411f2a95
11f1135 cmp esi, 0x64626e6c
11f113b jg 0x1411f1622
11f1141 cmp esi, 0x54766370
11f1147 je 0x1411f1c79
11f114d cmp esi, 0x54767370
11f1153 jne 0x1411f2a95
11f1159 lea rbx, [rbp - 0x50]
11f115d mov rcx, rbx
11f1160 call 0x1407c8b10
11f1165 mov rax, qword ptr [rdi + 0x18]
11f1169 cmp rax, qword ptr [rdi + 0x20]
11f116d je 0x1411f1252
11f1173 mov rsi, qword ptr [rax]
11f1176 test rsi, rsi
11f1179 je 0x1411f1252
11f117f cmp byte ptr [rdi + 0xba], 0
11f1186 jne 0x1411f1252
11f118c mov rcx, rsi
11f118f call 0x1411a35a0
11f1194 test rax, rax
11f1197 je 0x1411f1252
11f119d mov ecx, 0xc18
11f11a2 add rcx, qword ptr [rax + 0x370]
11f11a9 mov qword ptr [rbp + 0xf10], rsi
11f11b0 mov qword ptr [rbp + 0xf18], rcx
11f11b7 mov qword ptr [rbp + 0xf20], rbx
11f11be lea rdi, [rbp + 0xf10]
11f11c5 mov rcx, rdi
11f11c8 mov dl, 7
11f11ca call 0x1411f4260
11f11cf mov rcx, rdi
11f11d2 mov dl, 6
11f11d4 call 0x1411f4260
11f11d9 mov rcx, rdi
11f11dc mov dl, 5
11f11de call 0x1411f4260
11f11e3 mov rcx, rdi
11f11e6 mov dl, 4
11f11e8 call 0x1411f4260
11f11ed cmp qword ptr [rsi + 0x30], 0
11f11f2 je 0x1411f1244
11f11f4 mov rax, qword ptr [rsi + 0x50]
11f11f8 test rax, rax
11f11fb je 0x1411f1244
11f11fd mov rsi, qword ptr [rax + 0xb0]
11f1204 test rsi, rsi
11f1207 je 0x1411f1236
11f1209 mov rcx, rsi
11f120c call 0x1409310c0
11f1211 test rax, rax
11f1214 jne 0x1411f1228
11f1216 mov rcx, rsi
11f1219 xor edx, edx
11f121b xor r8d, r8d
11f121e call 0x140944990
11f1223 test rax, rax
11f1226 je 0x1411f1236
11f1228 lea rcx, [rbp + 0xf10]
11f122f mov dl, 3
11f1231 call 0x1411f4260
11f1236 lea rcx, [rbp + 0xf10]
11f123d mov dl, 2
11f123f call 0x1411f4260
11f1244 lea rcx, [rbp + 0xf10]
11f124b mov dl, 1
11f124d call 0x1411f4260
11f1252 lea rsi, [rbp + 0xf10]
11f1259 lea rdx, [rbp - 0x50]
11f125d mov rcx, rsi
11f1260 call 0x14083d180
11f1265 mov rcx, r14
11f1268 mov rdx, rsi
11f126b call 0x14083d5a0
11f1270 mov rcx, qword ptr [rbp + 0xf10]
11f1277 mov rax, qword ptr [rcx]
11f127a mov rdx, rsi
11f127d call qword ptr [rax + 0x10]
11f1280 jmp 0x1411f191d
11f1285 cmp esi, 0x544c6566
11f128b jg 0x1411f1665
11f1291 cmp esi, 0x544b7041
11f1297 je 0x1411f1c9f
11f129d cmp esi, 0x544b704c
11f12a3 jne 0x1411f2a95
11f12a9 cmp byte ptr [rdi + 0xba], 0
11f12b0 jne 0x1411f2abd
11f12b6 mov rax, qword ptr [rdi]
11f12b9 mov rcx, rdi
11f12bc call qword ptr [rax + 0x38]
11f12bf cmp eax, 3
11f12c2 jne 0x1411f2abd
11f12c8 mov rcx, rdi
11f12cb mov dl, 8
11f12cd mov r8b, 1
11f12d0 mov r9b, 1
11f12d3 call 0x140e66bc0
11f12d8 mov r9, rax
11f12db jmp 0x1411f2ac0
11f12e0 cmp esi, 0x4e477064
11f12e6 jg 0x1411f175f
11f12ec cmp esi, 0x4e47666e
11f12f2 je 0x1411f1773
11f12f8 cmp esi, 0x4e47676c
11f12fe je 0x1411f1773
11f1304 jmp 0x1411f2a95
11f1309 cmp esi, 0x7041636b
11f130f jg 0x1411f1793
11f1315 cmp esi, 0x66696c74
11f131b je 0x1411f16ec
11f1321 cmp esi, 0x6c696e6b
11f1327 je 0x1411f170a
11f132d jmp 0x1411f2a95
11f1332 cmp esi, 0x43574365
11f1338 je 0x1411f1cd6
11f133e cmp esi, 0x43574367
11f1344 je 0x1411f1ce6
11f134a cmp esi, 0x43574373
11f1350 jne 0x1411f2a95
11f1356 mov rcx, rdi
11f1359 mov dl, 0x12
11f135b mov r8d, 0x73746474
11f1361 jmp 0x1411f2a60
11f1366 cmp esi, 0x43575267
11f136c je 0x1411f1cf6
11f1372 cmp esi, 0x43575273
11f1378 je 0x1411f1d06
11f137e cmp esi, 0x43575365
11f1384 jne 0x1411f2a95
11f138a mov rcx, rdi
11f138d mov dl, 0x13
11f138f mov r8d, 0x656e6474
11f1395 jmp 0x1411f2a60
11f139a cmp esi, 0x43616c74
11f13a0 je 0x1411f219c
11f13a6 cmp esi, 0x43617464
11f13ac je 0x1411f21bf
11f13b2 cmp esi, 0x43637469
11f13b8 jne 0x1411f2a95
11f13be mov rax, qword ptr [rdi]
11f13c1 mov rcx, rdi
11f13c4 call qword ptr [rax + 0x1a0]
11f13ca test rax, rax
11f13cd je 0x1411f2ccf
11f13d3 mov rax, qword ptr [rdi]
11f13d6 mov rcx, rdi
11f13d9 call qword ptr [rax + 0x1a0]
11f13df mov rcx, qword ptr [rax + 0xf0]
11f13e6 jmp 0x1411f2cd1
11f13eb cmp esi, 0x434c5265
11f13f1 je 0x1411f18a9
11f13f7 cmp esi, 0x434c5267
11f13fd jne 0x1411f2a95
11f1403 mov rcx, rdi
11f1406 mov dl, 0xd
11f1408 mov r8d, 0x67616d73
11f140e jmp 0x1411f2a60
11f1413 cmp esi, 0x43574c73
11f1419 je 0x1411f1d16
11f141f cmp esi, 0x43575265
11f1425 jne 0x1411f2a95
11f142b mov rcx, rdi
11f142e mov dl, 0xc
11f1430 mov r8d, 0x656e6474
11f1436 jmp 0x1411f2a60
11f143b cmp esi, 0x43575765
11f1441 je 0x1411f1d26
11f1447 cmp esi, 0x43575767
11f144d jne 0x1411f2a95
11f1453 mov rcx, rdi
11f1456 mov dl, 0xf
11f1458 mov r8d, 0x67616d73
11f145e jmp 0x1411f2a60
11f1463 cmp esi, 0x54436e6e
11f1469 je 0x1411f17b0
11f146f cmp esi, 0x54436e73
11f1475 jne 0x1411f2a95
11f147b mov rax, qword ptr [rdi]
11f147e mov rcx, rdi
11f1481 call qword ptr [rax + 0x170]
11f1487 mov rsi, rax
11f148a call 0x14083caf0
11f148f lea rcx, [rbp - 0x48]
11f1493 mov qword ptr [rbp - 0x48], 0
11f149b cmp rcx, rsi
11f149e je 0x1411f14b0
11f14a0 mov rcx, qword ptr [rsi]
11f14a3 test rcx, rcx
11f14a6 je 0x1411f14ac
11f14a8 lock inc dword ptr [rcx - 4]
11f14ac mov qword ptr [rbp - 0x48], rcx
11f14b0 add rax, 0x88
11f14b6 mov qword ptr [rbp - 0x50], rax
11f14ba lea rsi, [rbp - 0x50]
11f14be mov rcx, r14
11f14c1 mov rdx, rsi
11f14c4 call 0x14083d5a0
11f14c9 mov rcx, qword ptr [rbp - 0x50]
11f14cd mov rax, qword ptr [rcx]
11f14d0 mov rdx, rsi
11f14d3 call qword ptr [rax + 0x10]
11f14d6 jmp 0x1411f0b49
11f14db cmp esi, 0x436e6b6e
11f14e1 je 0x1411f17b0
11f14e7 cmp esi, 0x44454c45
11f14ed jne 0x1411f2a95
11f14f3 mov rsi, qword ptr [rdi + 0x18]
11f14f7 mov rdi, qword ptr [rdi + 0x20]
11f14fb call 0x14083caf0
11f1500 cmp rsi, rdi
11f1503 sete byte ptr [rbp - 0x48]
11f1507 add rax, 0x18
11f150b mov qword ptr [rbp - 0x50], rax
11f150f lea rsi, [rbp - 0x50]
11f1513 mov rcx, r14
11f1516 mov rdx, rsi
11f1519 call 0x14083d5a0
11f151e mov rcx, qword ptr [rbp - 0x50]
11f1522 mov rax, qword ptr [rcx]
11f1525 mov rdx, rsi
11f1528 call qword ptr [rax + 0x10]
11f152b jmp 0x1411f0b49
11f1530 cmp esi, 0x54635373
11f1536 je 0x1411f1d36
11f153c cmp esi, 0x54636170
11f1542 jne 0x1411f2a95
11f1548 mov rcx, rdi
11f154b xor edx, edx
11f154d mov r8d, 0x54636170
11f1553 jmp 0x1411f1c84
11f1558 cmp esi, 0x54495343
11f155e je 0x1411f1dec
11f1564 cmp esi, 0x5449534e
11f156a jne 0x1411f2a95
11f1570 mov bl, byte ptr [rdi + 0xba]
11f1576 call 0x14083caf0
11f157b add rax, 0x18
11f157f cmp bl, 1
11f1582 sete byte ptr [rbp - 0x48]
11f1586 mov qword ptr [rbp - 0x50], rax
11f158a lea rsi, [rbp - 0x50]
11f158e mov rcx, r14
11f1591 mov rdx, rsi
11f1594 call 0x14083d5a0
11f1599 mov rcx, qword ptr [rbp - 0x50]
11f159d mov rax, qword ptr [rcx]
11f15a0 mov rdx, rsi
11f15a3 call qword ptr [rax + 0x10]
11f15a6 jmp 0x1411f0b49
11f15ab cmp esi, 0x54437273
11f15b1 je 0x1411f1e26
11f15b7 cmp esi, 0x54437367
11f15bd jne 0x1411f2a95
11f15c3 mov rax, qword ptr [rdi]
11f15c6 mov rcx, rdi
11f15c9 call qword ptr [rax + 0x188]
11f15cf mov bl, al
11f15d1 call 0x14083caf0
11f15d6 add rax, 0x28
11f15da movsx ecx, bl
11f15dd mov dword ptr [rbp - 0x48], ecx
11f15e0 mov qword ptr [rbp - 0x50], rax
11f15e4 lea rsi, [rbp - 0x50]
11f15e8 mov rcx, r14
11f15eb mov rdx, rsi
11f15ee call 0x14083d5a0
11f15f3 mov rcx, qword ptr [rbp - 0x50]
11f15f7 mov rax, qword ptr [rcx]
11f15fa mov rdx, rsi
11f15fd call qword ptr [rax + 0x10]
11f1600 jmp 0x1411f0b49
11f1605 cmp esi, 0x4e417065
11f160b je 0x1411f1773
11f1611 cmp esi, 0x4e41736e
11f1617 je 0x1411f1773
11f161d jmp 0x1411f2a95
11f1622 cmp esi, 0x64626e6d
11f1628 je 0x1411f1e65
11f162e cmp esi, 0x64647072
11f1634 jne 0x1411f2a95
11f163a mov rax, qword ptr [rdi + 0x18]
11f163e cmp rax, qword ptr [rdi + 0x20]
11f1642 je 0x1411f170a
11f1648 mov rcx, qword ptr [rax]
11f164b test rcx, rcx
11f164e je 0x1411f170a
11f1654 mov rax, qword ptr [rcx]
11f1657 mov rax, qword ptr [rax + 0x10]
11f165b mov edx, 0x64647072
11f1660 jmp 0x1411f2aa4
11f1665 cmp esi, 0x544c6567
11f166b je 0x1411f1f3b
11f1671 cmp esi, 0x544d6e52
11f1677 je 0x1411f16ec
11f1679 jmp 0x1411f2a95
11f167e cmp esi, 0x54436170
11f1684 je 0x1411f16ec
11f1686 cmp esi, 0x5443686e
11f168c jne 0x1411f2a95
11f1692 mov rax, qword ptr [rdi + 0xb0]
11f1699 mov rax, qword ptr [rax + 0x90]
11f16a0 mov bl, 1
11f16a2 test rax, rax
11f16a5 je 0x1411f16bb
11f16a7 cmp dword ptr [rax], 0
11f16aa je 0x1411f16bb
11f16ac mov rcx, rdi
11f16af mov dl, 1
11f16b1 call 0x1411d6840
11f16b6 mov ebx, eax
11f16b8 xor bl, 1
11f16bb call 0x14083caf0
11f16c0 add rax, 0x18
11f16c4 mov byte ptr [rbp - 0x48], bl
11f16c7 mov qword ptr [rbp - 0x50], rax
11f16cb lea rsi, [rbp - 0x50]
11f16cf mov rcx, r14
11f16d2 mov rdx, rsi
11f16d5 call 0x14083d5a0
11f16da mov rcx, qword ptr [rbp - 0x50]
11f16de mov rax, qword ptr [rcx]
11f16e1 mov rdx, rsi
11f16e4 call qword ptr [rax + 0x10]
11f16e7 jmp 0x1411f0b49
11f16ec mov rax, qword ptr [rdi + 0x18]
11f16f0 cmp rax, qword ptr [rdi + 0x20]
11f16f4 je 0x1411f170a
11f16f6 mov rcx, qword ptr [rax]
11f16f9 test rcx, rcx
11f16fc je 0x1411f170a
11f16fe mov rax, qword ptr [rcx]
11f1701 mov rax, qword ptr [rax + 0x10]
11f1705 jmp 0x1411f2aa2
11f170a xor ebx, ebx
11f170c jmp 0x1411f0b4b
11f1711 cmp esi, 0x73756274
11f1717 je 0x1411f21fa
11f171d cmp esi, 0x7462636c
11f1723 jne 0x1411f2a95
11f1729 lea rdx, [rbp - 0x48]
11f172d mov rcx, rdi
11f1730 call 0x1411ddb60
11f1735 call 0x141335560
11f173a mov qword ptr [rbp - 0x50], rax
11f173e lea rsi, [rbp - 0x50]
11f1742 mov rcx, r14
11f1745 mov rdx, rsi
11f1748 call 0x14083d5a0
11f174d mov rcx, qword ptr [rbp - 0x50]
11f1751 mov rax, qword ptr [rcx]
11f1754 mov rdx, rsi
11f1757 call qword ptr [rax + 0x10]
11f175a jmp 0x1411f0b49
11f175f cmp esi, 0x4e477065
11f1765 je 0x1411f1773
11f1767 cmp esi, 0x4e47736e
11f176d jne 0x1411f2a95
11f1773 mov rcx, rdi
11f1776 mov edx, esi
11f1778 mov r8, r14
11f177b add rsp, 0x1878
11f1782 pop rbx
11f1783 pop rdi
11f1784 pop rsi
11f1785 pop r12
11f1787 pop r13
11f1789 pop r14
11f178b pop r15
11f178d pop rbp
11f178e jmp 0x1411e9c20
11f1793 cmp esi, 0x7041636c
11f1799 je 0x1411f18e1
11f179f cmp esi, 0x7054636c
11f17a5 je 0x1411f18e1
11f17ab jmp 0x1411f2a95
11f17b0 mov rax, qword ptr [rdi + 0xb0]
11f17b7 mov rax, qword ptr [rax + 0x90]
11f17be test rax, rax
11f17c1 je 0x1411f1833
11f17c3 cmp dword ptr [rax], 0
11f17c6 je 0x1411f1833
11f17c8 mov rcx, rdi
11f17cb mov dl, 1
11f17cd call 0x1411d6840
11f17d2 test al, al
11f17d4 je 0x1411f1833
11f17d6 mov esi, 0x90
11f17db add rsi, qword ptr [rdi + 0xb0]
11f17e2 call 0x14083caf0
11f17e7 lea rcx, [rbp - 0x48]
11f17eb mov qword ptr [rbp - 0x48], 0
11f17f3 cmp rcx, rsi
11f17f6 je 0x1411f1808
11f17f8 mov rcx, qword ptr [rsi]
11f17fb test rcx, rcx
11f17fe je 0x1411f1804
11f1800 lock inc dword ptr [rcx - 4]
11f1804 mov qword ptr [rbp - 0x48], rcx
11f1808 add rax, 0x88
11f180e mov qword ptr [rbp - 0x50], rax
11f1812 lea rsi, [rbp - 0x50]
11f1816 mov rcx, r14
11f1819 mov rdx, rsi
11f181c call 0x14083d5a0
11f1821 mov rcx, qword ptr [rbp - 0x50]
11f1825 mov rax, qword ptr [rcx]
11f1828 mov rdx, rsi
11f182b call qword ptr [rax + 0x10]
11f182e jmp 0x1411f0b49
11f1833 call 0x14083caf0
11f1838 mov qword ptr [rbp - 0x48], 0
11f1840 mov rcx, qword ptr [rip + 0x967ca1]
11f1847 test rcx, rcx
11f184a je 0x1411f1850
11f184c lock inc dword ptr [rcx - 4]
11f1850 mov qword ptr [rbp - 0x48], rcx
11f1854 add rax, 0x88
11f185a mov qword ptr [rbp - 0x50], rax
11f185e lea rsi, [rbp - 0x50]
11f1862 mov rcx, r14
11f1865 mov rdx, rsi
11f1868 call 0x14083d5a0
11f186d mov rcx, qword ptr [rbp - 0x50]
11f1871 mov rax, qword ptr [rcx]
11f1874 mov rdx, rsi
11f1877 call qword ptr [rax + 0x10]
11f187a jmp 0x1411f0b49
11f187f mov rcx, rdi
11f1882 mov dl, 0x1a
11f1884 mov r8d, 0x636f6d70
11f188a jmp 0x1411f2a60
11f188f mov rcx, rdi
11f1892 mov dl, 0x1a
11f1894 mov r8d, 0x73746474
11f189a jmp 0x1411f2a60
11f189f mov rcx, rdi
11f18a2 mov dl, 0x1a
11f18a4 jmp 0x1411f2a5a
11f18a9 mov rcx, rdi
11f18ac mov dl, 0xd
11f18ae mov r8d, 0x656e6474
11f18b4 jmp 0x1411f2a60
11f18b9 cmp esi, 0x43575773
11f18bf jne 0x1411f2a95
11f18c5 mov rcx, rdi
11f18c8 mov dl, 0xf
11f18ca mov r8d, 0x73746474
11f18d0 jmp 0x1411f2a60
11f18d5 cmp esi, 0x4163636c
11f18db jne 0x1411f2a95
11f18e1 lea rsi, [rbp - 0x50]
11f18e5 mov rcx, rdi
11f18e8 mov rdx, rsi
11f18eb call 0x1411dd660
11f18f0 lea rdi, [rbp + 0xf10]
11f18f7 mov rcx, rdi
11f18fa mov rdx, rsi
11f18fd call 0x14083d180
11f1902 mov rcx, r14
11f1905 mov rdx, rdi
11f1908 call 0x14083d5a0
11f190d mov rcx, qword ptr [rbp + 0xf10]
11f1914 mov rax, qword ptr [rcx]
11f1917 mov rdx, rdi
11f191a call qword ptr [rax + 0x10]
11f191d lea rcx, [rbp - 0x50]
11f1921 call 0x14083a6a0
11f1926 jmp 0x1411f0b49
11f192b mov rcx, rdi
11f192e mov dl, 0x17
11f1930 mov r8d, 0x73746474
11f1936 jmp 0x1411f2a60
11f193b mov rcx, rdi
11f193e mov dl, 0x17
11f1940 mov r8d, 0x676f6c73
11f1946 jmp 0x1411f2a60
11f194b mov rcx, rdi
11f194e mov dl, 0x17
11f1950 mov r8d, 0x73746e6d
11f1956 jmp 0x1411f2a60
11f195b mov rcx, rdi
11f195e mov dl, 0x17
11f1960 jmp 0x1411f2a5a
11f1965 mov rcx, rdi
11f1968 mov dl, 0x17
11f196a mov r8d, 0x73746964
11f1970 jmp 0x1411f2a60
11f1975 mov rcx, rdi
11f1978 mov dl, 9
11f197a mov r8d, 0x636f6d70
11f1980 jmp 0x1411f2a60
11f1985 mov rcx, rdi
11f1988 mov dl, 9
11f198a mov r8d, 0x73746474
11f1990 jmp 0x1411f2a60
11f1995 mov rcx, rdi
11f1998 mov dl, 9
11f199a mov r8d, 0x676f6c73
11f19a0 jmp 0x1411f2a60
11f19a5 mov rcx, rdi
11f19a8 mov dl, 9
11f19aa jmp 0x1411f2a5a
11f19af mov rcx, rdi
11f19b2 mov dl, 0x19
11f19b4 mov r8d, 0x73746474
11f19ba jmp 0x1411f2a60
11f19bf mov rcx, rdi
11f19c2 mov dl, 0x19
11f19c4 mov r8d, 0x636f6d70
11f19ca jmp 0x1411f2a60
11f19cf mov rcx, rdi
11f19d2 mov dl, 0x19
11f19d4 mov r8d, 0x676f6c73
11f19da jmp 0x1411f2a60
11f19df mov rcx, rdi
11f19e2 mov dl, 0x19
11f19e4 jmp 0x1411f2a5a
11f19e9 mov rcx, rdi
11f19ec mov dl, 0xa
11f19ee mov r8d, 0x73746462
11f19f4 jmp 0x1411f2a60
11f19f9 mov rcx, rdi
11f19fc mov dl, 0xa
11f19fe mov r8d, 0x73746e6d
11f1a04 jmp 0x1411f2a60
11f1a09 mov rcx, rdi
11f1a0c mov dl, 0xa
11f1a0e jmp 0x1411f2a5a
11f1a13 mov rcx, rdi
11f1a16 mov dl, 0xa
11f1a18 mov r8d, 0x73746964
11f1a1e jmp 0x1411f2a60
11f1a23 mov rcx, rdi
11f1a26 mov dl, 0x18
11f1a28 mov r8d, 0x636f6d70
11f1a2e jmp 0x1411f2a60
11f1a33 mov rcx, rdi
11f1a36 mov dl, 0x18
11f1a38 jmp 0x1411f2a5a
11f1a3d mov rcx, rdi
11f1a40 mov dl, 0x18
11f1a42 mov r8d, 0x73746964
11f1a48 jmp 0x1411f2a60
11f1a4d mov rcx, rdi
11f1a50 mov dl, 0x18
11f1a52 mov r8d, 0x66736774
11f1a58 jmp 0x1411f2a60
11f1a5d mov rcx, rdi
11f1a60 mov dl, 0xa
11f1a62 mov r8d, 0x73746474
11f1a68 jmp 0x1411f2a60
11f1a6d mov rcx, rdi
11f1a70 mov dl, 0x18
11f1a72 mov r8d, 0x73746e6d
11f1a78 jmp 0x1411f2a60
11f1a7d mov rcx, rdi
11f1a80 mov dl, 0x1b
11f1a82 mov r8d, 0x73746462
11f1a88 jmp 0x1411f2a60
11f1a8d mov rcx, rdi
11f1a90 mov dl, 0x1b
11f1a92 mov r8d, 0x73746474
11f1a98 jmp 0x1411f2a60
11f1a9d mov rcx, rdi
11f1aa0 mov dl, 0x1b
11f1aa2 mov r8d, 0x73746e6d
11f1aa8 jmp 0x1411f2a60
11f1aad mov rcx, rdi
11f1ab0 mov dl, 0x1b
11f1ab2 jmp 0x1411f2a5a
11f1ab7 mov rcx, rdi
11f1aba mov dl, 0x1b
11f1abc mov r8d, 0x73746964
11f1ac2 jmp 0x1411f2a60
11f1ac7 mov rcx, rdi
11f1aca mov dl, 8
11f1acc mov r8d, 0x676f6c73
11f1ad2 jmp 0x1411f2a60
11f1ad7 mov rcx, rdi
11f1ada mov dl, 8
11f1adc mov r8d, 0x636f6d70
11f1ae2 jmp 0x1411f2a60
11f1ae7 mov rcx, rdi
11f1aea mov dl, 8
11f1aec mov r8d, 0x73746474
11f1af2 jmp 0x1411f2a60
11f1af7 mov rcx, rdi
11f1afa mov dl, 8
11f1afc jmp 0x1411f2a5a
11f1b01 mov rax, qword ptr [rdi + 0x18]
11f1b05 cmp rax, qword ptr [rdi + 0x20]
11f1b09 je 0x1411f2c9f
11f1b0f mov rax, qword ptr [rax]
11f1b12 test rax, rax
11f1b15 je 0x1411f2c9f
11f1b1b mov rax, qword ptr [rax + 0x80]
11f1b22 test rax, rax
11f1b25 je 0x1411f2c9f
11f1b2b mov rcx, qword ptr [rax + 8]
11f1b2f movsxd rdx, dword ptr [rcx + 4]
11f1b33 lea rcx, [rax + rdx + 8]
11f1b38 mov rax, qword ptr [rax + rdx + 8]
11f1b3d lea rsi, [rbp - 0x50]
11f1b41 mov rdx, rsi
11f1b44 call qword ptr [rax + 0x90]
11f1b4a lea rdi, [rbp + 0xf10]
11f1b51 mov rcx, rsi
11f1b54 mov rdx, rdi
11f1b57 call 0x140fea300
11f1b5c mov rcx, r14
11f1b5f mov rdx, rdi
11f1b62 call 0x14083d5a0
11f1b67 mov rcx, qword ptr [rbp + 0xf10]
11f1b6e mov rax, qword ptr [rcx]
11f1b71 mov rdx, rdi
11f1b74 call qword ptr [rax + 0x10]
11f1b77 lea rdx, [rbp - 0x48]
11f1b7b mov rcx, qword ptr [rbp - 0x48]
11f1b7f mov rax, qword ptr [rcx]
11f1b82 call qword ptr [rax + 0x10]
11f1b85 jmp 0x1411f0b49
11f1b8a mov rcx, rdi
11f1b8d mov dl, 0xe
11f1b8f mov r8d, 0x656e6474
11f1b95 jmp 0x1411f2a60
11f1b9a mov rax, qword ptr [rdi + 0xb0]
11f1ba1 mov esi, dword ptr [rax + 0x6c]
11f1ba4 call 0x14083caf0
11f1ba9 add rax, 0x28
11f1bad mov dword ptr [rbp - 0x48], esi
11f1bb0 mov qword ptr [rbp - 0x50], rax
11f1bb4 lea rsi, [rbp - 0x50]
11f1bb8 mov rcx, r14
11f1bbb mov rdx, rsi
11f1bbe call 0x14083d5a0
11f1bc3 mov rcx, qword ptr [rbp - 0x50]
11f1bc7 mov rax, qword ptr [rcx]
11f1bca mov rdx, rsi
11f1bcd call qword ptr [rax + 0x10]
11f1bd0 jmp 0x1411f0b49
11f1bd5 mov rax, qword ptr [rdi]
11f1bd8 mov rcx, rdi
11f1bdb call qword ptr [rax + 0x178]
11f1be1 mov rsi, rax
11f1be4 call 0x14083caf0
11f1be9 lea rcx, [rbp - 0x48]
11f1bed mov qword ptr [rbp - 0x48], 0
11f1bf5 cmp rcx, rsi
11f1bf8 je 0x1411f1c0a
11f1bfa mov rcx, qword ptr [rsi]
11f1bfd test rcx, rcx
11f1c00 je 0x1411f1c06
11f1c02 lock inc dword ptr [rcx - 4]
11f1c06 mov qword ptr [rbp - 0x48], rcx
11f1c0a add rax, 0x88
11f1c10 mov qword ptr [rbp - 0x50], rax
11f1c14 lea rsi, [rbp - 0x50]
11f1c18 mov rcx, r14
11f1c1b mov rdx, rsi
11f1c1e call 0x14083d5a0
11f1c23 mov rcx, qword ptr [rbp - 0x50]
11f1c27 mov rax, qword ptr [rcx]
11f1c2a mov rdx, rsi
11f1c2d call qword ptr [rax + 0x10]
11f1c30 jmp 0x1411f0b49
11f1c35 mov rcx, rdi
11f1c38 mov dl, 0x13
11f1c3a mov r8d, 0x67616d73
11f1c40 jmp 0x1411f2a60
11f1c45 mov esi, dword ptr [rdi + 0xc]
11f1c48 call 0x14083caf0
11f1c4d add rax, 0x28
11f1c51 mov dword ptr [rbp - 0x48], esi
11f1c54 mov qword ptr [rbp - 0x50], rax
11f1c58 lea rsi, [rbp - 0x50]
11f1c5c mov rcx, r14
11f1c5f mov rdx, rsi
11f1c62 call 0x14083d5a0
11f1c67 mov rcx, qword ptr [rbp - 0x50]
11f1c6b mov rax, qword ptr [rcx]
11f1c6e mov rdx, rsi
11f1c71 call qword ptr [rax + 0x10]
11f1c74 jmp 0x1411f0b49
11f1c79 mov rcx, rdi
11f1c7c xor edx, edx
11f1c7e mov r8d, 0x54766370
11f1c84 mov r9, r14
11f1c87 add rsp, 0x1878
11f1c8e pop rbx
11f1c8f pop rdi
11f1c90 pop rsi
11f1c91 pop r12
11f1c93 pop r13
11f1c95 pop r14
11f1c97 pop r15
11f1c99 pop rbp
11f1c9a jmp 0x1411f41d0
11f1c9f cmp byte ptr [rdi + 0xba], 0
11f1ca6 jne 0x1411f2bae
11f1cac mov rax, qword ptr [rdi]
11f1caf mov rcx, rdi
11f1cb2 call qword ptr [rax + 0x38]
11f1cb5 cmp eax, 3
11f1cb8 jne 0x1411f2bae
11f1cbe mov rcx, rdi
11f1cc1 mov dl, 8
11f1cc3 mov r8b, 1
11f1cc6 mov r9b, 1
11f1cc9 call 0x140e66bc0
11f1cce mov r9, rax
11f1cd1 jmp 0x1411f2bb1
11f1cd6 mov rcx, rdi
11f1cd9 mov dl, 0x12
11f1cdb mov r8d, 0x656e6474
11f1ce1 jmp 0x1411f2a60
11f1ce6 mov rcx, rdi
11f1ce9 mov dl, 0x12
11f1ceb mov r8d, 0x67616d73
11f1cf1 jmp 0x1411f2a60
11f1cf6 mov rcx, rdi
11f1cf9 mov dl, 0xc
11f1cfb mov r8d, 0x67616d73
11f1d01 jmp 0x1411f2a60
11f1d06 mov rcx, rdi
11f1d09 mov dl, 0xc
11f1d0b mov r8d, 0x73746474
11f1d11 jmp 0x1411f2a60
11f1d16 mov rcx, rdi
11f1d19 mov dl, 0xe
11f1d1b mov r8d, 0x73746474
11f1d21 jmp 0x1411f2a60
11f1d26 mov rcx, rdi
11f1d29 mov dl, 0xf
11f1d2b mov r8d, 0x656e6474
11f1d31 jmp 0x1411f2a60
11f1d36 lea rcx, [rbp + 0x17d8]
11f1d3d call 0x1407c8b10
11f1d42 xor esi, esi
11f1d44 lea rcx, [rbp + rsi + 0xf10]
11f1d4c call 0x1407c8b10
11f1d51 add rsi, 0x18
11f1d55 cmp rsi, 0x888
11f1d5c jne 0x1411f1d44
11f1d5e xor esi, esi
11f1d60 lea rcx, [rbp + rsi - 0x50]
11f1d65 call 0x1407c8b10
11f1d6a add rsi, 0x18
11f1d6e cmp rsi, 0xf60
11f1d75 jne 0x1411f1d60
11f1d77 mov rax, qword ptr [rdi + 0x20]
11f1d7b sub rax, qword ptr [rdi + 0x18]
11f1d7f je 0x1411f1f6b
11f1d85 sar rax, 3
11f1d89 cmp rax, 2
11f1d8d mov r13d, 1
11f1d93 cmovae r13, rax
11f1d97 xor ebx, ebx
11f1d99 lea r15, [rbp + 0xf10]
11f1da0 lea r12, [rbp - 0x50]
11f1da4 jmp 0x1411f1dc0
11f1da6 mov rcx, rsi
11f1da9 mov rdx, r15
11f1dac mov r8, r12
11f1daf call 0x1411bc380
11f1db4 inc rbx
11f1db7 cmp r13, rbx
11f1dba je 0x1411f1f6b
11f1dc0 mov rax, qword ptr [rdi + 0x18]
11f1dc4 mov rsi, qword ptr [rax + rbx*8]
11f1dc8 test rsi, rsi
11f1dcb je 0x1411f1db4
11f1dcd cmp byte ptr [rdi + 0xba], 1
11f1dd4 jne 0x1411f1da6
11f1dd6 call 0x140fe7830
11f1ddb test rax, rax
11f1dde je 0x1411f1da6
11f1de0 call 0x140fe7830
11f1de5 cmp rsi, rax
11f1de8 jne 0x1411f1db4
11f1dea jmp 0x1411f1da6
11f1dec mov bl, byte ptr [rdi + 0xba]
11f1df2 call 0x14083caf0
11f1df7 test bl, bl
11f1df9 sete byte ptr [rbp - 0x48]
11f1dfd add rax, 0x18
11f1e01 mov qword ptr [rbp - 0x50], rax
11f1e05 lea rsi, [rbp - 0x50]
11f1e09 mov rcx, r14
11f1e0c mov rdx, rsi
11f1e0f call 0x14083d5a0
11f1e14 mov rcx, qword ptr [rbp - 0x50]
11f1e18 mov rax, qword ptr [rcx]
11f1e1b mov rdx, rsi
11f1e1e call qword ptr [rax + 0x10]
11f1e21 jmp 0x1411f0b49
11f1e26 lea rsi, [rbp - 0x50]
11f1e2a mov rcx, rsi
11f1e2d mov rdx, rdi
11f1e30 call 0x1415634b0
11f1e35 mov rcx, rsi
11f1e38 mov rdx, r14
11f1e3b call 0x1411f3dc0
11f1e40 mov rdx, qword ptr [rbp - 0x50]
11f1e44 test rdx, rdx
11f1e47 je 0x1411f0b49
11f1e4d mov r8, qword ptr [rbp - 0x40]
11f1e51 sub r8, rdx
11f1e54 mov rcx, qword ptr [rip + 0x8cac15]
11f1e5b call 0x1407e3e90
11f1e60 jmp 0x1411f0b49
11f1e65 mov rax, qword ptr [rdi]
11f1e68 mov rcx, rdi
11f1e6b call qword ptr [rax + 0x170]
11f1e71 mov rsi, rax
11f1e74 call 0x14083caf0
11f1e79 lea r15, [rbp - 0x48]
11f1e7d mov qword ptr [rbp - 0x48], 0
11f1e85 cmp r15, rsi
11f1e88 je 0x1411f1e9a
11f1e8a mov rcx, qword ptr [rsi]
11f1e8d test rcx, rcx
11f1e90 je 0x1411f1e96
11f1e92 lock inc dword ptr [rcx - 4]
11f1e96 mov qword ptr [rbp - 0x48], rcx
11f1e9a add rax, 0x88
11f1ea0 mov qword ptr [rbp - 0x50], rax
11f1ea4 lea rsi, [rbp - 0x50]
11f1ea8 mov rcx, r14
11f1eab mov rdx, rsi
11f1eae call 0x14083d5a0
11f1eb3 mov rcx, qword ptr [rbp - 0x50]
11f1eb7 mov rax, qword ptr [rcx]
11f1eba mov rdx, rsi
11f1ebd call qword ptr [rax + 0x10]
11f1ec0 mov rax, qword ptr [rdi]
11f1ec3 mov rcx, rdi
11f1ec6 call qword ptr [rax + 0x170]
11f1ecc mov rax, qword ptr [rax]
11f1ecf test rax, rax
11f1ed2 je 0x1411f1edf
11f1ed4 mov bl, 1
11f1ed6 cmp dword ptr [rax], 0
11f1ed9 jne 0x1411f0b4b
11f1edf mov rax, qword ptr [rdi]
11f1ee2 mov rcx, rdi
11f1ee5 call qword ptr [rax + 0x178]
11f1eeb mov rsi, rax
11f1eee call 0x14083caf0
11f1ef3 mov qword ptr [rbp - 0x48], 0
11f1efb cmp r15, rsi
11f1efe je 0x1411f1f10
11f1f00 mov rcx, qword ptr [rsi]
11f1f03 test rcx, rcx
11f1f06 je 0x1411f1f0c
11f1f08 lock inc dword ptr [rcx - 4]
11f1f0c mov qword ptr [rbp - 0x48], rcx
11f1f10 add rax, 0x88
11f1f16 mov qword ptr [rbp - 0x50], rax
11f1f1a lea rsi, [rbp - 0x50]
11f1f1e mov rcx, r14
11f1f21 mov rdx, rsi
11f1f24 call 0x14083d5a0
11f1f29 mov rcx, qword ptr [rbp - 0x50]
11f1f2d mov rax, qword ptr [rcx]
11f1f30 mov rdx, rsi
11f1f33 call qword ptr [rax + 0x10]
11f1f36 jmp 0x1411f0b49
11f1f3b movzx eax, byte ptr [rdi + 0xba]
11f1f42 mov bl, 1
11f1f44 test eax, eax
11f1f46 je 0x1411f2cde
11f1f4c cmp eax, 1
11f1f4f jne 0x1411f0b4b
11f1f55 mov rax, qword ptr [rdi]
11f1f58 mov rcx, rdi
11f1f5b mov edx, 0x4e776370
11f1f60 mov r8, r14
11f1f63 call qword ptr [rax + 0x10]
11f1f66 jmp 0x1411f0b4b
11f1f6b lea r15, [rbp + 0x17c0]
11f1f72 mov rcx, r15
11f1f75 call 0x1407c8b10
11f1f7a lea rdi, [rbp + 0xf10]
11f1f81 xor ebx, ebx
11f1f83 lea rsi, [rbp + 0x1798]
11f1f8a jmp 0x1411f1f9d
11f1f8c inc rbx
11f1f8f add rdi, 0x18
11f1f93 cmp rbx, 0x5b
11f1f97 je 0x1411f2434
11f1f9d mov rax, qword ptr [rdi]
11f1fa0 cmp rax, qword ptr [rdi + 8]
11f1fa4 je 0x1411f1f8c
11f1fa6 mov rcx, rsi
11f1fa9 mov rdx, rdi
11f1fac call 0x14083d180
11f1fb1 mov rcx, r15
11f1fb4 mov edx, ebx
11f1fb6 mov r8, rsi
11f1fb9 call 0x140834980
11f1fbe mov rcx, qword ptr [rbp + 0x1798]
11f1fc5 mov rax, qword ptr [rcx]
11f1fc8 mov rdx, rsi
11f1fcb call qword ptr [rax + 0x10]
11f1fce jmp 0x1411f1f8c
11f1fd0 mov esi, 0x98
11f1fd5 add rsi, qword ptr [rdi + 0xb0]
11f1fdc call 0x14083caf0
11f1fe1 lea rcx, [rbp - 0x48]
11f1fe5 mov qword ptr [rbp - 0x48], 0
11f1fed cmp rcx, rsi
11f1ff0 je 0x1411f2002
11f1ff2 mov rcx, qword ptr [rsi]
11f1ff5 test rcx, rcx
11f1ff8 je 0x1411f1ffe
11f1ffa lock inc dword ptr [rcx - 4]
11f1ffe mov qword ptr [rbp - 0x48], rcx
11f2002 add rax, 0x88
11f2008 mov qword ptr [rbp - 0x50], rax
11f200c lea rsi, [rbp - 0x50]
11f2010 mov rcx, r14
11f2013 mov rdx, rsi
11f2016 call 0x14083d5a0
11f201b mov rcx, qword ptr [rbp - 0x50]
11f201f mov rax, qword ptr [rcx]
11f2022 mov rdx, rsi
11f2025 call qword ptr [rax + 0x10]
11f2028 jmp 0x1411f0b49
11f202d mov rax, qword ptr [rdi]
11f2030 mov rcx, rdi
11f2033 call qword ptr [rax + 0x180]
11f2039 mov bl, al
11f203b call 0x14083caf0
11f2040 add rax, 0x28
11f2044 movsx ecx, bl
11f2047 mov dword ptr [rbp - 0x48], ecx
11f204a mov qword ptr [rbp - 0x50], rax
11f204e lea rsi, [rbp - 0x50]
11f2052 mov rcx, r14
11f2055 mov rdx, rsi
11f2058 call 0x14083d5a0
11f205d mov rcx, qword ptr [rbp - 0x50]
11f2061 mov rax, qword ptr [rcx]
11f2064 mov rdx, rsi
11f2067 call qword ptr [rax + 0x10]
11f206a jmp 0x1411f0b49
11f206f call 0x14083caf0
11f2074 add rax, 0x28
11f2078 mov dword ptr [rbp - 0x48], 0
11f207f mov qword ptr [rbp - 0x50], rax
11f2083 lea rsi, [rbp - 0x50]
11f2087 mov rcx, r14
11f208a mov rdx, rsi
11f208d call 0x14083d5a0
11f2092 mov rcx, qword ptr [rbp - 0x50]
11f2096 mov rax, qword ptr [rcx]
11f2099 mov rdx, rsi
11f209c call qword ptr [rax + 0x10]
11f209f mov bl, 1
11f20a1 cmp byte ptr [rdi + 0xba], 0
11f20a8 jne 0x1411f0b4b
11f20ae mov rax, qword ptr [rdi + 0x118]
11f20b5 mov rcx, qword ptr [rdi + 0x120]
11f20bc cmp rax, rcx
11f20bf je 0x1411f0b4b
11f20c5 mov r8d, 0x1001f0
11f20cb jmp 0x1411f20da
11f20cd add rax, 8
11f20d1 cmp rax, rcx
11f20d4 je 0x1411f0b4b
11f20da mov rsi, qword ptr [rax]
11f20dd cmp qword ptr [rsi + 8], rdi
11f20e1 jne 0x1411f20cd
11f20e3 movzx edx, byte ptr [rsi + 0x30]
11f20e7 cmp edx, 0x14
11f20ea ja 0x1411f20cd
11f20ec bt r8d, edx
11f20f0 jae 0x1411f20cd
11f20f2 mov rcx, qword ptr [rsi]
11f20f5 test rcx, rcx
11f20f8 je 0x1411f0b4b
11f20fe call 0x140e68240
11f2103 cmp rax, rdi
11f2106 je 0x1411f2f29
11f210c call 0x14083caf0
11f2111 add rax, 0x28
11f2115 mov dword ptr [rbp - 0x48], 0xd
11f211c mov qword ptr [rbp - 0x50], rax
11f2120 lea rsi, [rbp - 0x50]
11f2124 mov rcx, r14
11f2127 mov rdx, rsi
11f212a call 0x14083d5a0
11f212f mov rcx, qword ptr [rbp - 0x50]
11f2133 mov rax, qword ptr [rcx]
11f2136 mov rdx, rsi
11f2139 call qword ptr [rax + 0x10]
11f213c jmp 0x1411f0b4b
11f2141 lea rdx, [rbp - 0x50]
11f2145 mov rcx, rdi
11f2148 call 0x1411ddb60
11f214d movzx eax, byte ptr [rbp - 0x4e]
11f2151 movzx ecx, byte ptr [rbp - 0x4f]
11f2155 add ecx, eax
11f2157 movzx eax, byte ptr [rbp - 0x50]
11f215b add eax, ecx
11f215d cmp eax, 0x180
11f2162 mov eax, 0xffffffff
11f2167 mov esi, 0xff000000
11f216c cmovb esi, eax
11f216f call 0x141335560
11f2174 mov dword ptr [rbp - 0x48], esi
11f2177 mov qword ptr [rbp - 0x50], rax
11f217b lea rsi, [rbp - 0x50]
11f217f mov rcx, r14
11f2182 mov rdx, rsi
11f2185 call 0x14083d5a0
11f218a mov rcx, qword ptr [rbp - 0x50]
11f218e mov rax, qword ptr [rcx]
11f2191 mov rdx, rsi
11f2194 call qword ptr [rax + 0x10]
11f2197 jmp 0x1411f0b49
11f219c mov qword ptr [rbp - 0x50], rdi
11f21a0 lea rax, [rbp - 0x50]
11f21a4 mov qword ptr [rbp + 0xf10], rax
11f21ab lea rcx, [rbp + 0xf10]
11f21b2 mov rdx, r14
11f21b5 call 0x1411ff710
11f21ba jmp 0x1411f0b49
11f21bf mov rax, qword ptr [rdi + 0xb0]
11f21c6 mov esi, dword ptr [rax + 0x68]
11f21c9 call 0x14083caf0
11f21ce add rax, 0x28
11f21d2 mov dword ptr [rbp - 0x48], esi
11f21d5 mov qword ptr [rbp - 0x50], rax
11f21d9 lea rsi, [rbp - 0x50]
11f21dd mov rcx, r14
11f21e0 mov rdx, rsi
11f21e3 call 0x14083d5a0
11f21e8 mov rcx, qword ptr [rbp - 0x50]
11f21ec mov rax, qword ptr [rcx]
11f21ef mov rdx, rsi
11f21f2 call qword ptr [rax + 0x10]
11f21f5 jmp 0x1411f0b49
11f21fa mov rax, qword ptr [rip + 0x96d207]
11f2201 mov bl, 1
11f2203 test rax, rax
11f2206 je 0x1411f0b4b
11f220c mov rax, qword ptr [rax + 0x80]
11f2213 mov rcx, qword ptr [rax]
11f2216 cmp rcx, qword ptr [rax + 8]
11f221a je 0x1411f0b4b
11f2220 cmp byte ptr [rip + 0x96d6f9], 0
11f2227 je 0x1411f0b4b
11f222d lea rcx, [rbp - 0x50]
11f2231 call 0x1407c8b10
11f2236 lea r15, [rbp + 0xf10]
11f223d mov rcx, r15
11f2240 call 0x1407c8b10
11f2245 call 0x14083caf0
11f224a add rax, 0x38
11f224e mov dword ptr [rbp + 0x17e0], 0x54646976
11f2258 mov qword ptr [rbp + 0x17d8], rax
11f225f lea rsi, [rbp + 0x17d8]
11f2266 mov rcx, r15
11f2269 mov rdx, rsi
11f226c call 0x14083abf0
11f2271 mov rcx, qword ptr [rbp + 0x17d8]
11f2278 mov rax, qword ptr [rcx]
11f227b mov rdx, rsi
11f227e call qword ptr [rax + 0x10]
11f2281 call 0x14083caf0
11f2286 add rax, 0x38
11f228a mov dword ptr [rbp + 0x17e0], 0x54706f73
11f2294 mov qword ptr [rbp + 0x17d8], rax
11f229b lea rcx, [rbp + 0xf10]
11f22a2 lea rsi, [rbp + 0x17d8]
11f22a9 mov rdx, rsi
11f22ac call 0x14083abf0
11f22b1 mov rcx, qword ptr [rbp + 0x17d8]
11f22b8 mov rax, qword ptr [rcx]
11f22bb mov rdx, rsi
11f22be call qword ptr [rax + 0x10]
11f22c1 call 0x14083caf0
11f22c6 add rax, 0x38
11f22ca mov dword ptr [rbp + 0x17e0], 0x5464666e
11f22d4 mov qword ptr [rbp + 0x17d8], rax
11f22db lea rcx, [rbp + 0xf10]
11f22e2 lea rsi, [rbp + 0x17d8]
11f22e9 mov rdx, rsi
11f22ec call 0x14083abf0
11f22f1 mov rcx, qword ptr [rbp + 0x17d8]
11f22f8 mov rax, qword ptr [rcx]
11f22fb mov rdx, rsi
11f22fe call qword ptr [rax + 0x10]
11f2301 call 0x14083caf0
11f2306 add rax, 0x38
11f230a mov dword ptr [rbp + 0x17e0], 0x4e6e6174
11f2314 mov qword ptr [rbp + 0x17d8], rax
11f231b lea rcx, [rbp + 0xf10]
11f2322 lea rsi, [rbp + 0x17d8]
11f2329 mov rdx, rsi
11f232c call 0x14083abf0
11f2331 mov rcx, qword ptr [rbp + 0x17d8]
11f2338 mov rax, qword ptr [rcx]
11f233b mov rdx, rsi
11f233e call qword ptr [rax + 0x10]
11f2341 call 0x14083caf0
11f2346 add rax, 0x38
11f234a mov dword ptr [rbp + 0x17e0], 0x5469736e
11f2354 mov qword ptr [rbp + 0x17d8], rax
11f235b lea rcx, [rbp + 0xf10]
11f2362 lea rsi, [rbp + 0x17d8]
11f2369 mov rdx, rsi
11f236c call 0x14083abf0
11f2371 mov rcx, qword ptr [rbp + 0x17d8]
11f2378 mov rax, qword ptr [rcx]
11f237b mov rdx, rsi
11f237e call qword ptr [rax + 0x10]
11f2381 call 0x14083caf0
11f2386 add rax, 0x38
11f238a mov dword ptr [rbp + 0x17e0], 0x5443534f
11f2394 mov qword ptr [rbp + 0x17d8], rax
11f239b lea rcx, [rbp + 0xf10]
11f23a2 lea rsi, [rbp + 0x17d8]
11f23a9 mov rdx, rsi
11f23ac call 0x14083abf0
11f23b1 mov rcx, qword ptr [rbp + 0x17d8]
11f23b8 mov rax, qword ptr [rcx]
11f23bb mov rdx, rsi
11f23be call qword ptr [rax + 0x10]
11f23c1 call 0x14083caf0
11f23c6 add rax, 0x38
11f23ca mov dword ptr [rbp + 0x17e0], 0x436b6e77
11f23d4 mov qword ptr [rbp + 0x17d8], rax
11f23db lea rcx, [rbp + 0xf10]
11f23e2 lea rsi, [rbp + 0x17d8]
11f23e9 mov rdx, rsi
11f23ec call 0x14083abf0
11f23f1 mov rcx, qword ptr [rbp + 0x17d8]
11f23f8 mov rax, qword ptr [rcx]
11f23fb mov rdx, rsi
11f23fe call qword ptr [rax + 0x10]
11f2401 mov rcx, qword ptr [rip + 0x96de30]
11f2408 mov rax, qword ptr [rip + 0x96de21]
11f240f xor esi, esi
11f2411 cmp rax, rcx
11f2414 je 0x1411f2d3e
11f241a cmp dword ptr [rax], 0x53696454
11f2420 je 0x1411f2d31
11f2426 add rax, 0x10
11f242a cmp rax, rcx
11f242d jne 0x1411f241a
11f242f jmp 0x1411f2d3e
11f2434 lea r15, [rbp + 0x1798]
11f243b mov rcx, r15
11f243e call 0x1407c8b10
11f2443 lea rdi, [rbp - 0x50]
11f2447 xor ebx, ebx
11f2449 lea rsi, [rbp + 0x17b0]
11f2450 jmp 0x1411f2462
11f2452 inc rbx
11f2455 add rdi, 0x18
11f2459 cmp rbx, 0xa4
11f2460 je 0x1411f2495
11f2462 mov rax, qword ptr [rdi]
11f2465 cmp rax, qword ptr [rdi + 8]
11f2469 je 0x1411f2452
11f246b mov rcx, rsi
11f246e mov rdx, rdi
11f2471 call 0x14083d180
11f2476 mov rcx, r15
11f2479 mov edx, ebx
11f247b mov r8, rsi
11f247e call 0x140834980
11f2483 mov rcx, qword ptr [rbp + 0x17b0]
11f248a mov rax, qword ptr [rcx]
11f248d mov rdx, rsi
11f2490 call qword ptr [rax + 0x10]
11f2493 jmp 0x1411f2452
11f2495 lea rsi, [rbp + 0x17b0]
11f249c lea rdx, [rbp + 0x17c0]
11f24a3 mov rcx, rsi
11f24a6 call 0x14083d3a0
11f24ab lea rcx, [rbp + 0x17d8]
11f24b2 mov edx, 0x43496e53
11f24b7 mov r8, rsi
11f24ba call 0x140834980
11f24bf mov rcx, qword ptr [rbp + 0x17b0]
11f24c6 mov rax, qword ptr [rcx]
11f24c9 mov rdx, rsi
11f24cc call qword ptr [rax + 0x10]
11f24cf lea rsi, [rbp + 0x17b0]
11f24d6 lea rdx, [rbp + 0x1798]
11f24dd mov rcx, rsi
11f24e0 call 0x14083d3a0
11f24e5 lea rcx, [rbp + 0x17d8]
11f24ec mov edx, 0x43456c53
11f24f1 mov r8, rsi
11f24f4 call 0x140834980
11f24f9 mov rcx, qword ptr [rbp + 0x17b0]
11f2500 mov rax, qword ptr [rcx]
11f2503 mov rdx, rsi
11f2506 call qword ptr [rax + 0x10]
11f2509 lea rsi, [rbp + 0x17b0]
11f2510 lea rdx, [rbp + 0x17d8]
11f2517 mov rcx, rsi
11f251a call 0x14083d3a0
11f251f mov rcx, r14
11f2522 mov rdx, rsi
11f2525 call 0x14083d5a0
11f252a mov rcx, qword ptr [rbp + 0x17b0]
11f2531 mov rax, qword ptr [rcx]
11f2534 mov rdx, rsi
11f2537 call qword ptr [rax + 0x10]
11f253a lea rcx, [rbp + 0x1798]
11f2541 call 0x140832f70
11f2546 lea rcx, [rbp + 0x17c0]
11f254d call 0x140832f70
11f2552 mov esi, 0xf48
11f2557 lea rcx, [rbp + rsi - 0x50]
11f255c call 0x14083a6a0
11f2561 add rsi, -0x18
11f2565 cmp rsi, -0x18
11f2569 jne 0x1411f2557
11f256b lea rcx, [rbp + 0x1780]
11f2572 call 0x14083a6a0
11f2577 lea rcx, [rbp + 0x1768]
11f257e call 0x14083a6a0
11f2583 lea rcx, [rbp + 0x1750]
11f258a call 0x14083a6a0
11f258f lea rcx, [rbp + 0x1738]
11f2596 call 0x14083a6a0
11f259b lea rcx, [rbp + 0x1720]
11f25a2 call 0x14083a6a0
11f25a7 lea rcx, [rbp + 0x1708]
11f25ae call 0x14083a6a0
11f25b3 lea rcx, [rbp + 0x16f0]
11f25ba call 0x14083a6a0
11f25bf lea rcx, [rbp + 0x16d8]
11f25c6 call 0x14083a6a0
11f25cb lea rcx, [rbp + 0x16c0]
11f25d2 call 0x14083a6a0
11f25d7 lea rcx, [rbp + 0x16a8]
11f25de call 0x14083a6a0
11f25e3 lea rcx, [rbp + 0x1690]
11f25ea call 0x14083a6a0
11f25ef lea rcx, [rbp + 0x1678]
11f25f6 call 0x14083a6a0
11f25fb lea rcx, [rbp + 0x1660]
11f2602 call 0x14083a6a0
11f2607 lea rcx, [rbp + 0x1648]
11f260e call 0x14083a6a0
11f2613 lea rcx, [rbp + 0x1630]
11f261a call 0x14083a6a0
11f261f lea rcx, [rbp + 0x1618]
11f2626 call 0x14083a6a0
11f262b lea rcx, [rbp + 0x1600]
11f2632 call 0x14083a6a0
11f2637 lea rcx, [rbp + 0x15e8]
11f263e call 0x14083a6a0
11f2643 lea rcx, [rbp + 0x15d0]
11f264a call 0x14083a6a0
11f264f lea rcx, [rbp + 0x15b8]
11f2656 call 0x14083a6a0
11f265b lea rcx, [rbp + 0x15a0]
11f2662 call 0x14083a6a0
11f2667 lea rcx, [rbp + 0x1588]
11f266e call 0x14083a6a0
11f2673 lea rcx, [rbp + 0x1570]
11f267a call 0x14083a6a0
11f267f lea rcx, [rbp + 0x1558]
11f2686 call 0x14083a6a0
11f268b lea rcx, [rbp + 0x1540]
11f2692 call 0x14083a6a0
11f2697 lea rcx, [rbp + 0x1528]
11f269e call 0x14083a6a0
11f26a3 lea rcx, [rbp + 0x1510]
11f26aa call 0x14083a6a0
11f26af lea rcx, [rbp + 0x14f8]
11f26b6 call 0x14083a6a0
11f26bb lea rcx, [rbp + 0x14e0]
11f26c2 call 0x14083a6a0
11f26c7 lea rcx, [rbp + 0x14c8]
11f26ce call 0x14083a6a0
11f26d3 lea rcx, [rbp + 0x14b0]
11f26da call 0x14083a6a0
11f26df lea rcx, [rbp + 0x1498]
11f26e6 call 0x14083a6a0
11f26eb lea rcx, [rbp + 0x1480]
11f26f2 call 0x14083a6a0
11f26f7 lea rcx, [rbp + 0x1468]
11f26fe call 0x14083a6a0
11f2703 lea rcx, [rbp + 0x1450]
11f270a call 0x14083a6a0
11f270f lea rcx, [rbp + 0x1438]
11f2716 call 0x14083a6a0
11f271b lea rcx, [rbp + 0x1420]
11f2722 call 0x14083a6a0
11f2727 lea rcx, [rbp + 0x1408]
11f272e call 0x14083a6a0
11f2733 lea rcx, [rbp + 0x13f0]
11f273a call 0x14083a6a0
11f273f lea rcx, [rbp + 0x13d8]
11f2746 call 0x14083a6a0
11f274b lea rcx, [rbp + 0x13c0]
11f2752 call 0x14083a6a0
11f2757 lea rcx, [rbp + 0x13a8]
11f275e call 0x14083a6a0
11f2763 lea rcx, [rbp + 0x1390]
11f276a call 0x14083a6a0
11f276f lea rcx, [rbp + 0x1378]
11f2776 call 0x14083a6a0
11f277b lea rcx, [rbp + 0x1360]
11f2782 call 0x14083a6a0
11f2787 lea rcx, [rbp + 0x1348]
11f278e call 0x14083a6a0
11f2793 lea rcx, [rbp + 0x1330]
11f279a call 0x14083a6a0
11f279f lea rcx, [rbp + 0x1318]
11f27a6 call 0x14083a6a0
11f27ab lea rcx, [rbp + 0x1300]
11f27b2 call 0x14083a6a0
11f27b7 lea rcx, [rbp + 0x12e8]
11f27be call 0x14083a6a0
11f27c3 lea rcx, [rbp + 0x12d0]
11f27ca call 0x14083a6a0
11f27cf lea rcx, [rbp + 0x12b8]
11f27d6 call 0x14083a6a0
11f27db lea rcx, [rbp + 0x12a0]
11f27e2 call 0x14083a6a0
11f27e7 lea rcx, [rbp + 0x1288]
11f27ee call 0x14083a6a0
11f27f3 lea rcx, [rbp + 0x1270]
11f27fa call 0x14083a6a0
11f27ff lea rcx, [rbp + 0x1258]
11f2806 call 0x14083a6a0
11f280b lea rcx, [rbp + 0x1240]
11f2812 call 0x14083a6a0
11f2817 lea rcx, [rbp + 0x1228]
11f281e call 0x14083a6a0
11f2823 lea rcx, [rbp + 0x1210]
11f282a call 0x14083a6a0
11f282f lea rcx, [rbp + 0x11f8]
11f2836 call 0x14083a6a0
11f283b lea rcx, [rbp + 0x11e0]
11f2842 call 0x14083a6a0
11f2847 lea rcx, [rbp + 0x11c8]
11f284e call 0x14083a6a0
11f2853 lea rcx, [rbp + 0x11b0]
11f285a call 0x14083a6a0
11f285f lea rcx, [rbp + 0x1198]
11f2866 call 0x14083a6a0
11f286b lea rcx, [rbp + 0x1180]
11f2872 call 0x14083a6a0
11f2877 lea rcx, [rbp + 0x1168]
11f287e call 0x14083a6a0
11f2883 lea rcx, [rbp + 0x1150]
11f288a call 0x14083a6a0
11f288f lea rcx, [rbp + 0x1138]
11f2896 call 0x14083a6a0
11f289b lea rcx, [rbp + 0x1120]
11f28a2 call 0x14083a6a0
11f28a7 lea rcx, [rbp + 0x1108]
11f28ae call 0x14083a6a0
11f28b3 lea rcx, [rbp + 0x10f0]
11f28ba call 0x14083a6a0
11f28bf lea rcx, [rbp + 0x10d8]
11f28c6 call 0x14083a6a0
11f28cb lea rcx, [rbp + 0x10c0]
11f28d2 call 0x14083a6a0
11f28d7 lea rcx, [rbp + 0x10a8]
11f28de call 0x14083a6a0
11f28e3 lea rcx, [rbp + 0x1090]
11f28ea call 0x14083a6a0
11f28ef lea rcx, [rbp + 0x1078]
11f28f6 call 0x14083a6a0
11f28fb lea rcx, [rbp + 0x1060]
11f2902 call 0x14083a6a0
11f2907 lea rcx, [rbp + 0x1048]
11f290e call 0x14083a6a0
11f2913 lea rcx, [rbp + 0x1030]
11f291a call 0x14083a6a0
11f291f lea rcx, [rbp + 0x1018]
11f2926 call 0x14083a6a0
11f292b lea rcx, [rbp + 0x1000]
11f2932 call 0x14083a6a0
11f2937 lea rcx, [rbp + 0xfe8]
11f293e call 0x14083a6a0
11f2943 lea rcx, [rbp + 0xfd0]
11f294a call 0x14083a6a0
11f294f lea rcx, [rbp + 0xfb8]
11f2956 call 0x14083a6a0
11f295b lea rcx, [rbp + 0xfa0]
11f2962 call 0x14083a6a0
11f2967 lea rcx, [rbp + 0xf88]
11f296e call 0x14083a6a0
11f2973 lea rcx, [rbp + 0xf70]
11f297a call 0x14083a6a0
11f297f lea rcx, [rbp + 0xf58]
11f2986 call 0x14083a6a0
11f298b lea rcx, [rbp + 0xf40]
11f2992 call 0x14083a6a0
11f2997 lea rcx, [rbp + 0xf28]
11f299e call 0x14083a6a0
11f29a3 lea rcx, [rbp + 0xf10]
11f29aa call 0x14083a6a0
11f29af lea rcx, [rbp + 0x17d8]
11f29b6 call 0x140832f70
11f29bb jmp 0x1411f0b49
11f29c0 mov rcx, rdi
11f29c3 mov dl, 7
11f29c5 mov r8d, 0x636f6d70
11f29cb jmp 0x1411f2a60
11f29d0 mov rcx, rdi
11f29d3 mov dl, 7
11f29d5 mov r8d, 0x73746474
11f29db jmp 0x1411f2a60
11f29e0 mov rcx, rdi
11f29e3 mov dl, 7
11f29e5 jmp 0x1411f2a5a
11f29e7 cmp esi, 0x434c5273
11f29ed jne 0x1411f2a95
11f29f3 mov rcx, rdi
11f29f6 mov dl, 0xd
11f29f8 mov r8d, 0x73746474
11f29fe jmp 0x1411f2a60
11f2a00 mov rcx, rdi
11f2a03 mov dl, 0xb
11f2a05 jmp 0x1411f2a5a
11f2a07 mov rcx, rdi
11f2a0a mov dl, 0xb
11f2a0c mov r8d, 0x73746462
11f2a12 jmp 0x1411f2a60
11f2a14 mov rcx, rdi
11f2a17 mov dl, 0xb
11f2a19 mov r8d, 0x73746474
11f2a1f jmp 0x1411f2a60
11f2a21 mov rcx, rdi
11f2a24 mov dl, 0xb
11f2a26 mov r8d, 0x73746e6d
11f2a2c jmp 0x1411f2a60
11f2a2e mov rcx, rdi
11f2a31 mov dl, 0xb
11f2a33 mov r8d, 0x73746964
11f2a39 jmp 0x1411f2a60
11f2a3b mov rcx, rdi
11f2a3e mov dl, 0x1c
11f2a40 mov r8d, 0x73746462
11f2a46 jmp 0x1411f2a60
11f2a48 mov rcx, rdi
11f2a4b mov dl, 0x1c
11f2a4d mov r8d, 0x73746e6d
11f2a53 jmp 0x1411f2a60
11f2a55 mov rcx, rdi
11f2a58 mov dl, 0x1c
11f2a5a mov r8d, 0x6f746874
11f2a60 mov r9, r14
11f2a63 add rsp, 0x1878
11f2a6a pop rbx
11f2a6b pop rdi
11f2a6c pop rsi
11f2a6d pop r12
11f2a6f pop r13
11f2a71 pop r14
11f2a73 pop r15
11f2a75 pop rbp
11f2a76 jmp 0x1411e8af0
11f2a7b mov rcx, rdi
11f2a7e mov dl, 0x1c
11f2a80 mov r8d, 0x73746964
11f2a86 jmp 0x1411f2a60
11f2a88 mov rcx, rdi
11f2a8b mov dl, 0x1c
11f2a8d mov r8d, 0x73746474
11f2a93 jmp 0x1411f2a60
11f2a95 mov rax, qword ptr [rdi]
11f2a98 mov rax, qword ptr [rax + 0x1c0]
11f2a9f mov rcx, rdi
11f2aa2 mov edx, esi
11f2aa4 mov r8, r14
11f2aa7 add rsp, 0x1878
11f2aae pop rbx
11f2aaf pop rdi
11f2ab0 pop rsi
11f2ab1 pop r12
11f2ab3 pop r13
11f2ab5 pop r14
11f2ab7 pop r15
11f2ab9 pop rbp
11f2aba jmp rax
11f2abd xor r9d, r9d
11f2ac0 mov byte ptr [rsp + 0x20], 1
11f2ac5 lea rdx, [rbp + 0x17d8]
11f2acc lea r8, [rbp + 0x17c0]
11f2ad3 mov rcx, rdi
11f2ad6 call 0x1411d6d90
11f2adb mov rdi, rax
11f2ade call 0x14083caf0
11f2ae3 mov rcx, rax
11f2ae6 add rcx, 8
11f2aea mov qword ptr [rbp + 0xf18], 0
11f2af5 mov qword ptr [rbp + 0xf10], rcx
11f2afc lea rsi, [rbp - 0x48]
11f2b00 mov rax, qword ptr [rax + 8]
11f2b04 lea rbx, [rbp + 0xf10]
11f2b0b mov rdx, rbx
11f2b0e mov r8, rsi
11f2b11 call qword ptr [rax + 0x18]
11f2b14 mov dword ptr [rbp - 0x50], 0xff7fffff
11f2b1b mov rcx, qword ptr [rbp + 0xf10]
11f2b22 mov rax, qword ptr [rcx]
11f2b25 mov rdx, rbx
11f2b28 call qword ptr [rax + 0x10]
11f2b2b test rdi, rdi
11f2b2e je 0x1411f2b6e
11f2b30 mov rax, qword ptr [rdi]
11f2b33 lea rdx, [rbp + 0xf10]
11f2b3a mov rcx, rdi
11f2b3d call qword ptr [rax + 0x90]
11f2b43 mov eax, dword ptr [rbp + 0xf10]
11f2b49 mov dword ptr [rbp - 0x50], eax
11f2b4c lea rdi, [rbp + 0xf18]
11f2b53 mov rcx, rsi
11f2b56 mov rdx, rdi
11f2b59 call 0x14083d5a0
11f2b5e mov rcx, qword ptr [rbp + 0xf18]
11f2b65 mov rax, qword ptr [rcx]
11f2b68 mov rdx, rdi
11f2b6b call qword ptr [rax + 0x10]
11f2b6e lea rcx, [rbp - 0x50]
11f2b72 lea rdi, [rbp + 0xf10]
11f2b79 mov rdx, rdi
11f2b7c call 0x140fea300
11f2b81 mov rcx, r14
11f2b84 mov rdx, rdi
11f2b87 call 0x14083d5a0
11f2b8c mov rcx, qword ptr [rbp + 0xf10]
11f2b93 mov rax, qword ptr [rcx]
11f2b96 mov rdx, rdi
11f2b99 call qword ptr [rax + 0x10]
11f2b9c mov rcx, qword ptr [rbp - 0x48]
11f2ba0 mov rax, qword ptr [rcx]
11f2ba3 mov rdx, rsi
11f2ba6 call qword ptr [rax + 0x10]
11f2ba9 jmp 0x1411f0b49
11f2bae xor r9d, r9d
11f2bb1 mov byte ptr [rsp + 0x20], 0
11f2bb6 lea rdx, [rbp + 0x17d8]
11f2bbd lea r8, [rbp + 0x17c0]
11f2bc4 mov rcx, rdi
11f2bc7 call 0x1411d6d90
11f2bcc mov rdi, rax
11f2bcf call 0x14083caf0
11f2bd4 mov rcx, rax
11f2bd7 add rcx, 8
11f2bdb mov qword ptr [rbp + 0xf18], 0
11f2be6 mov qword ptr [rbp + 0xf10], rcx
11f2bed lea rsi, [rbp - 0x48]
11f2bf1 mov rax, qword ptr [rax + 8]
11f2bf5 lea rbx, [rbp + 0xf10]
11f2bfc mov rdx, rbx
11f2bff mov r8, rsi
11f2c02 call qword ptr [rax + 0x18]
11f2c05 mov dword ptr [rbp - 0x50], 0xff7fffff
11f2c0c mov rcx, qword ptr [rbp + 0xf10]
11f2c13 mov rax, qword ptr [rcx]
11f2c16 mov rdx, rbx
11f2c19 call qword ptr [rax + 0x10]
11f2c1c test rdi, rdi
11f2c1f je 0x1411f2c5f
11f2c21 mov rax, qword ptr [rdi]
11f2c24 lea rdx, [rbp + 0xf10]
11f2c2b mov rcx, rdi
11f2c2e call qword ptr [rax + 0x90]
11f2c34 mov eax, dword ptr [rbp + 0xf10]
11f2c3a mov dword ptr [rbp - 0x50], eax
11f2c3d lea rdi, [rbp + 0xf18]
11f2c44 mov rcx, rsi
11f2c47 mov rdx, rdi
11f2c4a call 0x14083d5a0
11f2c4f mov rcx, qword ptr [rbp + 0xf18]
11f2c56 mov rax, qword ptr [rcx]
11f2c59 mov rdx, rdi
11f2c5c call qword ptr [rax + 0x10]
11f2c5f lea rcx, [rbp - 0x50]
11f2c63 lea rdi, [rbp + 0xf10]
11f2c6a mov rdx, rdi
11f2c6d call 0x140fea300
11f2c72 mov rcx, r14
11f2c75 mov rdx, rdi
11f2c78 call 0x14083d5a0
11f2c7d mov rcx, qword ptr [rbp + 0xf10]
11f2c84 mov rax, qword ptr [rcx]
11f2c87 mov rdx, rdi
11f2c8a call qword ptr [rax + 0x10]
11f2c8d mov rcx, qword ptr [rbp - 0x48]
11f2c91 mov rax, qword ptr [rcx]
11f2c94 mov rdx, rsi
11f2c97 call qword ptr [rax + 0x10]
11f2c9a jmp 0x1411f0b49
11f2c9f lea rcx, [rip + 0x96d61a]
11f2ca6 lea rsi, [rbp - 0x50]
11f2caa mov rdx, rsi
11f2cad call 0x140fea300
11f2cb2 mov rcx, r14
11f2cb5 mov rdx, rsi
11f2cb8 call 0x14083d5a0
11f2cbd mov rcx, qword ptr [rbp - 0x50]
11f2cc1 mov rax, qword ptr [rcx]
11f2cc4 mov rdx, rsi
11f2cc7 call qword ptr [rax + 0x10]
11f2cca jmp 0x1411f0b49
11f2ccf xor ecx, ecx
11f2cd1 mov rdx, r14
11f2cd4 call 0x140fe6e60
11f2cd9 jmp 0x1411f0b49
11f2cde mov rax, qword ptr [rdi]
11f2ce1 mov rcx, rdi
11f2ce4 call qword ptr [rax + 0x38]
11f2ce7 cmp eax, 3
11f2cea jne 0x1411f0b4b
11f2cf0 test byte ptr [rdi + 0x161], 1
11f2cf7 jne 0x1411f0b4b
11f2cfd mov rcx, rdi
11f2d00 call 0x1408fec50
11f2d05 test al, al
11f2d07 jne 0x1411f0b4b
11f2d0d mov rax, qword ptr [rdi]
11f2d10 mov rcx, rdi
11f2d13 call qword ptr [rax + 0x160]
11f2d19 test al, al
11f2d1b jne 0x1411f0b4b
11f2d21 mov rax, qword ptr [rdi]
11f2d24 mov rcx, rdi
11f2d27 mov edx, 0x436c6570
11f2d2c jmp 0x1411f1f60
11f2d31 cmp rax, rcx
11f2d34 je 0x1411f2d3c
11f2d36 mov rsi, qword ptr [rax + 8]
11f2d3a jmp 0x1411f2d3e
11f2d3c xor esi, esi
11f2d3e call 0x14083caf0
11f2d43 test rsi, rsi
11f2d46 lea rdx, [rip + 0x966d53]
11f2d4d cmovne rdx, rsi
11f2d51 add rax, 8
11f2d55 mov qword ptr [rbp + 0x17e8], 0
11f2d60 mov qword ptr [rbp + 0x17e0], rax
11f2d67 lea rcx, [rbp + 0x17d8]
11f2d6e call 0x140fea870
11f2d73 mov ecx, dword ptr [rbp + 0x17d8]
11f2d79 cmp ecx, 0xfeffffff
11f2d7f ja 0x1411f2eb8
11f2d85 and ecx, 0x7fffff
11f2d8b cmp ecx, 0x7fffff
11f2d91 je 0x1411f2eb8
11f2d97 call 0x140f5bde0
11f2d9c test rax, rax
11f2d9f je 0x1411f2eb8
11f2da5 cmp qword ptr [rax + 0x30], rdi
11f2da9 jne 0x1411f2eb8
11f2daf call 0x14083caf0
11f2db4 add rax, 0x38
11f2db8 mov dword ptr [rbp + 0x17c8], 0x546e6566
11f2dc2 mov qword ptr [rbp + 0x17c0], rax
11f2dc9 lea rcx, [rbp + 0xf10]
11f2dd0 lea rsi, [rbp + 0x17c0]
11f2dd7 mov rdx, rsi
11f2dda call 0x14083abf0
11f2ddf mov rcx, qword ptr [rbp + 0x17c0]
11f2de6 mov rax, qword ptr [rcx]
11f2de9 mov rdx, rsi
11f2dec call qword ptr [rax + 0x10]
11f2def call 0x14083caf0
11f2df4 add rax, 0x38
11f2df8 mov dword ptr [rbp + 0x17c8], 0x54437374
11f2e02 mov qword ptr [rbp + 0x17c0], rax
11f2e09 lea rcx, [rbp + 0xf10]
11f2e10 lea rsi, [rbp + 0x17c0]
11f2e17 mov rdx, rsi
11f2e1a call 0x14083abf0
11f2e1f mov rcx, qword ptr [rbp + 0x17c0]
11f2e26 mov rax, qword ptr [rcx]
11f2e29 mov rdx, rsi
11f2e2c call qword ptr [rax + 0x10]
11f2e2f call 0x14083caf0
11f2e34 add rax, 0x38
11f2e38 mov dword ptr [rbp + 0x17c8], 0x54434d4a
11f2e42 mov qword ptr [rbp + 0x17c0], rax
11f2e49 lea rcx, [rbp + 0xf10]
11f2e50 lea rsi, [rbp + 0x17c0]
11f2e57 mov rdx, rsi
11f2e5a call 0x14083abf0
11f2e5f mov rcx, qword ptr [rbp + 0x17c0]
11f2e66 mov rax, qword ptr [rcx]
11f2e69 mov rdx, rsi
11f2e6c call qword ptr [rax + 0x10]
11f2e6f cmp byte ptr [rdi + 0xba], 0
11f2e76 jne 0x1411f2eb8
11f2e78 call 0x14083caf0
11f2e7d add rax, 0x38
11f2e81 mov dword ptr [rbp + 0x17c8], 0x43736673
11f2e8b mov qword ptr [rbp + 0x17c0], rax
11f2e92 lea rcx, [rbp + 0xf10]
11f2e99 lea rsi, [rbp + 0x17c0]
11f2ea0 mov rdx, rsi
11f2ea3 call 0x14083abf0
11f2ea8 mov rcx, qword ptr [rbp + 0x17c0]
11f2eaf mov rax, qword ptr [rcx]
11f2eb2 mov rdx, rsi
11f2eb5 call qword ptr [rax + 0x10]
11f2eb8 lea rsi, [rbp - 0x50]
11f2ebc lea r8, [rbp + 0xf10]
11f2ec3 mov rcx, rdi
11f2ec6 mov rdx, rsi
11f2ec9 call 0x1407ea5e0
11f2ece lea rdi, [rbp + 0x17c0]
11f2ed5 mov rcx, rdi
11f2ed8 mov rdx, rsi
11f2edb call 0x14083d3a0
11f2ee0 mov rcx, r14
11f2ee3 mov rdx, rdi
11f2ee6 call 0x14083d5a0
11f2eeb mov rcx, qword ptr [rbp + 0x17c0]
11f2ef2 mov rax, qword ptr [rcx]
11f2ef5 mov rdx, rdi
11f2ef8 call qword ptr [rax + 0x10]