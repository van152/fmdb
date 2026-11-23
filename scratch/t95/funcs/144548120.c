bool __fastcall sub_144548120(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rax
  int v7; // eax
  _DWORD *v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  _DWORD *v12; // rdi
  __int64 v13; // rdx
  char v15; // [rsp+23h] [rbp-25h] BYREF
  _DWORD v16[9]; // [rsp+24h] [rbp-24h] BYREF

  v4 = (_DWORD *)*a2;
  v15 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v4 + 40LL))(v4, &v15, 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  v6 = *(_QWORD *)(a1 + 24);
  v7 = v6 != 0 ? *(_DWORD *)(v6 + 8) : -1;
  v16[0] = v7;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v5 + 40LL))(v5, v16, 4);
  if ( v5[4] != 0 )
    return false;
  v8 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 2);
  if ( v8[4] != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 34, 2);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return false;
  v12 = (_DWORD *)*a2;
  v13 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(v12, v13, 4);
  return v12[4] == 0;
}
