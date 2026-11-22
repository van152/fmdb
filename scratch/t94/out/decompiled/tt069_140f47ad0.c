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
  _QWORD *v12; // rsi
  __int64 v17; // rax
  __int64 v18; // rcx
  _QWORD *v19; // rdx
  _QWORD *v20; // rdi
  unsigned int v21; // r12d
  __int64 v22; // rcx
  __int64 v23; // rdx
  _QWORD *v24; // rax
  _QWORD *v25; // rdx
  __int64 v26; // rax
  __int64 v27; // rcx
  void *v28; // rdx
  __int64 v29; // rax
  __int64 v30; // rcx
  __int64 v31; // rdx
  _QWORD *v32; // rdx
  __int64 v33; // rax
  __int64 v34; // rcx
  bool v35; // zf
  _QWORD *v36; // rdx
  __int64 v37; // rbx
  __int64 v38; // rcx
  _QWORD *v39; // rdx
  __int64 v40; // rax
  _QWORD *v41; // rdx
  _QWORD *v42; // rax
  __int64 v43; // rax
  __int64 v44; // rax
  __int64 v45; // rax
  __int64 v46; // rbx
  __int64 v47; // rax
  __int64 v48; // rax
  __int64 v49; // rax
  unsigned __int64 v50; // rsi
  __int64 v51; // rax
  __int64 v52; // rax
  __int64 v53; // rax
  __int64 v54; // rcx
  _QWORD *v55; // rax
  __int64 *v56; // rsi
  __int64 *v57; // rsi
  bool v58; // si
  __int64 v59; // rax
  __int64 v60; // rax
  __int64 v61; // rax
  __int64 v62; // rax
  char v63; // bl
  __int64 *v64; // rsi
  __int64 *v65; // rsi
  __int64 v66; // rax
  __int64 v67; // rcx
  __int64 v68; // rax
  __int64 v69; // rax
  __int64 v70; // rcx
  __int64 v71; // rax
  __int64 v72; // rax
  __int64 v73; // rcx
  _QWORD *v74; // rdx
  __int64 *v75; // rsi
  __int64 *v76; // rsi
  __int64 v77; // rsi
  __int64 v78; // rdi
  __int64 v79; // rcx
  __int64 v80; // rcx
  void (__fastcall ***v81)(_QWORD, __int64); // rcx
  void (__fastcall ***v82)(_QWORD, __int64); // rcx
  _QWORD *v83; // rax
  __int64 v84; // rax
  __int64 v85; // rax
  __int64 v86; // rsi
  unsigned __int64 v87; // rsi
  __int64 v88; // rax
  __int64 v89; // rbx
  __int64 v90; // r13
  _QWORD *v91; // rbx
  _QWORD *v92; // rdi
  __int64 v93; // rdi
  int *v94; // rax
  int v95; // edi
  __int64 v96; // rax
  __int64 v97; // rcx
  _QWORD *v98; // rdx
  __int64 v99; // rax
  __int64 v100; // rcx
  __int64 v101; // rdx
  _QWORD *v102; // rdx
  __int64 v103; // rsi
  __int64 v104; // rcx
  __int64 v105; // rax
  __int64 v106; // rcx
  _QWORD *v107; // rdx
  __int64 v108; // r12
  _QWORD *v109; // rdi
  __int64 v110; // r15
  __int64 v111; // r15
  __int64 v112; // rbx
  __int64 v113; // rcx
  __int64 v114; // rdx
  _QWORD *v115; // rax
  __int64 v116; // rax
  _QWORD *v117; // r8
  _QWORD *v118; // rax
  _QWORD *v119; // rdx
  __int64 v120; // rcx
  __int64 v121; // rcx
  _QWORD *v122; // rax
  _QWORD *v123; // r8
  __int64 v124; // rcx
  __int64 v126; // rdi
  __int64 v127; // rcx
  void (__fastcall ***v128)(_QWORD, __int64); // rcx
  __int64 v129; // rcx
  __int64 v130; // rdi
  __int64 v131; // rcx
  __int64 v132; // rcx
  __int64 v133; // rcx
  int v134; // [rsp+20h] [rbp-60h]
  unsigned int v135; // [rsp+38h] [rbp-48h]
  char v136; // [rsp+44h] [rbp-3Ch]
  __int64 v137; // [rsp+48h] [rbp-38h] BYREF
  __int64 v138; // [rsp+50h] [rbp-30h]
  _QWORD *v139; // [rsp+58h] [rbp-28h]
  __int64 v140; // [rsp+60h] [rbp-20h]
  unsigned int v141; // [rsp+68h] [rbp-18h] BYREF
  unsigned int v142; // [rsp+6Ch] [rbp-14h]
  __int64 v143; // [rsp+70h] [rbp-10h] BYREF
  char v144; // [rsp+7Fh] [rbp-1h]
  __int64 v145; // [rsp+80h] [rbp+0h] BYREF
  __int64 v146; // [rsp+88h] [rbp+8h] BYREF
  unsigned __int64 v147; // [rsp+90h] [rbp+10h]
  char v148; // [rsp+AFh] [rbp+2Fh]
  __int64 v149; // [rsp+B0h] [rbp+30h]

  v149 = -2;
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
      v19 = *(_QWORD **)(v17 + 8);
  }
LABEL_8:
  v20 = &unk_141B5A4A0;
  if ( v19 == nullptr )
    v19 = &unk_141B5A4A0;
  v21 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v19 + 64LL))(*v19);
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
        v24 = *(_QWORD **)(v22 + 8);
    }
LABEL_18:
    v25 = &unk_141B5A4A0;
    if ( v24 != nullptr )
      v25 = v24;
    LOBYTE(v12) = 1;
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)*v25 + 48LL))(*v25) == 0
      || v21 == 1 && byte_141B60320 == 0 )
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
      v28 = *(void **)(v26 + 8);
  }
LABEL_30:
  if ( v28 == nullptr )
    v28 = &unk_141B5A4A0;
  ((void (__fastcall *)(unsigned int *, void *))unk_140FE3720)(&v141, v28);
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
        v32 = *(_QWORD **)(v29 + 8);
LABEL_48:
      if ( v32 == nullptr )
        v32 = &unk_141B5A4A0;
      LODWORD(v12) = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v32 + 48LL))(*v32);
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
  v148 = a3;
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
    v36 = *(_QWORD **)(v33 + 8);
LABEL_62:
  if ( v36 == nullptr )
    v36 = &unk_141B5A4A0;
  v138 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v36 + 80LL))(*v36);
  v37 = *a2;
  v38 = a2[1];
  v136 = (char)v12;
  if ( *a2 == v38 )
  {
    v41 = nullptr;
    v139 = &unk_141B5A4A0;
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
      v39 = *(_QWORD **)(v40 + 8);
LABEL_73:
    v42 = &unk_141B5A4A0;
    if ( v39 != nullptr )
      v42 = v39;
    v139 = v42;
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
      v41 = *(_QWORD **)(v37 + 8);
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
  if ( v43 == qword_141B60C38 || (v12 = *(_QWORD **)(v43 + 8)) == nullptr )
  {
LABEL_87:
    ((void (__fastcall *)(__int64 *, __int64, _QWORD *))unk_140835A40)(&qword_141B60C30, 1986359923, v20);
  }
  else if ( v12 != v20 )
  {
    (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v12 + 16LL))(*v12, v12);
    (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*v20 + 24LL))(*v20, v20, v12);
  }
  v44 = sub_140E78A80();
  ((void (__fastcall *)(__int64, _QWORD, _QWORD, __int64, _QWORD *))unk_140FF58B0)(v44, v21, v141, v138, v139);
  v45 = ((__int64 (__fastcall *)(__int64, _QWORD))unk_140F216C0)(a1, v21);
  if ( v45 == 0 )
    goto LABEL_107;
  v12 = (_QWORD *)v45;
  v46 = (*(__int64 (__fastcall **)(__int64, unsigned int *))(*(_QWORD *)v45 + 32LL))(v45, &v141);
  if ( v21 == 55 && (*(__int64 (__fastcall **)(_QWORD *))(*v12 + 48LL))(v12) != 0 )
    v46 = (*(__int64 (__fastcall **)(_QWORD *, _QWORD))(*v12 + 16LL))(v12, 0);
  if ( v46 != 0 )
  {
    if ( a10 != 0 )
    {
      v47 = ((__int64 (*)(void))unk_14083D4F0)();
      LODWORD(v147) = 3569;
      v146 = v47 + 40;
      sub_140835380(a2, 1986359923, &v146);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    }
    v48 = ((__int64 (*)(void))unk_14083D4F0)();
    LODWORD(v147) = v21;
    v146 = v48 + 40;
    v49 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_98;
    while ( *(_DWORD *)v49 != 1685353593 )
    {
      v49 += 16;
      if ( v49 == qword_141B60C38 )
        goto LABEL_98;
    }
    if ( v49 == qword_141B60C38 || (v56 = *(__int64 **)(v49 + 8)) == nullptr )
    {
LABEL_98:
      ((void (__fastcall *)(__int64 *, __int64, __int64 *))unk_140835A40)(&qword_141B60C30, 1685353593, &v146);
    }
    else if ( v56 != &v146 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v56 + 16LL))(*v56, v56);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v146 + 24LL))(v146, &v146, v56);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    v50 = ((unsigned __int64)v142 << 32) | (int)v141;
    v51 = ((__int64 (*)(void))unk_14083D4F0)();
    v147 = v50;
    v146 = v51 + 72;
    v52 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_102;
    while ( *(_DWORD *)v52 != 1685417577 )
    {
      v52 += 16;
      if ( v52 == qword_141B60C38 )
        goto LABEL_102;
    }
    if ( v52 == qword_141B60C38 || (v57 = *(__int64 **)(v52 + 8)) == nullptr )
    {
LABEL_102:
      ((void (__fastcall *)(__int64 *, __int64, __int64 *))unk_140835A40)(&qword_141B60C30, 1685417577, &v146);
    }
    else if ( v57 != &v146 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v57 + 16LL))(*v57, v57);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v146 + 24LL))(v146, &v146, v57);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    v53 = *a2;
    v54 = a2[1];
    if ( *a2 == v54 )
      goto LABEL_128;
    while ( *(_DWORD *)v53 != 1986359923 )
    {
      v53 += 16;
      if ( v53 == v54 )
        goto LABEL_128;
    }
    if ( v53 == v54 )
LABEL_128:
      v58 = false;
    else
      v58 = *(_QWORD *)(v53 + 8) != 0;
    v59 = ((__int64 (*)(void))unk_14083D4F0)();
    LOBYTE(v147) = !v58;
    v146 = v59 + 24;
    v60 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_132;
    while ( *(_DWORD *)v60 != 1766410053 )
    {
      v60 += 16;
      if ( v60 == qword_141B60C38 )
        goto LABEL_132;
    }
    if ( v60 == qword_141B60C38 || (v64 = *(__int64 **)(v60 + 8)) == nullptr )
    {
LABEL_132:
      ((void (__fastcall *)(__int64 *, __int64, __int64 *))unk_140835A40)(&qword_141B60C30, 1766410053, &v146);
    }
    else if ( v64 != &v146 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v64 + 16LL))(*v64, v64);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v146 + 24LL))(v146, &v146, v64);
    }
    v140 = v46;
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    v61 = ((__int64 (*)(void))unk_14083D4F0)();
    LOBYTE(v147) = a7;
    v146 = v61 + 24;
    v62 = qword_141B60C30;
    v63 = v148;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_145;
    while ( *(_DWORD *)v62 != 1668178792 )
    {
      v62 += 16;
      if ( v62 == qword_141B60C38 )
        goto LABEL_145;
    }
    if ( v62 == qword_141B60C38 || (v65 = *(__int64 **)(v62 + 8)) == nullptr )
    {
LABEL_145:
      ((void (__fastcall *)(__int64 *, __int64, __int64 *))unk_140835A40)(&qword_141B60C30, 1668178792, &v146);
    }
    else if ( v65 != &v146 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v65 + 16LL))(*v65, v65);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v146 + 24LL))(v146, &v146, v65);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    v66 = ((__int64 (*)(void))unk_14083D4F0)();
    v147 = 0;
    v67 = qword_141B59EE0;
    if ( qword_141B59EE0 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
    v147 = v67;
    v146 = v66 + 136;
    v68 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_151;
    while ( *(_DWORD *)v68 != 1668179565 )
    {
      v68 += 16;
      if ( v68 == qword_141B60C38 )
        goto LABEL_151;
    }
    if ( v68 == qword_141B60C38 || (v75 = *(__int64 **)(v68 + 8)) == nullptr )
    {
LABEL_151:
      ((void (__fastcall *)(__int64 *, __int64, __int64 *))unk_140835A40)(&qword_141B60C30, 1668179565, &v146);
    }
    else if ( v75 != &v146 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v75 + 16LL))(*v75, v75);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v146 + 24LL))(v146, &v146, v75);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    v69 = ((__int64 (*)(void))unk_14083D4F0)();
    v147 = 0;
    v70 = qword_141B59EE0;
    if ( qword_141B59EE0 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
    v147 = v70;
    v146 = v69 + 136;
    v71 = qword_141B60C30;
    if ( qword_141B60C30 == qword_141B60C38 )
      goto LABEL_157;
    while ( *(_DWORD *)v71 != 1684170098 )
    {
      v71 += 16;
      if ( v71 == qword_141B60C38 )
        goto LABEL_157;
    }
    if ( v71 == qword_141B60C38 || (v76 = *(__int64 **)(v71 + 8)) == nullptr )
    {
LABEL_157:
      ((void (__fastcall *)(__int64 *, __int64, __int64 *))unk_140835A40)(&qword_141B60C30, 1684170098, &v146);
    }
    else if ( v76 != &v146 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v76 + 16LL))(*v76, v76);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v146 + 24LL))(v146, &v146, v76);
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    v72 = *a2;
    v73 = a2[1];
    v74 = nullptr;
    if ( *a2 != v73 )
    {
      while ( *(_DWORD *)v72 != 1668248696 )
      {
        v72 += 16;
        if ( v72 == v73 )
          goto LABEL_193;
      }
      if ( v72 == v73 )
        v74 = nullptr;
      else
        v74 = *(_QWORD **)(v72 + 8);
    }
LABEL_193:
    if ( v74 == nullptr )
      v74 = &unk_141B5A4A0;
    v84 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*v74 + 176LL))(*v74, v74, 0);
    sub_1408350B0(&qword_141B60C30, v84);
    if ( v142 == 0 )
    {
      v85 = *(int *)(v140 + 12);
      v141 = *(_DWORD *)(v140 + 12);
      v86 = *(unsigned int *)(v140 + 16);
      if ( (_DWORD)v86 == 0 )
        v86 = (unsigned int)v85;
      v142 = v86;
      v87 = v85 | (v86 << 32);
      v88 = ((__int64 (*)(void))unk_14083D4F0)();
      v147 = v87;
      v146 = v88 + 72;
      sub_140835380(a2, 1685417577, &v146);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
    }
    if ( dword_141B5E5E8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      ((void (__fastcall *)(int *))unk_141750E08)(&dword_141B5E5E8);
      if ( dword_141B5E5E8 == -1 )
      {
        ((void (__fastcall *)(__int64 *))unk_1407C9510)(&qword_141B5E5D0);
        ((void (__fastcall *)(void *))unk_141751048)(&unk_140F49020);
        ((void (__fastcall *)(int *))unk_141750EA0)(&dword_141B5E5E8);
      }
    }
    v135 = v21;
    v144 = a4;
    if ( v63 != 0 )
    {
      v12 = &v146;
      sub_14083DC80(&v146, a2);
      sub_14083B5F0(&qword_141B5E5D0, &v146);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
      v89 = v140;
    }
    else
    {
      v12 = (_QWORD *)qword_141B5E5D8;
      v90 = qword_141B5E5D0;
      v89 = v140;
      if ( qword_141B5E5D0 != qword_141B5E5D8 )
      {
        v91 = (_QWORD *)qword_141B5E5D0;
        do
        {
          v92 = (_QWORD *)*v91;
          if ( *v91 != 0 )
          {
            (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v92 + 16LL))(*v92, *v91);
            sub_1408B5E70(v92);
          }
          ++v91;
        }
        while ( v91 != v12 );
        v93 = qword_141B5E5D8 - (_QWORD)v12;
        ((void (__fastcall *)(__int64, _QWORD *, __int64))unk_141758A00)(v90, v12, qword_141B5E5D8 - (_QWORD)v12);
        qword_141B5E5D8 = v90 + v93;
        v89 = v140;
      }
    }
    *(_BYTE *)(a1 + 1484) = v136;
    v94 = *(int **)(a1 + 1344);
    if ( v94 == *(int **)(a1 + 1352) )
      v95 = -1;
    else
      v95 = *v94;
    v96 = *a2;
    v97 = a2[1];
    v98 = nullptr;
    if ( *a2 != v97 )
    {
      while ( *(_DWORD *)v96 != 1230195782 )
      {
        v96 += 16;
        if ( v96 == v97 )
          goto LABEL_218;
      }
      if ( v96 == v97 )
        v98 = nullptr;
      else
        v98 = *(_QWORD **)(v96 + 8);
    }
LABEL_218:
    if ( v98 == nullptr )
      v98 = &unk_141B5A4A0;
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)*v98 + 48LL))(*v98) == 0 )
      goto LABEL_245;
    v99 = *a2;
    v100 = a2[1];
    if ( *a2 == v100 )
      goto LABEL_245;
    v101 = *a2;
    while ( *(_DWORD *)v101 != 1129663566 )
    {
      v101 += 16;
      if ( v101 == v100 )
        goto LABEL_245;
    }
    if ( v101 == v100 || *(_QWORD *)(v101 + 8) == 0 )
      goto LABEL_245;
    v102 = nullptr;
    while ( *(_DWORD *)v99 != 1129663566 )
    {
      v99 += 16;
      if ( v99 == v100 )
        goto LABEL_242;
    }
    v102 = v99 == v100 ? nullptr : *(_QWORD **)(v99 + 8);
LABEL_242:
    if ( v102 == nullptr )
      v102 = &unk_141B5A4A0;
    LOBYTE(v12) = 1;
    if ( v95 == (*(unsigned int (__fastcall **)(_QWORD))(*(_QWORD *)*v102 + 64LL))(*v102) )
LABEL_245:
      LODWORD(v12) = (*(__int64 (__fastcall **)(__int64, __int64, _QWORD *))(*(_QWORD *)v89 + 24LL))(v89, v138, v139);
    ((void (__fastcall *)(__int64 *, __int64))unk_140835C40)(&qword_141B60C30, 1986359923);
    v105 = *a2;
    v106 = a2[1];
    if ( *a2 == v106 )
      goto LABEL_253;
    v107 = nullptr;
    while ( *(_DWORD *)v105 != 1668248696 )
    {
      v105 += 16;
      if ( v105 == v106 )
      {
        v108 = a1;
        goto LABEL_254;
      }
    }
    if ( v105 == v106 )
    {
LABEL_253:
      v108 = a1;
      v107 = nullptr;
    }
    else
    {
      v108 = a1;
      v107 = *(_QWORD **)(v105 + 8);
    }
LABEL_254:
    if ( v107 == nullptr )
      v107 = &unk_141B5A4A0;
    v109 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*v107 + 176LL))(*v107, v107, 0);
    v110 = v109[1] - *v109;
    if ( v110 != 0 )
    {
      v111 = v110 >> 4;
      v112 = 0;
      do
      {
        ((void (__fastcall *)(__int64 *, _QWORD))unk_140835C40)(&qword_141B60C30, *(unsigned int *)(*v109 + v112));
        v112 += 16;
        --v111;
      }
      while ( v111 != 0 );
    }
    if ( (_BYTE)v12 != 0 )
      goto LABEL_260;
    if ( a8 != nullptr )
    {
      v116 = qword_141B60C30;
      v117 = nullptr;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v116 != 1668179565 )
        {
          v116 += 16;
          if ( v116 == qword_141B60C38 )
            goto LABEL_295;
        }
        if ( v116 == qword_141B60C38 )
          v117 = nullptr;
        else
          v117 = *(_QWORD **)(v116 + 8);
      }
LABEL_295:
      if ( v117 == nullptr )
        v117 = &unk_141B5A4A0;
      (*(void (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)*v117 + 128LL))(*v117, &v146);
      v120 = *a8;
      if ( *a8 == v146 )
      {
        if ( v120 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v120 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v120 - 4);
      }
      else
      {
        if ( v120 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v120 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v120 - 4);
        *a8 = v146;
      }
      if ( a9 == nullptr )
        goto LABEL_320;
    }
    else if ( a9 == nullptr )
    {
      if ( (byte_141B5E4BC & 1) != 0 )
      {
        v118 = &unk_141B5E4A0;
        while ( 1 )
        {
          v118 = (_QWORD *)v118[2];
          if ( v118 == nullptr || *v118 == 0 )
            break;
          if ( (*((_BYTE *)v118 + 28) & 1) == 0 )
            goto LABEL_260;
        }
        v126 = qword_141ABD468;
        v145 = 0;
        sub_140809040(&v145, 0x141926836LL, 0xFFFFFFFFLL);
        ((void (__fastcall *)(__int64, __int64 *, __int64 *))unk_140824A20)(v126, &v146, &v145);
        v127 = v145;
        if ( v145 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v145 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v127 - 4);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v140 + 200LL))(v140, &v143);
        LOBYTE(v134) = 0;
        sub_14081AF20(v143, &v145, &qword_141B59EE0, 0, v134, 0);
        v128 = (void (__fastcall ***)(_QWORD, __int64))v143;
        if ( v143 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v143 + 8)) == 0 )
          (**v128)(v128, 1);
        LODWORD(v143) = *(_DWORD *)(v140 + 12);
        sub_14089F940(&v146, &v143);
        sub_140B6A440(&v146, 1, &v145);
        v143 = 0;
        sub_14082DAF0(v138, &v143);
        sub_140B6A440(&v146, 2, &v143);
        (*(void (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)*v139 + 128LL))(*v139, &v137);
        sub_140B6A440(&v146, 3, &v137);
        v129 = v137;
        if ( v137 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v137 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v129 - 4);
        if ( (unsigned __int8)((__int64 (*)(void))unk_140F49030)() != 0 )
        {
          v130 = ((__int64 (__fastcall *)(__int64))unk_1407E2C90)(2160);
          ((void (__fastcall *)(__int64, __int64, __int64, __int64, _DWORD, int))unk_1407E2EB0)(
            v130,
            0x1418F6778LL,
            2766,
            0x141912215LL,
            0,
            1);
          ((void (__fastcall *)(__int64 *, __int64 *, _QWORD))unk_14081ED40)(&v146, &v137, 0);
          ((void (__fastcall *)(__int64, __int64 *))unk_14080CDB0)(v130, &v137);
          v131 = v137;
          if ( v137 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v137 - 4)) == 0 )
            ((void (__fastcall *)(__int64))unk_1412EC9A0)(v131 - 4);
          if ( (((__int64 (__fastcall *)(void *, __int64))unk_1407E0380)(&unk_141B5E4A0, v130) & 4) != 0
            && (unsigned int)MEMORY[0x1419475E0]() != 0 )
          {
            __debugbreak();
          }
        }
        v132 = v143;
        if ( v143 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v143 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v132 - 4);
        v133 = v145;
        if ( v145 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v145 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v133 - 4);
        ((void (__fastcall *)(__int64 *))unk_14081D040)(&v146);
      }
LABEL_260:
      if ( v148 == 0 && a11 != 0 && qword_141B5E5D8 != qword_141B5E5D0 )
        sub_14083BFF0(a11, &qword_141B5E5D0);
      if ( v135 != 1 && a12 == 0 && (_BYTE)v12 != 0 && v144 != 0 )
      {
        v113 = *a2;
        v114 = a2[1];
        v115 = nullptr;
        if ( *a2 != v114 )
        {
          while ( *(_DWORD *)v113 != 1230193478 )
          {
            v113 += 16;
            if ( v113 == v114 )
              goto LABEL_289;
          }
          if ( v113 == v114 )
            v115 = nullptr;
          else
            v115 = *(_QWORD **)(v113 + 8);
        }
LABEL_289:
        v119 = &unk_141B5A4A0;
        if ( v115 != nullptr )
          v119 = v115;
        LOBYTE(v12) = 1;
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)*v119 + 48LL))(*v119) != 0
          && *(_BYTE *)(v108 + 1400) != 0 )
        {
          sub_141109FB0(a2);
          sub_14083DC80(&v146, a2);
          sub_14083B5F0(v108 + 1456, &v146);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v146 + 16LL))(v146, &v146);
        }
      }
      return (unsigned int)v12;
    }
    v121 = qword_141B60C30;
    v122 = nullptr;
    if ( qword_141B60C30 != qword_141B60C38 )
    {
      while ( *(_DWORD *)v121 != 1684170098 )
      {
        v121 += 16;
        if ( v121 == qword_141B60C38 )
          goto LABEL_313;
      }
      if ( v121 == qword_141B60C38 )
        v122 = nullptr;
      else
        v122 = *(_QWORD **)(v121 + 8);
    }
LABEL_313:
    v123 = &unk_141B5A4A0;
    if ( v122 != nullptr )
      v123 = v122;
    (*(void (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)*v123 + 128LL))(*v123, &v146);
    v124 = *a9;
    if ( *a9 == v146 )
    {
      if ( v124 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v124 - 4)) == 0 )
        ((void (__fastcall *)(__int64))unk_1412EC9A0)(v124 - 4);
    }
    else
    {
      if ( v124 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v124 - 4)) == 0 )
        ((void (__fastcall *)(__int64))unk_1412EC9A0)(v124 - 4);
      *a9 = v146;
    }
  }
  else
  {
LABEL_107:
    LOBYTE(v12) = 1;
    if ( a5 == 0 )
      return (unsigned int)v12;
    if ( (byte_141B5E4BC & 1) != 0 )
    {
      v55 = &unk_141B5E4A0;
      while ( 1 )
      {
        v55 = (_QWORD *)v55[2];
        if ( v55 == nullptr || *v55 == 0 )
          break;
        if ( (*((_BYTE *)v55 + 28) & 1) == 0 )
          goto LABEL_320;
      }
      v77 = qword_141ABD468;
      v145 = 0;
      v78 = ((__int64 (__fastcall *)(__int64, __int64))unk_1412EC810)(264, 54);
      *(_QWORD *)v78 = 0x3600000000LL;
      strcpy((char *)(v78 + 8), "Could not find record [%number#1] in table [%number#2]");
      if ( v145 != 0 )
      {
        v79 = v145 - 4;
        if ( _InterlockedDecrement((volatile signed __int32 *)(v145 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v79);
      }
      v145 = 0;
      _InterlockedIncrement((volatile signed __int32 *)v78);
      v145 = v78 + 4;
      ((void (__fastcall *)(__int64, __int64 *, __int64 *))unk_140824A20)(v77, &v146, &v145);
      v80 = v145;
      if ( v145 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v145 - 4)) == 0 )
        ((void (__fastcall *)(__int64))unk_1412EC9A0)(v80 - 4);
      LODWORD(v143) = v141;
      sub_140828CE0(&v145, &v143);
      ((void (__fastcall *)(__int64 *, __int64, __int64 *, _QWORD))unk_14081D7C0)(&v146, 1, &v145, 0);
      v81 = (void (__fastcall ***)(_QWORD, __int64))v145;
      if ( v145 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v145 + 8)) == 0 )
        (**v81)(v81, 1);
      LODWORD(v143) = v21;
      sub_140828CE0(&v145, &v143);
      ((void (__fastcall *)(__int64 *, __int64, __int64 *, _QWORD))unk_14081D7C0)(&v146, 2, &v145, 0);
      v82 = (void (__fastcall ***)(_QWORD, __int64))v145;
      if ( v145 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v145 + 8)) == 0 )
        (**v82)(v82, 1);
      if ( (byte_141B5E4BC & 1) != 0 && dword_141B5E4B8 <= 1 )
      {
        v83 = &unk_141B5E4A0;
        while ( 1 )
        {
          v83 = (_QWORD *)v83[2];
          if ( v83 == nullptr || *v83 == 0 )
            break;
          if ( (*((_BYTE *)v83 + 28) & 1) == 0 || *((int *)v83 + 6) > 1 )
            goto LABEL_238;
        }
        v103 = ((__int64 (__fastcall *)(__int64))unk_1407E2C90)(2160);
        ((void (__fastcall *)(__int64, __int64, __int64, __int64, _DWORD, int))unk_1407E2EB0)(
          v103,
          0x1418F6778LL,
          2809,
          0x141912215LL,
          0,
          1);
        ((void (__fastcall *)(__int64 *, __int64 *, _QWORD))unk_14081ED40)(&v146, &v145, 0);
        ((void (__fastcall *)(__int64, __int64 *))unk_14080CDB0)(v103, &v145);
        v104 = v145;
        if ( v145 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v145 - 4)) == 0 )
          ((void (__fastcall *)(__int64))unk_1412EC9A0)(v104 - 4);
        if ( (((__int64 (__fastcall *)(void *, __int64))unk_1407E0380)(&unk_141B5E4A0, v103) & 4) != 0
          && (unsigned int)MEMORY[0x1419475E0]() != 0 )
        {
          __debugbreak();
        }
      }
LABEL_238:
      ((void (__fastcall *)(__int64 *))unk_14081D040)(&v146);
    }
  }
LABEL_320:
  LODWORD(v12) = 0;
  return (unsigned int)v12;
}
