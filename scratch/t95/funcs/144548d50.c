bool __fastcall sub_144548D50(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rsi
  __int64 v6; // rsi
  __int64 v7; // rsi
  _DWORD *v8; // rdi
  __int64 v9; // rdx
  char v11; // [rsp+2Fh] [rbp-29h] BYREF
  _DWORD v12[10]; // [rsp+30h] [rbp-28h] BYREF

  v4 = (_DWORD *)*a2;
  v11 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v4 + 40LL))(v4, &v11, 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 59, 1);
  if ( v5[4] != 0 )
    return false;
  if ( (*(_BYTE *)(a1 + 59) & 1) != 0 )
  {
    sub_1408149D0(*a2, v12, a1 + 24);
    if ( v12[0] != 0 )
      return false;
  }
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = (_DWORD *)*a2;
  v9 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v8 + 40LL))(v8, v9, 4);
  return v8[4] == 0;
}
