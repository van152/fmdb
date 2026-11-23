__int64 *__fastcall sub_141561880(__int64 *a1, __int64 a2, char a3, char a4, char a5, unsigned __int8 a6)
{
  __int64 *v8; // rsi
  __int64 v9; // rsi
  __int64 v10; // r8
  __int64 v11; // rsi
  _QWORD *v12; // r15
  __int64 v13; // r9
  __int64 v14; // rdi
  __int64 *v15; // rdx
  __int64 v16; // rcx
  __int64 v17; // rdx
  __int64 v18; // r14
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // r13
  unsigned __int64 v24; // rcx
  unsigned __int64 v25; // rax
  unsigned __int64 v26; // rdx
  unsigned __int64 v27; // rax
  __int64 v28; // rbx
  _QWORD *v29; // r14
  __int64 v30; // r15
  __int64 v31; // rbx
  unsigned __int64 v32; // rcx
  __int64 v33; // r8
  __int64 v34; // r14
  bool v35; // al
  __int64 v36; // rcx
  _QWORD *v37; // r12
  __int64 v38; // r9
  __int64 v39; // r13
  __int64 *v40; // rdx
  __int64 v41; // rcx
  __int64 v42; // rdx
  __int64 v43; // r14
  __int64 v44; // rax
  __int64 v45; // rcx
  __int64 v46; // rax
  __int64 v47; // rcx
  __int64 v48; // r12
  unsigned __int64 v49; // rax
  unsigned __int64 v50; // rdx
  unsigned __int64 v51; // rax
  __int64 v52; // rdi
  _QWORD *v53; // r14
  __int64 v54; // rbx
  unsigned __int64 v55; // rcx
  __int64 v56; // r8
  __int64 v57; // r14
  bool v58; // al
  _QWORD *v59; // r12
  __int64 v60; // r9
  __int64 v61; // r13
  __int64 *v62; // rdx
  __int64 v63; // rcx
  __int64 v64; // rdx
  __int64 v65; // r14
  __int64 v66; // rax
  __int64 v67; // rcx
  __int64 v68; // rax
  __int64 v69; // rcx
  __int64 v70; // r15
  unsigned __int64 v71; // rcx
  unsigned __int64 v72; // rax
  unsigned __int64 v73; // rdx
  unsigned __int64 v74; // rax
  __int64 v75; // rdi
  _QWORD *v76; // r14
  __int64 v77; // r15
  __int64 v78; // rdi
  unsigned __int64 v79; // rcx
  __int64 v80; // r8
  __int64 v81; // r14
  bool v82; // al
  __int64 v83; // rdi
  _QWORD *v84; // r15
  __int64 v85; // r9
  __int64 i; // rdi
  __int64 *v87; // rdx
  __int64 v88; // rcx
  __int64 v89; // rdx
  __int64 v90; // r14
  __int64 v91; // rax
  __int64 v92; // rcx
  __int64 v93; // rax
  __int64 v94; // rcx
  __int64 v95; // r13
  unsigned __int64 v96; // rcx
  unsigned __int64 v97; // rax
  unsigned __int64 v98; // rdx
  unsigned __int64 v99; // rax
  __int64 v100; // rbx
  _QWORD *v101; // r14
  __int64 v102; // r15
  __int64 v103; // rbx
  unsigned __int64 v104; // rcx
  __int64 v105; // r8
  __int64 v106; // r14
  bool v107; // al
  __int64 v108; // rcx
  __int64 *v109; // rdx
  __int64 v110; // rcx
  __int64 v111; // rdx
  __int64 v112; // r15
  __int64 v113; // rcx
  _QWORD *v114; // rbx
  __int64 v115; // r13
  unsigned __int64 v116; // rcx
  unsigned __int64 v117; // rax
  unsigned __int64 v118; // r10
  unsigned __int64 v119; // rax
  __int64 v120; // r14
  _QWORD *v121; // r15
  __int64 v122; // rbx
  unsigned __int64 v123; // rcx
  __int64 v124; // r8
  __int64 v125; // r15
  bool v126; // al
  __int64 v128; // [rsp+28h] [rbp-28h]
  unsigned __int64 v131; // [rsp+40h] [rbp-10h]
  __int64 v132; // [rsp+48h] [rbp-8h]
  _QWORD *v133; // [rsp+48h] [rbp-8h]
  __int64 v134; // [rsp+48h] [rbp-8h]
  __int64 v135; // [rsp+48h] [rbp-8h]
  unsigned __int64 v136; // [rsp+48h] [rbp-8h]

  v8 = a1;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
        v8 = a1;
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v8[2] = 0;
  v8[1] = 0;
  *v8 = 0;
  v9 = *(_QWORD *)(*(_QWORD *)(qword_141B5FE40 + 128) + 8LL) - **(_QWORD **)(qword_141B5FE40 + 128);
  if ( v9 != 0 )
  {
    v10 = a6;
    v11 = v9 >> 3;
    if ( a3 != 0 )
    {
      if ( a4 != 0 )
      {
        v12 = nullptr;
        v13 = 0x1FFFFFFFFFFFFFFFLL;
        v14 = 0;
        while ( 1 )
        {
          if ( (int)v14 >= 0 )
          {
            if ( (_BYTE)word_141B60320 != 0 )
            {
              v15 = *(__int64 **)(qword_141B5FE40 + 128);
              v16 = *v15;
              v17 = v15[1];
            }
            else
            {
              v16 = *(_QWORD *)(qword_141B5FE40 + 96);
              v17 = *(_QWORD *)(qword_141B5FE40 + 104);
            }
            if ( (v17 - v16) >> 3 > (unsigned __int64)(unsigned int)v14 )
            {
              v18 = *(_QWORD *)(v16 + 8LL * (unsigned int)v14);
              if ( v18 != 0 )
              {
                v19 = *(_QWORD *)(v18 + 112);
                if ( v19 == 0 )
                  v19 = *(_QWORD *)(v18 + 104);
                if ( v19 == a2 )
                {
LABEL_8:
                  if ( v12 == (_QWORD *)a1[2] )
                  {
                    v23 = (__int64)v12 - *a1;
                    v24 = v23 >> 3;
                    v25 = (unsigned __int64)(v23 >> 3) >> 1;
                    v26 = 0x1FFFFFFFFFFFFFFFLL - v25;
                    v27 = (v23 >> 3) + v25;
                    if ( v27 <= (v23 >> 3) + 1 )
                      v27 = v24 + 1;
                    if ( v24 <= v26 )
                      v13 = v27;
                    v132 = v13;
                    v28 = sub_1407E4490(qword_141ABD470, 8 * v13);
                    *(_QWORD *)(v28 + v23) = v18;
                    v29 = (_QWORD *)a1[1];
                    sub_141758A00();
                    if ( v29 != v12 )
                      sub_141758A00();
                    v30 = v28;
                    v31 = *a1;
                    if ( *a1 != 0 )
                    {
                      v32 = a1[2] - v31;
                      if ( v32 == -1 )
                        v32 = *(unsigned int *)(v31 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v33 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 > v32)
                        && (v34 = *(_QWORD *)(v33 + 8 * v32)) != 0 )
                      {
                        MEMORY[0x1419475D8](v34 + 32, v31 - *(unsigned int *)(v34 + 120));
                        v35 = *(_BYTE *)(v34 + 72) != 0
                           && _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) != 0;
                        if ( !v35 && *(_BYTE *)(v34 + 97) != 0 )
                          sub_1412D33C0(v34);
                      }
                      else
                      {
                        MEMORY[0x141948990](v31 - *(unsigned int *)(qword_141ABD470 + 48));
                      }
                    }
                    v36 = v30;
                    *a1 = v30;
                    v12 = (_QWORD *)(v30 + 8 * ((v23 >> 3) + 1));
                    a1[1] = (__int64)v12;
                    a1[2] = v36 + 8 * v132;
                    LOBYTE(v10) = a6;
                    v13 = 0x1FFFFFFFFFFFFFFFLL;
                  }
                  else
                  {
                    *v12 = v18;
                    v12 = (_QWORD *)(a1[1] + 8);
                    a1[1] = (__int64)v12;
                  }
                  goto LABEL_10;
                }
                if ( v19 != 0 && (_BYTE)v10 != 0 )
                {
                  v20 = *(_QWORD *)(v19 + 176);
                  if ( v20 != 0 )
                  {
                    v21 = *(_QWORD *)(v20 + 1576);
                    if ( v21 == 0 )
                      goto LABEL_10;
                    v22 = *(_QWORD *)(v21 + 288);
                  }
                  else
                  {
                    v22 = *(_QWORD *)(v19 + 104);
                    if ( v22 == v19 )
                      v22 = 0;
                  }
                  if ( v22 == a2 )
                    goto LABEL_8;
                }
              }
            }
          }
LABEL_10:
          if ( v11 == ++v14 )
            return a1;
        }
      }
      v59 = nullptr;
      v60 = 0x1FFFFFFFFFFFFFFFLL;
      v61 = 0;
      while ( 1 )
      {
        if ( (int)v61 >= 0 )
        {
          if ( (_BYTE)word_141B60320 != 0 )
          {
            v62 = *(__int64 **)(qword_141B5FE40 + 128);
            v63 = *v62;
            v64 = v62[1];
          }
          else
          {
            v63 = *(_QWORD *)(qword_141B5FE40 + 96);
            v64 = *(_QWORD *)(qword_141B5FE40 + 104);
          }
          if ( (v64 - v63) >> 3 > (unsigned __int64)(unsigned int)v61 )
          {
            v65 = *(_QWORD *)(v63 + 8LL * (unsigned int)v61);
            if ( v65 != 0 )
            {
              v66 = *(_QWORD *)(v65 + 88);
              if ( v66 == 0 )
                v66 = *(_QWORD *)(v65 + 80);
              if ( v66 == a2 )
              {
LABEL_91:
                if ( v59 == (_QWORD *)a1[2] )
                {
                  v70 = (__int64)v59 - *a1;
                  v71 = v70 >> 3;
                  v72 = (unsigned __int64)(v70 >> 3) >> 1;
                  v73 = 0x1FFFFFFFFFFFFFFFLL - v72;
                  v74 = (v70 >> 3) + v72;
                  v131 = (v70 >> 3) + 1;
                  if ( v74 <= v131 )
                    v74 = v71 + 1;
                  if ( v71 <= v73 )
                    v60 = v74;
                  v134 = v60;
                  v75 = sub_1407E4490(qword_141ABD470, 8 * v60);
                  *(_QWORD *)(v75 + v70) = v65;
                  v76 = (_QWORD *)a1[1];
                  sub_141758A00();
                  if ( v76 != v59 )
                    sub_141758A00();
                  v77 = v75;
                  v78 = *a1;
                  if ( *a1 != 0 )
                  {
                    v79 = a1[2] - v78;
                    if ( v79 == -1 )
                      v79 = *(unsigned int *)(v78 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v80 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v80) >> 3 > v79)
                      && (v81 = *(_QWORD *)(v80 + 8 * v79)) != 0 )
                    {
                      MEMORY[0x1419475D8](v81 + 32, v78 - *(unsigned int *)(v81 + 120));
                      v82 = *(_BYTE *)(v81 + 72) != 0
                         && _InterlockedDecrement((volatile signed __int32 *)(v81 + 64)) != 0;
                      if ( !v82 && *(_BYTE *)(v81 + 97) != 0 )
                        sub_1412D33C0(v81);
                    }
                    else
                    {
                      MEMORY[0x141948990](v78 - *(unsigned int *)(qword_141ABD470 + 48));
                    }
                  }
                  *a1 = v77;
                  v59 = (_QWORD *)(v77 + 8 * v131);
                  a1[1] = (__int64)v59;
                  a1[2] = v77 + 8 * v134;
                  LOBYTE(v10) = a6;
                  v60 = 0x1FFFFFFFFFFFFFFFLL;
                }
                else
                {
                  *v59 = v65;
                  v59 = (_QWORD *)(a1[1] + 8);
                  a1[1] = (__int64)v59;
                }
                goto LABEL_93;
              }
              if ( v66 != 0 && (_BYTE)v10 != 0 )
              {
                v67 = *(_QWORD *)(v66 + 176);
                if ( v67 != 0 )
                {
                  v68 = *(_QWORD *)(v67 + 1576);
                  if ( v68 == 0 )
                    goto LABEL_93;
                  v69 = *(_QWORD *)(v68 + 288);
                }
                else
                {
                  v69 = *(_QWORD *)(v66 + 104);
                  if ( v69 == v66 )
                    v69 = 0;
                }
                if ( v69 == a2 )
                  goto LABEL_91;
              }
            }
          }
        }
LABEL_93:
        if ( v11 == ++v61 )
          return a1;
      }
    }
    if ( a4 != 0 )
    {
      v37 = nullptr;
      v38 = 0x1FFFFFFFFFFFFFFFLL;
      v39 = 0;
      while ( 1 )
      {
        if ( (int)v39 >= 0 )
        {
          if ( (_BYTE)word_141B60320 != 0 )
          {
            v40 = *(__int64 **)(qword_141B5FE40 + 128);
            v41 = *v40;
            v42 = v40[1];
          }
          else
          {
            v41 = *(_QWORD *)(qword_141B5FE40 + 96);
            v42 = *(_QWORD *)(qword_141B5FE40 + 104);
          }
          if ( (v42 - v41) >> 3 > (unsigned __int64)(unsigned int)v39 )
          {
            v43 = *(_QWORD *)(v41 + 8LL * (unsigned int)v39);
            if ( v43 != 0 )
            {
              v44 = *(_QWORD *)(v43 + 104);
              if ( v44 == a2 )
                goto LABEL_51;
              if ( v44 != 0 && (_BYTE)v10 != 0 )
              {
                v45 = *(_QWORD *)(v44 + 176);
                if ( v45 != 0 )
                {
                  v46 = *(_QWORD *)(v45 + 1576);
                  if ( v46 == 0 )
                    goto LABEL_53;
                  v47 = *(_QWORD *)(v46 + 288);
                }
                else
                {
                  v47 = *(_QWORD *)(v44 + 104);
                  if ( v47 == v44 )
                    v47 = 0;
                }
                if ( v47 == a2 )
                {
LABEL_51:
                  if ( v37 == (_QWORD *)a1[2] )
                  {
                    v133 = v37;
                    v48 = (__int64)v37 - *a1;
                    v49 = (unsigned __int64)(v48 >> 3) >> 1;
                    v50 = 0x1FFFFFFFFFFFFFFFLL - v49;
                    v51 = (v48 >> 3) + v49;
                    if ( v51 <= (v48 >> 3) + 1 )
                      v51 = (v48 >> 3) + 1;
                    if ( v48 >> 3 <= v50 )
                      v38 = v51;
                    v128 = v38;
                    v52 = sub_1407E4490(qword_141ABD470, 8 * v38);
                    *(_QWORD *)(v52 + v48) = v43;
                    v53 = (_QWORD *)a1[1];
                    sub_141758A00();
                    if ( v53 != v133 )
                      sub_141758A00();
                    v54 = *a1;
                    if ( *a1 != 0 )
                    {
                      v55 = a1[2] - v54;
                      if ( v55 == -1 )
                        v55 = *(unsigned int *)(v54 - *(unsigned int *)(qword_141ABD470 + 48));
                      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                        && (v56 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v56) >> 3 > v55)
                        && (v57 = *(_QWORD *)(v56 + 8 * v55)) != 0 )
                      {
                        MEMORY[0x1419475D8](v57 + 32, v54 - *(unsigned int *)(v57 + 120));
                        v58 = *(_BYTE *)(v57 + 72) != 0
                           && _InterlockedDecrement((volatile signed __int32 *)(v57 + 64)) != 0;
                        if ( !v58 && *(_BYTE *)(v57 + 97) != 0 )
                          sub_1412D33C0(v57);
                      }
                      else
                      {
                        MEMORY[0x141948990](v54 - *(unsigned int *)(qword_141ABD470 + 48));
                      }
                    }
                    *a1 = v52;
                    v37 = (_QWORD *)(v52 + 8 * ((v48 >> 3) + 1));
                    a1[1] = (__int64)v37;
                    a1[2] = v52 + 8 * v128;
                    LOBYTE(v10) = a6;
                    v38 = 0x1FFFFFFFFFFFFFFFLL;
                  }
                  else
                  {
                    *v37 = v43;
                    v37 = (_QWORD *)(a1[1] + 8);
                    a1[1] = (__int64)v37;
                  }
                }
              }
            }
          }
        }
LABEL_53:
        if ( v11 == ++v39 )
          return a1;
      }
    }
    if ( a5 != 0 )
    {
      v83 = 0;
      do
      {
        if ( (int)v83 >= 0 )
        {
          if ( (_BYTE)word_141B60320 != 0 )
          {
            v109 = *(__int64 **)(qword_141B5FE40 + 128);
            v110 = *v109;
            v111 = v109[1];
          }
          else
          {
            v110 = *(_QWORD *)(qword_141B5FE40 + 96);
            v111 = *(_QWORD *)(qword_141B5FE40 + 104);
          }
          if ( (v111 - v110) >> 3 > (unsigned __int64)(unsigned int)v83 )
          {
            v112 = *(_QWORD *)(v110 + 8LL * (unsigned int)v83);
            if ( v112 != 0 && *(_BYTE *)(v112 + 47) == 0 )
            {
              v113 = *(_QWORD *)(v112 + 48);
              if ( v113 != 0 && (unsigned __int8)sub_140E65110(v113, *(unsigned int *)(a2 + 12), v10) != 0 )
              {
                v114 = (_QWORD *)a1[1];
                if ( v114 == (_QWORD *)a1[2] )
                {
                  v115 = (__int64)v114 - *a1;
                  v116 = v115 >> 3;
                  v117 = (unsigned __int64)(v115 >> 3) >> 1;
                  v118 = 0x1FFFFFFFFFFFFFFFLL - v117;
                  v119 = (v115 >> 3) + v117;
                  if ( v119 <= (v115 >> 3) + 1 )
                    v119 = v116 + 1;
                  if ( v116 > v118 )
                    v119 = 0x1FFFFFFFFFFFFFFFLL;
                  v136 = v119;
                  v120 = sub_1407E4490(qword_141ABD470, 8 * v119);
                  *(_QWORD *)(v120 + v115) = v112;
                  v121 = (_QWORD *)a1[1];
                  sub_141758A00();
                  if ( v121 != v114 )
                    sub_141758A00();
                  v122 = *a1;
                  if ( *a1 != 0 )
                  {
                    v123 = a1[2] - v122;
                    if ( v123 == -1 )
                      v123 = *(unsigned int *)(v122 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                      && (v124 = *(_QWORD *)(qword_141ABD470 + 24),
                          (*(_QWORD *)(qword_141ABD470 + 32) - v124) >> 3 > v123)
                      && (v125 = *(_QWORD *)(v124 + 8 * v123)) != 0 )
                    {
                      MEMORY[0x1419475D8](v125 + 32, v122 - *(unsigned int *)(v125 + 120));
                      v126 = *(_BYTE *)(v125 + 72) != 0
                          && _InterlockedDecrement((volatile signed __int32 *)(v125 + 64)) != 0;
                      if ( !v126 && *(_BYTE *)(v125 + 97) != 0 )
                        sub_1412D33C0(v125);
                    }
                    else
                    {
                      MEMORY[0x141948990](v122 - *(unsigned int *)(qword_141ABD470 + 48));
                    }
                  }
                  *a1 = v120;
                  a1[1] = v120 + 8 * ((v115 >> 3) + 1);
                  a1[2] = v120 + 8 * v136;
                }
                else
                {
                  *v114 = v112;
                  a1[1] += 8;
                }
              }
            }
          }
        }
        ++v83;
      }
      while ( v11 != v83 );
      return a1;
    }
    v84 = nullptr;
    v85 = 0x1FFFFFFFFFFFFFFFLL;
    for ( i = 0; v11 != i; ++i )
    {
      if ( (int)i >= 0 )
      {
        if ( (_BYTE)word_141B60320 != 0 )
        {
          v87 = *(__int64 **)(qword_141B5FE40 + 128);
          v88 = *v87;
          v89 = v87[1];
        }
        else
        {
          v88 = *(_QWORD *)(qword_141B5FE40 + 96);
          v89 = *(_QWORD *)(qword_141B5FE40 + 104);
        }
        if ( (v89 - v88) >> 3 > (unsigned __int64)(unsigned int)i )
        {
          v90 = *(_QWORD *)(v88 + 8LL * (unsigned int)i);
          if ( v90 != 0 )
          {
            v91 = *(_QWORD *)(v90 + 48);
            if ( v91 != 0 )
              v91 = *(_QWORD *)(v90 + 80);
            if ( v91 == a2 )
            {
LABEL_135:
              if ( v84 == (_QWORD *)a1[2] )
              {
                v95 = (__int64)v84 - *a1;
                v96 = v95 >> 3;
                v97 = (unsigned __int64)(v95 >> 3) >> 1;
                v98 = 0x1FFFFFFFFFFFFFFFLL - v97;
                v99 = (v95 >> 3) + v97;
                if ( v99 <= (v95 >> 3) + 1 )
                  v99 = v96 + 1;
                if ( v96 <= v98 )
                  v85 = v99;
                v135 = v85;
                v100 = sub_1407E4490(qword_141ABD470, 8 * v85);
                *(_QWORD *)(v100 + v95) = v90;
                v101 = (_QWORD *)a1[1];
                sub_141758A00();
                if ( v101 != v84 )
                  sub_141758A00();
                v102 = v100;
                v103 = *a1;
                if ( *a1 != 0 )
                {
                  v104 = a1[2] - v103;
                  if ( v104 == -1 )
                    v104 = *(unsigned int *)(v103 - *(unsigned int *)(qword_141ABD470 + 48));
                  if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                    && (v105 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v105) >> 3 > v104)
                    && (v106 = *(_QWORD *)(v105 + 8 * v104)) != 0 )
                  {
                    MEMORY[0x1419475D8](v106 + 32, v103 - *(unsigned int *)(v106 + 120));
                    v107 = *(_BYTE *)(v106 + 72) != 0
                        && _InterlockedDecrement((volatile signed __int32 *)(v106 + 64)) != 0;
                    if ( !v107 && *(_BYTE *)(v106 + 97) != 0 )
                      sub_1412D33C0(v106);
                  }
                  else
                  {
                    MEMORY[0x141948990](v103 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                }
                v108 = v102;
                *a1 = v102;
                v84 = (_QWORD *)(v102 + 8 * ((v95 >> 3) + 1));
                a1[1] = (__int64)v84;
                a1[2] = v108 + 8 * v135;
                LOBYTE(v10) = a6;
                v85 = 0x1FFFFFFFFFFFFFFFLL;
              }
              else
              {
                *v84 = v90;
                v84 = (_QWORD *)(a1[1] + 8);
                a1[1] = (__int64)v84;
              }
              continue;
            }
            if ( v91 != 0 && (_BYTE)v10 != 0 )
            {
              v92 = *(_QWORD *)(v91 + 176);
              if ( v92 != 0 )
              {
                v93 = *(_QWORD *)(v92 + 1576);
                if ( v93 == 0 )
                  continue;
                v94 = *(_QWORD *)(v93 + 288);
              }
              else
              {
                v94 = *(_QWORD *)(v91 + 104);
                if ( v94 == v91 )
                  v94 = 0;
              }
              if ( v94 == a2 )
                goto LABEL_135;
            }
          }
        }
      }
    }
  }
  return a1;
}
