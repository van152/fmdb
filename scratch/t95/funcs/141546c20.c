__int64 __fastcall sub_141546C20(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  __int64 v8; // rbx
  _DWORD *v9; // rbx
  __int64 v10; // rdx
  unsigned __int64 v11; // rbp
  __int64 v12; // rbx
  __int64 v13; // rbx
  __int64 v14; // rbx
  _DWORD *v15; // rbx
  __int64 v16; // rax
  unsigned __int64 v17; // r15
  __int64 v18; // rax
  int v19; // eax
  _DWORD *v20; // rbx
  _DWORD *v21; // r14
  __int64 v22; // rax
  int v23; // eax
  _DWORD *v24; // rbx
  __int64 v25; // rax
  unsigned __int64 v26; // r15
  __int64 v27; // rax
  int v28; // eax
  _DWORD *v29; // rbx
  _DWORD *v30; // rbx
  __int64 v31; // rax
  unsigned __int64 v32; // r15
  __int64 v33; // rax
  int v34; // eax
  _DWORD *v35; // rbx
  _DWORD *v36; // r14
  __int64 v37; // rax
  int v38; // eax
  _DWORD *v39; // rbx
  __int64 v41; // rax
  unsigned __int64 v42; // rbx
  __int64 v43; // r15
  __int64 v44; // rbx
  __int64 v45; // rbx
  _DWORD *v46; // rbx
  __int64 v47; // rax
  unsigned __int64 v48; // r15
  __int64 v49; // rax
  int v50; // eax
  _DWORD *v51; // rbx
  _DWORD *v52; // rbx
  __int64 v53; // rax
  unsigned __int64 v54; // r15
  __int64 v55; // rax
  int v56; // eax
  _DWORD *v57; // rbx
  __int64 v58; // rbx
  _DWORD v59[16]; // [rsp+28h] [rbp-40h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v59[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v59, 1);
  if ( v7[4] != 0 )
    return 0;
  sub_1408149D0(*a2, v59, a1 + 24);
  if ( v59[0] != 0 )
    return 0;
  v8 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 209, 1);
  if ( *(_DWORD *)(v8 + 16) != 0 )
    return 0;
  v9 = (_DWORD *)*a2;
  v59[0] = *(_DWORD *)(a1 + 56) - *(_DWORD *)(a1 + 48);
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v59, 4);
  if ( v9[4] != 0 )
    return 0;
  v10 = *(_QWORD *)(a1 + 48);
  if ( *(_QWORD *)(a1 + 56) != v10 )
  {
    v11 = 0;
    do
    {
      v12 = *a2;
      (*(void (__fastcall **)(_QWORD, unsigned __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v11 + v10, 1);
      if ( *(_DWORD *)(v12 + 16) != 0 )
        return 0;
      ++v11;
      v10 = *(_QWORD *)(a1 + 48);
    }
    while ( v11 < *(_QWORD *)(a1 + 56) - v10 );
  }
  sub_1408149D0(*a2, v59, a1 + 32);
  if ( v59[0] != 0 )
    return 0;
  sub_1408149D0(*a2, v59, a1 + 40);
  if ( v59[0] != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 210, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 208, 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = (_DWORD *)*a2;
  v59[0] = (*(_QWORD *)(a1 + 80) - *(_QWORD *)(a1 + 72)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v15 + 40LL))(v15, v59, 4);
  if ( v15[4] != 0 )
    return 0;
  v16 = *(_QWORD *)(a1 + 72);
  if ( *(_QWORD *)(a1 + 80) != v16 )
  {
    v17 = 0;
    do
    {
      v18 = *(_QWORD *)(v16 + 8 * v17);
      v19 = v18 != 0 ? *(_DWORD *)(v18 + 8) : -1;
      v20 = (_DWORD *)*a2;
      v59[0] = v19;
      (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v20 + 40LL))(v20, v59, 4);
      if ( v20[4] != 0 )
        return 0;
      ++v17;
      v16 = *(_QWORD *)(a1 + 72);
    }
    while ( v17 < (*(_QWORD *)(a1 + 80) - v16) >> 3 );
  }
  v21 = (_DWORD *)*a2;
  v22 = *(_QWORD *)(a1 + 192);
  v23 = v22 != 0 ? *(_DWORD *)(v22 + 8) : -1;
  v59[0] = v23;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v21 + 40LL))(v21, v59, 4);
  if ( v21[4] != 0 )
    return 0;
  v24 = (_DWORD *)*a2;
  v59[0] = (*(_QWORD *)(a1 + 128) - *(_QWORD *)(a1 + 120)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v24 + 40LL))(v24, v59, 4);
  if ( v24[4] != 0 )
    return 0;
  v25 = *(_QWORD *)(a1 + 120);
  if ( *(_QWORD *)(a1 + 128) != v25 )
  {
    v26 = 0;
    do
    {
      v27 = *(_QWORD *)(v25 + 8 * v26);
      v28 = v27 != 0 ? *(_DWORD *)(v27 + 8) : -1;
      v29 = (_DWORD *)*a2;
      v59[0] = v28;
      (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v29 + 40LL))(v29, v59, 4);
      if ( v29[4] != 0 )
        return 0;
      ++v26;
      v25 = *(_QWORD *)(a1 + 120);
    }
    while ( v26 < (*(_QWORD *)(a1 + 128) - v25) >> 3 );
  }
  v30 = (_DWORD *)*a2;
  v59[0] = (*(_QWORD *)(a1 + 104) - *(_QWORD *)(a1 + 96)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v30 + 40LL))(v30, v59, 4);
  if ( v30[4] != 0 )
    return 0;
  v31 = *(_QWORD *)(a1 + 96);
  if ( *(_QWORD *)(a1 + 104) != v31 )
  {
    v32 = 0;
    do
    {
      v33 = *(_QWORD *)(v31 + 8 * v32);
      v34 = v33 != 0 ? *(_DWORD *)(v33 + 8) : -1;
      v35 = (_DWORD *)*a2;
      v59[0] = v34;
      (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v35 + 40LL))(v35, v59, 4);
      if ( v35[4] != 0 )
        return 0;
      ++v32;
      v31 = *(_QWORD *)(a1 + 96);
    }
    while ( v32 < (*(_QWORD *)(a1 + 104) - v31) >> 3 );
  }
  v36 = (_DWORD *)*a2;
  v37 = *(_QWORD *)(a1 + 200);
  v38 = v37 != 0 ? *(_DWORD *)(v37 + 8) : -1;
  v59[0] = v38;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v36 + 40LL))(v36, v59, 4);
  if ( v36[4] != 0 )
    return 0;
  v39 = (_DWORD *)*a2;
  v59[0] = (*(_QWORD *)(a1 + 176) - *(_QWORD *)(a1 + 168)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v39 + 40LL))(v39, v59, 4);
  if ( v39[4] != 0 )
    return 0;
  v41 = *(_QWORD *)(a1 + 168);
  if ( *(_QWORD *)(a1 + 176) != v41 )
  {
    v42 = 0;
    do
    {
      v43 = *(_QWORD *)(v41 + 8 * v42);
      if ( (unsigned __int8)sub_140FEA120(v43, a2) == 0 )
        return 0;
      sub_1408149D0(*a2, v59, v43 + 8);
      if ( v59[0] != 0 )
        return 0;
      ++v42;
      v41 = *(_QWORD *)(a1 + 168);
    }
    while ( v42 < (*(_QWORD *)(a1 + 176) - v41) >> 3 );
  }
  if ( (_BYTE)a4 != 0 )
  {
    v44 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 240, 1);
    if ( *(_DWORD *)(v44 + 16) != 0 )
      return 0;
    v45 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 241, 1);
    if ( *(_DWORD *)(v45 + 16) != 0 )
      return 0;
    if ( (unsigned __int8)sub_140DB89D0(a1 + 212, a2) == 0 )
      return 0;
    v46 = (_DWORD *)*a2;
    LOBYTE(v59[0]) = (unsigned int)(*(_DWORD *)(a1 + 224) - *(_DWORD *)(a1 + 216)) >> 3;
    (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v46 + 40LL))(v46, v59, 1);
    if ( v46[4] != 0 )
      return 0;
    v47 = *(_QWORD *)(a1 + 216);
    if ( *(_QWORD *)(a1 + 224) != v47 )
    {
      v48 = 0;
      do
      {
        v49 = *(_QWORD *)(v47 + 8 * v48);
        v50 = v49 != 0 ? *(_DWORD *)(v49 + 144) : -1;
        v51 = (_DWORD *)*a2;
        v59[0] = v50;
        (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v51 + 40LL))(v51, v59, 4);
        if ( v51[4] != 0 )
          return 0;
        ++v48;
        v47 = *(_QWORD *)(a1 + 216);
      }
      while ( v48 < (*(_QWORD *)(a1 + 224) - v47) >> 3 );
    }
  }
  v52 = (_DWORD *)*a2;
  v59[0] = (*(_QWORD *)(a1 + 152) - *(_QWORD *)(a1 + 144)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v52 + 40LL))(v52, v59, 4);
  if ( v52[4] != 0 )
    return 0;
  v53 = *(_QWORD *)(a1 + 144);
  if ( *(_QWORD *)(a1 + 152) != v53 )
  {
    v54 = 0;
    do
    {
      v55 = *(_QWORD *)(v53 + 8 * v54);
      v56 = v55 != 0 ? *(_DWORD *)(v55 + 8) : -1;
      v57 = (_DWORD *)*a2;
      v59[0] = v56;
      (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v57 + 40LL))(v57, v59, 4);
      if ( v57[4] != 0 )
        return 0;
      ++v54;
      v53 = *(_QWORD *)(a1 + 144);
    }
    while ( v54 < (*(_QWORD *)(a1 + 152) - v53) >> 3 );
  }
  v58 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 211, 1);
  if ( *(_DWORD *)(v58 + 16) != 0 )
    return 0;
  return sub_140FE22B0(a1, a2, 0, a4);
}
