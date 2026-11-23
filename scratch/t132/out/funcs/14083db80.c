_QWORD *__fastcall sub_14083DB80(_QWORD *a1, __int64 *a2)
{
  __int64 v4; // r15
  __int64 v5; // rsi
  __int64 v6; // rax
  _QWORD *v7; // rbx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rdx

  v4 = sub_14083D4F0(a1);
  v5 = sub_14082ABE0();
  v6 = MEMORY[0x1419475D0](a1: v5 + 32);
  v7 = (_QWORD *)v6;
  if ( v6 != 0 && *(_BYTE *)(v5 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 64));
  if ( v6 == 0 )
    v7 = (_QWORD *)sub_1412D31C0(
                     a1: v5,
                     a2: *(unsigned int *)(v5 + 80),
                     a3: *(unsigned int *)(v5 + 4LL * (*(_DWORD *)(v5 + 56) != 0) + 84));
  if ( v7 != nullptr && *(_BYTE *)(v5 + 96) != 0 )
    sub_141758A10(a1: v7, a2: 0, a3: *(unsigned int *)(v5 + 80));
  v8 = a2[2];
  a2[2] = 0;
  v9 = *a2;
  v10 = a2[1];
  a2[1] = 0;
  *a2 = 0;
  *v7 = v9;
  v7[1] = v10;
  v7[2] = v8;
  a1[1] = v7;
  *a1 = v4 + 168;
  return a1;
}
