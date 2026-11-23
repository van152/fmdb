__int64 __fastcall sub_14090B120(__int64 a1, __int64 *a2, char a3)
{
  char v3; // r15
  __int64 *v4; // r9
  __int64 v5; // r14
  __int64 v6; // rcx
  __int64 result; // rax
  _QWORD *v8; // rbp
  unsigned __int64 v9; // rsi
  _QWORD *v10; // rbx
  __int64 v11; // rdi
  unsigned __int64 v12; // rcx
  unsigned __int64 v13; // r13
  unsigned __int64 v14; // rax
  __int64 v15; // r15
  unsigned __int64 v16; // rdx
  unsigned __int64 v17; // rax
  __int64 v18; // r12
  _QWORD *v19; // rbx
  __int64 v20; // rbx
  unsigned __int64 v21; // rcx
  __int64 v22; // rbp
  __int64 v23; // rdi
  bool v24; // al
  _QWORD *v25; // rbp
  __int64 v26; // rax
  _QWORD *v27; // r14
  _QWORD *v28; // rdi
  __int64 v29; // r8
  __int64 v30; // rax
  unsigned __int64 v31; // rcx
  _QWORD *i; // rsi
  char v33; // al
  unsigned __int64 v34; // r13
  __int64 v35; // rdi
  __int64 v36; // rsi
  __int64 v37; // rbp
  __int64 v38; // rbx
  __int64 v39; // rdi
  unsigned __int64 v40; // rcx
  __int64 v41; // r8
  __int64 v42; // r14
  bool v43; // al
  __int64 v44; // rdx
  __int64 v45; // rdx
  _QWORD *v46; // rbp
  __int64 v47; // rsi
  __int64 v48; // rbx
  __int64 v49; // rdi
  unsigned __int64 v50; // rcx
  unsigned __int64 v51; // r14
  unsigned __int64 v52; // rax
  __int64 v53; // r15
  unsigned __int64 v54; // rdx
  unsigned __int64 v55; // rax
  __int64 v56; // r12
  _QWORD *v57; // rbx
  __int64 v58; // rbx
  unsigned __int64 v59; // rcx
  __int64 v60; // rbp
  __int64 v61; // rdi
  bool v62; // al
  _QWORD *v63; // rdi
  unsigned __int64 v64; // rcx
  _QWORD *j; // rsi
  char v66; // al
  __int64 *v67; // rax
  __int64 v68; // rcx
  __int64 v69; // rax
  __int64 v70; // rax
  __int64 v71; // rdx
  unsigned __int64 v72; // rax
  unsigned __int64 v73; // rcx
  __int64 v74; // rbx
  _QWORD *v75; // rbp
  _QWORD *v76; // rax
  __int64 v77; // rcx
  __int64 v78; // rdi
  unsigned __int64 v79; // rax
  unsigned __int64 v80; // r14
  unsigned __int64 v81; // r12
  unsigned __int64 v82; // rcx
  unsigned __int64 v83; // r12
  __int64 *v84; // rsi
  __int64 v85; // r15
  _QWORD *v86; // rbx
  __int64 v87; // rbx
  unsigned __int64 v88; // rcx
  unsigned __int64 v89; // rsi
  __int64 v90; // r15
  __int64 v91; // rdi
  __int64 v92; // rbx
  __int64 v93; // rbp
  unsigned __int64 v94; // rcx
  __int64 v95; // r8
  __int64 v96; // r14
  bool v97; // al
  __int64 v98; // rbp
  __int64 v99; // rdi
  bool v100; // al
  unsigned int v101; // ecx
  int v102; // edx
  unsigned __int64 v103; // r15
  _QWORD *v104; // rax
  __int64 v105; // rbp
  unsigned __int64 v106; // rcx
  unsigned __int64 v107; // rdx
  __int64 v108; // r12
  _QWORD *v109; // rbp
  __int64 v110; // rdi
  unsigned __int64 v111; // rax
  unsigned __int64 v112; // r13
  unsigned __int64 v113; // rcx
  unsigned __int64 v114; // r13
  __int64 *v115; // r14
  __int64 v116; // rbx
  _QWORD *v117; // rsi
  __int64 v118; // rsi
  bool v119; // zf
  unsigned __int64 v120; // rcx
  __int64 v121; // rbp
  __int64 v122; // rdi
  bool v123; // al
  __int64 v125; // [rsp+78h] [rbp-60h]
  _QWORD *v126; // [rsp+80h] [rbp-58h]
  char v127; // [rsp+88h] [rbp-50h]
  __int64 v128; // [rsp+88h] [rbp-50h]
  unsigned __int64 v129; // [rsp+88h] [rbp-50h]
  unsigned __int64 v130; // [rsp+90h] [rbp-48h]

  v3 = a3;
  v4 = a2;
  v5 = a1;
  v6 = *(_QWORD *)(a1 + 288);
  v125 = v5;
  if ( v6 == 0 || *(_DWORD *)(v6 + 12) != 100000023 )
  {
    v25 = *(_QWORD **)(v5 + 928);
    if ( v25 == nullptr )
      v25 = *(_QWORD **)(v5 + 920);
    if ( v25 != nullptr )
    {
      if ( a3 != 0 )
      {
        v26 = v5;
        v27 = (_QWORD *)(v5 + 1008);
        v28 = (_QWORD *)(v26 + 1016);
        v29 = *(_QWORD *)(v26 + 1008);
        v30 = *(_QWORD *)(v26 + 1016);
        v31 = 0;
        for ( i = v25; i != nullptr; i = (_QWORD *)i[13] )
          v31 += (__int64)(i[2] - i[1]) >> 3;
        if ( (v30 - v29) >> 3 <= v31
          || (v33 = (*(__int64 (__fastcall **)(__int64, _QWORD, __int64, __int64 *))(*(_QWORD *)v125 + 112LL))(
                      v125,
                      0,
                      v29,
                      a2),
              v4 = a2,
              v33 == 0) )
        {
          v34 = 0;
          do
          {
            v6 = v25[13];
            v34 += (__int64)(v25[2] - v25[1]) >> 3;
            v25 = (_QWORD *)v6;
          }
          while ( v6 != 0 );
LABEL_44:
          v126 = v4 + 2;
          v36 = *v4;
          v5 = v125;
          v127 = v3;
          if ( (v4[2] - *v4) >> 3 >= v34 )
            goto LABEL_110;
          if ( v34 <= 0x1FFFFFFFFFFFFFFFLL )
          {
            v37 = v4[1];
            v38 = sub_1407E4490(qword_141ABD470, 8 * v34);
            sub_141758A00();
            v4 = a2;
            v39 = *a2;
            if ( *a2 != 0 )
            {
              v40 = *v126 - v39;
              if ( v40 == -1 )
                v40 = *(unsigned int *)(v39 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v41 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v41) >> 3 > v40)
                && (v42 = *(_QWORD *)(v41 + 8 * v40)) != 0 )
              {
                MEMORY[0x1419475D8](v42 + 32, v39 - *(unsigned int *)(v42 + 120));
                v43 = *(_BYTE *)(v42 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v42 + 64)) != 0;
                v4 = a2;
                if ( v43 || *(_BYTE *)(v42 + 97) == 0 )
                  goto LABEL_84;
                sub_1412D33C0(v42);
              }
              else
              {
                MEMORY[0x141948990](v39 - *(unsigned int *)(qword_141ABD470 + 48));
              }
              v4 = a2;
            }
LABEL_84:
            *v4 = v38;
            v4[1] = v38 + v37 - v36;
            v4[2] = v38 + 8 * v34;
            v5 = v125;
            while ( 1 )
            {
              while ( 1 )
              {
                v63 = *(_QWORD **)(v5 + 928);
                if ( v63 == nullptr )
                  v63 = *(_QWORD **)(v5 + 920);
                --v34;
                if ( v63 != nullptr )
                  break;
                v68 = *(_QWORD *)(v5 + 528);
                if ( v68 == 0 )
                  goto LABEL_110;
                v69 = *(_QWORD *)(v68 + 1976);
                if ( (*(_QWORD *)(v68 + 1984) - v69) >> 3 <= v34 )
                  goto LABEL_110;
                v70 = *(_QWORD *)(v69 + 8 * v34);
                if ( v70 == 0 )
                  goto LABEL_110;
                v67 = (__int64 *)(v70 + 8);
LABEL_107:
                v74 = *v67;
                if ( *v67 == 0 )
                  goto LABEL_110;
                v75 = (_QWORD *)v4[1];
                if ( v75 != (_QWORD *)v4[2] )
                {
                  *v75 = v74;
                  v4[1] += 8;
                  goto LABEL_110;
                }
                v78 = (__int64)v75 - *v4;
                v79 = v78 >> 3;
                v80 = (v78 >> 3) + 1;
                v81 = (unsigned __int64)(v78 >> 3) >> 1;
                v82 = 0x1FFFFFFFFFFFFFFFLL - v81;
                v83 = (v78 >> 3) + v81;
                if ( v83 <= v80 )
                  v83 = v79 + 1;
                if ( v79 > v82 )
                  v83 = 0x1FFFFFFFFFFFFFFFLL;
                v84 = v4;
                v85 = sub_1407E4490(qword_141ABD470, 8 * v83);
                *(_QWORD *)(v85 + v78) = v74;
                v86 = (_QWORD *)v84[1];
                sub_141758A00();
                if ( v86 != v75 )
                  sub_141758A00();
                v87 = *v84;
                v4 = v84;
                if ( *v84 != 0 )
                {
                  v88 = *v126 - v87;
                  if ( v88 == -1 )
                  {
                    v88 = *(unsigned int *)(v87 - *(unsigned int *)(qword_141ABD470 + 48));
                    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                      goto LABEL_144;
                  }
                  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
                  {
                    goto LABEL_144;
                  }
                  v98 = *(_QWORD *)(qword_141ABD470 + 24);
                  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v98) >> 3 > v88 && (v99 = *(_QWORD *)(v98 + 8 * v88)) != 0 )
                  {
                    MEMORY[0x1419475D8](v99 + 32, v87 - *(unsigned int *)(v99 + 120));
                    v100 = *(_BYTE *)(v99 + 72) != 0
                        && _InterlockedDecrement((volatile signed __int32 *)(v99 + 64)) != 0;
                    v4 = a2;
                    if ( v100 || *(_BYTE *)(v99 + 97) == 0 )
                      goto LABEL_146;
                    sub_1412D33C0(v99);
                  }
                  else
                  {
LABEL_144:
                    MEMORY[0x141948990](v87 - *(unsigned int *)(qword_141ABD470 + 48));
                  }
                  v4 = a2;
                }
LABEL_146:
                *v4 = v85;
                v4[1] = v85 + 8 * v80;
                v4[2] = v85 + 8 * v83;
                v5 = v125;
                v3 = v127;
                if ( v34 == 0 )
                  goto LABEL_111;
              }
              if ( v3 != 0 )
              {
                v64 = 0;
                for ( j = v63; j != nullptr; j = (_QWORD *)j[13] )
                  v64 += (__int64)(j[2] - j[1]) >> 3;
                if ( (__int64)(*(_QWORD *)(v5 + 1016) - *(_QWORD *)(v5 + 1008)) >> 3 > v64
                  && (v66 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v5 + 112LL))(v5), v4 = a2, v66 != 0) )
                {
                  v67 = *(__int64 **)(*(_QWORD *)(v5 + 1008) + 8 * v34);
                }
                else
                {
                  v71 = v63[1];
                  v72 = (v63[2] - v71) >> 3;
                  v73 = v34;
                  if ( v72 <= v34 )
                  {
                    v73 = v34;
                    do
                    {
                      v63 = (_QWORD *)v63[13];
                      if ( v63 == nullptr )
                        goto LABEL_110;
                      v73 -= v72;
                      v71 = v63[1];
                      v72 = (v63[2] - v71) >> 3;
                    }
                    while ( v72 <= v73 );
                  }
                  v67 = (__int64 *)(v71 + 8 * v73);
                }
                goto LABEL_107;
              }
LABEL_110:
              if ( v34 == 0 )
                goto LABEL_111;
            }
          }
LABEL_198:
          sub_1400526C0(v6);
        }
LABEL_43:
        v34 = (__int64)(*v28 - *v27) >> 3;
        goto LABEL_44;
      }
    }
    else
    {
      v35 = *(_QWORD *)(v5 + 528);
      if ( v35 != 0 )
      {
        v27 = (_QWORD *)(v35 + 1976);
        v28 = (_QWORD *)(v35 + 1984);
        goto LABEL_43;
      }
    }
    v126 = a2 + 2;
LABEL_111:
    v76 = *(_QWORD **)(v5 + 920);
    if ( (*(_OWORD *)(v5 + 920) != 0
       || (v77 = *(_QWORD *)(v5 + 528)) == 0
       || *(_QWORD *)(v77 + 1984) == *(_QWORD *)(v77 + 1976))
      && v3 == 0
      && v76 != nullptr )
    {
      v89 = 0;
      do
      {
        v6 = (__int64)(v76[2] - v76[1]) >> 3;
        v89 += v6;
        v76 = (_QWORD *)v76[13];
      }
      while ( v76 != nullptr );
      v90 = *v4;
      if ( (v4[2] - *v4) >> 3 < v89 )
      {
        if ( v89 > 0x1FFFFFFFFFFFFFFFLL )
          goto LABEL_198;
        v91 = v4[1];
        v92 = sub_1407E4490(qword_141ABD470, 8 * v89);
        sub_141758A00();
        v4 = a2;
        v93 = *a2;
        if ( *a2 != 0 )
        {
          v94 = *v126 - v93;
          if ( v94 == -1 )
            v94 = *(unsigned int *)(v93 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v95 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v95) >> 3 > v94)
            && (v96 = *(_QWORD *)(v95 + 8 * v94)) != 0 )
          {
            MEMORY[0x1419475D8](v96 + 32, v93 - *(unsigned int *)(v96 + 120));
            v97 = *(_BYTE *)(v96 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v96 + 64)) != 0;
            v4 = a2;
            if ( v97 || *(_BYTE *)(v96 + 97) == 0 )
              goto LABEL_158;
            sub_1412D33C0(v96);
          }
          else
          {
            MEMORY[0x141948990](v93 - *(unsigned int *)(qword_141ABD470 + 48));
          }
          v4 = a2;
        }
LABEL_158:
        *v4 = v92;
        v4[1] = v92 + v91 - v90;
        v4[2] = v92 + 8 * v89;
        v5 = v125;
        goto LABEL_159;
      }
      if ( v89 != 0 )
      {
LABEL_159:
        v103 = 0;
        v130 = v89;
        while ( 1 )
        {
          v104 = *(_QWORD **)(v5 + 920);
          v105 = v104[1];
          v106 = (v104[2] - v105) >> 3;
          v107 = v103;
          if ( v106 > v103 )
          {
LABEL_165:
            v108 = *(_QWORD *)(v105 + 8 * v107);
          }
          else
          {
            while ( 1 )
            {
              v104 = (_QWORD *)v104[13];
              if ( v104 == nullptr )
                break;
              v107 -= v106;
              v105 = v104[1];
              v106 = (v104[2] - v105) >> 3;
              if ( v106 > v107 )
                goto LABEL_165;
            }
            v108 = 0;
          }
          v109 = (_QWORD *)v4[1];
          if ( v109 == (_QWORD *)v4[2] )
            break;
          *v109 = v108;
          v4[1] += 8;
LABEL_161:
          if ( ++v103 == v89 )
            goto LABEL_149;
        }
        v110 = (__int64)v109 - *v4;
        v111 = v110 >> 3;
        v112 = (unsigned __int64)(v110 >> 3) >> 1;
        v113 = 0x1FFFFFFFFFFFFFFFLL - v112;
        v114 = (v110 >> 3) + v112;
        v129 = (v110 >> 3) + 1;
        if ( v114 <= v129 )
          v114 = v111 + 1;
        if ( v111 > v113 )
          v114 = 0x1FFFFFFFFFFFFFFFLL;
        v115 = v4;
        v116 = sub_1407E4490(qword_141ABD470, 8 * v114);
        *(_QWORD *)(v116 + v110) = v108;
        v117 = (_QWORD *)v115[1];
        sub_141758A00();
        if ( v117 != v109 )
          sub_141758A00();
        v118 = *v115;
        v119 = *v115 == 0;
        v4 = v115;
        v5 = v125;
        if ( v119 )
        {
LABEL_185:
          *v4 = v116;
          v4[1] = v116 + 8 * v129;
          v4[2] = v116 + 8 * v114;
          v89 = v130;
          goto LABEL_161;
        }
        v120 = *v126 - v118;
        if ( v120 == -1 )
        {
          v120 = *(unsigned int *)(v118 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
            goto LABEL_183;
        }
        else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
          goto LABEL_183;
        }
        v121 = *(_QWORD *)(qword_141ABD470 + 24);
        if ( (*(_QWORD *)(qword_141ABD470 + 32) - v121) >> 3 > v120 )
        {
          v122 = *(_QWORD *)(v121 + 8 * v120);
          if ( v122 != 0 )
          {
            MEMORY[0x1419475D8](v122 + 32, v118 - *(unsigned int *)(v122 + 120));
            v123 = *(_BYTE *)(v122 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122 + 64)) != 0;
            v4 = a2;
            if ( v123 || *(_BYTE *)(v122 + 97) == 0 )
              goto LABEL_185;
            sub_1412D33C0(v122);
            goto LABEL_184;
          }
        }
LABEL_183:
        MEMORY[0x141948990](v118 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_184:
        v4 = a2;
        goto LABEL_185;
      }
    }
LABEL_149:
    result = *v4;
    if ( *v4 == v4[1] )
    {
      result = *(_QWORD *)(v5 + 288);
      if ( result != 0 && *(_QWORD *)(result + 96) != 0 )
      {
        v101 = *(unsigned __int8 *)(v5 + 572);
        if ( v101 <= 0xE )
        {
          v102 = 16387;
          if ( _bittest(&v102, v101) )
            return sub_140909910(
                     *(_DWORD *)(result + 12),
                     (_DWORD)v4,
                     -1,
                     0,
                     1,
                     -1,
                     -1,
                     255,
                     0,
                     (__int64)&qword_141B5A4A0,
                     0,
                     0,
                     0);
        }
      }
    }
    return result;
  }
  result = *(_QWORD *)(v5 + 1008);
  if ( *(_QWORD *)(v5 + 1016) != result )
  {
    v8 = (_QWORD *)a2[1];
    v9 = 0;
    while ( 1 )
    {
      v10 = *(_QWORD **)(result + 8 * v9);
      if ( v8 == (_QWORD *)v4[2] )
        break;
      *v8 = *v10;
      v8 = (_QWORD *)(v4[1] + 8);
      v4[1] = (__int64)v8;
LABEL_6:
      ++v9;
      result = *(_QWORD *)(v5 + 1008);
      if ( v9 >= (*(_QWORD *)(v5 + 1016) - result) >> 3 )
        return result;
    }
    v11 = (__int64)v8 - *v4;
    v12 = v11 >> 3;
    v13 = (v11 >> 3) + 1;
    v14 = (unsigned __int64)(v11 >> 3) >> 1;
    v15 = 0x1FFFFFFFFFFFFFFFLL;
    v16 = 0x1FFFFFFFFFFFFFFFLL - v14;
    v17 = (v11 >> 3) + v14;
    if ( v17 <= v13 )
      v17 = v12 + 1;
    if ( v12 <= v16 )
      v15 = v17;
    v18 = sub_1407E4490(qword_141ABD470, 8 * v15);
    *(_QWORD *)(v18 + v11) = *v10;
    v19 = (_QWORD *)a2[1];
    sub_141758A00();
    if ( v19 != v8 )
      sub_141758A00();
    v20 = *a2;
    v4 = a2;
    v5 = v125;
    if ( *a2 == 0 )
    {
LABEL_25:
      *v4 = v18;
      v8 = (_QWORD *)(v18 + 8 * v13);
      v4[1] = (__int64)v8;
      v4[2] = v18 + 8 * v15;
      goto LABEL_6;
    }
    v21 = a2[2] - v20;
    if ( v21 == -1 )
    {
      v21 = *(unsigned int *)(v20 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_23;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_23;
    }
    v22 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v22) >> 3 > v21 )
    {
      v23 = *(_QWORD *)(v22 + 8 * v21);
      if ( v23 != 0 )
      {
        MEMORY[0x1419475D8](v23 + 32, v20 - *(unsigned int *)(v23 + 120));
        v24 = *(_BYTE *)(v23 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v23 + 64)) != 0;
        v4 = a2;
        if ( v24 || *(_BYTE *)(v23 + 97) == 0 )
          goto LABEL_25;
        sub_1412D33C0(v23);
        goto LABEL_24;
      }
    }
LABEL_23:
    MEMORY[0x141948990](v20 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_24:
    v4 = a2;
    goto LABEL_25;
  }
  result = *(_QWORD *)(v6 + 24);
  v44 = *(_QWORD *)(v6 + 32) - result;
  if ( v44 != 0 )
  {
    v45 = v44 >> 3;
    v46 = (_QWORD *)v4[1];
    v47 = 0;
    v128 = v45;
    while ( 1 )
    {
      result = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(v5 + 288) + 24LL) + 8 * v47);
      v48 = *(_QWORD *)result;
      if ( v46 == (_QWORD *)v4[2] )
        break;
      *v46 = v48;
      v46 = (_QWORD *)(v4[1] + 8);
      v4[1] = (__int64)v46;
LABEL_58:
      if ( v45 == ++v47 )
        return result;
    }
    v49 = (__int64)v46 - *v4;
    v50 = v49 >> 3;
    v51 = (v49 >> 3) + 1;
    v52 = (unsigned __int64)(v49 >> 3) >> 1;
    v53 = 0x1FFFFFFFFFFFFFFFLL;
    v54 = 0x1FFFFFFFFFFFFFFFLL - v52;
    v55 = (v49 >> 3) + v52;
    if ( v55 <= v51 )
      v55 = v50 + 1;
    if ( v50 <= v54 )
      v53 = v55;
    v56 = sub_1407E4490(qword_141ABD470, 8 * v53);
    *(_QWORD *)(v56 + v49) = v48;
    v57 = (_QWORD *)a2[1];
    sub_141758A00();
    if ( v57 != v46 )
      sub_141758A00();
    v58 = *a2;
    v4 = a2;
    if ( *a2 == 0 )
    {
LABEL_77:
      *v4 = v56;
      v46 = (_QWORD *)(v56 + 8 * v51);
      v4[1] = (__int64)v46;
      result = v56 + 8 * v53;
      v4[2] = result;
      v5 = v125;
      v45 = v128;
      goto LABEL_58;
    }
    v59 = a2[2] - v58;
    if ( v59 == -1 )
    {
      v59 = *(unsigned int *)(v58 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_75;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_75;
    }
    v60 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v60) >> 3 > v59 )
    {
      v61 = *(_QWORD *)(v60 + 8 * v59);
      if ( v61 != 0 )
      {
        MEMORY[0x1419475D8](v61 + 32, v58 - *(unsigned int *)(v61 + 120));
        v62 = *(_BYTE *)(v61 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v61 + 64)) != 0;
        v4 = a2;
        if ( v62 || *(_BYTE *)(v61 + 97) == 0 )
          goto LABEL_77;
        sub_1412D33C0(v61);
        goto LABEL_76;
      }
    }
LABEL_75:
    MEMORY[0x141948990](v58 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_76:
    v4 = a2;
    goto LABEL_77;
  }
  return result;
}
