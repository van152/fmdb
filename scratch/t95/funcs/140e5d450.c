__int64 __fastcall sub_140E5D450(_QWORD *a1, _QWORD *a2, unsigned int a3, unsigned int a4)
{
  unsigned int v5; // ebx
  _DWORD *v8; // rbp
  _DWORD *v9; // rbp
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbp
  __int64 v13; // rax
  int v14; // eax
  _DWORD *v15; // rbp
  __int64 v16; // rax
  int v17; // eax
  _DWORD *v18; // rbp
  __int64 v19; // rax
  int v20; // eax
  _DWORD *v21; // rbp
  __int64 v22; // rax
  int v23; // eax
  _DWORD *v24; // rbp
  __int64 v25; // rbp
  __int64 v26; // rbp
  __int64 v28; // rbp
  __int64 v29; // rbp
  _DWORD *v30; // r14
  __int64 v31; // rax
  int v32; // eax
  __int64 v33; // rbp
  _DWORD *v34; // rcx
  unsigned int v35; // eax
  __int64 v36; // rbp
  __int64 v37; // rbp
  _DWORD *v38; // r12
  __int64 v39; // rax
  _DWORD *v40; // r14
  __int64 v41; // rcx
  char v42; // al
  __int64 v43; // rcx
  _DWORD *v44; // rcx
  unsigned int v45; // eax
  __int64 v46; // rbp
  __int64 v47; // rbp
  _DWORD *v48; // rcx
  unsigned int v49; // eax
  __int64 v50; // rbp
  __int64 v51; // rbp
  __int64 v52; // rbp
  _DWORD *v53; // rbp
  __int64 v54; // rax
  int v55; // eax
  int v56; // [rsp+28h] [rbp-40h] BYREF
  char v57; // [rsp+2Dh] [rbp-3Bh] BYREF
  char v58; // [rsp+2Eh] [rbp-3Ah] BYREF
  char v59[57]; // [rsp+2Fh] [rbp-39h] BYREF

  v5 = a3;
  if ( (_BYTE)a3 != 0 )
  {
    v8 = (_DWORD *)*a2;
    LOBYTE(v56) = 0;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v8 + 40LL))(v8, &v56, 1);
    if ( v8[4] != 0 )
      return 0;
  }
  v9 = (_DWORD *)*a2;
  v10 = a1[27];
  v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
  v56 = v11;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v9 + 40LL))(v9, &v56, 4);
  if ( v9[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  v13 = a1[28];
  v14 = v13 != 0 ? *(_DWORD *)(v13 + 8) : -1;
  v56 = v14;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v12 + 40LL))(v12, &v56, 4);
  if ( v12[4] != 0 )
    return 0;
  v15 = (_DWORD *)*a2;
  v16 = a1[29];
  v17 = v16 != 0 ? *(_DWORD *)(v16 + 8) : -1;
  v56 = v17;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v15 + 40LL))(v15, &v56, 4);
  if ( v15[4] != 0 )
    return 0;
  v18 = (_DWORD *)*a2;
  v19 = a1[30];
  v20 = v19 != 0 ? *(_DWORD *)(v19 + 8) : -1;
  v56 = v20;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v18 + 40LL))(v18, &v56, 4);
  if ( v18[4] != 0 )
    return 0;
  v21 = (_DWORD *)*a2;
  v22 = a1[31];
  v23 = v22 != 0 ? *(_DWORD *)(v22 + 8) : -1;
  v56 = v23;
  (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v21 + 40LL))(v21, &v56, 4);
  if ( v21[4] != 0 )
    return 0;
  v24 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 44, 4);
  if ( v24[4] != 0 )
    return 0;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 356, 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return 0;
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 357, 1);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    return 0;
  sub_1408149D0(*a2, &v56, a1 + 24);
  if ( v56 != 0 )
    return 0;
  sub_1408149D0(*a2, &v56, a1 + 25);
  if ( v56 != 0 )
    return 0;
  if ( (_BYTE)a4 != 0 )
  {
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 362, 1);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 358, 2);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return 0;
    v30 = (_DWORD *)*a2;
    v31 = a1[41];
    v32 = v31 != 0 ? *(_DWORD *)(*(int *)(*(_QWORD *)(v31 + 8) + 4LL) + v31 + 16) : -1;
    v56 = v32;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v30 + 40LL))(v30, &v56, 4);
    if ( v30[4] != 0 )
      return 0;
    v33 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 363, 1);
    if ( *(_DWORD *)(v33 + 16) != 0 )
      return 0;
    v34 = (_DWORD *)a1[34];
    if ( v34 != nullptr )
      v35 = (unsigned int)(v34[2] - *v34) >> 3;
    else
      LOBYTE(v35) = 0;
    v59[0] = v35;
    v36 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v59, 1);
    if ( *(_DWORD *)(v36 + 16) != 0 )
      return 0;
    if ( v59[0] > 0 )
    {
      v37 = 0;
      do
      {
        v38 = (_DWORD *)*a2;
        v39 = *(_QWORD *)(*(_QWORD *)a1[34] + 8 * v37);
        v56 = *(_DWORD *)(*(int *)(*(_QWORD *)(v39 + 8) + 4LL) + v39 + 16);
        (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v38 + 40LL))(v38, &v56, 4);
        if ( v38[4] != 0 )
          return 0;
      }
      while ( ++v37 < v59[0] );
    }
    v40 = (_DWORD *)*a2;
    v41 = a1[42];
    v42 = v41 != 0 ? (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v41 + 56LL))(v41) : 2;
    LOBYTE(v56) = v42;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v40 + 40LL))(v40, &v56, 1);
    if ( v40[4] != 0 )
      return 0;
    v43 = a1[42];
    if ( v43 != 0 && (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v43 + 48LL))(v43, a2) == 0 )
      return 0;
    v44 = (_DWORD *)a1[38];
    if ( v44 != nullptr )
      v45 = (unsigned int)(v44[2] - *v44) >> 3;
    else
      LOBYTE(v45) = 0;
    v58 = v45;
    v46 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v58, 1);
    if ( *(_DWORD *)(v46 + 16) != 0 )
      return 0;
    if ( v58 > 0 )
    {
      v47 = 0;
      while ( (unsigned __int8)sub_140E5D990(*(_QWORD *)(*(_QWORD *)a1[38] + 8 * v47), a2) != 0 )
      {
        if ( ++v47 >= v58 )
          goto LABEL_60;
      }
      return 0;
    }
LABEL_60:
    v48 = (_DWORD *)a1[39];
    if ( v48 != nullptr )
      v49 = (unsigned int)(v48[2] - *v48) >> 3;
    else
      LOBYTE(v49) = 0;
    v57 = v49;
    v50 = *a2;
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v57, 1);
    if ( *(_DWORD *)(v50 + 16) != 0 )
      return 0;
    if ( a1[39] != 0 && v57 > 0 )
    {
      v51 = 0;
      while ( (unsigned __int8)sub_140E5DB50(*(_QWORD *)(*(_QWORD *)a1[39] + 8 * v51), a2) != 0 )
      {
        if ( ++v51 >= v57 )
          goto LABEL_69;
      }
      return 0;
    }
LABEL_69:
    v52 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 45, 2);
    if ( *(_DWORD *)(v52 + 16) != 0 )
      return 0;
    v53 = (_DWORD *)*a2;
    v54 = a1[40];
    v55 = v54 != 0 ? *(_DWORD *)(v54 + 8) : -1;
    v56 = v55;
    (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v53 + 40LL))(v53, &v56, 4);
    if ( v53[4] != 0 )
      return 0;
  }
  if ( (_BYTE)v5 == 0 || (v5 = 0, (unsigned __int8)sub_1411D3570(a1, a2, 0, a4) != 0) )
    LOBYTE(v5) = 1;
  return v5;
}
