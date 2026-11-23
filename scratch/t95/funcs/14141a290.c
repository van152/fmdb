char __fastcall sub_14141A290(_QWORD *a1)
{
  _QWORD *v1; // r13
  _QWORD *v2; // rdi
  _QWORD *v3; // r14
  _QWORD *v4; // rsi
  _QWORD *v5; // rbx
  __int64 v6; // rbx
  unsigned __int64 v7; // rcx
  __int64 v8; // rdx
  __int64 v9; // rbx
  _QWORD *v10; // rdi
  _QWORD *v11; // r14
  _QWORD *v12; // rsi
  _QWORD *v13; // rbx
  __int64 v14; // rbx
  unsigned __int64 v15; // rcx
  __int64 v16; // rdx
  __int64 v17; // rbx
  __int64 v18; // rsi
  unsigned __int64 v19; // rcx
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rsi
  unsigned __int64 v23; // rcx
  __int64 v24; // rbx
  __int64 v25; // rbx
  _QWORD *v26; // r14
  _QWORD *v27; // r12
  _QWORD *v28; // rbx
  __int64 v29; // rdi
  unsigned __int64 v30; // rcx
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  unsigned __int64 v34; // rcx
  __int64 v35; // rdx
  __int64 v36; // rsi
  _QWORD *v37; // rdi
  _QWORD *v38; // rsi
  _QWORD *v39; // rbx
  __int64 v40; // rbx
  unsigned __int64 v41; // rcx
  __int64 v42; // rdx
  __int64 v43; // rdi
  __int64 v44; // rsi
  unsigned __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rbx
  _QWORD *v48; // rdi
  _QWORD *v49; // rsi
  _QWORD *v50; // rbx
  __int64 v51; // rbx
  unsigned __int64 v52; // rcx
  __int64 v53; // rdx
  __int64 v54; // rdi
  __int64 v55; // rsi
  __int64 v56; // rdi
  _QWORD *v57; // rdi
  _QWORD *v58; // rsi
  _QWORD *v59; // rbx
  __int64 v60; // rbx
  unsigned __int64 v61; // rcx
  __int64 v62; // rdx
  __int64 v63; // rdi
  __int64 v64; // rdi
  unsigned __int64 v65; // rcx
  __int64 v66; // rbx
  __int64 v67; // rbx
  _QWORD *v68; // rdi
  _QWORD *v69; // rsi
  _QWORD *v70; // rbx
  __int64 v71; // rbx
  unsigned __int64 v72; // rcx
  __int64 v73; // rdx
  __int64 v74; // rdi
  char result; // al
  __int64 v76; // rdi
  unsigned __int64 v77; // rcx
  __int64 v78; // rbx
  __int64 v79; // rbx
  signed __int32 v80; // et0
  __int64 v81; // rsi
  unsigned __int64 v82; // rcx
  __int64 v83; // rbx
  __int64 v84; // rbx
  signed __int32 v85; // et0
  __int64 v86; // rsi
  unsigned __int64 v87; // rcx
  __int64 v88; // rbx
  __int64 v89; // rbx
  signed __int32 v90; // et0
  _QWORD **v91; // r15
  _QWORD **v92; // r13
  __int64 *v93; // rsi
  __int64 v94; // rdi
  unsigned __int64 v95; // rcx
  __int64 v96; // rbx
  __int64 v97; // r14
  _QWORD *v98; // rdi
  __int64 v99; // rsi
  _QWORD **v100; // rbx
  unsigned __int64 v101; // rcx
  _QWORD *v102; // rbx
  __int64 v103; // rdx
  __int64 v104; // rsi
  signed __int32 v105; // et0
  _QWORD *v106; // r14
  _QWORD *v107; // rdi
  _QWORD *v108; // rsi
  _QWORD *v109; // rbx
  __int64 v110; // rbx
  unsigned __int64 v111; // rcx
  _QWORD *v112; // r14
  __int64 v113; // rdx
  __int64 v114; // rdi
  signed __int32 v115; // et0
  char v116[8]; // [rsp+28h] [rbp-18h] BYREF
  _QWORD **v117; // [rsp+30h] [rbp-10h]
  _QWORD *v118; // [rsp+38h] [rbp-8h]
  __int64 v119; // [rsp+40h] [rbp+0h]

  v119 = -2;
  v1 = a1;
  v2 = (_QWORD *)a1[53];
  if ( v2 != nullptr )
  {
    v3 = (_QWORD *)*v2;
    v4 = (_QWORD *)v2[1];
    if ( (_QWORD *)*v2 != v4 )
    {
      v5 = (_QWORD *)*v2;
      do
      {
        if ( *v5 != 0 )
          (**(void (__fastcall ***)(_QWORD, __int64))*v5)(*v5, 1);
        ++v5;
      }
      while ( v5 != v4 );
      v6 = v2[1] - (_QWORD)v4;
      sub_141758A00();
      v2[1] = (char *)v3 + v6;
      v4 = (_QWORD *)*v2;
    }
    if ( v4 == nullptr )
      goto LABEL_20;
    v7 = v2[2] - (_QWORD)v4;
    if ( v7 == -1 )
    {
      v7 = *(unsigned int *)((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_18;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_18;
    }
    v8 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v8) >> 3 > v7 )
    {
      v9 = *(_QWORD *)(v8 + 8 * v7);
      if ( v9 != 0 )
      {
        MEMORY[0x1419475D8](v9 + 32, (char *)v4 - *(unsigned int *)(v9 + 120));
        if ( (*(_BYTE *)(v9 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v9 + 64)) == 0)
          && *(_BYTE *)(v9 + 97) != 0 )
        {
          sub_1412D33C0(v9);
        }
        goto LABEL_19;
      }
    }
LABEL_18:
    MEMORY[0x141948990]((char *)v4 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_19:
    v2[2] = 0;
    v2[1] = 0;
    *v2 = 0;
LABEL_20:
    sub_140DC1870(v2);
  }
  v10 = (_QWORD *)v1[52];
  if ( v10 == nullptr )
    goto LABEL_41;
  v11 = (_QWORD *)*v10;
  v12 = (_QWORD *)v10[1];
  if ( (_QWORD *)*v10 != v12 )
  {
    v13 = (_QWORD *)*v10;
    do
    {
      if ( *v13 != 0 )
        (**(void (__fastcall ***)(_QWORD, __int64))*v13)(*v13, 1);
      ++v13;
    }
    while ( v13 != v12 );
    v14 = v10[1] - (_QWORD)v12;
    sub_141758A00();
    v10[1] = (char *)v11 + v14;
    v12 = (_QWORD *)*v10;
  }
  if ( v12 != nullptr )
  {
    v15 = v10[2] - (_QWORD)v12;
    if ( v15 == -1 )
    {
      v15 = *(unsigned int *)((char *)v12 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_38;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_38;
    }
    v16 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 > v15 )
    {
      v17 = *(_QWORD *)(v16 + 8 * v15);
      if ( v17 != 0 )
      {
        MEMORY[0x1419475D8](v17 + 32, (char *)v12 - *(unsigned int *)(v17 + 120));
        if ( (*(_BYTE *)(v17 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v17 + 64)) == 0)
          && *(_BYTE *)(v17 + 97) != 0 )
        {
          sub_1412D33C0(v17);
        }
        goto LABEL_39;
      }
    }
LABEL_38:
    MEMORY[0x141948990]((char *)v12 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_39:
    v10[2] = 0;
    v10[1] = 0;
    *v10 = 0;
  }
  sub_140DC1870(v10);
LABEL_41:
  v18 = v1[49];
  if ( v18 != 0 )
  {
    v19 = v1[51] - v18;
    if ( v19 == -1 )
      v19 = *(unsigned int *)(v18 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v20 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v20) >> 3 > v19)
      && (v21 = *(_QWORD *)(v20 + 8 * v19)) != 0 )
    {
      MEMORY[0x1419475D8](v21 + 32, v18 - *(unsigned int *)(v21 + 120));
      if ( (*(_BYTE *)(v21 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v21 + 64)) == 0)
        && *(_BYTE *)(v21 + 97) != 0 )
      {
        sub_1412D33C0(v21);
      }
    }
    else
    {
      MEMORY[0x141948990](v18 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[51] = 0;
    v1[50] = 0;
    v1[49] = 0;
  }
  v22 = v1[46];
  if ( v22 != 0 )
  {
    v23 = v1[48] - v22;
    if ( v23 == -1 )
      v23 = *(unsigned int *)(v22 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v24 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v24) >> 3 > v23)
      && (v25 = *(_QWORD *)(v24 + 8 * v23)) != 0 )
    {
      MEMORY[0x1419475D8](v25 + 32, v22 - *(unsigned int *)(v25 + 120));
      if ( (*(_BYTE *)(v25 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) == 0)
        && *(_BYTE *)(v25 + 97) != 0 )
      {
        sub_1412D33C0(v25);
      }
    }
    else
    {
      MEMORY[0x141948990](v22 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[48] = 0;
    v1[47] = 0;
    v1[46] = 0;
  }
  v26 = (_QWORD *)v1[43];
  v27 = (_QWORD *)v1[44];
  if ( v26 != v27 )
  {
    v118 = (_QWORD *)v1[43];
    do
    {
      v28 = (_QWORD *)*v26;
      if ( *v26 != 0 )
      {
        v29 = v28[4];
        if ( v29 != 0 )
        {
          v30 = v28[6] - v29;
          if ( v30 == -1 )
            v30 = *(unsigned int *)(v29 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v31 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v31) >> 3 > v30)
            && (v32 = *(_QWORD *)(v31 + 8 * v30)) != 0 )
          {
            MEMORY[0x1419475D8](v32 + 32, v29 - *(unsigned int *)(v32 + 120));
            if ( (*(_BYTE *)(v32 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v32 + 64)) == 0)
              && *(_BYTE *)(v32 + 97) != 0 )
            {
              sub_1412D33C0(v32);
            }
          }
          else
          {
            MEMORY[0x141948990](v29 - *(unsigned int *)(qword_141ABD470 + 48));
          }
          v28[6] = 0;
          v28[5] = 0;
          v28[4] = 0;
        }
        sub_14141D1A0(v28);
      }
      ++v26;
    }
    while ( v26 != v27 );
    v33 = v1[44] - (_QWORD)v27;
    sub_141758A00();
    v1[44] = (char *)v118 + v33;
    v27 = (_QWORD *)v1[43];
  }
  if ( v27 != nullptr )
  {
    v34 = v1[45] - (_QWORD)v27;
    if ( v34 == -1 )
      v34 = *(unsigned int *)((char *)v27 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v35 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v35) >> 3 > v34)
      && (v36 = *(_QWORD *)(v35 + 8 * v34)) != 0 )
    {
      MEMORY[0x1419475D8](v36 + 32, (char *)v27 - *(unsigned int *)(v36 + 120));
      if ( (*(_BYTE *)(v36 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v36 + 64)) == 0)
        && *(_BYTE *)(v36 + 97) != 0 )
      {
        sub_1412D33C0(v36);
      }
    }
    else
    {
      MEMORY[0x141948990]((char *)v27 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[45] = 0;
    v1[44] = 0;
    v1[43] = 0;
  }
  v37 = (_QWORD *)v1[40];
  v38 = (_QWORD *)v1[41];
  if ( v37 != v38 )
  {
    v39 = (_QWORD *)v1[40];
    do
    {
      if ( *v39 != 0 )
        sub_14141D040();
      ++v39;
    }
    while ( v39 != v38 );
    v40 = v1[41] - (_QWORD)v38;
    sub_141758A00();
    v1[41] = (char *)v37 + v40;
    v38 = (_QWORD *)v1[40];
  }
  if ( v38 != nullptr )
  {
    v41 = v1[42] - (_QWORD)v38;
    if ( v41 == -1 )
      v41 = *(unsigned int *)((char *)v38 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v42 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v42) >> 3 > v41)
      && (v43 = *(_QWORD *)(v42 + 8 * v41)) != 0 )
    {
      MEMORY[0x1419475D8](v43 + 32, (char *)v38 - *(unsigned int *)(v43 + 120));
      if ( (*(_BYTE *)(v43 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v43 + 64)) == 0)
        && *(_BYTE *)(v43 + 97) != 0 )
      {
        sub_1412D33C0(v43);
      }
    }
    else
    {
      MEMORY[0x141948990]((char *)v38 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[42] = 0;
    v1[41] = 0;
    v1[40] = 0;
  }
  v44 = v1[37];
  if ( v44 != 0 )
  {
    v45 = v1[39] - v44;
    if ( v45 == -1 )
      v45 = *(unsigned int *)(v44 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v46 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v46) >> 3 > v45)
      && (v47 = *(_QWORD *)(v46 + 8 * v45)) != 0 )
    {
      MEMORY[0x1419475D8](v47 + 32, v44 - *(unsigned int *)(v47 + 120));
      if ( (*(_BYTE *)(v47 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v47 + 64)) == 0)
        && *(_BYTE *)(v47 + 97) != 0 )
      {
        sub_1412D33C0(v47);
      }
    }
    else
    {
      MEMORY[0x141948990](v44 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[39] = 0;
    v1[38] = 0;
    v1[37] = 0;
  }
  v48 = (_QWORD *)v1[34];
  v49 = (_QWORD *)v1[35];
  if ( v48 != v49 )
  {
    v50 = (_QWORD *)v1[34];
    do
    {
      if ( *v50 != 0 )
        sub_14141C980();
      ++v50;
    }
    while ( v50 != v49 );
    v51 = v1[35] - (_QWORD)v49;
    sub_141758A00();
    v1[35] = (char *)v48 + v51;
    v49 = (_QWORD *)v1[34];
  }
  if ( v49 != nullptr )
  {
    v52 = v1[36] - (_QWORD)v49;
    if ( v52 == -1 )
      v52 = *(unsigned int *)((char *)v49 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v53 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v53) >> 3 > v52)
      && (v54 = *(_QWORD *)(v53 + 8 * v52)) != 0 )
    {
      MEMORY[0x1419475D8](v54 + 32, (char *)v49 - *(unsigned int *)(v54 + 120));
      if ( (*(_BYTE *)(v54 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v54 + 64)) == 0)
        && *(_BYTE *)(v54 + 97) != 0 )
      {
        sub_1412D33C0(v54);
      }
    }
    else
    {
      MEMORY[0x141948990]((char *)v49 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[36] = 0;
    v1[35] = 0;
    v1[34] = 0;
  }
  v55 = v1[33];
  v118 = v1;
  if ( v55 != 0 )
  {
    sub_1407E4890(qword_141ABD470, *(_QWORD *)v55, 16LL * *(unsigned int *)(v55 + 8));
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
        v1 = v118;
      }
    }
    if ( byte_141B59A9C != 0
      && (unsigned __int64)(qword_141B59A88 - qword_141B59A80) >= 0x81
      && (v56 = *(_QWORD *)(qword_141B59A80 + 128)) != 0 )
    {
      MEMORY[0x1419475D8](v56 + 32, v55 - *(unsigned int *)(v56 + 120));
      if ( (*(_BYTE *)(v56 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v56 + 64)) == 0)
        && *(_BYTE *)(v56 + 97) != 0 )
      {
        sub_1412D33C0(v56);
      }
    }
    else
    {
      MEMORY[0x141948990](v55 - (unsigned int)dword_141B59A98);
    }
  }
  v57 = (_QWORD *)v1[28];
  v58 = (_QWORD *)v1[29];
  if ( v57 != v58 )
  {
    v59 = (_QWORD *)v1[28];
    do
    {
      if ( *v59 != 0 )
        sub_1411FA450();
      ++v59;
    }
    while ( v59 != v58 );
    v60 = v1[29] - (_QWORD)v58;
    sub_141758A00();
    v1[29] = (char *)v57 + v60;
    v58 = (_QWORD *)v1[28];
  }
  if ( v58 != nullptr )
  {
    v61 = v1[30] - (_QWORD)v58;
    if ( v61 == -1 )
      v61 = *(unsigned int *)((char *)v58 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v62 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v62) >> 3 > v61)
      && (v63 = *(_QWORD *)(v62 + 8 * v61)) != 0 )
    {
      MEMORY[0x1419475D8](v63 + 32, (char *)v58 - *(unsigned int *)(v63 + 120));
      if ( (*(_BYTE *)(v63 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v63 + 64)) == 0)
        && *(_BYTE *)(v63 + 97) != 0 )
      {
        sub_1412D33C0(v63);
      }
    }
    else
    {
      MEMORY[0x141948990]((char *)v58 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[30] = 0;
    v1[29] = 0;
    v1[28] = 0;
  }
  sub_14141CAE0(v1 + 25, v116, v1[25], v1[26]);
  v64 = v1[25];
  if ( v64 != 0 )
  {
    v65 = v1[27] - v64;
    if ( v65 == -1 )
    {
      v65 = *(unsigned int *)(v64 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_173;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_173;
    }
    v66 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v66) >> 3 > v65 )
    {
      v67 = *(_QWORD *)(v66 + 8 * v65);
      if ( v67 != 0 )
      {
        MEMORY[0x1419475D8](v67 + 32, v64 - *(unsigned int *)(v67 + 120));
        if ( (*(_BYTE *)(v67 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v67 + 64)) == 0)
          && *(_BYTE *)(v67 + 97) != 0 )
        {
          sub_1412D33C0(v67);
        }
        goto LABEL_174;
      }
    }
LABEL_173:
    MEMORY[0x141948990](v64 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_174:
    v1[27] = 0;
    v1[26] = 0;
    v1[25] = 0;
  }
  v68 = (_QWORD *)v1[22];
  v69 = (_QWORD *)v1[23];
  if ( v68 != v69 )
  {
    v70 = (_QWORD *)v1[22];
    do
    {
      if ( *v70 != 0 )
        sub_14141CEE0();
      ++v70;
    }
    while ( v70 != v69 );
    v71 = v1[23] - (_QWORD)v69;
    sub_141758A00();
    v1[23] = (char *)v68 + v71;
    v69 = (_QWORD *)v1[22];
  }
  if ( v69 != nullptr )
  {
    v72 = v1[24] - (_QWORD)v69;
    if ( v72 == -1 )
      v72 = *(unsigned int *)((char *)v69 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
      && (v73 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v73) >> 3 > v72)
      && (v74 = *(_QWORD *)(v73 + 8 * v72)) != 0 )
    {
      MEMORY[0x1419475D8](v74 + 32, (char *)v69 - *(unsigned int *)(v74 + 120));
      if ( (*(_BYTE *)(v74 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v74 + 64)) == 0)
        && *(_BYTE *)(v74 + 97) != 0 )
      {
        sub_1412D33C0(v74);
      }
    }
    else
    {
      MEMORY[0x141948990]((char *)v69 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v1[24] = 0;
    v1[23] = 0;
    v1[22] = 0;
  }
  result = sub_14141CAE0(v1 + 19, v116, v1[19], v1[20]);
  v76 = v1[19];
  if ( v76 != 0 )
  {
    v77 = v1[21] - v76;
    if ( v77 == -1 )
    {
      v77 = *(unsigned int *)(v76 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_202;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_202;
    }
    v78 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v78) >> 3 > v77 )
    {
      v79 = *(_QWORD *)(v78 + 8 * v77);
      if ( v79 != 0 )
      {
        MEMORY[0x1419475D8](v79 + 32, v76 - *(unsigned int *)(v79 + 120));
        if ( *(_BYTE *)(v79 + 72) != 0 )
        {
          v80 = _InterlockedDecrement((volatile signed __int32 *)(v79 + 64));
          result = v80 != 0;
          if ( v80 != 0 )
            goto LABEL_203;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v79 + 97) != 0 )
          result = sub_1412D33C0(v79);
        goto LABEL_203;
      }
    }
LABEL_202:
    result = MEMORY[0x141948990](v76 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_203:
    v1[21] = 0;
    v1[20] = 0;
    v1[19] = 0;
  }
  v81 = v1[15];
  if ( v81 == 0 )
    goto LABEL_215;
  v82 = v1[17] - v81;
  if ( v82 == -1 )
    v82 = *(unsigned int *)(v81 - *(unsigned int *)(qword_141ABD470 + 48));
  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
  {
    v83 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v83) >> 3 > v82 )
    {
      v84 = *(_QWORD *)(v83 + 8 * v82);
      if ( v84 != 0 )
      {
        MEMORY[0x1419475D8](v84 + 32, v81 - *(unsigned int *)(v84 + 120));
        if ( *(_BYTE *)(v84 + 72) != 0 )
        {
          v85 = _InterlockedDecrement((volatile signed __int32 *)(v84 + 64));
          result = v85 != 0;
          if ( v85 != 0 )
            goto LABEL_214;
        }
        else
        {
          result = 0;
        }
        if ( *(_BYTE *)(v84 + 97) != 0 )
          result = sub_1412D33C0(v84);
        goto LABEL_214;
      }
    }
  }
  result = MEMORY[0x141948990](v81 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_214:
  v1[17] = 0;
  v1[16] = 0;
  v1[15] = 0;
LABEL_215:
  v86 = v1[12];
  if ( v86 != 0 )
  {
    v87 = v1[14] - v86;
    if ( v87 == -1 )
      v87 = *(unsigned int *)(v86 - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0 )
    {
      v88 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v88) >> 3 > v87 )
      {
        v89 = *(_QWORD *)(v88 + 8 * v87);
        if ( v89 != 0 )
        {
          MEMORY[0x1419475D8](v89 + 32, v86 - *(unsigned int *)(v89 + 120));
          if ( *(_BYTE *)(v89 + 72) != 0 )
          {
            v90 = _InterlockedDecrement((volatile signed __int32 *)(v89 + 64));
            result = v90 != 0;
            if ( v90 != 0 )
              goto LABEL_225;
          }
          else
          {
            result = 0;
          }
          if ( *(_BYTE *)(v89 + 97) != 0 )
            result = sub_1412D33C0(v89);
          goto LABEL_225;
        }
      }
    }
    result = MEMORY[0x141948990](v86 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_225:
    v1[14] = 0;
    v1[13] = 0;
    v1[12] = 0;
  }
  v91 = (_QWORD **)v1[9];
  v92 = (_QWORD **)v1[10];
  if ( v91 == v92 )
    goto LABEL_248;
  v117 = v91;
  do
  {
    v93 = *v91;
    if ( *v91 == nullptr )
      goto LABEL_232;
    v94 = *v93;
    if ( *v93 != 0 )
    {
      v95 = v93[2] - v94;
      if ( v95 == -1 )
      {
        v95 = *(unsigned int *)(v94 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          goto LABEL_228;
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_228;
      }
      v96 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v96) >> 3 > v95 )
      {
        v97 = *(_QWORD *)(v96 + 8 * v95);
        if ( v97 != 0 )
        {
          MEMORY[0x1419475D8](v97 + 32, v94 - *(unsigned int *)(v97 + 120));
          if ( (*(_BYTE *)(v97 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v97 + 64)) == 0)
            && *(_BYTE *)(v97 + 97) != 0 )
          {
            sub_1412D33C0(v97);
          }
          goto LABEL_229;
        }
      }
LABEL_228:
      MEMORY[0x141948990](v94 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_229:
      v93[2] = 0;
      v93[1] = 0;
      *v93 = 0;
    }
    if ( dword_141B59AF0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AF0);
      if ( dword_141B59AF0 == -1 )
      {
        sub_1407E5B40(&unk_141B59AB0);
        sub_141751048(sub_1407E6720);
        sub_141750EA0(&dword_141B59AF0);
      }
    }
    sub_1407E6420(&unk_141B59AB0, v93, 32);
LABEL_232:
    ++v91;
  }
  while ( v91 != v92 );
  v98 = v118;
  v99 = v118[10] - (_QWORD)v92;
  v100 = v117;
  result = sub_141758A00();
  v98[10] = (char *)v100 + v99;
  v92 = (_QWORD **)v98[9];
LABEL_248:
  if ( v92 != nullptr )
  {
    v101 = v118[11] - (_QWORD)v92;
    if ( v101 == -1 )
      v101 = *(unsigned int *)((char *)v92 - *(unsigned int *)(qword_141ABD470 + 48));
    v102 = v118 + 9;
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0
      || (v103 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v103) >> 3 <= v101)
      || (v104 = *(_QWORD *)(v103 + 8 * v101)) == 0 )
    {
      result = MEMORY[0x141948990]((char *)v92 - *(unsigned int *)(qword_141ABD470 + 48));
      goto LABEL_258;
    }
    MEMORY[0x1419475D8](v104 + 32, (char *)v92 - *(unsigned int *)(v104 + 120));
    if ( *(_BYTE *)(v104 + 72) != 0 )
    {
      v105 = _InterlockedDecrement((volatile signed __int32 *)(v104 + 64));
      result = v105 != 0;
      if ( v105 != 0 )
        goto LABEL_258;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v104 + 97) != 0 )
      result = sub_1412D33C0(v104);
LABEL_258:
    v102[2] = 0;
    v102[1] = 0;
    *v102 = 0;
  }
  v106 = v118;
  v107 = (_QWORD *)v118[4];
  v108 = (_QWORD *)v118[5];
  if ( v107 != v108 )
  {
    v109 = (_QWORD *)v118[4];
    do
    {
      if ( *v109 != 0 )
        sub_1409E0870();
      ++v109;
    }
    while ( v109 != v108 );
    v110 = v106[5] - (_QWORD)v108;
    result = sub_141758A00();
    v106[5] = (char *)v107 + v110;
    v108 = (_QWORD *)v106[4];
  }
  if ( v108 != nullptr )
  {
    v111 = v106[6] - (_QWORD)v108;
    if ( v111 == -1 )
      v111 = *(unsigned int *)((char *)v108 - *(unsigned int *)(qword_141ABD470 + 48));
    v112 = v106 + 4;
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0
      || (v113 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v113) >> 3 <= v111)
      || (v114 = *(_QWORD *)(v113 + 8 * v111)) == 0 )
    {
      result = MEMORY[0x141948990]((char *)v108 - *(unsigned int *)(qword_141ABD470 + 48));
      goto LABEL_275;
    }
    MEMORY[0x1419475D8](v114 + 32, (char *)v108 - *(unsigned int *)(v114 + 120));
    if ( *(_BYTE *)(v114 + 72) != 0 )
    {
      v115 = _InterlockedDecrement((volatile signed __int32 *)(v114 + 64));
      result = v115 != 0;
      if ( v115 != 0 )
        goto LABEL_275;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v114 + 97) != 0 )
      result = sub_1412D33C0(v114);
LABEL_275:
    v112[2] = 0;
    v112[1] = 0;
    *v112 = 0;
  }
  return result;
}
