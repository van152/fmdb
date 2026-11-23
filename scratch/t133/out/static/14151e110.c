bool __fastcall sub_1444A71C0(_BYTE *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v6; // rsi
  _BYTE *v7; // rbx
  __int64 v8; // rdi
  char v9; // al
  __int64 v10; // rcx
  _BYTE v11[41]; // [rsp+2Fh] [rbp-29h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11, a3: 1);
  if ( *(_DWORD *)(v4 + 16) == 0 )
  {
    v6 = 12;
    if ( v11[0] >= 2u )
      v6 = (v11[0] == 2) ^ 0xFLL;
    v7 = a1;
    do
    {
      v8 = *a2;
      (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v7, a3: 1);
      if ( *(_DWORD *)(v8 + 16) != 0 )
        return false;
      ++v7;
      --v6;
    }
    while ( v6 != 0 );
    if ( v11[0] > 1u )
    {
      if ( v11[0] != 2 )
        return *(_DWORD *)(*a2 + 16LL) == 0;
      v9 = a1[4];
      v10 = 14;
    }
    else
    {
      v9 = a1[8];
      a1[12] = v9;
      v10 = 13;
    }
    a1[v10] = v9;
    return *(_DWORD *)(*a2 + 16LL) == 0;
  }
  return false;
}
