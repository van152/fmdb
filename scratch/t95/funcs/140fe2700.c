__int64 __fastcall sub_140FE2700(_DWORD *a1, int a2, __int64 **a3)
{
  __int64 v3; // r15
  __int64 v7; // rax
  __int64 v8; // r14
  __int64 v9; // rax
  __int64 v10; // r13
  unsigned __int8 v11; // r12
  unsigned int v12; // eax
  int v13; // ecx
  unsigned int v14; // esi
  __int64 v15; // rax
  __int64 v16; // rax
  __int64 v17; // rsi
  unsigned __int64 v18; // rcx
  __int64 v19; // rbx
  __int64 v20; // rsi
  bool v21; // al
  __int64 v22; // rax
  __int64 v24; // rax
  __int64 v25; // rsi
  __int64 v26; // rax
  __int64 v27; // rax
  char v28; // al
  __int64 *v29; // rcx
  __int64 v30; // rsi
  int v31; // eax
  char v32; // al
  __int64 *v33; // rcx
  __int64 v34; // rdi
  __int64 *v35; // rbx
  __int64 v36; // rax
  __int64 v37; // rcx
  __int64 v38; // rdx
  _QWORD **v39; // rax
  __int64 v40; // rdx
  _QWORD *v41; // rax
  __int64 v42; // rdi
  unsigned __int64 v43; // rbx
  __int64 v44; // rdi
  unsigned __int64 v45; // rcx
  __int64 v46; // rbx
  __int64 v47; // rsi
  bool v48; // al
  __int64 v49; // rsi
  char v50; // bl
  void (__fastcall ***v51)(_QWORD, __int64); // rcx
  char v52; // al
  int v53; // eax
  __int64 *v54; // rdx
  __int64 v55; // r8
  bool v56; // cf
  _QWORD **v57; // rax
  _QWORD *v58; // rax
  __int64 **v59; // rax
  __int64 *v60; // rsi
  __int64 v61; // r12
  __int64 *v62; // r14
  __int64 v63; // rcx
  __int64 v64; // rax
  unsigned __int64 v65; // rax
  __int64 v66; // r13
  __int64 i; // r14
  __int64 *v68; // rdi
  __int64 v69; // rax
  __int64 v70; // rax
  __int64 v71; // rbx
  _QWORD *v72; // rdi
  __int64 v73; // r12
  __int64 *v74; // r8
  __int64 v75; // rax
  __int64 *v76; // r14
  __int64 v77; // rax
  __int64 v78; // rax
  __int64 v79; // rcx
  __int64 *v80; // rsi
  __int64 v81; // rcx
  __int64 v82; // rdx
  __int64 *v83; // rax
  _QWORD **v84; // rax
  _QWORD *v85; // rax
  __int64 v86; // rdi
  unsigned __int64 v87; // rbx
  __int64 v88; // rdi
  __int64 v89; // rax
  __int64 v90; // rcx
  __int64 *v91; // rdx
  __int64 v92; // r8
  _QWORD **v93; // rax
  _QWORD *v94; // rax
  __int64 **v95; // rax
  __int64 v96; // rdx
  __int64 *v97; // rsi
  __int64 v98; // r12
  __int64 *v99; // r14
  __int64 v100; // rcx
  __int64 v101; // rax
  __int64 v102; // rax
  __int64 v103; // r12
  _QWORD *v104; // rsi
  __int64 v105; // rdi
  __int64 v106; // rdi
  __int64 v107; // rbx
  __int64 *v108; // r8
  int v109; // eax
  unsigned int v110; // esi
  _QWORD **v111; // rax
  _QWORD *v112; // rax
  unsigned __int64 v113; // rbx
  __int64 v114; // rax
  __int64 v115; // rdx
  __int64 v116; // rsi
  _QWORD *v117; // rdi
  __int64 v118; // r8
  __int64 **v119; // r14
  __int64 *v120; // rbx
  __int64 v121; // rcx
  int v122; // eax
  unsigned int v123; // esi
  _QWORD **v124; // rax
  _QWORD *v125; // rax
  __int64 v126; // rsi
  __int64 v127; // rdi
  __int64 v128; // rcx
  __int64 *v129; // rdx
  __int64 v130; // rax
  __int64 *v131; // rbx
  unsigned int v132; // eax
  _QWORD *v133; // [rsp+48h] [rbp-38h] BYREF
  _QWORD v134[2]; // [rsp+50h] [rbp-30h] BYREF
  _QWORD v135[2]; // [rsp+60h] [rbp-20h] BYREF
  __int64 v136; // [rsp+70h] [rbp-10h]
  int v137; // [rsp+78h] [rbp-8h]
  __int64 v138; // [rsp+80h] [rbp+0h]
  __int64 v139; // [rsp+88h] [rbp+8h]
  __int64 v140; // [rsp+90h] [rbp+10h]
  char v141; // [rsp+9Ch] [rbp+1Ch]
  _QWORD *v142; // [rsp+A0h] [rbp+20h]
  __int64 v143; // [rsp+A8h] [rbp+28h] BYREF
  _DWORD *v144; // [rsp+B0h] [rbp+30h] BYREF
  _DWORD *v145; // [rsp+B8h] [rbp+38h] BYREF
  __int64 v146; // [rsp+C0h] [rbp+40h]
  __int64 v147; // [rsp+D0h] [rbp+50h]

  v147 = -2;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5FD48 + 32LL))(qword_141B5FD48) == 0 )
  {
    LOBYTE(v3) = 1;
    if ( (*(unsigned __int8 (__fastcall **)(__int64, _DWORD *, _QWORD, __int64 **))(*(_QWORD *)qword_141B5FD48 + 48LL))(
           qword_141B5FD48,
           a1,
           (unsigned int)a2,
           a3) != 0 )
      return (unsigned int)v3;
  }
  if ( a2 <= 1852798052 )
  {
    if ( a2 > 1685417576 )
    {
      if ( a2 != 1685417577 )
      {
        if ( a2 != 1852073332 && a2 != 1852796521 )
        {
LABEL_45:
          v22 = (*(__int64 (__fastcall **)(_DWORD *, _QWORD))(*(_QWORD *)a1 + 80LL))(a1, (unsigned int)a2);
          if ( v22 != 0 )
            return (*(__int64 (__fastcall **)(__int64, _QWORD, __int64 **))(*(_QWORD *)v22 + 24LL))(
                     v22,
                     (unsigned int)a2,
                     a3);
LABEL_240:
          LODWORD(v3) = 0;
          return (unsigned int)v3;
        }
        goto LABEL_29;
      }
      v28 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
      v29 = *a3;
      v30 = **a3;
      if ( v28 == 15 )
      {
        v31 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(v30 + 64))(v29, a3);
      }
      else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v30 + 8))(v29, a3) == 10 )
      {
        sub_140FE7960(&v133, a3, 0);
        v31 = (int)v133;
      }
      else
      {
        v49 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        v31 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        if ( v49 != v31 )
          v31 = v49;
      }
      a1[3] = v31;
LABEL_88:
      LOBYTE(v3) = 1;
      return (unsigned int)v3;
    }
    if ( a2 == 1129271385 )
    {
      sub_1407C9510(&v133);
      if ( (*(unsigned __int8 (__fastcall **)(_DWORD *, _QWORD **))(*(_QWORD *)a1 + 40LL))(a1, &v133) != 0 )
      {
        LOBYTE(v144) = 0;
        v26 = (*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 176))(*a3, a3, 0);
        v27 = sub_140E475B0(v26, &v144);
        LOBYTE(v3) = v27 != 0;
        if ( v27 != 0 && (_BYTE)v144 == 0 )
          sub_1407EB170(v27, a1, &v133);
      }
      else
      {
        LODWORD(v3) = 0;
      }
      sub_14083B0A0(&v133);
      return (unsigned int)v3;
    }
    if ( a2 != 1634496109 )
    {
      if ( a2 != 1685284961 )
        goto LABEL_45;
      a1[2] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_88;
    }
    v144 = a1;
    v145 = a1;
    v133 = &v144;
    v134[0] = &v145;
    v32 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
    v33 = *a3;
    v34 = **a3;
    if ( v32 != 10 )
    {
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v34 + 8))(v33, a3) == 11 )
      {
        v142 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
        v39 = (_QWORD **)(*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v145 + 96LL))(v145);
        if ( v39 != nullptr )
        {
          v41 = *v39;
          if ( v41 != nullptr )
          {
            v42 = v41[1] - *v41;
            if ( v42 != 0 )
            {
              v43 = (v42 >> 3) - 1;
              v44 = -(__int64)(v42 & 0xFFFFFFFFFFFFFFF8uLL);
              do
              {
                v57 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(**(_QWORD **)v134[0] + 96LL))(*(_QWORD *)v134[0]);
                if ( v57 != nullptr )
                {
                  v58 = *v57;
                  if ( v58 != nullptr && *(_QWORD *)(*v58 + 8 * v43) != 0 )
                  {
                    v59 = (__int64 **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v133 + 96LL))(*v133);
                    if ( v59 != nullptr )
                    {
                      v60 = *v59;
                      if ( *v59 != nullptr )
                      {
                        v61 = *v60;
                        v55 = v60[1];
                        if ( (v55 - *v60) >> 3 > v43 )
                        {
                          v62 = *(__int64 **)(v61 + 8 * v43);
                          if ( v62 != nullptr )
                          {
                            v63 = *v62;
                            if ( *v62 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v63 - 4)) == 0 )
                              sub_1412EC9A0(v63 - 4, v40);
                            sub_140E469C0(v62);
                            v55 = v60[1];
                          }
                          sub_141758A00(v61 + 8 * v43, v61 + 8 * v43 + 8, v44 + v55 - v61);
                          v60[1] -= 8;
                        }
                      }
                    }
                  }
                }
                v44 += 8;
                v56 = v43-- != 0;
              }
              while ( v56 );
            }
          }
        }
        v64 = v142[1] - *v142;
        if ( v64 != 0 )
        {
          v65 = v64 >> 3;
          v66 = 1;
          if ( v65 >= 2 )
            v66 = v65;
          for ( i = 0; i != v66; ++i )
          {
            v68 = *(__int64 **)(*v142 + 8 * i);
            if ( v68 == nullptr )
              v68 = &qword_141B5A4A0;
            v69 = (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v133 + 96LL))(*v133);
            if ( v69 != 0 )
            {
              v70 = sub_140E44CE0(v69, &qword_141B59EE0, 0, 0);
              if ( v70 != 0 )
              {
                v71 = v70;
                v72 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v68 + 176LL))(
                                  *v68,
                                  v68,
                                  0);
                v3 = v72[1] - *v72;
                if ( v3 != 0 )
                {
                  v3 >>= 4;
                  v73 = 8;
                  do
                  {
                    v74 = *(__int64 **)(*v72 + v73);
                    if ( v74 == nullptr )
                      v74 = &qword_141B5A4A0;
                    sub_140E46160(v71, *(unsigned int *)(*v72 + v73 - 8), v74);
                    v73 += 16;
                    --v3;
                  }
                  while ( v3 != 0 );
                }
              }
            }
          }
        }
        v75 = qword_141B60C30;
        if ( qword_141B60C30 == qword_141B60C38 )
          goto LABEL_145;
        while ( *(_DWORD *)v75 != 1986359923 )
        {
          v75 += 16;
          if ( v75 == qword_141B60C38 )
            goto LABEL_145;
        }
        if ( v75 == qword_141B60C38 || (LOBYTE(v3) = 1, *(_QWORD *)(v75 + 8) == 0) )
        {
LABEL_145:
          LOBYTE(v3) = 1;
          LOBYTE(v40) = 1;
          sub_140FEA1B0(&v133, v40);
        }
        return (unsigned int)v3;
      }
      goto LABEL_240;
    }
    LODWORD(v3) = 0;
    v35 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v34 + 176))(v33, a3, 0);
    v36 = *v35;
    v37 = v35[1];
    if ( *v35 != v37 )
    {
      v38 = *v35;
      while ( *(_DWORD *)v38 != 1819504496 )
      {
        v38 += 16;
        if ( v38 == v37 )
          goto LABEL_240;
      }
      if ( v38 != v37 && *(_QWORD *)(v38 + 8) != 0 )
      {
        v54 = nullptr;
        while ( *(_DWORD *)v36 != 1819504496 )
        {
          v36 += 16;
          if ( v36 == v37 )
            goto LABEL_160;
        }
        v54 = v36 == v37 ? nullptr : *(__int64 **)(v36 + 8);
LABEL_160:
        v76 = &qword_141B5A4A0;
        if ( v54 == nullptr )
          v54 = &qword_141B5A4A0;
        switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v54 + 64LL))(*v54) )
        {
          case 0u:
            v77 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v144 + 96LL))(v144);
            if ( v77 == 0 )
              goto LABEL_240;
            LOBYTE(v3) = sub_140E44CE0(v77, &qword_141B59EE0, 0, 0) != 0;
            return (unsigned int)v3;
          case 1u:
            v89 = *v35;
            v90 = v35[1];
            v91 = nullptr;
            if ( *v35 != v90 )
            {
              while ( *(_DWORD *)v89 != 1869379180 )
              {
                v89 += 16;
                if ( v89 == v90 )
                  goto LABEL_229;
              }
              if ( v89 == v90 )
                v91 = nullptr;
              else
                v91 = *(__int64 **)(v89 + 8);
            }
LABEL_229:
            if ( v91 == nullptr )
              v91 = &qword_141B5A4A0;
            v122 = sub_140FEA3A0(v134, v91);
            if ( v122 < 0 )
              goto LABEL_240;
            v123 = v122;
            v124 = (_QWORD **)(*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v145 + 96LL))(v145);
            if ( v124 == nullptr )
              goto LABEL_240;
            v125 = *v124;
            if ( v125 == nullptr )
              goto LABEL_240;
            v126 = *(_QWORD *)(*v125 + 8LL * v123);
            if ( v126 == 0 )
              goto LABEL_240;
            v127 = *v35;
            v128 = v35[1];
            v129 = nullptr;
            if ( *v35 == v128 )
            {
              v131 = &qword_141B5A4A0;
            }
            else
            {
              v130 = *v35;
              while ( *(_DWORD *)v130 != 1986096245 )
              {
                v130 += 16;
                if ( v130 == v128 )
                  goto LABEL_248;
              }
              if ( v130 == v128 )
                v129 = nullptr;
              else
                v129 = *(__int64 **)(v130 + 8);
LABEL_248:
              v131 = &qword_141B5A4A0;
              if ( v129 != nullptr )
                v131 = v129;
              v129 = nullptr;
              while ( *(_DWORD *)v127 != 1768169504 )
              {
                v127 += 16;
                if ( v127 == v128 )
                  goto LABEL_257;
              }
              if ( v127 == v128 )
                v129 = nullptr;
              else
                v129 = *(__int64 **)(v127 + 8);
            }
LABEL_257:
            if ( v129 != nullptr )
              v76 = v129;
            v132 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v76 + 80LL))(*v76, v76);
            LODWORD(v3) = sub_140E46160(v126, v132, v131);
            return (unsigned int)v3;
          case 2u:
            v81 = *v35;
            v82 = v35[1];
            v83 = nullptr;
            if ( *v35 != v82 )
            {
              while ( *(_DWORD *)v81 != 1869379180 )
              {
                v81 += 16;
                if ( v81 == v82 )
                  goto LABEL_213;
              }
              if ( v81 == v82 )
                v83 = nullptr;
              else
                v83 = *(__int64 **)(v81 + 8);
            }
LABEL_213:
            if ( v83 != nullptr )
              v76 = v83;
            v109 = sub_140FEA3A0(v134, v76);
            if ( v109 < 0 )
              goto LABEL_240;
            v110 = v109;
            v111 = (_QWORD **)(*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v145 + 96LL))(v145);
            if ( v111 == nullptr )
              goto LABEL_240;
            v112 = *v111;
            if ( v112 == nullptr )
              goto LABEL_240;
            v113 = v110;
            if ( *(_QWORD *)(*v112 + 8LL * v110) == 0 )
              goto LABEL_240;
            v114 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v144 + 96LL))(v144);
            v116 = v114;
            if ( v114 != 0 )
            {
              v117 = *(_QWORD **)v114;
              if ( *(_QWORD *)v114 != 0 && ((v118 = v117[1]) - *v117) >> 3 > v113 )
              {
                v119 = (__int64 **)(*v117 + 8 * v113);
                v120 = *v119;
                if ( *v119 != nullptr )
                {
                  v121 = *v120;
                  if ( *v120 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v121 - 4)) == 0 )
                    sub_1412EC9A0(v121 - 4, v115);
                  sub_140E469C0(v120);
                  v118 = v117[1];
                }
                sub_141758A00(v119, v119 + 1, v118 - (_QWORD)(v119 + 1));
                v117[1] -= 8LL;
                LOBYTE(v114) = 1;
              }
              else
              {
                LOBYTE(v114) = 0;
              }
            }
            LOBYTE(v3) = v114 & (v116 != 0);
            return (unsigned int)v3;
          case 3u:
            v84 = (_QWORD **)(*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v145 + 96LL))(v145);
            LOBYTE(v3) = 1;
            if ( v84 != nullptr )
            {
              v85 = *v84;
              if ( v85 != nullptr )
              {
                v86 = v85[1] - *v85;
                if ( v86 != 0 )
                {
                  v87 = (v86 >> 3) - 1;
                  v88 = -(__int64)(v86 & 0xFFFFFFFFFFFFFFF8uLL);
                  do
                  {
                    v93 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(**(_QWORD **)v134[0] + 96LL))(*(_QWORD *)v134[0]);
                    if ( v93 != nullptr )
                    {
                      v94 = *v93;
                      if ( v94 != nullptr && *(_QWORD *)(*v94 + 8 * v87) != 0 )
                      {
                        v95 = (__int64 **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)*v133 + 96LL))(*v133);
                        if ( v95 != nullptr )
                        {
                          v97 = *v95;
                          if ( *v95 != nullptr )
                          {
                            v98 = *v97;
                            v92 = v97[1];
                            if ( (v92 - *v97) >> 3 > v87 )
                            {
                              v99 = *(__int64 **)(v98 + 8 * v87);
                              if ( v99 != nullptr )
                              {
                                v100 = *v99;
                                if ( *v99 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v100 - 4)) == 0 )
                                  sub_1412EC9A0(v100 - 4, v96);
                                sub_140E469C0(v99);
                                v92 = v97[1];
                              }
                              sub_141758A00(v98 + 8 * v87, v98 + 8 * v87 + 8, v88 + v92 - v98);
                              v97[1] -= 8;
                            }
                          }
                        }
                      }
                    }
                    v88 += 8;
                    v56 = v87-- != 0;
                  }
                  while ( v56 );
                }
              }
            }
            return (unsigned int)v3;
          case 4u:
            v78 = *v35;
            v79 = v35[1];
            v80 = nullptr;
            if ( *v35 == v79 )
              goto LABEL_202;
            break;
          case 5u:
            sub_140FEA1B0(&v133, 0);
            goto LABEL_88;
          default:
            goto LABEL_240;
        }
        while ( *(_DWORD *)v78 != 1869379180 )
        {
          v78 += 16;
          if ( v78 == v79 )
            goto LABEL_202;
        }
        v80 = v78 == v79 ? nullptr : *(__int64 **)(v78 + 8);
LABEL_202:
        if ( v80 == nullptr )
          v80 = &qword_141B5A4A0;
        v101 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v144 + 96LL))(v144);
        if ( v101 != 0 )
        {
          LODWORD(v3) = 0;
          v102 = sub_140E44CE0(v101, &qword_141B59EE0, 0, 0);
          if ( v102 != 0 )
          {
            v103 = v102;
            v104 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v80 + 176LL))(
                               *v80,
                               v80,
                               0);
            LOBYTE(v3) = 1;
            v105 = v104[1] - *v104;
            if ( v105 != 0 )
            {
              v106 = v105 >> 4;
              v107 = 8;
              do
              {
                v108 = *(__int64 **)(*v104 + v107);
                if ( v108 == nullptr )
                  v108 = &qword_141B5A4A0;
                sub_140E46160(v103, *(unsigned int *)(*v104 + v107 - 8), v108);
                v107 += 16;
                --v106;
              }
              while ( v106 != 0 );
            }
          }
          return (unsigned int)v3;
        }
      }
      goto LABEL_240;
    }
  }
  else
  {
    if ( a2 > 1853122155 )
    {
      if ( a2 <= 1919186280 )
      {
        if ( a2 != 1853122156 && a2 != 1853122419 )
          goto LABEL_45;
LABEL_29:
        v15 = sub_140FE35F0();
        if ( v15 == 0 )
          goto LABEL_45;
        sub_14100C380(v15 + 1104, (unsigned int)a2, a3);
        goto LABEL_88;
      }
      if ( a2 != 1919186281 )
      {
        if ( a2 == 1935829358 )
        {
          v16 = sub_140FE35F0();
          LOBYTE(v3) = 1;
          if ( v16 != 0 )
          {
            v17 = v16;
            sub_14150F810(&v133);
            if ( dword_141B59E30 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                               + (unsigned int)TlsIndex)
                                             + 4LL) )
            {
              sub_141750E08(&dword_141B59E30);
              if ( dword_141B59E30 == -1 )
              {
                sub_1408040C0(&qword_141B59E00);
                sub_141751048(sub_140804150);
                sub_141750EA0(&dword_141B59E30);
              }
            }
            if ( *a3 != &qword_141B59E00 )
              goto LABEL_36;
            sub_140805330(&v144, a3[1]);
            v143 = v146;
            if ( v146 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v146 + 8));
            sub_1412D68A0(&v144);
            if ( v143 == 0 )
              goto LABEL_36;
            v50 = sub_14151C2A0(&v133, &v143);
            v51 = (void (__fastcall ***)(_QWORD, __int64))v143;
            if ( v143 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v143 + 8)) == 0 )
              (**v51)(v51, 1);
            if ( v50 != 0 )
              sub_14101DBD0(v17, (_DWORD)a1, (unsigned int)v135, v137, v141, 1, 0);
            else
LABEL_36:
              sub_14101E230(v17, a1);
            if ( v138 != 0 )
            {
              v18 = v140 - v138;
              if ( v140 - v138 == -1 )
                v18 = *(unsigned int *)(v138 - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v19 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v19) >> 3 > v18)
                && (v20 = *(_QWORD *)(v19 + 8 * v18)) != 0 )
              {
                MEMORY[0x1419475D8](v20 + 32, v138 - *(unsigned int *)(v20 + 120));
                v21 = *(_BYTE *)(v20 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 + 64)) != 0;
                if ( !v21 && *(_BYTE *)(v20 + 97) != 0 )
                  sub_1412D33C0(v20);
              }
              else
              {
                MEMORY[0x141948990](v138 - *(unsigned int *)(qword_141ABD470 + 48));
              }
              v140 = 0;
              v139 = 0;
              v138 = 0;
            }
            if ( v135[0] != 0 )
            {
              v45 = v136 - v135[0];
              if ( v136 - v135[0] == -1 )
                v45 = *(unsigned int *)(v135[0] - *(unsigned int *)(qword_141ABD470 + 48));
              if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
                && (v46 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v46) >> 3 > v45)
                && (v47 = *(_QWORD *)(v46 + 8 * v45)) != 0 )
              {
                MEMORY[0x1419475D8](v47 + 32, v135[0] - *(unsigned int *)(v47 + 120));
                v48 = *(_BYTE *)(v47 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v47 + 64)) != 0;
                if ( !v48 && *(_BYTE *)(v47 + 97) != 0 )
                  sub_1412D33C0(v47);
              }
              else
              {
                MEMORY[0x141948990](v135[0] - *(unsigned int *)(qword_141ABD470 + 48));
              }
              v136 = 0;
              v135[1] = 0;
              v135[0] = 0;
            }
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v134[0] + 16LL))(v134[0], v134);
          }
          return (unsigned int)v3;
        }
        goto LABEL_45;
      }
      a1[4] = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_88;
    }
    if ( a2 == 1852798053 || a2 == 1852798067 )
    {
      v24 = sub_140FE35F0();
      v25 = v24;
      if ( v24 != 0 )
        sub_141026FD0(v24, a1, a3);
      LOBYTE(v3) = v25 != 0;
      return (unsigned int)v3;
    }
    if ( a2 != 1853059955 )
      goto LABEL_45;
    v7 = sub_140FE35F0();
    LOBYTE(v3) = 1;
    if ( v7 != 0 )
    {
      v8 = v7;
      v9 = sub_140FE35F0();
      if ( v9 != 0 )
      {
        v10 = v9;
        v11 = sub_14101D650(v9, a1);
        if ( (unsigned __int8)sub_14101D990(v10, a1) != 0 )
        {
          v12 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1);
          if ( v12 <= 0x19 )
          {
            v13 = 50332201;
            if ( _bittest(&v13, v12) )
              goto LABEL_99;
            if ( v12 == 1 && (*(unsigned int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1) == 1 )
            {
              v14 = 1;
              if ( (((*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 1760LL))(a1) == 0) | v11) == 0 )
                goto LABEL_103;
LABEL_99:
              v52 = sub_14101A340(v10, a1, 0, 0);
              v14 = 3;
              if ( (~v52 & 3) != 0 )
              {
                v14 = 4;
                if ( (v52 & 1) == 0 )
                {
                  v14 = 5;
                  if ( (v52 & 2) == 0 )
                    v14 = v52 & 4 | 2;
                }
              }
              goto LABEL_103;
            }
          }
        }
        v14 = 1;
        if ( v11 != 0 )
          goto LABEL_99;
      }
      else
      {
        v14 = 0;
      }
LABEL_103:
      v53 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      if ( v14 >= 2 && v14 != v53 )
      {
        if ( (unsigned int)(v53 - 3) > 0xFFFFFFFD )
          sub_14101E230(v8, a1);
        else
          sub_14101DBD0(v8, (_DWORD)a1, 0, 0, 0, 1, 0);
      }
    }
  }
  return (unsigned int)v3;
}
