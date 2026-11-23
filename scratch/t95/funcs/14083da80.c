_QWORD *__fastcall sub_14083DA80(_QWORD *a1, __int64 a2)
{
  __int64 v4; // rdi
  __int64 v5; // rbx
  __int64 v6; // rax
  __int64 v7; // rsi

  v4 = sub_14083D4F0(a1);
  v5 = sub_14082ABE0();
  v6 = MEMORY[0x1419475D0](v5 + 32);
  v7 = v6;
  if ( v6 != 0 && *(_BYTE *)(v5 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 64));
  if ( v6 == 0 )
    v7 = sub_1412D31C0(v5, *(unsigned int *)(v5 + 80), *(unsigned int *)(v5 + 4LL * (*(_DWORD *)(v5 + 56) != 0) + 84));
  if ( v7 != 0 && *(_BYTE *)(v5 + 96) != 0 )
    sub_141758A10(v7, 0, *(unsigned int *)(v5 + 80));
  sub_14083ADC0(v7, a2);
  a1[1] = v7;
  *a1 = v4 + 168;
  return a1;
}
