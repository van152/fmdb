_QWORD *__fastcall sub_14083DC80(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // r15
  __int64 v5; // rsi
  __int64 v6; // rax
  _QWORD *v7; // rdi

  v4 = sub_14083D4F0(a1);
  v5 = sub_1408433F0();
  v6 = MEMORY[0x1419475D0](v5 + 32);
  v7 = (_QWORD *)v6;
  if ( v6 != 0 && *(_BYTE *)(v5 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 64));
  if ( v6 == 0 )
    v7 = (_QWORD *)sub_1412D31C0(
                     v5,
                     *(unsigned int *)(v5 + 80),
                     *(unsigned int *)(v5 + 4LL * (*(_DWORD *)(v5 + 56) != 0) + 84));
  if ( v7 != nullptr && *(_BYTE *)(v5 + 96) != 0 )
    sub_141758A10(v7, 0, *(unsigned int *)(v5 + 80));
  v7[2] = 0;
  v7[1] = 0;
  *v7 = 0;
  sub_1408367A0(v7, (__int64)(a2[1] - *a2) >> 4, a2, a2 + 1);
  a1[1] = v7;
  *a1 = v4 + 184;
  return a1;
}
