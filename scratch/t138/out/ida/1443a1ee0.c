char __fastcall sub_1443A1EE0(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rcx
  __int64 v7; // rbx
  int v8; // ebp
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // r8
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  _DWORD *v22; // rdi
  char v23; // [rsp+36h] [rbp-22h] BYREF
  _BYTE v24[33]; // [rsp+37h] [rbp-21h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v24, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_140F91ED0(
                          a1: (unsigned int)&qword_141B5FDA8,
                          a2: (int)a1 + 8,
                          a3: (_DWORD)a2,
                          a4: qword_141B5FDE8,
                          a5: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return 0;
  v23 = 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v23, a3: 1);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return 0;
  if ( v23 != 0 )
  {
    v6 = *a1;
    if ( *a1 == 0 )
    {
      v6 = sub_140B526C0(a1: 40);
      *(_QWORD *)v6 = 0;
      *(_QWORD *)(v6 + 8) = 0;
      *(_QWORD *)(v6 + 16) = 0;
      *(_DWORD *)(v6 + 24) = 124518401;
      *(_QWORD *)(v6 + 28) = 0x4FFFFFFFFFFFFLL;
      *a1 = v6;
    }
    if ( (unsigned __int8)sub_141353C00(a1: v6, a2) == 0 )
      return 0;
  }
  else
  {
    *a1 = 0;
  }
  v7 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v7 + 8));
    (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: a1 + 4, a3: 4);
  }
  v8 = *(_DWORD *)(v7 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v7 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v7)(a1: v7, a2: 1);
  if ( v8 != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 42, a3: 2);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 5, a3: 2);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 46, a3: 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 6, a3: 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 50, a3: 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_140F83A50(a1: a1 + 2, a2) == 0 )
    return 0;
  LOBYTE(v14) = 4 - (byte_141B5FC2C == 0);
  if ( (unsigned __int8)sub_140F80980(a1: a1 + 3, a2, a3: v14) == 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 47, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 36, a3: 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 44, a3: 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 45, a3: 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  if ( v24[0] >= 2u )
  {
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 49, a3: 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return 0;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 51, a3: 1);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      return 0;
    v22 = (_DWORD *)*a2;
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v22 + 40LL))(a1: v22, a2: (__int64)a1 + 52, a3: 1);
    if ( v22[4] != 0 )
      return 0;
  }
  return 1;
}
