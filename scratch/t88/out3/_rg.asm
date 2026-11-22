1543ca0 push rbp
1543ca1 push rsi
1543ca2 push rdi
1543ca3 push rbx
1543ca4 sub rsp, 0x38
1543ca8 lea rbp, [rsp + 0x30]
1543cad mov qword ptr [rbp], 0xfffffffffffffffe
1543cb5 mov rsi, r8
1543cb8 mov rdi, rcx
1543cbb cmp edx, 0x696e666e
1543cc1 jg 0x141543d6d
1543cc7 cmp edx, 0x656e6473
1543ccd jg 0x141543e08
1543cd3 cmp edx, 0x63617367
1543cd9 jle 0x141543f4c
1543cdf cmp edx, 0x63617368
1543ce5 je 0x14154421e
1543ceb cmp edx, 0x636e7374
1543cf1 je 0x14154427c
1543cf7 cmp edx, 0x636f6d70
1543cfd jne 0x1415446e0
1543d03 mov eax, dword ptr [rdi + 0x34]
1543d06 shl rax, 0x20
1543d0a movsxd rdi, dword ptr [rdi + 0x30]
1543d0e or rdi, rax
1543d11 call 0x14083caf0
1543d16 add rax, 0x48
1543d1a mov qword ptr [rbp - 8], rdi
1543d1e mov qword ptr [rbp - 0x10], rax
1543d22 lea rcx, [rbp - 0x10]
1543d26 cmp rcx, rsi
1543d29 je 0x141543d5b
1543d2b mov rcx, qword ptr [rsi]
1543d2e mov rax, qword ptr [rcx]
1543d31 mov rdx, rsi
1543d34 call qword ptr [rax + 0x10]
1543d37 mov rax, qword ptr [rbp - 0x10]
1543d3b mov rcx, qword ptr [rbp - 8]
1543d3f mov qword ptr [rsi + 8], rcx
1543d43 mov qword ptr [rsi], rax
1543d46 call 0x14083caf0
1543d4b add rax, 8
1543d4f mov qword ptr [rbp - 8], 0
1543d57 mov qword ptr [rbp - 0x10], rax
1543d5b mov rbx, qword ptr [rax]
1543d5e lea rdx, [rbp - 0x10]
1543d62 mov rcx, rax
1543d65 call qword ptr [rbx + 0x10]
1543d68 jmp 0x1415446d5
1543d6d cmp edx, 0x73746461
1543d73 jg 0x141543eb2
1543d79 cmp edx, 0x6f746873
1543d7f jle 0x141543fdc
1543d85 cmp edx, 0x6f746874
1543d8b je 0x1415442df
1543d91 cmp edx, 0x72617469
1543d97 je 0x141544349
1543d9d cmp edx, 0x72726561
1543da3 jne 0x1415446e0
1543da9 movsx edi, byte ptr [rdi + 0x5c]
1543dad call 0x14083caf0
1543db2 add rax, 0x28
1543db6 mov dword ptr [rbp - 8], edi
1543db9 mov qword ptr [rbp - 0x10], rax
1543dbd lea rcx, [rbp - 0x10]
1543dc1 cmp rcx, rsi
1543dc4 je 0x141543df6
1543dc6 mov rcx, qword ptr [rsi]
1543dc9 mov rax, qword ptr [rcx]
1543dcc mov rdx, rsi
1543dcf call qword ptr [rax + 0x10]
1543dd2 mov rax, qword ptr [rbp - 0x10]
1543dd6 mov rcx, qword ptr [rbp - 8]
1543dda mov qword ptr [rsi + 8], rcx
1543dde mov qword ptr [rsi], rax
1543de1 call 0x14083caf0
1543de6 add rax, 8
1543dea mov qword ptr [rbp - 8], 0
1543df2 mov qword ptr [rbp - 0x10], rax
1543df6 mov rbx, qword ptr [rax]
1543df9 lea rdx, [rbp - 0x10]
1543dfd mov rcx, rax
1543e00 call qword ptr [rbx + 0x10]
1543e03 jmp 0x1415446d5
1543e08 cmp edx, 0x66736773
1543e0e jle 0x14154406e
1543e14 cmp edx, 0x66736774
1543e1a je 0x1415443a8
1543e20 cmp edx, 0x67616d73
1543e26 je 0x1415441bf
1543e2c cmp edx, 0x676f6c73
1543e32 jne 0x1415446e0
1543e38 movsx ebx, word ptr [rdi + 0x56]
1543e3c call 0x14083caf0
1543e41 add rax, 0x28
1543e45 mov dword ptr [rbp - 8], ebx
1543e48 mov qword ptr [rbp - 0x10], rax
1543e4c lea rcx, [rbp - 0x10]
1543e50 cmp rcx, rsi
1543e53 je 0x141543e85
1543e55 mov rcx, qword ptr [rsi]
1543e58 mov rax, qword ptr [rcx]
1543e5b mov rdx, rsi
1543e5e call qword ptr [rax + 0x10]
1543e61 mov rax, qword ptr [rbp - 0x10]
1543e65 mov rcx, qword ptr [rbp - 8]
1543e69 mov qword ptr [rsi + 8], rcx
1543e6d mov qword ptr [rsi], rax
1543e70 call 0x14083caf0
1543e75 add rax, 8
1543e79 mov qword ptr [rbp - 8], 0
1543e81 mov qword ptr [rbp - 0x10], rax
1543e85 mov rbx, qword ptr [rax]
1543e88 lea rdx, [rbp - 0x10]
1543e8c mov rcx, rax
1543e8f call qword ptr [rbx + 0x10]
1543e92 lea rax, [rip + 0x615c07]
1543e99 cmp rsi, rax
1543e9c je 0x1415446d5
1543ea2 cmp word ptr [rdi + 0x56], 0
1543ea7 js 0x141544617
1543ead jmp 0x1415446d5
1543eb2 cmp edx, 0x73746963
1543eb8 jle 0x1415440e5
1543ebe cmp edx, 0x7465616d
1543ec4 je 0x141544407
1543eca cmp edx, 0x73746e6d
1543ed0 je 0x141544471
1543ed6 cmp edx, 0x73746964
1543edc jne 0x1415446e0
1543ee2 mov eax, dword ptr [rdi + 0x1c]
1543ee5 shl rax, 0x20
1543ee9 movsxd rdi, dword ptr [rdi + 0x18]
1543eed or rdi, rax
1543ef0 call 0x14083caf0
1543ef5 add rax, 0x48
1543ef9 mov qword ptr [rbp - 8], rdi
1543efd mov qword ptr [rbp - 0x10], rax
1543f01 lea rcx, [rbp - 0x10]
1543f05 cmp rcx, rsi
1543f08 je 0x141543f3a
1543f0a mov rcx, qword ptr [rsi]
1543f0d mov rax, qword ptr [rcx]
1543f10 mov rdx, rsi
1543f13 call qword ptr [rax + 0x10]
1543f16 mov rax, qword ptr [rbp - 0x10]
1543f1a mov rcx, qword ptr [rbp - 8]
1543f1e mov qword ptr [rsi + 8], rcx
1543f22 mov qword ptr [rsi], rax
1543f25 call 0x14083caf0
1543f2a add rax, 8
1543f2e mov qword ptr [rbp - 8], 0
1543f36 mov qword ptr [rbp - 0x10], rax
1543f3a mov rdi, qword ptr [rax]
1543f3d lea rdx, [rbp - 0x10]
1543f41 mov rcx, rax
1543f44 call qword ptr [rdi + 0x10]
1543f47 jmp 0x1415446d5
1543f4c cmp edx, 0x61707073
1543f52 je 0x1415441bf
1543f58 cmp edx, 0x61747465
1543f5e jne 0x1415446e0
1543f64 mov ebx, dword ptr [rdi + 0x50]
1543f67 call 0x14083caf0
1543f6c add rax, 0x28
1543f70 mov dword ptr [rbp - 8], ebx
1543f73 mov qword ptr [rbp - 0x10], rax
1543f77 lea rcx, [rbp - 0x10]
1543f7b cmp rcx, rsi
1543f7e je 0x141543fb0
1543f80 mov rcx, qword ptr [rsi]
1543f83 mov rax, qword ptr [rcx]
1543f86 mov rdx, rsi
1543f89 call qword ptr [rax + 0x10]
1543f8c mov rax, qword ptr [rbp - 0x10]
1543f90 mov rcx, qword ptr [rbp - 8]
1543f94 mov qword ptr [rsi + 8], rcx
1543f98 mov qword ptr [rsi], rax
1543f9b call 0x14083caf0
1543fa0 add rax, 8
1543fa4 mov qword ptr [rbp - 8], 0
1543fac mov qword ptr [rbp - 0x10], rax
1543fb0 mov rbx, qword ptr [rax]
1543fb3 lea rdx, [rbp - 0x10]
1543fb7 mov rcx, rax
1543fba call qword ptr [rbx + 0x10]
1543fbd lea rax, [rip + 0x615adc]
1543fc4 cmp rsi, rax
1543fc7 je 0x1415446d5
1543fcd cmp dword ptr [rdi + 0x50], -1
1543fd1 je 0x141544617
1543fd7 jmp 0x1415446d5
1543fdc cmp edx, 0x696e666f
1543fe2 je 0x1415444f0
1543fe8 cmp edx, 0x6f676c73
1543fee jne 0x1415446e0
1543ff4 movsx ebx, word ptr [rdi + 0x58]
1543ff8 call 0x14083caf0
1543ffd add rax, 0x28
1544001 mov dword ptr [rbp - 8], ebx
1544004 mov qword ptr [rbp - 0x10], rax
1544008 lea rcx, [rbp - 0x10]
154400c cmp rcx, rsi
154400f je 0x141544041
1544011 mov rcx, qword ptr [rsi]
1544014 mov rax, qword ptr [rcx]
1544017 mov rdx, rsi
154401a call qword ptr [rax + 0x10]
154401d mov rax, qword ptr [rbp - 0x10]
1544021 mov rcx, qword ptr [rbp - 8]
1544025 mov qword ptr [rsi + 8], rcx
1544029 mov qword ptr [rsi], rax
154402c call 0x14083caf0
1544031 add rax, 8
1544035 mov qword ptr [rbp - 8], 0
154403d mov qword ptr [rbp - 0x10], rax
1544041 mov rbx, qword ptr [rax]
1544044 lea rdx, [rbp - 0x10]
1544048 mov rcx, rax
154404b call qword ptr [rbx + 0x10]
154404e lea rax, [rip + 0x615a4b]
1544055 cmp rsi, rax
1544058 je 0x1415446d5
154405e cmp word ptr [rdi + 0x58], 0
1544063 js 0x141544617
1544069 jmp 0x1415446d5
154406e cmp edx, 0x656e6474
1544074 je 0x14154454f
154407a cmp edx, 0x6574696e
1544080 jne 0x1415446e0
1544086 movsx edi, byte ptr [rdi + 0x5d]
154408a call 0x14083caf0
154408f add rax, 0x28
1544093 mov dword ptr [rbp - 8], edi
1544096 mov qword ptr [rbp - 0x10], rax
154409a lea rcx, [rbp - 0x10]
154409e cmp rcx, rsi
15440a1 je 0x1415440d3
15440a3 mov rcx, qword ptr [rsi]
15440a6 mov rax, qword ptr [rcx]
15440a9 mov rdx, rsi
15440ac call qword ptr [rax + 0x10]
15440af mov rax, qword ptr [rbp - 0x10]
15440b3 mov rcx, qword ptr [rbp - 8]
15440b7 mov qword ptr [rsi + 8], rcx
15440bb mov qword ptr [rsi], rax
15440be call 0x14083caf0
15440c3 add rax, 8
15440c7 mov qword ptr [rbp - 8], 0
15440cf mov qword ptr [rbp - 0x10], rax
15440d3 mov rbx, qword ptr [rax]
15440d6 lea rdx, [rbp - 0x10]
15440da mov rcx, rax
15440dd call qword ptr [rbx + 0x10]
15440e0 jmp 0x1415446d5
15440e5 cmp edx, 0x73746462
15440eb je 0x14154463f
15440f1 cmp edx, 0x73746474
15440f7 jne 0x1415446e0
15440fd mov eax, dword ptr [rip + 0x617dcd]
1544103 mov ecx, dword ptr [rip + 0x581257]
1544109 mov rdx, qword ptr gs:[0x58]
1544112 mov rcx, qword ptr [rdx + rcx*8]
1544116 cmp eax, dword ptr [rcx + 4]
154411c jg 0x1415446f3
1544122 movzx eax, word ptr [rdi + 0x40]
1544126 mov ecx, eax
1544128 and ecx, 0x1ff
154412e shl ecx, 8
1544131 movzx edx, word ptr [rdi + 0x42]
1544135 shr eax, 9
1544138 shl edx, 0x11
154413b or edx, eax
154413d or edx, ecx
154413f mov dword ptr [rbp - 8], edx
1544142 lea rcx, [rip + 0x617d57]
1544149 mov qword ptr [rbp - 0x10], rcx
154414d lea rax, [rbp - 0x10]
1544151 cmp rax, rsi
1544154 je 0x141544189
1544156 mov rcx, qword ptr [rsi]
1544159 mov rax, qword ptr [rcx]
154415c mov rdx, rsi
154415f call qword ptr [rax + 0x10]
1544162 mov rax, qword ptr [rbp - 0x10]
1544166 mov rcx, qword ptr [rbp - 8]
154416a mov qword ptr [rsi + 8], rcx
154416e mov qword ptr [rsi], rax
1544171 call 0x14083caf0
1544176 mov rcx, rax
1544179 add rcx, 8
154417d mov qword ptr [rbp - 8], 0
1544185 mov qword ptr [rbp - 0x10], rcx
1544189 mov rax, qword ptr [rcx]
154418c lea rdx, [rbp - 0x10]
1544190 call qword ptr [rax + 0x10]
1544193 lea rax, [rip + 0x615906]
154419a cmp rsi, rax
154419d je 0x1415446d5
15441a3 movzx eax, word ptr [rdi + 0x40]
15441a7 and eax, 0x1ff
15441ac cmp ax, 1
15441b0 jne 0x1415446d5
15441b6 movzx eax, word ptr [rdi + 0x42]
15441ba jmp 0x14154460c
15441bf movsx edi, word ptr [rdi + 0x54]
15441c3 call 0x14083caf0
15441c8 add rax, 0x28
15441cc mov dword ptr [rbp - 8], edi
15441cf mov qword ptr [rbp - 0x10], rax
15441d3 lea rcx, [rbp - 0x10]
15441d7 cmp rcx, rsi
15441da je 0x14154420c
15441dc mov rcx, qword ptr [rsi]
15441df mov rax, qword ptr [rcx]
15441e2 mov rdx, rsi
15441e5 call qword ptr [rax + 0x10]
15441e8 mov rax, qword ptr [rbp - 0x10]
15441ec mov rcx, qword ptr [rbp - 8]
15441f0 mov qword ptr [rsi + 8], rcx
15441f4 mov qword ptr [rsi], rax
15441f7 call 0x14083caf0
15441fc add rax, 8
1544200 mov qword ptr [rbp - 8], 0
1544208 mov qword ptr [rbp - 0x10], rax
154420c mov rdi, qword ptr [rax]
154420f lea rdx, [rbp - 0x10]
1544213 mov rcx, rax
1544216 call qword ptr [rdi + 0x10]
1544219 jmp 0x1415446d5
154421e mov edi, dword ptr [rdi + 0x50]
1544221 call 0x14083caf0
1544226 add rax, 0x28
154422a mov dword ptr [rbp - 8], edi
154422d mov qword ptr [rbp - 0x10], rax
1544231 lea rcx, [rbp - 0x10]
1544235 cmp rcx, rsi
1544238 je 0x14154426a
154423a mov rcx, qword ptr [rsi]
154423d mov rax, qword ptr [rcx]
1544240 mov rdx, rsi
1544243 call qword ptr [rax + 0x10]
1544246 mov rax, qword ptr [rbp - 0x10]
154424a mov rcx, qword ptr [rbp - 8]
154424e mov qword ptr [rsi + 8], rcx
1544252 mov qword ptr [rsi], rax
1544255 call 0x14083caf0
154425a add rax, 8
154425e mov qword ptr [rbp - 8], 0
1544266 mov qword ptr [rbp - 0x10], rax
154426a mov rdi, qword ptr [rax]
154426d lea rdx, [rbp - 0x10]
1544271 mov rcx, rax
1544274 call qword ptr [rdi + 0x10]
1544277 jmp 0x1415446d5
154427c movzx ebx, byte ptr [rdi + 0x5d]
1544280 call 0x14083caf0
1544285 add rax, 0x18
1544289 cmp bl, 1
154428c sete byte ptr [rbp - 8]
1544290 mov qword ptr [rbp - 0x10], rax
1544294 lea rcx, [rbp - 0x10]
1544298 cmp rcx, rsi
154429b je 0x1415442cd
154429d mov rcx, qword ptr [rsi]
15442a0 mov rax, qword ptr [rcx]
15442a3 mov rdx, rsi
15442a6 call qword ptr [rax + 0x10]
15442a9 mov rax, qword ptr [rbp - 0x10]
15442ad mov rcx, qword ptr [rbp - 8]
15442b1 mov qword ptr [rsi + 8], rcx
15442b5 mov qword ptr [rsi], rax
15442b8 call 0x14083caf0
15442bd add rax, 8
15442c1 mov qword ptr [rbp - 8], 0
15442c9 mov qword ptr [rbp - 0x10], rax
15442cd mov rbx, qword ptr [rax]
15442d0 lea rdx, [rbp - 0x10]
15442d4 mov rcx, rax
15442d7 call qword ptr [rbx + 0x10]
15442da jmp 0x1415446d5
15442df mov eax, dword ptr [rdi + 0x2c]
15442e2 shl rax, 0x20
15442e6 movsxd rdi, dword ptr [rdi + 0x28]
15442ea or rdi, rax
15442ed call 0x14083caf0
15442f2 add rax, 0x48
15442f6 mov qword ptr [rbp - 8], rdi
15442fa mov qword ptr [rbp - 0x10], rax
15442fe lea rcx, [rbp - 0x10]
1544302 cmp rcx, rsi
1544305 je 0x141544337
1544307 mov rcx, qword ptr [rsi]
154430a mov rax, qword ptr [rcx]
154430d mov rdx, rsi
1544310 call qword ptr [rax + 0x10]
1544313 mov rax, qword ptr [rbp - 0x10]
1544317 mov rcx, qword ptr [rbp - 8]
154431b mov qword ptr [rsi + 8], rcx
154431f mov qword ptr [rsi], rax
1544322 call 0x14083caf0
1544327 add rax, 8
154432b mov qword ptr [rbp - 8], 0
1544333 mov qword ptr [rbp - 0x10], rax
1544337 mov rdi, qword ptr [rax]
154433a lea rdx, [rbp - 0x10]
154433e mov rcx, rax
1544341 call qword ptr [rdi + 0x10]
1544344 jmp 0x1415446d5
1544349 movsx edi, byte ptr [rdi + 0x5a]
154434d call 0x14083caf0
1544352 add rax, 0x28
1544356 mov dword ptr [rbp - 8], edi
1544359 mov qword ptr [rbp - 0x10], rax
154435d lea rcx, [rbp - 0x10]
1544361 cmp rcx, rsi
1544364 je 0x141544396
1544366 mov rcx, qword ptr [rsi]
1544369 mov rax, qword ptr [rcx]
154436c mov rdx, rsi
154436f call qword ptr [rax + 0x10]
1544372 mov rax, qword ptr [rbp - 0x10]
1544376 mov rcx, qword ptr [rbp - 8]
154437a mov qword ptr [rsi + 8], rcx
154437e mov qword ptr [rsi], rax
1544381 call 0x14083caf0
1544386 add rax, 8
154438a mov qword ptr [rbp - 8], 0
1544392 mov qword ptr [rbp - 0x10], rax
1544396 mov rbx, qword ptr [rax]
1544399 lea rdx, [rbp - 0x10]
154439d mov rcx, rax
15443a0 call qword ptr [rbx + 0x10]
15443a3 jmp 0x1415446d5
15443a8 movsx edi, word ptr [rdi + 0x58]
15443ac call 0x14083caf0
15443b1 add rax, 0x28
15443b5 mov dword ptr [rbp - 8], edi
15443b8 mov qword ptr [rbp - 0x10], rax
15443bc lea rcx, [rbp - 0x10]
15443c0 cmp rcx, rsi
15443c3 je 0x1415443f5
15443c5 mov rcx, qword ptr [rsi]
15443c8 mov rax, qword ptr [rcx]
15443cb mov rdx, rsi
15443ce call qword ptr [rax + 0x10]
15443d1 mov rax, qword ptr [rbp - 0x10]
15443d5 mov rcx, qword ptr [rbp - 8]
15443d9 mov qword ptr [rsi + 8], rcx
15443dd mov qword ptr [rsi], rax
15443e0 call 0x14083caf0
15443e5 add rax, 8
15443e9 mov qword ptr [rbp - 8], 0
15443f1 mov qword ptr [rbp - 0x10], rax
15443f5 mov rbx, qword ptr [rax]
15443f8 lea rdx, [rbp - 0x10]
15443fc mov rcx, rax
15443ff call qword ptr [rbx + 0x10]
1544402 jmp 0x1415446d5
1544407 mov eax, dword ptr [rdi + 0x24]
154440a shl rax, 0x20
154440e movsxd rdi, dword ptr [rdi + 0x20]
1544412 or rdi, rax
1544415 call 0x14083caf0
154441a add rax, 0x48
154441e mov qword ptr [rbp - 8], rdi
1544422 mov qword ptr [rbp - 0x10], rax
1544426 lea rcx, [rbp - 0x10]
154442a cmp rcx, rsi
154442d je 0x14154445f
154442f mov rcx, qword ptr [rsi]
1544432 mov rax, qword ptr [rcx]
1544435 mov rdx, rsi
1544438 call qword ptr [rax + 0x10]
154443b mov rax, qword ptr [rbp - 0x10]
154443f mov rcx, qword ptr [rbp - 8]
1544443 mov qword ptr [rsi + 8], rcx
1544447 mov qword ptr [rsi], rax
154444a call 0x14083caf0
154444f add rax, 8
1544453 mov qword ptr [rbp - 8], 0
154445b mov qword ptr [rbp - 0x10], rax
154445f mov rdi, qword ptr [rax]
1544462 lea rdx, [rbp - 0x10]
1544466 mov rcx, rax
1544469 call qword ptr [rdi + 0x10]
154446c jmp 0x1415446d5
1544471 add rdi, 0x38
1544475 call 0x14083caf0
154447a lea rcx, [rbp - 8]
154447e mov qword ptr [rbp - 8], 0
1544486 cmp rcx, rdi
1544489 je 0x14154449b
154448b mov rcx, qword ptr [rdi]
154448e test rcx, rcx
1544491 je 0x141544497
1544493 lock inc dword ptr [rcx - 4]
1544497 mov qword ptr [rbp - 8], rcx
154449b add rax, 0x88
15444a1 mov qword ptr [rbp - 0x10], rax
15444a5 lea rcx, [rbp - 0x10]
15444a9 cmp rcx, rsi
15444ac je 0x1415444de
15444ae mov rcx, qword ptr [rsi]
15444b1 mov rax, qword ptr [rcx]
15444b4 mov rdx, rsi
15444b7 call qword ptr [rax + 0x10]
15444ba mov rax, qword ptr [rbp - 0x10]
15444be mov rcx, qword ptr [rbp - 8]
15444c2 mov qword ptr [rsi + 8], rcx
15444c6 mov qword ptr [rsi], rax
15444c9 call 0x14083caf0
15444ce add rax, 8
15444d2 mov qword ptr [rbp - 8], 0
15444da mov qword ptr [rbp - 0x10], rax
15444de mov rdi, qword ptr [rax]
15444e1 lea rdx, [rbp - 0x10]
15444e5 mov rcx, rax
15444e8 call qword ptr [rdi + 0x10]
15444eb jmp 0x1415446d5
15444f0 movsx edi, byte ptr [rdi + 0x5b]
15444f4 call 0x14083caf0
15444f9 add rax, 0x28
15444fd mov dword ptr [rbp - 8], edi
1544500 mov qword ptr [rbp - 0x10], rax
1544504 lea rcx, [rbp - 0x10]
1544508 cmp rcx, rsi
154450b je 0x14154453d
154450d mov rcx, qword ptr [rsi]
1544510 mov rax, qword ptr [rcx]
1544513 mov rdx, rsi
1544516 call qword ptr [rax + 0x10]
1544519 mov rax, qword ptr [rbp - 0x10]
154451d mov rcx, qword ptr [rbp - 8]
1544521 mov qword ptr [rsi + 8], rcx
1544525 mov qword ptr [rsi], rax
1544528 call 0x14083caf0
154452d add rax, 8
1544531 mov qword ptr [rbp - 8], 0
1544539 mov qword ptr [rbp - 0x10], rax
154453d mov rbx, qword ptr [rax]
1544540 lea rdx, [rbp - 0x10]
1544544 mov rcx, rax
1544547 call qword ptr [rbx + 0x10]
154454a jmp 0x1415446d5
154454f mov eax, dword ptr [rip + 0x61797b]
1544555 mov ecx, dword ptr [rip + 0x580e05]
154455b mov rdx, qword ptr gs:[0x58]
1544564 mov rcx, qword ptr [rdx + rcx*8]
1544568 cmp eax, dword ptr [rcx + 4]
154456e jg 0x141544735
1544574 movzx eax, word ptr [rdi + 0x44]
1544578 mov ecx, eax
154457a and ecx, 0x1ff
1544580 shl ecx, 8
1544583 movzx edx, word ptr [rdi + 0x46]
1544587 shr eax, 9
154458a shl edx, 0x11
154458d or edx, eax
154458f or edx, ecx
1544591 mov dword ptr [rbp - 8], edx
1544594 lea rcx, [rip + 0x617905]
154459b mov qword ptr [rbp - 0x10], rcx
154459f lea rax, [rbp - 0x10]
15445a3 cmp rax, rsi
15445a6 je 0x1415445db
15445a8 mov rcx, qword ptr [rsi]
15445ab mov rax, qword ptr [rcx]
15445ae mov rdx, rsi
15445b1 call qword ptr [rax + 0x10]
15445b4 mov rax, qword ptr [rbp - 0x10]
15445b8 mov rcx, qword ptr [rbp - 8]
15445bc mov qword ptr [rsi + 8], rcx
15445c0 mov qword ptr [rsi], rax
15445c3 call 0x14083caf0
15445c8 mov rcx, rax
15445cb add rcx, 8
15445cf mov qword ptr [rbp - 8], 0
15445d7 mov qword ptr [rbp - 0x10], rcx
15445db mov rax, qword ptr [rcx]
15445de lea rdx, [rbp - 0x10]
15445e2 call qword ptr [rax + 0x10]
15445e5 lea rax, [rip + 0x6154b4]
15445ec cmp rsi, rax
15445ef je 0x1415446d5
15445f5 movzx eax, word ptr [rdi + 0x44]
15445f9 and eax, 0x1ff
15445fe cmp ax, 1
1544602 jne 0x1415446d5
1544608 movzx eax, word ptr [rdi + 0x46]
154460c cmp eax, 0x76c
1544611 jne 0x1415446d5
1544617 mov rcx, qword ptr [rsi]
154461a mov rax, qword ptr [rcx]
154461d mov rdx, rsi
1544620 call qword ptr [rax + 0x10]
1544623 lea rdx, [rip + 0x615476]
154462a mov rcx, qword ptr [rip + 0x61546f]
1544631 mov rax, qword ptr [rcx]
1544634 mov r8, rsi
1544637 call qword ptr [rax + 0x18]
154463a jmp 0x1415446d5
154463f mov eax, dword ptr [rip + 0x61788b]
1544645 mov ecx, dword ptr [rip + 0x580d15]
154464b mov rdx, qword ptr gs:[0x58]
1544654 mov rcx, qword ptr [rdx + rcx*8]
1544658 cmp eax, dword ptr [rcx + 4]
154465e jg 0x141544777
1544664 movzx eax, word ptr [rdi + 0x48]
1544668 mov ecx, eax
154466a and ecx, 0x1ff
1544670 shl ecx, 8
1544673 movzx edx, word ptr [rdi + 0x4a]
1544677 shr eax, 9
154467a shl edx, 0x11
154467d or edx, eax
154467f or edx, ecx
1544681 mov dword ptr [rbp - 8], edx
1544684 lea rcx, [rip + 0x617815]
154468b mov qword ptr [rbp - 0x10], rcx
154468f lea rax, [rbp - 0x10]
1544693 cmp rax, rsi
1544696 je 0x1415446cb
1544698 mov rcx, qword ptr [rsi]
154469b mov rax, qword ptr [rcx]
154469e mov rdx, rsi
15446a1 call qword ptr [rax + 0x10]
15446a4 mov rax, qword ptr [rbp - 0x10]
15446a8 mov rcx, qword ptr [rbp - 8]
15446ac mov qword ptr [rsi + 8], rcx
15446b0 mov qword ptr [rsi], rax
15446b3 call 0x14083caf0
15446b8 mov rcx, rax
15446bb add rcx, 8
15446bf mov qword ptr [rbp - 8], 0
15446c7 mov qword ptr [rbp - 0x10], rcx
15446cb mov rax, qword ptr [rcx]
15446ce lea rdx, [rbp - 0x10]
15446d2 call qword ptr [rax + 0x10]
15446d5 mov al, 1
15446d7 add rsp, 0x38
15446db pop rbx
15446dc pop rdi
15446dd pop rsi
15446de pop rbp
15446df ret 
15446e0 mov rcx, rdi
15446e3 mov r8, rsi
15446e6 add rsp, 0x38
15446ea pop rbx
15446eb pop rdi
15446ec pop rsi
15446ed pop rbp
15446ee jmp 0x140fe3520
15446f3 lea rcx, [rip + 0x6177d6]
15446fa call 0x141750408
15446ff cmp dword ptr [rip + 0x6177ca], -1
1544706 jne 0x141544122
154470c lea rcx, [rip + 0x61778d]
1544713 call 0x140dbbfb0
1544718 lea rcx, [rip - 0x78870f]
154471f call 0x141750648
1544724 lea rcx, [rip + 0x6177a5]
154472b call 0x1417504a0
1544730 jmp 0x141544122
1544735 lea rcx, [rip + 0x617794]
154473c call 0x141750408
1544741 cmp dword ptr [rip + 0x617788], -1
1544748 jne 0x141544574
154474e lea rcx, [rip + 0x61774b]
1544755 call 0x140dbbfb0
154475a lea rcx, [rip - 0x788751]
1544761 call 0x141750648
1544766 lea rcx, [rip + 0x617763]
154476d call 0x1417504a0
1544772 jmp 0x141544574
1544777 lea rcx, [rip + 0x617752]
154477e call 0x141750408
1544783 cmp dword ptr [rip + 0x617746], -1
154478a jne 0x141544664
1544790 lea rcx, [rip + 0x617709]
1544797 call 0x140dbbfb0
154479c lea rcx, [rip - 0x788793]
15447a3 call 0x141750648
15447a8 lea rcx, [rip + 0x617721]
15447af call 0x1417504a0
15447b4 jmp 0x141544664
15447b9 nop dword ptr [rax]
15447c0 mov qword ptr [rsp + 0x10], rdx
15447c5 push rbp
15447c6 push rsi
15447c7 push rdi
15447c8 push rbx
15447c9 sub rsp, 0x28
15447cd lea rbp, [rdx + 0x30]
15447d1 call 0x141757f70
15447d6 int3 
15447d7 nop word ptr [rax + rax]
15447e0 mov qword ptr [rsp + 0x10], rdx
15447e5 push rbp
15447e6 push rsi
15447e7 push rdi
15447e8 push rbx
15447e9 sub rsp, 0x28
15447ed lea rbp, [rdx + 0x30]
15447f1 call 0x141757f70
15447f6 int3 
15447f7 nop word ptr [rax + rax]
1544800 mov qword ptr [rsp + 0x10], rdx
1544805 push rbp
1544806 push rsi
1544807 push rdi
1544808 push rbx
1544809 sub rsp, 0x28
154480d lea rbp, [rdx + 0x30]
1544811 call 0x141757f70
1544816 int3 
1544817 nop word ptr [rax + rax]
1544820 mov qword ptr [rsp + 0x10], rdx
1544825 push rbp
1544826 push rsi
1544827 push rdi
1544828 push rbx
1544829 sub rsp, 0x28
154482d lea rbp, [rdx + 0x30]
1544831 call 0x141757f70
1544836 int3 
1544837 nop word ptr [rax + rax]
1544840 mov qword ptr [rsp + 0x10], rdx
1544845 push rbp
1544846 push rsi
1544847 push rdi
1544848 push rbx
1544849 sub rsp, 0x28
154484d lea rbp, [rdx + 0x30]
1544851 call 0x141757f70
1544856 int3 
1544857 nop word ptr [rax + rax]
1544860 mov qword ptr [rsp + 0x10], rdx
1544865 push rbp
1544866 push rsi
1544867 push rdi
1544868 push rbx
1544869 sub rsp, 0x28
154486d lea rbp, [rdx + 0x30]
1544871 call 0x141757f70
1544876 int3 
1544877 nop word ptr [rax + rax]
1544880 mov qword ptr [rsp + 0x10], rdx
1544885 push rbp
1544886 push rsi
1544887 push rdi
1544888 push rbx
1544889 sub rsp, 0x28
154488d lea rbp, [rdx + 0x30]
1544891 call 0x141757f70
1544896 int3 
1544897 nop word ptr [rax + rax]
15448a0 mov qword ptr [rsp + 0x10], rdx
15448a5 push rbp
15448a6 push rsi
15448a7 push rdi
15448a8 push rbx
15448a9 sub rsp, 0x28
15448ad lea rbp, [rdx + 0x30]
15448b1 call 0x141757f70
15448b6 int3 
15448b7 nop word ptr [rax + rax]
15448c0 mov qword ptr [rsp + 0x10], rdx
15448c5 push rbp
15448c6 push rsi
15448c7 push rdi
15448c8 push rbx
15448c9 sub rsp, 0x28
15448cd lea rbp, [rdx + 0x30]
15448d1 call 0x141757f70
15448d6 int3 
15448d7 nop word ptr [rax + rax]
15448e0 mov qword ptr [rsp + 0x10], rdx
15448e5 push rbp
15448e6 push rsi
15448e7 push rdi
15448e8 push rbx
15448e9 sub rsp, 0x28
15448ed lea rbp, [rdx + 0x30]
15448f1 call 0x141757f70
15448f6 int3 
15448f7 nop word ptr [rax + rax]
1544900 mov qword ptr [rsp + 0x10], rdx
1544905 push rbp
1544906 push rsi
1544907 push rdi
1544908 push rbx
1544909 sub rsp, 0x28
154490d lea rbp, [rdx + 0x30]
1544911 call 0x141757f70
1544916 int3 
1544917 nop word ptr [rax + rax]
1544920 mov qword ptr [rsp + 0x10], rdx
1544925 push rbp
1544926 push rsi
1544927 push rdi
1544928 push rbx
1544929 sub rsp, 0x28
154492d lea rbp, [rdx + 0x30]
1544931 call 0x141757f70
1544936 int3 
1544937 nop word ptr [rax + rax]
1544940 mov qword ptr [rsp + 0x10], rdx
1544945 push rbp
1544946 push rsi
1544947 push rdi
1544948 push rbx
1544949 sub rsp, 0x28
154494d lea rbp, [rdx + 0x30]
1544951 call 0x141757f70
1544956 int3 
1544957 nop word ptr [rax + rax]
1544960 mov qword ptr [rsp + 0x10], rdx
1544965 push rbp
1544966 push rsi
1544967 push rdi
1544968 push rbx
1544969 sub rsp, 0x28
154496d lea rbp, [rdx + 0x30]
1544971 call 0x141757f70
1544976 int3 
1544977 nop word ptr [rax + rax]
1544980 mov qword ptr [rsp + 0x10], rdx
1544985 push rbp
1544986 push rsi
1544987 push rdi
1544988 push rbx
1544989 sub rsp, 0x28
154498d lea rbp, [rdx + 0x30]
1544991 call 0x141757f70
1544996 int3 
1544997 nop word ptr [rax + rax]
15449a0 mov qword ptr [rsp + 0x10], rdx
15449a5 push rbp
15449a6 push rsi
15449a7 push rdi
15449a8 push rbx
15449a9 sub rsp, 0x28
15449ad lea rbp, [rdx + 0x30]
15449b1 call 0x141757f70
15449b6 int3 
15449b7 nop word ptr [rax + rax]
15449c0 mov qword ptr [rsp + 0x10], rdx
15449c5 push rbp
15449c6 push rsi
15449c7 push rdi
15449c8 push rbx
15449c9 sub rsp, 0x28
15449cd lea rbp, [rdx + 0x30]
15449d1 call 0x141757f70
15449d6 int3 
15449d7 nop word ptr [rax + rax]
15449e0 mov qword ptr [rsp + 0x10], rdx
15449e5 push rbp
15449e6 push rsi
15449e7 push rdi
15449e8 push rbx
15449e9 sub rsp, 0x28
15449ed lea rbp, [rdx + 0x30]
15449f1 call 0x141757f70
15449f6 int3 
15449f7 nop word ptr [rax + rax]
1544a00 mov qword ptr [rsp + 0x10], rdx
1544a05 push rbp
1544a06 push rsi
1544a07 push rdi
1544a08 push rbx
1544a09 sub rsp, 0x28
1544a0d lea rbp, [rdx + 0x30]
1544a11 call 0x141757f70
1544a16 int3 
1544a17 nop word ptr [rax + rax]
1544a20 mov qword ptr [rsp + 0x10], rdx
1544a25 push rbp
1544a26 push rsi
1544a27 push rdi
1544a28 push rbx
1544a29 sub rsp, 0x28
1544a2d lea rbp, [rdx + 0x30]
1544a31 call 0x141757f70
1544a36 int3 
1544a37 nop word ptr [rax + rax]
1544a40 mov qword ptr [rsp + 0x10], rdx
1544a45 push rbp
1544a46 push rsi
1544a47 push rdi
1544a48 push rbx
1544a49 sub rsp, 0x28
1544a4d lea rbp, [rdx + 0x30]
1544a51 call 0x141757f70
1544a56 int3 
1544a57 nop word ptr [rax + rax]
1544a60 mov qword ptr [rsp + 0x10], rdx
1544a65 push rbp
1544a66 push rsi
1544a67 push rdi
1544a68 push rbx
1544a69 sub rsp, 0x28
1544a6d lea rbp, [rdx + 0x30]
1544a71 call 0x141757f70
1544a76 int3 
1544a77 nop word ptr [rax + rax]
1544a80 mov qword ptr [rsp + 0x10], rdx
1544a85 push rbp
1544a86 push rsi
1544a87 push rdi
1544a88 push rbx
1544a89 sub rsp, 0x28
1544a8d lea rbp, [rdx + 0x30]
1544a91 call 0x141757f70
1544a96 int3 
1544a97 nop word ptr [rax + rax]
1544aa0 mov qword ptr [rsp + 0x10], rdx
1544aa5 push rbp
1544aa6 push rsi
1544aa7 push rdi
1544aa8 push rbx
1544aa9 sub rsp, 0x28
1544aad lea rbp, [rdx + 0x30]
1544ab1 call 0x141757f70
1544ab6 int3 
1544ab7 nop word ptr [rax + rax]
1544ac0 mov qword ptr [rsp + 0x10], rdx
1544ac5 push rbp
1544ac6 push rsi
1544ac7 push rdi
1544ac8 push rbx
1544ac9 sub rsp, 0x28
1544acd lea rbp, [rdx + 0x30]
1544ad1 call 0x141757f70
1544ad6 int3 
1544ad7 nop word ptr [rax + rax]
1544ae0 mov qword ptr [rsp + 0x10], rdx
1544ae5 push rbp
1544ae6 push rsi
1544ae7 push rdi
1544ae8 push rbx
1544ae9 sub rsp, 0x28
1544aed lea rbp, [rdx + 0x30]
1544af1 call 0x141757f70
1544af6 int3 
1544af7 nop word ptr [rax + rax]
1544b00 mov qword ptr [rsp + 0x10], rdx
1544b05 push rbp
1544b06 push rsi
1544b07 push rdi
1544b08 push rbx
1544b09 sub rsp, 0x28
1544b0d lea rbp, [rdx + 0x30]
1544b11 call 0x141757f70
1544b16 int3 
1544b17 nop word ptr [rax + rax]
1544b20 mov qword ptr [rsp + 0x10], rdx
1544b25 push rbp
1544b26 push rsi
1544b27 push rdi
1544b28 push rbx
1544b29 sub rsp, 0x28
1544b2d lea rbp, [rdx + 0x30]
1544b31 call 0x141757f70
1544b36 int3 
1544b37 nop word ptr [rax + rax]
1544b40 mov qword ptr [rsp + 0x10], rdx
1544b45 push rbp
1544b46 push rsi
1544b47 push rdi
1544b48 push rbx
1544b49 sub rsp, 0x28
1544b4d lea rbp, [rdx + 0x30]
1544b51 call 0x141757f70
1544b56 int3 
1544b57 nop word ptr [rax + rax]
1544b60 mov qword ptr [rsp + 0x10], rdx
1544b65 push rbp
1544b66 push rsi
1544b67 push rdi
1544b68 push rbx
1544b69 sub rsp, 0x28
1544b6d lea rbp, [rdx + 0x30]
1544b71 call 0x141757f70
1544b76 int3 
1544b77 nop word ptr [rax + rax]
1544b80 mov qword ptr [rsp + 0x10], rdx
1544b85 push rbp
1544b86 push rsi
1544b87 push rdi
1544b88 push rbx
1544b89 sub rsp, 0x28
1544b8d lea rbp, [rdx + 0x30]
1544b91 call 0x141757f70
1544b96 int3 
1544b97 nop word ptr [rax + rax]
1544ba0 mov qword ptr [rsp + 0x10], rdx
1544ba5 push rbp
1544ba6 push rsi
1544ba7 push rdi
1544ba8 push rbx
1544ba9 sub rsp, 0x28
1544bad lea rbp, [rdx + 0x30]
1544bb1 call 0x141757f70
1544bb6 int3 
1544bb7 nop word ptr [rax + rax]
1544bc0 mov qword ptr [rsp + 0x10], rdx
1544bc5 push rbp
1544bc6 push rsi
1544bc7 push rdi
1544bc8 push rbx
1544bc9 sub rsp, 0x28
1544bcd lea rbp, [rdx + 0x30]
1544bd1 call 0x141757f70
1544bd6 int3 
1544bd7 nop word ptr [rax + rax]
1544be0 mov qword ptr [rsp + 0x10], rdx
1544be5 push rbp
1544be6 push rsi
1544be7 push rdi
1544be8 push rbx
1544be9 sub rsp, 0x28
1544bed lea rbp, [rdx + 0x30]
1544bf1 call 0x141757f70
1544bf6 int3 
1544bf7 nop word ptr [rax + rax]
1544c00 mov qword ptr [rsp + 0x10], rdx
1544c05 push rbp
1544c06 push rsi
1544c07 push rdi
1544c08 push rbx
1544c09 sub rsp, 0x28
1544c0d lea rbp, [rdx + 0x30]
1544c11 call 0x141757f70
1544c16 int3 
1544c17 nop word ptr [rax + rax]
1544c20 mov qword ptr [rsp + 0x10], rdx
1544c25 push rbp
1544c26 push rsi
1544c27 push rdi
1544c28 push rbx
1544c29 sub rsp, 0x28
1544c2d lea rbp, [rdx + 0x30]
1544c31 call 0x141757f70
1544c36 int3 
1544c37 nop word ptr [rax + rax]
1544c40 mov qword ptr [rsp + 0x10], rdx
1544c45 push rbp
1544c46 push rsi
1544c47 push rdi
1544c48 push rbx
1544c49 sub rsp, 0x28
1544c4d lea rbp, [rdx + 0x30]
1544c51 call 0x141757f70
1544c56 int3 
1544c57 nop word ptr [rax + rax]
1544c60 mov qword ptr [rsp + 0x10], rdx
1544c65 push rbp
1544c66 push rsi
1544c67 push rdi
1544c68 push rbx
1544c69 sub rsp, 0x28
1544c6d lea rbp, [rdx + 0x30]
1544c71 call 0x141757f70
1544c76 int3 
1544c77 int3 
1544c78 int3 
1544c79 int3 
1544c7a int3 
1544c7b int3 
1544c7c int3 
1544c7d int3 
1544c7e int3 
1544c7f int3 
1544c80 push rsi
1544c81 push rdi
1544c82 push rbx
1544c83 sub rsp, 0x30
1544c87 mov rdi, r8
1544c8a mov ebx, edx
1544c8c mov rsi, rcx
1544c8f call 0x140fe1d00
1544c94 test al, al
1544c96 je 0x141544ca2
1544c98 mov al, 1
1544c9a add rsp, 0x30
1544c9e pop rbx
1544c9f pop rdi
1544ca0 pop rsi
1544ca1 ret 
1544ca2 xor eax, eax
1544ca4 cmp ebx, 0x696e666e
1544caa jg 0x141544cff
1544cac cmp ebx, 0x656e6473
1544cb2 jg 0x141544d4f
1544cb8 cmp ebx, 0x63617367
1544cbe jle 0x141544dfc
1544cc4 cmp ebx, 0x63617368
1544cca je 0x141544f55
1544cd0 cmp ebx, 0x636e7374
1544cd6 je 0x141544f69
1544cdc cmp ebx, 0x636f6d70
1544ce2 jne 0x141544c9a
1544ce4 lea rcx, [rsp + 0x28]
1544ce9 mov rdx, rdi
1544cec xor r8d, r8d
1544cef call 0x140fe6f60
1544cf4 mov rax, qword ptr [rsp + 0x28]
1544cf9 mov qword ptr [rsi + 0x30], rax
1544cfd jmp 0x141544c98
1544cff cmp ebx, 0x73746461
1544d05 jg 0x141544dae
1544d0b cmp ebx, 0x6f746873
1544d11 jle 0x141544e43
1544d17 cmp ebx, 0x6f746874
1544d1d je 0x141544f86
1544d23 cmp ebx, 0x72617469
1544d29 je 0x141544fa4
1544d2f cmp ebx, 0x72726561
1544d35 jne 0x141544c9a
1544d3b mov rcx, qword ptr [rdi]
1544d3e mov rax, qword ptr [rcx]
1544d41 mov rdx, rdi
1544d44 call qword ptr [rax + 0x40]
1544d47 mov byte ptr [rsi + 0x5c], al
1544d4a jmp 0x141544c98
1544d4f cmp ebx, 0x66736773
1544d55 jle 0x141544e8a
1544d5b cmp ebx, 0x66736774
1544d61 je 0x141544fb8
1544d67 cmp ebx, 0x67616d73
1544d6d je 0x141544f40
1544d73 cmp ebx, 0x676f6c73
1544d79 jne 0x141544c9a
1544d7f mov rcx, qword ptr [rdi]
1544d82 mov rax, qword ptr [rcx]
1544d85 mov rdx, rdi
1544d88 call qword ptr [rax + 0x40]
1544d8b mov word ptr [rsi + 0x56], ax
1544d8f mov rcx, qword ptr [rdi]
1544d92 mov rax, qword ptr [rcx]
1544d95 mov rdx, rdi
1544d98 call qword ptr [rax + 8]
1544d9b test al, al
1544d9d jne 0x141544c98
1544da3 mov word ptr [rsi + 0x56], 0xffff
1544da9 jmp 0x141544c98
1544dae cmp ebx, 0x73746963
1544db4 jle 0x141544eb6
1544dba cmp ebx, 0x7465616d
1544dc0 je 0x141544fcd
1544dc6 cmp ebx, 0x73746e6d
1544dcc je 0x141544feb
1544dd2 cmp ebx, 0x73746964
1544dd8 jne 0x141544c9a
1544dde lea rcx, [rsp + 0x28]
1544de3 mov rdx, rdi
1544de6 xor r8d, r8d
1544de9 call 0x140fe6f60
1544dee mov rax, qword ptr [rsp + 0x28]
1544df3 mov qword ptr [rsi + 0x18], rax
1544df7 jmp 0x141544c98
1544dfc cmp ebx, 0x61707073
1544e02 je 0x141544f40
1544e08 cmp ebx, 0x61747465
1544e0e jne 0x141544c9a
1544e14 mov rcx, qword ptr [rdi]
1544e17 mov rax, qword ptr [rcx]
1544e1a mov rdx, rdi
1544e1d call qword ptr [rax + 0x40]
1544e20 mov dword ptr [rsi + 0x50], eax
1544e23 mov rcx, qword ptr [rdi]
1544e26 mov rax, qword ptr [rcx]
1544e29 mov rdx, rdi
1544e2c call qword ptr [rax + 8]
1544e2f test al, al
1544e31 jne 0x141544c98
1544e37 mov dword ptr [rsi + 0x50], 0xffffffff
1544e3e jmp 0x141544c98
1544e43 cmp ebx, 0x696e666f
1544e49 je 0x141545036
1544e4f cmp ebx, 0x6f676c73
1544e55 jne 0x141544c9a
1544e5b mov rcx, qword ptr [rdi]
1544e5e mov rax, qword ptr [rcx]
1544e61 mov rdx, rdi
1544e64 call qword ptr [rax + 0x40]
1544e67 mov word ptr [rsi + 0x58], ax
1544e6b mov rcx, qword ptr [rdi]
1544e6e mov rax, qword ptr [rcx]
1544e71 mov rdx, rdi
1544e74 call qword ptr [rax + 8]
1544e77 test al, al
1544e79 jne 0x141544c98
1544e7f mov word ptr [rsi + 0x58], 0xffff
1544e85 jmp 0x141544c98
1544e8a cmp ebx, 0x656e6474
1544e90 je 0x14154504a
1544e96 cmp ebx, 0x6574696e
1544e9c jne 0x141544c9a
1544ea2 mov rcx, qword ptr [rdi]
1544ea5 mov rax, qword ptr [rcx]
1544ea8 mov rdx, rdi
1544eab call qword ptr [rax + 0x40]
1544eae mov byte ptr [rsi + 0x5d], al
1544eb1 jmp 0x141544c98
1544eb6 cmp ebx, 0x73746462
1544ebc je 0x1415450bc
1544ec2 cmp ebx, 0x73746474
1544ec8 jne 0x141544c9a
1544ece mov eax, dword ptr [rip + 0x616ffc]
1544ed4 mov ecx, dword ptr [rip + 0x580486]
1544eda mov rdx, qword ptr gs:[0x58]
1544ee3 mov rcx, qword ptr [rdx + rcx*8]
1544ee7 cmp eax, dword ptr [rcx + 4]
1544eed jg 0x141545326
1544ef3 mov rcx, qword ptr [rdi]
1544ef6 lea rax, [rip + 0x616fa3]
1544efd cmp rcx, rax
1544f00 je 0x1415451a6
1544f06 mov rax, qword ptr [rcx]
1544f09 mov rdx, rdi
1544f0c call qword ptr [rax + 8]
1544f0f cmp al, 0x1b
1544f11 jne 0x1415451ca
1544f17 mov rcx, qword ptr [rdi]
1544f1a mov rax, qword ptr [rcx]
1544f1d lea rbx, [rsp + 0x28]
1544f22 mov rdx, rbx
1544f25 mov r8, rdi
1544f28 call qword ptr [rax + 0xa0]
1544f2e lea rcx, [rsp + 0x20]
1544f33 mov rdx, rbx
1544f36 call 0x1413c9e30
1544f3b jmp 0x1415451d2
1544f40 mov rcx, qword ptr [rdi]
1544f43 mov rax, qword ptr [rcx]
1544f46 mov rdx, rdi
1544f49 call qword ptr [rax + 0x40]
1544f4c mov word ptr [rsi + 0x54], ax
1544f50 jmp 0x141544c98
1544f55 mov rcx, qword ptr [rdi]
1544f58 mov rax, qword ptr [rcx]
1544f5b mov rdx, rdi
1544f5e call qword ptr [rax + 0x40]
1544f61 mov dword ptr [rsi + 0x50], eax
1544f64 jmp 0x141544c98
1544f69 mov rcx, qword ptr [rdi]
1544f6c mov rax, qword ptr [rcx]
1544f6f mov rdx, rdi
1544f72 call qword ptr [rax + 0x30]
1544f75 test al, al
1544f77 je 0x14154512e
1544f7d mov byte ptr [rsi + 0x5d], 1
1544f81 jmp 0x141544c98
1544f86 lea rcx, [rsp + 0x28]
1544f8b mov rdx, rdi
1544f8e xor r8d, r8d
1544f91 call 0x140fe6f60
1544f96 mov rax, qword ptr [rsp + 0x28]
1544f9b mov qword ptr [rsi + 0x28], rax
1544f9f jmp 0x141544c98
1544fa4 mov rcx, qword ptr [rdi]
1544fa7 mov rax, qword ptr [rcx]
1544faa mov rdx, rdi
1544fad call qword ptr [rax + 0x40]
1544fb0 mov byte ptr [rsi + 0x5a], al
1544fb3 jmp 0x141544c98
1544fb8 mov rcx, qword ptr [rdi]
1544fbb mov rax, qword ptr [rcx]
1544fbe mov rdx, rdi
1544fc1 call qword ptr [rax + 0x40]
1544fc4 mov word ptr [rsi + 0x58], ax
1544fc8 jmp 0x141544c98
1544fcd lea rcx, [rsp + 0x28]
1544fd2 mov rdx, rdi
1544fd5 xor r8d, r8d
1544fd8 call 0x140fe6f60
1544fdd mov rax, qword ptr [rsp + 0x28]
1544fe2 mov qword ptr [rsi + 0x20], rax
1544fe6 jmp 0x141544c98
1544feb mov rcx, qword ptr [rdi]
1544fee mov rax, qword ptr [rcx]
1544ff1 lea rdx, [rsp + 0x28]
1544ff6 mov r8, rdi
1544ff9 call qword ptr [rax + 0x80]
1544fff mov rcx, qword ptr [rsi + 0x38]
1545003 cmp rcx, qword ptr [rsp + 0x28]
1545008 je 0x141545137
154500e lea rax, [rcx - 4]
1545012 test rcx, rcx
1545015 cmove rax, rcx
1545019 je 0x141545028
154501b lock dec dword ptr [rax]
154501e jne 0x141545028
1545020 mov rcx, rax
1545023 call 0x1412ebfa0
1545028 mov rax, qword ptr [rsp + 0x28]
154502d mov qword ptr [rsi + 0x38], rax
1545031 jmp 0x141544c98
1545036 mov rcx, qword ptr [rdi]
1545039 mov rax, qword ptr [rcx]
154503c mov rdx, rdi
154503f call qword ptr [rax + 0x40]
1545042 mov byte ptr [rsi + 0x5b], al
1545045 jmp 0x141544c98
154504a mov eax, dword ptr [rip + 0x616e80]
1545050 mov ecx, dword ptr [rip + 0x58030a]
1545056 mov rdx, qword ptr gs:[0x58]
154505f mov rcx, qword ptr [rdx + rcx*8]
1545063 cmp eax, dword ptr [rcx + 4]
1545069 jg 0x141545368
154506f mov rcx, qword ptr [rdi]
1545072 lea rax, [rip + 0x616e27]
1545079 cmp rcx, rax
154507c je 0x141545158
1545082 mov rax, qword ptr [rcx]
1545085 mov rdx, rdi
1545088 call qword ptr [rax + 8]
154508b cmp al, 0x1b
154508d jne 0x14154526e
1545093 mov rcx, qword ptr [rdi]
1545096 mov rax, qword ptr [rcx]
1545099 lea rbx, [rsp + 0x28]
154509e mov rdx, rbx
15450a1 mov r8, rdi
15450a4 call qword ptr [rax + 0xa0]
15450aa lea rcx, [rsp + 0x20]
15450af mov rdx, rbx
15450b2 call 0x1413c9e30
15450b7 jmp 0x141545276
15450bc mov eax, dword ptr [rip + 0x616e0e]
15450c2 mov ecx, dword ptr [rip + 0x580298]
15450c8 mov rdx, qword ptr gs:[0x58]
15450d1 mov rcx, qword ptr [rdx + rcx*8]
15450d5 cmp eax, dword ptr [rcx + 4]
15450db jg 0x1415453aa
15450e1 mov rcx, qword ptr [rdi]
15450e4 lea rax, [rip + 0x616db5]
15450eb cmp rcx, rax
15450ee je 0x14154517f
15450f4 mov rax, qword ptr [rcx]
15450f7 mov rdx, rdi
15450fa call qword ptr [rax + 8]
15450fd cmp al, 0x1b
15450ff jne 0x141545312
1545105 mov rcx, qword ptr [rdi]
1545108 mov rax, qword ptr [rcx]
154510b lea rbx, [rsp + 0x28]
1545110 mov rdx, rbx
1545113 mov r8, rdi
1545116 call qword ptr [rax + 0xa0]
154511c lea rcx, [rsp + 0x20]
1545121 mov rdx, rbx
1545124 call 0x1413c9e30
1545129 jmp 0x14154531a
154512e mov byte ptr [rsi + 0x5d], 0
1545132 jmp 0x141544c98
1545137 test rcx, rcx
154513a je 0x141544c98
1545140 lock dec dword ptr [rcx - 4]
1545144 jne 0x141544c98
154514a add rcx, -4
154514e call 0x1412ebfa0
1545153 jmp 0x141544c98
1545158 mov eax, dword ptr [rdi + 8]
154515b mov ecx, eax
154515d shr ecx, 0x11
1545160 mov word ptr [rsp + 0x22], cx
1545165 mov ecx, eax
1545167 shr ecx, 8
154516a and ecx, 0x1ff
1545170 shl eax, 9
1545173 or eax, ecx
1545175 mov word ptr [rsp + 0x20], ax
154517a jmp 0x141545276
154517f mov eax, dword ptr [rdi + 8]
1545182 mov ecx, eax
1545184 shr ecx, 0x11
1545187 mov word ptr [rsp + 0x22], cx
154518c mov ecx, eax
154518e shr ecx, 8
1545191 and ecx, 0x1ff
1545197 shl eax, 9
154519a or eax, ecx
154519c mov word ptr [rsp + 0x20], ax
15451a1 jmp 0x14154531a
15451a6 mov eax, dword ptr [rdi + 8]
15451a9 mov ecx, eax
15451ab shr ecx, 0x11
15451ae mov word ptr [rsp + 0x22], cx
15451b3 mov ecx, eax
15451b5 shr ecx, 8
15451b8 and ecx, 0x1ff
15451be shl eax, 9
15451c1 or eax, ecx
15451c3 mov word ptr [rsp + 0x20], ax
15451c8 jmp 0x1415451d2
15451ca mov dword ptr [rsp + 0x20], 0x76c0001
15451d2 mov eax, dword ptr [rsp + 0x20]
15451d6 mov dword ptr [rsi + 0x40], eax
15451d9 mov rcx, qword ptr [rdi]
15451dc mov rax, qword ptr [rcx]
15451df mov rdx, rdi
15451e2 call qword ptr [rax + 8]
15451e5 test al, al
15451e7 je 0x141544c98
15451ed movzx eax, word ptr [rsi + 0x40]
15451f1 mov ecx, eax
15451f3 and ecx, 0x1ff
15451f9 cmp cx, 1
15451fd jne 0x141544c98
1545203 movzx ecx, word ptr [rsi + 0x42]
1545207 cmp ecx, 0x76c
154520d jne 0x141544c98
1545213 movzx ecx, word ptr [rip + 0x56a646]
154521a cmp ecx, 0x7e8
1545220 jb 0x14154522f
1545222 mov word ptr [rip + 0x56a635], 0x7e7
154522b mov cx, 0x7e7
154522f movzx edx, cx
1545232 imul ecx, ecx, 0x5c29
1545238 movzx ecx, cx
154523b cmp ecx, 0xa3e
1545241 mov ecx, 0xf
1545246 mov ebx, 3
154524b cmovb ebx, ecx
154524e mov word ptr [rsi + 0x42], dx
1545252 xor ecx, ecx
1545254 test ebx, edx
1545256 sete cl
1545259 and eax, 0xfffffe00
154525e lea eax, [rcx + rax + 0xb6]
1545265 mov word ptr [rsi + 0x40], ax
1545269 jmp 0x141544c98
154526e mov dword ptr [rsp + 0x20], 0x76c0001
1545276 mov eax, dword ptr [rsp + 0x20]
154527a mov dword ptr [rsi + 0x44], eax
154527d mov rcx, qword ptr [rdi]
1545280 mov rax, qword ptr [rcx]
1545283 mov rdx, rdi
1545286 call qword ptr [rax + 8]
1545289 test al, al
154528b je 0x141544c98
1545291 movzx eax, word ptr [rsi + 0x44]
1545295 mov ecx, eax
1545297 and ecx, 0x1ff
154529d cmp cx, 1
15452a1 jne 0x141544c98
15452a7 movzx ecx, word ptr [rsi + 0x46]
15452ab cmp ecx, 0x76c
15452b1 jne 0x141544c98
15452b7 movzx ecx, word ptr [rip + 0x56a5a2]
15452be cmp ecx, 0x7e8
15452c4 jb 0x1415452d3
15452c6 mov word ptr [rip + 0x56a591], 0x7e7
15452cf mov cx, 0x7e7
15452d3 movzx edx, cx
15452d6 imul ecx, ecx, 0x5c29
15452dc movzx ecx, cx
15452df cmp ecx, 0xa3e
15452e5 mov ecx, 0xf
15452ea mov ebx, 3
15452ef cmovb ebx, ecx
15452f2 mov word ptr [rsi + 0x46], dx
15452f6 xor ecx, ecx
15452f8 test ebx, edx
15452fa sete cl
15452fd and eax, 0xfffffe00
1545302 lea eax, [rcx + rax + 0xb6]
1545309 mov word ptr [rsi + 0x44], ax
154530d jmp 0x141544c98
1545312 mov dword ptr [rsp + 0x20], 0x76c0001
154531a mov eax, dword ptr [rsp + 0x20]
154531e mov dword ptr [rsi + 0x48], eax
1545321 jmp 0x141544c98
1545326 lea rcx, [rip + 0x616ba3]
154532d call 0x141750408
1545332 cmp dword ptr [rip + 0x616b97], -1
1545339 jne 0x141544ef3
154533f lea rcx, [rip + 0x616b5a]
1545346 call 0x140dbbfb0
154534b lea rcx, [rip - 0x789342]
1545352 call 0x141750648
1545357 lea rcx, [rip + 0x616b72]
154535e call 0x1417504a0
1545363 jmp 0x141544ef3
1545368 lea rcx, [rip + 0x616b61]
154536f call 0x141750408
1545374 cmp dword ptr [rip + 0x616b55], -1
154537b jne 0x14154506f
1545381 lea rcx, [rip + 0x616b18]
1545388 call 0x140dbbfb0
154538d lea rcx, [rip - 0x789384]
1545394 call 0x141750648
1545399 lea rcx, [rip + 0x616b30]
15453a0 call 0x1417504a0
15453a5 jmp 0x14154506f
15453aa lea rcx, [rip + 0x616b1f]
15453b1 call 0x141750408
15453b6 cmp dword ptr [rip + 0x616b13], -1
15453bd jne 0x1415450e1
15453c3 lea rcx, [rip + 0x616ad6]
15453ca call 0x140dbbfb0
15453cf lea rcx, [rip - 0x7893c6]
15453d6 call 0x141750648
15453db lea rcx, [rip + 0x616aee]
15453e2 call 0x1417504a0
15453e7 jmp 0x1415450e1
15453ec int3 
15453ed int3 
15453ee int3 
15453ef int3 
15453f0 jmp 0x1444e46d0
15453f5 jmp 0x1416dfdef
15453fa xor eax, 0xc80126b5
15453ff jp 0x1418791c6
1545406 movabs al, byte ptr [0xf38015434a8e91f]
154540f cmp byte ptr [rsi], 0
1545412 sbb byte ptr [rax], al
1545414 mov bh, 0x9a
1545416 jmp 0x141975e16
154541b scasd eax, dword ptr [rdi]
154541c je 0x141c888e2
1545422 retf 0x482c
1545425 jg 0x141545472
1545427 add byte ptr [rax + 0x70], ch
154542a ret 0xf178
154542d push rsp
154542e sahf 
154542f jmp 0x14179d853
1545434 jmp 0x141579ad2
1545439 fidiv word ptr [rbx - 0x72f316a2]
154543f xor eax, 0xa1756601
1545444 xor eax, 0xb3868e0f
154544a adc eax, dword ptr [rax]
154544c jmp 0x141cce76d
1545451 jge 0x141545435
1545453 jmp 0x141798131
1545458 push rsi
1545459 cdq 
154545a jnp 0x141cc47ca
1545460 adc al, 0xf
1545462 mov byte ptr [rdx], cl
1545464 jns 0x1415454b8
1545466 add edi, esp
1545468 int3 
1545469 jmp 0x142433a41
154546e ror dword ptr [rdi], 1
1545470 adc dword ptr [rdx + 0x70], -9
1545474 add byte ptr [rdx + 0x45], cl