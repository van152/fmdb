__int64 __fastcall sub_140931AC0(_QWORD *a1)
{
  _QWORD *v1; // rsi
  __int64 v2; // rax
  __int64 v3; // rax
  __int64 v4; // rcx
  unsigned __int64 i; // rbx
  __int64 *v6; // rdi
  char v7; // al
  __int64 v8; // rdx
  __int64 v9; // rax
  __int64 v10; // rdx

  v1 = a1;
  v2 = a1[24];
  if ( v2 != a1[25] )
  {
    do
    {
      v1 = *(_QWORD **)v2;
      v2 = *(_QWORD *)(*(_QWORD *)v2 + 192LL);
    }
    while ( v2 != v1[25] );
  }
  v3 = v1[56];
  v4 = v1[57];
  if ( v4 != v3 )
  {
    for ( i = 0; i < (v4 - v3) >> 3; ++i )
    {
      v6 = *(__int64 **)(v3 + 8 * i);
      if ( v6 != nullptr )
      {
        v7 = (*(__int64 (__fastcall **)(__int64 *))(*v6 + 624))(v6);
        v8 = *v6;
        if ( v7 != 0 )
          return (*(__int64 (__fastcall **)(__int64 *, _QWORD))(v8 + 1000))(v6, 0);
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *))(v8 + 632))(v6) != 0 )
          return (*(__int64 (__fastcall **)(__int64 *))(*v6 + 832))(v6);
        v3 = v1[56];
        v4 = v1[57];
      }
    }
  }
  v9 = v1[115];
  if ( v9 == 0 )
    return 0;
  v10 = *(unsigned int *)(v9 + 112);
  if ( (_DWORD)v10 == -1 )
    return 0;
  else
    return sub_140F45DB0(qword_141B5FDC0, v10);
}
