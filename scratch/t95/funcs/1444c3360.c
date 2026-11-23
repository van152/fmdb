bool __fastcall sub_1444C3360(_DWORD *a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  _DWORD *v6; // rbx
  _DWORD *v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  _DWORD *v10; // rdi
  __int64 v11; // rdx
  char v13; // [rsp+2Fh] [rbp-29h] BYREF
  int v14; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v15[9]; // [rsp+34h] [rbp-24h] BYREF

  v4 = (_DWORD *)*a2;
  v13 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v4 + 40LL))(v4, &v13, 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  v15[0] = a1[6];
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v5 + 40LL))(v5, v15, 4);
  if ( v5[4] != 0 )
    return false;
  v6 = (_DWORD *)*a2;
  v14 = a1[7];
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v6 + 40LL))(v6, &v14, 4);
  if ( v6[4] != 0 )
    return false;
  v7 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 2);
  if ( v7[4] != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 2, 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 3, 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = (_DWORD *)*a2;
  v11 = (__int64)(a1[4] != 0 ? a1 + 4 : a1 + 3);
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, v11, 4);
  return v10[4] == 0;
}
