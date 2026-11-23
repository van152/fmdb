__int64 __fastcall sub_1444E07D0(_QWORD *a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
  __int64 v12; // rax
  int v13; // eax
  _DWORD *v14; // rbx
  __int64 v15; // rbx
  _DWORD *v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  _DWORD v20[10]; // [rsp+20h] [rbp-28h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v20[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v20, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = a1[3];
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v20[0] = v10;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v20, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  v12 = a1[4];
  v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
  v20[0] = v13;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, v20, 4);
  if ( v11[4] != 0 )
    return 0;
  v20[0] = (a1[7] - a1[6]) >> 3;
  v14 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v20, 4);
  if ( v14[4] != 0 )
    return 0;
  if ( v20[0] != 0 )
  {
    v15 = 0;
    while ( (unsigned __int8)sub_140F82F50(*(_QWORD *)(a1[6] + 8 * v15), a2) != 0 )
    {
      if ( ++v15 >= (unsigned __int64)v20[0] )
        goto LABEL_15;
    }
    return 0;
  }
LABEL_15:
  v16 = (_DWORD *)*a2;
  if ( *(_DWORD *)(*a2 + 16LL) != 0 )
    return 0;
  v20[0] = (a1[10] - a1[9]) >> 3;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v16 + 40LL))(v16, v20, 4);
  if ( v16[4] != 0 )
    return 0;
  if ( v20[0] != 0 )
  {
    v17 = 0;
    while ( (unsigned __int8)sub_140F82F50(*(_QWORD *)(a1[9] + 8 * v17), a2) != 0 )
    {
      if ( ++v17 >= (unsigned __int64)v20[0] )
        goto LABEL_21;
    }
    return 0;
  }
LABEL_21:
  if ( *(_DWORD *)(*a2 + 16LL) != 0 )
    return 0;
  if ( (unsigned __int8)sub_1417266E0(a1 + 12, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_1417266E0(a1 + 15, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB89D0(a1 + 5, a2) == 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 44, 4);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  sub_14153F930(v20, a2, a1 + 18);
  if ( v20[0] != 0 )
    return 0;
  sub_14153F9C0(v20, a2, a1 + 21);
  if ( v20[0] != 0 )
    return 0;
  sub_14153F930(v20, a2, a1 + 24);
  if ( v20[0] != 0 )
    return 0;
  sub_14153F9C0(v20, a2, a1 + 27);
  if ( v20[0] != 0 )
    return 0;
  return sub_140FE22B0(a1, a2, 0, a4);
}
