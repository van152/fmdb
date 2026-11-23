bool __fastcall sub_144557D40(__int64 a1, _QWORD *a2)
{
  _DWORD *v4; // rbx
  _DWORD *v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  __int64 v8; // rbx
  _DWORD *v9; // rdi
  __int64 v10; // rdx
  _BYTE v12[33]; // [rsp+27h] [rbp-21h] BYREF

  v4 = (_DWORD *)*a2;
  v12[0] = 0;
  (*(void (__fastcall **)(_DWORD *, _BYTE *, __int64))(*(_QWORD *)v4 + 40LL))(v4, v12, 1);
  if ( v4[4] != 0 )
    return false;
  v5 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 1);
  if ( v5[4] != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 33, 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 8, 4);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 12, 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = (_DWORD *)*a2;
  v10 = *(_DWORD *)(a1 + 16) != 0 ? a1 + 16 : a1 + 12;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v9 + 40LL))(v9, v10, 4);
  return v9[4] == 0;
}
