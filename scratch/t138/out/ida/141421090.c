__int64 __fastcall sub_141421090(__int64 a1, __int64 *a2)
{
  __int64 v3; // rax
  unsigned __int8 *v4; // rdi
  __int64 v5; // rbx
  __int64 *v6; // rdi
  __int64 v7; // r8
  unsigned __int8 *v8; // rbx
  __int64 v9; // r8
  unsigned __int64 v10; // r14
  __int64 v11; // rcx
  _QWORD *v12; // rax
  char *v13; // rbx
  unsigned __int64 v14; // rsi
  unsigned __int64 v15; // rdx
  unsigned __int64 v16; // r15
  __int64 v17; // rax
  unsigned __int64 v18; // rcx
  unsigned __int64 v19; // r10
  unsigned __int64 v20; // r8
  __int64 v21; // rdi
  unsigned __int64 v22; // rcx
  unsigned __int64 v23; // rdx
  __int64 v24; // rsi
  unsigned __int64 v25; // rsi
  __int64 v26; // rdx
  __int128 v27; // xmm0
  __int64 v28; // rdx
  __int64 v29; // rbx
  __int128 v30; // xmm0
  __int64 v31; // rdx
  __int64 v32; // rsi
  __int64 v33; // rdi
  unsigned __int64 v34; // rcx
  __int64 v35; // rbx
  __int64 v36; // rbx
  bool v37; // al
  __int64 v38; // r8
  __int64 v39; // rax
  __int64 v40; // rsi
  unsigned __int64 v41; // rbx
  __int64 v42; // rdi
  unsigned __int64 v43; // rbx
  __int128 v44; // xmm0
  __int64 v45; // rbx
  __int64 v46; // rsi
  __int128 v47; // xmm0
  __int64 v48; // rax
  unsigned __int64 v49; // rcx
  __int64 v50; // r8
  unsigned __int64 v51; // r15
  unsigned int v52; // esi
  char v53; // bl
  __int64 v54; // rcx
  unsigned __int8 v55; // bl
  __int64 v56; // rax
  __int64 v57; // rdx
  unsigned __int64 v58; // rdx
  unsigned __int64 v59; // rsi
  __int64 v60; // r8
  __int64 v61; // rdx
  __int64 v62; // rsi
  unsigned __int64 i; // rbx
  __int64 v64; // rax
  __int64 *v65; // rsi
  __int64 v66; // r8
  bool v67; // zf
  __int64 v68; // rbx
  __int64 v69; // rdi
  __int64 v70; // r8
  __int64 v71; // rax
  void (__fastcall ***v72)(_QWORD, __int64); // rcx
  _BYTE *v74; // [rsp+28h] [rbp-38h]
  __int64 v75; // [rsp+30h] [rbp-30h] BYREF
  _DWORD *v76; // [rsp+38h] [rbp-28h] BYREF
  __int64 *v77; // [rsp+40h] [rbp-20h]
  __int64 v78; // [rsp+48h] [rbp-18h]
  unsigned __int8 *v79; // [rsp+50h] [rbp-10h]
  unsigned __int8 v80; // [rsp+5Eh] [rbp-2h] BYREF
  unsigned __int8 v81; // [rsp+5Fh] [rbp-1h] BYREF
  _QWORD v82[8]; // [rsp+60h] [rbp+0h] BYREF

  v82[0] = -2;
  v3 = *a2;
  v76 = (_DWORD *)v3;
  if ( v3 != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v3 + 8));
  v77 = (__int64 *)(a1 + 179);
  v78 = 1;
  v79 = (unsigned __int8 *)(a1 + 180);
  v4 = (unsigned __int8 *)(a1 + 152);
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 + 179, a3: 1);
  v77 = (__int64 *)(a1 + 152);
  v78 = 16;
  v79 = (unsigned __int8 *)(a1 + 168);
  if ( (unsigned __int16)qword_141B60330 > 0xDC8u || HIBYTE(qword_141B6034C) != 0 )
  {
    v74 = (_BYTE *)(a1 + 168);
    if ( HIBYTE(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
    {
      if ( v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 + 152, a3: 16);
      v77 = (__int64 *)(a1 + 144);
      v78 = 4;
      v4 = (unsigned __int8 *)(a1 + 148);
    }
    else
    {
      if ( v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 + 152, a3: 16);
      v77 = (__int64 *)(a1 + 144);
      v78 = 8;
    }
    v79 = v4;
  }
  else
  {
    v5 = (__int64)v76;
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: a1 + 152, a3: 16);
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: &v75, a3: 8);
    if ( *(_DWORD *)(v5 + 16) != 0 )
      goto LABEL_166;
    v74 = (_BYTE *)(a1 + 168);
    *(_QWORD *)(a1 + 144) = v75;
    v4 = v79;
  }
  if ( v4 == (unsigned __int8 *)(a1 + 178) )
  {
    v6 = (__int64 *)(a1 + 176);
    v7 = v78 + 1;
    v78 = v7;
    v79 = (unsigned __int8 *)(a1 + 179);
    if ( v7 == 0 )
      goto LABEL_28;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = (__int64 *)(a1 + 178);
    v78 = 1;
    v79 = (unsigned __int8 *)(a1 + 179);
    v6 = (__int64 *)(a1 + 176);
    v7 = 1;
  }
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v7);
LABEL_28:
  v77 = v6;
  v78 = 2;
  v79 = (unsigned __int8 *)(a1 + 178);
  v8 = &v80;
  if ( (unsigned __int8 *)(a1 + 178) == &v80 )
  {
    v9 = 3;
    v8 = (unsigned __int8 *)v6;
  }
  else
  {
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v6, a3: 2);
    v77 = (__int64 *)&v80;
    v9 = 1;
  }
  v78 = v9;
  v79 = &v81;
  if ( v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, unsigned __int8 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v8);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  v10 = v80;
  if ( v80 == 0 )
    goto LABEL_119;
  v11 = *(_QWORD *)(a1 + 96);
  v12 = *(_QWORD **)(a1 + 104);
  v13 = (char *)v12 - v11;
  v14 = ((__int64)v12 - v11) >> 3;
  if ( v14 > v80 )
  {
    *(_QWORD *)(a1 + 104) = v11 + 8LL * v80;
    goto LABEL_69;
  }
  if ( v14 >= v80 )
    goto LABEL_69;
  v15 = (*(_QWORD *)(a1 + 112) - v11) >> 3;
  if ( v15 < v80 )
  {
    v16 = v15 + (v15 >> 1);
    if ( v16 <= v80 )
      v16 = v80;
    v17 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v16);
    v18 = v10 - v14;
    if ( v10 != v14 )
    {
      v19 = v17 + 8 * v14;
      if ( v18 < 4 )
        goto LABEL_57;
      v20 = v18 & 0xFFFFFFFFFFFFFFFCuLL;
      if ( (v18 & 0xFFFFFFFFFFFFFFFCuLL) - 4 >= 0xC )
      {
        v25 = ((((v18 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 0x7FFFFFFFFFFFFFFCLL;
        v26 = (__int64)&v13[v17 + 112];
        v21 = 0;
        v27 = MEMORY[0x1418B5CF0];
        do
        {
          *(_OWORD *)&v13[8 * v21 + v17] = v27;
          *(_OWORD *)(v26 + 8 * v21 - 96) = v27;
          *(_OWORD *)(v26 + 8 * v21 - 80) = v27;
          *(_OWORD *)(v26 + 8 * v21 - 64) = v27;
          *(_OWORD *)(v26 + 8 * v21 - 48) = v27;
          *(_OWORD *)(v26 + 8 * v21 - 32) = v27;
          *(_OWORD *)(v26 + 8 * v21 - 16) = v27;
          *(_OWORD *)(v26 + 8 * v21) = v27;
          v21 += 16;
          v25 -= 4LL;
        }
        while ( v25 != 0 );
      }
      else
      {
        v21 = 0;
      }
      if ( (((unsigned __int8)(((v18 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != 0 )
      {
        v28 = (__int64)&v13[8 * v21 + 16 + v17];
        v29 = 0;
        v30 = MEMORY[0x1418B5CF0];
        do
        {
          *(_OWORD *)(v28 + v29 - 16) = v30;
          *(_OWORD *)(v28 + v29) = v30;
          v29 += 32;
        }
        while ( 32LL * (((unsigned __int8)(((v18 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != v29 );
      }
      if ( v18 != v20 )
      {
        v18 &= 3u;
        v19 += 8 * v20;
LABEL_57:
        v31 = 0;
        do
          *(_QWORD *)(v19 + 8 * v31++) = 0xFFFFFFFFFFFFFFLL;
        while ( v18 != v31 );
      }
    }
    v32 = v17;
    sub_141758A00(a1: v17, a2: *(_QWORD *)(a1 + 96), a3: *(_QWORD *)(a1 + 104) - *(_QWORD *)(a1 + 96));
    v33 = *(_QWORD *)(a1 + 96);
    if ( v33 != 0 )
    {
      v34 = *(_QWORD *)(a1 + 112) - v33;
      if ( v34 == -1 )
        v34 = *(unsigned int *)(v33 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v35 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v35) >> 3 > v34)
        && (v36 = *(_QWORD *)(v35 + 8 * v34)) != 0 )
      {
        MEMORY[0x1419475D8](a1: v36 + 32, a2: v33 - *(unsigned int *)(v36 + 120));
        v37 = *(_BYTE *)(v36 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v36 + 64)) != 0;
        if ( !v37 && *(_BYTE *)(v36 + 97) != 0 )
          sub_1412D33C0(a1: v36);
      }
      else
      {
        MEMORY[0x141948990](a1: v33 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    *(_QWORD *)(a1 + 96) = v32;
    *(_QWORD *)(a1 + 104) = v32 + 8 * v10;
    *(_QWORD *)(a1 + 112) = v32 + 8 * v16;
    LOBYTE(v10) = v80;
    if ( v80 != 0 )
      goto LABEL_69;
LABEL_86:
    v38 = v78;
    LOBYTE(v10) = 0;
    goto LABEL_87;
  }
  v22 = v80 - v14;
  if ( v80 != v14 )
  {
    if ( v22 < 4 )
      goto LABEL_84;
    v23 = v22 & 0xFFFFFFFFFFFFFFFCuLL;
    if ( (v22 & 0xFFFFFFFFFFFFFFFCuLL) - 4 >= 0xC )
    {
      v43 = ((((v22 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 0x7FFFFFFFFFFFFFFCLL;
      v24 = 0;
      v44 = MEMORY[0x1418B5CF0];
      do
      {
        *(_OWORD *)&v12[v24] = v44;
        *(_OWORD *)&v12[v24 + 2] = v44;
        *(_OWORD *)&v12[v24 + 4] = v44;
        *(_OWORD *)&v12[v24 + 6] = v44;
        *(_OWORD *)&v12[v24 + 8] = v44;
        *(_OWORD *)&v12[v24 + 10] = v44;
        *(_OWORD *)&v12[v24 + 12] = v44;
        *(_OWORD *)&v12[v24 + 14] = v44;
        v24 += 16;
        v43 -= 4LL;
      }
      while ( v43 != 0 );
    }
    else
    {
      v24 = 0;
    }
    if ( (((unsigned __int8)(((v22 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != 0 )
    {
      v45 = (__int64)&v12[v24 + 2];
      v46 = 0;
      v47 = MEMORY[0x1418B5CF0];
      do
      {
        *(_OWORD *)(v45 + v46 - 16) = v47;
        *(_OWORD *)(v45 + v46) = v47;
        v46 += 32;
      }
      while ( 32LL * (((unsigned __int8)(((v22 & 0xFFFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1) & 3) != v46 );
    }
    v12 += v23;
    if ( v22 != v23 )
    {
      v22 &= 3u;
      do
      {
LABEL_84:
        *v12++ = 0xFFFFFFFFFFFFFFLL;
        --v22;
      }
      while ( v22 != 0 );
    }
  }
  *(_QWORD *)(a1 + 104) = v12;
  if ( (_BYTE)v10 == 0 )
    goto LABEL_86;
LABEL_69:
  v38 = v78;
  v39 = (__int64)v79;
  v40 = 8;
  v41 = 0;
  do
  {
    v42 = *(_QWORD *)(a1 + 96);
    if ( v42 + v40 - 8 == v39 )
    {
      v38 += 8;
    }
    else
    {
      if ( v38 != 0 && v76 != nullptr )
      {
        (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
        LOBYTE(v10) = v80;
      }
      v77 = (__int64 *)(v42 + v40 - 8);
      v38 = 8;
    }
    v78 = v38;
    v39 = v42 + 8 * v41 + 8;
    v79 = (unsigned __int8 *)(v40 + v42);
    ++v41;
    v40 += 8;
  }
  while ( v41 < (unsigned __int8)v10 );
LABEL_87:
  if ( v38 != 0 && v76 != nullptr )
  {
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    LOBYTE(v10) = v80;
  }
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( (_BYTE)v10 == 0 )
  {
LABEL_119:
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v77 = (__int64 *)&v81;
    v78 = 1;
    v79 = (unsigned __int8 *)v82;
    v60 = 1;
LABEL_123:
    v49 = (unsigned __int64)v76;
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v60);
    goto LABEL_125;
  }
  v10 = (unsigned __int8)v10;
  do
  {
    v51 = v10--;
    v52 = *(unsigned __int8 *)(*(_QWORD *)(a1 + 96) + 8 * v51 - 2);
    v53 = sub_1400015B0();
    if ( (unsigned __int8)((__int64 (*)(void))sub_1400015E0)() == 0 )
    {
      v48 = *(_QWORD *)(a1 + 96);
LABEL_93:
      v49 = v48 + 8 * v10;
      v50 = *(_QWORD *)(a1 + 104);
LABEL_94:
      sub_141758A00(a1: v49, a2: v48 + 8 * v51, a3: v50 - (v48 + 8 * v51));
      *(_QWORD *)(a1 + 104) -= 8LL;
      continue;
    }
    if ( v52 <= 0x38 && (v54 = 0x18000470040F93FLL, _bittest64(&v54, v52)) )
    {
      v48 = *(_QWORD *)(a1 + 96);
    }
    else
    {
      v48 = *(_QWORD *)(a1 + 96);
      if ( v53 != 0 )
        goto LABEL_93;
    }
    v55 = *(_BYTE *)(v48 + 8 * v10 + 6);
    if ( (unsigned __int8)sub_1400015B0() != 0
      || (v55 > 0x1Fu || (v49 = 2282160129LL, !_bittest((const int *)&v49, v55))) && (v55 & 0xFE) != 0x3A )
    {
      v56 = *(_QWORD *)(a1 + 96);
      v49 = *(unsigned __int8 *)(v56 + 8 * v10 + 6);
      if ( v49 > 0x29 || (v57 = 0x3002778EF38LL, !_bittest64(&v57, v49)) )
        *(_WORD *)(v56 + 8 * v10 + 4) = -1;
    }
    if ( (unsigned __int16)qword_141B60330 <= 0xDEAu )
    {
      v48 = *(_QWORD *)(a1 + 96);
      v50 = *(_QWORD *)(a1 + 104);
      v58 = (v50 - v48) >> 3;
      if ( v51 < v58 )
      {
        v49 = v48 + 8 * v10;
        v59 = v51;
        while ( *(_BYTE *)(v48 + 8 * v10 + 6) != *(_BYTE *)(v48 + 8 * v59 + 6)
             || *(_DWORD *)v49 != *(_DWORD *)(v48 + 8 * v59)
             || *(_WORD *)(v48 + 8 * v10 + 4) != *(_WORD *)(v48 + 8 * v59 + 4) )
        {
          if ( ++v59 >= v58 )
            goto LABEL_95;
        }
        goto LABEL_94;
      }
    }
LABEL_95:
    ;
  }
  while ( v10 != 0 );
  if ( v79 != &v81 )
    goto LABEL_119;
  v60 = v78 + 1;
  v67 = v78++ == -1;
  v79 = (unsigned __int8 *)v82;
  if ( !v67 )
    goto LABEL_123;
LABEL_125:
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  v61 = v81;
  if ( v81 != 0 )
  {
    sub_141196590(a1: a1 + 120, a2: v81, a3: &v75);
    if ( v81 != 0 )
    {
      v62 = 0;
      for ( i = 0; i < v81; ++i )
      {
        sub_14156AF70(a1: v62 + *(_QWORD *)(a1 + 120), a2: &v76);
        v62 += 32;
      }
    }
  }
  if ( (unsigned __int8)sub_1400015E0(a1: v49, a2: v61, a3: v60) == 0 )
  {
    v64 = *(_QWORD *)(a1 + 120);
    if ( v64 != *(_QWORD *)(a1 + 128) )
      *(_QWORD *)(a1 + 128) = v64;
  }
  v65 = &v75;
  if ( v79 == (unsigned __int8 *)&v75 )
  {
    v67 = v78 == -4;
    v66 = v78 + 4;
    v78 += 4;
    v79 = (unsigned __int8 *)&v75 + 4;
    if ( !v67 )
      goto LABEL_138;
  }
  else
  {
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
    v77 = &v75;
    v78 = 4;
    v79 = (unsigned __int8 *)&v75 + 4;
    v66 = 4;
LABEL_138:
    if ( v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v66);
  }
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( (_DWORD)v75 == 0 )
  {
LABEL_152:
    if ( v78 != 0 && v76 != nullptr )
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
    v77 = (__int64 *)(a1 + 180);
    v71 = 1;
    goto LABEL_157;
  }
  v68 = 0;
  LODWORD(v65) = 124518401;
  while ( 2 )
  {
    v69 = sub_141750CC0(a1: 32);
    *(_QWORD *)(v69 + 8) = 0;
    *(_QWORD *)(v69 + 24) = 0;
    *(_QWORD *)v69 = 0;
    *(_DWORD *)(v69 + 12) = -1;
    *(_QWORD *)(v69 + 16) = 0x76C0001076C0001LL;
    *(_BYTE *)(v69 + 26) = 3;
    if ( v79 == (unsigned __int8 *)v69 )
    {
      v67 = v78 == -31;
      v70 = v78 + 31;
      v78 += 31;
      v79 = (unsigned __int8 *)(v69 + 31);
      if ( !v67 )
        goto LABEL_149;
    }
    else
    {
      if ( v78 != 0 && v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v78);
      v77 = (__int64 *)v69;
      v78 = 31;
      v79 = (unsigned __int8 *)(v69 + 31);
      v70 = 31;
LABEL_149:
      if ( v76 != nullptr )
        (*(void (__fastcall **)(_DWORD *, __int64 *, __int64))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77, a3: v70);
    }
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    sub_141750CFC(a1: v69);
    if ( ++v68 < (unsigned __int64)(unsigned int)v75 )
      continue;
    break;
  }
  if ( v79 != (unsigned __int8 *)(a1 + 180) )
    goto LABEL_152;
  v71 = v78 + 1;
LABEL_157:
  v78 = v71;
  v79 = (unsigned __int8 *)(a1 + 181);
  if ( sub_140EDF6C0(a1: v74, a2: &v76) == 0 )
    goto LABEL_166;
  if ( v78 != 0 && v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  if ( (unsigned __int8)sub_140EDFB90(a1, a2: (__int64 *)&v76) == 0 )
  {
LABEL_166:
    LODWORD(v65) = 0;
    goto LABEL_167;
  }
  if ( v78 != 0 && v76 != nullptr )
    (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
  v79 = nullptr;
  v78 = 0;
  v77 = nullptr;
  LOBYTE(v65) = v76[4] == 0;
LABEL_167:
  if ( v78 != 0 )
  {
    if ( v76 != nullptr )
    {
      (*(void (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)v76 + 40LL))(a1: v76, a2: v77);
      goto LABEL_170;
    }
  }
  else
  {
LABEL_170:
    v72 = (void (__fastcall ***)(_QWORD, __int64))v76;
    v79 = nullptr;
    v78 = 0;
    v77 = nullptr;
    if ( v76 != nullptr && _InterlockedDecrement(v76 + 2) == 0 )
      (**v72)(a1: v72, a2: 1);
  }
  return (unsigned int)v65;
}
