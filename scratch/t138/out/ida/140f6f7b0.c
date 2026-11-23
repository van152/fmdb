__int64 __fastcall sub_140F6F7B0(
        __int64 a1,
        unsigned int a2,
        _QWORD *a3,
        unsigned __int8 a4,
        unsigned __int8 a5,
        char a6,
        char a7,
        char a8,
        char a9,
        char a10)
{
  _QWORD *v10; // r15
  char v12; // al
  __int64 v13; // rax
  __int64 *v14; // r8
  __int64 v15; // rdi
  __int64 v16; // rcx
  __int64 v17; // rax
  __int64 *v18; // rdx
  char v19; // al
  __int64 v20; // rax
  __int64 *v21; // rdx
  __int64 v22; // rax
  __int64 *v23; // rdx
  __int64 v24; // rax
  __int64 *v25; // rdx
  __int64 v26; // rsi
  __int64 v27; // rax
  int v28; // r14d
  char v29; // bl
  int v30; // edx
  int v31; // r9d
  int v32; // ecx
  __int64 v33; // rcx
  __int64 v34; // rsi
  volatile signed __int32 *v35; // rcx
  __int64 v36; // r15
  __int64 *v37; // r14
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 *v40; // r8
  __int64 v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rcx
  __int64 *v44; // rdi
  int v45; // edx
  int v46; // r9d
  int v47; // eax
  int v48; // ecx
  __int64 v49; // rcx
  char v50; // bl
  __int64 v51; // rcx
  int v52; // edi
  volatile signed __int32 *v53; // rdi
  char v54; // r12
  volatile signed __int32 *v55; // rdi
  __int64 v56; // rax
  volatile signed __int32 *v57; // rcx
  __int64 v58; // rdx
  __int64 v59; // rdx
  __int64 v60; // rcx
  __int64 v61; // rcx
  __int64 v62; // rcx
  __int64 v63; // rcx
  __int64 v64; // rax
  __int64 *v65; // r8
  __int64 v66; // rcx
  __int64 v67; // rax
  unsigned __int64 v68; // rbx
  __int64 *v69; // rdi
  __int64 v70; // rax
  __int64 v71; // rcx
  __int64 *v72; // r8
  __int64 v73; // rcx
  __int64 v74; // rax
  __int64 v75; // rcx
  __int64 *v76; // rdi
  __int64 v77; // r8
  char v78; // r14
  volatile signed __int32 *v79; // rdi
  volatile signed __int32 *v80; // rdi
  __int64 v81; // rdi
  volatile signed __int32 *v82; // rcx
  volatile signed __int32 *v83; // rdi
  __int64 v84; // rdi
  volatile signed __int32 *v85; // rcx
  __int64 v86; // rax
  __int16 v87; // r13
  void (__fastcall ***v88)(_QWORD, __int64); // rcx
  char v89; // di
  void (__fastcall ***v90)(_QWORD, __int64); // rcx
  void (__fastcall ***v91)(_QWORD, __int64); // rcx
  __int64 v92; // rcx
  volatile signed __int32 *v93; // rcx
  __int64 v94; // rsi
  volatile signed __int32 *v95; // rcx
  __int64 v97; // [rsp+38h] [rbp-48h]
  char v98[8]; // [rsp+50h] [rbp-30h] BYREF
  __int64 v99; // [rsp+58h] [rbp-28h] BYREF
  __int64 v100; // [rsp+60h] [rbp-20h]
  __int64 v101; // [rsp+70h] [rbp-10h]
  _QWORD *v102; // [rsp+78h] [rbp-8h]
  _QWORD v103[2]; // [rsp+80h] [rbp+0h] BYREF
  __int128 v104; // [rsp+90h] [rbp+10h] BYREF
  int v105; // [rsp+A0h] [rbp+20h]
  char v106; // [rsp+A4h] [rbp+24h]
  char v107; // [rsp+A5h] [rbp+25h]
  char v108; // [rsp+A6h] [rbp+26h]
  char v109; // [rsp+A7h] [rbp+27h]
  __int16 v110; // [rsp+A8h] [rbp+28h]
  char v111; // [rsp+AAh] [rbp+2Ah]
  bool v112; // [rsp+ABh] [rbp+2Bh]
  __int64 v113; // [rsp+B8h] [rbp+38h] BYREF
  __int64 v114; // [rsp+C0h] [rbp+40h]
  __int64 v115; // [rsp+C8h] [rbp+48h] BYREF
  __int64 v116; // [rsp+D0h] [rbp+50h]
  __int128 v117; // [rsp+E0h] [rbp+60h] BYREF
  __int64 v118; // [rsp+F0h] [rbp+70h]
  unsigned int v119; // [rsp+104h] [rbp+84h]
  __int64 v120; // [rsp+108h] [rbp+88h] BYREF
  __int128 v121; // [rsp+110h] [rbp+90h] BYREF
  __int64 v122; // [rsp+120h] [rbp+A0h]
  __int128 v123; // [rsp+130h] [rbp+B0h] BYREF
  __int64 v124; // [rsp+140h] [rbp+C0h]
  volatile signed __int32 *v125; // [rsp+148h] [rbp+C8h] BYREF
  unsigned __int8 v126; // [rsp+157h] [rbp+D7h]
  __int64 v127; // [rsp+158h] [rbp+D8h]

  v127 = -2;
  v126 = a4;
  v101 = a1;
  if ( *a3 == 0 )
    return 0;
  v10 = a3;
  sub_1407C9510(a1: &v99);
  sub_1407C9510(a1: &v117);
  v12 = sub_140F4BD10(a1: v10, a2: &v117);
  v119 = a2;
  if ( v12 != 0 )
  {
    v13 = v117;
    v14 = nullptr;
    if ( (_QWORD)v117 != *((_QWORD *)&v117 + 1) )
    {
      while ( *(_DWORD *)v13 != 1986359923 )
      {
        v13 += 16;
        if ( v13 == *((_QWORD *)&v117 + 1) )
          goto LABEL_11;
      }
      if ( v13 == *((_QWORD *)&v117 + 1) )
        v14 = nullptr;
      else
        v14 = *(__int64 **)(v13 + 8);
    }
LABEL_11:
    if ( v14 == nullptr )
      v14 = &qword_141B5A4A0;
    (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)*v14 + 128LL))(a1: *v14, a2: &v104);
    v123 = 0;
    v124 = 0x200000005LL;
    sub_1407C2950(a1: &v123, a2: &v104);
    v16 = v104;
    if ( (_QWORD)v104 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v104 - 4)) == 0 )
      sub_1412EC9A0(a1: v16 - 4);
    v104 = 0;
    v105 = 124518401;
    v110 = 0;
    v112 = true;
    v17 = v117;
    v18 = nullptr;
    if ( (_QWORD)v117 != *((_QWORD *)&v117 + 1) )
    {
      while ( *(_DWORD *)v17 != 1718444900 )
      {
        v17 += 16;
        if ( v17 == *((_QWORD *)&v117 + 1) )
          goto LABEL_23;
      }
      if ( v17 == *((_QWORD *)&v117 + 1) )
        v18 = nullptr;
      else
        v18 = *(__int64 **)(v17 + 8);
    }
LABEL_23:
    if ( v18 == nullptr )
      v18 = &qword_141B5A4A0;
    if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v18 + 48LL))(a1: *v18) != 0 )
    {
      v19 = 0;
    }
    else
    {
      v20 = v117;
      v21 = nullptr;
      if ( (_QWORD)v117 != *((_QWORD *)&v117 + 1) )
      {
        while ( *(_DWORD *)v20 != 1718447460 )
        {
          v20 += 16;
          if ( v20 == *((_QWORD *)&v117 + 1) )
            goto LABEL_34;
        }
        if ( v20 == *((_QWORD *)&v117 + 1) )
          v21 = nullptr;
        else
          v21 = *(__int64 **)(v20 + 8);
      }
LABEL_34:
      if ( v21 == nullptr )
        v21 = &qword_141B5A4A0;
      v19 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v21 + 48LL))(a1: *v21) ^ 1;
    }
    v106 = v19;
    v22 = v117;
    v23 = nullptr;
    if ( (_QWORD)v117 != *((_QWORD *)&v117 + 1) )
    {
      while ( *(_DWORD *)v22 != 1718444900 )
      {
        v22 += 16;
        if ( v22 == *((_QWORD *)&v117 + 1) )
          goto LABEL_44;
      }
      if ( v22 == *((_QWORD *)&v117 + 1) )
        v23 = nullptr;
      else
        v23 = *(__int64 **)(v22 + 8);
    }
LABEL_44:
    if ( v23 == nullptr )
      v23 = &qword_141B5A4A0;
    v107 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v23 + 48LL))(a1: *v23);
    v24 = v117;
    v25 = nullptr;
    if ( (_QWORD)v117 != *((_QWORD *)&v117 + 1) )
    {
      while ( *(_DWORD *)v24 != 1718447460 )
      {
        v24 += 16;
        if ( v24 == *((_QWORD *)&v117 + 1) )
          goto LABEL_53;
      }
      if ( v24 == *((_QWORD *)&v117 + 1) )
        v25 = nullptr;
      else
        v25 = *(__int64 **)(v24 + 8);
    }
LABEL_53:
    if ( v25 == nullptr )
      v25 = &qword_141B5A4A0;
    v109 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v25 + 48LL))(a1: *v25);
    v26 = qword_141ABDFE8;
    v27 = sub_14083D4F0();
    LOBYTE(v116) = 0;
    v115 = v27 + 24;
    v28 = 0;
    v29 = sub_140800A10(a1: v26, a2: &unk_141B5E3E8, a3: &v115, a4: 0);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v115 + 16LL))(a1: v115, a2: &v115);
    v111 = v29;
    v108 = 1;
    (*(void (__fastcall **)(_QWORD, __int64 *))(*(_QWORD *)*v10 + 16LL))(a1: *v10, a2: &v115);
    v30 = qword_141B5E418 + 4;
    if ( qword_141B5E418 != 0 )
      v28 = *(_DWORD *)qword_141B5E418;
    else
      v30 = 1100232177;
    if ( v115 != 0 )
      v31 = *(_DWORD *)v115;
    else
      v31 = 0;
    v32 = v115 + 4;
    if ( v115 == 0 )
      v32 = 1100232177;
    v112 = (unsigned int)sub_14080E770(a1: v32, a2: v30, a3: -1, a4: v31, a5: v28, a6: 0) == 0;
    v33 = v115;
    if ( v115 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v115 - 4)) == 0 )
      sub_1412EC9A0(a1: v33 - 4);
    sub_1407C9510(a1: &v115);
    sub_140F4BFB0(a1: &v115, a2: &v104);
    sub_140FC35E0(a1: v115, a2: v116, a3: (v116 - v115) >> 3);
    v120 = 0;
    v113 = 0;
    v34 = sub_1412EC810(a1: 264, a2: 7);
    *(_QWORD *)v34 = 0x700000000LL;
    strcpy((char *)(v34 + 8), "lang_db");
    _InterlockedIncrement((volatile signed __int32 *)v34);
    _InterlockedIncrement((volatile signed __int32 *)v34);
    if ( v120 == v34 + 4 )
    {
      if ( _InterlockedDecrement((volatile signed __int32 *)v34) == 0 )
        sub_1412EC9A0(a1: v34);
    }
    else
    {
      v35 = (volatile signed __int32 *)(v120 - 4);
      if ( v120 != 0 && _InterlockedDecrement(v35) == 0 )
        sub_1412EC9A0(a1: v35);
      v120 = v34 + 4;
    }
    v102 = v10;
    if ( _InterlockedDecrement((volatile signed __int32 *)v34) == 0 )
      sub_1412EC9A0(a1: v34);
    sub_140F4D8A0(a1: &v113, a2, a3: 0);
    if ( v116 != v115 )
    {
      v36 = (v116 - v115) >> 3;
      v114 = 0;
      do
      {
        v37 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD, _QWORD))(***(_QWORD ***)(v115 + 8 * v36 - 8) + 176LL))(
                           a1: **(_QWORD **)(v115 + 8 * v36 - 8),
                           a2: *(_QWORD *)(v115 + 8 * v36 - 8),
                           a3: 0);
        v38 = *v37;
        v39 = v37[1];
        v40 = nullptr;
        if ( *v37 != v39 )
        {
          while ( *(_DWORD *)v38 != 1986359923 )
          {
            v38 += 16;
            if ( v38 == v39 )
              goto LABEL_84;
          }
          if ( v38 != v39 )
          {
            v40 = *(__int64 **)(v38 + 8);
            goto LABEL_85;
          }
LABEL_84:
          v40 = nullptr;
        }
LABEL_85:
        if ( v40 == nullptr )
          v40 = &qword_141B5A4A0;
        (*(void (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)*v40 + 128LL))(a1: *v40, a2: v103);
        v121 = 0;
        v122 = 0x200000005LL;
        sub_1407C2950(a1: &v121, a2: v103);
        v41 = v103[0];
        if ( v103[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v103[0] - 4LL)) == 0 )
          sub_1412EC9A0(a1: v41 - 4);
        if ( (_DWORD)v121 != (_DWORD)v123
          || a10 == 0
          && (DWORD1(v121) > DWORD1(v123)
           || DWORD1(v121) == DWORD1(v123) && DWORD2(v121) > DWORD2(v123)
           || SHIDWORD(v121) > SHIDWORD(v123)
           || (unsigned int)v122 > (unsigned int)v124) )
        {
          goto LABEL_77;
        }
        v42 = *v37;
        v43 = v37[1];
        if ( *v37 == v43 )
          goto LABEL_104;
        while ( *(_DWORD *)v42 != 1718578276 )
        {
          v42 += 16;
          if ( v42 == v43 )
            goto LABEL_104;
        }
        if ( v42 == v43 )
LABEL_104:
          v44 = nullptr;
        else
          v44 = *(__int64 **)(v42 + 8);
        if ( v44 == nullptr )
          v44 = &qword_141B5A4A0;
        if ( dword_141B5A4E0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5A4E0);
          if ( dword_141B5A4E0 == -1 )
          {
            qword_141B5A4B0 = 0x141759DF8LL;
            byte_141B5A4B8 = 12;
            LOBYTE(v58) = 12;
            sub_1412EA280(a1: &qword_141B5A4C0, a2: v58);
            LOBYTE(v59) = 12;
            sub_1412EB230(a1: &qword_141B5A4D0, a2: v59);
            qword_141B5A4B0 = 0x141860DA8LL;
            qword_141B5A4C0 = 0x141860E88LL;
            qword_141B5A4D0 = 0x141860EA8LL;
            sub_141751048(a1: sub_1408436B0);
            sub_141750EA0(a1: &dword_141B5A4E0);
          }
        }
        sub_1408436F0(a1: &qword_141B5A4B0, a2: &v125, a3: v44);
        if ( v125 == nullptr )
          goto LABEL_77;
        (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v125 + 16LL))(a1: v125, a2: v103);
        v45 = qword_141B5E418 + 4;
        v46 = 0;
        v47 = 0;
        if ( qword_141B5E418 != 0 )
          v47 = *(_DWORD *)qword_141B5E418;
        else
          v45 = 1100232177;
        if ( v103[0] != 0 )
          v46 = *(_DWORD *)v103[0];
        v48 = LODWORD(v103[0]) + 4;
        if ( v103[0] == 0 )
          v48 = 1100232177;
        if ( (unsigned int)sub_14080E770(a1: v48, a2: v45, a3: -1, a4: v46, a5: v47, a6: 0) != 0 )
        {
          v49 = v103[0];
          if ( v103[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v103[0] - 4LL)) == 0 )
            sub_1412EC9A0(a1: v49 - 4);
        }
        else
        {
          v50 = sub_1407D30A0(a1: v125, a2: *v102);
          v51 = v103[0];
          if ( v103[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v103[0] - 4LL)) == 0 )
            sub_1412EC9A0(a1: v51 - 4);
          v52 = 3;
          if ( v50 != 0 )
            goto LABEL_154;
        }
        v53 = v125;
        sub_14080D0E0(a1: v103, a2: 0x1418E2C24LL);
        v54 = 1;
        if ( (*(unsigned __int8 (__fastcall **)(volatile signed __int32 *, __int64 *, _QWORD *))(*(_QWORD *)v53 + 192LL))(
               a1: v53,
               a2: &v120,
               a3: v103) == 0 )
        {
          v55 = v125;
          sub_14080D0E0(a1: v98, a2: 0x1418E2C24LL);
          v54 = (*(__int64 (__fastcall **)(volatile signed __int32 *, __int64 *, char *))(*(_QWORD *)v55 + 192LL))(
                  a1: v55,
                  a2: &v113,
                  a3: v98);
        }
        if ( (unsigned int)v121 > (unsigned int)v123
          || (_DWORD)v121 == (_DWORD)v123
          && (DWORD1(v121) > DWORD1(v123) || DWORD1(v121) == DWORD1(v123) && DWORD2(v121) > DWORD2(v123))
          || SHIDWORD(v121) > SHIDWORD(v123)
          || (unsigned int)v122 > (unsigned int)v124 )
        {
          v52 = 3;
          if ( (v114 & 1) != 0 )
            goto LABEL_154;
          v56 = (unsigned __int8)v114;
          if ( v54 != 0 )
            v56 = 1;
          v114 = v56;
        }
        sub_14083DC80(a1: v103, a2: v37);
        sub_14083BBE0(a1: &v99, a2: v103, a3: 0);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v103[0] + 16LL))(a1: v103[0], a2: v103);
        if ( v54 == 0 )
        {
LABEL_153:
          v52 = 0;
          goto LABEL_154;
        }
        v52 = 2;
        if ( (unsigned int)v121 >= (unsigned int)v123
          && ((_DWORD)v121 != (_DWORD)v123
           || DWORD1(v121) >= DWORD1(v123) && (DWORD1(v121) != DWORD1(v123) || DWORD2(v121) >= DWORD2(v123)))
          && SHIDWORD(v121) >= SHIDWORD(v123) )
        {
          if ( (unsigned int)v122 >= (unsigned int)v124 && (_DWORD)v121 == (_DWORD)v123 )
          {
            if ( DWORD1(v121) != DWORD1(v123)
              || *((_QWORD *)&v121 + 1) != *((_QWORD *)&v123 + 1)
              || (_DWORD)v122 != (_DWORD)v124 )
            {
              goto LABEL_153;
            }
          }
          else if ( (unsigned int)v122 >= (unsigned int)v124 )
          {
            goto LABEL_153;
          }
        }
LABEL_154:
        v57 = v125;
        if ( v125 != nullptr && _InterlockedDecrement(v125 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v57)(a1: v57, a2: 1);
        if ( v52 != 3 && v52 != 0 )
          break;
LABEL_77:
        --v36;
      }
      while ( v36 != 0 );
    }
    v60 = v113;
    if ( v113 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v113 - 4)) == 0 )
      sub_1412EC9A0(a1: v60 - 4);
    v61 = v120;
    v10 = v102;
    if ( v120 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v120 - 4)) == 0 )
      sub_1412EC9A0(a1: v61 - 4);
    sub_14083B0A0(a1: &v115);
    v62 = *((_QWORD *)&v104 + 1);
    if ( *((_QWORD *)&v104 + 1) != 0
      && _InterlockedDecrement((volatile signed __int32 *)(*((_QWORD *)&v104 + 1) - 4LL)) == 0 )
    {
      sub_1412EC9A0(a1: v62 - 4);
    }
    v63 = v104;
    a2 = v119;
    if ( (_QWORD)v104 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v104 - 4)) == 0 )
      sub_1412EC9A0(a1: v63 - 4);
  }
  sub_140833970(a1: &v117);
  v15 = sub_141750CC0(a1: 376);
  sub_140FCF870(a1: v15, a2);
  sub_1407C9510(a1: &v104);
  if ( (unsigned __int8)sub_140F4BD10(a1: v10, a2: &v104) != 0 )
  {
    v64 = v104;
    v65 = nullptr;
    if ( (_QWORD)v104 != *((_QWORD *)&v104 + 1) )
    {
      while ( *(_DWORD *)v64 != 1986359923 )
      {
        v64 += 16;
        if ( v64 == *((_QWORD *)&v104 + 1) )
          goto LABEL_183;
      }
      if ( v64 == *((_QWORD *)&v104 + 1) )
        v65 = nullptr;
      else
        v65 = *(__int64 **)(v64 + 8);
    }
LABEL_183:
    if ( v65 == nullptr )
      v65 = &qword_141B5A4A0;
    (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)*v65 + 128LL))(a1: *v65, a2: &v123);
    v117 = 0;
    v118 = 0x200000005LL;
    sub_1407C2950(a1: &v117, a2: &v123);
    v66 = v123;
    if ( (_QWORD)v123 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v123 - 4)) == 0 )
      sub_1412EC9A0(a1: v66 - 4);
    v67 = v99;
    if ( v100 != v99 )
    {
      v114 = v15;
      v68 = 0;
      while ( 1 )
      {
        v69 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD, _QWORD))(***(_QWORD ***)(v67 + 8 * v68) + 176LL))(
                           a1: **(_QWORD **)(v67 + 8 * v68),
                           a2: *(_QWORD *)(v67 + 8 * v68),
                           a3: 0);
        v70 = *v69;
        v71 = v69[1];
        v72 = nullptr;
        if ( *v69 != v71 )
        {
          while ( *(_DWORD *)v70 != 1986359923 )
          {
            v70 += 16;
            if ( v70 == v71 )
              goto LABEL_197;
          }
          if ( v70 != v71 )
          {
            v72 = *(__int64 **)(v70 + 8);
            goto LABEL_198;
          }
LABEL_197:
          v72 = nullptr;
        }
LABEL_198:
        if ( v72 == nullptr )
          v72 = &qword_141B5A4A0;
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v72 + 128LL))(a1: *v72, a2: &v115);
        v123 = 0;
        v124 = 0x200000005LL;
        sub_1407C2950(a1: &v123, a2: &v115);
        v73 = v115;
        if ( v115 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v115 - 4)) == 0 )
          sub_1412EC9A0(a1: v73 - 4);
        v74 = *v69;
        v75 = v69[1];
        if ( *v69 == v75 )
          goto LABEL_209;
        while ( *(_DWORD *)v74 != 1718578276 )
        {
          v74 += 16;
          if ( v74 == v75 )
            goto LABEL_209;
        }
        if ( v74 == v75 )
LABEL_209:
          v76 = nullptr;
        else
          v76 = *(__int64 **)(v74 + 8);
        if ( v76 == nullptr )
          v76 = &qword_141B5A4A0;
        if ( dword_141B5A4E0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(a1: &dword_141B5A4E0);
          if ( dword_141B5A4E0 == -1 )
          {
            sub_140843570(a1: &qword_141B5A4B0);
            sub_141751048(a1: sub_1408436B0);
            sub_141750EA0(a1: &dword_141B5A4E0);
            a2 = v119;
          }
        }
        sub_1408436F0(a1: &qword_141B5A4B0, a2: &v125, a3: v76);
        v78 = 1;
        if ( (unsigned int)v123 >= (unsigned int)v117
          && ((_DWORD)v123 != (_DWORD)v117
           || DWORD1(v123) >= DWORD1(v117) && (DWORD1(v123) != DWORD1(v117) || DWORD2(v123) >= DWORD2(v117)))
          && SHIDWORD(v123) >= SHIDWORD(v117) )
        {
          v77 = (unsigned int)v118;
          v78 = (unsigned int)v124 < (unsigned int)v118;
          if ( (unsigned int)v124 >= (unsigned int)v118 && (_DWORD)v123 == (_DWORD)v117 )
            v78 = DWORD1(v123) == DWORD1(v117)
               && (DWORD2(v117) ^ DWORD2(v123) | HIDWORD(v117) ^ HIDWORD(v123) | (unsigned int)v118 ^ (unsigned int)v124) == 0;
        }
        v115 = 0;
        LOBYTE(v77) = 1;
        sub_140F4D8A0(a1: &v115, a2, a3: v77);
        v79 = v125;
        sub_14080D0E0(a1: &v121, a2: 0x1418E2C24LL);
        if ( (*(unsigned __int8 (__fastcall **)(volatile signed __int32 *, __int64 *, __int128 *))(*(_QWORD *)v79 + 192LL))(
               a1: v79,
               a2: &v115,
               a3: &v121) == 0 )
        {
          sub_140F4D8A0(a1: &v115, a2, a3: 0);
          v80 = v125;
          sub_14080D0E0(a1: &v121, a2: 0x1418E2C24LL);
          if ( (*(unsigned __int8 (__fastcall **)(volatile signed __int32 *, __int64 *, __int128 *))(*(_QWORD *)v80 + 192LL))(
                 a1: v80,
                 a2: &v115,
                 a3: &v121) == 0 )
          {
            v81 = sub_1412EC810(a1: 264, a2: 14);
            *(_QWORD *)v81 = 0xE00000000LL;
            strcpy((char *)(v81 + 8), "lang_update_db");
            _InterlockedIncrement((volatile signed __int32 *)v81);
            _InterlockedIncrement((volatile signed __int32 *)v81);
            if ( v115 == v81 + 4 )
            {
              if ( _InterlockedDecrement((volatile signed __int32 *)v81) == 0 )
                sub_1412EC9A0(a1: v81);
            }
            else
            {
              v82 = (volatile signed __int32 *)(v115 - 4);
              if ( v115 != 0 && _InterlockedDecrement(v82) == 0 )
                sub_1412EC9A0(a1: v82);
              v115 = v81 + 4;
            }
            if ( _InterlockedDecrement((volatile signed __int32 *)v81) == 0 )
              sub_1412EC9A0(a1: v81);
            v83 = v125;
            sub_14080D0E0(a1: &v121, a2: 0x1418E2C24LL);
            if ( (*(unsigned __int8 (__fastcall **)(volatile signed __int32 *, __int64 *, __int128 *))(*(_QWORD *)v83 + 192LL))(
                   a1: v83,
                   a2: &v115,
                   a3: &v121) == 0 )
            {
              v84 = sub_1412EC810(a1: 264, a2: 7);
              *(_QWORD *)v84 = 0x700000000LL;
              strcpy((char *)(v84 + 8), "lang_db");
              _InterlockedIncrement((volatile signed __int32 *)v84);
              _InterlockedIncrement((volatile signed __int32 *)v84);
              if ( v115 == v84 + 4 )
              {
                if ( _InterlockedDecrement((volatile signed __int32 *)v84) == 0 )
                  sub_1412EC9A0(a1: v84);
              }
              else
              {
                v85 = (volatile signed __int32 *)(v115 - 4);
                if ( v115 != 0 && _InterlockedDecrement(v85) == 0 )
                  sub_1412EC9A0(a1: v85);
                v115 = v84 + 4;
              }
              if ( _InterlockedDecrement((volatile signed __int32 *)v84) == 0 )
                sub_1412EC9A0(a1: v84);
            }
          }
        }
        *(_QWORD *)&v121 = 0x80100004E554C4CLL;
        sub_14080D0E0(a1: &v120, a2: 0x1418E2C24LL);
        LOBYTE(v97) = 0;
        sub_1407D0F70(
          a1: (unsigned int)&v121,
          a2: (unsigned int)v103,
          a3: (unsigned int)&v125,
          a4: (unsigned int)&v115,
          a5: (__int64)&v120,
          a6: 0,
          a7: 0,
          v97);
        v86 = v103[0];
        if ( v103[0] != 0 )
        {
          v87 = *(_WORD *)(v101 + 1416);
          *(_WORD *)(v101 + 1416) = WORD2(v121);
          v113 = v86;
          _InterlockedIncrement((volatile signed __int32 *)(v86 + 8));
          sub_1407C5A20(a1: &v120, a2: &v113, a3: &v125, a4: &v115);
          v88 = (void (__fastcall ***)(_QWORD, __int64))v113;
          if ( v113 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v113 + 8)) == 0 )
            (**v88)(a1: v88, a2: 1);
          if ( v120 == 0
            || (LOBYTE(v97) = a9,
                v89 = 1,
                (unsigned __int8)sub_140FD0F50(
                                   a1: v114,
                                   a2: (unsigned int)&v120,
                                   a3: v126,
                                   a4: a5,
                                   a5: a6,
                                   a6: a7,
                                   a7: a8,
                                   a8: v97,
                                   a9: v78,
                                   a10: v68 == 0) == 0) )
          {
            v89 = 0;
          }
          *(_WORD *)(v101 + 1416) = v87;
          v90 = (void (__fastcall ***)(_QWORD, __int64))v120;
          if ( v120 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v120 + 8)) == 0 )
            (**v90)(a1: v90, a2: 1);
          a2 = v119;
        }
        else
        {
          sub_140F2B090();
          v89 = 0;
        }
        v91 = (void (__fastcall ***)(_QWORD, __int64))v103[0];
        if ( v103[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v103[0] + 8LL)) == 0 )
          (**v91)(a1: v91, a2: 1);
        v92 = v115;
        if ( v115 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v115 - 4)) == 0 )
          sub_1412EC9A0(a1: v92 - 4);
        if ( v89 == 0 )
          break;
        v93 = v125;
        if ( v125 != nullptr && _InterlockedDecrement(v125 + 2) == 0 )
          (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v93)(a1: v93, a2: 1);
        ++v68;
        v67 = v99;
        if ( v68 >= (v100 - v99) >> 3 )
        {
          v15 = v114;
          goto LABEL_274;
        }
      }
      v94 = v114;
      sub_140FCF970(a1: v114);
      sub_141750CFC(a1: v94);
      v95 = v125;
      if ( v125 != nullptr && _InterlockedDecrement(v125 + 2) == 0 )
        (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v95)(a1: v95, a2: 1);
      v15 = 0;
    }
  }
  else
  {
    sub_140FCF970(a1: v15);
    sub_141750CFC(a1: v15);
    v15 = 0;
  }
LABEL_274:
  sub_140833970(a1: &v104);
  sub_14083B0A0(a1: &v99);
  return v15;
}
