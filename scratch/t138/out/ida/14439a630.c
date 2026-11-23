bool __fastcall sub_14439A630(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // rbx
  __int64 v6; // rbx
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
  unsigned __int8 v18; // [rsp+2Bh] [rbp-1Dh] BYREF
  _DWORD v19[7]; // [rsp+2Ch] [rbp-1Ch] BYREF

  v18 = 0;
  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v18, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
    return false;
  v5 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 2, a3: 4);
  if ( *(_DWORD *)(v5 + 16) != 0 )
    return false;
  v6 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 20, a3: 4);
  if ( *(_DWORD *)(v6 + 16) != 0 )
    return false;
  v7 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 3, a3: 4);
  if ( *(_DWORD *)(v7 + 16) != 0 )
    return false;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 28, a3: 4);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return false;
  if ( (unsigned __int8)sub_140F925B0(
                          a1: (unsigned int)&qword_141B5FDA8,
                          a2: (int)a1 + 32,
                          a3: (_DWORD)a2,
                          a4: qword_141B5FDB8,
                          a5: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return false;
  if ( (unsigned __int8)sub_140F925B0(
                          a1: (unsigned int)&qword_141B5FDA8,
                          a2: (int)a1 + 40,
                          a3: (_DWORD)a2,
                          a4: qword_141B5FDB8,
                          a5: (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: a1 + 1, a2) == 0 )
    return false;
  if ( (unsigned __int8)sub_140DB8980(a1: (char *)a1 + 12, a2) == 0 )
    return false;
  v9 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 6, a3: 8);
  if ( *(_DWORD *)(v9 + 16) != 0 )
    return false;
  v10 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 7, a3: 4);
  if ( *(_DWORD *)(v10 + 16) != 0 )
    return false;
  if ( v18 >= 2u )
  {
    v12 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1, a3: 8);
    if ( *(_DWORD *)(v12 + 16) == 0 )
      goto LABEL_18;
    return false;
  }
  v19[0] = 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v19, a3: 4);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return false;
  *a1 = v19[0];
LABEL_18:
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 61, a3: 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return false;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 60, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return false;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 62, a3: 1);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return false;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: (__int64)a1 + 63, a3: 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return false;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
