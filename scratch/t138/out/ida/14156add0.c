bool __fastcall sub_14156ADD0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  int v6; // ebp
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  _DWORD *v15; // rbx
  char v17; // [rsp+25h] [rbp-23h] BYREF
  _BYTE v18[34]; // [rsp+26h] [rbp-22h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v18, a3: 2);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1, a3: 4);
  }
  v6 = *(_DWORD *)(v5 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v5)(a1: v5, a2: 1);
  if ( v6 != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 20, a3: 4);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 24, a3: 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 28, a3: 2);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v17, a3: 1);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return false;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 12, a3: 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return false;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 4, a3: 4);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return false;
  v15 = (_DWORD *)*a2;
  if ( *(_DWORD *)(*a2 + 16LL) != 0 )
    return false;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v15 + 40LL))(a1: *a2, a2: a1 + 30, a3: 1);
  return v15[4] == 0 && *(_DWORD *)(*a2 + 16LL) == 0;
}
