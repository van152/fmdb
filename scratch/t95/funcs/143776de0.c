void __fastcall sub_143776DE0(__int64 *a1, unsigned __int64 a2, __int64 *a3, __int64 *a4)
{
  __int64 v7; // rsi
  __int64 v8; // r13
  __int64 v9; // r15
  __int64 v10; // rsi
  __int64 (__fastcall *i)(__int64); // r12
  __int64 v12; // rbx
  __int64 v13; // rax
  __int64 v14; // rdi

  if ( a2 != 0 )
  {
    if ( a2 >> 60 != 0 )
      sub_1400526C0(a1);
    v7 = 16 * a2;
    v8 = sub_1407E4490(qword_141ABD470, 16 * a2);
    *a1 = v8;
    a1[1] = v8;
    a1[2] = v8 + v7;
    v9 = *a4;
    v10 = *a3;
    for ( i = MEMORY[0x1419475D0]; v10 != v9; v10 += 16 )
    {
      *(_DWORD *)v8 = *(_DWORD *)v10;
      v12 = sub_140836BC0();
      v13 = i(v12 + 32);
      v14 = v13;
      if ( v13 != 0 && *(_BYTE *)(v12 + 72) != 0 )
        _InterlockedIncrement((volatile signed __int32 *)(v12 + 64));
      if ( v13 == 0 )
        v14 = sub_1412D31C0(
                v12,
                *(unsigned int *)(v12 + 80),
                *(unsigned int *)(v12 + 4LL * (*(_DWORD *)(v12 + 56) != 0) + 84));
      if ( v14 != 0 && *(_BYTE *)(v12 + 96) != 0 )
        sub_141758A10(v14, 0, *(unsigned int *)(v12 + 80));
      (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(***(_QWORD ***)(v10 + 8) + 24LL))(
        **(_QWORD **)(v10 + 8),
        *(_QWORD *)(v10 + 8),
        v14);
      *(_QWORD *)(v8 + 8) = v14;
      v8 += 16;
    }
    a1[1] = v8;
  }
}
