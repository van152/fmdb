__int64 __fastcall sub_141041E60(__int64 a1, _QWORD *a2, __int64 a3, unsigned int a4)
{
  _DWORD *v7; // rbx
  _DWORD *v9; // rbx
  __int64 v10; // rax
  int v11; // eax
  _DWORD *v12; // rbx
  __int64 v13; // rax
  unsigned __int64 v14; // rbx
  __int64 v15; // rax
  int v16; // eax
  _DWORD *v17; // rbp
  _DWORD *v18; // rbx
  __int64 v19; // rax
  unsigned __int64 v20; // rbp
  _DWORD *v21; // rbx
  _DWORD *v22; // rbx
  __int64 *v23; // rcx
  __int64 v24; // rax
  unsigned __int64 v25; // rbx
  __int64 *v26; // rcx
  __int64 v27; // rbx
  __int64 v28; // rbx
  __int64 v29; // rbx
  __int64 v30; // rbx
  __int64 v31; // rbx
  __int64 v32; // rbx
  _DWORD *v33; // rbx
  _QWORD *v34; // rax
  _QWORD *v35; // rbx
  __int64 v36; // rbp
  __int64 v37; // rbx
  _DWORD *v38; // rbx
  __int64 v39; // rax
  int v40; // eax
  _DWORD *v41; // rbx
  __int64 v42; // rax
  int v43; // eax
  _DWORD *v44; // rbx
  __int64 v45; // rax
  int v46; // eax
  _DWORD *v47; // rbx
  __int64 v48; // rax
  int v49; // eax
  __int64 v50; // rbx
  __int64 v51; // rbx
  __int64 v52; // rbx
  __int64 v53; // rbx
  _DWORD *v54; // rbx
  __int64 v55; // rax
  unsigned __int64 v56; // rbx
  _DWORD *v57; // rbx
  _QWORD *v58; // rbx
  _QWORD *v59; // rbp
  _DWORD *v60; // rbx
  _QWORD *v61; // rbx
  _QWORD *v62; // rbp
  _DWORD *v63; // rbx
  __int64 v64; // rbx
  __int64 v65; // rbp
  __int64 v66; // rbx
  __int64 v67; // rbx
  __int64 v68; // rbx
  __int64 v69; // rbx
  __int64 v70; // rbx
  __int64 v71; // rbx
  __int64 v72; // rbx
  __int64 v73; // rbx
  __int64 v74; // rbx
  __int64 v75; // rbx
  __int64 v76; // rbx
  __int64 v77; // rbx
  _QWORD v78[7]; // [rsp+20h] [rbp-38h] BYREF

  v7 = (_DWORD *)*a2;
  LOBYTE(v78[0]) = 0;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v7 + 40LL))(v7, v78, 1);
  if ( v7[4] != 0 )
    return 0;
  if ( (_BYTE)a4 != 0 )
  {
    v9 = (_DWORD *)*a2;
    v10 = *(_QWORD *)(a1 + 280);
    v11 = v10 != 0 ? *(_DWORD *)(v10 + 8) : -1;
    LODWORD(v78[0]) = v11;
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v9 + 40LL))(v9, v78, 4);
    if ( v9[4] != 0 )
      return 0;
    v12 = (_DWORD *)*a2;
    LOWORD(v78[0]) = (unsigned int)(*(_DWORD *)(a1 + 304) - *(_DWORD *)(a1 + 296)) >> 3;
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v12 + 40LL))(v12, v78, 2);
    if ( v12[4] != 0 )
      return 0;
    v13 = *(_QWORD *)(a1 + 296);
    if ( *(_QWORD *)(a1 + 304) != v13 )
    {
      v14 = 0;
      do
      {
        v15 = *(_QWORD *)(v13 + 8 * v14);
        v16 = v15 != 0 ? *(_DWORD *)(v15 + 8) : -1;
        v17 = (_DWORD *)*a2;
        LODWORD(v78[0]) = v16;
        (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, v78, 4);
        if ( v17[4] != 0 )
          return 0;
        v14 = (unsigned int)(v14 + 1);
        v13 = *(_QWORD *)(a1 + 296);
      }
      while ( (*(_QWORD *)(a1 + 304) - v13) >> 3 > v14 );
    }
    v18 = (_DWORD *)*a2;
    LODWORD(v78[0]) = (*(_QWORD *)(a1 + 352) - *(_QWORD *)(a1 + 344)) >> 2;
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v18 + 40LL))(v18, v78, 4);
    if ( v18[4] != 0 )
      return 0;
    v19 = *(_QWORD *)(a1 + 344);
    if ( *(_QWORD *)(a1 + 352) != v19 )
    {
      v20 = 0;
      do
      {
        v21 = (_DWORD *)*a2;
        (*(void (__fastcall **)(_QWORD, unsigned __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v19 + 4 * v20, 4);
        if ( v21[4] != 0 )
          return 0;
        v20 = (unsigned int)(v20 + 1);
        v19 = *(_QWORD *)(a1 + 344);
      }
      while ( (*(_QWORD *)(a1 + 352) - v19) >> 2 > v20 );
    }
    v22 = (_DWORD *)*a2;
    LOWORD(v78[0]) = (unsigned int)(*(_DWORD *)(*(_QWORD *)(a1 + 368) + 8LL) - **(_DWORD **)(a1 + 368)) >> 3;
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v22 + 40LL))(v22, v78, 2);
    if ( v22[4] != 0 )
      return 0;
    v23 = *(__int64 **)(a1 + 368);
    v24 = *v23;
    if ( v23[1] != *v23 )
    {
      v25 = 0;
      while ( (unsigned __int8)sub_1415CFC40(*(_QWORD *)(v24 + 8 * v25), a2) != 0 )
      {
        v25 = (unsigned int)(v25 + 1);
        v26 = *(__int64 **)(a1 + 368);
        v24 = *v26;
        if ( (v26[1] - *v26) >> 3 <= v25 )
          goto LABEL_26;
      }
      return 0;
    }
LABEL_26:
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 388, 4);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return 0;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 392, 4);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 396, 4);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return 0;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 400, 4);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return 0;
    v31 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 404, 4);
    if ( *(_DWORD *)(v31 + 16) != 0 )
      return 0;
    v32 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 408, 4);
    if ( *(_DWORD *)(v32 + 16) != 0 )
      return 0;
    sub_141042730(v78, a2, a1 + 96);
    if ( LODWORD(v78[0]) != 0 )
      return 0;
    v33 = (_DWORD *)*a2;
    LODWORD(v78[0]) = *(_DWORD *)(a1 + 224);
    (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v33 + 40LL))(v33, v78, 4);
    if ( v33[4] != 0 )
      return 0;
    v34 = *(_QWORD **)(a1 + 216);
    v35 = (_QWORD *)*v34;
    v78[0] = v35;
    if ( v35 != v34 )
    {
      do
      {
        v36 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)v35 + 28, 4);
        if ( *(_DWORD *)(v36 + 16) != 0
          || (unsigned __int8)sub_140DB89D0(v35 + 4, a2) == 0
          || (unsigned __int8)sub_140DB89D0((char *)v35 + 36, a2) == 0 )
        {
          return 0;
        }
        sub_1410427D0(v78);
        v35 = (_QWORD *)v78[0];
      }
      while ( v78[0] != *(_QWORD *)(a1 + 216) );
    }
    sub_141042820(v78, a2, a1 + 120);
    if ( LODWORD(v78[0]) != 0 )
      return 0;
  }
  v37 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 459, 1);
  if ( *(_DWORD *)(v37 + 16) != 0 )
    return 0;
  v38 = (_DWORD *)*a2;
  v39 = *(_QWORD *)(a1 + 240);
  v40 = v39 != 0 ? *(_DWORD *)(v39 + 8) : -1;
  LODWORD(v78[0]) = v40;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v38 + 40LL))(v38, v78, 4);
  if ( v38[4] != 0 )
    return 0;
  v41 = (_DWORD *)*a2;
  v42 = *(_QWORD *)(a1 + 248);
  v43 = v42 != 0 ? *(_DWORD *)(v42 + 8) : -1;
  LODWORD(v78[0]) = v43;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v41 + 40LL))(v41, v78, 4);
  if ( v41[4] != 0 )
    return 0;
  v44 = (_DWORD *)*a2;
  v45 = *(_QWORD *)(a1 + 232);
  v46 = v45 != 0 ? *(_DWORD *)(v45 + 8) : -1;
  LODWORD(v78[0]) = v46;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v44 + 40LL))(v44, v78, 4);
  if ( v44[4] != 0 )
    return 0;
  v47 = (_DWORD *)*a2;
  v48 = *(_QWORD *)(a1 + 256);
  v49 = v48 != 0 ? *(_DWORD *)(v48 + 8) : -1;
  LODWORD(v78[0]) = v49;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v47 + 40LL))(v47, v78, 4);
  if ( v47[4] != 0 )
    return 0;
  v50 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 460, 1);
  if ( *(_DWORD *)(v50 + 16) != 0 )
    return 0;
  v51 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 464, 1);
  if ( *(_DWORD *)(v51 + 16) != 0 )
    return 0;
  v52 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 436, 4);
  if ( *(_DWORD *)(v52 + 16) != 0 )
    return 0;
  v53 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 461, 1);
  if ( *(_DWORD *)(v53 + 16) != 0 )
    return 0;
  v54 = (_DWORD *)*a2;
  LOBYTE(v78[0]) = (unsigned int)(*(_DWORD *)(a1 + 80) - *(_DWORD *)(a1 + 72)) >> 4;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v54 + 40LL))(v54, v78, 1);
  if ( v54[4] != 0 )
    return 0;
  v55 = *(_QWORD *)(a1 + 72);
  if ( *(_QWORD *)(a1 + 80) != v55 )
  {
    v56 = 0;
    while ( (unsigned __int8)sub_141071160(v55 + 16 * v56, a2) != 0 )
    {
      v56 = (unsigned int)(v56 + 1);
      v55 = *(_QWORD *)(a1 + 72);
      if ( (*(_QWORD *)(a1 + 80) - v55) >> 4 <= v56 )
        goto LABEL_66;
    }
    return 0;
  }
LABEL_66:
  v57 = (_DWORD *)*a2;
  LODWORD(v78[0]) = (*(_QWORD *)(a1 + 176) - *(_QWORD *)(a1 + 168)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v57 + 40LL))(v57, v78, 4);
  if ( v57[4] != 0 )
    return 0;
  v58 = *(_QWORD **)(a1 + 168);
  v59 = *(_QWORD **)(a1 + 176);
  if ( v58 != v59 )
  {
    while ( (unsigned __int8)sub_1415CFF70(*v58, a2) != 0 )
    {
      if ( ++v58 == v59 )
        goto LABEL_70;
    }
    return 0;
  }
LABEL_70:
  v60 = (_DWORD *)*a2;
  LODWORD(v78[0]) = (*(_QWORD *)(a1 + 152) - *(_QWORD *)(a1 + 144)) >> 3;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v60 + 40LL))(v60, v78, 4);
  if ( v60[4] != 0 )
    return 0;
  v61 = *(_QWORD **)(a1 + 144);
  v62 = *(_QWORD **)(a1 + 152);
  if ( v61 != v62 )
  {
    while ( (unsigned __int8)sub_1415CFF70(*v61, a2) != 0 )
    {
      if ( ++v61 == v62 )
        goto LABEL_74;
    }
    return 0;
  }
LABEL_74:
  v63 = (_DWORD *)*a2;
  LODWORD(v78[0]) = (*(_QWORD *)(a1 + 200) - *(_QWORD *)(a1 + 192)) >> 4;
  (*(void (__fastcall **)(_DWORD *, _QWORD *, __int64))(*(_QWORD *)v63 + 40LL))(v63, v78, 4);
  if ( v63[4] != 0 )
    return 0;
  v64 = *(_QWORD *)(a1 + 192);
  v65 = *(_QWORD *)(a1 + 200);
  if ( v64 != v65 )
  {
    while ( (unsigned __int8)sub_141070950(v64, a2) != 0 )
    {
      v64 += 16;
      if ( v64 == v65 )
        goto LABEL_78;
    }
    return 0;
  }
LABEL_78:
  if ( (_BYTE)a4 != 0 )
  {
    v66 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 420, 4);
    if ( *(_DWORD *)(v66 + 16) != 0 )
      return 0;
    v67 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 424, 4);
    if ( *(_DWORD *)(v67 + 16) != 0 )
      return 0;
    v68 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 432, 4);
    if ( *(_DWORD *)(v68 + 16) != 0 )
      return 0;
    v69 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 428, 4);
    if ( *(_DWORD *)(v69 + 16) != 0 )
      return 0;
    v70 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 440, 4);
    if ( *(_DWORD *)(v70 + 16) != 0 )
      return 0;
    v71 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 444, 4);
    if ( *(_DWORD *)(v71 + 16) != 0 )
      return 0;
    v72 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 448, 4);
    if ( *(_DWORD *)(v72 + 16) != 0 )
      return 0;
    v73 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 452, 4);
    if ( *(_DWORD *)(v73 + 16) != 0 )
      return 0;
    v74 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 380, 4);
    if ( *(_DWORD *)(v74 + 16) != 0 )
      return 0;
    v75 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 384, 4);
    if ( *(_DWORD *)(v75 + 16) != 0 )
      return 0;
    v76 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 456, 2);
    if ( *(_DWORD *)(v76 + 16) != 0 )
      return 0;
    v77 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 458, 1);
    if ( *(_DWORD *)(v77 + 16) != 0 )
      return 0;
  }
  return sub_140FE22B0(a1, a2, 0, a4);
}
