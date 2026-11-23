__int64 __fastcall sub_14130CC70(unsigned __int64 *a1, volatile signed __int32 **a2, int a3, unsigned int a4)
{
  volatile signed __int32 *v5; // rdi
  void (__fastcall *v6)(volatile signed __int32 *, __int128 *, unsigned __int64 *, __int64 *); // rax
  int v7; // r9d
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  unsigned __int64 v9; // rcx
  int v10; // r9d
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  __int64 v12; // rcx
  volatile signed __int32 *v13; // rcx
  void (__fastcall *v14)(volatile signed __int32 *, __int128 *); // rax
  void (__fastcall ***v15)(_QWORD, __int64); // rcx
  void (__fastcall ***v16)(_QWORD, __int64); // rax
  __int64 v17; // rax
  volatile signed __int32 *v18; // rcx
  _QWORD *v19; // rsi
  __int64 v20; // rsi
  void (__fastcall ***v21)(_QWORD, __int64); // rcx
  unsigned int v22; // r12d
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 *v25; // r14
  volatile signed __int32 *v26; // rcx
  void (__fastcall ***v27)(_QWORD, __int64); // rcx
  __int64 v29; // rcx
  unsigned int v30; // r14d
  unsigned int *v31; // rbx
  int *v32; // rdi
  __int64 v33; // rsi
  __int64 v34; // rsi
  __int64 v35; // rsi
  __int64 v36; // rdx
  BOOL v37; // r15d
  __int64 *v38; // r12
  __int64 v39; // rax
  unsigned int *v40; // r8
  int *v41; // rbx
  unsigned int v42; // edi
  __int64 *v43; // rdx
  int v44; // r13d
  __int64 v45; // rax
  __int64 v46; // r15
  __int64 *v47; // rcx
  unsigned int v48; // edx
  __int64 *v49; // rsi
  __int64 *v50; // rax
  __int64 *v51; // rbx
  __int64 *v52; // rdx
  __int64 *v53; // rax
  __int64 *v54; // rdx
  __int64 v55; // rax
  unsigned __int64 v56; // rdx
  __int64 v57; // r8
  __int64 v58; // rbx
  char *v59; // rdi
  char *v60; // r12
  int **v61; // r15
  __int64 v62; // rdx
  int *v63; // rax
  int v64; // ecx
  int v65; // esi
  __int64 v66; // rcx
  unsigned __int64 v67; // rcx
  bool v68; // si
  unsigned __int64 *v69; // rdi
  bool v70; // di
  __int64 *v71; // rdx
  __int64 *v72; // rax
  __int64 *v73; // rdi
  unsigned int v74; // ecx
  __int64 *v75; // r15
  __int64 v76; // rdx
  int v77; // r12d
  __int64 v78; // rdi
  __int64 v79; // rax
  bool v80; // dl
  bool v81; // cl
  __int64 *v82; // rdx
  bool v83; // dl
  __int64 v84; // rsi
  __int64 v85; // rbx
  __int64 *v86; // rcx
  __int64 v87; // rcx
  _QWORD *v88; // rcx
  __int64 v89; // rbx
  volatile signed __int32 *v90; // rcx
  __int64 v91; // rbx
  __int64 v92; // rsi
  __int64 *v93; // rcx
  __int64 *v94; // rax
  __int64 *v95; // rcx
  _BYTE *v96; // rsi
  _QWORD *v97; // rdx
  _QWORD *v98; // r8
  _QWORD *v99; // rdi
  _QWORD *v100; // rbx
  _QWORD *v101; // rbx
  __int64 v102; // rbx
  _QWORD *v103; // rbx
  _QWORD *v104; // rdi
  _QWORD *v105; // rbx
  _QWORD *v106; // rdx
  _QWORD *v107; // rbx
  _QWORD *v108; // rsi
  _QWORD *v109; // rdi
  __int64 v110; // rdi
  _QWORD *v111; // rdi
  __int64 v112; // rsi
  volatile signed __int32 **v113; // rsi
  volatile signed __int32 **v114; // rbx
  __int64 v115; // rsi
  unsigned int v116; // [rsp+48h] [rbp-38h]
  __int64 **v117; // [rsp+50h] [rbp-30h]
  int v118; // [rsp+5Ch] [rbp-24h] BYREF
  unsigned int v119; // [rsp+60h] [rbp-20h]
  unsigned int v120; // [rsp+64h] [rbp-1Ch]
  volatile signed __int32 *v121; // [rsp+68h] [rbp-18h]
  int v122; // [rsp+74h] [rbp-Ch] BYREF
  unsigned __int64 *v123; // [rsp+78h] [rbp-8h]
  __int128 v124; // [rsp+80h] [rbp+0h] BYREF
  __int64 v125; // [rsp+90h] [rbp+10h]
  __int64 v126; // [rsp+98h] [rbp+18h]
  __int128 v127; // [rsp+A0h] [rbp+20h] BYREF
  volatile signed __int32 *v128; // [rsp+B0h] [rbp+30h] BYREF
  unsigned int v129; // [rsp+BCh] [rbp+3Ch] BYREF
  __int128 v130; // [rsp+C0h] [rbp+40h] BYREF
  unsigned int v131; // [rsp+D0h] [rbp+50h] BYREF
  volatile signed __int32 *v132; // [rsp+D8h] [rbp+58h]
  _QWORD v133[2]; // [rsp+E0h] [rbp+60h] BYREF

  v133[1] = -2;
  v123 = a1;
  v118 = a3;
  v5 = *a2;
  if ( *a2 != nullptr )
    _InterlockedIncrement(v5 + 2);
  v120 = a4;
  if ( a4 == 0 )
  {
    v13 = *a2;
    if ( *a2 != nullptr )
    {
      v14 = *(void (__fastcall **)(volatile signed __int32 *, __int128 *))(*(_QWORD *)v13 + 16LL);
      v121 = v5;
      v14(a1: v13, a2: &v127);
      v132 = v5;
      (*(void (__fastcall **)(volatile signed __int32 *, __int128 *))(*(_QWORD *)*a2 + 120LL))(a1: *a2, a2: &v124);
      if ( (_QWORD)v124 != 0 )
      {
        (*(void (__fastcall **)(_QWORD, __int128 *, __int128 *, __int64 *))(*(_QWORD *)v124 + 224LL))(
          a1: v124,
          a2: &v130,
          a3: &v127,
          a4: &qword_141B59858);
        v5 = v132;
        if ( v132 == (volatile signed __int32 *)v130 )
        {
          if ( v132 != nullptr )
          {
            if ( _InterlockedDecrement(v132 + 2) == 0 )
              (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v5)(a1: v5, a2: 1);
          }
          else
          {
            v5 = nullptr;
          }
        }
        else
        {
          if ( v132 != nullptr && _InterlockedDecrement(v132 + 2) == 0 )
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v5)(a1: v5, a2: 1);
          v5 = (volatile signed __int32 *)v130;
        }
        v15 = (void (__fastcall ***)(_QWORD, __int64))v124;
        if ( (_QWORD)v124 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v124 + 8)) == 0 )
          (**v15)(a1: v15, a2: 1);
      }
      else
      {
        v5 = v132;
      }
      v29 = v127;
      if ( (_QWORD)v127 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v127 - 4)) == 0 )
        sub_1412EC9A0(a1: v29 - 4);
    }
  }
  *(_QWORD *)&v124 = 0x80100004E554C4CLL;
  v132 = v5;
  if ( v5 != nullptr
    && (v6 = *(void (__fastcall **)(volatile signed __int32 *, __int128 *, unsigned __int64 *, __int64 *))(*(_QWORD *)v5 + 224LL),
        v121 = v5,
        v6(a1: v5, a2: &v127, a3: v123 + 15, a4: &qword_141B65EC0),
        (_QWORD)v127 != 0) )
  {
    LOWORD(v7) = 16;
    sub_1407D1280(a1: (unsigned int)&v124, a2: (unsigned int)v133, a3: (unsigned int)&v127, a4: v7, a5: 0);
    v8 = (void (__fastcall ***)(_QWORD, __int64))v127;
    if ( (_QWORD)v127 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v127 + 8)) == 0 )
      (**v8)(a1: v8, a2: 1);
    v5 = v132;
    if ( v133[0] != 0 )
      goto LABEL_34;
  }
  else
  {
    v133[0] = 0;
  }
  v9 = v123[14];
  if ( v9 == 0 )
    goto LABEL_59;
  *(_QWORD *)&v124 = 0x80100004E554C4CLL;
  (*(void (__fastcall **)(unsigned __int64, __int128 *, unsigned __int64 *, __int64 *))(*(_QWORD *)v9 + 224LL))(
    a1: v9,
    a2: &v127,
    a3: v123 + 15,
    a4: &qword_141B65EC0);
  if ( (_QWORD)v127 != 0 )
  {
    LOWORD(v10) = 16;
    sub_1407D1280(a1: (unsigned int)&v124, a2: (unsigned int)&v130, a3: (unsigned int)&v127, a4: v10, a5: 0);
    v11 = (void (__fastcall ***)(_QWORD, __int64))v127;
    if ( (_QWORD)v127 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v127 + 8)) == 0 )
      (**v11)(a1: v11, a2: 1);
    v12 = v130;
  }
  else
  {
    *(_QWORD *)&v130 = 0;
    v12 = 0;
  }
  v5 = v132;
  v16 = (void (__fastcall ***)(_QWORD, __int64))v133[0];
  if ( v133[0] == v12 )
  {
    if ( v133[0] != 0 )
    {
      if ( _InterlockedDecrement((volatile signed __int32 *)(v12 + 8)) == 0 )
        (**(void (__fastcall ***)(__int64, __int64))v12)(a1: v12, a2: 1);
      if ( v133[0] != 0 )
        goto LABEL_34;
LABEL_56:
      LODWORD(v25) = 0;
      goto LABEL_57;
    }
LABEL_59:
    LODWORD(v25) = 0;
    if ( v5 == nullptr )
      return (unsigned int)v25;
    goto LABEL_60;
  }
  if ( v133[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v133[0] + 8LL)) == 0 )
    (**v16)(a1: v16, a2: 1);
  v133[0] = v130;
  if ( (_QWORD)v130 == 0 )
    goto LABEL_56;
LABEL_34:
  v127 = 0;
  v17 = sub_141750CC0(a1: 40);
  *(_QWORD *)v17 = v17;
  *(_QWORD *)(v17 + 8) = v17;
  *(_QWORD *)(v17 + 16) = v17;
  *(_WORD *)(v17 + 24) = 257;
  *(_QWORD *)&v127 = v17;
  v18 = *a2;
  v128 = v18;
  v19 = (_QWORD *)v17;
  if ( v18 != nullptr )
  {
    _InterlockedIncrement(v18 + 2);
    v19 = (_QWORD *)v127;
    v17 = *(_QWORD *)(v127 + 8);
  }
  sub_1400D93A0(a1: &v127, a2: &v127, a3: v17);
  v19[1] = v19;
  *v19 = v19;
  v19[2] = v19;
  *((_QWORD *)&v127 + 1) = 0;
  if ( v128 != nullptr )
  {
    *(_QWORD *)&v124 = 0x80100004E554C4CLL;
    sub_1407D0F70(
      a1: (unsigned int)&v124,
      a2: (unsigned int)&v130,
      a3: (unsigned int)&v128,
      a4: (unsigned int)&qword_141B62BB0,
      a5: (__int64)&unk_141B62BA8,
      a6: 4,
      a7: 0,
      0);
    v20 = v130;
    if ( (_QWORD)v130 != 0 )
    {
      (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)v130 + 40LL))(a1: v130, a2: &v129, a3: 4);
      if ( *(_DWORD *)(v20 + 16) == 0 )
      {
        v30 = 0;
        v31 = &v131;
        v32 = &v122;
        while ( v30 < v129 )
        {
          v33 = v130;
          (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)v130 + 40LL))(a1: v130, a2: v31, a3: 4);
          if ( *(_DWORD *)(v33 + 16) != 0 )
            break;
          v34 = v130;
          (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v130 + 40LL))(a1: v130, a2: v32, a3: 4);
          if ( *(_DWORD *)(v34 + 16) != 0 )
            break;
          v35 = v127;
          v36 = *(_QWORD *)(v127 + 8);
          v37 = false;
          if ( *(_BYTE *)(v36 + 25) != 0 )
          {
            v38 = *(__int64 **)(v127 + 8);
            v39 = v127;
          }
          else
          {
            v40 = v31;
            v41 = v32;
            v39 = v127;
            do
            {
              v38 = (__int64 *)v36;
              v42 = *(_DWORD *)(v36 + 28);
              v43 = (__int64 *)(v36 + 16);
              if ( v42 >= v131 )
              {
                v39 = (__int64)v38;
                v43 = v38;
              }
              v36 = *v43;
            }
            while ( *(_BYTE *)(v36 + 25) == 0 );
            v37 = v42 >= v131;
            v32 = v41;
            v31 = v40;
          }
          v44 = v122;
          if ( *(_BYTE *)(v39 + 25) != 0 || v131 < *(_DWORD *)(v39 + 28) )
          {
            if ( *((_QWORD *)&v127 + 1) == 0x666666666666666LL )
              sub_140052D20();
            v45 = sub_141750CC0(a1: 40);
            *(_DWORD *)(v45 + 28) = v131;
            *(_DWORD *)(v45 + 32) = 0;
            *(_QWORD *)v45 = v35;
            *(_QWORD *)(v45 + 8) = v35;
            *(_QWORD *)(v45 + 16) = v35;
            *(_WORD *)(v45 + 24) = 0;
            *(_QWORD *)&v124 = v38;
            DWORD2(v124) = v37;
            v39 = sub_1407FAE70(a1: &v127, a2: &v124, a3: v45);
          }
          *(_DWORD *)(v39 + 32) = v44;
          ++v30;
        }
      }
      v21 = (void (__fastcall ***)(_QWORD, __int64))v130;
      if ( (_QWORD)v130 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v130 + 8)) == 0 )
        (**v21)(a1: v21, a2: 1);
    }
  }
  v22 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v133[0] + 16LL))(a1: v133[0]);
  v129 = 0;
  v23 = v133[0];
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)v133[0] + 40LL))(a1: v133[0], a2: &v129, a3: 4);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    goto LABEL_44;
  v24 = v133[0];
  (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v133[0] + 40LL))(a1: v133[0], a2: &v118, a3: 4);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    goto LABEL_44;
  sub_1408149D0(a1: v133[0], a2: &v124, a3: v123 + 10);
  LODWORD(v25) = 0;
  v5 = v132;
  if ( (_DWORD)v124 != 0 )
    goto LABEL_45;
  v46 = v133[0];
  v47 = *(__int64 **)v127;
  if ( *(_QWORD *)v127 != (_QWORD)v127 && *((_QWORD *)&v127 + 1) != 0 )
  {
    LODWORD(v25) = 0;
    do
    {
      v48 = *((_DWORD *)v47 + 7);
      if ( v48 != -1 )
      {
        v49 = *(__int64 **)(v127 + 8);
        v50 = (__int64 *)v127;
        if ( *((_BYTE *)v49 + 25) == 0 )
        {
          v50 = (__int64 *)v127;
          do
          {
            v51 = v49 + 2;
            if ( *((_DWORD *)v49 + 7) >= v48 )
            {
              v50 = v49;
              v51 = v49;
            }
            v49 = (__int64 *)*v51;
          }
          while ( *(_BYTE *)(*v51 + 25) == 0 );
        }
        if ( *((_BYTE *)v50 + 25) == 0 && *((_DWORD *)v50 + 7) <= v48 && v50 != (__int64 *)v127 )
          LODWORD(v25) = (*((_DWORD *)v50 + 8) < 0x3E9u) + (_DWORD)v25;
      }
      v52 = (__int64 *)v47[2];
      if ( *((_BYTE *)v52 + 25) != 0 )
      {
        do
        {
          v53 = (__int64 *)v47[1];
          if ( *((_BYTE *)v53 + 25) != 0 )
            break;
          v54 = v47;
          v47 = (__int64 *)v47[1];
        }
        while ( v54 == (__int64 *)v53[2] );
      }
      else
      {
        do
        {
          v53 = v52;
          v52 = (__int64 *)*v52;
        }
        while ( *((_BYTE *)v52 + 25) == 0 );
      }
      v47 = v53;
    }
    while ( v53 != (__int64 *)v127 );
  }
  LODWORD(v124) = (_DWORD)v25;
  (*(void (__fastcall **)(_QWORD, __int128 *, __int64))(*(_QWORD *)v133[0] + 40LL))(a1: v133[0], a2: &v124, a3: 4);
  if ( *(_DWORD *)(v46 + 16) != 0 )
  {
LABEL_44:
    LODWORD(v25) = 0;
    v5 = v132;
  }
  else
  {
    v130 = 0;
    v55 = sub_141750CC0(a1: 40);
    *(_QWORD *)v55 = v55;
    *(_QWORD *)(v55 + 8) = v55;
    *(_QWORD *)(v55 + 16) = v55;
    *(_WORD *)(v55 + 24) = 257;
    *(_QWORD *)&v130 = v55;
    v124 = 0;
    v125 = 0;
    v56 = (unsigned __int64)&v123[2 * v120];
    v117 = (__int64 **)v56;
    v25 = **(__int64 ***)v56;
    v57 = 0xFFFFFFFFLL;
    v116 = v22;
    if ( v25 != *(__int64 **)v56 )
    {
      while ( 1 )
      {
        v58 = v25[4];
        v56 = (unsigned int)v58;
        if ( (_DWORD)v57 != (_DWORD)v58 )
          goto LABEL_138;
        LODWORD(v126) = v57;
        v59 = (char *)v25[5];
        v60 = (char *)v25[6];
        v61 = (int **)v124;
        if ( v60 - v59 != *((_QWORD *)&v124 + 1) - (_QWORD)v124 )
          break;
        for ( ; v59 != v60; ++v61 )
        {
          v62 = (__int64)(*v61 + 1);
          if ( *v61 != nullptr )
          {
            v64 = **v61;
            v63 = *(int **)v59;
            if ( v64 == -1 )
              goto LABEL_119;
          }
          else
          {
            v62 = 0x1419435F1LL;
            v63 = *(int **)v59;
            v64 = 0;
          }
          if ( v63 != nullptr )
            v65 = *v63;
          else
            v65 = 0;
          if ( v65 != v64 )
            goto LABEL_137;
LABEL_119:
          v66 = (__int64)(v63 + 1);
          if ( v63 == nullptr )
            v66 = 0x1419435F1LL;
          if ( (unsigned int)sub_141758D90(a1: v66, a2: v62) != 0 )
            goto LABEL_137;
          v59 += 8;
        }
        if ( v120 == 1 )
        {
          v56 = *(_QWORD *)(*v123 + 8);
          v67 = *v123;
          v57 = (unsigned int)v126;
          if ( *(_BYTE *)(v56 + 25) == 0 )
          {
            v67 = *v123;
            do
            {
              v68 = *(_DWORD *)(v56 + 32) < (unsigned int)v126;
              if ( *(_DWORD *)(v56 + 32) == (_DWORD)v126 )
                v68 = *(_DWORD *)(v56 + 36) < SHIDWORD(v58);
              v69 = (unsigned __int64 *)(v56 + 16);
              if ( !v68 )
              {
                v67 = v56;
                v69 = (unsigned __int64 *)v56;
              }
              v56 = *v69;
            }
            while ( *(_BYTE *)(*v69 + 25) == 0 );
          }
          if ( *(_BYTE *)(v67 + 25) == 0 )
          {
            v56 = *(_DWORD *)(v67 + 36) > SHIDWORD(v58);
            v70 = *(_DWORD *)(v67 + 32) > (unsigned int)v126;
            if ( *(_DWORD *)(v67 + 32) == (_DWORD)v126 )
              v70 = *(_DWORD *)(v67 + 36) > SHIDWORD(v58);
            if ( !v70 )
            {
              v56 = (unsigned int)v126;
              if ( v67 != *v123 )
                goto LABEL_138;
            }
          }
        }
        else
        {
          v57 = (unsigned int)v126;
        }
LABEL_184:
        v93 = (__int64 *)v25[2];
        v22 = v116;
        if ( *((_BYTE *)v93 + 25) != 0 )
        {
          do
          {
            v94 = (__int64 *)v25[1];
            if ( *((_BYTE *)v94 + 25) != 0 )
              break;
            v95 = v25;
            v25 = (__int64 *)v25[1];
          }
          while ( v95 == (__int64 *)v94[2] );
        }
        else
        {
          do
          {
            v94 = v93;
            v93 = (__int64 *)*v93;
          }
          while ( *((_BYTE *)v93 + 25) == 0 );
        }
        v25 = v94;
        if ( v94 == *v117 )
          goto LABEL_236;
      }
LABEL_137:
      LODWORD(v56) = v126;
LABEL_138:
      v119 = v56;
      if ( &v124 != (__int128 *)(v25 + 5) )
        sub_141310EF0(a1: &v124, a2: v25[5], a3: (v25[6] - v25[5]) >> 3);
      v126 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v133[0] + 16LL))(a1: v133[0]);
      if ( (_DWORD)v58 != -1 && *((_QWORD *)&v127 + 1) != 0 )
      {
        v71 = *(__int64 **)(v127 + 8);
        v72 = (__int64 *)v127;
        if ( *((_BYTE *)v71 + 25) == 0 )
        {
          v72 = (__int64 *)v127;
          do
          {
            v73 = v71 + 2;
            if ( *((_DWORD *)v71 + 7) >= (unsigned int)v58 )
            {
              v72 = v71;
              v73 = v71;
            }
            v71 = (__int64 *)*v73;
          }
          while ( *(_BYTE *)(*v73 + 25) == 0 );
        }
        if ( *((_BYTE *)v72 + 25) == 0 && *((_DWORD *)v72 + 7) <= (unsigned int)v58 && v72 != (__int64 *)v127 )
        {
          v74 = v126 | 0x80000000;
          if ( *((_DWORD *)v72 + 8) >= 0x3E9u )
            v74 = v126;
          v126 = v74;
        }
      }
      v75 = (__int64 *)v130;
      v76 = *(_QWORD *)(v130 + 8);
      v77 = 0;
      if ( *(_BYTE *)(v76 + 25) != 0 )
      {
        v78 = *(_QWORD *)(v130 + 8);
        v79 = v130;
      }
      else
      {
        v79 = v130;
        do
        {
          v78 = v76;
          v80 = *(_DWORD *)(v76 + 32) < SHIDWORD(v58);
          v81 = *(_DWORD *)(v78 + 28) < (unsigned int)v58;
          if ( *(_DWORD *)(v78 + 28) == (_DWORD)v58 )
            v81 = v80;
          v82 = (__int64 *)(v78 + 16);
          if ( !v81 )
          {
            v79 = v78;
            v82 = (__int64 *)v78;
          }
          v76 = *v82;
        }
        while ( *(_BYTE *)(v76 + 25) == 0 );
        v77 = !v81;
      }
      if ( *(_BYTE *)(v79 + 25) == 0 )
      {
        v83 = *(_DWORD *)(v79 + 28) <= (unsigned int)v58;
        if ( *(_DWORD *)(v79 + 28) == (_DWORD)v58 )
          v83 = *(_DWORD *)(v79 + 32) <= SHIDWORD(v58);
        if ( v83 )
        {
LABEL_178:
          *(_DWORD *)(v79 + 36) = v126;
          LOBYTE(v122) = (unsigned int)(*((_DWORD *)v25 + 12) - *((_DWORD *)v25 + 10)) >> 3;
          v89 = v133[0];
          (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)v133[0] + 40LL))(a1: v133[0], a2: &v122, a3: 1);
          if ( *(_DWORD *)(v89 + 16) != 0 )
            goto LABEL_242;
          v91 = v25[5];
          v92 = v25[6];
          while ( v91 != v92 )
          {
            sub_1408149D0(a1: v133[0], a2: &v131, a3: v91);
            v91 += 8;
            if ( v131 != 0 )
              goto LABEL_242;
          }
          v57 = v119;
          goto LABEL_184;
        }
      }
      v84 = *((_QWORD *)&v130 + 1);
      if ( *((_QWORD *)&v130 + 1) == 0x666666666666666LL )
        sub_140052D20();
      v79 = sub_141750CC0(a1: 40);
      *(_QWORD *)(v79 + 28) = v58;
      *(_DWORD *)(v79 + 36) = 0;
      *(_QWORD *)v79 = v75;
      *(_QWORD *)(v79 + 16) = v75;
      *(_WORD *)(v79 + 24) = 0;
      *((_QWORD *)&v130 + 1) = v84 + 1;
      *(_QWORD *)(v79 + 8) = v78;
      if ( (__int64 *)v78 == v75 )
      {
        *v75 = v79;
        v75[1] = v79;
        v75[2] = v79;
        v87 = v79;
LABEL_177:
        *(_BYTE *)(v87 + 24) = 1;
        goto LABEL_178;
      }
      v85 = v79 + 8;
      if ( v77 != 0 )
      {
        *(_QWORD *)v78 = v79;
        v86 = v75;
        if ( v78 == *v75 )
          goto LABEL_174;
      }
      else
      {
        *(_QWORD *)(v78 + 16) = v79;
        if ( v78 == v75[2] )
        {
          v86 = v75 + 2;
LABEL_174:
          *v86 = v79;
        }
      }
      v88 = *(_QWORD **)v85;
      if ( *(_BYTE *)(*(_QWORD *)v85 + 24LL) != 0 )
      {
LABEL_176:
        v87 = v75[1];
        goto LABEL_177;
      }
      v96 = v88 + 3;
      v97 = (_QWORD *)v79;
      while ( 1 )
      {
        v98 = (_QWORD *)v88[1];
        v99 = (_QWORD *)*v98;
        if ( v88 == (_QWORD *)*v98 )
        {
          v99 = (_QWORD *)v98[2];
          if ( *((_BYTE *)v99 + 24) != 0 )
          {
            if ( v97 == (_QWORD *)v88[2] )
            {
              v88[2] = *v97;
              if ( *(_BYTE *)(*v97 + 25LL) == 0 )
              {
                *(_QWORD *)(*v97 + 8LL) = v88;
                v98 = (_QWORD *)v88[1];
              }
              v97[1] = v98;
              if ( *(_QWORD **)(v130 + 8) == v88 )
              {
                v105 = (_QWORD *)(v130 + 8);
              }
              else
              {
                v104 = (_QWORD *)v88[1];
                v105 = v104 + 2;
                if ( (_QWORD *)*v104 == v88 )
                  v105 = (_QWORD *)v88[1];
              }
              *v105 = v97;
              *v97 = v88;
              v88[1] = v97;
              v101 = v97;
            }
            else
            {
              v101 = v88;
              v88 = v97;
            }
            *((_BYTE *)v101 + 24) = 1;
            *(_BYTE *)(*(_QWORD *)(v88[1] + 8LL) + 24LL) = 0;
            v106 = *(_QWORD **)(v88[1] + 8LL);
            v107 = (_QWORD *)*v106;
            *v106 = *(_QWORD *)(*v106 + 16LL);
            v110 = v107[2];
            if ( *(_BYTE *)(v110 + 25) == 0 )
              *(_QWORD *)(v110 + 8) = v106;
            v107[1] = v106[1];
            if ( *(_QWORD **)(v130 + 8) == v106 )
            {
              v111 = (_QWORD *)(v130 + 8);
            }
            else
            {
              v111 = (_QWORD *)(v106[1] + 16LL);
              if ( (_QWORD *)*v111 != v106 )
                v111 = (_QWORD *)v106[1];
            }
            *v111 = v107;
            v107[2] = v106;
            goto LABEL_233;
          }
        }
        else if ( *((_BYTE *)v99 + 24) != 0 )
        {
          if ( v97 == (_QWORD *)*v88 )
          {
            *v88 = v97[2];
            v102 = v97[2];
            if ( *(_BYTE *)(v102 + 25) == 0 )
            {
              *(_QWORD *)(v102 + 8) = v88;
              v98 = (_QWORD *)v88[1];
            }
            v97[1] = v98;
            if ( *(_QWORD **)(v130 + 8) == v88 )
            {
              v103 = (_QWORD *)(v130 + 8);
            }
            else
            {
              v103 = (_QWORD *)(v88[1] + 16LL);
              if ( (_QWORD *)*v103 != v88 )
                v103 = (_QWORD *)v88[1];
            }
            *v103 = v97;
            v97[2] = v88;
            v88[1] = v97;
            v100 = v97;
          }
          else
          {
            v100 = v88;
            v88 = v97;
          }
          *((_BYTE *)v100 + 24) = 1;
          *(_BYTE *)(*(_QWORD *)(v88[1] + 8LL) + 24LL) = 0;
          v106 = *(_QWORD **)(v88[1] + 8LL);
          v107 = (_QWORD *)v106[2];
          v106[2] = *v107;
          if ( *(_BYTE *)(*v107 + 25LL) == 0 )
            *(_QWORD *)(*v107 + 8LL) = v106;
          v107[1] = v106[1];
          if ( *(_QWORD **)(v130 + 8) == v106 )
          {
            v109 = (_QWORD *)(v130 + 8);
          }
          else
          {
            v108 = (_QWORD *)v106[1];
            v109 = v108 + 2;
            if ( (_QWORD *)*v108 == v106 )
              v109 = (_QWORD *)v106[1];
          }
          *v109 = v107;
          *v107 = v106;
LABEL_233:
          v106[1] = v107;
          goto LABEL_193;
        }
        *v96 = 1;
        *((_BYTE *)v99 + 24) = 1;
        *(_BYTE *)(*(_QWORD *)(*(_QWORD *)v85 + 8LL) + 24LL) = 0;
        v88 = *(_QWORD **)(*(_QWORD *)v85 + 8LL);
LABEL_193:
        v97 = v88;
        v85 = (__int64)(v88 + 1);
        v88 = (_QWORD *)v88[1];
        v96 = v88 + 3;
        if ( *((_BYTE *)v88 + 24) != 0 )
          goto LABEL_176;
      }
    }
LABEL_236:
    v90 = (volatile signed __int32 *)v133[0];
    LOBYTE(v25) = 1;
    if ( *(_DWORD *)(v133[0] + 16LL) == 0 )
    {
      v129 = (*(__int64 (__fastcall **)(_QWORD, unsigned __int64, __int64))(*(_QWORD *)v133[0] + 16LL))(
               a1: v133[0],
               a2: v56,
               a3: v57);
      if ( (unsigned __int8)sub_14130E710(a1: &v130, a2: v133) != 0
        && (unsigned __int8)sub_14130E830(a1: v123 + 4, a2: v133) != 0
        && (unsigned __int8)sub_14130E830(a1: v123 + 7, a2: v133) != 0
        && ((*(void (__fastcall **)(_QWORD, unsigned int *, _QWORD))(*(_QWORD *)v133[0] + 24LL))(
              a1: v133[0],
              a2: &v131,
              a3: v22),
            v131 == 0)
        && (v112 = v133[0],
            (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)v133[0] + 40LL))(
              a1: v133[0],
              a2: &v129,
              a3: 4),
            *(_DWORD *)(v112 + 16) == 0) )
      {
        v90 = (volatile signed __int32 *)v133[0];
        if ( v133[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v133[0] + 8LL)) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v90)(a1: v90, a2: 1);
        v133[0] = 0;
      }
      else
      {
LABEL_242:
        LODWORD(v25) = 0;
      }
    }
    v5 = v132;
    v113 = (volatile signed __int32 **)v124;
    if ( (_QWORD)v124 != 0 )
    {
      v114 = *((volatile signed __int32 ***)&v124 + 1);
      if ( (_QWORD)v124 != *((_QWORD *)&v124 + 1) )
      {
        do
        {
          v90 = *v113;
          if ( *v113 != nullptr && _InterlockedDecrement(v90 - 1) == 0 )
            sub_1412EC9A0(a1: v90 - 1);
          ++v113;
        }
        while ( v113 != v114 );
        v113 = (volatile signed __int32 **)v124;
      }
      if ( (unsigned __int64)(v125 - (_QWORD)v113) >= 0x1000 )
      {
        if ( (unsigned __int64)((char *)(v113 - 1) - (char *)*(v113 - 1)) >= 0x20 )
        {
          MEMORY[0x1419488E8](a1: v90, a2: v125 - (_QWORD)v113, a3: v57);
          __debugbreak();
        }
        v113 = (volatile signed __int32 **)*(v113 - 1);
      }
      sub_141750D04(a1: v113);
    }
    v115 = v130;
    sub_1407E2B40(a1: *(_QWORD *)(v130 + 8), a2: v56, a3: v57);
    sub_141750D04(a1: v115);
  }
LABEL_45:
  v26 = v128;
  if ( v128 != nullptr && _InterlockedDecrement(v128 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v26)(a1: v26, a2: 1);
  sub_1400D93A0(a1: &v127, a2: &v127, a3: *(_QWORD *)(v127 + 8));
  sub_141750D04(a1: v127);
  v27 = (void (__fastcall ***)(_QWORD, __int64))v133[0];
  if ( v133[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v133[0] + 8LL)) == 0 )
  {
    (**v27)(a1: v27, a2: 1);
    if ( v5 == nullptr )
      return (unsigned int)v25;
    goto LABEL_60;
  }
LABEL_57:
  if ( v5 == nullptr )
    return (unsigned int)v25;
LABEL_60:
  if ( _InterlockedDecrement(v5 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v5)(a1: v5, a2: 1);
  return (unsigned int)v25;
}
