__int64 __fastcall sub_1440212F0(__int64 a1)
{
  __int64 v1; // rax
  unsigned __int64 v3; // rax
  __int64 v4; // r14
  __int64 v5; // rsi
  __int64 v6; // rdi
  __int64 v7; // rax
  __int64 v8; // rcx
  __int64 v9; // rbx
  unsigned int v10; // eax
  __int64 v11; // rcx

  v1 = *(_QWORD *)(a1 + 104) - *(_QWORD *)(a1 + 96);
  if ( v1 == 0 )
    return 0;
  v3 = v1 >> 3;
  v4 = 1;
  if ( v3 >= 2 )
    v4 = v3;
  v5 = 0;
  while ( 1 )
  {
    v6 = *(_QWORD *)(*(_QWORD *)(a1 + 96) + 8 * v5);
    if ( v6 != 0 )
    {
      v7 = sub_140DE1C70(*(int *)(*(_QWORD *)(v6 + 8) + 8LL) + v6 + 344, a1, 0);
      if ( v7 != 0 )
      {
        v9 = v7;
        LOBYTE(v8) = 50;
        if ( (unsigned __int8)sub_141033EF0(v8, *(unsigned __int8 *)(v7 + 28)) != 0 )
          break;
        v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v9 + 104LL))(v9);
        LOBYTE(v11) = 50;
        if ( (unsigned __int8)sub_141033EF0(v11, v10) != 0 )
          break;
      }
    }
    if ( v4 == ++v5 )
      return 0;
  }
  return v6;
}
