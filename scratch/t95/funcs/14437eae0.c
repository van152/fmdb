bool __fastcall sub_14437EAE0(__int64 a1, _QWORD *a2, __int64 a3, char a4)
{
  _DWORD *v7; // rsi
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbx
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // rsi
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  _DWORD *v20; // rdi
  __int64 v21; // rdx
  char v22; // [rsp+2Fh] [rbp-29h] BYREF
  int v23; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v24[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v22 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v22, 1);
  if ( v7[4] != 0 )
    return false;
  if ( a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 24);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    v24[0] = v11;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v24, 4);
    if ( v9[4] != 0 )
      return false;
    v12 = (_DWORD *)*a2;
    v13 = *(_QWORD *)(a1 + 32);
    v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
    v23 = v14;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v12 + 40LL))(v12, &v23, 4);
    if ( v12[4] != 0 )
      return false;
    v15 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 60, 1);
    if ( v15[4] != 0 )
      return false;
    v16 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 56, 2);
    if ( *(_DWORD *)(v16 + 16) != 0 )
      return false;
    v17 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 58, 1);
    if ( *(_DWORD *)(v17 + 16) != 0
      || (unsigned __int8)sub_140DB89D0(a1 + 40, a2) == 0
      || (unsigned __int8)sub_140DB89D0(a1 + 44, a2) == 0 )
    {
      return false;
    }
  }
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return false;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return false;
  v20 = (_DWORD *)*a2;
  v21 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v20 + 40LL))(v20, v21, 4);
  return v20[4] == 0;
}
