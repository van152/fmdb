bool __fastcall sub_144354740(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rsi
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  _DWORD *v14; // rbx
  __int64 v15; // rax
  int v16; // eax
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  _DWORD *v24; // rdi
  __int64 v25; // rdx
  char v26; // [rsp+2Fh] [rbp-29h] BYREF
  int v27; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v28[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v26 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v26, 1);
  if ( v7[4] != 0 )
    return false;
  if ( a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 24);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    v28[0] = v11;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v28, 4);
    if ( v9[4] != 0 )
      return false;
    v12 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 80, 2);
    if ( v12[4] != 0 )
      return false;
    v13 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 82, 2);
    if ( *(_DWORD *)(v13 + 16) != 0 )
      return false;
    v14 = (_DWORD *)*a2;
    v15 = *(_QWORD *)(a1 + 32);
    v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
    v27 = v16;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v14 + 40LL))(v14, &v27, 4);
    if ( v14[4] != 0 )
      return false;
    v17 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 1);
    if ( *(_DWORD *)(v17 + 16) != 0 )
      return false;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 85, 1);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return false;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 86, 1);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return false;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 76, 4);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return false;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 87, 1);
    if ( *(_DWORD *)(v21 + 16) != 0 || (unsigned __int8)sub_140FEA120(a1 + 48, a2) == 0 )
      return false;
  }
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return false;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return false;
  v24 = (_DWORD *)*a2;
  v25 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v24 + 40LL))(v24, v25, 4);
  return v24[4] == 0;
}
