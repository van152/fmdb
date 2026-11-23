__int64 __fastcall sub_140E4A470(__int64 a1, int a2, __int64 *a3)
{
  __int64 v3; // rbx
  int v7; // esi
  __int64 v8; // rax
  int v9; // esi
  __int64 v10; // rax
  __int64 *v11; // rax
  int v12; // esi
  __int64 *v13; // rax
  int v14; // esi
  __int64 *v15; // rax
  int v16; // esi
  int v17; // edi
  int v18; // eax
  int v19; // esi
  bool v20; // zf
  int v21; // eax
  __int64 v22; // rcx
  __int64 v23; // rax
  int v24; // esi
  __int64 *v25; // rax
  int v26; // esi
  int v27; // esi
  __int64 *v28; // rax
  int v29; // esi
  __int64 *v30; // rax
  __int64 v31; // rcx
  int v32; // eax
  int v33; // ecx
  char v34; // bl
  __int64 *v35; // rax
  char v36; // bl
  __int64 *v37; // rax
  __int64 *v38; // rcx
  __int64 *v39; // rax
  __int64 v40; // rcx
  int v41; // eax
  int v42; // ecx
  __int64 *v43; // rax
  int v44; // esi
  __int64 *v45; // rax
  int v46; // esi
  __int64 *v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rsi
  __int64 v50; // rdx
  __int64 v51; // r12
  __int64 v52; // rsi
  __int64 v53; // rsi
  __int64 *v54; // r15
  __int64 v55; // rax
  __int64 v56; // rcx
  __int64 *v57; // rax
  __int64 *v59; // rax
  __int64 v60; // rsi
  __int64 v61; // rax
  char v62; // di
  __int64 v63; // rax
  __int64 v64; // rax
  unsigned __int64 v65; // r14
  __int64 *v66; // rsi
  __int64 v67; // rbx
  int v68; // esi
  int v69; // edi
  int v70; // eax
  int v71; // esi
  char v72; // si
  unsigned __int64 v73; // rcx
  void (__fastcall ***v74)(_QWORD, __int64); // rcx
  __int64 v75; // rbx
  __int64 v76; // r12
  bool v77; // al
  unsigned __int64 v78; // rcx
  __int64 v79; // rbx
  __int64 v80; // rbx
  bool v81; // al
  __int64 *v82; // rax
  char v83; // bl
  __int64 *v84; // rax
  __int64 *v85; // rax
  char v86; // bl
  __int64 *v87; // rax
  int v88; // esi
  __int64 *v89; // rax
  int v90; // esi
  __int64 *v91; // rax
  int v92; // esi
  __int64 *v93; // rax
  int v94; // esi
  __int64 *v95; // rax
  __int64 v96; // rax
  __int64 v97; // rcx
  int v98; // eax
  int v99; // ecx
  __int64 *v100; // r15
  __int64 v101; // rax
  __int64 v102; // rcx
  __int64 *v103; // rax
  int v104; // esi
  __int64 *v105; // rax
  int v106; // esi
  __int64 *v107; // rax
  __int64 v108; // rdx
  unsigned __int64 v109; // rdi
  __int64 v110; // r14
  __int64 v111; // r15
  unsigned __int64 v112; // rcx
  __int64 v113; // r8
  __int64 v114; // rcx
  bool v115; // al
  __int64 v116; // rdx
  __int64 v117; // rax
  __int64 *v118; // rax
  __int64 v119; // rsi
  __int64 v120; // rdi
  __int64 v121; // rax
  __int64 v122; // rcx
  __int64 v123; // rax
  __int64 *v124; // [rsp+28h] [rbp-58h]
  __int64 v125; // [rsp+30h] [rbp-50h]
  __int64 v126; // [rsp+38h] [rbp-48h]
  _QWORD v127[2]; // [rsp+40h] [rbp-40h] BYREF
  _QWORD v128[2]; // [rsp+50h] [rbp-30h] BYREF
  __int64 v129; // [rsp+60h] [rbp-20h] BYREF
  __int64 v130; // [rsp+68h] [rbp-18h]
  __int64 v131; // [rsp+78h] [rbp-8h] BYREF
  __int64 v132; // [rsp+80h] [rbp+0h] BYREF
  __int64 v133; // [rsp+88h] [rbp+8h]
  __int64 *v134; // [rsp+98h] [rbp+18h] BYREF
  __int64 v135; // [rsp+A0h] [rbp+20h] BYREF
  unsigned __int64 v136; // [rsp+A8h] [rbp+28h]
  __int64 v137; // [rsp+B0h] [rbp+30h]
  __int64 v138; // [rsp+B8h] [rbp+38h]
  __int64 v139; // [rsp+C0h] [rbp+40h]
  __int64 v140; // [rsp+D0h] [rbp+50h]
  __int64 v141; // [rsp+D8h] [rbp+58h]
  __int64 v142; // [rsp+E0h] [rbp+60h]
  __int64 v143; // [rsp+F0h] [rbp+70h]

  v143 = -2;
  if ( a2 <= 1096249953 )
  {
    if ( a2 <= 1096247666 )
    {
      if ( a2 <= 1096246120 )
      {
        if ( a2 > 1096245858 )
        {
          if ( a2 != 1096245859 )
          {
            if ( a2 == 1096245874 )
            {
              v29 = *(char *)(a1 + 131);
              v10 = sub_14083D4F0() + 40;
              LODWORD(v135) = v29;
              v134 = (__int64 *)v10;
              if ( &v134 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                v30 = v134;
                a3[1] = v135;
                *a3 = (__int64)v30;
                v10 = sub_14083D4F0() + 8;
                v135 = 0;
                v134 = (__int64 *)v10;
              }
              goto LABEL_221;
            }
            goto LABEL_112;
          }
          if ( dword_141B62F80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B62F80);
            if ( dword_141B62F80 == -1 )
            {
              sub_141336010(&qword_141B62F50);
              sub_141751048(sub_1413360A0);
              sub_141750EA0(&dword_141B62F80);
            }
          }
          LODWORD(v135) = *(_DWORD *)(a1 + 28);
          v38 = &qword_141B62F50;
          v134 = &qword_141B62F50;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v82 = v134;
            a3[1] = v135;
            *a3 = (__int64)v82;
            v38 = (__int64 *)(sub_14083D4F0() + 8);
            v135 = 0;
            v134 = v38;
          }
        }
        else
        {
          if ( a2 != 1096245604 )
          {
            if ( a2 == 1096245616 )
            {
              v24 = *(char *)(a1 + 136);
              v10 = sub_14083D4F0() + 40;
              LODWORD(v135) = v24;
              v134 = (__int64 *)v10;
              if ( &v134 != (__int64 **)a3 )
              {
                (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
                v25 = v134;
                a3[1] = v135;
                *a3 = (__int64)v25;
                v10 = sub_14083D4F0() + 8;
                v135 = 0;
                v134 = (__int64 *)v10;
              }
              goto LABEL_221;
            }
            goto LABEL_112;
          }
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
          LODWORD(v135) = ((*(_WORD *)(a1 + 76) & 0x1FF) << 8)
                        | (*(unsigned __int16 *)(a1 + 76) >> 9)
                        | (*(unsigned __int16 *)(a1 + 78) << 17);
          v38 = &qword_141B5C8A0;
          v134 = &qword_141B5C8A0;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v59 = v134;
            a3[1] = v135;
            *a3 = (__int64)v59;
            v38 = (__int64 *)(sub_14083D4F0() + 8);
            v135 = 0;
            v134 = v38;
          }
        }
        goto LABEL_184;
      }
      if ( a2 > 1096246385 )
      {
        if ( a2 == 1096246386 )
        {
          v90 = *(char *)(a1 + 130);
          v10 = sub_14083D4F0() + 40;
          LODWORD(v135) = v90;
          v134 = (__int64 *)v10;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v91 = v134;
            a3[1] = v135;
            *a3 = (__int64)v91;
            v10 = sub_14083D4F0() + 8;
            v135 = 0;
            v134 = (__int64 *)v10;
          }
          goto LABEL_221;
        }
        if ( a2 != 1096246883 )
        {
          if ( a2 == 1096246895 )
          {
            v9 = *(char *)(a1 + 142);
            v10 = sub_14083D4F0() + 40;
            LODWORD(v135) = v9;
            v134 = (__int64 *)v10;
            if ( &v134 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v11 = v134;
              a3[1] = v135;
              *a3 = (__int64)v11;
              v10 = sub_14083D4F0() + 8;
              v135 = 0;
              v134 = (__int64 *)v10;
            }
            goto LABEL_221;
          }
          goto LABEL_112;
        }
        if ( dword_141B62F80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B62F80);
          if ( dword_141B62F80 == -1 )
          {
            sub_141336010(&qword_141B62F50);
            sub_141751048(sub_1413360A0);
            sub_141750EA0(&dword_141B62F80);
          }
        }
        LODWORD(v135) = *(_DWORD *)(a1 + 24);
        v38 = &qword_141B62F50;
        v134 = &qword_141B62F50;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v85 = v134;
          a3[1] = v135;
          *a3 = (__int64)v85;
          v38 = (__int64 *)(sub_14083D4F0() + 8);
          v135 = 0;
          v134 = v38;
        }
        goto LABEL_184;
      }
      if ( a2 != 1096246121 )
      {
        if ( a2 != 1096246369 )
          goto LABEL_112;
        if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
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
        LODWORD(v135) = ((*(_WORD *)(a1 + 72) & 0x1FF) << 8)
                      | (*(unsigned __int16 *)(a1 + 72) >> 9)
                      | (*(unsigned __int16 *)(a1 + 74) << 17);
        v38 = &qword_141B5C8A0;
        v134 = &qword_141B5C8A0;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v39 = v134;
          a3[1] = v135;
          *a3 = (__int64)v39;
          v38 = (__int64 *)(sub_14083D4F0() + 8);
          v135 = 0;
          v134 = v38;
        }
        goto LABEL_184;
      }
      v97 = *(_QWORD *)(a1 + 80);
      if ( v97 != 0 )
      {
        v98 = *(_DWORD *)(v97 + 12);
        v99 = *(_DWORD *)(v97 + 16);
        if ( v99 == 0 )
          v99 = v98;
      }
      else
      {
        v98 = -1;
        v99 = -1;
      }
      v134 = (__int64 *)__PAIR64__(v99, v98);
      v116 = 1668247156;
LABEL_239:
      sub_140FE72B0(&v134, v116, a3);
      goto LABEL_259;
    }
    if ( a2 > 1096248928 )
    {
      if ( a2 > 1096248943 )
      {
        switch ( a2 )
        {
          case 1096248944:
            v92 = *(char *)(a1 + 139);
            v10 = sub_14083D4F0() + 40;
            LODWORD(v135) = v92;
            v134 = (__int64 *)v10;
            if ( &v134 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v93 = v134;
              a3[1] = v135;
              *a3 = (__int64)v93;
              v10 = sub_14083D4F0() + 8;
              v135 = 0;
              v134 = (__int64 *)v10;
            }
            goto LABEL_221;
          case 1096249200:
            v86 = *(_BYTE *)(a1 + 141);
            v10 = sub_14083D4F0() + 24;
            LOBYTE(v135) = (v86 & 2) != 0;
            v134 = (__int64 *)v10;
            if ( &v134 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v87 = v134;
              a3[1] = v135;
              *a3 = (__int64)v87;
              v10 = sub_14083D4F0() + 8;
              v135 = 0;
              v134 = (__int64 *)v10;
            }
            goto LABEL_221;
          case 1096249455:
            v14 = *(_DWORD *)(a1 + 120);
            v10 = sub_14083D4F0() + 56;
            LODWORD(v135) = v14;
            v134 = (__int64 *)v10;
            if ( &v134 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v15 = v134;
              a3[1] = v135;
              *a3 = (__int64)v15;
              v10 = sub_14083D4F0() + 8;
              v135 = 0;
              v134 = (__int64 *)v10;
            }
            goto LABEL_221;
          default:
            break;
        }
        goto LABEL_112;
      }
      if ( a2 == 1096248929 )
      {
        v100 = (__int64 *)(a1 + 48);
        v101 = sub_14083D4F0();
        v135 = 0;
        if ( &v135 != v100 )
        {
          v102 = *v100;
          if ( *v100 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v102 - 4));
          v135 = v102;
        }
        v10 = v101 + 136;
        v134 = (__int64 *)v10;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v103 = v134;
          a3[1] = v135;
          *a3 = (__int64)v103;
          v10 = sub_14083D4F0() + 8;
          v135 = 0;
          v134 = (__int64 *)v10;
        }
        goto LABEL_221;
      }
      if ( a2 != 1096248937 )
        goto LABEL_112;
      v40 = *(_QWORD *)(a1 + 96);
      if ( v40 != 0 )
      {
        v41 = *(_DWORD *)(v40 + 12);
        v42 = *(_DWORD *)(v40 + 16);
        if ( v42 == 0 )
          v42 = v41;
      }
      else
      {
        v41 = -1;
        v42 = -1;
      }
      v134 = (__int64 *)__PAIR64__(v42, v41);
      v116 = 1315856756;
      goto LABEL_239;
    }
    if ( a2 > 1096248678 )
    {
      if ( a2 == 1096248679 )
      {
        v26 = *(unsigned __int8 *)(a1 + 147);
        if ( (char)v26 <= 0 )
          goto LABEL_203;
        goto LABEL_202;
      }
      if ( a2 != 1096248681 )
        goto LABEL_112;
      v31 = *(_QWORD *)(a1 + 88);
      if ( v31 != 0 )
      {
        v32 = *(_DWORD *)(v31 + 12);
        v33 = *(_DWORD *)(v31 + 16);
        if ( v33 == 0 )
          v33 = v32;
      }
      else
      {
        v32 = -1;
        v33 = -1;
      }
      v134 = (__int64 *)__PAIR64__(v33, v32);
      v116 = 1668246896;
      goto LABEL_239;
    }
    if ( a2 != 1096247667 )
    {
      if ( a2 != 1096248673 )
        goto LABEL_112;
      v26 = *(unsigned __int8 *)(a1 + 144);
      if ( (char)v26 <= 0 )
        goto LABEL_203;
      goto LABEL_202;
    }
    v60 = sub_14083D4F0() + 8;
    v127[1] = 0;
    v127[0] = v60;
    v61 = sub_140FE35F0();
    if ( v61 != 0 )
    {
      sub_1410224E0(v61 + 1104, 1215196787, v127);
      v60 = v127[0];
    }
    v62 = 0;
    v63 = (*(__int64 (__fastcall **)(__int64, _QWORD *, _QWORD))(*(_QWORD *)v60 + 184LL))(v60, v127, 0);
    sub_14083ADC0(&v129, v63);
    v64 = v129;
    if ( v130 == v129 )
    {
LABEL_241:
      v117 = sub_14083D4F0() + 24;
      LOBYTE(v135) = v62;
      v134 = (__int64 *)v117;
      if ( &v134 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v118 = v134;
        a3[1] = v135;
        *a3 = (__int64)v118;
        v117 = sub_14083D4F0() + 8;
        v135 = 0;
        v134 = (__int64 *)v117;
      }
      v3 = *(_QWORD *)v117;
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v117 + 16LL))(v117, &v134);
      sub_14083B0A0(&v129);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v127[0] + 16LL))(v127[0], v127);
      goto LABEL_259;
    }
    v65 = 0;
    while ( 1 )
    {
      v66 = *(__int64 **)(v64 + 8 * v65);
      if ( v66 == nullptr )
        v66 = &qword_141B5A4A0;
      sub_14150F810(&v134);
      if ( dword_141B59E30 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
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
      if ( (__int64 *)*v66 == &qword_141B59E00 )
      {
        sub_140805330(&v131, v66[1]);
        v128[0] = v133;
        if ( v133 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v133 + 8));
        sub_1412D68A0(&v131);
        if ( v128[0] != 0 )
        {
          sub_14151C2A0(&v134, v128);
          v74 = (void (__fastcall ***)(_QWORD, __int64))v128[0];
          if ( v128[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v128[0] + 8LL)) == 0 )
            (**v74)(v74, 1);
        }
      }
      v67 = sub_14083D4F0() + 8;
      v128[1] = 0;
      v128[0] = v67;
      v68 = *(_DWORD *)(a1 + 8);
      v69 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 56LL))(a1);
      (*(void (__fastcall **)(__int64, _QWORD *, __int64 *))(*(_QWORD *)v67 + 24LL))(v67, v128, &v132);
      v70 = v68 & v69;
      v71 = (v69 << 24) | v68 & 0x7FFFFF;
      if ( v70 == -1 )
        v71 = -8388609;
      LODWORD(v131) = v71;
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v128[0] + 16LL))(v128[0], v128);
      v72 = sub_140FEB670(&v134, &v131);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v132 + 16LL))(v132, &v132);
      if ( v140 != 0 )
        break;
LABEL_146:
      if ( v137 == 0 )
        goto LABEL_157;
      v78 = v139 - v137;
      if ( v139 - v137 == -1 )
      {
        v78 = *(unsigned int *)(v137 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
          goto LABEL_155;
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_155;
      }
      v79 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v79) >> 3 > v78 )
      {
        v80 = *(_QWORD *)(v79 + 8 * v78);
        if ( v80 != 0 )
        {
          MEMORY[0x1419475D8](v80 + 32, v137 - *(unsigned int *)(v80 + 120));
          v81 = *(_BYTE *)(v80 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v80 + 64)) != 0;
          if ( !v81 && *(_BYTE *)(v80 + 97) != 0 )
            sub_1412D33C0(v80);
          goto LABEL_156;
        }
      }
LABEL_155:
      MEMORY[0x141948990](v137 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_156:
      v139 = 0;
      v138 = 0;
      v137 = 0;
LABEL_157:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v135 + 16LL))(v135, &v135);
      if ( v72 != 0 )
      {
        v62 = 1;
        goto LABEL_241;
      }
      ++v65;
      v64 = v129;
      if ( v65 >= (v130 - v129) >> 3 )
      {
        v62 = 0;
        goto LABEL_241;
      }
    }
    v73 = v142 - v140;
    if ( v142 - v140 == -1 )
    {
      v73 = *(unsigned int *)(v140 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_144;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_144;
    }
    v75 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v75) >> 3 > v73 )
    {
      v76 = *(_QWORD *)(v75 + 8 * v73);
      if ( v76 != 0 )
      {
        MEMORY[0x1419475D8](v76 + 32, v140 - *(unsigned int *)(v76 + 120));
        v77 = *(_BYTE *)(v76 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v76 + 64)) != 0;
        if ( !v77 && *(_BYTE *)(v76 + 97) != 0 )
          sub_1412D33C0(v76);
        goto LABEL_145;
      }
    }
LABEL_144:
    MEMORY[0x141948990](v140 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_145:
    v142 = 0;
    v141 = 0;
    v140 = 0;
    goto LABEL_146;
  }
  if ( a2 <= 1096250488 )
  {
    if ( a2 <= 1096250210 )
    {
      switch ( a2 )
      {
        case 1096249954:
          v106 = *(char *)(a1 + 133);
          v10 = sub_14083D4F0() + 40;
          LODWORD(v135) = v106;
          v134 = (__int64 *)v10;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v107 = v134;
            a3[1] = v135;
            *a3 = (__int64)v107;
            v10 = sub_14083D4F0() + 8;
            v135 = 0;
            v134 = (__int64 *)v10;
          }
          goto LABEL_221;
        case 1096249957:
          v104 = *(__int16 *)(a1 + 124);
          v10 = sub_14083D4F0() + 40;
          LODWORD(v135) = v104;
          v134 = (__int64 *)v10;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v105 = v134;
            a3[1] = v135;
            *a3 = (__int64)v105;
            v10 = sub_14083D4F0() + 8;
            v135 = 0;
            v134 = (__int64 *)v10;
          }
          goto LABEL_221;
        case 1096249972:
          v27 = *(char *)(a1 + 137);
          v10 = sub_14083D4F0() + 40;
          LODWORD(v135) = v27;
          v134 = (__int64 *)v10;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v28 = v134;
            a3[1] = v135;
            *a3 = (__int64)v28;
            v10 = sub_14083D4F0() + 8;
            v135 = 0;
            v134 = (__int64 *)v10;
          }
          goto LABEL_221;
        default:
          break;
      }
      goto LABEL_112;
    }
    switch ( a2 )
    {
      case 1096250211:
        v12 = *(char *)(a1 + 128);
        v10 = sub_14083D4F0() + 40;
        LODWORD(v135) = v12;
        v134 = (__int64 *)v10;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v13 = v134;
          a3[1] = v135;
          *a3 = (__int64)v13;
          v10 = sub_14083D4F0() + 8;
          v135 = 0;
          v134 = (__int64 *)v10;
        }
        goto LABEL_221;
      case 1096250212:
      case 1096250213:
      case 1096250214:
      case 1096250215:
      case 1096250217:
      case 1096250218:
      case 1096250219:
      case 1096250220:
      case 1096250221:
      case 1096250223:
      case 1096250224:
      case 1096250225:
        goto LABEL_112;
      case 1096250216:
        sub_14151D370(&v131, a1);
        v49 = v132 - v131;
        v50 = v132 - v131;
        if ( v132 == v131 )
        {
          v51 = 0;
          v53 = 0;
          v125 = 0;
        }
        else
        {
          if ( v132 - v131 < 0 )
            sub_1400526C0(v48, v50);
          v51 = sub_1407E4490(qword_141ABD470, v50);
          v125 = v51 + 8 * (v49 >> 3);
          v52 = v132 - v131;
          sub_141758A00(v51, v131, v132 - v131);
          v53 = v51 + v52;
        }
        sub_1407C9510(&v134);
        v108 = v53 - v51;
        v109 = (v53 - v51) >> 3;
        if ( (__int64)(v136 - (_QWORD)v134) >> 3 < v109 )
        {
          v124 = v134;
          if ( v108 < 0 )
            sub_1400526C0(v134, v108);
          v110 = v135;
          v111 = sub_1407E4490(qword_141ABD470, v108);
          sub_141758A00(v111, v134, v135 - (_QWORD)v134);
          LODWORD(v3) = (_DWORD)v134;
          if ( v134 != nullptr )
          {
            v112 = v136 - (_QWORD)v134;
            if ( v136 - (_QWORD)v134 == -1 )
              v112 = *(unsigned int *)((char *)v134 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v113 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v113) >> 3 > v112)
              && (v114 = *(_QWORD *)(v113 + 8 * v112)) != 0 )
            {
              v3 = (__int64)v134 - *(unsigned int *)(v114 + 120);
              v126 = v114;
              MEMORY[0x1419475D8](v114 + 32, v3);
              v115 = *(_BYTE *)(v126 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v126 + 64)) != 0;
              if ( !v115 && *(_BYTE *)(v126 + 97) != 0 )
                sub_1412D33C0(v126);
            }
            else
            {
              LODWORD(v3) = (_DWORD)v134 - *(_DWORD *)(qword_141ABD470 + 48);
              MEMORY[0x141948990]((char *)v134 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v134 = (__int64 *)v111;
          v135 = v111 + v110 - (_QWORD)v124;
          v136 = v111 + 8 * v109;
        }
        if ( v53 != v51 )
        {
          v3 = 1;
          if ( v109 >= 2 )
            v3 = (v53 - v51) >> 3;
          v119 = 0;
          do
          {
            v120 = *(_QWORD *)(v51 + 8 * v119);
            if ( v120 != 0 )
            {
              v121 = sub_14083D4F0();
              v130 = 0;
              v129 = v121 + 8;
              sub_140E4DC70(v120, &v129);
              sub_14083B5F0(&v134, &v129);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v129 + 16LL))(v129, &v129);
            }
            ++v119;
          }
          while ( v3 != v119 );
        }
        sub_14083DB80(&v129, &v134);
        v122 = *a3;
        if ( &v129 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, a3);
          v123 = v129;
          a3[1] = v130;
          *a3 = v123;
          v122 = sub_14083D4F0() + 8;
          v130 = 0;
          v129 = v122;
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v122 + 16LL))(v122, &v129);
        sub_14083B0A0(&v134);
        if ( v51 != 0 )
          sub_1407E4890(qword_141ABD470, v51, v125 - v51);
        if ( v131 != 0 )
          sub_1407E4890(qword_141ABD470, v131, v133 - v131);
        goto LABEL_259;
      case 1096250222:
        v54 = (__int64 *)(a1 + 56);
        v55 = sub_14083D4F0();
        v135 = 0;
        if ( &v135 != v54 )
        {
          v56 = *v54;
          if ( *v54 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v56 - 4));
          v135 = v56;
        }
        v10 = v55 + 136;
        v134 = (__int64 *)v10;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v57 = v134;
          a3[1] = v135;
          *a3 = (__int64)v57;
          v10 = sub_14083D4F0() + 8;
          v135 = 0;
          v134 = (__int64 *)v10;
        }
        goto LABEL_221;
      case 1096250226:
        v46 = *(char *)(a1 + 132);
        v10 = sub_14083D4F0() + 40;
        LODWORD(v135) = v46;
        v134 = (__int64 *)v10;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v47 = v134;
          a3[1] = v135;
          *a3 = (__int64)v47;
          v10 = sub_14083D4F0() + 8;
          v135 = 0;
          v134 = (__int64 *)v10;
        }
        goto LABEL_221;
      case 1096250227:
        v44 = *(char *)(a1 + 135);
        v10 = sub_14083D4F0() + 40;
        LODWORD(v135) = v44;
        v134 = (__int64 *)v10;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v45 = v134;
          a3[1] = v135;
          *a3 = (__int64)v45;
          v10 = sub_14083D4F0() + 8;
          v135 = 0;
          v134 = (__int64 *)v10;
        }
        goto LABEL_221;
      default:
        if ( a2 != 1096250467 )
          goto LABEL_112;
        if ( dword_141B62F80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B62F80);
          if ( dword_141B62F80 == -1 )
          {
            sub_141336010(&qword_141B62F50);
            sub_141751048(sub_1413360A0);
            sub_141750EA0(&dword_141B62F80);
          }
        }
        LODWORD(v135) = *(_DWORD *)(a1 + 32);
        v38 = &qword_141B62F50;
        v134 = &qword_141B62F50;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v43 = v134;
          a3[1] = v135;
          *a3 = (__int64)v43;
          v38 = (__int64 *)(sub_14083D4F0() + 8);
          v135 = 0;
          v134 = v38;
        }
        break;
    }
LABEL_184:
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v38 + 16))(v38, &v134);
    goto LABEL_259;
  }
  if ( a2 > 1096251488 )
  {
    if ( a2 > 1635218019 )
    {
      switch ( a2 )
      {
        case 1684303986:
          LODWORD(v3) = 0;
          return (unsigned int)v3;
        case 1683177847:
          v83 = *(_BYTE *)(a1 + 134);
          v10 = sub_14083D4F0() + 24;
          LOBYTE(v135) = v83;
          v134 = (__int64 *)v10;
          if ( &v134 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v84 = v134;
            a3[1] = v135;
            *a3 = (__int64)v84;
            v10 = sub_14083D4F0() + 8;
            v135 = 0;
            v134 = (__int64 *)v10;
          }
          goto LABEL_221;
        case 1635218020:
          v3 = sub_14083D4F0() + 8;
          v132 = 0;
          v131 = v3;
          v16 = *(_DWORD *)(a1 + 8);
          v17 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 56LL))(a1);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)v3 + 24LL))(v3, &v131, &v135);
          v18 = v16 & v17;
          v19 = (v17 << 24) | v16 & 0x7FFFFF;
          v20 = v18 == -1;
          v21 = -8388609;
          if ( !v20 )
            v21 = v19;
          LODWORD(v134) = v21;
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v131 + 16LL))(v131, &v131);
          sub_140FEAD00(&v134, &v131);
          v22 = *a3;
          if ( &v131 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, a3);
            v23 = v131;
            a3[1] = v132;
            *a3 = v23;
            v22 = sub_14083D4F0() + 8;
            v132 = 0;
            v131 = v22;
          }
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v131);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v135 + 16LL))(v135, &v135);
          goto LABEL_259;
        default:
          break;
      }
      goto LABEL_112;
    }
    if ( a2 != 1096251489 )
    {
      if ( a2 == 1145392197 )
      {
        v36 = *(_BYTE *)(a1 + 129);
        v10 = sub_14083D4F0() + 24;
        LOBYTE(v135) = v36 == -1;
        v134 = (__int64 *)v10;
        if ( &v134 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v37 = v134;
          a3[1] = v135;
          *a3 = (__int64)v37;
          v10 = sub_14083D4F0() + 8;
          v135 = 0;
          v134 = (__int64 *)v10;
        }
        goto LABEL_221;
      }
      goto LABEL_112;
    }
    v26 = *(unsigned __int8 *)(a1 + 143);
    if ( (char)v26 <= 0 )
      goto LABEL_203;
LABEL_202:
    v96 = sub_14083D4F0();
    LODWORD(v135) = v26;
    v134 = (__int64 *)(v96 + 40);
    sub_14083DFA0(a3, &v134);
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v134 + 16))(v134, &v134);
    goto LABEL_259;
  }
  if ( a2 > 1096250981 )
  {
    if ( a2 != 1096250982 )
    {
      if ( a2 == 1096251240 )
      {
        v7 = *(unsigned __int8 *)(a1 + 145);
        if ( *(_BYTE *)(a1 + 145) != 0 )
          goto LABEL_9;
        goto LABEL_203;
      }
      if ( a2 == 1096251250 )
      {
        v7 = *(unsigned __int8 *)(a1 + 146);
        if ( *(_BYTE *)(a1 + 146) != 0 )
        {
LABEL_9:
          v8 = sub_14083D4F0();
          LODWORD(v135) = v7;
          v134 = (__int64 *)(v8 + 56);
          sub_14083DFA0(a3, &v134);
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v134 + 16))(v134, &v134);
LABEL_259:
          LOBYTE(v3) = 1;
          return (unsigned int)v3;
        }
LABEL_203:
        LOBYTE(v3) = 1;
        if ( a3 != &qword_141B5A4A0 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            a3);
        }
        return (unsigned int)v3;
      }
      goto LABEL_112;
    }
    v88 = *(char *)(a1 + 138);
    v10 = sub_14083D4F0() + 40;
    LODWORD(v135) = v88;
    v134 = (__int64 *)v10;
    if ( &v134 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v89 = v134;
      a3[1] = v135;
      *a3 = (__int64)v89;
      v10 = sub_14083D4F0() + 8;
      v135 = 0;
      v134 = (__int64 *)v10;
    }
LABEL_221:
    v3 = *(_QWORD *)v10;
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v10 + 16LL))(v10, &v134);
    goto LABEL_259;
  }
  if ( a2 == 1096250489 )
  {
    v94 = *(char *)(a1 + 129);
    v10 = sub_14083D4F0() + 40;
    LODWORD(v135) = v94;
    v134 = (__int64 *)v10;
    if ( &v134 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v95 = v134;
      a3[1] = v135;
      *a3 = (__int64)v95;
      v10 = sub_14083D4F0() + 8;
      v135 = 0;
      v134 = (__int64 *)v10;
    }
    goto LABEL_221;
  }
  if ( a2 == 1096250739 )
  {
    v34 = *(_BYTE *)(a1 + 141) & 1;
    v10 = sub_14083D4F0() + 24;
    LOBYTE(v135) = v34;
    v134 = (__int64 *)v10;
    if ( &v134 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v35 = v134;
      a3[1] = v135;
      *a3 = (__int64)v35;
      v10 = sub_14083D4F0() + 8;
      v135 = 0;
      v134 = (__int64 *)v10;
    }
    goto LABEL_221;
  }
LABEL_112:
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5ECC0 + 32LL))(qword_141B5ECC0) != 0 )
    return sub_140FE3F20(a1, (unsigned int)a2, a3);
  LOBYTE(v3) = 1;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64, _QWORD, __int64 *))(*(_QWORD *)qword_141B5ECC0 + 48LL))(
         qword_141B5ECC0,
         a1,
         (unsigned int)a2,
         a3) == 0 )
    return sub_140FE3F20(a1, (unsigned int)a2, a3);
  return (unsigned int)v3;
}
