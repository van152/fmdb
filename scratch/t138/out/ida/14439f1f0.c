bool __fastcall sub_14439F1F0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  int v7; // ebp
  __int64 v8; // rbx
  int v9; // ebp
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  _DWORD *v15; // rdi
  _BYTE v16[33]; // [rsp+27h] [rbp-21h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v16, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v6 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: a1 + 8, a3: 4);
  }
  v7 = *(_DWORD *)(v6 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v6 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v6)(a1: v6, a2: 1);
  if ( v7 != 0 )
    return false;
  v8 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v8 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a1 + 12, a3: 4);
  }
  v9 = *(_DWORD *)(v8 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v8)(a1: v8, a2: 1);
  if ( v9 != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 20, a3: 1);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 22, a3: 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return false;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 23, a3: 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return false;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 4);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  v15 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(a1: v15, a2: a1 + 21, a3: 1);
  return v15[4] == 0;
}
