bool __fastcall sub_14439E0E0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  int v6; // ebp
  __int64 v7; // rbx
  int v8; // ebp
  __int64 v9; // rbx
  _DWORD *v11; // rdi
  _BYTE v12[33]; // [rsp+27h] [rbp-21h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v12, a3: 1);
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
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v7 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 4, a3: 4);
  }
  v8 = *(_DWORD *)(v7 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v7 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v7)(a1: v7, a2: 1);
  if ( v8 != 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(a1: v11, a2: a1 + 12, a3: 4);
  return v11[4] == 0;
}
