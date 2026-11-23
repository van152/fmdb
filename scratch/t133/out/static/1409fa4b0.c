__int64 __fastcall sub_14392CEB0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int16 *v7; // r12
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
  __int64 v11; // rbx
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  __int64 v15; // rbx
  __int64 v16; // rbx
  __int64 v17; // rbx
  __int64 v18; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rbx
  __int16 *v24; // r15
  int v25; // eax
  __int16 v26; // cx
  unsigned __int8 v27; // [rsp+26h] [rbp-32h] BYREF
  _BYTE v28[49]; // [rsp+27h] [rbp-31h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v27, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return 0;
  v6 = *a2;
  v7 = (__int16 *)(a1 + 84);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 84, a3: 2);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return 0;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 86, a3: 2);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 8, a3: 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 16, a3: 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 24, a3: 4);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 32, a3: 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 48, a3: 4);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 56, a3: 4);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  if ( v27 < 2u )
  {
    *(_QWORD *)(a1 + 64) = -1;
  }
  else
  {
    v15 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 64, a3: 4);
    if ( *(_DWORD *)(v15 + 16) != 0 )
      return 0;
  }
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 40, a3: 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 72, a3: 4);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 94, a3: 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  if ( v27 >= 3u )
  {
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 92, a3: 2);
    if ( *(_DWORD *)(v20 + 16) == 0 )
      goto LABEL_24;
    return 0;
  }
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v28, a3: 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  *(_WORD *)(a1 + 92) = v28[0];
LABEL_24:
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 88, a3: 2);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v23 = *a2;
  v24 = (__int16 *)(a1 + 90);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 90, a3: 2);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return 0;
  v25 = *v24;
  if ( v25 >= 1901 )
  {
    v26 = *v7;
    if ( (__int16)v25 < *v7 )
    {
      *v24 = v26;
      *(_WORD *)(a1 + 88) = v26;
    }
  }
  return sub_140DB8980(a1: a1 + 80, a2);
}
