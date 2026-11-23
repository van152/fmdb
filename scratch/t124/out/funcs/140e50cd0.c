__int64 __fastcall sub_140E50CD0(__int64 a1, int a2, __int64 *a3)
{
  __int64 *v5; // rbx
  int v6; // edi
  int v7; // edi
  __int64 v8; // rax
  __int64 *v9; // rax
  int v10; // eax
  unsigned __int16 v11; // cx
  int v12; // edi
  __int64 *v13; // rax
  int v14; // edi
  __int64 *v15; // rax
  int v16; // edi
  __int64 *v17; // rax
  int v18; // edi
  __int64 *v19; // rax
  __int64 v20; // rax
  unsigned int v21; // edi
  __int64 *v22; // rax
  __int64 v23; // rax
  bool v24; // zf
  __int64 v25; // rax
  __int64 v26; // rdx
  __int64 v27; // rax
  int v28; // edi
  __int64 *v29; // rax
  int v30; // edi
  __int64 *v31; // rax
  __int64 *v32; // rax
  __int64 v33; // rax
  __int64 v34; // rax
  __int64 v35; // rdx
  __int64 v36; // rax
  __int64 *v37; // rax
  __int64 *v38; // rax
  unsigned int v39; // edi
  __int64 *v40; // rax
  int v41; // edi
  __int64 *v42; // rax
  __int64 v43; // rax
  unsigned __int64 v44; // rax
  __int64 *v45; // rax
  int v46; // edi
  __int64 *v47; // rax
  int v48; // edi
  __int64 *v49; // rax
  int v50; // edi
  __int64 *v51; // rax
  __int64 *v52; // rax
  unsigned int v53; // edi
  __int64 *v54; // rax
  unsigned int v55; // ecx
  unsigned int v56; // eax
  __int64 v57; // rdx
  __int64 v58; // rax
  __int64 v59; // rdx
  __int64 *v60; // rcx
  __int64 v61; // rcx
  char v62; // dl
  _QWORD *v63; // rdi
  int v64; // eax
  __int64 v65; // rdx
  float v66; // xmm0_4
  unsigned __int64 v67; // rax
  float v68; // xmm1_4
  __int64 v69; // rax
  __int64 v70; // rcx
  __int64 v71; // rdx
  __int64 *v72; // rax
  int v73; // eax
  int v74; // edi
  __int64 *v75; // rcx
  __int64 *v76; // rax
  __int64 v77; // rax
  __int64 v78; // rax
  __int64 v79; // rax
  __int64 v80; // rax
  __int64 v81; // rax
  __int64 v82; // rax
  __int64 v83; // rax
  __int64 v84; // rax
  __int64 v85; // rax
  __int64 v86; // rax
  __int64 v87; // rax
  __int64 v88; // rax
  __int64 v89; // rax
  __int64 v90; // rax
  __int64 v91; // rax
  __int64 v92; // rax
  __int64 v93; // rcx
  __int64 v94; // rax
  int v95; // edi
  __int64 *v96; // rax
  int v97; // edi
  __int64 *v98; // rax
  __int64 v99; // rax
  unsigned int v100; // ecx
  unsigned int v101; // eax
  int v102; // edi
  __int64 *v103; // rax
  __int64 *v104; // rax
  _QWORD *v106; // rdx
  _QWORD *v107; // rcx
  _BYTE v108[24]; // [rsp+28h] [rbp-48h] BYREF
  __int64 v109; // [rsp+40h] [rbp-30h] BYREF
  __int64 v110; // [rsp+48h] [rbp-28h]
  __int64 *v111; // [rsp+50h] [rbp-20h] BYREF
  __int64 v112; // [rsp+58h] [rbp-18h]
  __int64 v113; // [rsp+68h] [rbp-8h]

  v113 = -2;
  LODWORD(v5) = 0;
  if ( a2 > 1348759393 )
  {
    if ( a2 <= 1885565538 )
    {
      if ( a2 <= 1349416040 )
      {
        if ( a2 <= 1349083503 )
        {
          if ( a2 == 1348759394 )
          {
            v74 = *(unsigned __int16 *)(a1 + 90);
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
            LODWORD(v112) = (v74 << 17) | 0x100;
            v75 = &qword_141B5C8A0;
            v111 = &qword_141B5C8A0;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v76 = v111;
              a3[1] = v112;
              *a3 = (__int64)v76;
              v75 = (__int64 *)(sub_14083D4F0() + 8);
              v112 = 0;
              v111 = v75;
            }
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v75 + 16))(v75, &v111);
            goto LABEL_207;
          }
          if ( a2 != 1348761185 )
            return (unsigned int)v5;
          v16 = *(_DWORD *)(a1 + 72);
          v8 = sub_14083D4F0() + 40;
          LODWORD(v112) = v16;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v17 = v111;
            a3[1] = v112;
            *a3 = (__int64)v17;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        }
        if ( a2 == 1349083504 )
        {
          v95 = *(unsigned __int8 *)(a1 + 100);
          v8 = sub_14083D4F0() + 56;
          LODWORD(v112) = v95;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v96 = v111;
            a3[1] = v112;
            *a3 = (__int64)v96;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        }
        if ( a2 != 1349411177 )
          return (unsigned int)v5;
        v20 = *(_QWORD *)(a1 + 40);
        if ( v20 != 0 )
          goto LABEL_146;
        goto LABEL_199;
      }
      if ( a2 <= 1685417576 )
      {
        if ( a2 != 1349416041 )
        {
          if ( a2 != 1349810544 )
            return (unsigned int)v5;
          v30 = *(char *)(a1 + 101);
          v8 = sub_14083D4F0() + 40;
          LODWORD(v112) = v30;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v31 = v111;
            a3[1] = v112;
            *a3 = (__int64)v31;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        }
        v99 = *(_QWORD *)(a1 + 48);
        if ( v99 != 0 )
        {
          v100 = *(_DWORD *)(v99 + 12);
          v101 = *(_DWORD *)(v99 + 16);
          if ( v101 == 0 )
            v101 = v100;
          v111 = (__int64 *)__PAIR64__(v101, v100);
          v57 = 1315856756;
          goto LABEL_198;
        }
        goto LABEL_199;
      }
      if ( a2 == 1685417577 )
      {
        v50 = *(_DWORD *)(a1 + 12);
        v8 = sub_14083D4F0() + 40;
        LODWORD(v112) = v50;
        v111 = (__int64 *)v8;
        if ( &v111 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v51 = v111;
          a3[1] = v112;
          *a3 = (__int64)v51;
          v8 = sub_14083D4F0() + 8;
          v112 = 0;
          v111 = (__int64 *)v8;
        }
        goto LABEL_205;
      }
      if ( a2 == 1885500270 )
      {
        v8 = sub_14083D4F0() + 24;
        LOBYTE(v112) = 1;
        v111 = (__int64 *)v8;
        if ( &v111 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v52 = v111;
          a3[1] = v112;
          *a3 = (__int64)v52;
          v8 = sub_14083D4F0() + 8;
          v112 = 0;
          v111 = (__int64 *)v8;
        }
        goto LABEL_205;
      }
      if ( a2 != 1885563241 )
        return (unsigned int)v5;
      if ( (*(_BYTE *)(a1 + 101) & 0xFE) != 2 || *(_BYTE *)(a1 + 100) == 0 )
        goto LABEL_206;
      v10 = *(unsigned __int16 *)(a1 + 90);
      v11 = word_141AB0260;
      if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
      {
        word_141AB0260 = 2023;
        v11 = 2023;
      }
      if ( v11 - 35 >= v10 )
        goto LABEL_206;
    }
    else
    {
      if ( a2 <= 1886286445 )
      {
        if ( a2 <= 1885954914 )
        {
          if ( a2 != 1885565539 && a2 != 1885565550 )
            return (unsigned int)v5;
          v23 = *(_QWORD *)(a1 + 32);
          if ( v23 != 0 )
          {
            v24 = *(_BYTE *)(v23 + 47) == 0;
            v25 = *(_QWORD *)(v23 + 48);
            v26 = 368;
            if ( v24 )
              v26 = 216;
            v27 = *(_QWORD *)(v25 + v26);
            if ( v27 != 0 && *(_QWORD *)(v27 + 240) != 0 && *(__int16 *)(a1 + 82) >= 6001 )
              goto LABEL_217;
          }
          v8 = sub_14083D4F0() + 24;
          LOBYTE(v112) = 0;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v37 = v111;
            a3[1] = v112;
            *a3 = (__int64)v37;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        }
        if ( a2 != 1885954915 )
        {
          if ( a2 == 1886282100 )
          {
            v8 = sub_14083D4F0() + 24;
            LOBYTE(v112) = 1;
            v111 = (__int64 *)v8;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v45 = v111;
              a3[1] = v112;
              *a3 = (__int64)v45;
              v8 = sub_14083D4F0() + 8;
              v112 = 0;
              v111 = (__int64 *)v8;
            }
            goto LABEL_205;
          }
          if ( a2 != 1886286435 )
            return (unsigned int)v5;
LABEL_103:
          v33 = *(_QWORD *)(a1 + 32);
          if ( v33 != 0 )
          {
            v24 = *(_BYTE *)(v33 + 47) == 0;
            v34 = *(_QWORD *)(v33 + 48);
            v35 = 368;
            if ( v24 )
              v35 = 216;
            v36 = *(_QWORD *)(v34 + v35);
            if ( v36 != 0 && *(_QWORD *)(v36 + 240) != 0 && *(__int16 *)(a1 + 82) >= 4501 )
              goto LABEL_217;
          }
          v8 = sub_14083D4F0() + 24;
          LOBYTE(v112) = 0;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v38 = v111;
            a3[1] = v112;
            *a3 = (__int64)v38;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        }
        v43 = *(_QWORD *)(a1 + 32);
        if ( v43 != 0 )
        {
          v44 = *(unsigned int *)(v43 + 8);
          if ( (v44 & 0x80000000) == 0LL
            && (qword_141B61A68 - qword_141B61A60) >> 2 > v44
            && *(int *)(qword_141B61A60 + 4 * v44) > 0 )
          {
            goto LABEL_217;
          }
        }
LABEL_206:
        LOBYTE(v112) = 0;
        v111 = (__int64 *)(sub_14083D4F0() + 24);
        sub_14083DFA0(a3, &v111);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
        goto LABEL_207;
      }
      if ( a2 <= 1886675821 )
      {
        if ( a2 != 1886286446 )
        {
          if ( a2 != 1886545014 )
            return (unsigned int)v5;
          v8 = sub_14083D4F0() + 24;
          LOBYTE(v112) = 1;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v32 = v111;
            a3[1] = v112;
            *a3 = (__int64)v32;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        }
        goto LABEL_103;
      }
      switch ( a2 )
      {
        case 1886675822:
          v58 = *(_QWORD *)(a1 + 32);
          if ( v58 == 0 )
            goto LABEL_203;
          v59 = *(_QWORD *)(v58 + 48);
          v60 = (__int64 *)(v59 + 368);
          if ( *(_BYTE *)(v58 + 47) == 0 )
            v60 = (__int64 *)(v59 + 216);
          v61 = *v60;
          if ( v61 == 0 )
            goto LABEL_203;
          v62 = *(_BYTE *)(v59 + 185);
          if ( v62 == 0 || (v5 = *(__int64 **)(v61 + 272)) == nullptr )
            v5 = *(__int64 **)(v61 + 264);
          v63 = (_QWORD *)v5[3];
          if ( v63 == (_QWORD *)v5[4] || *v63 == 0 )
            goto LABEL_203;
          v64 = *(__int16 *)(v58 + 168);
          if ( v62 == 0 || (v65 = *(_QWORD *)(v61 + 272)) == 0 )
            v65 = *(_QWORD *)(v61 + 264);
          v66 = (float)v64;
          v67 = *(unsigned int *)(**(_QWORD **)(v65 + 24) + 8LL);
          v68 = 0.0;
          if ( (v67 & 0x80000000) == 0LL && (qword_141B61A68 - qword_141B61A60) >> 2 > v67 )
            v68 = (float)*(int *)(qword_141B61A60 + 4 * v67) * MEMORY[0x141770830];
          if ( v66 <= v68 )
          {
LABEL_203:
            v8 = sub_14083D4F0() + 24;
            LOBYTE(v112) = 0;
            v111 = (__int64 *)v8;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v104 = v111;
              a3[1] = v112;
              *a3 = (__int64)v104;
              v8 = sub_14083D4F0() + 8;
              v112 = 0;
              v111 = (__int64 *)v8;
            }
            goto LABEL_205;
          }
          break;
        case 1886676078:
          v69 = *(_QWORD *)(a1 + 32);
          if ( v69 == 0 )
            goto LABEL_170;
          v70 = *(_QWORD *)(v69 + 48);
          if ( v70 == 0 )
            goto LABEL_170;
          v71 = *(_QWORD *)(v69 + 80);
          if ( v71 == 0 || *(_BYTE *)(v71 + 418) != 0 )
            goto LABEL_170;
          v106 = (_QWORD *)(v70 + 368);
          v107 = (_QWORD *)(v70 + 216);
          if ( *(_BYTE *)(v69 + 47) != 0 )
            v107 = v106;
          if ( *v107 == 0 )
          {
LABEL_170:
            v8 = sub_14083D4F0() + 24;
            LOBYTE(v112) = 0;
            v111 = (__int64 *)v8;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v72 = v111;
              a3[1] = v112;
              *a3 = (__int64)v72;
              v8 = sub_14083D4F0() + 8;
              v112 = 0;
              v111 = (__int64 *)v8;
            }
            goto LABEL_205;
          }
          break;
        case 1919250549:
          v12 = *(__int16 *)(a1 + 92);
          v8 = sub_14083D4F0() + 40;
          LODWORD(v112) = v12;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v13 = v111;
            a3[1] = v112;
            *a3 = (__int64)v13;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
          goto LABEL_205;
        default:
          return (unsigned int)v5;
      }
    }
LABEL_217:
    LOBYTE(v112) = 1;
    v111 = (__int64 *)(sub_14083D4F0() + 24);
    sub_14083DFA0(a3, &v111);
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
    goto LABEL_207;
  }
  if ( a2 <= 1346587214 )
  {
    if ( a2 > 1315140209 )
    {
      if ( a2 <= 1315992672 )
      {
        if ( a2 == 1315140210 )
        {
          v97 = *(__int16 *)(a1 + 82);
          v8 = sub_14083D4F0() + 40;
          LODWORD(v112) = v97;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v98 = v111;
            a3[1] = v112;
            *a3 = (__int64)v98;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
        }
        else
        {
          if ( a2 != 1315466610 )
            return (unsigned int)v5;
          v28 = *(__int16 *)(a1 + 84);
          v8 = sub_14083D4F0() + 40;
          LODWORD(v112) = v28;
          v111 = (__int64 *)v8;
          if ( &v111 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v29 = v111;
            a3[1] = v112;
            *a3 = (__int64)v29;
            v8 = sub_14083D4F0() + 8;
            v112 = 0;
            v111 = (__int64 *)v8;
          }
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1315992673:
            v46 = *(__int16 *)(a1 + 88);
            v8 = sub_14083D4F0() + 40;
            LODWORD(v112) = v46;
            v111 = (__int64 *)v8;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v47 = v111;
              a3[1] = v112;
              *a3 = (__int64)v47;
              v8 = sub_14083D4F0() + 8;
              v112 = 0;
              v111 = (__int64 *)v8;
            }
            break;
          case 1316450930:
            v48 = *(__int16 *)(a1 + 80);
            v8 = sub_14083D4F0() + 40;
            LODWORD(v112) = v48;
            v111 = (__int64 *)v8;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v49 = v111;
              a3[1] = v112;
              *a3 = (__int64)v49;
              v8 = sub_14083D4F0() + 8;
              v112 = 0;
              v111 = (__int64 *)v8;
            }
            break;
          case 1346584898:
            v7 = *(__int16 *)(a1 + 86);
            v8 = sub_14083D4F0() + 40;
            LODWORD(v112) = v7;
            v111 = (__int64 *)v8;
            if ( &v111 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v9 = v111;
              a3[1] = v112;
              *a3 = (__int64)v9;
              v8 = sub_14083D4F0() + 8;
              v112 = 0;
              v111 = (__int64 *)v8;
            }
            break;
          default:
            return (unsigned int)v5;
        }
      }
      goto LABEL_205;
    }
    if ( a2 > 1112756291 )
    {
      if ( a2 == 1112756292 )
      {
        sub_1407C9510(&v111);
        sub_1407C9510(v108);
        v77 = sub_14083D4F0();
        LODWORD(v110) = 1348695145;
        v109 = v77 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v78 = sub_14083D4F0();
        LODWORD(v110) = 1346587215;
        v109 = v78 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v79 = sub_14083D4F0();
        LODWORD(v110) = 1347635791;
        v109 = v79 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v80 = sub_14083D4F0();
        LODWORD(v110) = 1349411177;
        v109 = v80 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v81 = sub_14083D4F0();
        LODWORD(v110) = 1098081136;
        v109 = v81 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v82 = sub_14083D4F0();
        LODWORD(v110) = 1349416041;
        v109 = v82 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v83 = sub_14083D4F0();
        LODWORD(v110) = 1349413487;
        v109 = v83 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v84 = sub_14083D4F0();
        LODWORD(v110) = 1346584898;
        v109 = v84 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v85 = sub_14083D4F0();
        LODWORD(v110) = 1347436866;
        v109 = v85 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v86 = sub_14083D4F0();
        LODWORD(v110) = 1346589264;
        v109 = v86 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v87 = sub_14083D4F0();
        LODWORD(v110) = 1346916944;
        v109 = v87 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v88 = sub_14083D4F0();
        LODWORD(v110) = 1347899984;
        v109 = v88 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v89 = sub_14083D4F0();
        LODWORD(v110) = 1348759394;
        v109 = v89 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v90 = sub_14083D4F0();
        LODWORD(v110) = 1349083504;
        v109 = v90 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v91 = sub_14083D4F0();
        LODWORD(v110) = 1349810544;
        v109 = v91 + 56;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        v92 = sub_14083D4F0();
        LODWORD(v110) = 1112490825;
        v109 = v92 + 56;
        v5 = &v109;
        sub_14083B5F0(v108, &v109);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v109 + 16LL))(v109, &v109);
        sub_1407EAFE0(a1, &v111, v108);
        sub_14083DDA0(&v109, &v111);
        v93 = *a3;
        if ( &v109 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v93 + 16LL))(v93, a3);
          v94 = v109;
          a3[1] = v110;
          *a3 = v94;
          v93 = sub_14083D4F0() + 8;
          v110 = 0;
          v109 = v93;
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v93 + 16LL))(v93, &v109);
        sub_14083B0A0(v108);
        sub_140833970(&v111);
        goto LABEL_207;
      }
      if ( a2 != 1315140193 )
        return (unsigned int)v5;
      v18 = *(__int16 *)(a1 + 86);
      v8 = sub_14083D4F0() + 40;
      LODWORD(v112) = v18;
      v111 = (__int64 *)v8;
      if ( &v111 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v19 = v111;
        a3[1] = v112;
        *a3 = (__int64)v19;
        v8 = sub_14083D4F0() + 8;
        v112 = 0;
        v111 = (__int64 *)v8;
      }
      goto LABEL_205;
    }
    if ( a2 != 1098081136 )
    {
      if ( a2 != 1112490825 )
        return (unsigned int)v5;
      v14 = *(_DWORD *)(a1 + 8);
      v8 = sub_14083D4F0() + 40;
      LODWORD(v112) = v14;
      v111 = (__int64 *)v8;
      if ( &v111 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v15 = v111;
        a3[1] = v112;
        *a3 = (__int64)v15;
        v8 = sub_14083D4F0() + 8;
        v112 = 0;
        v111 = (__int64 *)v8;
      }
      goto LABEL_205;
    }
    if ( *(_BYTE *)(a1 + 101) == 18 )
    {
      v73 = *(unsigned __int16 *)(a1 + 80);
      if ( v73 == 4250 )
      {
        LODWORD(v112) = 1;
        v111 = (__int64 *)(sub_14083D4F0() + 40);
        sub_14083DFA0(a3, &v111);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
      }
      else if ( v73 == 6250 )
      {
        LODWORD(v112) = 2;
        v111 = (__int64 *)(sub_14083D4F0() + 40);
        sub_14083DFA0(a3, &v111);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
      }
      else
      {
        if ( v73 == 7750 )
          LODWORD(v112) = 3;
        else
          LODWORD(v112) = 0;
        v111 = (__int64 *)(sub_14083D4F0() + 40);
        sub_14083DFA0(a3, &v111);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
      }
      goto LABEL_207;
    }
    goto LABEL_199;
  }
  if ( a2 > 1347436865 )
  {
    if ( a2 <= 1347899983 )
    {
      if ( a2 == 1347436866 )
      {
        v102 = *(__int16 *)(a1 + 88);
        v8 = sub_14083D4F0() + 40;
        LODWORD(v112) = v102;
        v111 = (__int64 *)v8;
        if ( &v111 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v103 = v111;
          a3[1] = v112;
          *a3 = (__int64)v103;
          v8 = sub_14083D4F0() + 8;
          v112 = 0;
          v111 = (__int64 *)v8;
        }
        goto LABEL_205;
      }
      if ( a2 != 1347635791 )
        return (unsigned int)v5;
      v6 = *(unsigned __int16 *)(a1 + 96);
      if ( *(_WORD *)(a1 + 96) != 0 )
        goto LABEL_190;
    }
    else
    {
      if ( a2 == 1347899984 )
      {
        v53 = ((unsigned int)(5243 * *(__int16 *)(a1 + 80)) >> 31) + ((5243 * *(__int16 *)(a1 + 80)) >> 18);
        v8 = sub_14083D4F0() + 40;
        LODWORD(v112) = v53;
        v111 = (__int64 *)v8;
        if ( &v111 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v54 = v111;
          a3[1] = v112;
          *a3 = (__int64)v54;
          v8 = sub_14083D4F0() + 8;
          v112 = 0;
          v111 = (__int64 *)v8;
        }
        goto LABEL_205;
      }
      if ( a2 != 1348695145 )
      {
        if ( a2 == 1348695927 )
        {
          if ( *(int *)(a1 + 76) > 0 )
          {
            LODWORD(v112) = *(_DWORD *)(a1 + 76);
            v111 = (__int64 *)(sub_14083D4F0() + 40);
            sub_14083DFA0(a3, &v111);
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
LABEL_207:
            LOBYTE(v5) = 1;
            return (unsigned int)v5;
          }
          LOBYTE(v5) = 1;
          if ( a3 != &qword_141B5A4A0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
              qword_141B5A4A0,
              &qword_141B5A4A0,
              a3);
          }
        }
        return (unsigned int)v5;
      }
      v20 = *(_QWORD *)(a1 + 32);
      if ( v20 != 0 )
      {
LABEL_146:
        v55 = *(_DWORD *)(v20 + 12);
        v56 = *(_DWORD *)(v20 + 16);
        if ( v56 == 0 )
          v56 = v55;
        v111 = (__int64 *)__PAIR64__(v56, v55);
        v57 = 1416914273;
LABEL_198:
        sub_140FE72B0(&v111, v57, a3);
        goto LABEL_207;
      }
    }
LABEL_199:
    LODWORD(v5) = 0;
    return (unsigned int)v5;
  }
  if ( a2 <= 1346916943 )
  {
    if ( a2 == 1346587215 )
    {
      v6 = *(unsigned __int16 *)(a1 + 94);
      if ( *(_WORD *)(a1 + 94) != 0 )
      {
LABEL_190:
        LODWORD(v112) = v6;
        v111 = (__int64 *)(sub_14083D4F0() + 56);
        sub_14083DFA0(a3, &v111);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v111 + 16))(v111, &v111);
        goto LABEL_207;
      }
      goto LABEL_199;
    }
    if ( a2 != 1346589264 )
      return (unsigned int)v5;
    v21 = ((unsigned int)(5243 * *(__int16 *)(a1 + 82)) >> 31) + ((5243 * *(__int16 *)(a1 + 82)) >> 18);
    v8 = sub_14083D4F0() + 40;
    LODWORD(v112) = v21;
    v111 = (__int64 *)v8;
    if ( &v111 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v22 = v111;
      a3[1] = v112;
      *a3 = (__int64)v22;
      v8 = sub_14083D4F0() + 8;
      v112 = 0;
      v111 = (__int64 *)v8;
    }
LABEL_205:
    v5 = *(__int64 **)v8;
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v8 + 16LL))(v8, &v111);
    goto LABEL_207;
  }
  switch ( a2 )
  {
    case 1346916944:
      v39 = ((unsigned int)(5243 * *(__int16 *)(a1 + 84)) >> 31) + ((5243 * *(__int16 *)(a1 + 84)) >> 18);
      v8 = sub_14083D4F0() + 40;
      LODWORD(v112) = v39;
      v111 = (__int64 *)v8;
      if ( &v111 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v40 = v111;
        a3[1] = v112;
        *a3 = (__int64)v40;
        v8 = sub_14083D4F0() + 8;
        v112 = 0;
        v111 = (__int64 *)v8;
      }
      goto LABEL_205;
    case 1347182951:
      v41 = *(char *)(a1 + 104);
      v8 = sub_14083D4F0() + 40;
      LODWORD(v112) = v41;
      v111 = (__int64 *)v8;
      if ( &v111 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v42 = v111;
        a3[1] = v112;
        *a3 = (__int64)v42;
        v8 = sub_14083D4F0() + 8;
        v112 = 0;
        v111 = (__int64 *)v8;
      }
      goto LABEL_205;
    case 1347308111:
      v6 = *(unsigned __int16 *)(a1 + 98);
      if ( *(_WORD *)(a1 + 98) != 0 )
        goto LABEL_190;
      goto LABEL_199;
    default:
      break;
  }
  return (unsigned int)v5;
}
