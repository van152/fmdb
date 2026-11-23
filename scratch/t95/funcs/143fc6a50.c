__int64 __fastcall sub_143FC6A50(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
  __int64 v12; // rax
  int v13; // eax
  _DWORD *v14; // rbx
  __int64 v15; // rax
  int v16; // eax
  _DWORD *v17; // rbx
  __int64 v18; // rbx
  __int64 v19; // rbx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rbx
  __int64 v23; // rbx
  unsigned __int8 v25; // [rsp+29h] [rbp-2Fh] BYREF
  bool v26; // [rsp+2Ah] [rbp-2Eh] BYREF
  char v27; // [rsp+2Bh] [rbp-2Dh] BYREF
  int v28; // [rsp+2Ch] [rbp-2Ch] BYREF
  int v29; // [rsp+30h] [rbp-28h] BYREF
  _DWORD v30[9]; // [rsp+34h] [rbp-24h] BYREF

  v7 = (_DWORD *)*a2;
  v27 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v27, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = *(_QWORD *)(a1 + 72);
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v30[0] = v10;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v8 + 40LL))(v8, v30, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  v12 = *(_QWORD *)(a1 + 56);
  v13 = v12 != 0 ? *(_DWORD *)(v12 + 8) : -1;
  v29 = v13;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v11 + 40LL))(v11, &v29, 4);
  if ( v11[4] != 0 )
    return 0;
  v14 = (_DWORD *)*a2;
  v15 = *(_QWORD *)(a1 + 64);
  v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
  v28 = v16;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v14 + 40LL))(v14, &v28, 4);
  if ( v14[4] != 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB89D0(a1 + 80, a2) == 0 )
    return 0;
  v17 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 4);
  if ( v17[4] != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 88, 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 89, 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 90, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v25 = (unsigned int)(*(_DWORD *)(a1 + 32) - *(_DWORD *)(a1 + 24)) >> 3;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned __int8 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v25, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  if ( v25 != 0 )
  {
    v22 = 0;
    while ( (unsigned __int8)sub_141192180(*(_QWORD *)(*(_QWORD *)(a1 + 24) + 8 * v22), a2) != 0 )
    {
      if ( ++v22 >= (unsigned __int64)v25 )
        goto LABEL_24;
    }
    return 0;
  }
LABEL_24:
  v26 = *(_QWORD *)(a1 + 48) != 0;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, bool *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v26, 1);
  if ( *(_DWORD *)(v23 + 16) != 0 || v26 && (unsigned __int8)sub_1415786E0(*(_QWORD *)(a1 + 48), a2) == 0 )
    return 0;
  return sub_140FE22B0(a1, a2, 0, a4);
}
