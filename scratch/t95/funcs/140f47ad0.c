__int64 __fastcall sub_140F47AD0(
        __int64 a1,
        __int64 *a2,
        char a3,
        char a4,
        char a5,
        unsigned __int8 a6,
        char a7,
        __int64 *a8,
        __int64 *a9,
        char a10,
        __int64 a11,
        char a12)
{
  __int64 *v12; // rsi
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 *v19; // rdx
  __int64 *v20; // rdi
  int v21; // r12d
  __int64 v22; // rcx
  __int64 v23; // rdx
  __int64 *v24; // rax
  __int64 *v25; // rdx
  __int64 v26; // rax
  __int64 v27; // rcx
  __int64 *v28; // rdx
  __int64 v29; // rax
  __int64 v30; // rcx
  __int64 v31; // rdx
  __int64 *v32; // rdx
  __int64 v33; // rax
  __int64 v34; // rcx
  bool v35; // zf
  __int64 *v36; // rdx
  __int64 v37; // rbx
  __int64 v38; // rcx
  __int64 *v39; // rdx
  __int64 v40; // rax
  __int64 *v41; // rdx
  __int64 *v42; // rax
  __int64 v43; // rax
  unsigned int v44; // eax
  __int64 v45; // rax
  __int64 v46; // rcx
  __int64 v47; // rbx
  __int64 v48; // rax
  __int64 v49; // rax
  __int64 v50; // rax
  unsigned __int64 v51; // rsi
  __int64 v52; // rcx
  __int64 v53; // rax
  __int64 v54; // rax
  __int64 v55; // rax
  __int64 v56; // rcx
  __int64 *v57; // rax
  __int64 *v58; // rsi
  __int64 *v59; // rsi
  bool v60; // si
  __int64 v61; // rax
  __int64 v62; // rax
  __int64 v63; // rcx
  __int64 v64; // rax
  __int64 v65; // rax
  char v66; // bl
  __int64 *v67; // rsi
  __int64 *v68; // rsi
  __int64 v69; // rcx
  __int64 v70; // rax
  __int64 v71; // rcx
  __int64 v72; // rax
  __int64 v73; // rcx
  __int64 v74; // rax
  __int64 v75; // rcx
  __int64 v76; // rax
  __int64 v77; // rax
  __int64 v78; // rcx
  __int64 *v79; // rdx
  __int64 *v80; // rsi
  __int64 *v81; // rsi
  __int64 v82; // rsi
  __int64 v83; // rdi
  volatile signed __int32 *v84; // rcx
  volatile signed __int32 *v85; // rcx
  volatile signed __int32 *v86; // rcx
  volatile signed __int32 *v87; // rcx
  __int64 *v88; // rax
  __int64 v89; // rax
  __int64 v90; // rax
  __int64 v91; // rsi
  unsigned __int64 v92; // rsi
  __int64 v93; // rax
  __int64 v94; // rbx
  __int64 v95; // r13
  __int64 *v96; // rbx
  _QWORD *v97; // rdi
  __int64 v98; // rdi
  int *v99; // rax
  int v100; // edi
  __int64 v101; // rax
  __int64 v102; // rcx
  __int64 *v103; // rdx
  __int64 v104; // rax
  __int64 v105; // rcx
  __int64 v106; // rdx
  __int64 *v107; // rdx
  __int64 v108; // rsi
  volatile signed __int32 *v109; // rcx
  __int64 v110; // rax
  __int64 v111; // rcx
  __int64 *v112; // rdx
  __int64 v113; // r12
  _QWORD *v114; // rdi
  __int64 v115; // r15
  __int64 v116; // r15
  __int64 v117; // rbx
  __int64 v118; // rcx
  __int64 v119; // rdx
  __int64 *v120; // rax
  __int64 v121; // rax
  __int64 *v122; // r8
  __int64 *v123; // rax
  __int64 *v124; // rdx
  __int64 v125; // rcx
  __int64 v126; // rcx
  __int64 *v127; // rax
  __int64 *v128; // r8
  __int64 v129; // rcx
  __int64 v131; // rdi
  volatile signed __int32 *v132; // rcx
  volatile signed __int32 *v133; // rcx
  __int64 v134; // rcx
  __int64 v135; // rdi
  __int64 v136; // rcx
  volatile signed __int32 *v137; // rcx
  volatile signed __int32 *v138; // rcx
  int v139; // [rsp+38h] [rbp-48h]
  char v140; // [rsp+44h] [rbp-3Ch]
  __int64 v141; // [rsp+48h] [rbp-38h] BYREF
  __int64 v142; // [rsp+50h] [rbp-30h]
  __int64 *v143; // [rsp+58h] [rbp-28h]
  __int64 v144; // [rsp+60h] [rbp-20h]
  int v145; // [rsp+68h] [rbp-18h] BYREF
  unsigned int v146; // [rsp+6Ch] [rbp-14h]
  volatile signed __int32 *v147; // [rsp+70h] [rbp-10h] BYREF
  char v148; // [rsp+7Fh] [rbp-1h]
  volatile signed __int32 *v149; // [rsp+80h] [rbp+0h] BYREF
  __int64 v150; // [rsp+88h] [rbp+8h] BYREF
  unsigned __int64 v151; // [rsp+90h] [rbp+10h]
  char v152; // [rsp+AFh] [rbp+2Fh]
  __int64 v153; // [rsp+B0h] [rbp+30h]

  v153 = -2;
  v17 = *a2;
  v18 = a2[1];
  v19 = nullptr;
  if ( v17 != v18 )
  {
    while ( *(_DWORD *)v17 != 1685353593 )
    {
      v17 += 16;
      if ( v17 == v18 )
        goto LABEL_8;
    }
    if ( v17 == v18 )
      v19 = nullptr;
    else
      v19 = *(__int64 **)(v17 + 8);
  }
LABEL_8:
  v20 = &qword_141B5A4A0;
  if ( v19 == nullptr )
    v19 = &qword_141B5A4A0;
  v21 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v19 + 64LL))(*v19);
  if ( a12 != 0 )
  {
    v22 = *a2;
    v23 = a2[1];
    v24 = nullptr;
    if ( *a2 != v23 )
    {
      while ( *(_DWORD *)v22 != 1230195782 )
      {
        v22 += 16;
        if ( v22 == v23 )
          goto LABEL_18;
      }
      if ( v22 == v23 )
        v24 = nullptr;
      else
        v24 = *(__int64 **)(v22 + 8);
    }
LABEL_18:
    v25 = &qword_141B5A4A0;
    if ( v24 != nullptr )
      v25 = v24;
    LOBYTE(v12) = 1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v25 + 48LL))(*v25) == 0
      || v21 == 1 && (_BYTE)word_141B60320 == 0 )
    {
      return (unsigned int)v12;
    }
  }
  v26 = *a2;
  v27 = a2[1];
  v28 = nullptr;
  if ( *a2 != v27 )
  {
    while ( *(_DWORD *)v26 != 1685417577 )
    {
      v26 += 16;
      if ( v26 == v27 )
        goto LABEL_30;
    }
    if ( v26 == v27 )
      v28 = nullptr;
    else
      v28 = *(__int64 **)(v26 + 8);
  }
LABEL_30:
  if ( v28 == nullptr )
    v28 = &qword_141B5A4A0;
  sub_140FE3720(&v145, v28);
  v29 = *a2;
  v30 = a2[1];
  if ( v30 == *a2 )
  {
    LOBYTE(v12) = 1;
    return (unsigned int)v12;
  }
  LODWORD(v12) = a6;
  if ( *(_BYTE *)(a1 + 1400) != 0 )
  {
    v31 = *a2;
    while ( *(_DWORD *)v31 != 1433420099 )
    {
      v31 += 16;
      if ( v31 == v30 )
        goto LABEL_51;
    }
    if ( v31 != v30 && *(_QWORD *)(v31 + 8) != 0 )
    {
      v32 = nullptr;
      while ( *(_DWORD *)v29 != 1433420099 )
      {
        v29 += 16;
        if ( v29 == v30 )
          goto LABEL_48;
      }
      if ( v29 == v30 )
        v32 = nullptr;
      else
        v32 = *(__int64 **)(v29 + 8);
LABEL_48:
      if ( v32 == nullptr )
        v32 = &qword_141B5A4A0;
      LODWORD(v12) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v32 + 48LL))(*v32);
    }
LABEL_51:
    if ( (_BYTE)v12 != 0 )
    {
      ++*(_DWORD *)(a1 + 1520);
      LOBYTE(v12) = 1;
    }
    else
    {
      LODWORD(v12) = 0;
    }
  }
  v33 = *a2;
  v34 = a2[1];
  v35 = *a2 == v34;
  v152 = a3;
  if ( v35 )
    goto LABEL_61;
  v36 = nullptr;
  while ( *(_DWORD *)v33 != 1886549113 )
  {
    v33 += 16;
    if ( v33 == v34 )
      goto LABEL_62;
  }
  if ( v33 == v34 )
LABEL_61:
    v36 = nullptr;
  else
    v36 = *(__int64 **)(v33 + 8);
LABEL_62:
  if ( v36 == nullptr )
    v36 = &qword_141B5A4A0;
  v142 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v36 + 80LL))(*v36);
  v37 = *a2;
  v38 = a2[1];
  v140 = (char)v12;
  if ( *a2 == v38 )
  {
    v41 = nullptr;
    v143 = &qword_141B5A4A0;
  }
  else
  {
    v39 = nullptr;
    v40 = *a2;
    while ( *(_DWORD *)v40 != 1853322860 )
    {
      v40 += 16;
      if ( v40 == v38 )
        goto LABEL_73;
    }
    if ( v40 == v38 )
      v39 = nullptr;
    else
      v39 = *(__int64 **)(v40 + 8);
LABEL_73:
    v42 = &qword_141B5A4A0;
    if ( v39 != nullptr )
      v42 = v39;
    v143 = v42;
    v41 = nullptr;
    while ( *(_DWORD *)v37 != 1986359923 )
    {
      v37 += 16;
      if ( v37 == v38 )
        goto LABEL_82;
    }
    if ( v37 == v38 )
      v41 = nullptr;
    else
      v41 = *(__int64 **)(v37 + 8);
  }
LABEL_82:
  if ( v41 != nullptr )
    v20 = v41;
  v43 = qword_141B60C30;
  if ( qword_141B60C30 == qword_141B60C38 )
    goto LABEL_87;
  while ( *(_DWORD *)v43 != 1986359923 )
  {
    v43 += 16;
    if ( v43 == qword_141B60C38 )
      goto LABEL_87;
  }
  if ( v43 == qword_141B60C38 || (v12 = *(__int64 **)(v43 + 8)) == nullptr )
  {
LABEL_87:
    sub_140835A40(&qword_141B60C30, 1986359923, v20);
  }
  else if ( v12 != v20 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v12 + 16LL))(*v12, v12);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v20 + 24LL))(*v20, v20, v12);
  }
  v44 = (unsigned int)sub_140E78A80();
  sub_140FF58B0(v44, v21, v145, v142, (__int64)v143);
  v45 = sub_140F216C0(a1);
  if ( v45 == 0 )
    goto LABEL_107;
  v12 = (__int64 *)v45;
  v47 = (*(__int64 (__fastcall **)(__int64, int *))(*(_QWORD *)v45 + 32LL))(v45, &v145);
  if ( v21 == 55 && (*(__int64 (__fastcall **)(__int64 *))(*v12 + 48))(v12) != 0 )
    v47 = (*(__int64 (__fastcall **)(__int64 *, _QWORD))(*v12 + 16))(v12, 0);
  if ( v47 != 0 )
  {
    if ( a10 != 0 )
    {
      v48 = sub_14083D4F0(v46);
      LODWORD(v151) = 3569;
      v150 = v48 + 40;
      sub_140835380(a2, 1986359923, &v150);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    }
    v49 = sub_14083D4F0(v46);
    LODWORD(v151) = v21;
    v150 = v49 + 40;
    v50 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_98;
    while ( *(_DWORD *)v50 != 1685353593 )
    {
      v50 += 16;
      if ( v50 == qword_141B60C38 )
        goto LABEL_98;
    }
    if ( v50 == qword_141B60C38 || (v58 = *(__int64 **)(v50 + 8)) == nullptr )
    {
LABEL_98:
      sub_140835A40(&qword_141B60C30, 1685353593, &v150);
    }
    else if ( v58 != &v150 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v58 + 16LL))(*v58, v58);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v150 + 24LL))(v150, &v150, v58);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    v51 = ((unsigned __int64)v146 << 32) | v145;
    v53 = sub_14083D4F0(v52);
    v151 = v51;
    v150 = v53 + 72;
    v54 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_102;
    while ( *(_DWORD *)v54 != 1685417577 )
    {
      v54 += 16;
      if ( v54 == qword_141B60C38 )
        goto LABEL_102;
    }
    if ( v54 == qword_141B60C38 || (v59 = *(__int64 **)(v54 + 8)) == nullptr )
    {
LABEL_102:
      sub_140835A40(&qword_141B60C30, 1685417577, &v150);
    }
    else if ( v59 != &v150 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v59 + 16LL))(*v59, v59);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v150 + 24LL))(v150, &v150, v59);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    v55 = *a2;
    v56 = a2[1];
    if ( *a2 == v56 )
      goto LABEL_128;
    while ( *(_DWORD *)v55 != 1986359923 )
    {
      v55 += 16;
      if ( v55 == v56 )
        goto LABEL_128;
    }
    if ( v55 == v56 )
LABEL_128:
      v60 = false;
    else
      v60 = *(_QWORD *)(v55 + 8) != 0;
    v61 = sub_14083D4F0(v56);
    LOBYTE(v151) = !v60;
    v150 = v61 + 24;
    v62 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_132;
    while ( *(_DWORD *)v62 != 1766410053 )
    {
      v62 += 16;
      if ( v62 == qword_141B60C38 )
        goto LABEL_132;
    }
    if ( v62 == qword_141B60C38 || (v67 = *(__int64 **)(v62 + 8)) == nullptr )
    {
LABEL_132:
      sub_140835A40(&qword_141B60C30, 1766410053, &v150);
    }
    else if ( v67 != &v150 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v67 + 16LL))(*v67, v67);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v150 + 24LL))(v150, &v150, v67);
    }
    v144 = v47;
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    v64 = sub_14083D4F0(v63);
    LOBYTE(v151) = a7;
    v150 = v64 + 24;
    v65 = qword_141B60C30;
    v66 = v152;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_145;
    while ( *(_DWORD *)v65 != 1668178792 )
    {
      v65 += 16;
      if ( v65 == qword_141B60C38 )
        goto LABEL_145;
    }
    if ( v65 == qword_141B60C38 || (v68 = *(__int64 **)(v65 + 8)) == nullptr )
    {
LABEL_145:
      sub_140835A40(&qword_141B60C30, 1668178792, &v150);
    }
    else if ( v68 != &v150 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v68 + 16LL))(*v68, v68);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v150 + 24LL))(v150, &v150, v68);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    v70 = sub_14083D4F0(v69);
    v151 = 0;
    v71 = qword_141B59EE0;
    if ( qword_141B59EE0 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
    v151 = v71;
    v150 = v70 + 136;
    v72 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_151;
    while ( *(_DWORD *)v72 != 1668179565 )
    {
      v72 += 16;
      if ( v72 == qword_141B60C38 )
        goto LABEL_151;
    }
    if ( v72 == qword_141B60C38 || (v80 = *(__int64 **)(v72 + 8)) == nullptr )
    {
LABEL_151:
      sub_140835A40(&qword_141B60C30, 1668179565, &v150);
    }
    else if ( v80 != &v150 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v80 + 16LL))(*v80, v80);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v150 + 24LL))(v150, &v150, v80);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    v74 = sub_14083D4F0(v73);
    v151 = 0;
    v75 = qword_141B59EE0;
    if ( qword_141B59EE0 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
    v151 = v75;
    v150 = v74 + 136;
    v76 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_157;
    while ( *(_DWORD *)v76 != 1684170098 )
    {
      v76 += 16;
      if ( v76 == qword_141B60C38 )
        goto LABEL_157;
    }
    if ( v76 == qword_141B60C38 || (v81 = *(__int64 **)(v76 + 8)) == nullptr )
    {
LABEL_157:
      sub_140835A40(&qword_141B60C30, 1684170098, &v150);
    }
    else if ( v81 != &v150 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v81 + 16LL))(*v81, v81);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v150 + 24LL))(v150, &v150, v81);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    v77 = *a2;
    v78 = a2[1];
    v79 = nullptr;
    if ( *a2 != v78 )
    {
      while ( *(_DWORD *)v77 != 1668248696 )
      {
        v77 += 16;
        if ( v77 == v78 )
          goto LABEL_193;
      }
      if ( v77 == v78 )
        v79 = nullptr;
      else
        v79 = *(__int64 **)(v77 + 8);
    }
LABEL_193:
    if ( v79 == nullptr )
      v79 = &qword_141B5A4A0;
    v89 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v79 + 176LL))(*v79, v79, 0);
    sub_1408350B0(&qword_141B60C30, v89);
    if ( v146 == 0 )
    {
      v90 = *(int *)(v144 + 12);
      v145 = *(_DWORD *)(v144 + 12);
      v91 = *(unsigned int *)(v144 + 16);
      if ( (_DWORD)v91 == 0 )
        v91 = (unsigned int)v90;
      v146 = v91;
      v92 = v90 | (v91 << 32);
      v93 = sub_14083D4F0(v144);
      v151 = v92;
      v150 = v93 + 72;
      sub_140835380(a2, 1685417577, &v150);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
    }
    if ( dword_141B5E5E8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5E5E8);
      if ( dword_141B5E5E8 == -1 )
      {
        sub_1407C9510(&qword_141B5E5D0);
        sub_141751048(sub_140F49020);
        sub_141750EA0(&dword_141B5E5E8);
      }
    }
    v139 = v21;
    v148 = a4;
    if ( v66 != 0 )
    {
      v12 = &v150;
      sub_14083DC80(&v150, a2);
      sub_14083B5F0(&qword_141B5E5D0, &v150);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
      v94 = v144;
    }
    else
    {
      v12 = (__int64 *)qword_141B5E5D8;
      v95 = qword_141B5E5D0;
      v94 = v144;
      if ( qword_141B5E5D0 != qword_141B5E5D8 )
      {
        v96 = (__int64 *)qword_141B5E5D0;
        do
        {
          v97 = (_QWORD *)*v96;
          if ( *v96 != 0 )
          {
            (*(void (__fastcall **)(_QWORD, __int64))(*(_QWORD *)*v97 + 16LL))(*v97, *v96);
            sub_1408B5E70(v97);
          }
          ++v96;
        }
        while ( v96 != v12 );
        v98 = qword_141B5E5D8 - (_QWORD)v12;
        sub_141758A00();
        qword_141B5E5D8 = v95 + v98;
        v94 = v144;
      }
    }
    *(_BYTE *)(a1 + 1484) = v140;
    v99 = *(int **)(a1 + 1344);
    if ( v99 == *(int **)(a1 + 1352) )
      v100 = -1;
    else
      v100 = *v99;
    v101 = *a2;
    v102 = a2[1];
    v103 = nullptr;
    if ( *a2 != v102 )
    {
      while ( *(_DWORD *)v101 != 1230195782 )
      {
        v101 += 16;
        if ( v101 == v102 )
          goto LABEL_218;
      }
      if ( v101 == v102 )
        v103 = nullptr;
      else
        v103 = *(__int64 **)(v101 + 8);
    }
LABEL_218:
    if ( v103 == nullptr )
      v103 = &qword_141B5A4A0;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v103 + 48LL))(*v103) == 0 )
      goto LABEL_245;
    v104 = *a2;
    v105 = a2[1];
    if ( *a2 == v105 )
      goto LABEL_245;
    v106 = *a2;
    while ( *(_DWORD *)v106 != 1129663566 )
    {
      v106 += 16;
      if ( v106 == v105 )
        goto LABEL_245;
    }
    if ( v106 == v105 || *(_QWORD *)(v106 + 8) == 0 )
      goto LABEL_245;
    v107 = nullptr;
    while ( *(_DWORD *)v104 != 1129663566 )
    {
      v104 += 16;
      if ( v104 == v105 )
        goto LABEL_242;
    }
    v107 = v104 == v105 ? nullptr : *(__int64 **)(v104 + 8);
LABEL_242:
    if ( v107 == nullptr )
      v107 = &qword_141B5A4A0;
    LOBYTE(v12) = 1;
    if ( v100 == (*(unsigned int (__fastcall **)(__int64))(*(_QWORD *)*v107 + 64LL))(*v107) )
LABEL_245:
      LODWORD(v12) = (*(__int64 (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)v94 + 24LL))(v94, v142, v143);
    sub_140835C40(&qword_141B60C30, 1986359923);
    v110 = *a2;
    v111 = a2[1];
    if ( *a2 == v111 )
      goto LABEL_253;
    v112 = nullptr;
    while ( *(_DWORD *)v110 != 1668248696 )
    {
      v110 += 16;
      if ( v110 == v111 )
      {
        v113 = a1;
        goto LABEL_254;
      }
    }
    if ( v110 == v111 )
    {
LABEL_253:
      v113 = a1;
      v112 = nullptr;
    }
    else
    {
      v113 = a1;
      v112 = *(__int64 **)(v110 + 8);
    }
LABEL_254:
    if ( v112 == nullptr )
      v112 = &qword_141B5A4A0;
    v114 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v112 + 176LL))(*v112, v112, 0);
    v115 = v114[1] - *v114;
    if ( v115 != 0 )
    {
      v116 = v115 >> 4;
      v117 = 0;
      do
      {
        sub_140835C40(&qword_141B60C30, *(unsigned int *)(*v114 + v117));
        v117 += 16;
        --v116;
      }
      while ( v116 != 0 );
    }
    if ( (_BYTE)v12 != 0 )
      goto LABEL_260;
    if ( a8 != nullptr )
    {
      v121 = qword_141B60C30;
      v122 = nullptr;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v121 != 1668179565 )
        {
          v121 += 16;
          if ( v121 == qword_141B60C38 )
            goto LABEL_295;
        }
        if ( v121 == qword_141B60C38 )
          v122 = nullptr;
        else
          v122 = *(__int64 **)(v121 + 8);
      }
LABEL_295:
      if ( v122 == nullptr )
        v122 = &qword_141B5A4A0;
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v122 + 128LL))(*v122, &v150);
      v125 = *a8;
      if ( *a8 == v150 )
      {
        if ( v125 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 - 4)) == 0 )
          sub_1412EC9A0(v125 - 4);
      }
      else
      {
        if ( v125 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 - 4)) == 0 )
          sub_1412EC9A0(v125 - 4);
        *a8 = v150;
      }
      if ( a9 == nullptr )
        goto LABEL_320;
    }
    else if ( a9 == nullptr )
    {
      if ( (qword_141B5E4B8 & 0x100000000LL) != 0 )
      {
        v123 = &qword_141B5E4A0;
        while ( 1 )
        {
          v123 = (__int64 *)v123[2];
          if ( v123 == nullptr || *v123 == 0 )
            break;
          if ( (*((_BYTE *)v123 + 28) & 1) == 0 )
            goto LABEL_260;
        }
        v131 = qword_141ABD468;
        v149 = nullptr;
        sub_140809040(&v149, 0x141926836LL, 0xFFFFFFFFLL);
        sub_140824A20(v131, &v150, &v149);
        v132 = v149;
        if ( v149 != nullptr && _InterlockedDecrement(v149 - 1) == 0 )
          sub_1412EC9A0((__int64)(v132 - 1));
        (*(void (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v144 + 200LL))(v144, &v147);
        sub_14081AF20(v147, &v149, &qword_141B59EE0, 0, 0, 0);
        v133 = v147;
        if ( v147 != nullptr && _InterlockedDecrement(v147 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v133)(v133, 1);
        LODWORD(v147) = *(_DWORD *)(v144 + 12);
        sub_14089F940(&v150, &v147);
        sub_140B6A440(&v150, 1, &v149);
        v147 = nullptr;
        sub_14082DAF0(v142, &v147);
        sub_140B6A440(&v150, 2, &v147);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v143 + 128LL))(*v143, &v141);
        sub_140B6A440(&v150, 3, &v141);
        v134 = v141;
        if ( v141 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v141 - 4)) == 0 )
          sub_1412EC9A0(v134 - 4);
        if ( (unsigned __int8)sub_140F49030() != 0 )
        {
          v135 = sub_1407E2C90(2160);
          sub_1407E2EB0(v135, 1099917176, 2766, 1100030485, 0, 1);
          sub_14081ED40(&v150, &v141, 0);
          sub_14080CDB0(v135, &v141);
          v136 = v141;
          if ( v141 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v141 - 4)) == 0 )
            sub_1412EC9A0(v136 - 4);
          if ( (sub_1407E0380(&qword_141B5E4A0, v135) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
            __debugbreak();
        }
        v137 = v147;
        if ( v147 != nullptr && _InterlockedDecrement(v147 - 1) == 0 )
          sub_1412EC9A0((__int64)(v137 - 1));
        v138 = v149;
        if ( v149 != nullptr && _InterlockedDecrement(v149 - 1) == 0 )
          sub_1412EC9A0((__int64)(v138 - 1));
        sub_14081D040(&v150);
      }
LABEL_260:
      if ( v152 == 0 && a11 != 0 && qword_141B5E5D8 != qword_141B5E5D0 )
        sub_14083BFF0(a11, &qword_141B5E5D0);
      if ( v139 != 1 && a12 == 0 && (_BYTE)v12 != 0 && v148 != 0 )
      {
        v118 = *a2;
        v119 = a2[1];
        v120 = nullptr;
        if ( *a2 != v119 )
        {
          while ( *(_DWORD *)v118 != 1230193478 )
          {
            v118 += 16;
            if ( v118 == v119 )
              goto LABEL_289;
          }
          if ( v118 == v119 )
            v120 = nullptr;
          else
            v120 = *(__int64 **)(v118 + 8);
        }
LABEL_289:
        v124 = &qword_141B5A4A0;
        if ( v120 != nullptr )
          v124 = v120;
        LOBYTE(v12) = 1;
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v124 + 48LL))(*v124) != 0
          && *(_BYTE *)(v113 + 1400) != 0 )
        {
          sub_141109FB0(a2);
          sub_14083DC80(&v150, a2);
          sub_14083B5F0(v113 + 1456, &v150);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v150 + 16LL))(v150, &v150);
        }
      }
      return (unsigned int)v12;
    }
    v126 = qword_141B60C30;
    v127 = nullptr;
    if ( qword_141B60C30 != qword_141B60C38 )
    {
      while ( *(_DWORD *)v126 != 1684170098 )
      {
        v126 += 16;
        if ( v126 == qword_141B60C38 )
          goto LABEL_313;
      }
      if ( v126 == qword_141B60C38 )
        v127 = nullptr;
      else
        v127 = *(__int64 **)(v126 + 8);
    }
LABEL_313:
    v128 = &qword_141B5A4A0;
    if ( v127 != nullptr )
      v128 = v127;
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v128 + 128LL))(*v128, &v150);
    v129 = *a9;
    if ( *a9 == v150 )
    {
      if ( v129 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v129 - 4)) == 0 )
        sub_1412EC9A0(v129 - 4);
    }
    else
    {
      if ( v129 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v129 - 4)) == 0 )
        sub_1412EC9A0(v129 - 4);
      *a9 = v150;
    }
  }
  else
  {
LABEL_107:
    LOBYTE(v12) = 1;
    if ( a5 == 0 )
      return (unsigned int)v12;
    if ( (qword_141B5E4B8 & 0x100000000LL) != 0 )
    {
      v57 = &qword_141B5E4A0;
      while ( 1 )
      {
        v57 = (__int64 *)v57[2];
        if ( v57 == nullptr || *v57 == 0 )
          break;
        if ( (*((_BYTE *)v57 + 28) & 1) == 0 )
          goto LABEL_320;
      }
      v82 = qword_141ABD468;
      v149 = nullptr;
      v83 = sub_1412EC810(264, 54);
      *(_QWORD *)v83 = 0x3600000000LL;
      strcpy((char *)(v83 + 8), "Could not find record [%number#1] in table [%number#2]");
      if ( v149 != nullptr )
      {
        v84 = v149 - 1;
        if ( _InterlockedDecrement(v149 - 1) == 0 )
          sub_1412EC9A0((__int64)v84);
      }
      v149 = nullptr;
      _InterlockedIncrement((volatile signed __int32 *)v83);
      v149 = (volatile signed __int32 *)(v83 + 4);
      sub_140824A20(v82, &v150, &v149);
      v85 = v149;
      if ( v149 != nullptr && _InterlockedDecrement(v149 - 1) == 0 )
        sub_1412EC9A0((__int64)(v85 - 1));
      LODWORD(v147) = v145;
      sub_140828CE0(&v149, &v147);
      sub_14081D7C0(&v150, 1, &v149, 0);
      v86 = v149;
      if ( v149 != nullptr && _InterlockedDecrement(v149 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v86)(v86, 1);
      LODWORD(v147) = v21;
      sub_140828CE0(&v149, &v147);
      sub_14081D7C0(&v150, 2, &v149, 0);
      v87 = v149;
      if ( v149 != nullptr && _InterlockedDecrement(v149 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v87)(v87, 1);
      if ( (qword_141B5E4B8 & 0x100000000LL) != 0 && (int)qword_141B5E4B8 <= 1 )
      {
        v88 = &qword_141B5E4A0;
        while ( 1 )
        {
          v88 = (__int64 *)v88[2];
          if ( v88 == nullptr || *v88 == 0 )
            break;
          if ( (*((_BYTE *)v88 + 28) & 1) == 0 || *((int *)v88 + 6) > 1 )
            goto LABEL_238;
        }
        v108 = sub_1407E2C90(2160);
        sub_1407E2EB0(v108, 1099917176, 2809, 1100030485, 0, 1);
        sub_14081ED40(&v150, &v149, 0);
        sub_14080CDB0(v108, &v149);
        v109 = v149;
        if ( v149 != nullptr && _InterlockedDecrement(v149 - 1) == 0 )
          sub_1412EC9A0((__int64)(v109 - 1));
        if ( (sub_1407E0380(&qword_141B5E4A0, v108) & 4) != 0 && (unsigned int)MEMORY[0x1419475E0]() != 0 )
          __debugbreak();
      }
LABEL_238:
      sub_14081D040(&v150);
    }
  }
LABEL_320:
  LODWORD(v12) = 0;
  return (unsigned int)v12;
}
