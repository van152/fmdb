__int64 __fastcall sub_1415461C0(_QWORD *a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rsi
  __int64 v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // r15
  __int64 v15; // rbx
  __int64 v16; // rbp
  __int64 v17; // rdx
  __int64 v18; // rdi
  __int64 v19; // rbx
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rbx
  __int64 v24; // rsi
  _QWORD *v25; // rdi
  __int64 v26; // rbp
  unsigned __int64 v27; // rax
  unsigned __int64 v28; // r15
  unsigned __int64 v29; // rcx
  unsigned __int64 v30; // r15
  __int64 v31; // rsi
  __int64 v32; // rdx
  __int64 v33; // rsi
  __int64 v34; // rsi
  __int64 v35; // rdi
  __int64 v36; // rbx
  __int64 v37; // rsi
  __int64 v38; // rdi
  __int64 v39; // rbx
  __int64 v40; // rsi
  __int64 v41; // rsi
  __int64 v43; // rsi
  _QWORD *v44; // rbp
  __int64 v45; // rsi
  __int64 v46; // rsi
  __int64 v47; // rsi
  __int64 v48; // rdi
  __int64 v49; // rbx
  __int64 v50; // rsi
  __int64 v51; // rdi
  __int64 v52; // rbx
  __int64 v53; // rsi
  unsigned int v54; // [rsp+4Ch] [rbp-6Ch] BYREF
  _QWORD *v55; // [rsp+50h] [rbp-68h] BYREF
  int v56; // [rsp+58h] [rbp-60h] BYREF
  _QWORD *v57; // [rsp+60h] [rbp-58h]
  _QWORD *v58; // [rsp+68h] [rbp-50h]
  unsigned __int64 v59; // [rsp+70h] [rbp-48h]

  sub_140814B10(*a2, &v55, a1 + 3);
  if ( (_DWORD)v55 != 0 )
    return 0;
  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 209, 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v54, 4);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  v13 = v54;
  v14 = a1[6];
  if ( a1[8] - v14 < (unsigned __int64)v54 )
  {
    v15 = a1[7];
    v16 = sub_1407E4490(qword_141ABD470, v54);
    sub_141758A00(v16, a1[6], a1[7] - a1[6]);
    v17 = a1[6];
    if ( v17 != 0 )
      sub_1407E4890(qword_141ABD470, v17, a1[8] - v17);
    a1[6] = v16;
    a1[7] = v16 + v15 - v14;
    a1[8] = v13 + v16;
    LODWORD(v13) = v54;
  }
  if ( (_DWORD)v13 != 0 )
  {
    v18 = 0;
    do
    {
      v19 = *a2;
      (*(void (__fastcall **)(_QWORD, _QWORD **, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 1);
      if ( *(_DWORD *)(v19 + 16) != 0 )
        return 0;
      if ( (char)v55 > 0 )
        sub_1408E91B0(a1 + 6, &v55);
    }
    while ( ++v18 < (unsigned __int64)v54 );
  }
  sub_140814B10(*a2, &v55, a1 + 4);
  if ( (_DWORD)v55 != 0 )
    return 0;
  sub_140814B10(*a2, &v55, a1 + 5);
  if ( (_DWORD)v55 != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 210, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 26, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v54, 4);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v57 = a1 + 9;
  sub_14096BFE0(a1 + 9, v54);
  if ( v54 != 0 )
  {
    v23 = 0;
    do
    {
      v55 = nullptr;
      v24 = *a2;
      (*(void (__fastcall **)(_QWORD, _QWORD **, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 4);
      if ( *(_DWORD *)(v24 + 16) != 0 )
        return 0;
      v25 = (_QWORD *)a1[10];
      if ( v25 == (_QWORD *)a1[11] )
      {
        v26 = (__int64)v25 - a1[9];
        v27 = v26 >> 3;
        v28 = (unsigned __int64)(v26 >> 3) >> 1;
        v29 = 0x1FFFFFFFFFFFFFFFLL - v28;
        v30 = (v26 >> 3) + v28;
        v59 = (v26 >> 3) + 1;
        if ( v30 <= v59 )
          v30 = v27 + 1;
        if ( v27 > v29 )
          v30 = 0x1FFFFFFFFFFFFFFFLL;
        v31 = sub_1407E4490(qword_141ABD470, 8 * v30);
        *(_QWORD *)(v31 + v26) = v55;
        v32 = a1[9];
        v58 = (_QWORD *)a1[10];
        sub_141758A00(v31, v32, (char *)v25 - v32);
        if ( v58 != v25 )
          sub_141758A00(v31 + v26 + 8, v25, a1[10] - (_QWORD)v25);
        if ( *v57 != 0 )
          sub_1407E4890(qword_141ABD470, *v57, a1[11] - *v57);
        a1[9] = v31;
        a1[10] = v31 + 8 * v59;
        a1[11] = v31 + 8 * v30;
      }
      else
      {
        *v25 = v55;
        a1[10] += 8LL;
      }
    }
    while ( ++v23 < (unsigned __int64)v54 );
  }
  v33 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *(_DWORD *)(v33 + 16) != 0 )
    return 0;
  v34 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v54, 4);
  if ( *(_DWORD *)(v34 + 16) != 0 )
    return 0;
  sub_14096BFE0(a1 + 15, v54);
  if ( v54 != 0 )
  {
    v35 = 0;
    do
    {
      v55 = nullptr;
      v36 = *a2;
      (*(void (__fastcall **)(_QWORD, _QWORD **, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 4);
      if ( *(_DWORD *)(v36 + 16) != 0 )
        return 0;
      sub_14087F540(a1 + 15, &v55);
    }
    while ( ++v35 < (unsigned __int64)v54 );
  }
  v37 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v54, 4);
  if ( *(_DWORD *)(v37 + 16) != 0 )
    return 0;
  sub_140893BE0(a1 + 12, v54);
  if ( v54 != 0 )
  {
    v38 = 0;
    do
    {
      v55 = nullptr;
      v39 = *a2;
      (*(void (__fastcall **)(_QWORD, _QWORD **, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 4);
      if ( *(_DWORD *)(v39 + 16) != 0 )
        return 0;
      sub_14087F540(a1 + 12, &v55);
    }
    while ( ++v38 < (unsigned __int64)v54 );
  }
  v40 = *a2;
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 25, 4);
  if ( *(_DWORD *)(v40 + 16) != 0 )
    return 0;
  v41 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v54, 4);
  if ( *(_DWORD *)(v41 + 16) != 0 )
    return 0;
  sub_14096BFE0(a1 + 21, v54);
  if ( v54 != 0 )
  {
    v43 = 0;
    do
    {
      v44 = (_QWORD *)sub_1415468D0(16);
      *v44 = -1;
      v44[1] = 0;
      v55 = v44;
      if ( (unsigned __int8)sub_140FEA0C0(v44, a2) == 0 )
        return 0;
      sub_140814B10(*a2, &v56, v44 + 1);
      if ( v56 != 0 )
        return 0;
      sub_14087F540(a1 + 21, &v55);
    }
    while ( ++v43 < (unsigned __int64)v54 );
  }
  if ( a7 != 0 )
  {
    v45 = *a2;
    (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 30, 1);
    if ( *(_DWORD *)(v45 + 16) != 0 )
      return 0;
    v46 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 241, 1);
    if ( *(_DWORD *)(v46 + 16) != 0 )
      return 0;
    if ( (unsigned __int8)sub_140DB8980((char *)a1 + 212, a2) == 0 )
      return 0;
    v47 = *a2;
    (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v56, 1);
    if ( *(_DWORD *)(v47 + 16) != 0 )
      return 0;
    sub_14096BFE0(a1 + 27, (unsigned __int8)v56);
    if ( (_BYTE)v56 != 0 )
    {
      v48 = 0;
      do
      {
        v55 = nullptr;
        v49 = *a2;
        (*(void (__fastcall **)(_QWORD, _QWORD **, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 4);
        if ( *(_DWORD *)(v49 + 16) != 0 )
          return 0;
        sub_14087F540(a1 + 27, &v55);
      }
      while ( ++v48 < (unsigned __int64)(unsigned __int8)v56 );
    }
  }
  v50 = *a2;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v54, 4);
  if ( *(_DWORD *)(v50 + 16) != 0 )
    return 0;
  sub_14096BFE0(a1 + 18, v54);
  if ( v54 != 0 )
  {
    v51 = 0;
    do
    {
      v55 = nullptr;
      v52 = *a2;
      (*(void (__fastcall **)(_QWORD, _QWORD **, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 4);
      if ( *(_DWORD *)(v52 + 16) != 0 )
        return 0;
      sub_14087F540(a1 + 18, &v55);
    }
    while ( ++v51 < (unsigned __int64)v54 );
  }
  v53 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 211, 1);
  if ( *(_DWORD *)(v53 + 16) != 0 )
    return 0;
  return sub_140FAED40((_DWORD)a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
