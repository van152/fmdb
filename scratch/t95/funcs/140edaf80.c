char __fastcall sub_140EDAF80(_DWORD *a1, int a2, __int64 *a3)
{
  __int64 v6; // rcx
  __int64 v7; // r8
  __int64 *v8; // rcx
  __int64 v9; // rcx
  _OWORD *v10; // rdi
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rax
  __int64 v14; // rcx
  int v15; // xmm6_4
  __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 v18; // rcx
  __int64 v19; // rcx
  _OWORD *v20; // rdi
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // rcx
  __int64 v24; // rcx
  __int64 v25; // rax
  __int64 v26; // rcx
  _OWORD *v27; // rdi
  __int64 v28; // rax
  __int64 v29; // rcx
  __int64 v30; // rcx
  _OWORD *v31; // rdi
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rcx
  __int64 v35; // rcx
  __int64 v36; // rcx
  int v37; // esi
  int v38; // edi
  int v39; // eax
  int v40; // esi
  bool v41; // zf
  int v42; // eax
  __int64 v43; // rcx
  __int64 v44; // rax
  __int64 v45; // rcx
  _OWORD *v46; // rdi
  __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rcx
  __int64 v50; // rcx
  __int64 v51; // rcx
  __int64 v52; // rax
  __int64 v53; // rcx
  __int64 v54; // rax
  __int64 v55; // rcx
  __int64 v56; // rax
  __int64 v57; // rcx
  __int64 v58; // rax
  __int64 v59; // rax
  __int64 v60; // rcx
  __int64 v62; // rdi
  __int64 v63; // rcx
  __int64 v64; // rcx
  __int64 *v65; // rax
  __int64 v66; // rcx
  __int64 *v67; // rax
  __int64 v68; // r8
  __int64 v69; // rcx
  __int64 *v70; // rax
  __int64 v71; // rcx
  __int64 *v72; // rax
  __int64 v73; // rcx
  __int64 v74; // rax
  __int64 v75; // rsi
  __int64 v76; // rax
  __int64 v77; // rcx
  __int64 *v78; // rax
  __int64 v79; // rcx
  __int64 v80; // rbx
  __int64 v81; // rbx
  __int64 *v82; // rdx
  int v83; // eax
  int v84; // r8d
  __int64 *v85; // rdx
  int v86; // eax
  int v87; // r8d
  __int64 *v88; // rdx
  _QWORD *v89; // rax
  __int64 v90; // rax
  __int64 v91; // rax
  __int64 v92; // r12
  volatile signed __int32 *v93; // rcx
  __int64 v94; // rdi
  __int64 v95; // rcx
  __int64 v96; // rax
  __int64 v97; // rbx
  __int64 v98; // rax
  __int64 v99; // rcx
  char v100; // r14
  __int64 v101; // rsi
  __int64 v102; // rbx
  __int64 v103; // rax
  __int64 v104; // rax
  __int64 v105; // rcx
  _BYTE *v106; // rax
  _BYTE *v107; // r13
  __int64 v108; // rax
  __int64 v109; // rax
  __int64 v110; // rcx
  _BYTE *v111; // rax
  _BYTE *v112; // rbx
  __int64 v113; // rax
  __int64 v114; // rax
  __int64 v115; // rcx
  __int64 v116; // rcx
  __int64 v117; // rax
  char *v118; // rax
  __int64 v119; // rax
  __int64 v120; // rcx
  __int64 *v121; // rdx
  int v122; // eax
  __int64 v123; // r8
  __int64 *v124; // rdx
  int v125; // eax
  __int64 v126; // r8
  _QWORD v127[2]; // [rsp+28h] [rbp-58h] BYREF
  __int64 v128; // [rsp+38h] [rbp-48h]
  __int64 v129; // [rsp+40h] [rbp-40h] BYREF
  __int64 v130; // [rsp+48h] [rbp-38h] BYREF
  volatile signed __int32 *v131; // [rsp+58h] [rbp-28h]
  char v132; // [rsp+67h] [rbp-19h] BYREF
  __int64 v133; // [rsp+68h] [rbp-18h] BYREF
  __int64 v134; // [rsp+70h] [rbp-10h]
  __int128 v135; // [rsp+80h] [rbp+0h] BYREF
  __int64 v136; // [rsp+90h] [rbp+10h]
  __int64 v137; // [rsp+98h] [rbp+18h]

  v137 = -2;
  if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5ED80 + 32LL))(qword_141B5ED80) == 0
    && (*(unsigned __int8 (__fastcall **)(__int64, _DWORD *, _QWORD, __int64 *))(*(_QWORD *)qword_141B5ED80 + 48LL))(
         qword_141B5ED80,
         a1,
         (unsigned int)a2,
         a3) != 0 )
  {
    return 1;
  }
  if ( a2 <= 1131307372 )
  {
    if ( a2 > 1129604706 )
    {
      if ( a2 <= 1130591352 )
      {
        if ( a2 == 1129604707 )
        {
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
          DWORD2(v135) = a1[18];
          v8 = &qword_141B62F50;
          *(_QWORD *)&v135 = &qword_141B62F50;
          if ( &v135 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v36 = *((_QWORD *)&v135 + 1);
            *(_OWORD *)a3 = v135;
            v8 = (__int64 *)(sub_14083D4F0(v36) + 8);
            v135 = (unsigned __int64)v8;
          }
          goto LABEL_91;
        }
        if ( a2 == 1129608291 )
        {
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
          DWORD2(v135) = a1[20];
          v8 = &qword_141B62F50;
          *(_QWORD *)&v135 = &qword_141B62F50;
          if ( &v135 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v17 = *((_QWORD *)&v135 + 1);
            *(_OWORD *)a3 = v135;
            v8 = (__int64 *)(sub_14083D4F0(v17) + 8);
            v135 = (unsigned __int64)v8;
          }
          goto LABEL_91;
        }
        goto LABEL_63;
      }
      if ( a2 == 1130591353 )
      {
        v46 = a1 + 10;
        v47 = sub_14083D4F0(v6);
        *((_QWORD *)&v135 + 1) = 0;
        if ( (__int128 *)((char *)&v135 + 8) != v46 )
        {
          v48 = *(_QWORD *)v46;
          if ( *(_QWORD *)v46 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v48 - 4));
          *((_QWORD *)&v135 + 1) = v48;
        }
        v13 = v47 + 136;
        *(_QWORD *)&v135 = v13;
        if ( &v135 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v49 = *((_QWORD *)&v135 + 1);
          *(_OWORD *)a3 = v135;
          v13 = sub_14083D4F0(v49) + 8;
          v135 = (unsigned __int64)v13;
        }
      }
      else
      {
        if ( a2 != 1130783854 )
          goto LABEL_63;
        v20 = a1 + 12;
        v21 = sub_14083D4F0(v6);
        *((_QWORD *)&v135 + 1) = 0;
        if ( (__int128 *)((char *)&v135 + 8) != v20 )
        {
          v22 = *(_QWORD *)v20;
          if ( *(_QWORD *)v20 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v22 - 4));
          *((_QWORD *)&v135 + 1) = v22;
        }
        v13 = v21 + 136;
        *(_QWORD *)&v135 = v13;
        if ( &v135 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v23 = *((_QWORD *)&v135 + 1);
          *(_OWORD *)a3 = v135;
          v13 = sub_14083D4F0(v23) + 8;
          v135 = (unsigned __int64)v13;
        }
      }
    }
    else
    {
      if ( a2 > 1129473381 )
      {
        if ( a2 == 1129473382 )
        {
          v134 = 0;
          v133 = sub_14083D4F0(v6) + 8;
          v37 = a1[2];
          v38 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1);
          (*(void (__fastcall **)(__int64, __int64 *, char *))(*(_QWORD *)v133 + 24LL))(v133, &v133, (char *)&v135 + 8);
          v39 = v37 & v38;
          v40 = (v38 << 24) | v37 & 0x7FFFFF;
          v41 = v39 == -1;
          v42 = -8388609;
          if ( !v41 )
            v42 = v40;
          LODWORD(v135) = v42;
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
          sub_140FEAD00(&v135, &v133);
          v43 = *a3;
          if ( &v133 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v43 + 16LL))(v43, a3);
            v44 = v133;
            v45 = v134;
            a3[1] = v134;
            *a3 = v44;
            v43 = sub_14083D4F0(v45) + 8;
            v134 = 0;
            v133 = v43;
          }
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v43 + 16LL))(v43, &v133);
          (*(void (__fastcall **)(_QWORD, char *))(**((_QWORD **)&v135 + 1) + 16LL))(
            *((_QWORD *)&v135 + 1),
            (char *)&v135 + 8);
          return 1;
        }
        if ( a2 == 1129603683 )
        {
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
          DWORD2(v135) = a1[19];
          v8 = &qword_141B62F50;
          *(_QWORD *)&v135 = &qword_141B62F50;
          if ( &v135 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v19 = *((_QWORD *)&v135 + 1);
            *(_OWORD *)a3 = v135;
            v8 = (__int64 *)(sub_14083D4F0(v19) + 8);
            v135 = (unsigned __int64)v8;
          }
          goto LABEL_91;
        }
        goto LABEL_63;
      }
      if ( a2 == 1097032556 )
        goto LABEL_60;
      if ( a2 != 1127443566 )
        goto LABEL_63;
      v10 = a1 + 8;
      v11 = sub_14083D4F0(v6);
      *((_QWORD *)&v135 + 1) = 0;
      if ( (__int128 *)((char *)&v135 + 8) != v10 )
      {
        v12 = *(_QWORD *)v10;
        if ( *(_QWORD *)v10 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v12 - 4));
        *((_QWORD *)&v135 + 1) = v12;
      }
      v13 = v11 + 136;
      *(_QWORD *)&v135 = v13;
      if ( &v135 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v14 = *((_QWORD *)&v135 + 1);
        *(_OWORD *)a3 = v135;
        v13 = sub_14083D4F0(v14) + 8;
        v135 = (unsigned __int64)v13;
      }
    }
LABEL_103:
    (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v13 + 16LL))(v13, &v135);
    return 1;
  }
  if ( a2 <= 1684303985 )
  {
    if ( a2 > 1131636333 )
    {
      if ( a2 == 1131636334 )
      {
        v31 = a1 + 16;
        v32 = sub_14083D4F0(v6);
        *((_QWORD *)&v135 + 1) = 0;
        if ( (__int128 *)((char *)&v135 + 8) != v31 )
        {
          v33 = *(_QWORD *)v31;
          if ( *(_QWORD *)v31 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v33 - 4));
          *((_QWORD *)&v135 + 1) = v33;
        }
        v13 = v32 + 136;
        *(_QWORD *)&v135 = v13;
        if ( &v135 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v34 = *((_QWORD *)&v135 + 1);
          *(_OWORD *)a3 = v135;
          v13 = sub_14083D4F0(v34) + 8;
          v135 = (unsigned __int64)v13;
        }
      }
      else
      {
        if ( a2 != 1145392197 || a1[3] != 7 )
          goto LABEL_63;
        v13 = sub_14083D4F0(v6) + 24;
        BYTE8(v135) = 1;
        *(_QWORD *)&v135 = v13;
        if ( &v135 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v18 = *((_QWORD *)&v135 + 1);
          *(_OWORD *)a3 = v135;
          v13 = sub_14083D4F0(v18) + 8;
          v135 = (unsigned __int64)v13;
        }
      }
    }
    else if ( a2 == 1131307373 )
    {
      v27 = a1 + 6;
      v28 = sub_14083D4F0(v6);
      *((_QWORD *)&v135 + 1) = 0;
      if ( (__int128 *)((char *)&v135 + 8) != v27 )
      {
        v29 = *(_QWORD *)v27;
        if ( *(_QWORD *)v27 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v29 - 4));
        *((_QWORD *)&v135 + 1) = v29;
      }
      v13 = v28 + 136;
      *(_QWORD *)&v135 = v13;
      if ( &v135 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v30 = *((_QWORD *)&v135 + 1);
        *(_OWORD *)a3 = v135;
        v13 = sub_14083D4F0(v30) + 8;
        v135 = (unsigned __int64)v13;
      }
    }
    else
    {
      if ( a2 != 1131571059 )
        goto LABEL_63;
      v15 = a1[57];
      v13 = sub_14083D4F0(v6) + 104;
      DWORD2(v135) = v15;
      *(_QWORD *)&v135 = v13;
      if ( &v135 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v16 = *((_QWORD *)&v135 + 1);
        *(_OWORD *)a3 = v135;
        v13 = sub_14083D4F0(v16) + 8;
        v135 = (unsigned __int64)v13;
      }
    }
    goto LABEL_103;
  }
  if ( a2 <= 1884578667 )
  {
    if ( a2 == 1684303986 )
    {
      sub_1407C9510(&v135);
      LODWORD(v134) = 1131307373;
      v133 = sub_14083D4F0(v50) + 56;
      sub_14083B5F0(&v135, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
      v52 = sub_14083D4F0(v51);
      LODWORD(v134) = 1130783854;
      v133 = v52 + 56;
      sub_14083B5F0(&v135, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
      v54 = sub_14083D4F0(v53);
      LODWORD(v134) = 1129344880;
      v133 = v54 + 56;
      sub_14083B5F0(&v135, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
      v56 = sub_14083D4F0(v55);
      LODWORD(v134) = 1129210179;
      v133 = v56 + 56;
      sub_14083B5F0(&v135, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
      v58 = sub_14083D4F0(v57);
      LODWORD(v134) = 1129604419;
      v133 = v58 + 56;
      sub_14083B5F0(&v135, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
      sub_14083DB80(&v133, &v135);
      v24 = *a3;
      if ( &v133 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, a3);
        v59 = v133;
        v60 = v134;
        a3[1] = v134;
        *a3 = v59;
        v24 = sub_14083D4F0(v60) + 8;
        v134 = 0;
        v133 = v24;
      }
      goto LABEL_106;
    }
    if ( a2 != 1883333484 )
      goto LABEL_63;
LABEL_60:
    sub_1407C9510(&v135);
    sub_1407EB3A0(a1, &v133, 1952605036);
    sub_14083B5F0(&v135, &v133);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
    sub_1407EB3A0(a1, &v133, 1953784684);
    sub_14083B5F0(&v135, &v133);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
    sub_14083DB80(&v133, &v135);
    v24 = *a3;
    if ( &v133 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, a3);
      v25 = v133;
      v26 = v134;
      a3[1] = v134;
      *a3 = v25;
      v24 = sub_14083D4F0(v26) + 8;
      v134 = 0;
      v133 = v24;
    }
LABEL_106:
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v24 + 16LL))(v24, &v133);
    goto LABEL_107;
  }
  switch ( a2 )
  {
    case 1884578668:
      goto LABEL_60;
    case 1952605036:
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
      DWORD2(v135) = a1[19];
      v8 = &qword_141B62F50;
      *(_QWORD *)&v135 = &qword_141B62F50;
      if ( &v135 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v35 = *((_QWORD *)&v135 + 1);
        *(_OWORD *)a3 = v135;
        v8 = (__int64 *)(sub_14083D4F0(v35) + 8);
        v135 = (unsigned __int64)v8;
      }
      goto LABEL_91;
    case 1953784684:
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
      DWORD2(v135) = a1[18];
      v8 = &qword_141B62F50;
      *(_QWORD *)&v135 = &qword_141B62F50;
      if ( &v135 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v9 = *((_QWORD *)&v135 + 1);
        *(_OWORD *)a3 = v135;
        v8 = (__int64 *)(sub_14083D4F0(v9) + 8);
        v135 = (unsigned __int64)v8;
      }
LABEL_91:
      (*(void (__fastcall **)(__int64 *, __int128 *))(*v8 + 16))(v8, &v135);
      return 1;
    default:
      break;
  }
LABEL_63:
  if ( (_BYTE)word_141B60320 == 0 )
    return sub_140FE3F20(a1, a2, a3);
  if ( a2 <= 1130652779 )
  {
    if ( a2 > 1129344879 )
    {
      switch ( a2 )
      {
        case 1129344880:
          if ( qword_141ABD470 == 0 )
            qword_141ABD470 = sub_1407E4940();
          v135 = 0;
          v136 = 0;
          LOBYTE(v7) = 1;
          sub_140ED7A70(a1, &v135, v7);
          v62 = v135;
          v73 = *((_QWORD *)&v135 + 1) - v135;
          if ( *((_QWORD *)&v135 + 1) == (_QWORD)v135 )
          {
            v75 = 0;
          }
          else
          {
            v74 = 1;
            if ( (unsigned __int64)(v73 >> 3) >= 2 )
              v74 = v73 >> 3;
            if ( (unsigned __int64)v73 >= 0x10 )
            {
              v75 = 0;
              v73 = 0;
              do
              {
                v80 = *(_QWORD *)(v135 + 8 * v73);
                if ( v80 != 0 )
                  v75 += *(int *)(v80 + 452);
                v81 = *(_QWORD *)(v135 + 8 * v73 + 8);
                if ( v81 != 0 )
                  v75 += *(int *)(v81 + 452);
                v73 += 2;
              }
              while ( (v74 & 0xFFFFFFFFFFFFFFFEuLL) != v73 );
            }
            else
            {
              v75 = 0;
              v73 = 0;
            }
            if ( (v74 & 1) != 0 )
            {
              v76 = *(_QWORD *)(v135 + 8 * v73);
              if ( v76 != 0 )
                v75 += *(int *)(v76 + 452);
            }
          }
          v134 = v75;
          v133 = sub_14083D4F0(v73) + 88;
          sub_14083DFA0(a3, &v133);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
          break;
        case 1129604419:
          if ( qword_141ABD470 == 0 )
            qword_141ABD470 = sub_1407E4940();
          v135 = 0;
          v136 = 0;
          sub_140ED9260(a1, 0, &v135);
          v62 = v135;
          v134 = (__int64)(*((_QWORD *)&v135 + 1) - v135) >> 3;
          v133 = sub_14083D4F0(v79) + 88;
          sub_14083DFA0(a3, &v133);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
          break;
        case 1130587756:
          goto LABEL_129;
        default:
          return sub_140FE3F20(a1, a2, a3);
      }
      goto LABEL_163;
    }
    if ( a2 != 1129147497 )
    {
      if ( a2 == 1129148001 )
      {
        sub_1407C9510(&v135);
        v77 = qword_141B60C30;
        v78 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v77 != 1853189474 )
          {
            v77 += 16;
            if ( v77 == qword_141B60C38 )
              goto LABEL_238;
          }
          if ( v77 == qword_141B60C38 )
            v78 = nullptr;
          else
            v78 = *(__int64 **)(v77 + 8);
        }
LABEL_238:
        v121 = &qword_141B5A4A0;
        if ( v78 != nullptr )
          v121 = v78;
        v122 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v121 + 64LL))(*v121);
        v123 = 8;
        if ( v122 > 0 )
          v123 = (unsigned int)v122;
        sub_140ED8FD0(&v135, a1, v123);
        sub_14083DB80(&v133, &v135);
        sub_14083DFA0(a3, &v133);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
        goto LABEL_107;
      }
      if ( a2 != 1129210179 )
        return sub_140FE3F20(a1, a2, a3);
      if ( qword_141ABD470 == 0 )
        qword_141ABD470 = sub_1407E4940();
      v135 = 0;
      v136 = 0;
      sub_140ED7A70(a1, &v135, 0);
      v62 = v135;
      v134 = (__int64)(*((_QWORD *)&v135 + 1) - v135) >> 3;
      v133 = sub_14083D4F0(v63) + 88;
      sub_14083DFA0(a3, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
LABEL_163:
      if ( v62 != 0 )
        sub_1407E4890(qword_141ABD470, v62, v136 - v62);
      return 1;
    }
    v71 = qword_141B60C30;
    v72 = nullptr;
    if ( qword_141B60C30 != qword_141B60C38 )
    {
      while ( *(_DWORD *)v71 != 1718185076 )
      {
        v71 += 16;
        if ( v71 == qword_141B60C38 )
          goto LABEL_194;
      }
      if ( v71 == qword_141B60C38 )
        v72 = nullptr;
      else
        v72 = *(__int64 **)(v71 + 8);
    }
LABEL_194:
    v88 = &qword_141B5A4A0;
    if ( v72 != nullptr )
      v88 = v72;
    v89 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v88 + 176LL))(*v88, v88, 0);
    v135 = 0;
    v136 = 0;
    sub_1408367A0(&v135, (__int64)(v89[1] - *v89) >> 4, v89, v89 + 1);
    v90 = sub_1407E90B0(&v135, 0);
    v91 = sub_141758910(v90, 0, &unk_141A7E140, &unk_141A7FB50, 0);
    if ( v91 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v91 + 16));
    v131 = (volatile signed __int32 *)v91;
    sub_1407C9510(&v133);
    v92 = qword_141B5FEC0;
    v128 = qword_141B5FEC8;
    if ( qword_141B5FEC0 == qword_141B5FEC8 )
    {
LABEL_199:
      sub_14083DB80(&v129, &v133);
      sub_14083DFA0(a3, &v129);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v129 + 16LL))(v129, &v129);
      sub_14083B0A0(&v133);
      v93 = v131;
      if ( v131 != nullptr && _InterlockedDecrement(v131 + 4) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v93)(v93, 1);
      sub_140833970(&v135);
      return 1;
    }
    while ( 1 )
    {
      v94 = *(_QWORD *)v92;
      v95 = *(_QWORD *)v92 + *(int *)(*(_QWORD *)(*(_QWORD *)v92 + 8LL) + 4LL) + 8LL;
      v96 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v95 + 1752LL))(v95);
      if ( v96 == 0 || *(_BYTE *)(v96 + 1067) != 0 )
      {
        v97 = *(int *)(*(_QWORD *)(v94 + 8) + 8LL);
        v98 = *(_QWORD *)(v97 + v94 + 176);
        if ( v98 != 0 && (v99 = *(_QWORD *)(v98 + 16)) != 0 )
          v100 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v99 + 80LL))(v99);
        else
          v100 = 0;
        v101 = v97 + v94 + 8;
        v102 = v97 + v94 + 344;
        v103 = *(int *)(*(_QWORD *)(v102 - 328) + 4LL);
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)(v102 + v103 - 328) + 1296LL))(v103 + v101 + 8) != 0 )
        {
          v104 = *(int *)(*(_QWORD *)(v102 - 328) + 4LL);
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v102 + v104 - 328) + 640LL))(v104 + v101 + 8);
        }
        v105 = v94 + *(int *)(*(_QWORD *)(v94 + 8) + 4LL) + 8;
        v106 = (_BYTE *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v105 + 1032LL))(v105);
        if ( v106 != nullptr )
        {
          v107 = v106;
          if ( (v106[28] & 0xFE) == 0x10 )
            goto LABEL_220;
          if ( ((*(__int64 (__fastcall **)(_BYTE *))(*(_QWORD *)v106 + 104LL))(v106) & 0xFE) == 0x10 )
          {
            (*(void (__fastcall **)(_BYTE *))(*(_QWORD *)v107 + 88LL))(v107);
LABEL_220:
            v110 = v94 + *(int *)(*(_QWORD *)(v94 + 8) + 4LL) + 8;
            v111 = (_BYTE *)(*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v110 + 1032LL))(v110);
            if ( v111 == nullptr
              || (v112 = v111, v111[28] <= 1u)
              && (*(unsigned __int8 (__fastcall **)(_BYTE *))(*(_QWORD *)v111 + 104LL))(v111) < 2u
              || (v113 = *((_QWORD *)v112 + 2)) == 0
              || *(_BYTE *)(v113 + 47) != 0
              || *(_QWORD *)(v113 + 48) == 0
              || (unsigned __int8)sub_141097F40(v94 + *(int *)(*(_QWORD *)(v94 + 8) + 4LL) + 8, 0) != 0 )
            {
              v114 = *(_QWORD *)(v94 + 8);
              v115 = *(_QWORD *)(*(int *)(v114 + 8) + v94 + 176);
              if ( v115 == 0
                || (v116 = *(_QWORD *)(v115 + 16)) == 0
                || (v100 & 0xFE) != 0x10
                || *(_QWORD *)(v116 + 16) == 0
                || (unsigned __int8)sub_141088250(*(int *)(v114 + 4) + v94 + 8, 0) != 0
                || *(_BYTE *)(*(_QWORD *)(*(_QWORD *)(*(_QWORD *)((v117 = *(int *)(*(_QWORD *)(v94 + 8) + 8LL))
                                                                + v94
                                                                + 176)
                                                    + 16LL)
                                        + 16LL)
                            + 40LL) == 0
                || (v118 = *(char **)(v94 + v117 + 224)) == nullptr
                || *v118 >= 20 )
              {
                v132 = 0;
                v127[0] = 0x14175EE20LL;
                v119 = *(int *)(*(_QWORD *)(v94 + 8) + 4LL) + v94 + 8;
                v129 = 0x14187E8C8LL;
                v130 = v119;
                if ( (*(unsigned __int8 (__fastcall **)(volatile signed __int32 *, __int64 *, _QWORD *, char *))(*(_QWORD *)v131 + 56LL))(
                       v131,
                       &v129,
                       v127,
                       &v132) != 0 )
                {
                  v120 = v94 + *(int *)(*(_QWORD *)(v94 + 8) + 4LL) + 8;
                  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v120 + 144LL))(v120, &v129);
                  sub_140FEAD00(&v129, v127);
                  sub_14083B5F0(&v133, v127);
                  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v127[0] + 16LL))(v127[0], v127);
                  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v130 + 16LL))(v130, &v130);
                }
              }
            }
            goto LABEL_203;
          }
        }
        if ( (v100 & 0xFE) == 0x10 )
        {
          v108 = *(_QWORD *)(*(int *)(*(_QWORD *)(v94 + 8) + 8LL) + v94 + 176);
          if ( v108 != 0 )
          {
            v109 = *(_QWORD *)(v108 + 16);
            if ( v109 != 0 && *(_QWORD *)(v109 + 16) != 0 )
              goto LABEL_220;
          }
        }
      }
LABEL_203:
      v92 += 8;
      if ( v92 == v128 )
        goto LABEL_199;
    }
  }
  if ( a2 <= 1131245644 )
  {
    switch ( a2 )
    {
      case 1130652780:
        sub_1407C9510(&v135);
        LOBYTE(v68) = 1;
        sub_140EDA760(a1, &v135, v68);
        sub_14083DB80(&v133, &v135);
        sub_14083DFA0(a3, &v133);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
        goto LABEL_107;
      case 1130917965:
        sub_1407C9510(&v135);
        v69 = qword_141B60C30;
        v70 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v69 != 1853189474 )
          {
            v69 += 16;
            if ( v69 == qword_141B60C38 )
              goto LABEL_188;
          }
          if ( v69 == qword_141B60C38 )
            v70 = nullptr;
          else
            v70 = *(__int64 **)(v69 + 8);
        }
LABEL_188:
        v85 = &qword_141B5A4A0;
        if ( v70 != nullptr )
          v85 = v70;
        v86 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v85 + 64LL))(*v85);
        v87 = 6;
        if ( v86 > 0 )
          v87 = v86;
        sub_140ED9C80((_DWORD)a1, 0, v87, (unsigned int)&v135, 23);
        sub_14083DB80(&v133, &v135);
        sub_14083DFA0(a3, &v133);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
        goto LABEL_107;
      case 1131242317:
        sub_1407C9510(&v135);
        v64 = qword_141B60C30;
        v65 = nullptr;
        if ( qword_141B60C30 != qword_141B60C38 )
        {
          while ( *(_DWORD *)v64 != 1853189474 )
          {
            v64 += 16;
            if ( v64 == qword_141B60C38 )
              goto LABEL_244;
          }
          if ( v64 == qword_141B60C38 )
            v65 = nullptr;
          else
            v65 = *(__int64 **)(v64 + 8);
        }
LABEL_244:
        v124 = &qword_141B5A4A0;
        if ( v65 != nullptr )
          v124 = v65;
        v125 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v124 + 64LL))(*v124);
        v126 = 6;
        if ( v125 > 0 )
          v126 = (unsigned int)v125;
        sub_140ED94D0(a1, 0, v126, &v135);
        sub_14083DB80(&v133, &v135);
        sub_14083DFA0(a3, &v133);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
        goto LABEL_107;
      default:
        break;
    }
  }
  else
  {
    if ( a2 <= 1131373419 )
    {
      if ( a2 != 1131245645 )
      {
        if ( a2 != 1131373414 )
          return sub_140FE3F20(a1, a2, a3);
LABEL_129:
        sub_140EDAE60(a1, (unsigned int)a2, a3);
        return 1;
      }
      sub_1407C9510(&v135);
      v66 = qword_141B60C30;
      v67 = nullptr;
      if ( qword_141B60C30 != qword_141B60C38 )
      {
        while ( *(_DWORD *)v66 != 1853189474 )
        {
          v66 += 16;
          if ( v66 == qword_141B60C38 )
            goto LABEL_182;
        }
        if ( v66 == qword_141B60C38 )
          v67 = nullptr;
        else
          v67 = *(__int64 **)(v66 + 8);
      }
LABEL_182:
      v82 = &qword_141B5A4A0;
      if ( v67 != nullptr )
        v82 = v67;
      v83 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v82 + 64LL))(*v82);
      v84 = 6;
      if ( v83 > 0 )
        v84 = v83;
      sub_140ED9C80((_DWORD)a1, 0, v84, (unsigned int)&v135, 255);
      sub_14083DB80(&v133, &v135);
      sub_14083DFA0(a3, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
LABEL_107:
      sub_14083B0A0(&v135);
      return 1;
    }
    if ( a2 == 1131373420 )
    {
      sub_1407C9510(&v135);
      sub_140EDA760(a1, &v135, 0);
      sub_14083DB80(&v133, &v135);
      sub_14083DFA0(a3, &v133);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v133 + 16LL))(v133, &v133);
      goto LABEL_107;
    }
    if ( a2 == 1131443302 )
      goto LABEL_129;
  }
  return sub_140FE3F20(a1, a2, a3);
}
