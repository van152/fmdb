__int64 __fastcall sub_140FE3F20(_DWORD *a1, int a2, __int64 *a3)
{
  __int64 v3; // r14
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rax
  volatile signed __int32 *v11; // r13
  char *v12; // r14
  __int64 v13; // rdi
  unsigned __int64 v14; // rcx
  __int64 v15; // r8
  __int64 v16; // rcx
  char *v17; // rbx
  bool v18; // al
  __int64 v19; // rcx
  __int64 v20; // rax
  volatile signed __int32 *v21; // rcx
  __int64 v22; // rdx
  volatile signed __int32 *v23; // rcx
  volatile signed __int32 *v24; // rcx
  void (__fastcall **v25)(volatile signed __int32 *, __int64); // rax
  int v26; // esi
  __int64 v27; // rax
  __int64 v28; // rax
  volatile signed __int32 *v29; // rax
  char *v30; // rcx
  __int64 v31; // r8
  int v32; // esi
  __int64 v33; // rcx
  __int64 v34; // rax
  __int64 v35; // r8
  int v36; // esi
  volatile signed __int32 *v37; // rax
  char *v38; // rcx
  int v39; // esi
  volatile signed __int32 *v40; // rax
  char *v41; // rcx
  __int64 v42; // rcx
  volatile signed __int32 *v43; // rax
  volatile signed __int32 *v44; // rcx
  __int64 v45; // r8
  volatile signed __int32 *v46; // rcx
  __int64 *v47; // rax
  __int64 v48; // rax
  char v49; // bl
  __int64 v50; // rcx
  __int64 v51; // rax
  __int64 v52; // rax
  int v53; // eax
  __int64 v54; // rdx
  volatile signed __int32 *v55; // rcx
  volatile signed __int32 *v56; // rax
  unsigned __int64 v57; // rbx
  __int64 *v58; // rsi
  __int64 *v59; // rdi
  __int64 v60; // rax
  __int64 v61; // rcx
  __int64 *v62; // rdx
  __int64 v63; // rcx
  __int64 v64; // rdx
  __int64 *v65; // rax
  volatile signed __int32 *v66; // r13
  __int64 v67; // rcx
  __int64 v68; // rcx
  __int64 v69; // rax
  volatile signed __int32 *v70; // rcx
  __int64 v71; // rdx
  volatile signed __int32 *v72; // rcx
  __int64 v73; // rcx
  __int64 v74; // rcx
  __int64 v75; // rcx
  __int64 v76; // rdx
  __int64 v77; // rax
  volatile signed __int32 *v78; // rcx
  __int64 v79; // rdx
  volatile signed __int32 *v80; // rcx
  __int64 v81; // rax
  char *v82; // rcx
  __int64 v83; // rcx
  __int64 *v84; // r8
  __int64 v85; // rdx
  __int64 v86; // rcx
  __int64 v87; // rdx
  int v88; // esi
  __int64 v89; // rcx
  __int64 v90; // rax
  __int64 v91; // rax
  char v92; // bl
  __int64 v93; // rcx
  __int64 v94; // rax
  __int64 v95; // rax
  __int64 v96; // rax
  __int64 v97; // rsi
  __int64 v98; // rax
  __int64 v99; // rax
  int v100; // esi
  __int64 v101; // rcx
  __int64 v102; // rax
  __int64 v103; // rax
  __int64 v104; // rax
  __int64 v105; // r13
  __int64 v106; // rsi
  __int64 v107; // rdi
  unsigned __int64 v108; // rbx
  __int64 v109; // rcx
  __int64 v110; // rdi
  __int64 i; // rsi
  int v112; // r12d
  __int64 v113; // rax
  __int64 v114; // rax
  __int64 v115; // rax
  int v116; // [rsp+20h] [rbp-60h]
  __int64 v117; // [rsp+30h] [rbp-50h] BYREF
  __int64 v118; // [rsp+38h] [rbp-48h] BYREF
  __int64 v119; // [rsp+40h] [rbp-40h] BYREF
  volatile signed __int32 *v120; // [rsp+48h] [rbp-38h] BYREF
  __int64 v121; // [rsp+50h] [rbp-30h]
  _QWORD v122[2]; // [rsp+58h] [rbp-28h] BYREF
  volatile signed __int32 *v123; // [rsp+68h] [rbp-18h] BYREF
  volatile signed __int32 *v124; // [rsp+70h] [rbp-10h]
  volatile signed __int32 *v125; // [rsp+80h] [rbp+0h] BYREF
  char *v126; // [rsp+88h] [rbp+8h] BYREF
  __int64 v127; // [rsp+90h] [rbp+10h]
  __int64 v128; // [rsp+A0h] [rbp+20h]

  v128 = -2;
  v7 = qword_141B60C58;
  v8 = qword_141B60C50;
  if ( qword_141B60C50 != qword_141B60C58 )
  {
    while ( *(_DWORD *)v8 != a2 )
    {
      v8 += 16;
      if ( v8 == qword_141B60C58 )
        goto LABEL_4;
    }
    if ( v8 != qword_141B60C58 && *(_QWORD *)(v8 + 8) != 0 )
    {
      sub_1407C9510(&v125);
      v11 = v125;
      if ( (unsigned __int64)(v127 - (_QWORD)v125) <= 0xFF )
      {
        v12 = v126;
        v13 = sub_1407E4490(qword_141ABD470, 256);
        sub_141758A00(v13, v125, v126 - (char *)v125);
        if ( v125 != nullptr )
        {
          v14 = v127 - (_QWORD)v125;
          if ( v127 - (_QWORD)v125 == -1 )
            v14 = *(unsigned int *)((char *)v125 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v15 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v15) >> 3 > v14)
            && (v16 = *(_QWORD *)(v15 + 8 * v14)) != 0 )
          {
            v17 = (char *)v125 - *(unsigned int *)(v16 + 120);
            v121 = v16;
            MEMORY[0x1419475D8](v16 + 32, v17);
            v18 = *(_BYTE *)(v121 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v121 + 64)) != 0;
            if ( !v18 && *(_BYTE *)(v121 + 97) != 0 )
              sub_1412D33C0(v121);
          }
          else
          {
            MEMORY[0x141948990]((char *)v125 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v125 = (volatile signed __int32 *)v13;
        v3 = v13 + v12 - (char *)v11;
        v126 = (char *)v3;
        v127 = v13 + 256;
      }
      do
      {
        LOBYTE(v116) = 0;
        (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **, _QWORD, __int64 *, int))(*(_QWORD *)a1 + 232LL))(
          a1,
          &v125,
          (unsigned int)a2,
          &qword_141B60C30,
          v116);
        a1 = (_DWORD *)(*(__int64 (__fastcall **)(_DWORD *, _QWORD))(*(_QWORD *)a1 + 80LL))(a1, (unsigned int)a2);
      }
      while ( a1 != nullptr );
      sub_14083DB80(&v123, &v125);
      v42 = *a3;
      if ( &v123 != (volatile signed __int32 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v42 + 16LL))(v42, a3);
        v43 = v123;
        v44 = v124;
        a3[1] = (__int64)v124;
        *a3 = (__int64)v43;
        v42 = sub_14083D4F0(v44) + 8;
        v124 = nullptr;
        v123 = (volatile signed __int32 *)v42;
      }
      (*(void (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v42 + 16LL))(v42, &v123);
      sub_14083B0A0(&v125);
      LOBYTE(v3) = 1;
      return (unsigned int)v3;
    }
  }
LABEL_4:
  LOBYTE(v3) = 1;
  if ( a2 <= 1768124269 )
  {
    if ( a2 <= 1682002038 )
    {
      if ( a2 > 1313096769 )
      {
        if ( a2 <= 1634751058 )
        {
          if ( a2 != 1313096770 )
          {
            if ( a2 != 1634751056 )
              goto LABEL_142;
            goto LABEL_90;
          }
          v49 = sub_1407EB4D0(a1, 1145392197) ^ 1;
          v51 = sub_14083D4F0(v50);
          LOBYTE(v126) = v49;
          v125 = (volatile signed __int32 *)(v51 + 24);
          sub_14083DFA0(a3, &v125);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
            v125,
            &v125);
          return (unsigned int)v3;
        }
        if ( a2 == 1634751059 )
          goto LABEL_99;
        if ( a2 == 1667787116 )
        {
          sub_1407C9510(&v125);
          (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 256LL))(a1, &v125);
          sub_14083DB80(&v123, &v125);
          sub_14083DFA0(a3, &v123);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
            v123,
            &v123);
LABEL_218:
          sub_14083B0A0(&v125);
          return (unsigned int)v3;
        }
        goto LABEL_142;
      }
      if ( a2 > 1148546664 )
      {
        if ( a2 == 1148546665 )
        {
          v123 = nullptr;
          if ( (*(unsigned __int8 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 248LL))(a1) != 0 )
          {
            sub_140809670(&v123, &qword_141B60BE8);
            v53 = a1[4];
            if ( v53 == 0 )
              v53 = a1[3];
            LODWORD(v122[0]) = v53;
            sub_1408085A0(&v125, v122);
            sub_140809670(&v123, &v125);
            v55 = v125;
            if ( v125 != nullptr && _InterlockedDecrement(v125 - 1) == 0 )
              sub_1412EC9A0(v55 - 1, v54);
          }
          else
          {
            LODWORD(v122[0]) = a1[3];
            sub_1408085A0(&v125, v122);
            if ( v125 != nullptr )
              v123 = v125;
          }
          v77 = sub_14083D4F0(v55);
          v126 = nullptr;
          v78 = v123;
          if ( v123 != nullptr )
            _InterlockedIncrement(v123 - 1);
          v126 = (char *)v78;
          v125 = (volatile signed __int32 *)(v77 + 136);
          sub_14083DFA0(a3, &v125);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
            v125,
            &v125);
          v80 = v123;
          if ( v123 != nullptr && _InterlockedDecrement(v123 - 1) == 0 )
            sub_1412EC9A0(v80 - 1, v79);
          return (unsigned int)v3;
        }
        if ( a2 != 1230197840 )
          goto LABEL_142;
      }
      else
      {
        if ( a2 == 1113670480 )
        {
          v48 = sub_14083D4F0(qword_141B60C58);
          LOBYTE(v126) = 1;
          v125 = (volatile signed __int32 *)(v48 + 24);
          sub_14083DFA0(a3, &v125);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
            v125,
            &v125);
          return (unsigned int)v3;
        }
        if ( a2 != 1145392197 )
          goto LABEL_142;
      }
      v28 = sub_14083D4F0(qword_141B60C58) + 24;
      LOBYTE(v126) = 0;
      v125 = (volatile signed __int32 *)v28;
      if ( &v125 != (volatile signed __int32 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v29 = v125;
        v30 = v126;
        a3[1] = (__int64)v126;
        *a3 = (__int64)v29;
        v28 = sub_14083D4F0(v30) + 8;
        v126 = nullptr;
        v125 = (volatile signed __int32 *)v28;
      }
LABEL_110:
      (*(void (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v28 + 16LL))(v28, &v125);
      return (unsigned int)v3;
    }
    if ( a2 > 1685417576 )
    {
      if ( a2 > 1752191567 )
      {
        if ( a2 != 1752191568 )
        {
          if ( a2 != 1752191571 )
            goto LABEL_142;
          goto LABEL_99;
        }
LABEL_90:
        sub_1407C9510(&v125);
        if ( a2 <= 1768968783 )
        {
          if ( a2 > 1752191567 )
            v31 = 1802073137;
          else
            v31 = 1802073138;
        }
        else if ( a2 <= 1819300431 )
        {
          v31 = 1768124016;
        }
        else
        {
          v31 = 1819240303;
          if ( a2 != 1819300432 )
            v31 = 1802073139;
        }
        (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **, __int64, __int64 *, _BYTE))(*(_QWORD *)a1 + 232LL))(
          a1,
          &v125,
          v31,
          &qword_141B5A458,
          0);
        sub_1407C9510(&v123);
        if ( (unsigned __int8)sub_140FE5B80(&v123, &v125, v45, 0) != 0 )
        {
          v46 = v123;
          v47 = nullptr;
          if ( v123 != v124 )
          {
            while ( *v46 != 1885434984 )
            {
              v46 += 4;
              if ( v46 == v124 )
                goto LABEL_206;
            }
            if ( v46 == v124 )
              v47 = nullptr;
            else
              v47 = *((__int64 **)v46 + 1);
          }
LABEL_206:
          v84 = &qword_141B5A4A0;
          if ( v47 != nullptr )
            v84 = v47;
          (*(void (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)*v84 + 128LL))(*v84, v122);
          if ( (unsigned int)sub_14080AB90((unsigned int)v122, 1100189384, -1, 0, 0) == -1 )
          {
            v88 = sub_14080AB90((unsigned int)v122, 1100190006, -1, 0, 0);
            v89 = v122[0];
            if ( v122[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122[0] - 4LL)) == 0 )
              sub_1412EC9A0(v89 - 4, v87);
            if ( v88 == -1 )
            {
              sub_14083DDA0(v122, &v123);
              sub_14083DFA0(a3, v122);
              (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v122[0] + 16LL))(v122[0], v122);
            }
          }
          else
          {
            v86 = v122[0];
            if ( v122[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122[0] - 4LL)) == 0 )
              sub_1412EC9A0(v86 - 4, v85);
          }
        }
        sub_140833970(&v123);
        goto LABEL_218;
      }
      if ( a2 != 1685417577 )
      {
        if ( a2 != 1751737714 )
          goto LABEL_142;
        sub_140FE5FF0(a1, a3);
        return (unsigned int)v3;
      }
      goto LABEL_105;
    }
    if ( a2 <= 1685218661 )
    {
      if ( a2 == 1682002039 )
      {
        if ( (*(unsigned int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1) == 9 )
          sub_14103FBF0(*((_QWORD *)a1 + 46), &v125);
        else
          (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 200LL))(a1, &v125);
        v66 = v125;
        sub_14081AF20((_DWORD)v125, (unsigned int)v122, (unsigned int)&qword_141B59EE0, 0, 0, 0);
        if ( (unsigned __int8)sub_1407EB4D0(a1, 1683177847) != 0 )
        {
          sub_140823B40(qword_141ABD468, &v125, 595257);
          sub_14081ED40(&v125, &v118, 0);
          sub_1408094C0(v122, &v119, 0x14193EA6DLL);
          sub_140809550(&v119, &v117, &v118);
          sub_1408094C0(&v117, &v120, 0x14193EA3CLL);
          v69 = sub_14083D4F0(v68);
          v124 = nullptr;
          v70 = v120;
          if ( v120 != nullptr )
            _InterlockedIncrement(v120 - 1);
          v124 = v70;
          v123 = (volatile signed __int32 *)(v69 + 136);
          sub_14083DFA0(a3, &v123);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
            v123,
            &v123);
          v72 = v120;
          if ( v120 != nullptr && _InterlockedDecrement(v120 - 1) == 0 )
            sub_1412EC9A0(v72 - 1, v71);
          v73 = v117;
          if ( v117 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v117 - 4)) == 0 )
            sub_1412EC9A0(v73 - 4, v71);
          v74 = v119;
          if ( v119 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v119 - 4)) == 0 )
            sub_1412EC9A0(v74 - 4, v71);
          v75 = v118;
          if ( v118 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v118 - 4)) == 0 )
            sub_1412EC9A0(v75 - 4, v71);
          sub_14081D040(&v125);
        }
        else
        {
          v81 = sub_14083D4F0(v67);
          v126 = nullptr;
          v82 = (char *)v122[0];
          if ( v122[0] != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v122[0] - 4LL));
          v126 = v82;
          v125 = (volatile signed __int32 *)(v81 + 136);
          sub_14083DFA0(a3, &v125);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
            v125,
            &v125);
        }
        v83 = v122[0];
        if ( v122[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122[0] - 4LL)) == 0 )
          sub_1412EC9A0(v83 - 4, v76);
        if ( _InterlockedDecrement(v66 + 2) != 0 )
          return (unsigned int)v3;
        v25 = *(void (__fastcall ***)(volatile signed __int32 *, __int64))v66;
        v24 = v66;
      }
      else
      {
        if ( a2 != 1684172397 )
          goto LABEL_142;
        (*(void (__fastcall **)(_DWORD *, _QWORD *))(*(_QWORD *)a1 + 200LL))(a1, v122);
        sub_14081AF20(v122[0], (unsigned int)&v123, (unsigned int)&qword_141B59EE0, 0, 0, 0);
        v20 = sub_14083D4F0(v19);
        v126 = nullptr;
        v21 = v123;
        if ( v123 != nullptr )
          _InterlockedIncrement(v123 - 1);
        v126 = (char *)v21;
        v125 = (volatile signed __int32 *)(v20 + 136);
        sub_14083DFA0(a3, &v125);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
          v125,
          &v125);
        v23 = v123;
        if ( v123 != nullptr && _InterlockedDecrement(v123 - 1) == 0 )
          sub_1412EC9A0(v23 - 1, v22);
        v24 = (volatile signed __int32 *)v122[0];
        if ( v122[0] == 0 || _InterlockedDecrement((volatile signed __int32 *)(v122[0] + 8LL)) != 0 )
          return (unsigned int)v3;
        v25 = *(void (__fastcall ***)(volatile signed __int32 *, __int64))v24;
      }
      (*v25)(v24, 1);
      return (unsigned int)v3;
    }
    if ( a2 == 1685218662 )
    {
      (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 144LL))(a1, &v125);
      sub_140FEAD00(&v125, &v123);
      sub_14083DFA0(a3, &v123);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
        v123,
        &v123);
      (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v126 + 16LL))(v126, &v126);
      return (unsigned int)v3;
    }
    if ( a2 != 1685284961 )
      goto LABEL_142;
LABEL_108:
    v39 = a1[2];
    v28 = sub_14083D4F0(qword_141B60C58) + 40;
    LODWORD(v126) = v39;
    v125 = (volatile signed __int32 *)v28;
    if ( &v125 != (volatile signed __int32 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v40 = v125;
      v41 = v126;
      a3[1] = (__int64)v126;
      *a3 = (__int64)v40;
      v28 = sub_14083D4F0(v41) + 8;
      v126 = nullptr;
      v125 = (volatile signed __int32 *)v28;
    }
    goto LABEL_110;
  }
  if ( a2 <= 1886548066 )
  {
    if ( a2 > 1768968786 )
    {
      if ( a2 <= 1819300434 )
      {
        if ( a2 == 1768968787 )
          goto LABEL_99;
        if ( a2 != 1819300432 )
          goto LABEL_142;
        goto LABEL_90;
      }
      if ( a2 == 1819300435 )
        goto LABEL_99;
      if ( a2 != 1868723300 )
        goto LABEL_142;
      v32 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1);
      v34 = sub_14083D4F0(v33);
      LODWORD(v126) = v32;
      v125 = (volatile signed __int32 *)(v34 + 40);
      sub_14083DFA0(a3, &v125);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
        v125,
        &v125);
      return (unsigned int)v3;
    }
    if ( a2 <= 1768842359 )
    {
      if ( a2 == 1768124270 )
        return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)a1 + 16LL))(a1, 1936552035, a3);
      if ( a2 != 1768169504 )
        goto LABEL_142;
LABEL_105:
      v36 = a1[3];
      v28 = sub_14083D4F0(qword_141B60C58) + 40;
      LODWORD(v126) = v36;
      v125 = (volatile signed __int32 *)v28;
      if ( &v125 != (volatile signed __int32 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v37 = v125;
        v38 = v126;
        a3[1] = (__int64)v126;
        *a3 = (__int64)v37;
        v28 = sub_14083D4F0(v38) + 8;
        v126 = nullptr;
        v125 = (volatile signed __int32 *)v28;
      }
      goto LABEL_110;
    }
    if ( a2 != 1768842360 )
    {
      if ( a2 != 1768968784 )
        goto LABEL_142;
      goto LABEL_90;
    }
    goto LABEL_108;
  }
  if ( a2 > 1952605035 )
  {
    if ( a2 > 1953518159 )
    {
      if ( a2 != 1953518160 )
      {
        if ( a2 != 1953518163 )
        {
          if ( a2 == 1953784684 )
          {
            v9 = (*(__int64 (__fastcall **)(_DWORD *, __int64))(*(_QWORD *)a1 + 80LL))(a1, 1953784684);
            if ( v9 == 0
              || (*(unsigned __int8 (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)v9 + 16LL))(
                   v9,
                   1953784684,
                   a3) == 0 )
            {
              return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)a1 + 16LL))(
                       a1,
                       1717792620,
                       a3);
            }
            return (unsigned int)v3;
          }
          goto LABEL_142;
        }
LABEL_99:
        sub_1407C9510(&v125);
        if ( a2 <= 1768968786 )
        {
          if ( a2 > 1752191570 )
            v35 = 1802073137;
          else
            v35 = 1802073138;
        }
        else
        {
          v35 = 1819240303;
          if ( a2 <= 1819300434 )
          {
            v35 = 1768124016;
          }
          else if ( a2 != 1819300435 )
          {
            v35 = 1802073139;
          }
        }
        (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **, __int64, __int64 *, _BYTE))(*(_QWORD *)a1 + 232LL))(
          a1,
          &v125,
          v35,
          &qword_141B5A458,
          0);
        v56 = v125;
        if ( v126 != (char *)v125 )
        {
          v57 = 0;
          v58 = &qword_141B5A4A0;
          while ( 1 )
          {
            v59 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD, _QWORD))(***(_QWORD ***)&v56[2 * v57] + 176LL))(
                               **(_QWORD **)&v56[2 * v57],
                               *(_QWORD *)&v56[2 * v57],
                               0);
            v60 = *v59;
            v61 = v59[1];
            v62 = nullptr;
            if ( *v59 != v61 )
            {
              while ( *(_DWORD *)v60 != 1936224360 )
              {
                v60 += 16;
                if ( v60 == v61 )
                  goto LABEL_160;
              }
              if ( v60 != v61 )
              {
                v62 = *(__int64 **)(v60 + 8);
                goto LABEL_161;
              }
LABEL_160:
              v62 = nullptr;
            }
LABEL_161:
            if ( v62 == nullptr )
              v62 = &qword_141B5A4A0;
            if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v62 + 48LL))(*v62) != 0 )
              break;
            ++v57;
            v56 = v125;
            if ( v57 >= (v126 - (char *)v125) >> 3 )
              goto LABEL_218;
          }
          v63 = *v59;
          v64 = v59[1];
          v65 = nullptr;
          if ( *v59 != v64 )
          {
            while ( *(_DWORD *)v63 != 1885434984 )
            {
              v63 += 16;
              if ( v63 == v64 )
                goto LABEL_226;
            }
            if ( v63 == v64 )
              v65 = nullptr;
            else
              v65 = *(__int64 **)(v63 + 8);
          }
LABEL_226:
          if ( v65 != nullptr )
            v58 = v65;
          if ( v58 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)*v58 + 24LL))(*v58, v58, a3);
          }
        }
        goto LABEL_218;
      }
      goto LABEL_90;
    }
    if ( a2 == 1952605036 )
    {
      v52 = (*(__int64 (__fastcall **)(_DWORD *, __int64))(*(_QWORD *)a1 + 80LL))(a1, 1952605036);
      if ( v52 == 0
        || (*(unsigned __int8 (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)v52 + 16LL))(v52, 1952605036, a3) == 0 )
      {
        return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)a1 + 16LL))(a1, 1651204972, a3);
      }
      return (unsigned int)v3;
    }
    if ( a2 != 1953068140 )
      goto LABEL_142;
    return (unsigned int)v3;
  }
  if ( a2 > 1919968369 )
  {
    if ( a2 == 1919968370 )
      goto LABEL_285;
    if ( a2 != 1937072756 )
      goto LABEL_142;
    return (unsigned int)v3;
  }
  if ( a2 == 1886548067 )
    return (*(__int64 (__fastcall **)(_DWORD *, __int64, __int64 *))(*(_QWORD *)a1 + 16LL))(a1, 1835954275, a3);
  if ( a2 == 1919186281 )
  {
    if ( a3 != &qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    v26 = a1[4];
    if ( a1[3] != v26 )
    {
      v27 = sub_14083D4F0(v7);
      LODWORD(v126) = v26;
      v125 = (volatile signed __int32 *)(v27 + 40);
      sub_14083DFA0(a3, &v125);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
        v125,
        &v125);
    }
    return (unsigned int)v3;
  }
LABEL_142:
  if ( (_BYTE)word_141B60320 == 0 )
    goto LABEL_283;
  if ( a2 > 1853059954 )
  {
    if ( a2 > 1934390131 )
    {
      if ( a2 <= 1936286322 )
      {
        if ( a2 == 1934390132 )
        {
          v103 = sub_140FE35F0();
          if ( v103 == 0 )
            return (unsigned int)v3;
          v104 = sub_14101E620(v103, a1);
          if ( v104 == 0 )
            return (unsigned int)v3;
          v105 = v104;
          sub_1407C9510(&v125);
          v106 = *(_QWORD *)(v105 + 32);
          v107 = *(_QWORD *)(v105 + 24);
          v108 = (v106 - v107) >> 2;
          sub_140893BE0(&v125, v108);
          if ( v106 != v107 )
          {
            v110 = 1;
            if ( v108 >= 2 )
              v110 = v108;
            for ( i = 0; i != v110; ++i )
            {
              v112 = *(_DWORD *)(*(_QWORD *)(v105 + 24) + 4 * i);
              v113 = sub_14083D4F0(v109);
              LODWORD(v124) = v112;
              v123 = (volatile signed __int32 *)(v113 + 40);
              sub_14083B5F0(&v125, &v123);
              (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
                v123,
                &v123);
            }
          }
          sub_14083DB80(&v123, &v125);
          sub_14083DFA0(a3, &v123);
          (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
            v123,
            &v123);
          goto LABEL_218;
        }
        if ( a2 == 1935829358 )
        {
          v90 = sub_140FE35F0();
          if ( v90 != 0 )
          {
            v91 = sub_14101E620(v90, a1);
            if ( v91 != 0 )
            {
              sub_140FE6450(&v125, v91);
              sub_14083DFA0(a3, &v125);
              (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
                v125,
                &v125);
            }
          }
          return (unsigned int)v3;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1936286323:
            sub_1407C9510(&v125);
            (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 120LL))(a1, &v125);
            sub_14083DB80(&v123, &v125);
            sub_14083DFA0(a3, &v123);
            (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
              v123,
              &v123);
            goto LABEL_218;
          case 1937072751:
            return (*(__int64 (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)a1 + 272LL))(a1, a3);
          case 2020832610:
            sub_1407C9510(&v125);
            sub_140893BE0(&v125, 32);
            LODWORD(v3) = (*(__int64 (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 288LL))(
                            a1,
                            &v125);
            sub_14083DB80(&v123, &v125);
            sub_14083DFA0(a3, &v123);
            (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
              v123,
              &v123);
            goto LABEL_218;
          default:
            break;
        }
      }
      goto LABEL_282;
    }
    if ( a2 <= 1853122418 )
    {
      if ( a2 == 1853059955 )
      {
        v100 = sub_140FE37B0(a1);
        v102 = sub_14083D4F0(v101);
        LODWORD(v126) = v100;
        v125 = (volatile signed __int32 *)(v102 + 40);
        sub_14083DFA0(a3, &v125);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
          v125,
          &v125);
        return (unsigned int)v3;
      }
      if ( a2 != 1853122156 )
        goto LABEL_282;
      goto LABEL_261;
    }
    if ( a2 != 1853122419 )
    {
      if ( a2 == 1886547572 )
      {
        v96 = (*(__int64 (__fastcall **)(_DWORD *, __int64))(*(_QWORD *)a1 + 80LL))(a1, 1314212940);
        if ( v96 != 0 )
        {
          v97 = v96;
          if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v96 + 208LL))(v96) != 0 )
          {
            (*(void (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v97 + 144LL))(v97, &v125);
            sub_140FEAD00(&v125, &v123);
            sub_14083DFA0(a3, &v123);
            (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
              v123,
              &v123);
            (*(void (__fastcall **)(char *, char **))(*(_QWORD *)v126 + 16LL))(v126, &v126);
          }
        }
        return (unsigned int)v3;
      }
      goto LABEL_282;
    }
LABEL_261:
    v99 = sub_140FE35F0();
    if ( v99 != 0 )
    {
      sub_1410224E0(v99 + 1104, (unsigned int)a2, a3);
      return (unsigned int)v3;
    }
    goto LABEL_263;
  }
  if ( a2 <= 1685288289 )
  {
    if ( a2 <= 1634496108 )
    {
      if ( a2 == 1214862181 )
      {
        sub_1407C9510(&v125);
        sub_140893BE0(&v125, 1);
        LODWORD(v3) = (*(__int64 (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 312LL))(
                        a1,
                        &v125);
        sub_14083DB80(&v123, &v125);
        sub_14083DFA0(a3, &v123);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
          v123,
          &v123);
        goto LABEL_218;
      }
      if ( a2 == 1382378575 )
      {
        sub_1407C9510(&v125);
        (*(void (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 128LL))(a1, &v125);
        sub_14083DB80(&v123, &v125);
        sub_14083DFA0(a3, &v123);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
          v123,
          &v123);
        goto LABEL_218;
      }
      goto LABEL_282;
    }
    if ( a2 != 1634496109 )
    {
      if ( a2 == 1667460719 )
      {
        v92 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 104LL))(a1);
        v94 = sub_14083D4F0(v93);
        LOBYTE(v126) = v92;
        v125 = (volatile signed __int32 *)(v94 + 24);
        sub_14083DFA0(a3, &v125);
        (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v125 + 16LL))(
          v125,
          &v125);
        if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 48LL))(*a3, a3) == 0 )
        {
          v95 = (*(__int64 (__fastcall **)(_DWORD *, __int64))(*(_QWORD *)a1 + 80LL))(a1, 1667460719);
          if ( v95 != 0 )
            LODWORD(v3) = (*(__int64 (__fastcall **)(__int64, __int64, __int64 *))(*(_QWORD *)v95 + 16LL))(
                            v95,
                            1667460719,
                            a3);
        }
        return (unsigned int)v3;
      }
      goto LABEL_282;
    }
    v114 = *(_QWORD *)(*(_QWORD *)(qword_141ABD468 + 8) + 64LL);
    if ( qword_141B5A1A0 != v114 && qword_141B5A1F0 != v114
      || (*(unsigned int (__fastcall **)(_DWORD *))(*(_QWORD *)a1 + 56LL))(a1) == 35 )
    {
      v125 = a1;
      v123 = (volatile signed __int32 *)&v125;
      sub_140FEA8D0(&v123, a3);
      return (unsigned int)v3;
    }
LABEL_285:
    LODWORD(v3) = 0;
    return (unsigned int)v3;
  }
  if ( a2 <= 1852796520 )
  {
    if ( a2 == 1685288290 )
      return (*(__int64 (__fastcall **)(_DWORD *, __int64 *))(*(_QWORD *)a1 + 280LL))(a1, a3);
    if ( a2 == 1752397154 )
    {
      sub_1407C9510(&v125);
      sub_140893BE0(&v125, 32);
      LODWORD(v3) = (*(__int64 (__fastcall **)(_DWORD *, volatile signed __int32 **))(*(_QWORD *)a1 + 296LL))(a1, &v125);
      sub_14083DB80(&v123, &v125);
      sub_14083DFA0(a3, &v123);
      (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **))(*(_QWORD *)v123 + 16LL))(
        v123,
        &v123);
      goto LABEL_218;
    }
    goto LABEL_282;
  }
  if ( a2 == 1852796521 )
    goto LABEL_261;
  if ( a2 == 1852798067 )
  {
    v98 = sub_140FE35F0();
    if ( v98 != 0 )
    {
      sub_141021FC0(v98, a1, a3);
      return (unsigned int)v3;
    }
LABEL_263:
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
LABEL_282:
  if ( (*(unsigned __int8 (__fastcall **)(__int64, _DWORD *, _QWORD, __int64 *))(*(_QWORD *)qword_141B5FD48 + 40LL))(
         qword_141B5FD48,
         a1,
         (unsigned int)a2,
         a3) != 0 )
    return (unsigned int)v3;
LABEL_283:
  v115 = (*(__int64 (__fastcall **)(_DWORD *, _QWORD))(*(_QWORD *)a1 + 80LL))(a1, (unsigned int)a2);
  if ( v115 == 0 )
    goto LABEL_285;
  return (*(__int64 (__fastcall **)(__int64, _QWORD, __int64 *))(*(_QWORD *)v115 + 16LL))(v115, (unsigned int)a2, a3);
}
