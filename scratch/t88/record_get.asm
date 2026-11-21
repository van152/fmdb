1415446a0 55 push rbp
1415446a1 56 push rsi
1415446a2 57 push rdi
1415446a3 53 push rbx
1415446a4 4883ec38 sub rsp, 0x38
1415446a8 488d6c2430 lea rbp, [rsp + 0x30]
1415446ad 48c74500feffffff mov qword ptr [rbp], 0xfffffffffffffffe
1415446b5 4c89c6 mov rsi, r8
1415446b8 4889cf mov rdi, rcx
1415446bb 81fa6e666e69 cmp edx, 0x696e666e
1415446c1 0f8fa6000000 jg 0x14154476d
1415446c7 81fa73646e65 cmp edx, 0x656e6473
1415446cd 0f8f35010000 jg 0x141544808
1415446d3 81fa67736163 cmp edx, 0x63617367
1415446d9 0f8e6d020000 jle 0x14154494c
1415446df 81fa68736163 cmp edx, 0x63617368
1415446e5 0f8433050000 je 0x141544c1e
1415446eb 81fa74736e63 cmp edx, 0x636e7374
1415446f1 0f8485050000 je 0x141544c7c
1415446f7 81fa706d6f63 cmp edx, 0x636f6d70
1415446fd 0f85dd090000 jne 0x1415450e0
141544703 8b4734 mov eax, dword ptr [rdi + 0x34]
141544706 48c1e020 shl rax, 0x20
14154470a 48637f30 movsxd rdi, dword ptr [rdi + 0x30]
14154470e 4809c7 or rdi, rax
141544711 e8da8d2fff call 0x14083d4f0
141544716 4883c048 add rax, 0x48
14154471a 48897df8 mov qword ptr [rbp - 8], rdi
14154471e 488945f0 mov qword ptr [rbp - 0x10], rax
141544722 488d4df0 lea rcx, [rbp - 0x10]
141544726 4839f1 cmp rcx, rsi
141544729 7430 je 0x14154475b
14154472b 488b0e mov rcx, qword ptr [rsi]
14154472e 488b01 mov rax, qword ptr [rcx]
141544731 4889f2 mov rdx, rsi
141544734 ff5010 call qword ptr [rax + 0x10]
141544737 488b45f0 mov rax, qword ptr [rbp - 0x10]
14154473b 488b4df8 mov rcx, qword ptr [rbp - 8]
14154473f 48894e08 mov qword ptr [rsi + 8], rcx
141544743 488906 mov qword ptr [rsi], rax
141544746 e8a58d2fff call 0x14083d4f0
14154474b 4883c008 add rax, 8
14154474f 48c745f800000000 mov qword ptr [rbp - 8], 0
141544757 488945f0 mov qword ptr [rbp - 0x10], rax
14154475b 488b18 mov rbx, qword ptr [rax]
14154475e 488d55f0 lea rdx, [rbp - 0x10]
141544762 4889c1 mov rcx, rax
141544765 ff5310 call qword ptr [rbx + 0x10]
141544768 e968090000 jmp 0x1415450d5
14154476d 81fa61647473 cmp edx, 0x73746461
141544773 0f8f39010000 jg 0x1415448b2
141544779 81fa7368746f cmp edx, 0x6f746873
14154477f 0f8e57020000 jle 0x1415449dc
141544785 81fa7468746f cmp edx, 0x6f746874
14154478b 0f844e050000 je 0x141544cdf
141544791 81fa69746172 cmp edx, 0x72617469
141544797 0f84ac050000 je 0x141544d49
14154479d 81fa61657272 cmp edx, 0x72726561
1415447a3 0f8537090000 jne 0x1415450e0
1415447a9 0fbe7f5c movsx edi, byte ptr [rdi + 0x5c]
1415447ad e83e8d2fff call 0x14083d4f0
1415447b2 4883c028 add rax, 0x28
1415447b6 897df8 mov dword ptr [rbp - 8], edi
1415447b9 488945f0 mov qword ptr [rbp - 0x10], rax
1415447bd 488d4df0 lea rcx, [rbp - 0x10]
1415447c1 4839f1 cmp rcx, rsi
1415447c4 7430 je 0x1415447f6
1415447c6 488b0e mov rcx, qword ptr [rsi]
1415447c9 488b01 mov rax, qword ptr [rcx]
1415447cc 4889f2 mov rdx, rsi
1415447cf ff5010 call qword ptr [rax + 0x10]
1415447d2 488b45f0 mov rax, qword ptr [rbp - 0x10]
1415447d6 488b4df8 mov rcx, qword ptr [rbp - 8]
1415447da 48894e08 mov qword ptr [rsi + 8], rcx
1415447de 488906 mov qword ptr [rsi], rax
1415447e1 e80a8d2fff call 0x14083d4f0
1415447e6 4883c008 add rax, 8
1415447ea 48c745f800000000 mov qword ptr [rbp - 8], 0
1415447f2 488945f0 mov qword ptr [rbp - 0x10], rax
1415447f6 488b18 mov rbx, qword ptr [rax]
1415447f9 488d55f0 lea rdx, [rbp - 0x10]
1415447fd 4889c1 mov rcx, rax
141544800 ff5310 call qword ptr [rbx + 0x10]
141544803 e9cd080000 jmp 0x1415450d5
141544808 81fa73677366 cmp edx, 0x66736773
14154480e 0f8e5a020000 jle 0x141544a6e
141544814 81fa74677366 cmp edx, 0x66736774
14154481a 0f8488050000 je 0x141544da8
141544820 81fa736d6167 cmp edx, 0x67616d73
141544826 0f8493030000 je 0x141544bbf
14154482c 81fa736c6f67 cmp edx, 0x676f6c73
141544832 0f85a8080000 jne 0x1415450e0
141544838 0fbf5f56 movsx ebx, word ptr [rdi + 0x56]
14154483c e8af8c2fff call 0x14083d4f0
141544841 4883c028 add rax, 0x28
141544845 895df8 mov dword ptr [rbp - 8], ebx
141544848 488945f0 mov qword ptr [rbp - 0x10], rax
14154484c 488d4df0 lea rcx, [rbp - 0x10]
141544850 4839f1 cmp rcx, rsi
141544853 7430 je 0x141544885
141544855 488b0e mov rcx, qword ptr [rsi]
141544858 488b01 mov rax, qword ptr [rcx]
14154485b 4889f2 mov rdx, rsi
14154485e ff5010 call qword ptr [rax + 0x10]
141544861 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544865 488b4df8 mov rcx, qword ptr [rbp - 8]
141544869 48894e08 mov qword ptr [rsi + 8], rcx
14154486d 488906 mov qword ptr [rsi], rax
141544870 e87b8c2fff call 0x14083d4f0
141544875 4883c008 add rax, 8
141544879 48c745f800000000 mov qword ptr [rbp - 8], 0
141544881 488945f0 mov qword ptr [rbp - 0x10], rax
141544885 488b18 mov rbx, qword ptr [rax]
141544888 488d55f0 lea rdx, [rbp - 0x10]
14154488c 4889c1 mov rcx, rax
14154488f ff5310 call qword ptr [rbx + 0x10]
141544892 488d05075c6100 lea rax, [rip + 0x615c07]
141544899 4839c6 cmp rsi, rax
14154489c 0f8433080000 je 0x1415450d5
1415448a2 66837f5600 cmp word ptr [rdi + 0x56], 0
1415448a7 0f886a070000 js 0x141545017
1415448ad e923080000 jmp 0x1415450d5
1415448b2 81fa63697473 cmp edx, 0x73746963
1415448b8 0f8e27020000 jle 0x141544ae5
1415448be 81fa6d616574 cmp edx, 0x7465616d
1415448c4 0f843d050000 je 0x141544e07
1415448ca 81fa6d6e7473 cmp edx, 0x73746e6d
1415448d0 0f849b050000 je 0x141544e71
1415448d6 81fa64697473 cmp edx, 0x73746964
1415448dc 0f85fe070000 jne 0x1415450e0
1415448e2 8b471c mov eax, dword ptr [rdi + 0x1c]
1415448e5 48c1e020 shl rax, 0x20
1415448e9 48637f18 movsxd rdi, dword ptr [rdi + 0x18]
1415448ed 4809c7 or rdi, rax
1415448f0 e8fb8b2fff call 0x14083d4f0
1415448f5 4883c048 add rax, 0x48
1415448f9 48897df8 mov qword ptr [rbp - 8], rdi
1415448fd 488945f0 mov qword ptr [rbp - 0x10], rax
141544901 488d4df0 lea rcx, [rbp - 0x10]
141544905 4839f1 cmp rcx, rsi
141544908 7430 je 0x14154493a
14154490a 488b0e mov rcx, qword ptr [rsi]
14154490d 488b01 mov rax, qword ptr [rcx]
141544910 4889f2 mov rdx, rsi
141544913 ff5010 call qword ptr [rax + 0x10]
141544916 488b45f0 mov rax, qword ptr [rbp - 0x10]
14154491a 488b4df8 mov rcx, qword ptr [rbp - 8]
14154491e 48894e08 mov qword ptr [rsi + 8], rcx
141544922 488906 mov qword ptr [rsi], rax
141544925 e8c68b2fff call 0x14083d4f0
14154492a 4883c008 add rax, 8
14154492e 48c745f800000000 mov qword ptr [rbp - 8], 0
141544936 488945f0 mov qword ptr [rbp - 0x10], rax
14154493a 488b38 mov rdi, qword ptr [rax]
14154493d 488d55f0 lea rdx, [rbp - 0x10]
141544941 4889c1 mov rcx, rax
141544944 ff5710 call qword ptr [rdi + 0x10]
141544947 e989070000 jmp 0x1415450d5
14154494c 81fa73707061 cmp edx, 0x61707073
141544952 0f8467020000 je 0x141544bbf
141544958 81fa65747461 cmp edx, 0x61747465
14154495e 0f857c070000 jne 0x1415450e0
141544964 8b5f50 mov ebx, dword ptr [rdi + 0x50]
141544967 e8848b2fff call 0x14083d4f0
14154496c 4883c028 add rax, 0x28
141544970 895df8 mov dword ptr [rbp - 8], ebx
141544973 488945f0 mov qword ptr [rbp - 0x10], rax
141544977 488d4df0 lea rcx, [rbp - 0x10]
14154497b 4839f1 cmp rcx, rsi
14154497e 7430 je 0x1415449b0
141544980 488b0e mov rcx, qword ptr [rsi]
141544983 488b01 mov rax, qword ptr [rcx]
141544986 4889f2 mov rdx, rsi
141544989 ff5010 call qword ptr [rax + 0x10]
14154498c 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544990 488b4df8 mov rcx, qword ptr [rbp - 8]
141544994 48894e08 mov qword ptr [rsi + 8], rcx
141544998 488906 mov qword ptr [rsi], rax
14154499b e8508b2fff call 0x14083d4f0
1415449a0 4883c008 add rax, 8
1415449a4 48c745f800000000 mov qword ptr [rbp - 8], 0
1415449ac 488945f0 mov qword ptr [rbp - 0x10], rax
1415449b0 488b18 mov rbx, qword ptr [rax]
1415449b3 488d55f0 lea rdx, [rbp - 0x10]
1415449b7 4889c1 mov rcx, rax
1415449ba ff5310 call qword ptr [rbx + 0x10]
1415449bd 488d05dc5a6100 lea rax, [rip + 0x615adc]
1415449c4 4839c6 cmp rsi, rax
1415449c7 0f8408070000 je 0x1415450d5
1415449cd 837f50ff cmp dword ptr [rdi + 0x50], -1
1415449d1 0f8440060000 je 0x141545017
1415449d7 e9f9060000 jmp 0x1415450d5
1415449dc 81fa6f666e69 cmp edx, 0x696e666f
1415449e2 0f8408050000 je 0x141544ef0
1415449e8 81fa736c676f cmp edx, 0x6f676c73
1415449ee 0f85ec060000 jne 0x1415450e0
1415449f4 0fbf5f58 movsx ebx, word ptr [rdi + 0x58]
1415449f8 e8f38a2fff call 0x14083d4f0
1415449fd 4883c028 add rax, 0x28
141544a01 895df8 mov dword ptr [rbp - 8], ebx
141544a04 488945f0 mov qword ptr [rbp - 0x10], rax
141544a08 488d4df0 lea rcx, [rbp - 0x10]
141544a0c 4839f1 cmp rcx, rsi
141544a0f 7430 je 0x141544a41
141544a11 488b0e mov rcx, qword ptr [rsi]
141544a14 488b01 mov rax, qword ptr [rcx]
141544a17 4889f2 mov rdx, rsi
141544a1a ff5010 call qword ptr [rax + 0x10]
141544a1d 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544a21 488b4df8 mov rcx, qword ptr [rbp - 8]
141544a25 48894e08 mov qword ptr [rsi + 8], rcx
141544a29 488906 mov qword ptr [rsi], rax
141544a2c e8bf8a2fff call 0x14083d4f0
141544a31 4883c008 add rax, 8
141544a35 48c745f800000000 mov qword ptr [rbp - 8], 0
141544a3d 488945f0 mov qword ptr [rbp - 0x10], rax
141544a41 488b18 mov rbx, qword ptr [rax]
141544a44 488d55f0 lea rdx, [rbp - 0x10]
141544a48 4889c1 mov rcx, rax
141544a4b ff5310 call qword ptr [rbx + 0x10]
141544a4e 488d054b5a6100 lea rax, [rip + 0x615a4b]
141544a55 4839c6 cmp rsi, rax
141544a58 0f8477060000 je 0x1415450d5
141544a5e 66837f5800 cmp word ptr [rdi + 0x58], 0
141544a63 0f88ae050000 js 0x141545017
141544a69 e967060000 jmp 0x1415450d5
141544a6e 81fa74646e65 cmp edx, 0x656e6474
141544a74 0f84d5040000 je 0x141544f4f
141544a7a 81fa6e697465 cmp edx, 0x6574696e
141544a80 0f855a060000 jne 0x1415450e0
141544a86 0fbe7f5d movsx edi, byte ptr [rdi + 0x5d]
141544a8a e8618a2fff call 0x14083d4f0
141544a8f 4883c028 add rax, 0x28
141544a93 897df8 mov dword ptr [rbp - 8], edi
141544a96 488945f0 mov qword ptr [rbp - 0x10], rax
141544a9a 488d4df0 lea rcx, [rbp - 0x10]
141544a9e 4839f1 cmp rcx, rsi
141544aa1 7430 je 0x141544ad3
141544aa3 488b0e mov rcx, qword ptr [rsi]
141544aa6 488b01 mov rax, qword ptr [rcx]
141544aa9 4889f2 mov rdx, rsi
141544aac ff5010 call qword ptr [rax + 0x10]
141544aaf 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544ab3 488b4df8 mov rcx, qword ptr [rbp - 8]
141544ab7 48894e08 mov qword ptr [rsi + 8], rcx
141544abb 488906 mov qword ptr [rsi], rax
141544abe e82d8a2fff call 0x14083d4f0
141544ac3 4883c008 add rax, 8
141544ac7 48c745f800000000 mov qword ptr [rbp - 8], 0
141544acf 488945f0 mov qword ptr [rbp - 0x10], rax
141544ad3 488b18 mov rbx, qword ptr [rax]
141544ad6 488d55f0 lea rdx, [rbp - 0x10]
141544ada 4889c1 mov rcx, rax
141544add ff5310 call qword ptr [rbx + 0x10]
141544ae0 e9f0050000 jmp 0x1415450d5
141544ae5 81fa62647473 cmp edx, 0x73746462
141544aeb 0f844e050000 je 0x14154503f
141544af1 81fa74647473 cmp edx, 0x73746474
141544af7 0f85e3050000 jne 0x1415450e0
141544afd 8b05cd7d6100 mov eax, dword ptr [rip + 0x617dcd]
141544b03 8b0d57125800 mov ecx, dword ptr [rip + 0x581257]
141544b09 65488b142558000000 mov rdx, qword ptr gs:[0x58]
141544b12 488b0cca mov rcx, qword ptr [rdx + rcx*8]
141544b16 3b8104000000 cmp eax, dword ptr [rcx + 4]
141544b1c 0f8fd1050000 jg 0x1415450f3
141544b22 0fb74740 movzx eax, word ptr [rdi + 0x40]
141544b26 89c1 mov ecx, eax
141544b28 81e1ff010000 and ecx, 0x1ff
141544b2e c1e108 shl ecx, 8
141544b31 0fb75742 movzx edx, word ptr [rdi + 0x42]
141544b35 c1e809 shr eax, 9
141544b38 c1e211 shl edx, 0x11
141544b3b 09c2 or edx, eax
141544b3d 09ca or edx, ecx
141544b3f 8955f8 mov dword ptr [rbp - 8], edx
141544b42 488d0d577d6100 lea rcx, [rip + 0x617d57]
141544b49 48894df0 mov qword ptr [rbp - 0x10], rcx
141544b4d 488d45f0 lea rax, [rbp - 0x10]
141544b51 4839f0 cmp rax, rsi
141544b54 7433 je 0x141544b89
141544b56 488b0e mov rcx, qword ptr [rsi]
141544b59 488b01 mov rax, qword ptr [rcx]
141544b5c 4889f2 mov rdx, rsi
141544b5f ff5010 call qword ptr [rax + 0x10]
141544b62 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544b66 488b4df8 mov rcx, qword ptr [rbp - 8]
141544b6a 48894e08 mov qword ptr [rsi + 8], rcx
141544b6e 488906 mov qword ptr [rsi], rax
141544b71 e87a892fff call 0x14083d4f0
141544b76 4889c1 mov rcx, rax
141544b79 4883c108 add rcx, 8
141544b7d 48c745f800000000 mov qword ptr [rbp - 8], 0
141544b85 48894df0 mov qword ptr [rbp - 0x10], rcx
141544b89 488b01 mov rax, qword ptr [rcx]
141544b8c 488d55f0 lea rdx, [rbp - 0x10]
141544b90 ff5010 call qword ptr [rax + 0x10]
141544b93 488d0506596100 lea rax, [rip + 0x615906]
141544b9a 4839c6 cmp rsi, rax
141544b9d 0f8432050000 je 0x1415450d5
141544ba3 0fb74740 movzx eax, word ptr [rdi + 0x40]
141544ba7 25ff010000 and eax, 0x1ff
141544bac 6683f801 cmp ax, 1
141544bb0 0f851f050000 jne 0x1415450d5
141544bb6 0fb74742 movzx eax, word ptr [rdi + 0x42]
141544bba e94d040000 jmp 0x14154500c
141544bbf 0fbf7f54 movsx edi, word ptr [rdi + 0x54]
141544bc3 e828892fff call 0x14083d4f0
141544bc8 4883c028 add rax, 0x28
141544bcc 897df8 mov dword ptr [rbp - 8], edi
141544bcf 488945f0 mov qword ptr [rbp - 0x10], rax
141544bd3 488d4df0 lea rcx, [rbp - 0x10]
141544bd7 4839f1 cmp rcx, rsi
141544bda 7430 je 0x141544c0c
141544bdc 488b0e mov rcx, qword ptr [rsi]
141544bdf 488b01 mov rax, qword ptr [rcx]
141544be2 4889f2 mov rdx, rsi
141544be5 ff5010 call qword ptr [rax + 0x10]
141544be8 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544bec 488b4df8 mov rcx, qword ptr [rbp - 8]
141544bf0 48894e08 mov qword ptr [rsi + 8], rcx
141544bf4 488906 mov qword ptr [rsi], rax
141544bf7 e8f4882fff call 0x14083d4f0
141544bfc 4883c008 add rax, 8
141544c00 48c745f800000000 mov qword ptr [rbp - 8], 0
141544c08 488945f0 mov qword ptr [rbp - 0x10], rax
141544c0c 488b38 mov rdi, qword ptr [rax]
141544c0f 488d55f0 lea rdx, [rbp - 0x10]
141544c13 4889c1 mov rcx, rax
141544c16 ff5710 call qword ptr [rdi + 0x10]
141544c19 e9b7040000 jmp 0x1415450d5
141544c1e 8b7f50 mov edi, dword ptr [rdi + 0x50]
141544c21 e8ca882fff call 0x14083d4f0
141544c26 4883c028 add rax, 0x28
141544c2a 897df8 mov dword ptr [rbp - 8], edi
141544c2d 488945f0 mov qword ptr [rbp - 0x10], rax
141544c31 488d4df0 lea rcx, [rbp - 0x10]
141544c35 4839f1 cmp rcx, rsi
141544c38 7430 je 0x141544c6a
141544c3a 488b0e mov rcx, qword ptr [rsi]
141544c3d 488b01 mov rax, qword ptr [rcx]
141544c40 4889f2 mov rdx, rsi
141544c43 ff5010 call qword ptr [rax + 0x10]
141544c46 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544c4a 488b4df8 mov rcx, qword ptr [rbp - 8]
141544c4e 48894e08 mov qword ptr [rsi + 8], rcx
141544c52 488906 mov qword ptr [rsi], rax
141544c55 e896882fff call 0x14083d4f0
141544c5a 4883c008 add rax, 8
141544c5e 48c745f800000000 mov qword ptr [rbp - 8], 0
141544c66 488945f0 mov qword ptr [rbp - 0x10], rax
141544c6a 488b38 mov rdi, qword ptr [rax]
141544c6d 488d55f0 lea rdx, [rbp - 0x10]
141544c71 4889c1 mov rcx, rax
141544c74 ff5710 call qword ptr [rdi + 0x10]
141544c77 e959040000 jmp 0x1415450d5
141544c7c 0fb65f5d movzx ebx, byte ptr [rdi + 0x5d]
141544c80 e86b882fff call 0x14083d4f0
141544c85 4883c018 add rax, 0x18
141544c89 80fb01 cmp bl, 1
141544c8c 0f9445f8 sete byte ptr [rbp - 8]
141544c90 488945f0 mov qword ptr [rbp - 0x10], rax
141544c94 488d4df0 lea rcx, [rbp - 0x10]
141544c98 4839f1 cmp rcx, rsi
141544c9b 7430 je 0x141544ccd
141544c9d 488b0e mov rcx, qword ptr [rsi]
141544ca0 488b01 mov rax, qword ptr [rcx]
141544ca3 4889f2 mov rdx, rsi
141544ca6 ff5010 call qword ptr [rax + 0x10]
141544ca9 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544cad 488b4df8 mov rcx, qword ptr [rbp - 8]
141544cb1 48894e08 mov qword ptr [rsi + 8], rcx
141544cb5 488906 mov qword ptr [rsi], rax
141544cb8 e833882fff call 0x14083d4f0
141544cbd 4883c008 add rax, 8
141544cc1 48c745f800000000 mov qword ptr [rbp - 8], 0
141544cc9 488945f0 mov qword ptr [rbp - 0x10], rax
141544ccd 488b18 mov rbx, qword ptr [rax]
141544cd0 488d55f0 lea rdx, [rbp - 0x10]
141544cd4 4889c1 mov rcx, rax
141544cd7 ff5310 call qword ptr [rbx + 0x10]
141544cda e9f6030000 jmp 0x1415450d5
141544cdf 8b472c mov eax, dword ptr [rdi + 0x2c]
141544ce2 48c1e020 shl rax, 0x20
141544ce6 48637f28 movsxd rdi, dword ptr [rdi + 0x28]
141544cea 4809c7 or rdi, rax
141544ced e8fe872fff call 0x14083d4f0
141544cf2 4883c048 add rax, 0x48
141544cf6 48897df8 mov qword ptr [rbp - 8], rdi
141544cfa 488945f0 mov qword ptr [rbp - 0x10], rax
141544cfe 488d4df0 lea rcx, [rbp - 0x10]
141544d02 4839f1 cmp rcx, rsi
141544d05 7430 je 0x141544d37
141544d07 488b0e mov rcx, qword ptr [rsi]
141544d0a 488b01 mov rax, qword ptr [rcx]
141544d0d 4889f2 mov rdx, rsi
141544d10 ff5010 call qword ptr [rax + 0x10]
141544d13 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544d17 488b4df8 mov rcx, qword ptr [rbp - 8]
141544d1b 48894e08 mov qword ptr [rsi + 8], rcx
141544d1f 488906 mov qword ptr [rsi], rax
141544d22 e8c9872fff call 0x14083d4f0
141544d27 4883c008 add rax, 8
141544d2b 48c745f800000000 mov qword ptr [rbp - 8], 0
141544d33 488945f0 mov qword ptr [rbp - 0x10], rax
141544d37 488b38 mov rdi, qword ptr [rax]
141544d3a 488d55f0 lea rdx, [rbp - 0x10]
141544d3e 4889c1 mov rcx, rax
141544d41 ff5710 call qword ptr [rdi + 0x10]
141544d44 e98c030000 jmp 0x1415450d5
141544d49 0fbe7f5a movsx edi, byte ptr [rdi + 0x5a]
141544d4d e89e872fff call 0x14083d4f0
141544d52 4883c028 add rax, 0x28
141544d56 897df8 mov dword ptr [rbp - 8], edi
141544d59 488945f0 mov qword ptr [rbp - 0x10], rax
141544d5d 488d4df0 lea rcx, [rbp - 0x10]
141544d61 4839f1 cmp rcx, rsi
141544d64 7430 je 0x141544d96
141544d66 488b0e mov rcx, qword ptr [rsi]
141544d69 488b01 mov rax, qword ptr [rcx]
141544d6c 4889f2 mov rdx, rsi
141544d6f ff5010 call qword ptr [rax + 0x10]
141544d72 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544d76 488b4df8 mov rcx, qword ptr [rbp - 8]
141544d7a 48894e08 mov qword ptr [rsi + 8], rcx
141544d7e 488906 mov qword ptr [rsi], rax
141544d81 e86a872fff call 0x14083d4f0
141544d86 4883c008 add rax, 8
141544d8a 48c745f800000000 mov qword ptr [rbp - 8], 0
141544d92 488945f0 mov qword ptr [rbp - 0x10], rax
141544d96 488b18 mov rbx, qword ptr [rax]
141544d99 488d55f0 lea rdx, [rbp - 0x10]
141544d9d 4889c1 mov rcx, rax
141544da0 ff5310 call qword ptr [rbx + 0x10]
141544da3 e92d030000 jmp 0x1415450d5
141544da8 0fbf7f58 movsx edi, word ptr [rdi + 0x58]
141544dac e83f872fff call 0x14083d4f0
141544db1 4883c028 add rax, 0x28
141544db5 897df8 mov dword ptr [rbp - 8], edi
141544db8 488945f0 mov qword ptr [rbp - 0x10], rax
141544dbc 488d4df0 lea rcx, [rbp - 0x10]
141544dc0 4839f1 cmp rcx, rsi
141544dc3 7430 je 0x141544df5
141544dc5 488b0e mov rcx, qword ptr [rsi]
141544dc8 488b01 mov rax, qword ptr [rcx]
141544dcb 4889f2 mov rdx, rsi
141544dce ff5010 call qword ptr [rax + 0x10]
141544dd1 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544dd5 488b4df8 mov rcx, qword ptr [rbp - 8]
141544dd9 48894e08 mov qword ptr [rsi + 8], rcx
141544ddd 488906 mov qword ptr [rsi], rax
141544de0 e80b872fff call 0x14083d4f0
141544de5 4883c008 add rax, 8
141544de9 48c745f800000000 mov qword ptr [rbp - 8], 0
141544df1 488945f0 mov qword ptr [rbp - 0x10], rax
141544df5 488b18 mov rbx, qword ptr [rax]
141544df8 488d55f0 lea rdx, [rbp - 0x10]
141544dfc 4889c1 mov rcx, rax
141544dff ff5310 call qword ptr [rbx + 0x10]
141544e02 e9ce020000 jmp 0x1415450d5
141544e07 8b4724 mov eax, dword ptr [rdi + 0x24]
141544e0a 48c1e020 shl rax, 0x20
141544e0e 48637f20 movsxd rdi, dword ptr [rdi + 0x20]
141544e12 4809c7 or rdi, rax
141544e15 e8d6862fff call 0x14083d4f0
141544e1a 4883c048 add rax, 0x48
141544e1e 48897df8 mov qword ptr [rbp - 8], rdi
141544e22 488945f0 mov qword ptr [rbp - 0x10], rax
141544e26 488d4df0 lea rcx, [rbp - 0x10]
141544e2a 4839f1 cmp rcx, rsi
141544e2d 7430 je 0x141544e5f
141544e2f 488b0e mov rcx, qword ptr [rsi]
141544e32 488b01 mov rax, qword ptr [rcx]
141544e35 4889f2 mov rdx, rsi
141544e38 ff5010 call qword ptr [rax + 0x10]
141544e3b 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544e3f 488b4df8 mov rcx, qword ptr [rbp - 8]
141544e43 48894e08 mov qword ptr [rsi + 8], rcx
141544e47 488906 mov qword ptr [rsi], rax
141544e4a e8a1862fff call 0x14083d4f0
141544e4f 4883c008 add rax, 8
141544e53 48c745f800000000 mov qword ptr [rbp - 8], 0
141544e5b 488945f0 mov qword ptr [rbp - 0x10], rax
141544e5f 488b38 mov rdi, qword ptr [rax]
141544e62 488d55f0 lea rdx, [rbp - 0x10]
141544e66 4889c1 mov rcx, rax
141544e69 ff5710 call qword ptr [rdi + 0x10]
141544e6c e964020000 jmp 0x1415450d5
141544e71 4883c738 add rdi, 0x38
141544e75 e876862fff call 0x14083d4f0
141544e7a 488d4df8 lea rcx, [rbp - 8]
141544e7e 48c745f800000000 mov qword ptr [rbp - 8], 0
141544e86 4839f9 cmp rcx, rdi
141544e89 7410 je 0x141544e9b
141544e8b 488b0f mov rcx, qword ptr [rdi]
141544e8e 4885c9 test rcx, rcx
141544e91 7404 je 0x141544e97
141544e93 f0ff41fc lock inc dword ptr [rcx - 4]
141544e97 48894df8 mov qword ptr [rbp - 8], rcx
141544e9b 480588000000 add rax, 0x88
141544ea1 488945f0 mov qword ptr [rbp - 0x10], rax
141544ea5 488d4df0 lea rcx, [rbp - 0x10]
141544ea9 4839f1 cmp rcx, rsi
141544eac 7430 je 0x141544ede
141544eae 488b0e mov rcx, qword ptr [rsi]
141544eb1 488b01 mov rax, qword ptr [rcx]
141544eb4 4889f2 mov rdx, rsi
141544eb7 ff5010 call qword ptr [rax + 0x10]
141544eba 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544ebe 488b4df8 mov rcx, qword ptr [rbp - 8]
141544ec2 48894e08 mov qword ptr [rsi + 8], rcx
141544ec6 488906 mov qword ptr [rsi], rax
141544ec9 e822862fff call 0x14083d4f0
141544ece 4883c008 add rax, 8
141544ed2 48c745f800000000 mov qword ptr [rbp - 8], 0
141544eda 488945f0 mov qword ptr [rbp - 0x10], rax
141544ede 488b38 mov rdi, qword ptr [rax]
141544ee1 488d55f0 lea rdx, [rbp - 0x10]
141544ee5 4889c1 mov rcx, rax
141544ee8 ff5710 call qword ptr [rdi + 0x10]
141544eeb e9e5010000 jmp 0x1415450d5
141544ef0 0fbe7f5b movsx edi, byte ptr [rdi + 0x5b]
141544ef4 e8f7852fff call 0x14083d4f0
141544ef9 4883c028 add rax, 0x28
141544efd 897df8 mov dword ptr [rbp - 8], edi
141544f00 488945f0 mov qword ptr [rbp - 0x10], rax
141544f04 488d4df0 lea rcx, [rbp - 0x10]
141544f08 4839f1 cmp rcx, rsi
141544f0b 7430 je 0x141544f3d
141544f0d 488b0e mov rcx, qword ptr [rsi]
141544f10 488b01 mov rax, qword ptr [rcx]
141544f13 4889f2 mov rdx, rsi
141544f16 ff5010 call qword ptr [rax + 0x10]
141544f19 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544f1d 488b4df8 mov rcx, qword ptr [rbp - 8]
141544f21 48894e08 mov qword ptr [rsi + 8], rcx
141544f25 488906 mov qword ptr [rsi], rax
141544f28 e8c3852fff call 0x14083d4f0
141544f2d 4883c008 add rax, 8
141544f31 48c745f800000000 mov qword ptr [rbp - 8], 0
141544f39 488945f0 mov qword ptr [rbp - 0x10], rax
141544f3d 488b18 mov rbx, qword ptr [rax]
141544f40 488d55f0 lea rdx, [rbp - 0x10]
141544f44 4889c1 mov rcx, rax
141544f47 ff5310 call qword ptr [rbx + 0x10]
141544f4a e986010000 jmp 0x1415450d5
141544f4f 8b057b796100 mov eax, dword ptr [rip + 0x61797b]
141544f55 8b0d050e5800 mov ecx, dword ptr [rip + 0x580e05]
141544f5b 65488b142558000000 mov rdx, qword ptr gs:[0x58]
141544f64 488b0cca mov rcx, qword ptr [rdx + rcx*8]
141544f68 3b8104000000 cmp eax, dword ptr [rcx + 4]
141544f6e 0f8fc1010000 jg 0x141545135
141544f74 0fb74744 movzx eax, word ptr [rdi + 0x44]
141544f78 89c1 mov ecx, eax
141544f7a 81e1ff010000 and ecx, 0x1ff
141544f80 c1e108 shl ecx, 8
141544f83 0fb75746 movzx edx, word ptr [rdi + 0x46]
141544f87 c1e809 shr eax, 9
141544f8a c1e211 shl edx, 0x11
141544f8d 09c2 or edx, eax
141544f8f 09ca or edx, ecx
141544f91 8955f8 mov dword ptr [rbp - 8], edx
141544f94 488d0d05796100 lea rcx, [rip + 0x617905]
141544f9b 48894df0 mov qword ptr [rbp - 0x10], rcx
141544f9f 488d45f0 lea rax, [rbp - 0x10]
141544fa3 4839f0 cmp rax, rsi
141544fa6 7433 je 0x141544fdb
141544fa8 488b0e mov rcx, qword ptr [rsi]
141544fab 488b01 mov rax, qword ptr [rcx]
141544fae 4889f2 mov rdx, rsi
141544fb1 ff5010 call qword ptr [rax + 0x10]
141544fb4 488b45f0 mov rax, qword ptr [rbp - 0x10]
141544fb8 488b4df8 mov rcx, qword ptr [rbp - 8]
141544fbc 48894e08 mov qword ptr [rsi + 8], rcx
141544fc0 488906 mov qword ptr [rsi], rax
141544fc3 e828852fff call 0x14083d4f0
141544fc8 4889c1 mov rcx, rax
141544fcb 4883c108 add rcx, 8
141544fcf 48c745f800000000 mov qword ptr [rbp - 8], 0
141544fd7 48894df0 mov qword ptr [rbp - 0x10], rcx
141544fdb 488b01 mov rax, qword ptr [rcx]
141544fde 488d55f0 lea rdx, [rbp - 0x10]
141544fe2 ff5010 call qword ptr [rax + 0x10]
141544fe5 488d05b4546100 lea rax, [rip + 0x6154b4]
141544fec 4839c6 cmp rsi, rax
141544fef 0f84e0000000 je 0x1415450d5
141544ff5 0fb74744 movzx eax, word ptr [rdi + 0x44]
141544ff9 25ff010000 and eax, 0x1ff
141544ffe 6683f801 cmp ax, 1
141545002 0f85cd000000 jne 0x1415450d5
141545008 0fb74746 movzx eax, word ptr [rdi + 0x46]
14154500c 3d6c070000 cmp eax, 0x76c
141545011 0f85be000000 jne 0x1415450d5
141545017 488b0e mov rcx, qword ptr [rsi]
14154501a 488b01 mov rax, qword ptr [rcx]
14154501d 4889f2 mov rdx, rsi
141545020 ff5010 call qword ptr [rax + 0x10]
141545023 488d1576546100 lea rdx, [rip + 0x615476]
14154502a 488b0d6f546100 mov rcx, qword ptr [rip + 0x61546f]
141545031 488b01 mov rax, qword ptr [rcx]
141545034 4989f0 mov r8, rsi
141545037 ff5018 call qword ptr [rax + 0x18]
14154503a e996000000 jmp 0x1415450d5
14154503f 8b058b786100 mov eax, dword ptr [rip + 0x61788b]
141545045 8b0d150d5800 mov ecx, dword ptr [rip + 0x580d15]
14154504b 65488b142558000000 mov rdx, qword ptr gs:[0x58]
141545054 488b0cca mov rcx, qword ptr [rdx + rcx*8]
141545058 3b8104000000 cmp eax, dword ptr [rcx + 4]
14154505e 0f8f13010000 jg 0x141545177
141545064 0fb74748 movzx eax, word ptr [rdi + 0x48]
141545068 89c1 mov ecx, eax
14154506a 81e1ff010000 and ecx, 0x1ff
141545070 c1e108 shl ecx, 8
141545073 0fb7574a movzx edx, word ptr [rdi + 0x4a]
141545077 c1e809 shr eax, 9
14154507a c1e211 shl edx, 0x11
14154507d 09c2 or edx, eax
14154507f 09ca or edx, ecx
141545081 8955f8 mov dword ptr [rbp - 8], edx
141545084 488d0d15786100 lea rcx, [rip + 0x617815]
14154508b 48894df0 mov qword ptr [rbp - 0x10], rcx
14154508f 488d45f0 lea rax, [rbp - 0x10]
141545093 4839f0 cmp rax, rsi
141545096 7433 je 0x1415450cb
141545098 488b0e mov rcx, qword ptr [rsi]
14154509b 488b01 mov rax, qword ptr [rcx]
14154509e 4889f2 mov rdx, rsi
1415450a1 ff5010 call qword ptr [rax + 0x10]
1415450a4 488b45f0 mov rax, qword ptr [rbp - 0x10]
1415450a8 488b4df8 mov rcx, qword ptr [rbp - 8]
1415450ac 48894e08 mov qword ptr [rsi + 8], rcx
1415450b0 488906 mov qword ptr [rsi], rax
1415450b3 e838842fff call 0x14083d4f0
1415450b8 4889c1 mov rcx, rax
1415450bb 4883c108 add rcx, 8
1415450bf 48c745f800000000 mov qword ptr [rbp - 8], 0
1415450c7 48894df0 mov qword ptr [rbp - 0x10], rcx
1415450cb 488b01 mov rax, qword ptr [rcx]
1415450ce 488d55f0 lea rdx, [rbp - 0x10]
1415450d2 ff5010 call qword ptr [rax + 0x10]
1415450d5 b001 mov al, 1
1415450d7 4883c438 add rsp, 0x38
1415450db 5b pop rbx
1415450dc 5f pop rdi
1415450dd 5e pop rsi
1415450de 5d pop rbp
1415450df c3 ret 
1415450e0 4889f9 mov rcx, rdi
1415450e3 4989f0 mov r8, rsi
1415450e6 4883c438 add rsp, 0x38
1415450ea 5b pop rbx
1415450eb 5f pop rdi
1415450ec 5e pop rsi
1415450ed 5d pop rbp
1415450ee e92deea9ff jmp 0x140fe3f20
1415450f3 488d0dd6776100 lea rcx, [rip + 0x6177d6]
1415450fa e809bd2000 call 0x141750e08
1415450ff 833dca776100ff cmp dword ptr [rip + 0x6177ca], -1
141545106 0f8516faffff jne 0x141544b22
14154510c 488d0d8d776100 lea rcx, [rip + 0x61778d]
141545113 e8987887ff call 0x140dbc9b0
141545118 488d0df17887ff lea rcx, [rip - 0x78870f]
14154511f e824bf2000 call 0x141751048
141545124 488d0da5776100 lea rcx, [rip + 0x6177a5]
14154512b e870bd2000 call 0x141750ea0
141545130 e9edf9ffff jmp 0x141544b22
141545135 488d0d94776100 lea rcx, [rip + 0x617794]
14154513c e8c7bc2000 call 0x141750e08
141545141 833d88776100ff cmp dword ptr [rip + 0x617788], -1
141545148 0f8526feffff jne 0x141544f74
14154514e 488d0d4b776100 lea rcx, [rip + 0x61774b]
141545155 e8567887ff call 0x140dbc9b0
14154515a 488d0daf7887ff lea rcx, [rip - 0x788751]
141545161 e8e2be2000 call 0x141751048
141545166 488d0d63776100 lea rcx, [rip + 0x617763]
14154516d e82ebd2000 call 0x141750ea0
141545172 e9fdfdffff jmp 0x141544f74
141545177 488d0d52776100 lea rcx, [rip + 0x617752]
14154517e e885bc2000 call 0x141750e08
141545183 833d46776100ff cmp dword ptr [rip + 0x617746], -1
14154518a 0f85d4feffff jne 0x141545064
141545190 488d0d09776100 lea rcx, [rip + 0x617709]
141545197 e8147887ff call 0x140dbc9b0
14154519c 488d0d6d7887ff lea rcx, [rip - 0x788793]
1415451a3 e8a0be2000 call 0x141751048
1415451a8 488d0d21776100 lea rcx, [rip + 0x617721]
1415451af e8ecbc2000 call 0x141750ea0
1415451b4 e9abfeffff jmp 0x141545064
1415451b9 0f1f8000000000 nop dword ptr [rax]
1415451c0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415451c5 55 push rbp
1415451c6 56 push rsi
1415451c7 57 push rdi
1415451c8 53 push rbx
1415451c9 4883ec28 sub rsp, 0x28
1415451cd 488d6a30 lea rbp, [rdx + 0x30]
1415451d1 e89a372100 call 0x141758970
1415451d6 cc int3 
1415451d7 660f1f840000000000 nop word ptr [rax + rax]
1415451e0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415451e5 55 push rbp
1415451e6 56 push rsi
1415451e7 57 push rdi
1415451e8 53 push rbx
1415451e9 4883ec28 sub rsp, 0x28
1415451ed 488d6a30 lea rbp, [rdx + 0x30]
1415451f1 e87a372100 call 0x141758970
1415451f6 cc int3 
1415451f7 660f1f840000000000 nop word ptr [rax + rax]
141545200 4889542410 mov qword ptr [rsp + 0x10], rdx
141545205 55 push rbp
141545206 56 push rsi
141545207 57 push rdi
141545208 53 push rbx
141545209 4883ec28 sub rsp, 0x28
14154520d 488d6a30 lea rbp, [rdx + 0x30]
141545211 e85a372100 call 0x141758970
141545216 cc int3 
141545217 660f1f840000000000 nop word ptr [rax + rax]
141545220 4889542410 mov qword ptr [rsp + 0x10], rdx
141545225 55 push rbp
141545226 56 push rsi
141545227 57 push rdi
141545228 53 push rbx
141545229 4883ec28 sub rsp, 0x28
14154522d 488d6a30 lea rbp, [rdx + 0x30]
141545231 e83a372100 call 0x141758970
141545236 cc int3 
141545237 660f1f840000000000 nop word ptr [rax + rax]
141545240 4889542410 mov qword ptr [rsp + 0x10], rdx
141545245 55 push rbp
141545246 56 push rsi
141545247 57 push rdi
141545248 53 push rbx
141545249 4883ec28 sub rsp, 0x28
14154524d 488d6a30 lea rbp, [rdx + 0x30]
141545251 e81a372100 call 0x141758970
141545256 cc int3 
141545257 660f1f840000000000 nop word ptr [rax + rax]
141545260 4889542410 mov qword ptr [rsp + 0x10], rdx
141545265 55 push rbp
141545266 56 push rsi
141545267 57 push rdi
141545268 53 push rbx
141545269 4883ec28 sub rsp, 0x28
14154526d 488d6a30 lea rbp, [rdx + 0x30]
141545271 e8fa362100 call 0x141758970
141545276 cc int3 
141545277 660f1f840000000000 nop word ptr [rax + rax]
141545280 4889542410 mov qword ptr [rsp + 0x10], rdx
141545285 55 push rbp
141545286 56 push rsi
141545287 57 push rdi
141545288 53 push rbx
141545289 4883ec28 sub rsp, 0x28
14154528d 488d6a30 lea rbp, [rdx + 0x30]
141545291 e8da362100 call 0x141758970
141545296 cc int3 
141545297 660f1f840000000000 nop word ptr [rax + rax]
1415452a0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415452a5 55 push rbp
1415452a6 56 push rsi
1415452a7 57 push rdi
1415452a8 53 push rbx
1415452a9 4883ec28 sub rsp, 0x28
1415452ad 488d6a30 lea rbp, [rdx + 0x30]
1415452b1 e8ba362100 call 0x141758970
1415452b6 cc int3 
1415452b7 660f1f840000000000 nop word ptr [rax + rax]
1415452c0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415452c5 55 push rbp
1415452c6 56 push rsi
1415452c7 57 push rdi
1415452c8 53 push rbx
1415452c9 4883ec28 sub rsp, 0x28
1415452cd 488d6a30 lea rbp, [rdx + 0x30]
1415452d1 e89a362100 call 0x141758970
1415452d6 cc int3 
1415452d7 660f1f840000000000 nop word ptr [rax + rax]
1415452e0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415452e5 55 push rbp
1415452e6 56 push rsi
1415452e7 57 push rdi
1415452e8 53 push rbx
1415452e9 4883ec28 sub rsp, 0x28
1415452ed 488d6a30 lea rbp, [rdx + 0x30]
1415452f1 e87a362100 call 0x141758970
1415452f6 cc int3 
1415452f7 660f1f840000000000 nop word ptr [rax + rax]
141545300 4889542410 mov qword ptr [rsp + 0x10], rdx
141545305 55 push rbp
141545306 56 push rsi
141545307 57 push rdi
141545308 53 push rbx
141545309 4883ec28 sub rsp, 0x28
14154530d 488d6a30 lea rbp, [rdx + 0x30]
141545311 e85a362100 call 0x141758970
141545316 cc int3 
141545317 660f1f840000000000 nop word ptr [rax + rax]
141545320 4889542410 mov qword ptr [rsp + 0x10], rdx
141545325 55 push rbp
141545326 56 push rsi
141545327 57 push rdi
141545328 53 push rbx
141545329 4883ec28 sub rsp, 0x28
14154532d 488d6a30 lea rbp, [rdx + 0x30]
141545331 e83a362100 call 0x141758970
141545336 cc int3 
141545337 660f1f840000000000 nop word ptr [rax + rax]
141545340 4889542410 mov qword ptr [rsp + 0x10], rdx
141545345 55 push rbp
141545346 56 push rsi
141545347 57 push rdi
141545348 53 push rbx
141545349 4883ec28 sub rsp, 0x28
14154534d 488d6a30 lea rbp, [rdx + 0x30]
141545351 e81a362100 call 0x141758970
141545356 cc int3 
141545357 660f1f840000000000 nop word ptr [rax + rax]
141545360 4889542410 mov qword ptr [rsp + 0x10], rdx
141545365 55 push rbp
141545366 56 push rsi
141545367 57 push rdi
141545368 53 push rbx
141545369 4883ec28 sub rsp, 0x28
14154536d 488d6a30 lea rbp, [rdx + 0x30]
141545371 e8fa352100 call 0x141758970
141545376 cc int3 
141545377 660f1f840000000000 nop word ptr [rax + rax]
141545380 4889542410 mov qword ptr [rsp + 0x10], rdx
141545385 55 push rbp
141545386 56 push rsi
141545387 57 push rdi
141545388 53 push rbx
141545389 4883ec28 sub rsp, 0x28
14154538d 488d6a30 lea rbp, [rdx + 0x30]
141545391 e8da352100 call 0x141758970
141545396 cc int3 
141545397 660f1f840000000000 nop word ptr [rax + rax]
1415453a0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415453a5 55 push rbp
1415453a6 56 push rsi
1415453a7 57 push rdi
1415453a8 53 push rbx
1415453a9 4883ec28 sub rsp, 0x28
1415453ad 488d6a30 lea rbp, [rdx + 0x30]
1415453b1 e8ba352100 call 0x141758970
1415453b6 cc int3 
1415453b7 660f1f840000000000 nop word ptr [rax + rax]
1415453c0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415453c5 55 push rbp
1415453c6 56 push rsi
1415453c7 57 push rdi
1415453c8 53 push rbx
1415453c9 4883ec28 sub rsp, 0x28
1415453cd 488d6a30 lea rbp, [rdx + 0x30]
1415453d1 e89a352100 call 0x141758970
1415453d6 cc int3 
1415453d7 660f1f840000000000 nop word ptr [rax + rax]
1415453e0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415453e5 55 push rbp
1415453e6 56 push rsi
1415453e7 57 push rdi
1415453e8 53 push rbx
1415453e9 4883ec28 sub rsp, 0x28
1415453ed 488d6a30 lea rbp, [rdx + 0x30]
1415453f1 e87a352100 call 0x141758970
1415453f6 cc int3 
1415453f7 660f1f840000000000 nop word ptr [rax + rax]
141545400 4889542410 mov qword ptr [rsp + 0x10], rdx
141545405 55 push rbp
141545406 56 push rsi
141545407 57 push rdi
141545408 53 push rbx
141545409 4883ec28 sub rsp, 0x28
14154540d 488d6a30 lea rbp, [rdx + 0x30]
141545411 e85a352100 call 0x141758970
141545416 cc int3 
141545417 660f1f840000000000 nop word ptr [rax + rax]
141545420 4889542410 mov qword ptr [rsp + 0x10], rdx
141545425 55 push rbp
141545426 56 push rsi
141545427 57 push rdi
141545428 53 push rbx
141545429 4883ec28 sub rsp, 0x28
14154542d 488d6a30 lea rbp, [rdx + 0x30]
141545431 e83a352100 call 0x141758970
141545436 cc int3 
141545437 660f1f840000000000 nop word ptr [rax + rax]
141545440 4889542410 mov qword ptr [rsp + 0x10], rdx
141545445 55 push rbp
141545446 56 push rsi
141545447 57 push rdi
141545448 53 push rbx
141545449 4883ec28 sub rsp, 0x28
14154544d 488d6a30 lea rbp, [rdx + 0x30]
141545451 e81a352100 call 0x141758970
141545456 cc int3 
141545457 660f1f840000000000 nop word ptr [rax + rax]
141545460 4889542410 mov qword ptr [rsp + 0x10], rdx
141545465 55 push rbp
141545466 56 push rsi
141545467 57 push rdi
141545468 53 push rbx
141545469 4883ec28 sub rsp, 0x28
14154546d 488d6a30 lea rbp, [rdx + 0x30]
141545471 e8fa342100 call 0x141758970
141545476 cc int3 
141545477 660f1f840000000000 nop word ptr [rax + rax]
141545480 4889542410 mov qword ptr [rsp + 0x10], rdx
141545485 55 push rbp
141545486 56 push rsi
141545487 57 push rdi
141545488 53 push rbx
141545489 4883ec28 sub rsp, 0x28
14154548d 488d6a30 lea rbp, [rdx + 0x30]
141545491 e8da342100 call 0x141758970
141545496 cc int3 
141545497 660f1f840000000000 nop word ptr [rax + rax]
1415454a0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415454a5 55 push rbp
1415454a6 56 push rsi
1415454a7 57 push rdi
1415454a8 53 push rbx
1415454a9 4883ec28 sub rsp, 0x28
1415454ad 488d6a30 lea rbp, [rdx + 0x30]
1415454b1 e8ba342100 call 0x141758970
1415454b6 cc int3 
1415454b7 660f1f840000000000 nop word ptr [rax + rax]
1415454c0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415454c5 55 push rbp
1415454c6 56 push rsi
1415454c7 57 push rdi
1415454c8 53 push rbx
1415454c9 4883ec28 sub rsp, 0x28
1415454cd 488d6a30 lea rbp, [rdx + 0x30]
1415454d1 e89a342100 call 0x141758970
1415454d6 cc int3 
1415454d7 660f1f840000000000 nop word ptr [rax + rax]
1415454e0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415454e5 55 push rbp
1415454e6 56 push rsi
1415454e7 57 push rdi
1415454e8 53 push rbx
1415454e9 4883ec28 sub rsp, 0x28
1415454ed 488d6a30 lea rbp, [rdx + 0x30]
1415454f1 e87a342100 call 0x141758970
1415454f6 cc int3 
1415454f7 660f1f840000000000 nop word ptr [rax + rax]
141545500 4889542410 mov qword ptr [rsp + 0x10], rdx
141545505 55 push rbp
141545506 56 push rsi
141545507 57 push rdi
141545508 53 push rbx
141545509 4883ec28 sub rsp, 0x28
14154550d 488d6a30 lea rbp, [rdx + 0x30]
141545511 e85a342100 call 0x141758970
141545516 cc int3 
141545517 660f1f840000000000 nop word ptr [rax + rax]
141545520 4889542410 mov qword ptr [rsp + 0x10], rdx
141545525 55 push rbp
141545526 56 push rsi
141545527 57 push rdi
141545528 53 push rbx
141545529 4883ec28 sub rsp, 0x28
14154552d 488d6a30 lea rbp, [rdx + 0x30]
141545531 e83a342100 call 0x141758970
141545536 cc int3 
141545537 660f1f840000000000 nop word ptr [rax + rax]
141545540 4889542410 mov qword ptr [rsp + 0x10], rdx
141545545 55 push rbp
141545546 56 push rsi
141545547 57 push rdi
141545548 53 push rbx
141545549 4883ec28 sub rsp, 0x28
14154554d 488d6a30 lea rbp, [rdx + 0x30]
141545551 e81a342100 call 0x141758970
141545556 cc int3 
141545557 660f1f840000000000 nop word ptr [rax + rax]
141545560 4889542410 mov qword ptr [rsp + 0x10], rdx
141545565 55 push rbp
141545566 56 push rsi
141545567 57 push rdi
141545568 53 push rbx
141545569 4883ec28 sub rsp, 0x28
14154556d 488d6a30 lea rbp, [rdx + 0x30]
141545571 e8fa332100 call 0x141758970
141545576 cc int3 
141545577 660f1f840000000000 nop word ptr [rax + rax]
141545580 4889542410 mov qword ptr [rsp + 0x10], rdx
141545585 55 push rbp
141545586 56 push rsi
141545587 57 push rdi
141545588 53 push rbx
141545589 4883ec28 sub rsp, 0x28
14154558d 488d6a30 lea rbp, [rdx + 0x30]
141545591 e8da332100 call 0x141758970
141545596 cc int3 
141545597 660f1f840000000000 nop word ptr [rax + rax]
1415455a0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415455a5 55 push rbp
1415455a6 56 push rsi
1415455a7 57 push rdi
1415455a8 53 push rbx
1415455a9 4883ec28 sub rsp, 0x28
1415455ad 488d6a30 lea rbp, [rdx + 0x30]
1415455b1 e8ba332100 call 0x141758970
1415455b6 cc int3 
1415455b7 660f1f840000000000 nop word ptr [rax + rax]
1415455c0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415455c5 55 push rbp
1415455c6 56 push rsi
1415455c7 57 push rdi
1415455c8 53 push rbx
1415455c9 4883ec28 sub rsp, 0x28
1415455cd 488d6a30 lea rbp, [rdx + 0x30]
1415455d1 e89a332100 call 0x141758970
1415455d6 cc int3 
1415455d7 660f1f840000000000 nop word ptr [rax + rax]
1415455e0 4889542410 mov qword ptr [rsp + 0x10], rdx
1415455e5 55 push rbp
1415455e6 56 push rsi
1415455e7 57 push rdi
1415455e8 53 push rbx
1415455e9 4883ec28 sub rsp, 0x28
1415455ed 488d6a30 lea rbp, [rdx + 0x30]
1415455f1 e87a332100 call 0x141758970
1415455f6 cc int3 
1415455f7 660f1f840000000000 nop word ptr [rax + rax]
141545600 4889542410 mov qword ptr [rsp + 0x10], rdx
141545605 55 push rbp
141545606 56 push rsi
141545607 57 push rdi
141545608 53 push rbx
141545609 4883ec28 sub rsp, 0x28
14154560d 488d6a30 lea rbp, [rdx + 0x30]
141545611 e85a332100 call 0x141758970
141545616 cc int3 
141545617 660f1f840000000000 nop word ptr [rax + rax]
141545620 4889542410 mov qword ptr [rsp + 0x10], rdx
141545625 55 push rbp
141545626 56 push rsi
141545627 57 push rdi
141545628 53 push rbx
141545629 4883ec28 sub rsp, 0x28
14154562d 488d6a30 lea rbp, [rdx + 0x30]
141545631 e83a332100 call 0x141758970
141545636 cc int3 
141545637 660f1f840000000000 nop word ptr [rax + rax]
141545640 4889542410 mov qword ptr [rsp + 0x10], rdx
141545645 55 push rbp
141545646 56 push rsi
141545647 57 push rdi
141545648 53 push rbx
141545649 4883ec28 sub rsp, 0x28
14154564d 488d6a30 lea rbp, [rdx + 0x30]
141545651 e81a332100 call 0x141758970
141545656 cc int3 
141545657 660f1f840000000000 nop word ptr [rax + rax]
141545660 4889542410 mov qword ptr [rsp + 0x10], rdx
141545665 55 push rbp
141545666 56 push rsi
141545667 57 push rdi
141545668 53 push rbx
141545669 4883ec28 sub rsp, 0x28
14154566d 488d6a30 lea rbp, [rdx + 0x30]
141545671 e8fa322100 call 0x141758970
141545676 cc int3 
141545677 cc int3 
141545678 cc int3 
141545679 cc int3 
14154567a cc int3 
14154567b cc int3 
14154567c cc int3 
14154567d cc int3 
14154567e cc int3 
14154567f cc int3 
141545680 56 push rsi
141545681 57 push rdi
141545682 53 push rbx
141545683 4883ec30 sub rsp, 0x30
141545687 4c89c7 mov rdi, r8
14154568a 89d3 mov ebx, edx
14154568c 4889ce mov rsi, rcx
14154568f e86cd0a9ff call 0x140fe2700
141545694 84c0 test al, al
141545696 740a je 0x1415456a2
141545698 b001 mov al, 1
14154569a 4883c430 add rsp, 0x30
14154569e 5b pop rbx
14154569f 5f pop rdi