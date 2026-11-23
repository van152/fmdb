bool __fastcall sub_141026FD0(__int64 a1, _QWORD *a2, __int64 **a3)
{
  _QWORD *v3; // rdi
  __int64 v4; // rax
  char v7; // al
  __int64 *v8; // rcx
  __int64 v9; // r9
  __int64 v10; // rax
  _QWORD **v11; // rdi
  _QWORD **v12; // r14
  __int64 v13; // rsi
  _QWORD *v14; // rax
  __int64 v15; // rcx
  __int64 v16; // rbx
  __int64 v17; // rax
  char v18; // dl
  __int64 v19; // rax
  __int64 v20; // rax
  __int64 v21; // rax
  __int64 v22; // rax
  __int64 *v23; // r13
  _QWORD *v24; // rsi
  __int64 v25; // r12
  __int64 *v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rcx
  __int64 *v29; // rdx
  __int64 v30; // rax
  __int64 v31; // rcx
  __int64 v32; // r13
  __int64 *v33; // rdx
  _QWORD *v34; // rax
  __int64 v35; // rax
  __int64 *v36; // rdx
  __int64 v37; // rax
  __int64 *v38; // rdx
  unsigned __int8 v39; // bl
  char v40; // al
  __int64 *v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rcx
  __int64 v44; // r14
  _QWORD **v45; // r14
  _QWORD **v46; // r12
  __int64 *v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rax
  __int64 *v50; // rbx
  char v51; // r12
  bool v52; // zf
  int v53; // edx
  int v54; // eax
  int v55; // r9d
  int v56; // r9d
  int v57; // ecx
  int v58; // eax
  int v59; // ecx
  int v60; // ebx
  _DWORD *v61; // rcx
  _DWORD *v62; // rcx
  __int64 *v63; // rbx
  int v64; // ebx
  __int64 v65; // rcx
  __int64 v66; // rax
  __int64 *v67; // rcx
  __int64 v68; // rax
  __int64 v69; // rdx
  int v70; // ebx
  __int64 v71; // rcx
  __int64 v72; // rax
  bool v73; // bl
  __int64 v74; // rax
  __int64 v75; // rcx
  __int64 v76; // rdx
  __int64 v77; // rdx
  __int64 *v78; // rbx
  __int64 v79; // rbx
  _QWORD *v80; // rbx
  __int64 *v81; // rsi
  __int64 v83; // [rsp+38h] [rbp-48h]
  __int64 v84; // [rsp+40h] [rbp-40h]
  _DWORD *v85; // [rsp+48h] [rbp-38h] BYREF
  _DWORD *v86; // [rsp+50h] [rbp-30h] BYREF
  __int64 v87; // [rsp+58h] [rbp-28h]
  _QWORD *v88; // [rsp+60h] [rbp-20h]
  _QWORD **v89; // [rsp+68h] [rbp-18h] BYREF
  _QWORD **v90; // [rsp+70h] [rbp-10h]
  __int64 v91; // [rsp+80h] [rbp+0h] BYREF
  __int64 v92; // [rsp+88h] [rbp+8h] BYREF
  _QWORD **v93; // [rsp+98h] [rbp+18h] BYREF
  _QWORD **v94; // [rsp+A0h] [rbp+20h]
  _QWORD v95[2]; // [rsp+B0h] [rbp+30h] BYREF
  __int128 v96; // [rsp+C0h] [rbp+40h] BYREF
  __int64 v97; // [rsp+D0h] [rbp+50h]
  _QWORD v98[2]; // [rsp+E0h] [rbp+60h] BYREF
  int v99; // [rsp+F0h] [rbp+70h]
  __int16 v100; // [rsp+F4h] [rbp+74h]
  _QWORD **v101; // [rsp+F8h] [rbp+78h]
  __int128 v102; // [rsp+100h] [rbp+80h] BYREF
  __int64 v103; // [rsp+110h] [rbp+90h]
  __int64 *v104; // [rsp+118h] [rbp+98h] BYREF
  int v105; // [rsp+120h] [rbp+A0h]
  int v106; // [rsp+128h] [rbp+A8h]
  __int16 v107; // [rsp+12Ch] [rbp+ACh]
  unsigned __int8 v108; // [rsp+137h] [rbp+B7h]
  __int64 v109; // [rsp+138h] [rbp+B8h]

  v109 = -2;
  v3 = a2;
  v4 = *(_QWORD *)(a1 + 816);
  if ( a2 == nullptr || v4 == 0 )
    return v3 != nullptr && v4 != 0;
  v84 = *(_QWORD *)(a1 + 816);
  sub_1407C9510(&v89);
  v7 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
  v8 = *a3;
  v9 = **a3;
  v88 = v3;
  v87 = a1;
  if ( v7 == 11 )
  {
    v10 = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v9 + 184))(v8, a3, 0);
    sub_14083BFF0(&v89, v10);
  }
  else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v9 + 8))(v8, a3) != 0 )
  {
    sub_14083B2B0(&v89, a3);
  }
  v11 = v89;
  v12 = v90;
  if ( v89 == v90 )
    goto LABEL_199;
  v13 = 0;
  do
  {
    v14 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, _QWORD, _QWORD))(*(_QWORD *)**v11 + 176LL))(**v11, *v11, 0);
    v96 = 0;
    v97 = 0;
    sub_1408367A0(&v96, (__int64)(v14[1] - *v14) >> 4, v14, v14 + 1);
    v15 = *((_QWORD *)&v96 + 1);
    v16 = v96;
    if ( (_QWORD)v96 == *((_QWORD *)&v96 + 1) )
      goto LABEL_18;
    v17 = v96;
    while ( *(_DWORD *)v17 != 1853122419 )
    {
      v17 += 16;
      if ( v17 == *((_QWORD *)&v96 + 1) )
        goto LABEL_18;
    }
    if ( v17 == *((_QWORD *)&v96 + 1) || (v18 = 1, *(_QWORD *)(v17 + 8) == 0) )
    {
LABEL_18:
      sub_14083DA80(&v91, &qword_141B5A470);
      sub_140835380((__int64 *)&v96, 1853122419, &v91);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v91 + 16LL))(v91, &v91);
      v15 = *((_QWORD *)&v96 + 1);
      v16 = v96;
      v18 = 0;
      if ( (_QWORD)v96 == *((_QWORD *)&v96 + 1) )
        goto LABEL_29;
    }
    else if ( (_QWORD)v96 == *((_QWORD *)&v96 + 1) )
    {
      goto LABEL_29;
    }
    v19 = v16;
    while ( *(_DWORD *)v19 != 1852797554 )
    {
      v19 += 16;
      if ( v19 == v15 )
        goto LABEL_29;
    }
    if ( v19 == v15 || *(_QWORD *)(v19 + 8) == 0 )
    {
LABEL_29:
      v21 = sub_14083D4F0(v15);
      LODWORD(v92) = 1852797541;
      v91 = v21 + 56;
      sub_140835380((__int64 *)&v96, 1852797554, &v91);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v91 + 16LL))(v91, &v91);
      v15 = *((_QWORD *)&v96 + 1);
      v16 = v96;
      if ( (_QWORD)v96 != *((_QWORD *)&v96 + 1) )
      {
        v22 = v96;
        while ( *(_DWORD *)v22 != 1852797540 )
        {
          v22 += 16;
          if ( v22 == *((_QWORD *)&v96 + 1) )
            goto LABEL_42;
        }
        if ( v22 != *((_QWORD *)&v96 + 1) && *(_QWORD *)(v22 + 8) != 0 )
          goto LABEL_49;
LABEL_42:
        while ( v16 != v15 )
        {
          if ( *(_DWORD *)v16 == 1852797540 )
          {
            if ( v16 == v15 )
              break;
            v23 = *(__int64 **)(v16 + 8);
            if ( v23 == nullptr )
              break;
            if ( v23 != &qword_141B5A4A0 )
            {
              (*(void (__fastcall **)(__int64, _QWORD))(*(_QWORD *)*v23 + 16LL))(*v23, *(_QWORD *)(v16 + 8));
              (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                qword_141B5A4A0,
                &qword_141B5A4A0,
                v23);
            }
            goto LABEL_49;
          }
          v16 += 16;
        }
      }
      sub_140835A40(&v96, 1852797540, &qword_141B5A4A0);
LABEL_49:
      sub_14083DC80(&v91, &v96);
      sub_14083BE60(&v89, &v91, v13);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v91 + 16LL))(v91, &v91);
      goto LABEL_50;
    }
    v20 = v16;
    while ( *(_DWORD *)v20 != 1852797540 )
    {
      v20 += 16;
      if ( v20 == v15 )
        goto LABEL_42;
    }
    if ( v20 == v15 || *(_QWORD *)(v20 + 8) == 0 )
      goto LABEL_42;
    if ( v18 == 0 )
      goto LABEL_49;
LABEL_50:
    sub_140833970(&v96);
    ++v11;
    ++v13;
  }
  while ( v11 != v12 );
  v24 = v88;
  if ( (*(unsigned int (__fastcall **)(_QWORD *))(*v88 + 56LL))(v88) == 24 )
  {
    v24 = v88;
    if ( (*(unsigned int (__fastcall **)(_QWORD *))(*v88 + 56LL))(v88) == 24 )
    {
      v24 = v88;
      if ( (_BYTE)word_141B60320 != 0 )
        v24 = (_QWORD *)v88[6];
    }
  }
  sub_1407C9510(&v96);
  (*(void (__fastcall **)(_QWORD *, __int128 *))(*v24 + 136LL))(v24, &v96);
  (*(void (__fastcall **)(_QWORD *, __int64 *))(*v24 + 144LL))(v24, &v91);
  v25 = v87;
  v26 = *(__int64 **)(v87 + 816);
  v27 = *v26;
  v28 = v26[1];
  v29 = nullptr;
  if ( v27 != v28 )
  {
    while ( *(_DWORD *)v27 != 1852798067 )
    {
      v27 += 16;
      if ( v27 == v28 )
        goto LABEL_62;
    }
    if ( v27 == v28 )
      v29 = nullptr;
    else
      v29 = *(__int64 **)(v27 + 8);
  }
LABEL_62:
  if ( v29 == nullptr )
    v29 = &qword_141B5A4A0;
  v30 = (*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v29 + 184LL))(*v29, v29, 0);
  sub_14083ADC0(&v93, v30);
  if ( v90 != v89 )
  {
    v31 = 1;
    if ( (unsigned __int64)(v90 - v89) >= 2 )
      v31 = v90 - v89;
    v83 = v31;
    v32 = 0;
    while ( 1 )
    {
      v33 = v89[v32];
      if ( v33 == nullptr )
        v33 = &qword_141B5A4A0;
      v34 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v33 + 176LL))(*v33, v33, 0);
      v102 = 0;
      v103 = 0;
      sub_1408367A0(&v102, (__int64)(v34[1] - *v34) >> 4, v34, v34 + 1);
      v35 = v102;
      v36 = nullptr;
      if ( (_QWORD)v102 != *((_QWORD *)&v102 + 1) )
      {
        while ( *(_DWORD *)v35 != 1768169504 )
        {
          v35 += 16;
          if ( v35 == *((_QWORD *)&v102 + 1) )
            goto LABEL_76;
        }
        if ( v35 != *((_QWORD *)&v102 + 1) )
        {
          v36 = *(__int64 **)(v35 + 8);
          goto LABEL_77;
        }
LABEL_76:
        v36 = nullptr;
      }
LABEL_77:
      if ( v36 == nullptr )
        v36 = &qword_141B5A4A0;
      (*(void (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)*v36 + 24LL))(*v36, v36, v95);
      v37 = v102;
      if ( (_QWORD)v102 == *((_QWORD *)&v102 + 1) )
        goto LABEL_85;
      while ( *(_DWORD *)v37 != 1684829284 )
      {
        v37 += 16;
        if ( v37 == *((_QWORD *)&v102 + 1) )
          goto LABEL_85;
      }
      if ( v37 == *((_QWORD *)&v102 + 1) )
LABEL_85:
        v38 = nullptr;
      else
        v38 = *(__int64 **)(v37 + 8);
      if ( v38 == nullptr )
        v38 = &qword_141B5A4A0;
      v39 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v38 + 48LL))(*v38);
      v40 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v95[0] + 8LL))(v95[0], v95);
      v108 = v39;
      if ( v39 == 0 && v40 == 0 )
        break;
      v44 = -1;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v95[0] + 8LL))(v95[0], v95) == 0 )
        goto LABEL_151;
      (*(void (__fastcall **)(_QWORD, _QWORD *, __int64 **))(*(_QWORD *)v95[0] + 24LL))(v95[0], v95, &v104);
      v106 = 1768169504;
      v107 = 256;
      (*(void (__fastcall **)(__int64 *, __int64 **, _QWORD *))(*v104 + 24))(v104, &v104, v98);
      v100 = v107;
      v99 = v106;
      v45 = v93;
      v46 = v94;
      v101 = v94;
      while ( v45 != v46 )
      {
        if ( *v45 != nullptr && (*(unsigned __int8 (__fastcall **)(_QWORD))(*(_QWORD *)**v45 + 8LL))(**v45) == 10 )
        {
          v47 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD, _QWORD))(*(_QWORD *)**v45 + 176LL))(
                             **v45,
                             *v45,
                             0);
          v48 = *v47;
          v49 = v47[1];
          if ( v49 != v48 )
          {
            while ( *(_DWORD *)v48 != v99 )
            {
              v48 += 16;
              if ( v48 == v49 )
                goto LABEL_108;
            }
            if ( v48 != v49 )
            {
              v50 = *(__int64 **)(v48 + 8);
              goto LABEL_109;
            }
LABEL_108:
            v50 = nullptr;
LABEL_109:
            if ( v50 == nullptr )
              v50 = &qword_141B5A4A0;
            if ( HIBYTE(v100) == 0
              || (v51 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v50 + 8LL))(*v50, v50),
                  v52 = v51 == (*(char (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v98[0] + 8LL))(v98[0], v98),
                  v46 = v101,
                  v52) )
            {
              if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v50 + 8LL))(*v50, v50) == 26 )
              {
                (*(void (__fastcall **)(__int64, _DWORD **, __int64 *))(*(_QWORD *)*v50 + 128LL))(*v50, &v85, v50);
                (*(void (__fastcall **)(_QWORD, _DWORD **, _QWORD *))(*(_QWORD *)v98[0] + 128LL))(v98[0], &v86, v98);
                v53 = (_DWORD)v86 + 4;
                if ( v86 != nullptr )
                {
                  v54 = *v86;
                }
                else
                {
                  v53 = 1100232177;
                  v54 = 0;
                }
                if ( (_BYTE)v100 != 0 )
                {
                  if ( v85 != nullptr )
                    v55 = *v85;
                  else
                    v55 = 0;
                  v57 = (_DWORD)v85 + 4;
                  if ( v85 == nullptr )
                    v57 = 1100232177;
                  v58 = sub_140811EA0(v57, v53, -1, v55, v54);
                }
                else
                {
                  if ( v85 != nullptr )
                    v56 = *v85;
                  else
                    v56 = 0;
                  v59 = (_DWORD)v85 + 4;
                  if ( v85 == nullptr )
                    v59 = 1100232177;
                  v58 = sub_14080E770(v59, v53, -1, v56, v54, 0);
                }
                v60 = v58;
                v61 = v86;
                if ( v86 != nullptr && _InterlockedDecrement(v86 - 1) == 0 )
                  sub_1412EC9A0((__int64)(v61 - 1));
                v62 = v85;
                if ( v85 != nullptr && _InterlockedDecrement(v85 - 1) == 0 )
                  sub_1412EC9A0((__int64)(v62 - 1));
                if ( v60 == 0 )
                {
LABEL_187:
                  v101 = v45;
                  break;
                }
              }
              else if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)*v50
                                                                                        + 8LL * (*v50 != v98[0])
                                                                                        + 32))(
                          *v50,
                          v50,
                          v98) != 0 )
              {
                goto LABEL_187;
              }
            }
          }
        }
        ++v45;
      }
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v98[0] + 16LL))(v98[0], v98);
      v25 = v87;
      if ( v101 == v94 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
        v73 = false;
        v44 = -1;
      }
      else
      {
        v79 = (char *)v101 - (char *)v93;
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
        v44 = v79 >> 3;
        v73 = v79 >= -7;
        if ( (v73 & v108) == 1 )
        {
          v80 = v93[v44];
          if ( v80 != nullptr )
          {
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v80 + 16LL))(*v80, v93[v44]);
            sub_1408B5E70(v80);
          }
          sub_141758A00();
          --v94;
          goto LABEL_193;
        }
      }
LABEL_152:
      if ( v108 == 0 )
      {
        v75 = *((_QWORD *)&v102 + 1);
        v74 = v102;
        if ( (_QWORD)v102 == *((_QWORD *)&v102 + 1) )
          goto LABEL_162;
        v76 = v102;
        while ( *(_DWORD *)v76 != 1685218662 )
        {
          v76 += 16;
          if ( v76 == *((_QWORD *)&v102 + 1) )
            goto LABEL_162;
        }
        if ( v76 == *((_QWORD *)&v102 + 1) || *(_QWORD *)(v76 + 8) == 0 )
        {
LABEL_162:
          sub_140FEAD00((int *)&v91, &v104);
          sub_140835380((__int64 *)&v102, 1685218662, (__int64 *)&v104);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
          v75 = *((_QWORD *)&v102 + 1);
          v74 = v102;
          if ( (_QWORD)v102 == *((_QWORD *)&v102 + 1) )
            goto LABEL_177;
        }
        else if ( (_QWORD)v102 == *((_QWORD *)&v102 + 1) )
        {
          goto LABEL_177;
        }
        v77 = v74;
        while ( *(_DWORD *)v77 != 1819175795 )
        {
          v77 += 16;
          if ( v77 == v75 )
            goto LABEL_177;
        }
        if ( v77 != v75 && *(_QWORD *)(v77 + 8) != 0 )
        {
          if ( v74 != v75 )
            goto LABEL_170;
          goto LABEL_172;
        }
LABEL_177:
        sub_14083DA80(&v104, &v96);
        sub_140835380((__int64 *)&v102, 1819175795, (__int64 *)&v104);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
        v75 = *((_QWORD *)&v102 + 1);
        v74 = v102;
        if ( (_QWORD)v102 == *((_QWORD *)&v102 + 1) )
          goto LABEL_172;
LABEL_170:
        while ( *(_DWORD *)v74 != 1852007521 )
        {
          v74 += 16;
          if ( v74 == v75 )
            goto LABEL_172;
        }
        if ( v74 == v75 || *(_QWORD *)(v74 + 8) == 0 )
        {
LABEL_172:
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B5C8D0);
            if ( dword_141B5C8D0 == -1 )
            {
              sub_140DBC9B0(&qword_141B5C8A0);
              sub_141751048(sub_140DBCA10);
              sub_141750EA0(&dword_141B5C8D0);
            }
          }
          v105 = ((dword_141AAE084 & 0x1FF) << 8)
               | ((unsigned __int16)dword_141AAE084 >> 9)
               | (HIWORD(dword_141AAE084) << 17);
          v104 = &qword_141B5C8A0;
          sub_140835380((__int64 *)&v102, 1852007521, (__int64 *)&v104);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
        }
        sub_14083DC80(&v104, &v102);
        if ( v73 )
          sub_14083BE60(&v93, &v104, v44);
        else
          sub_14083B5F0(&v93, &v104);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
      }
LABEL_193:
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v95[0] + 16LL))(v95[0], v95);
      sub_140833970(&v102);
      if ( ++v32 == v83 )
        goto LABEL_198;
    }
    v41 = *(__int64 **)(v25 + 816);
    if ( v41 != nullptr )
    {
      v42 = *v41;
      v43 = v41[1];
      if ( v42 == v43 )
        goto LABEL_140;
      while ( *(_DWORD *)v42 != 1852796521 )
      {
        v42 += 16;
        if ( v42 == v43 )
          goto LABEL_140;
      }
      if ( v42 == v43 )
LABEL_140:
        v63 = nullptr;
      else
        v63 = *(__int64 **)(v42 + 8);
      if ( v63 == nullptr )
        v63 = &qword_141B5A4A0;
      if ( v95 != v63 )
      {
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v95[0] + 16LL))(v95[0], v95);
        (*(void (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)*v63 + 24LL))(*v63, v63, v95);
      }
    }
    v64 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v95[0] + 80LL))(v95[0], v95) + 1;
    v66 = sub_14083D4F0(v65);
    v105 = v64;
    v104 = (__int64 *)(v66 + 56);
    v67 = *(__int64 **)(v25 + 816);
    if ( v67 != nullptr )
    {
      v68 = *v67;
      v69 = v67[1];
      if ( *v67 == v69 )
        goto LABEL_149;
      while ( *(_DWORD *)v68 != 1852796521 )
      {
        v68 += 16;
        if ( v68 == v69 )
          goto LABEL_149;
      }
      if ( v68 == v69 || (v78 = *(__int64 **)(v68 + 8)) == nullptr )
      {
LABEL_149:
        sub_140835A40(v67, 1852796521, &v104);
      }
      else if ( v78 != (__int64 *)&v104 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v78 + 16LL))(*v78, v78);
        (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v104 + 24))(v104, &v104, v78);
      }
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
    v70 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v95[0] + 80LL))(v95[0], v95);
    v72 = sub_14083D4F0(v71);
    v105 = v70;
    v104 = (__int64 *)(v72 + 56);
    sub_140835380((__int64 *)&v102, 1768169504, (__int64 *)&v104);
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v104 + 16))(v104, &v104);
    v44 = -1;
LABEL_151:
    v73 = false;
    goto LABEL_152;
  }
LABEL_198:
  v81 = *(__int64 **)(v25 + 816);
  sub_14083DA80(&v102, &v93);
  sub_140835380(v81, 1852798067, (__int64 *)&v102);
  (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v102 + 16LL))(v102, &v102);
  (*(void (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)qword_141B5EF38 + 480LL))(qword_141B5EF38, v25, &v91);
  sub_14083B0A0(&v93);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v92 + 16LL))(v92, &v92);
  sub_14083B0A0(&v96);
LABEL_199:
  sub_14083B0A0(&v89);
  v4 = v84;
  v3 = v88;
  return v3 != nullptr && v4 != 0;
}
