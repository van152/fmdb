__int64 __fastcall sub_144543630(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  _DWORD *v9; // rbx
  _DWORD *v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  char v14; // [rsp+2Fh] [rbp-29h] BYREF
  int v15; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v16[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v14 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v14, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v16[0] = *(_DWORD *)(a1 + 24);
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v16, 4);
  if ( v8[4] != 0 )
    return 0;
  v9 = (_DWORD *)*a2;
  v15 = *(_DWORD *)(a1 + 28);
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v9 + 40LL))(v9, &v15, 4);
  if ( v9[4] != 0 )
    return 0;
  v10 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 36, 1);
  if ( v10[4] != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 2);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 34, 2);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, 0, a4);
}
