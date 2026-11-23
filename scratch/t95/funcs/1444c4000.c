__int64 __fastcall sub_1444C4000(__int64 a1, _QWORD *a2, unsigned int a3, unsigned int a4)
{
  _DWORD *v8; // rbp
  _DWORD *v9; // rbp
  __int64 v10; // rbp
  __int64 v11; // rbp
  __int64 v12; // rbp
  __int64 v13; // rbp
  _BYTE v15[41]; // [rsp+2Fh] [rbp-29h] BYREF

  v8 = (_DWORD *)*a2;
  v15[0] = 0;
  (*(void (__fastcall **)(_DWORD *, _BYTE *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v15, 1);
  if ( v8[4] != 0 )
    return 0;
  v9 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( v9[4] != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 28, 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 33, 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 34, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  else
    return sub_140FE22B0(a1, a2, a3, a4);
}
