bool __fastcall sub_1445438A0(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  _DWORD *v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  _DWORD *v10; // rdi
  __int64 v11; // rdx
  char v13; // [rsp+23h] [rbp-25h] BYREF
  _DWORD v14[9]; // [rsp+24h] [rbp-24h] BYREF

  v4 = (_DWORD *)*a2;
  v13 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v4 + 40LL))(v4, &v13, 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  v14[0] = *(_DWORD *)(a1 + 24);
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v5 + 40LL))(v5, v14, 4);
  if ( v5[4] != 0 )
    return false;
  v6 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 28, 1);
  if ( v6[4] != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 30, 2);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = (_DWORD *)*a2;
  v11 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, v11, 4);
  return v10[4] == 0;
}
