0x1444dff00  4156                     push r14 <<
0x1444dff02  56                       push rsi
0x1444dff03  57                       push rdi
0x1444dff04  53                       push rbx
0x1444dff05  4883ec28                 sub rsp, 0x28
0x1444dff09  4d89ce                   mov r14, r9
0x1444dff0c  4889d7                   mov rdi, rdx
0x1444dff0f  4889cb                   mov rbx, rcx
0x1444dff12  488b32                   mov rsi, qword ptr [rdx]
0x1444dff15  488d5118                 lea rdx, [rcx + 0x18]
0x1444dff19  488b06                   mov rax, qword ptr [rsi]
0x1444dff1c  41b804000000             mov r8d, 4
0x1444dff22  4889f1                   mov rcx, rsi
0x1444dff25  ff5028                   call qword ptr [rax + 0x28]
0x1444dff28  837e1000                 cmp dword ptr [rsi + 0x10], 0
0x1444dff2c  0f850c010000             jne 0x1444e003e
0x1444dff32  488b37                   mov rsi, qword ptr [rdi]
0x1444dff35  488d5320                 lea rdx, [rbx + 0x20]
0x1444dff39  488b06                   mov rax, qword ptr [rsi]
0x1444dff3c  41b804000000             mov r8d, 4
0x1444dff42  4889f1                   mov rcx, rsi
0x1444dff45  ff5028                   call qword ptr [rax + 0x28]
0x1444dff48  837e1000                 cmp dword ptr [rsi + 0x10], 0
0x1444dff4c  0f85ec000000             jne 0x1444e003e
0x1444dff52  488d4b30                 lea rcx, [rbx + 0x30]
0x1444dff56  4889fa                   mov rdx, rdi
0x1444dff59  e8126824fd               call 0x141726770
0x1444dff5e  84c0                     test al, al
0x1444dff60  0f84d8000000             je 0x1444e003e
0x1444dff66  488d4b48                 lea rcx, [rbx + 0x48]
0x1444dff6a  4889fa                   mov rdx, rdi
0x1444dff6d  e8fe6724fd               call 0x141726770
0x1444dff72  84c0                     test al, al
0x1444dff74  0f84c4000000             je 0x1444e003e
0x1444dff7a  488d4b60                 lea rcx, [rbx + 0x60]
0x1444dff7e  4889fa                   mov rdx, rdi
0x1444dff81  e8ea6724fd               call 0x141726770
0x1444dff86  84c0                     test al, al
0x1444dff88  0f84b0000000             je 0x1444e003e
0x1444dff8e  488d4b78                 lea rcx, [rbx + 0x78]
0x1444dff92  4889fa                   mov rdx, rdi
0x1444dff95  e8d66724fd               call 0x141726770
0x1444dff9a  84c0                     test al, al
0x1444dff9c  0f849c000000             je 0x1444e003e
0x1444dffa2  488d4b28                 lea rcx, [rbx + 0x28]
0x1444dffa6  4889fa                   mov rdx, rdi
0x1444dffa9  e8d2898dfc               call 0x140db8980
0x1444dffae  84c0                     test al, al
0x1444dffb0  0f8488000000             je 0x1444e003e
0x1444dffb6  488b37                   mov rsi, qword ptr [rdi]
0x1444dffb9  488d532c                 lea rdx, [rbx + 0x2c]
0x1444dffbd  488b06                   mov rax, qword ptr [rsi]
0x1444dffc0  41b804000000             mov r8d, 4
0x1444dffc6  4889f1                   mov rcx, rsi
0x1444dffc9  ff5028                   call qword ptr [rax + 0x28]
0x1444dffcc  837e1000                 cmp dword ptr [rsi + 0x10], 0
0x1444dffd0  756c                     jne 0x1444e003e
0x1444dffd2  4c8d8390000000           lea r8, [rbx + 0x90]
0x1444dffd9  488d4c2420               lea rcx, [rsp + 0x20]
0x1444dffde  4889fa                   mov rdx, rdi
0x1444dffe1  e81a1006fd               call 0x141541000
0x1444dffe6  837c242000               cmp dword ptr [rsp + 0x20], 0
0x1444dffeb  7551                     jne 0x1444e003e
0x1444dffed  4c8d83a8000000           lea r8, [rbx + 0xa8]
0x1444dfff4  488d4c2420               lea rcx, [rsp + 0x20]
0x1444dfff9  4889fa                   mov rdx, rdi
0x1444dfffc  e87f1406fd               call 0x141541480
0x1444e0001  837c242000               cmp dword ptr [rsp + 0x20], 0
0x1444e0006  7536                     jne 0x1444e003e
0x1444e0008  4c8d83c0000000           lea r8, [rbx + 0xc0]
0x1444e000f  488d4c2420               lea rcx, [rsp + 0x20]
0x1444e0014  4889fa                   mov rdx, rdi
0x1444e0017  e8e40f06fd               call 0x141541000
0x1444e001c  837c242000               cmp dword ptr [rsp + 0x20], 0
0x1444e0021  751b                     jne 0x1444e003e
0x1444e0023  4c8d83d8000000           lea r8, [rbx + 0xd8]
0x1444e002a  488d4c2420               lea rcx, [rsp + 0x20]
0x1444e002f  4889fa                   mov rdx, rdi
0x1444e0032  e8491406fd               call 0x141541480
0x1444e0037  837c242000               cmp dword ptr [rsp + 0x20], 0
0x1444e003c  740c                     je 0x1444e004a
0x1444e003e  31c0                     xor eax, eax
0x1444e0040  4883c428                 add rsp, 0x28
0x1444e0044  5b                       pop rbx
0x1444e0045  5f                       pop rdi
0x1444e0046  5e                       pop rsi
0x1444e0047  415e                     pop r14
0x1444e0049  c3                       ret 
0x1444e004a  4889d9                   mov rcx, rbx
0x1444e004d  4889fa                   mov rdx, rdi
0x1444e0050  4531c0                   xor r8d, r8d
0x1444e0053  4d89f1                   mov r9, r14
0x1444e0056  4883c428                 add rsp, 0x28
0x1444e005a  5b                       pop rbx
0x1444e005b  5f                       pop rdi
0x1444e005c  5e                       pop rsi
0x1444e005d  415e                     pop r14
0x1444e005f  e9dcecacfc               jmp 0x140faed40
0x1444e0064  cc                       int3 
0x1444e0065  0f1f00                   nop dword ptr [rax]
