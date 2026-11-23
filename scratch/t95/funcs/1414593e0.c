__int64 __fastcall sub_1414593E0(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  _DWORD *v11; // rbx
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
  _DWORD *v25; // rbx
  __int64 v27; // r14
  __int64 v28; // r12
  unsigned __int64 v29; // r13
  __int64 v30; // rax
  int v31; // eax
  _DWORD *v32; // rbx
  __int64 v33; // rbx
  _DWORD *v34; // rbx
  __int64 v35; // rax
  int v36; // eax
  char v37; // [rsp+29h] [rbp-4Fh] BYREF
  __int16 v38; // [rsp+2Ah] [rbp-4Eh] BYREF
  int v39; // [rsp+2Ch] [rbp-4Ch] BYREF
  int v40; // [rsp+30h] [rbp-48h] BYREF
  _DWORD v41[17]; // [rsp+34h] [rbp-44h] BYREF

  v7 = (_DWORD *)*a2;
  v37 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v7 + 40LL))(v7, &v37, 1);
  if ( v7[4] != 0 )
    return 0;
  v8 = (_DWORD *)*a2;
  v9 = *(_QWORD *)(a1 + 96);
  v10 = v9 != 0 ? *(_DWORD *)(v9 + 8) : -1;
  v40 = v10;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v8 + 40LL))(v8, &v40, 4);
  if ( v8[4] != 0 )
    return 0;
  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 112, 4);
  if ( v11[4] != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 72, 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 73, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 74, 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 75, 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 76, 1);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 77, 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 78, 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 79, 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 80, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 81, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 82, 1);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 84, 2);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return 0;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 86, 1);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return 0;
  v25 = (_DWORD *)*a2;
  v38 = (unsigned int)(*(_DWORD *)(a1 + 56) - *(_DWORD *)(a1 + 48)) >> 4;
  (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v25 + 40LL))(v25, &v38, 2);
  if ( v25[4] != 0 )
    return 0;
  v27 = *(_QWORD *)(a1 + 48);
  if ( *(_QWORD *)(a1 + 56) != v27 )
  {
    v28 = 8;
    v29 = 0;
    do
    {
      v30 = *(_QWORD *)(v27 + v28 - 8);
      v31 = v30 != 0 ? *(_DWORD *)(v30 + 8) : -1;
      v32 = (_DWORD *)*a2;
      v41[0] = v31;
      (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v32 + 40LL))(v32, v41, 4);
      if ( v32[4] != 0 )
        return 0;
      v33 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v28 + v27, 1);
      if ( *(_DWORD *)(v33 + 16) != 0 )
        return 0;
      ++v29;
      v27 = *(_QWORD *)(a1 + 48);
      v28 += 16;
    }
    while ( v29 < (*(_QWORD *)(a1 + 56) - v27) >> 4 );
  }
  v34 = (_DWORD *)*a2;
  v35 = *(_QWORD *)(a1 + 104);
  v36 = v35 != 0 ? *(_DWORD *)(v35 + 8) : -1;
  v39 = v36;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v34 + 40LL))(v34, &v39, 4);
  if ( v34[4] != 0 )
    return 0;
  return sub_140FE22B0(a1, a2, 0, a4);
}
