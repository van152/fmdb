char __fastcall sub_141470930(__int64 *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rbx
  int v9; // ebp
  __int64 v10; // rbx
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
  __int64 v23; // rbx
  __int64 v24; // rbx
  _DWORD *v25; // rdi
  char v26; // [rsp+4Eh] [rbp-2Ah] BYREF
  char v27[41]; // [rsp+4Fh] [rbp-29h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v27, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return 0;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 1, a3: 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return 0;
  v26 = 0;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v26, a3: 1);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return 0;
  if ( v26 != 0 )
  {
    if ( dword_141B5B8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(a1: &dword_141B5B8D0);
      if ( dword_141B5B8D0 == -1 )
      {
        sub_1407E53D0(a1: (unsigned int)&unk_141B5B880, a2: 1100152096, a3: 64, a4: 40, a5: 0, a6: 0, a7: 64, a8: 4096);
        sub_141751048(a1: sub_140B56FE0);
        sub_141750EA0(a1: &dword_141B5B8D0);
      }
    }
    v7 = sub_1407E58C0(a1: &unk_141B5B880, a2: 40);
    *(_QWORD *)v7 = 0;
    *(_QWORD *)(v7 + 8) = 0;
    *(_QWORD *)(v7 + 16) = 0;
    *(_DWORD *)(v7 + 24) = 124518401;
    *(_QWORD *)(v7 + 28) = 0x4FFFFFFFFFFFFLL;
    *a1 = v7;
    if ( (unsigned __int8)sub_141353D50(a1: v7, a2) == 0 )
      return 0;
  }
  v8 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v8 + 8));
    (*(void (__fastcall **)(__int64, __int64 *, __int64))(*(_QWORD *)v8 + 40LL))(a1: v8, a2: a1 + 4, a3: 4);
  }
  v9 = *(_DWORD *)(v8 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v8 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v8)(a1: v8, a2: 1);
  if ( v9 != 0 )
    return 0;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 42, a3: 2);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 5, a3: 2);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 46, a3: 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 6, a3: 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 50, a3: 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 51, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 2, a3: 4);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 3, a3: 4);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 47, a3: 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 36, a3: 4);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 44, a3: 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 45, a3: 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  if ( v27[0] >= 2u
    && ((v23 = *a2,
         (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
           a1: *a2,
           a2: (__int64)a1 + 49,
           a3: 1),
         *(_DWORD *)(v23 + 16) != 0)
     || (v24 = *a2,
         (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(
           a1: *a2,
           a2: (__int64)a1 + 51,
           a3: 1),
         *(_DWORD *)(v24 + 16) != 0)
     || (v25 = (_DWORD *)*a2,
         (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v25 + 40LL))(
           a1: v25,
           a2: (__int64)a1 + 52,
           a3: 1),
         v25[4] != 0)) )
  {
    return 0;
  }
  else
  {
    return 1;
  }
}
