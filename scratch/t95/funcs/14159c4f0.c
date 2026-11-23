__int64 __fastcall sub_14159C4F0(__int64 a1, __int64 a2, __int64 **a3)
{
  _QWORD *v3; // r14
  __int64 v6; // rdx
  __int64 v7; // rcx
  _QWORD *v8; // rax
  _QWORD *v9; // r13
  __int64 v10; // rcx
  __int64 v11; // r8
  __int64 v12; // rbp
  _QWORD *v13; // rdi
  __int64 v14; // rbx
  __int64 v15; // rax
  __int64 v16; // rbp
  unsigned __int64 v17; // r13
  __int64 v18; // rcx
  __int64 v19; // rsi
  __int64 v20; // rbx
  __int64 v21; // rbx
  __int64 v22; // rax
  __int64 v23; // rbp
  unsigned __int64 v24; // rsi
  __int64 v25; // rcx
  __int64 v26; // rdi
  __int64 v27; // rbx
  char v28; // al
  __int64 *v29; // rcx
  __int64 v30; // rbp
  __int64 *v31; // rbx
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rdx
  _QWORD *v36; // rbx
  __int64 *v37; // rsi
  __int64 v38; // rdi
  __int64 v39; // rcx
  __int64 v40; // rcx
  __int64 v41; // rsi
  __int64 v42; // rax
  __int64 v43; // rbx
  __int64 j; // rdi
  __int64 v45; // rdi
  __int64 v46; // rsi
  __int64 v47; // rcx
  __int64 v48; // r8
  __int64 v49; // rdx
  __int64 v50; // rbp
  __int64 v51; // rax
  unsigned __int64 v52; // rax
  __int64 v53; // rbp
  __int64 k; // rsi
  __int64 *v55; // rdx
  __int64 v56; // rbx
  __int64 v57; // rax
  __int64 v58; // rbx
  __int64 v59; // rcx
  __int64 v60; // rax
  __int64 *v61; // rdx
  __int64 *v62; // r15
  __int64 v63; // rcx
  __int64 v64; // rdx
  __int64 *v65; // rax
  __int64 v66; // rax
  __int64 v67; // rcx
  __int64 *v68; // rdx
  __int64 v69; // rcx
  __int64 v70; // rdx
  __int64 *v71; // rax
  __int64 v72; // rsi
  __int64 v73; // r12
  __int64 v74; // rbx
  __int64 v75; // rcx
  __int64 v76; // r8
  __int64 v77; // rdx
  __int64 v78; // rbp
  __int64 v79; // rdi
  __int64 v80; // rax
  __int64 v81; // rsi
  int v82; // eax
  __int64 v83; // rcx
  __int64 v84; // r8
  __int64 v85; // rdx
  __int64 v86; // rbp
  __int64 v87; // rcx
  __int64 v88; // rdx
  __int64 *v89; // rax
  int v90; // eax
  __int64 v91; // rdi
  __int64 v92; // rcx
  __int64 v93; // r8
  __int64 v94; // rdx
  __int64 v95; // rbp
  unsigned __int64 v96; // rcx
  __int64 v97; // rbp
  __int64 v98; // rdi
  bool v99; // al
  __int64 v100; // [rsp+20h] [rbp-88h] BYREF
  __int64 v101; // [rsp+28h] [rbp-80h] BYREF
  __int64 v102; // [rsp+30h] [rbp-78h]
  __int64 v103; // [rsp+38h] [rbp-70h]
  __int64 v104; // [rsp+40h] [rbp-68h] BYREF
  __int64 v105; // [rsp+48h] [rbp-60h]
  _QWORD *i; // [rsp+50h] [rbp-58h]
  __int64 *v107; // [rsp+58h] [rbp-50h]
  _QWORD v108[9]; // [rsp+60h] [rbp-48h] BYREF

  if ( (int)a2 > 1097757800 )
  {
    if ( (_DWORD)a2 != 1097757801 )
    {
      if ( (_DWORD)a2 == 1145392197 )
      {
        v8 = *(_QWORD **)(qword_141B5FDD0 + 128);
        v9 = (_QWORD *)*v8;
        for ( i = (_QWORD *)v8[1]; v9 != i; ++v9 )
        {
          v3 = (_QWORD *)*v9;
          if ( sub_141048140(*v9, *(unsigned int *)(a1 + 12), 0xFFFFFFFFLL, 0xFFFFFFFFLL) != 0 )
          {
            v10 = v3[24];
            v11 = v3[25] - v10;
            if ( v11 != 0 )
            {
              a2 = v11 >> 4;
              if ( (unsigned __int64)(v11 >> 4) < 2 )
                a2 = 1;
              v12 = 0;
              while ( *(_DWORD *)(*(_QWORD *)(v10 + v12) + 12LL) != *(_DWORD *)(a1 + 12) )
              {
                v12 += 16;
                if ( --a2 == 0 )
                  goto LABEL_23;
              }
              sub_141758A00(v12 + v10, v10 + v12 + 16, v11 - v12 - 16);
              v3[25] -= 16LL;
            }
LABEL_23:
            v13 = v9;
            v14 = v3[21];
            v15 = v3[22];
            if ( v15 != v14 )
            {
              v16 = 0;
              v17 = 0;
              do
              {
                a2 = v16 >> 29;
                v18 = *(_QWORD *)(v14 + (v16 >> 29));
                if ( v18 != 0 )
                {
                  v19 = *(_QWORD *)(v18 + 32);
                  if ( v19 != 0 && v19 == a1 )
                  {
                    v20 = a2 + v14;
                    sub_141750CFC(v18);
                    sub_141758A00(v20, v20 + 8, v3[22] - (v20 + 8));
                    v14 = v3[21];
                    v15 = v3[22] - 8LL;
                    v3[22] = v15;
                  }
                }
                ++v17;
                v16 += 0x100000000LL;
              }
              while ( v17 < (v15 - v14) >> 3 );
            }
            v21 = v3[18];
            v22 = v3[19];
            v9 = v13;
            if ( v22 != v21 )
            {
              v23 = 0;
              v24 = 0;
              do
              {
                a2 = v23 >> 29;
                v25 = *(_QWORD *)(v21 + (v23 >> 29));
                if ( v25 != 0 )
                {
                  v26 = *(_QWORD *)(v25 + 32);
                  if ( v26 != 0 && v26 == a1 )
                  {
                    v27 = a2 + v21;
                    sub_141750CFC(v25);
                    sub_141758A00(v27, v27 + 8, v3[19] - (v27 + 8));
                    v21 = v3[18];
                    v22 = v3[19] - 8LL;
                    v3[19] = v22;
                  }
                }
                ++v24;
                v23 += 0x100000000LL;
              }
              while ( v24 < (v22 - v21) >> 3 );
            }
          }
        }
        v36 = *(_QWORD **)(qword_141B5FE60 + 128);
        v37 = (__int64 *)(*v36 + 8LL * *(int *)(a1 + 8));
        v38 = *v37;
        if ( *v37 != 0 )
        {
          v39 = *(_QWORD *)(v38 + 40);
          if ( v39 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v39 - 4)) == 0 )
            sub_1412EC9A0(v39 - 4, a2);
          v40 = *(_QWORD *)(v38 + 32);
          if ( v40 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v40 - 4)) == 0 )
            sub_1412EC9A0(v40 - 4, a2);
          sub_140E44A40(v38 + 24);
          sub_140FAF160(v38);
        }
        sub_141758A00(v37, v37 + 1, v36[1] - (_QWORD)(v37 + 1));
        v36[1] -= 8LL;
        v41 = qword_141B5FE60;
        v42 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5FE60 + 48LL))(qword_141B5FE60);
        LOBYTE(v3) = 1;
        if ( v42 != 0 )
        {
          v43 = v42;
          for ( j = 0; j != v43; ++j )
            *(_DWORD *)((*(__int64 (__fastcall **)(__int64, _QWORD))(*(_QWORD *)v41 + 16LL))(v41, (unsigned int)j) + 8) = j;
        }
        return (unsigned int)v3;
      }
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    }
    v100 = a1;
    sub_141735860(&v101, a1);
    v107 = &v100;
    v108[0] = &v101;
    v28 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3);
    v29 = *a3;
    v30 = **a3;
    if ( v28 == 10 )
    {
      LODWORD(v3) = 0;
      v31 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(v30 + 176))(v29, a3, 0);
      v32 = *v31;
      v33 = v31[1];
      if ( *v31 == v33 )
        goto LABEL_182;
      v34 = *v31;
      while ( *(_DWORD *)v34 != 1819504496 )
      {
        v34 += 16;
        if ( v34 == v33 )
          goto LABEL_181;
      }
      if ( v34 != v33 && *(_QWORD *)(v34 + 8) != 0 )
      {
        v61 = nullptr;
        while ( *(_DWORD *)v32 != 1819504496 )
        {
          v32 += 16;
          if ( v32 == v33 )
            goto LABEL_104;
        }
        if ( v32 == v33 )
          v61 = nullptr;
        else
          v61 = *(__int64 **)(v32 + 8);
LABEL_104:
        v62 = &qword_141B5A4A0;
        if ( v61 == nullptr )
          v61 = &qword_141B5A4A0;
        switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v61 + 64LL))(*v61) )
        {
          case 0u:
            v63 = *v31;
            v64 = v31[1];
            v65 = nullptr;
            if ( *v31 == v64 )
              goto LABEL_145;
            while ( *(_DWORD *)v63 != 1986096245 )
            {
              v63 += 16;
              if ( v63 == v64 )
                goto LABEL_145;
            }
            goto LABEL_136;
          case 1u:
            v66 = *v31;
            v67 = v31[1];
            v68 = nullptr;
            if ( *v31 != v67 )
            {
              while ( *(_DWORD *)v66 != 1869379180 )
              {
                v66 += 16;
                if ( v66 == v67 )
                  goto LABEL_151;
              }
              if ( v66 == v67 )
                v68 = nullptr;
              else
                v68 = *(__int64 **)(v66 + 8);
            }
LABEL_151:
            if ( v68 == nullptr )
              v68 = &qword_141B5A4A0;
            v82 = sub_14159D690(v108, v68);
            if ( v82 < 0 )
              goto LABEL_181;
            v72 = v101;
            v3 = *(_QWORD **)(v101 + 8LL * (unsigned int)v82);
            if ( v3 == nullptr )
              goto LABEL_196;
            v83 = v3[24];
            v84 = v3[25] - v83;
            if ( v84 != 0 )
            {
              v85 = 1;
              if ( (unsigned __int64)(v84 >> 4) >= 2 )
                v85 = v84 >> 4;
              v86 = 0;
              while ( *(_DWORD *)(*(_QWORD *)(v83 + v86) + 12LL) != *(_DWORD *)(v100 + 12) )
              {
                v86 += 16;
                if ( --v85 == 0 )
                  goto LABEL_163;
              }
              sub_141758A00(v86 + v83, v83 + v86 + 16, v84 - v86 - 16);
              v3[25] -= 16LL;
            }
LABEL_163:
            v87 = *v31;
            v88 = v31[1];
            v89 = nullptr;
            if ( *v31 != v88 )
            {
              while ( *(_DWORD *)v87 != 1986096245 )
              {
                v87 += 16;
                if ( v87 == v88 )
                  goto LABEL_199;
              }
              if ( v87 == v88 )
                v89 = nullptr;
              else
                v89 = *(__int64 **)(v87 + 8);
            }
LABEL_199:
            if ( v89 != nullptr )
              v62 = v89;
            LOBYTE(v3) = sub_141735B40(&v100, v62) != 0;
            goto LABEL_182;
          case 2u:
            v69 = *v31;
            v70 = v31[1];
            v71 = nullptr;
            if ( *v31 != v70 )
            {
              while ( *(_DWORD *)v69 != 1869379180 )
              {
                v69 += 16;
                if ( v69 == v70 )
                  goto LABEL_170;
              }
              if ( v69 == v70 )
                v71 = nullptr;
              else
                v71 = *(__int64 **)(v69 + 8);
            }
LABEL_170:
            if ( v71 != nullptr )
              v62 = v71;
            v90 = sub_14159D690(v108, v62);
            if ( v90 < 0 )
              goto LABEL_181;
            v72 = v101;
            v91 = *(_QWORD *)(v101 + 8LL * (unsigned int)v90);
            if ( v91 == 0 )
            {
LABEL_196:
              LODWORD(v3) = 0;
              goto LABEL_183;
            }
            v92 = *(_QWORD *)(v91 + 192);
            LOBYTE(v3) = 1;
            v93 = *(_QWORD *)(v91 + 200) - v92;
            if ( v93 != 0 )
            {
              v94 = 1;
              if ( (unsigned __int64)(v93 >> 4) >= 2 )
                v94 = v93 >> 4;
              v95 = 0;
              while ( *(_DWORD *)(*(_QWORD *)(v92 + v95) + 12LL) != *(_DWORD *)(v100 + 12) )
              {
                v95 += 16;
                if ( --v94 == 0 )
                  goto LABEL_182;
              }
              sub_141758A00(v95 + v92, v92 + v95 + 16, v93 - v95 - 16);
              *(_QWORD *)(v91 + 200) -= 16LL;
            }
            goto LABEL_182;
          case 3u:
            v72 = v102;
            if ( v102 != v101 )
            {
              v73 = (v102 - v101) >> 3;
              while ( 1 )
              {
                v74 = *(_QWORD *)(v101 + 8 * v73-- - 8);
                if ( v74 != 0 )
                {
                  v75 = *(_QWORD *)(v74 + 192);
                  v76 = *(_QWORD *)(v74 + 200) - v75;
                  if ( v76 != 0 )
                  {
                    v77 = v76 >> 4;
                    if ( (unsigned __int64)(v76 >> 4) < 2 )
                      v77 = 1;
                    v78 = 0;
                    while ( *(_DWORD *)(*(_QWORD *)(v75 + v78) + 12LL) != *(_DWORD *)(v100 + 12) )
                    {
                      v78 += 16;
                      if ( --v77 == 0 )
                        goto LABEL_122;
                    }
                    sub_141758A00(v78 + v75, v75 + v78 + 16, v76 - v78 - 16);
                    *(_QWORD *)(v74 + 200) -= 16LL;
                  }
                }
LABEL_122:
                LOBYTE(v3) = 1;
                if ( v73 == 0 )
                  goto LABEL_182;
              }
            }
            LOBYTE(v3) = 1;
            if ( v102 == 0 )
              return (unsigned int)v3;
            goto LABEL_183;
          case 4u:
            v63 = *v31;
            v64 = v31[1];
            v65 = nullptr;
            if ( *v31 == v64 )
              goto LABEL_145;
            break;
          case 5u:
            sub_140DF3CB0(0);
            LOBYTE(v3) = 1;
            goto LABEL_182;
          default:
            goto LABEL_181;
        }
        while ( *(_DWORD *)v63 != 1869379180 )
        {
          v63 += 16;
          if ( v63 == v64 )
            goto LABEL_145;
        }
LABEL_136:
        if ( v63 == v64 )
          v65 = nullptr;
        else
          v65 = *(__int64 **)(v63 + 8);
LABEL_145:
        if ( v65 != nullptr )
          v62 = v65;
        v79 = qword_141B5FDD0;
        LODWORD(v3) = 0;
        sub_140FE7960(&v104, v62, 0);
        v80 = sub_14002F670(v79, &v104);
        if ( v80 == 0 )
          goto LABEL_182;
        v81 = v80;
        if ( sub_141048140(v80, *(unsigned int *)(v100 + 12), 0xFFFFFFFFLL, 0xFFFFFFFFLL) == 0 )
        {
          v104 = v100;
          v105 = 0x76C0001076C0001LL;
          sub_14104DD70(v81, &v104);
          LOBYTE(v3) = 1;
          goto LABEL_182;
        }
      }
    }
    else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(v30 + 8))(v29, a3) == 11 )
    {
      v3 = (_QWORD *)(*(__int64 (__fastcall **)(__int64 *, __int64 **, _QWORD))(**a3 + 184))(*a3, a3, 0);
      if ( v102 != v101 )
      {
        v45 = (v102 - v101) >> 3;
        do
        {
          v46 = *(_QWORD *)(v101 + 8 * v45-- - 8);
          if ( v46 != 0 )
          {
            v47 = *(_QWORD *)(v46 + 192);
            v48 = *(_QWORD *)(v46 + 200) - v47;
            if ( v48 != 0 )
            {
              v49 = v48 >> 4;
              if ( (unsigned __int64)(v48 >> 4) < 2 )
                v49 = 1;
              v50 = 0;
              while ( *(_DWORD *)(*(_QWORD *)(v47 + v50) + 12LL) != *(_DWORD *)(v100 + 12) )
              {
                v50 += 16;
                if ( --v49 == 0 )
                  goto LABEL_69;
              }
              sub_141758A00(v50 + v47, v47 + v50 + 16, v48 - v50 - 16);
              *(_QWORD *)(v46 + 200) -= 16LL;
            }
          }
LABEL_69:
          ;
        }
        while ( v45 != 0 );
      }
      v51 = v3[1] - *v3;
      if ( v51 != 0 )
      {
        v52 = v51 >> 3;
        v53 = 1;
        if ( v52 >= 2 )
          v53 = v52;
        for ( k = 0; k != v53; ++k )
        {
          v55 = *(__int64 **)(*v3 + 8 * k);
          if ( v55 == nullptr )
            v55 = &qword_141B5A4A0;
          v56 = qword_141B5FDD0;
          sub_140FE7960(&v104, v55, 0);
          v57 = sub_14002F670(v56, &v104);
          if ( v57 != 0 )
          {
            v58 = v57;
            if ( sub_141048140(v57, *(unsigned int *)(v100 + 12), 0xFFFFFFFFLL, 0xFFFFFFFFLL) == 0 )
            {
              v104 = v100;
              v105 = 0x76C0001076C0001LL;
              sub_14104DD70(v58, &v104);
            }
          }
        }
      }
      v59 = qword_141B60C38;
      v60 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_91;
      while ( *(_DWORD *)v60 != 1986359923 )
      {
        v60 += 16;
        if ( v60 == qword_141B60C38 )
          goto LABEL_91;
      }
      if ( v60 == qword_141B60C38 || (LOBYTE(v3) = 1, *(_QWORD *)(v60 + 8) == 0) )
      {
LABEL_91:
        LOBYTE(v3) = 1;
        LOBYTE(v59) = 1;
        sub_140DF3CB0(v59);
      }
      goto LABEL_182;
    }
LABEL_181:
    LODWORD(v3) = 0;
LABEL_182:
    v72 = v101;
    if ( v101 != 0 )
    {
LABEL_183:
      v96 = v103 - v72;
      if ( v103 - v72 == -1 )
        v96 = *(unsigned int *)(v72 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v97 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v97) >> 3 > v96)
        && (v98 = *(_QWORD *)(v97 + 8 * v96)) != 0 )
      {
        MEMORY[0x1419475D8](v98 + 32, v72 - *(unsigned int *)(v98 + 120));
        v99 = *(_BYTE *)(v98 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v98 + 64)) != 0;
        if ( !v99 && *(_BYTE *)(v98 + 97) != 0 )
          sub_1412D33C0(v98);
      }
      else
      {
        MEMORY[0x141948990](v72 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    return (unsigned int)v3;
  }
  if ( (_DWORD)a2 == 1095200353 )
  {
    (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v100, a3);
    v7 = *(_QWORD *)(a1 + 32);
    if ( v7 != v100 )
    {
      if ( v7 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v7 - 4)) == 0 )
        sub_1412EC9A0(v7 - 4, v6);
      *(_QWORD *)(a1 + 32) = v100;
      goto LABEL_64;
    }
    goto LABEL_61;
  }
  if ( (_DWORD)a2 != 1095201646 )
    return sub_140FE2700((_DWORD *)a1, a2, a3);
  (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v100, a3);
  v7 = *(_QWORD *)(a1 + 40);
  if ( v7 == v100 )
  {
LABEL_61:
    if ( v7 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v7 - 4)) == 0 )
      sub_1412EC9A0(v7 - 4, v6);
    goto LABEL_64;
  }
  if ( v7 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v7 - 4)) == 0 )
    sub_1412EC9A0(v7 - 4, v6);
  *(_QWORD *)(a1 + 40) = v100;
LABEL_64:
  LOBYTE(v3) = 1;
  return (unsigned int)v3;
}
