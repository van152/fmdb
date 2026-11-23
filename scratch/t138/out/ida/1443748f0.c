bool __fastcall sub_1443748F0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rbx
  int v8; // ebp
  __int64 v9; // rbx
  int v10; // ebp
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rbx
  _DWORD *v25; // rdi
  _BYTE v26[33]; // [rsp+27h] [rbp-21h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v26, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 53, a3: 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v7 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1, a3: 4);
  }
  v8 = *(_DWORD *)(v7 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v7 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v7)(a1: v7, a2: 1);
  if ( v8 != 0 )
    return false;
  v9 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v9 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v9 + 40LL))(a1: v9, a2: a1 + 4, a3: 4);
  }
  v10 = *(_DWORD *)(v9 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v9 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v9)(a1: v9, a2: 1);
  if ( v10 != 0 )
    return false;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 50, a3: 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return false;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 20, a3: 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return false;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 42, a3: 2);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 44, a3: 2);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return false;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 49, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return false;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 46, a3: 2);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 8, a2) == 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 12, a2) == 0 )
    return false;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 48, a3: 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return false;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 52, a3: 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return false;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 51, a3: 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return false;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 24, a3: 4);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return false;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 40, a3: 2);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return false;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 28, a3: 4);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return false;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 32, a3: 4);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return false;
  v25 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(a1: v25, a2: a1 + 36, a3: 4);
  return v25[4] == 0;
}
