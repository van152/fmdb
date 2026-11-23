bool __fastcall sub_14432AD70(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  int v6; // ebp
  __int64 v7; // rbx
  __int64 v8; // rbx
  int v9; // ebp
  __int64 v10; // rbx
  _DWORD *v11; // rdi
  _BYTE v13[34]; // [rsp+26h] [rbp-22h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v13, a3: 2);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v5 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v5 + 40LL))(a1: v5, a2: a1 + 16, a3: 4);
  }
  v6 = *(_DWORD *)(v5 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v5 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v5)(a1: v5, a2: 1);
  if ( v6 != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 28, a3: 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v8 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a1 + 20, a3: 4);
  }
  v9 = *(_DWORD *)(v8 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v8)(a1: v8, a2: 1);
  if ( v9 != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
  if ( *(_DWORD *)(v10 + 16) != 0 || (unsigned __int8)sub_140DB8980(a1: a1 + 24, a2) == 0 )
    return false;
  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(a1: v11, a2: a1 + 12, a3: 4);
  return v11[4] == 0;
}
