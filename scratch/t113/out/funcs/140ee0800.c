unsigned __int8 __fastcall sub_140EE0800(
        _DWORD *a1,
        __int64 a2,
        char a3,
        char a4,
        unsigned __int8 a5,
        unsigned __int8 a6,
        int a7,
        char a8)
{
  __int64 v8; // rbp
  __int64 v13; // rax
  __int64 v14; // r14
  __int64 v15; // rcx
  __int64 v16; // rax
  __int64 v17; // rdx
  __int64 (**v18)(void); // rdx
  __int64 v19; // rax
  __int64 v20; // rdx
  __int64 v21; // rax
  _QWORD *v22; // rcx
  __int64 v23; // rax
  __int64 v24; // rdi
  __int64 v25; // rax
  __int64 v26; // rcx
  __int64 v27; // r13
  __int64 v28; // rcx
  __int64 v29; // rax
  int v30; // ecx
  char v31; // bl
  char v32; // al
  __int64 v33; // rax
  char v34; // al
  __int64 v35; // rbp
  __int64 v36; // r13
  unsigned int v37; // eax
  unsigned __int8 *v38; // rbp
  __int64 v39; // rdx
  __int64 v40; // rbp
  unsigned __int8 v41; // al
  __int64 v42; // rcx
  unsigned int v43; // eax
  unsigned __int16 v44; // bp
  __int64 v45; // rcx
  unsigned int v46; // ebp
  __int64 v47; // rdi
  __int64 v48; // rax
  __int64 v49; // r14
  __int64 v50; // rbx
  int v51; // r12d
  __int64 v52; // rax
  int v53; // eax
  int v54; // eax
  unsigned int v55; // eax
  int v56; // ecx
  __int64 v57; // rax
  char v58; // bl
  __int64 v59; // rax
  __int64 v60; // r13
  __int64 v61; // rax
  _QWORD *v62; // rbp
  _QWORD *v63; // rdi
  char v64; // al
  int v65; // eax
  bool v66; // bl
  int v67; // r12d
  char v68; // di
  int v69; // r9d
  int v70; // eax
  __int64 *v71; // rax
  bool v72; // bp
  __int64 v73; // rax
  int v74; // eax
  __int64 v75; // rax
  __int64 v76; // rcx
  char v77; // bl
  char v78; // r14
  __int64 v79; // rcx
  __int64 v80; // r8
  __int64 v81; // rcx
  __int64 v82; // rax
  __int64 v83; // rcx
  char v84; // bl
  char v85; // al
  __int64 v86; // rbp
  __int64 v87; // rax
  __int64 v88; // rax
  char v89; // bl
  __int64 v90; // rax
  __int64 v91; // r8
  int v92; // edx
  int v93; // eax
  unsigned int v94; // ecx
  int v95; // eax
  __int64 v96; // rcx
  __int64 v97; // rcx
  __int64 v98; // rax
  __int64 v99; // r8
  int v100; // edx
  __int64 v101; // rax
  __int64 v102; // rax
  __int64 *v103; // rcx
  __int64 v104; // rbx
  __int64 v105; // rbp
  __int64 v106; // rdi
  int v107; // eax
  unsigned int v108; // ecx
  unsigned int v109; // eax
  __int64 v110; // rbx
  int v111; // edi
  int v112; // r13d
  __int64 v113; // rbp
  __int64 v114; // rdx
  __int64 v115; // r8
  int v116; // eax
  char v117; // al
  int v118; // r8d
  int v119; // r9d
  int v120; // ebx
  __int64 v121; // rcx
  unsigned __int16 v122; // ax
  int *v123; // rdx
  __int64 v124; // rax
  __int16 v125; // ax
  int v126; // ecx
  int v127; // ebp
  int v128; // ebx
  unsigned __int16 v129; // di
  unsigned __int16 v130; // cx
  __int64 v131; // rdi
  int v132; // eax
  __int64 *v133; // rcx
  __int64 v134; // rcx
  int v135; // r14d
  __int64 v136; // rcx
  char v137; // cl
  char v138; // al
  unsigned int v139; // eax
  int v140; // eax
  int v141; // ecx
  unsigned __int16 v142; // bp
  unsigned __int16 v143; // di
  int v144; // edx
  unsigned __int16 v145; // bx
  __int64 v146; // rcx
  char v147; // al
  int v148; // ecx
  unsigned int v149; // ebp
  __int16 v150; // dx
  int v151; // ebx
  __int16 v152; // r8
  __int16 v153; // cx
  unsigned __int16 v154; // dx
  int v155; // ebx
  int v156; // eax
  int v157; // ebx
  int v158; // eax
  int v159; // ebx
  int v160; // eax
  _WORD *v161; // rdx
  unsigned __int16 v162; // cx
  __int64 *v163; // rax
  __int16 v164; // bx
  __int64 v165; // rax
  unsigned __int8 v166; // al
  __int64 v167; // rcx
  __int64 v168; // r8
  unsigned int v169; // edx
  int v170; // eax
  unsigned __int8 v171; // al
  int v172; // ecx
  int v173; // ebp
  unsigned __int8 v174; // bp
  int v175; // edi
  unsigned __int8 v176; // di
  unsigned __int8 v177; // dl
  unsigned __int8 v178; // bl
  __int64 v179; // rdi
  unsigned __int8 v180; // al
  float v181; // xmm0_4
  __int64 v182; // rcx
  __int64 v183; // r12
  unsigned __int8 v184; // al
  char v185; // al
  int v186; // r8d
  float v187; // xmm0_4
  __int64 v188; // rcx
  bool v189; // cc
  __int64 *v190; // rax
  __int64 v191; // r8
  __int64 v192; // rdx
  __int64 v193; // rdx
  __int64 v194; // rcx
  unsigned __int8 v195; // bl
  __int64 v196; // r8
  unsigned __int8 v197; // al
  int v198; // edx
  int v199; // ecx
  unsigned __int8 result; // al
  char v201; // [rsp+86h] [rbp-C2h]
  char v202; // [rsp+86h] [rbp-C2h]
  unsigned __int8 v203; // [rsp+87h] [rbp-C1h]
  unsigned __int8 v204; // [rsp+87h] [rbp-C1h]
  unsigned int v205; // [rsp+88h] [rbp-C0h] BYREF
  __int64 v206; // [rsp+90h] [rbp-B8h]
  __int16 v207; // [rsp+98h] [rbp-B0h] BYREF
  __int16 v208; // [rsp+9Ah] [rbp-AEh]
  __int64 v209; // [rsp+A0h] [rbp-A8h]
  char v210; // [rsp+AFh] [rbp-99h]
  __int64 v211; // [rsp+B0h] [rbp-98h]
  int v212; // [rsp+BCh] [rbp-8Ch]
  __int64 v213; // [rsp+C0h] [rbp-88h]
  __int64 v214; // [rsp+C8h] [rbp-80h]
  __int64 v215; // [rsp+D0h] [rbp-78h]
  __int64 v216; // [rsp+D8h] [rbp-70h]
  __int64 v217; // [rsp+E0h] [rbp-68h]
  __int64 v218; // [rsp+E8h] [rbp-60h]

  *((_BYTE *)a1 + 28) = a5;
  v13 = (*(__int64 (__fastcall **)(_DWORD *, _QWORD))(*(_QWORD *)a1 + 112LL))(a1, a6);
  v14 = *((_QWORD *)a1 + 2);
  v210 = a3;
  if ( v14 == 0 )
  {
    v15 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
    v16 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v15 + 656LL))(v15);
    v17 = *(_QWORD *)(a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8);
    if ( v16 != 0 )
    {
      v18 = (__int64 (**)(void))(v17 + 656);
    }
    else
    {
      v19 = (*(__int64 (**)(void))(v17 + 1080))();
      v20 = *(_QWORD *)(a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8);
      if ( v19 != 0 )
      {
        v18 = (__int64 (**)(void))(v20 + 1080);
      }
      else
      {
        v21 = (*(__int64 (**)(void))(v20 + 1096))();
        v22 = (_QWORD *)(a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8);
        if ( v21 == 0 )
        {
          *((_QWORD *)a1 + 1) = v22;
          goto LABEL_19;
        }
        v18 = (__int64 (**)(void))(*v22 + 1096LL);
      }
    }
    v14 = (*v18)();
    *((_QWORD *)a1 + 1) = *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + a2 + 8;
    if ( v14 != 0 )
    {
      if ( *((_QWORD *)a1 + 2) == 0 )
        *((_QWORD *)a1 + 2) = v14;
      goto LABEL_14;
    }
LABEL_19:
    v8 = 0;
    v14 = 0;
    v211 = 0;
    goto LABEL_20;
  }
  if ( a2 != 0 )
  {
    *((_QWORD *)a1 + 1) = *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + a2 + 8;
LABEL_14:
    v13 = 0;
    goto LABEL_15;
  }
  *((_QWORD *)a1 + 1) = 0;
  LOBYTE(v13) = 1;
LABEL_15:
  v211 = v13;
  LOBYTE(v8) = 1;
  if ( (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 88LL))(a1) == 0
    && (*(unsigned __int8 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 104LL))(a1) != 0 )
  {
    (*(void (__fastcall **)(_DWORD *, __int64))(*(_QWORD *)a1 + 96LL))(a1, v14);
  }
LABEL_20:
  v23 = *((_QWORD *)a1 + 2);
  if ( v23 == 0 )
  {
    v24 = 0;
    v206 = 0;
    goto LABEL_25;
  }
  v206 = 0;
  v24 = 0;
  if ( *(_BYTE *)(v23 + 47) != 0 )
  {
LABEL_25:
    v213 = 0;
    goto LABEL_26;
  }
  v25 = *(_QWORD *)(v23 + 48);
  v213 = 0;
  if ( v25 != 0 )
  {
    v213 = *(_QWORD *)(v25 + 336);
    LOBYTE(v24) = 1;
    v206 = v25;
  }
LABEL_26:
  v26 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
  v27 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v26 + 1720LL))(v26);
  v28 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
  v29 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v28 + 1688LL))(v28);
  v217 = v29;
  if ( v27 != 0 )
  {
    v30 = *(unsigned __int16 *)(v27 + 508);
    if ( (_BYTE)v8 != 0 )
    {
      if ( (__int16)v30 <= (__int16)*(_DWORD *)(v14 + 168) )
        v30 = *(_DWORD *)(v14 + 168);
      v212 = v30;
    }
    else
    {
      v212 = *(unsigned __int16 *)(v27 + 508);
    }
  }
  else if ( v29 != 0 )
  {
    v212 = *(unsigned __int16 *)(v29 + 210);
  }
  else
  {
    v212 = 0;
  }
  v31 = a8;
  v32 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1);
  v209 = v27;
  v216 = v8;
  if ( v32 == 6 )
  {
    v33 = *(_QWORD *)a1;
    if ( (_BYTE)v24 != 0 )
    {
      v34 = (*(__int64 (__fastcall **)(_DWORD *))(v33 + 80))(a1);
      v35 = *(_QWORD *)(v206 + 256);
      if ( (v34 & 1) != 0 )
      {
        v40 = v35 + 224;
        v41 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1) - 1;
        v42 = 4;
        if ( v41 <= 0x14u )
          v42 = *(_QWORD *)(8LL * (char)v41 + 0x14187F0B0LL);
        v38 = (unsigned __int8 *)(v42 + v40);
      }
      else
      {
        v36 = *((_QWORD *)a1 + 2);
        v37 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 80LL))(a1);
        v31 = a8;
        v38 = (unsigned __int8 *)(v35 + (unsigned int)sub_14151E1D0(v37, v36) + 231);
      }
      v39 = *v38;
      v33 = *(_QWORD *)a1;
      v27 = v209;
    }
    else
    {
      v39 = 0;
    }
    (*(void (__fastcall **)(_DWORD *, __int64))(v33 + 200))(a1, v39);
  }
  v205 = dword_141AAE084;
  if ( v31 != 0 )
  {
    v43 = a1[15];
LABEL_52:
    v205 = v43;
    goto LABEL_53;
  }
  if ( a4 != 0 )
  {
    v44 = *(_WORD *)(qword_141B5AD60 + 302);
    v27 = v209;
    if ( v44 > HIWORD(dword_141AAE084)
      || v44 >= HIWORD(dword_141AAE084)
      && (unsigned __int16)(*(_WORD *)(qword_141B5AD60 + 300) & 0x1FF) > (unsigned __int16)(dword_141AAE084 & 0x1FF) )
    {
      v43 = *(_DWORD *)(qword_141B5AD60 + 300);
      goto LABEL_52;
    }
  }
LABEL_53:
  v45 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
  v46 = (*(__int64 (__fastcall **)(__int64, unsigned int *))(*(_QWORD *)v45 + 408LL))(v45, &v205);
  v214 = v14;
  v201 = a4;
  v215 = v24;
  if ( (_BYTE)v24 != 0 )
  {
    v47 = v206;
    v48 = *(_QWORD *)(v206 + 216);
    if ( v48 != 0
      && (*(_BYTE *)(v206 + 185) != 0 && (v49 = *(_QWORD *)(v48 + 272)) != 0 || (v49 = *(_QWORD *)(v48 + 264)) != 0) )
    {
      if ( (_BYTE)v211 != 0 )
        v50 = 0;
      else
        v50 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
      v52 = sub_1408B4CB0(qword_141B5AD60, *(_QWORD *)(v49 + 368), *(unsigned __int8 *)(v49 + 185));
      if ( v52 != 0 )
      {
        v53 = sub_140D8BF00(v52, v47, v50, v46, 0);
        v51 = 100;
        if ( v53 > 0 )
          v51 = v53;
      }
      else
      {
        v51 = 100;
      }
      LOBYTE(v50) = 1;
    }
    else
    {
      v50 = 0;
      v49 = 0;
      v51 = 0;
    }
  }
  else
  {
    v50 = 0;
    v49 = 0;
    v51 = 0;
    v47 = v206;
  }
  v206 = v47;
  v218 = v50;
  if ( v27 != 0 )
  {
    if ( (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) < v51 )
    {
      v54 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1);
      if ( ((v54 < 2) | (unsigned __int8)v215 ^ 1) == 0 )
      {
        v55 = (*(char (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1);
        if ( v55 <= 0x14 )
        {
          v56 = 1912706;
          if ( _bittest(&v56, v55) )
          {
            if ( (char)v46 >= 17 )
              a1[6] = 0;
          }
        }
      }
    }
    if ( (_BYTE)v50 != 0 && v210 == 0 )
    {
      v57 = sub_1408B4CB0(qword_141B5AD60, *(_QWORD *)(v49 + 368), *(unsigned __int8 *)(v49 + 185));
      if ( v57 == 0 || (v58 = *(_BYTE *)(v57 + 429)) <= 0 )
        v58 = 19;
      if ( (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) <= 0 && *(__int16 *)(v27 + 512) <= 89 )
      {
        v59 = sub_1408B4CB0(qword_141B5AD60, *(_QWORD *)(v49 + 368), *(unsigned __int8 *)(v49 + 185));
        if ( v59 == 0 )
          goto LABEL_89;
        v203 = v46;
        v60 = v59;
        v61 = *(_QWORD *)(v59 + 280);
        v62 = *(_QWORD **)(v61 + 32);
        v63 = *(_QWORD **)(v61 + 40);
        if ( v62 == v63 )
        {
LABEL_87:
          v64 = *(_BYTE *)(v60 + 428);
        }
        else
        {
          while ( 1 )
          {
            v64 = (*(__int64 (__fastcall **)(_QWORD, __int64))(*(_QWORD *)*v62 + 936LL))(*v62, v206);
            if ( v64 != -1 )
              break;
            if ( ++v62 == v63 )
              goto LABEL_87;
          }
        }
        v47 = v206;
        v27 = v209;
        v46 = v203;
        if ( v64 <= 0 )
LABEL_89:
          v64 = 19;
        if ( (char)v46 < v58 && (char)v46 < v64 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1) != 1 )
          {
            if ( (*(unsigned __int8 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1) != 0 )
            {
              v65 = sub_14106EF90(v49, v47, v27, v46);
            }
            else
            {
              if ( (_BYTE)v211 != 0 )
                v69 = 0;
              else
                v69 = a2 + *(_DWORD *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
              v65 = sub_14106F930(v49, v47, v46, v69, 0);
            }
            v51 = v65;
          }
          a1[6] = v51;
        }
      }
      if ( (char)v46 < v58 )
        a1[6] = sub_14106EF90(v49, v47, v27, v46);
    }
    v66 = v217 != 0;
  }
  else
  {
    v66 = true;
    if ( v217 == 0 )
    {
      v67 = -1;
      v68 = v201;
      goto LABEL_193;
    }
  }
  if ( (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) <= 0
    || (v70 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1)) > 40 * (__int16)v212 )
  {
    v204 = v46;
    if ( ((v27 == 0) | (unsigned __int8)v215 ^ 1) != 0 )
    {
      v72 = false;
    }
    else
    {
      v71 = *(__int64 **)(v47 + 24);
      v72 = true;
      if ( v71 != *(__int64 **)(v47 + 32) )
      {
        v73 = *v71;
        if ( v73 != 0 )
        {
          v74 = *(__int16 *)(v73 + 168);
          if ( v74 >= 4500 )
            v72 = (double)(__int16)v74 * MEMORY[0x141862C38] > (double)*(__int16 *)(v209 + 508);
        }
      }
    }
    if ( v66 && *(_BYTE *)(*(_QWORD *)(*((_QWORD *)a1 + 2) + 48LL) + 186LL) == 1 )
    {
      v75 = *(_QWORD *)(a2 + 168);
      if ( v75 != 0 && (v76 = *(_QWORD *)(v75 + 16)) != 0 )
        v77 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v76 + 80LL))(v76);
      else
        v77 = 0;
      v79 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v79 + 1296LL))(v79) != 0 )
      {
        v81 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
        v77 |= (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v81 + 640LL))(v81) != 0;
      }
      if ( v77 != 0 )
      {
        if ( (_BYTE)v216 != 0 )
        {
          LOBYTE(v80) = *(_BYTE *)(v214 + 47) == 0;
          v78 = 0;
          v67 = 0;
          if ( (unsigned __int8)sub_141034D20(a5, a6, v80) != 0 )
            goto LABEL_164;
        }
        v82 = *(_QWORD *)(a2 + 168);
        if ( v82 != 0 && (v83 = *(_QWORD *)(v82 + 16)) != 0 )
          v84 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v83 + 80LL))(v83);
        else
          v84 = 0;
        v96 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v96 + 1296LL))(v96) != 0 )
        {
          v97 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
          v84 |= (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v97 + 640LL))(v97) != 0;
        }
        v98 = *((_QWORD *)a1 + 2);
        if ( v98 != 0 )
        {
          v99 = *(_QWORD *)(v98 + 48);
          if ( (_BYTE)v211 != 0 )
          {
LABEL_157:
            v100 = 0;
LABEL_161:
            v95 = sub_140EE1F50((_DWORD)a1, v100, v99, a7, 0, v84, v214, 0, 1, (__int64)&v205, 0, 0, 0, 4, 0);
            goto LABEL_162;
          }
        }
        else
        {
          LODWORD(v99) = 0;
          if ( (_BYTE)v211 != 0 )
            goto LABEL_157;
        }
        v100 = a2 + *(_DWORD *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
        goto LABEL_161;
      }
    }
    if ( v209 != 0 && v72 )
    {
      v85 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1);
      if ( ((((v85 - 2) & 0xFFFFFFFD) != 0 && v213 != 0) & (unsigned __int8)v218) == 1 && *(_QWORD *)(v49 + 1088) != 0 )
      {
        v86 = v209;
        v87 = *(_QWORD *)(v209 + 232);
        if ( v87 != 0 )
        {
          v88 = *(char *)(v87 + 53) - 11LL;
          v89 = v201;
          if ( (unsigned int)v88 > 8 )
            v78 = 0;
          else
            v78 = *(_BYTE *)(v88 + 0x14187F158LL);
        }
        else
        {
          v78 = 0;
          v89 = v201;
        }
        v182 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
        v183 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v182 + 672LL))(v182);
        v184 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1) - 1;
        if ( v184 > 0x15u )
          v185 = 0;
        else
          v185 = *(_BYTE *)((char)v184 + 0x14187B278LL);
        if ( (_BYTE)v211 != 0 )
          v186 = 0;
        else
          v186 = a2 + *(_DWORD *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
        sub_1414954A0(v213, 0, v186, v47, v86, *(_WORD *)(v86 + 508), v185, v78, v183, v89);
        v67 = (int)v187;
        goto LABEL_164;
      }
    }
    v90 = *((_QWORD *)a1 + 2);
    if ( v90 != 0 )
      v91 = *(_QWORD *)(v90 + 48);
    else
      LODWORD(v91) = 0;
    if ( (_BYTE)v211 != 0 )
      v92 = 0;
    else
      v92 = a2 + *(_DWORD *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
    v67 = sub_140EE1F50((_DWORD)a1, v92, v91, a7, 0, a5, v214, 0, v72, (__int64)&v205, 0, 0, 0, 4, 0);
    if ( (*(unsigned __int8 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1) != 0
      || (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) <= 0
      || (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) > 299 )
    {
      if ( (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) <= 0 )
        goto LABEL_147;
      v93 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) - v67;
      v94 = -v93;
      if ( v93 > 0 )
        v94 = v93;
      if ( v94 >= 0x64 )
      {
LABEL_147:
        if ( MEMORY[0x14186AAD8] * (double)v67 <= (double)(*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1)
          || (double)(*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) <= (double)v67 * MEMORY[0x141863AE8] )
        {
          a1[6] = 0;
LABEL_163:
          v78 = 0;
LABEL_164:
          v101 = *((_QWORD *)a1 + 2);
          if ( v101 != 0
            && (v102 = *(_QWORD *)(v101 + 48)) != 0
            && (v103 = *(__int64 **)(v102 + 24)) != *(__int64 **)(v102 + 32)
            && (v104 = *v103, *v103 != 0) )
          {
            v105 = *(_QWORD *)(v104 + 48);
            if ( v105 != 0 )
              v105 = *(_QWORD *)(v104 + 80);
            v106 = *(_QWORD *)(v104 + 96);
            if ( v209 == 0 )
              goto LABEL_171;
          }
          else
          {
            v105 = 0;
            v104 = 0;
            v106 = 0;
            if ( v209 == 0 )
            {
LABEL_171:
              v27 = v209;
              v68 = v201;
LABEL_172:
              v46 = v204;
              goto LABEL_193;
            }
          }
          v107 = sub_140DDC300(a2 + 336);
          if ( v106 != 0 && v105 != 0 && v107 >= 366 && v106 != v105 && v67 >= 201 )
          {
            v108 = ((unsigned int)(26215 * *(__int16 *)(v106 + 384)) >> 31) + ((26215 * *(__int16 *)(v106 + 384)) >> 18);
            if ( *(__int16 *)(v106 + 384) / 10 < 2 )
              LOWORD(v108) = 1;
            v109 = ((unsigned int)(26215 * *(__int16 *)(v105 + 384)) >> 31) + ((26215 * *(__int16 *)(v105 + 384)) >> 18);
            if ( *(__int16 *)(v105 + 384) / 10 < 2 )
              LOWORD(v109) = 1;
            if ( (unsigned __int16)v108 < (unsigned __int16)v109 )
              v67 = (int)(float)((float)v67
                               * fmaxf(
                                   MEMORY[0x141764684],
                                   (float)((float)(char)(((unsigned __int16)((unsigned int)(33555
                                                                                          * *(__int16 *)(v104 + 168)) >> 16) >> 15)
                                                       + ((unsigned int)(33555 * *(__int16 *)(v104 + 168)) >> 24)
                                                       - v109)
                                         / MEMORY[0x141775530])
                                 + MEMORY[0x1417597F0]));
          }
          v27 = v209;
          v68 = v201;
          v46 = v204;
          goto LABEL_186;
        }
      }
    }
    v95 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1);
LABEL_162:
    v67 = v95;
    goto LABEL_163;
  }
  v67 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1);
  v78 = 0;
  v68 = v201;
LABEL_186:
  if ( ((v27 == 0) | (unsigned __int8)v216 ^ 1) == 0 && *(_QWORD *)(v214 + 48) != 0 )
  {
    v110 = *(_QWORD *)(v214 + 80);
    if ( v110 != 0 && *(_QWORD *)(v110 + 176) != 0 && sub_1409A3C20() > 0.0 )
    {
      v111 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1);
      v112 = 0;
      v204 = v46;
      if ( *(_BYTE *)(v214 + 47) != 0 )
        LODWORD(v113) = 0;
      else
        v113 = *(_QWORD *)(v214 + 48);
      v180 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1) - 1;
      if ( v180 <= 0x15u )
        v112 = *(unsigned __int8 *)((char)v180 + 0x14187B278LL);
      sub_140EBDD70(v110, v112, v113, v111, v209, 1, v78);
      if ( v181 > MEMORY[0x141759000] && v67 >= (int)v181 )
        v67 = (int)v181;
      v68 = v201;
      v27 = v209;
      goto LABEL_172;
    }
  }
LABEL_193:
  if ( (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) <= 0
    && (((*(char (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1) - 2) & 0xFFFFFFFD) != 0 )
  {
    a1[6] = v67;
  }
  if ( v68 != 0 )
  {
    v116 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1);
    if ( v213 != 0 && v116 > 0 )
    {
      v117 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 208LL))(a1);
      v119 = (_BYTE)v211 != 0 ? 0 : a2 + *(_DWORD *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
      LOBYTE(v118) = *(_BYTE *)(v206 + 362) == 1;
      v120 = sub_141491280(v213, v46, v118, v119, v117, 0);
      if ( (*(int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 64LL))(a1) < v120 )
        a1[6] = v120;
    }
  }
  if ( a8 != 0 )
  {
    *((_BYTE *)a1 + 79) = 0;
    goto LABEL_346;
  }
  v121 = *((unsigned __int16 *)a1 + 31);
  v122 = a1[15] & 0x1FF;
  LOBYTE(v114) = v122 == 1;
  LOBYTE(v115) = (_DWORD)v121 == 2000;
  if ( (_DWORD)v121 == 1900 && v122 == 1 || (LOBYTE(v114) = v115 & v114, (_BYTE)v114 != 0) )
  {
    if ( v206 != 0 )
    {
      if ( (*(_BYTE *)(*(int *)(*(_QWORD *)(a2 + 8) + 4LL) + a2 + 32) & 8) != 0 )
      {
        if ( (unsigned __int8)sub_140087040(v121, v114, v115) != 0 )
          v123 = &dword_141AAE084;
        else
          v123 = (int *)(qword_141B5AD60 + 300);
      }
      else
      {
        v123 = (int *)(a2 + 292);
      }
    }
    else
    {
      v123 = (int *)(a2 + 288);
    }
  }
  else if ( (unsigned __int16)v121 <= HIWORD(v205) )
  {
    v123 = (int *)&v205;
    if ( (unsigned __int16)v121 < HIWORD(v205) || v122 <= (unsigned __int16)(v205 & 0x1FF) )
      goto LABEL_221;
  }
  else
  {
    v123 = (int *)&v205;
  }
  (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)a1 + 216LL))(a1, v123);
LABEL_221:
  v202 = v215 & v68;
  if ( ((unsigned __int8)v215 & (unsigned __int8)v68) == 1
    && (*(unsigned __int8 (__fastcall **)(_DWORD *, int *))(*(_QWORD *)a1 + 208LL))(a1, v123) == 3 )
  {
    v124 = *(_QWORD *)(v206 + 216);
    if ( v124 != 0 && *(_DWORD *)(v124 + 12) == 765 )
    {
      v125 = (v205 & 0x1FF) - 731;
      v126 = HIWORD(v205) - 1;
      do
      {
        v127 = (unsigned __int16)v126;
        v128 = 3;
        if ( 25
           * (unsigned __int16)((((18351 * (unsigned int)(unsigned __int16)v126) >> 16)
                               + ((unsigned __int16)(v126 - ((18351 * (unsigned int)(unsigned __int16)v126) >> 16)) >> 1)) >> 4) == (_WORD)v126 )
          v128 = 15;
        LOWORD(v126) = v126 - 1;
        v125 += ((v127 & v128) == 0) + 365;
      }
      while ( v125 < 0 );
      v129 = *((_WORD *)a1 + 31);
      v27 = v209;
      if ( (a1[15] & 0x1FF ^ 1 | v129 ^ 0x76C) == 0
        || (v130 = v126 + 1, v129 < v130)
        || v129 <= v130 && (unsigned __int16)(a1[15] & 0x1FF) <= (unsigned __int16)(v125 + 1) )
      {
        (*(void (__fastcall **)(_DWORD *, unsigned int *))(*(_QWORD *)a1 + 216LL))(a1, &v205);
        *((_BYTE *)a1 + 79) = 0;
        v131 = v206;
        goto LABEL_285;
      }
    }
  }
  if ( v27 != 0 )
  {
    v132 = *(__int16 *)(v27 + 510);
    if ( (_BYTE)v215 == 0
      || (v133 = *(__int64 **)(v206 + 24)) == *(__int64 **)(v206 + 32)
      || (v134 = *v133) == 0
      || v132 < 7751
      || (v135 = 730, *(__int16 *)(v134 + 168) <= 7250) )
    {
      v135 = 1095;
      if ( v132 <= 5250 )
      {
        v135 = 1825;
        if ( v132 >= 3751 )
          v135 = 1460;
      }
    }
    v136 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
    v137 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v136 + 408LL))(v136, 0x1418761ECLL);
    v138 = 16;
    if ( v137 >= 17 )
      v138 = v137;
    if ( (unsigned __int8)v138 <= 0x12u )
    {
      v139 = 365 * (unsigned __int8)(v138 - 14);
      if ( v139 < v135 )
        v135 = v139;
    }
  }
  else
  {
    v135 = 1825;
  }
  v140 = v205 & 0x1FF;
  v141 = a1[15] & 0x1FF;
  v142 = HIWORD(v205);
  v143 = *((_WORD *)a1 + 31);
  v144 = 365;
  if ( HIWORD(v205) <= v143 && (HIWORD(v205) < v143 || (unsigned __int16)v140 < (unsigned __int16)v141) )
  {
    v144 = -365;
    v145 = *((_WORD *)a1 + 31);
  }
  else
  {
    v145 = HIWORD(v205);
    v142 = *((_WORD *)a1 + 31);
  }
  v131 = v206;
  if ( v144 * (v145 - v142) + v140 - v141 > v135 )
  {
    v146 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
    v147 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v146 + 408LL))(v146, 0x1418761ECLL);
    if ( v147 > 20 )
    {
      if ( (unsigned __int8)v147 < 0x1Du )
      {
        if ( v209 != 0 && *(__int16 *)(v209 + 510) >= 5751 )
        {
          v152 = v205;
          v153 = (v205 & 0x1FF) - 729;
          v154 = HIWORD(v205) - 1;
          do
          {
            v157 = v154;
            v158 = 3;
            if ( 25
               * (unsigned __int16)((((18351 * (unsigned int)v154) >> 16)
                                   + ((unsigned __int16)(v154 - ((18351 * (unsigned int)v154) >> 16)) >> 1)) >> 4) == v154 )
              v158 = 15;
            --v154;
            v153 += ((v157 & v158) == 0) + 365;
          }
          while ( v153 < 0 );
        }
        else
        {
          v152 = v205;
          v153 = (v205 & 0x1FF) - 1093;
          v154 = HIWORD(v205) - 1;
          do
          {
            v159 = v154;
            v160 = 3;
            if ( 25
               * (unsigned __int16)((((18351 * (unsigned int)v154) >> 16)
                                   + ((unsigned __int16)(v154 - ((18351 * (unsigned int)v154) >> 16)) >> 1)) >> 4) == v154 )
              v160 = 15;
            --v154;
            v153 += ((v159 & v160) == 0) + 365;
          }
          while ( v153 < 0 );
        }
      }
      else
      {
        v152 = v205;
        v153 = (v205 & 0x1FF) - 729;
        v154 = HIWORD(v205) - 1;
        do
        {
          v155 = v154;
          v156 = 3;
          if ( 25
             * (unsigned __int16)((((18351 * (unsigned int)v154) >> 16)
                                 + ((unsigned __int16)(v154 - ((18351 * (unsigned int)v154) >> 16)) >> 1)) >> 4) == v154 )
            v156 = 15;
          --v154;
          v153 += ((v155 & v156) == 0) + 365;
        }
        while ( v153 < 0 );
      }
      v208 = v154 + 1;
      v207 = (v153 + 1) | v152 & 0xFE00;
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)a1 + 216LL))(a1, &v207);
      v131 = v206;
    }
    else
    {
      LOWORD(v148) = HIWORD(v205);
      v149 = v205 & 0x1FF;
      v150 = v149 - 365;
      if ( v149 <= 0x16C )
      {
        v148 = HIWORD(v205) - 1;
        v151 = 3;
        if ( (unsigned __int16)(23593 * v148) < 0xA3Eu )
          v151 = 15;
        v150 = ((v148 & v151) == 0) + (_WORD)v149;
      }
      v208 = v148;
      v207 = (v150 + 1) | v205 & 0xFE00;
      (*(void (__fastcall **)(_DWORD *, __int16 *))(*(_QWORD *)a1 + 216LL))(a1, &v207);
    }
    v161 = (_WORD *)(a2 + 292);
    v162 = *(_WORD *)(a2 + 294);
    if ( *((_WORD *)a1 + 31) < v162
      || *((_WORD *)a1 + 31) <= v162 && (unsigned __int16)(a1[15] & 0x1FF) < (unsigned __int16)(*v161 & 0x1FF) )
    {
      (*(void (__fastcall **)(_DWORD *, _WORD *))(*(_QWORD *)a1 + 216LL))(a1, v161);
    }
  }
  *((_BYTE *)a1 + 79) = 0;
  if ( v202 != 0 )
  {
LABEL_285:
    if ( *(_BYTE *)(v131 + 362) != 1 )
      goto LABEL_346;
    v163 = *(__int64 **)(v131 + 24);
    v164 = 1500;
    if ( v163 != *(__int64 **)(v131 + 32) )
    {
      v165 = *v163;
      if ( v165 != 0 )
        v164 = *(_WORD *)(v165 + 168);
    }
    v166 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1);
    if ( v166 > 0x14u )
    {
      v171 = 0;
      v168 = 0;
      v174 = 0;
      v176 = 0;
      v177 = 0;
    }
    else
    {
      v169 = v166;
      v170 = 32782;
      v171 = _bittest(&v170, v169);
      v172 = 2031728;
      LOBYTE(v168) = _bittest(&v172, v169);
      v173 = 6;
      v174 = _bittest(&v173, v169);
      v175 = 32776;
      v176 = _bittest(&v175, v169);
      v167 = 2064510;
      v177 = _bittest((const int *)&v167, v169);
    }
    if ( v164 < 5251 )
    {
      v179 = v206;
      if ( v164 < 3251 )
        goto LABEL_346;
      if ( v171 == 0 )
      {
        if ( (_BYTE)v168 != 0 )
        {
          v178 = 3;
          if ( v67 >= 750 )
          {
            v178 = 4;
            if ( (unsigned int)v67 >= 0x9C4 )
              goto LABEL_346;
          }
        }
        else
        {
          v178 = 4;
          if ( v67 <= 2500 )
            goto LABEL_346;
        }
        goto LABEL_333;
      }
      v178 = 3;
      if ( v67 >= 750 )
      {
        v178 = 4;
        if ( (unsigned int)v67 >= 0x9C4 )
        {
          LOBYTE(v167) = 6;
          if ( (unsigned int)v67 >= 0xFA0 )
            goto LABEL_346;
          goto LABEL_335;
        }
      }
    }
    else
    {
      if ( v174 != 0 )
      {
        v178 = 4;
        v179 = v206;
        if ( v67 >= 12500 )
        {
          LOBYTE(v167) = 8;
          if ( (unsigned int)v67 >= 0x4E20 )
            goto LABEL_346;
          goto LABEL_335;
        }
        goto LABEL_333;
      }
      if ( v176 == 0 )
      {
        v179 = v206;
        if ( v177 != 0 )
        {
          v178 = 3;
          if ( v67 >= 2500 )
          {
            v178 = 4;
            if ( (unsigned int)v67 >= 0x2710 )
              goto LABEL_346;
          }
        }
        else
        {
          v178 = 4;
          if ( v67 <= 15000 )
            goto LABEL_346;
        }
        goto LABEL_333;
      }
      v178 = 4;
      v179 = v206;
      if ( v67 >= 7500 )
      {
        LOBYTE(v167) = 7;
        if ( (unsigned int)v67 >= 0x3A98 )
          goto LABEL_346;
LABEL_335:
        v190 = *(__int64 **)(v179 + 24);
        if ( v190 == *(__int64 **)(v179 + 32) )
        {
          v191 = 0;
          if ( (_BYTE)v211 != 0 )
            goto LABEL_337;
        }
        else
        {
          v191 = *v190;
          if ( (_BYTE)v211 != 0 )
          {
LABEL_337:
            v192 = 0;
LABEL_340:
            v195 = sub_1410F1110(v167, v192, v191);
            if ( *((_BYTE *)a1 + 76) != v195 )
            {
              if ( (unsigned __int8)sub_140087040(v194, v193, v196) != 0 )
                (*(void (__fastcall **)(_DWORD *, int *))(*(_QWORD *)a1 + 280LL))(a1, &dword_141AAE084);
              if ( *((_BYTE *)a1 + 76) > v195 )
                *((_BYTE *)a1 + 84) = 20;
            }
            *((_BYTE *)a1 + 76) = v195;
            *((_BYTE *)a1 + 78) = v195;
            goto LABEL_346;
          }
        }
        v192 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
        goto LABEL_340;
      }
    }
LABEL_333:
    v188 = a2 + *(int *)(*(_QWORD *)(a2 + 8) + 4LL) + 8;
    v189 = (*(char (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v188 + 408LL))(v188, 0x1418761ECLL, v168) < 22;
    v167 = 6;
    if ( v189 )
      v167 = v178;
    goto LABEL_335;
  }
LABEL_346:
  *((_BYTE *)a1 + 86) = 0;
  *((_QWORD *)a1 + 4) = 0;
  v197 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1) - 1;
  LOWORD(v198) = -30;
  LOWORD(v199) = -30;
  if ( v197 <= 0x14u )
  {
    v198 = *(_DWORD *)(4LL * (char)v197 + 0x14187F178LL);
    v199 = *(_DWORD *)(4LL * (char)v197 + 0x14187F1CCLL);
  }
  *((_BYTE *)a1 + 83) = v199 + ((unsigned __int16)(v198 - v199 + ((unsigned __int16)(v198 - v199) >> 15)) >> 1);
  *((_BYTE *)a1 + 82) = *(_BYTE *)(a2 + 84) + *(_BYTE *)(a2 + 82) - *(_BYTE *)(a2 + 81) + 10;
  result = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1) - 1;
  if ( result <= 0x14u )
  {
    result = *(_BYTE *)((char)result + 0x14187F161LL);
    *((_BYTE *)a1 + 82) += result;
  }
  return result;
}
