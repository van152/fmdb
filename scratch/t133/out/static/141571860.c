char __fastcall sub_141571860(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  _WORD *v6; // r14
  __int64 v7; // rbx
  __int64 v8; // rbx
  __int64 v9; // rbx
  __int64 v10; // rbx
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
  __int64 v24; // rbx
  __int64 v25; // rbx
  __int64 v26; // rbx
  __int64 v27; // rbx
  __int64 v28; // rbx
  __int64 v29; // rbx
  __int64 v30; // rbx
  _DWORD *v31; // rdi
  unsigned __int8 v32; // [rsp+2Fh] [rbp-29h] BYREF
  _DWORD v33[10]; // [rsp+30h] [rbp-28h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v32, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  sub_140814B10(a1: *a2, a2: v33, a3: a1 + 32);
  if ( v33[0] != 0 )
    return 0;
  sub_140814B10(a1: *a2, a2: v33, a3: a1 + 40);
  if ( v33[0] != 0 )
    return 0;
  sub_140814B10(a1: *a2, a2: v33, a3: a1 + 48);
  if ( v33[0] != 0 )
    return 0;
  v5 = *a2;
  v6 = (_WORD *)(a1 + 92);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 92, a3: 2);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return 0;
  if ( (unsigned __int16)(*v6 - 32) <= 0xFFE0u )
    *v6 = 1;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 96, a3: 1);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return 0;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 94, a3: 2);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 64, a3: 4);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 60, a3: 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  if ( v32 >= 2u )
  {
    v12 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 76, a3: 4);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      return 0;
    sub_141572E80(a1: v33, a2, a3: a1 + 8);
    if ( v33[0] != 0 )
      return 0;
    v13 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 105, a3: 1);
    if ( *(_DWORD *)(v13 + 16) != 0 || (unsigned __int8)sub_140DB8980(a1: a1 + 56, a2) == 0 )
      return 0;
  }
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 104, a3: 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 97, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 98, a3: 1);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 99, a3: 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  if ( v32 >= 5u )
  {
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 100, a3: 1);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return 0;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 80, a3: 4);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return 0;
  }
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 84, a3: 2);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 86, a3: 2);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 88, a3: 2);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 90, a3: 2);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return 0;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 101, a3: 1);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return 0;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 102, a3: 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return 0;
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 103, a3: 1);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    return 0;
  v27 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 68, a3: 4);
  if ( *(_DWORD *)(v27 + 16) != 0 )
    return 0;
  v28 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 72, a3: 4);
  if ( *(_DWORD *)(v28 + 16) != 0 )
    return 0;
  if ( v32 >= 3u
    && ((v29 = *a2,
         (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 106, a3: 1),
         *(_DWORD *)(v29 + 16) != 0)
     || v32 >= 4u
     && ((v30 = *a2,
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 107, a3: 1),
          *(_DWORD *)(v30 + 16) != 0)
      || v32 >= 6u
      && (v31 = (_DWORD *)*a2,
          (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v31 + 40LL))(a1: v31, a2: a1 + 108, a3: 1),
          v31[4] != 0))) )
  {
    return 0;
  }
  else
  {
    return 1;
  }
}
