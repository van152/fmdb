__int64 __fastcall sub_1415E54E0(_QWORD *a1)
{
  __int64 v2; // rsi
  volatile signed __int32 *v3; // rcx
  __int64 v4; // rax
  volatile signed __int32 *v5; // rcx
  __int64 result; // rax
  __int64 v7; // rax
  __int64 *v8; // r12
  __int64 v9; // rdx
  __int64 *v10; // rdx
  __int64 *v11; // rax
  __int64 v12; // rdx
  __int64 v13; // rcx
  __int64 *v14; // r8
  volatile signed __int32 *v15; // rax
  __int64 v16; // rcx
  unsigned __int64 v17; // r14
  volatile signed __int32 *v18; // r13
  __int64 v19; // rax
  __int64 v20; // rcx
  __int64 v21; // rsi
  __int64 v22; // rdx
  int v23; // ecx
  _DWORD *v24; // rax
  __int64 v25; // rcx
  bool v26; // di
  _DWORD *v27; // rcx
  __int64 v28; // rax
  __int64 v29; // rax
  __int64 *v30; // rdi
  __int64 v31; // rax
  __int64 v32; // rcx
  _QWORD *v33; // rbx
  __int64 v34; // rcx
  char v35; // si
  __int64 *v36; // r8
  __int64 v37; // rsi
  __int64 v38; // rcx
  _DWORD *v39; // rcx
  __int64 v40; // rax
  __int64 v41; // rcx
  __int64 *v42; // r8
  volatile signed __int32 *v43; // rcx
  volatile signed __int32 *v44; // rsi
  volatile signed __int32 *v45; // rsi
  _DWORD *v46; // rcx
  __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rdx
  __int64 *v50; // rdx
  __int64 v51; // rax
  __int64 v52; // rcx
  __int64 *v53; // rdx
  __int64 v54; // rdx
  __int64 v55; // rax
  volatile signed __int32 *v56; // rax
  char *v57; // r12
  __int64 v58; // rax
  __int64 v59; // rdi
  unsigned __int64 v60; // rsi
  unsigned __int64 v61; // r15
  unsigned __int64 v62; // rbx
  unsigned __int64 v63; // rsi
  __int64 *v64; // rax
  __int64 v65; // rcx
  char *v66; // rcx
  char *v67; // rdx
  unsigned __int64 v68; // r10
  _QWORD *v69; // rdx
  unsigned __int64 v70; // rax
  _QWORD *v71; // rax
  __int64 v72; // r10
  __int64 v73; // r8
  unsigned __int64 v74; // r9
  unsigned __int64 v75; // rdi
  __int64 v76; // rdx
  __int128 v77; // xmm1
  __int128 v78; // xmm1
  __int128 v79; // xmm1
  unsigned __int64 v80; // r10
  __int64 v81; // r10
  __int64 v82; // r8
  unsigned __int64 v83; // r9
  unsigned __int64 v84; // rdi
  __int64 v85; // rcx
  __int64 v86; // rsi
  __int128 v87; // xmm1
  __int128 v88; // xmm1
  __int128 v89; // xmm1
  _QWORD *v90; // rax
  __int64 v91; // rax
  __int64 v92; // r8
  unsigned __int64 v93; // rdi
  unsigned __int64 v94; // rsi
  __int64 v95; // rdx
  __int128 v96; // xmm1
  __int128 v97; // xmm1
  __int128 v98; // xmm1
  _QWORD *v99; // rsi
  char *v100; // rsi
  __int64 v101; // rcx
  volatile signed __int32 *v102; // rcx
  __int64 v103; // rcx
  void (__fastcall ***v104)(_QWORD, __int64); // rcx
  __int64 v105; // rcx
  _DWORD *v106; // rcx
  volatile signed __int32 *v107; // rcx
  volatile signed __int32 *v108; // rsi
  __int64 v109; // rsi
  __int64 v110; // rcx
  __int64 v111; // rcx
  __int64 v112; // [rsp+38h] [rbp-48h]
  __int64 v113; // [rsp+48h] [rbp-38h] BYREF
  __int64 v114; // [rsp+50h] [rbp-30h]
  __int64 *v115; // [rsp+58h] [rbp-28h]
  unsigned __int64 v116; // [rsp+60h] [rbp-20h]
  _QWORD *v117; // [rsp+68h] [rbp-18h]
  __int64 v118; // [rsp+70h] [rbp-10h]
  __int64 v119; // [rsp+78h] [rbp-8h] BYREF
  __int64 *v120; // [rsp+80h] [rbp+0h]
  _DWORD *v121; // [rsp+88h] [rbp+8h] BYREF
  __int128 v122; // [rsp+90h] [rbp+10h] BYREF
  __int64 v123; // [rsp+A0h] [rbp+20h]
  __int16 v124; // [rsp+A8h] [rbp+28h]
  __int64 v125; // [rsp+B0h] [rbp+30h]
  int v126; // [rsp+B8h] [rbp+38h]
  volatile signed __int32 *v127; // [rsp+C0h] [rbp+40h]
  int v128[4]; // [rsp+C8h] [rbp+48h] BYREF
  volatile signed __int32 *v129; // [rsp+D8h] [rbp+58h] BYREF
  _DWORD *v130; // [rsp+E0h] [rbp+60h] BYREF
  __int64 v131; // [rsp+E8h] [rbp+68h] BYREF
  volatile signed __int32 *v132; // [rsp+F0h] [rbp+70h] BYREF
  _DWORD *v133; // [rsp+F8h] [rbp+78h] BYREF
  _QWORD *v134; // [rsp+100h] [rbp+80h]
  __int64 v135; // [rsp+108h] [rbp+88h]

  v135 = -2;
  sub_14080D0E0(a1: &v122, a2: 0x1419236C6LL);
  v132 = nullptr;
  v2 = sub_1412EC810(a1: 264, a2: 14);
  *(_QWORD *)v2 = 0xE00000000LL;
  strcpy((char *)(v2 + 8), "tactics/styles");
  v3 = v132;
  if ( v132 != nullptr )
  {
    v3 = v132 - 1;
    if ( _InterlockedDecrement(v132 - 1) == 0 )
      sub_1412EC9A0(a1: v3);
  }
  v132 = nullptr;
  _InterlockedIncrement((volatile signed __int32 *)v2);
  v132 = (volatile signed __int32 *)(v2 + 4);
  v4 = sub_1407F33D0(a1: v3);
  v129 = (volatile signed __int32 *)sub_14080D8E0(a1: v4 + 8, a2: &v132);
  sub_1407FCAF0(a1: &v119, a2: &v129, a3: &v122);
  v5 = v132;
  if ( v132 != nullptr && _InterlockedDecrement(v132 - 1) == 0 )
    sub_1412EC9A0(a1: v5 - 1);
  v129 = nullptr;
  result = sub_1415E3FC0(a1: &v132);
  if ( v132 != nullptr )
  {
    v134 = a1;
    result = (*(__int64 (__fastcall **)(volatile signed __int32 *, __int128 *, __int64 *, void *, volatile signed __int32 **, int))(*(_QWORD *)v132 + 216LL))(
               a1: v132,
               a2: &v122,
               a3: &qword_141B59758,
               a4: &unk_141B66298,
               a5: &v129,
               a6: 4);
    if ( v129 != nullptr )
    {
      if ( v119 != 0 )
      {
        v7 = sub_141758910(a1: *(_QWORD *)(v119 + 32), a2: 0, a3: &unk_141A83C00, a4: &unk_141A83BC0, a5: 0);
        v8 = &qword_141B5A458;
        if ( v7 != 0 )
          v8 = (__int64 *)(v7 + 8);
      }
      else
      {
        v8 = &qword_141B5A458;
      }
      result = *v8;
      if ( v8[1] != *v8 )
      {
        v117 = v134 + 7;
        v9 = 0;
        v120 = v8;
        while ( 1 )
        {
          v114 = v9;
          v10 = *(__int64 **)(result + 16 * v9 + 8);
          if ( v10 == nullptr )
            v10 = &qword_141B5A4A0;
          v11 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v10 + 176LL))(
                             a1: *v10,
                             a2: v10,
                             a3: 0);
          v12 = *v11;
          v115 = v11;
          v13 = v11[1];
          v14 = nullptr;
          if ( v12 != v13 )
          {
            while ( *(_DWORD *)v12 != 1718578276 )
            {
              v12 += 16;
              if ( v12 == v13 )
                goto LABEL_25;
            }
            if ( v12 != v13 )
            {
              v14 = *(__int64 **)(v12 + 8);
              goto LABEL_26;
            }
LABEL_25:
            v14 = nullptr;
          }
LABEL_26:
          if ( v14 == nullptr )
            v14 = &qword_141B5A4A0;
          (*(void (__fastcall **)(__int64, _DWORD **))(*(_QWORD *)*v14 + 128LL))(a1: *v14, a2: &v121);
          v15 = v129;
          v16 = *((_QWORD *)v129 + 1);
          if ( *((_QWORD *)v129 + 2) != v16 )
            break;
LABEL_240:
          v106 = v121;
          if ( v121 != nullptr && _InterlockedDecrement(v121 - 1) == 0 )
            sub_1412EC9A0(a1: v106 - 1);
          v9 = v114 + 1;
          result = *v8;
          if ( v114 + 1 >= (unsigned __int64)((v8[1] - *v8) >> 4) )
            goto LABEL_243;
        }
        v17 = 0;
        while ( 1 )
        {
          v18 = *(volatile signed __int32 **)(v16 + 8 * v17);
          if ( v18 == nullptr )
            goto LABEL_30;
          _InterlockedIncrement(v18 + 2);
          (*(void (__fastcall **)(volatile signed __int32 *, __int128 *))(*(_QWORD *)v18 + 16LL))(a1: v18, a2: &v122);
          v19 = v122;
          if ( (_QWORD)v122 != 0 )
          {
            v131 = 0;
            _InterlockedIncrement((volatile signed __int32 *)(v122 - 4));
            v20 = v122;
            v131 = v19;
            if ( (_QWORD)v122 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v122 - 4)) == 0 )
              sub_1412EC9A0(a1: v20 - 4);
          }
          else
          {
            v131 = 0;
          }
          (*(void (__fastcall **)(volatile signed __int32 *, __int128 *))(*(_QWORD *)v18 + 16LL))(a1: v18, a2: &v122);
          v21 = v122;
          v22 = v122 + 4;
          if ( (_QWORD)v122 != 0 )
          {
            v23 = *(_DWORD *)v122;
            v24 = v121;
            if ( *(_DWORD *)v122 == -1 )
              goto LABEL_42;
            if ( v121 != nullptr )
            {
LABEL_41:
              if ( *v24 != v23 )
                goto LABEL_48;
              goto LABEL_42;
            }
          }
          else
          {
            v22 = 0x1419435F1LL;
            v23 = 0;
            v24 = v121;
            if ( v121 != nullptr )
              goto LABEL_41;
          }
          if ( v23 != 0 )
          {
LABEL_48:
            v26 = false;
            if ( (_QWORD)v122 == 0 )
              goto LABEL_51;
LABEL_49:
            if ( _InterlockedDecrement((volatile signed __int32 *)(v21 - 4)) == 0 )
              sub_1412EC9A0(a1: v21 - 4);
            goto LABEL_51;
          }
LABEL_42:
          v25 = (__int64)(v24 + 1);
          if ( v24 == nullptr )
            v25 = 0x1419435F1LL;
          v26 = (unsigned int)sub_141758D90(a1: v25, a2: v22) == 0;
          if ( v21 != 0 )
            goto LABEL_49;
LABEL_51:
          if ( v26 )
          {
            (*(void (__fastcall **)(volatile signed __int32 *, __int64 *))(*(_QWORD *)v18 + 16LL))(a1: v18, a2: &v113);
            *(_QWORD *)&v122 = 0x80100004E554C4CLL;
            LOBYTE(v112) = 0;
            sub_1407D0F70(
              a1: (unsigned int)&v122,
              a2: (unsigned int)&v133,
              a3: (unsigned int)&v132,
              a4: (unsigned int)&v113,
              a5: (__int64)&unk_141B66298,
              a6: 0,
              a7: 0,
              v112);
            v27 = v133;
            v130 = v133;
            v133 = nullptr;
            v28 = v113;
            if ( v113 != 0 )
            {
              if ( _InterlockedDecrement((volatile signed __int32 *)(v113 - 4)) == 0 )
                sub_1412EC9A0(a1: v28 - 4);
              v27 = v130;
            }
            if ( v27 != nullptr )
            {
              LODWORD(v123) = 536;
              BYTE4(v123) = -1;
              v125 = 0;
              v124 = 1026;
              v122 = 0;
              v29 = qword_141B59EE0;
              if ( qword_141B59EE0 != 0 )
              {
                _InterlockedIncrement((volatile signed __int32 *)(qword_141B59EE0 - 4));
                v27 = v130;
              }
              v125 = v29;
              v126 = 1314212940;
              v127 = nullptr;
              v128[0] = 0;
              (*(void (__fastcall **)(_DWORD *, _DWORD **, __int64))(*(_QWORD *)v27 + 40LL))(a1: v27, a2: &v133, a3: 2);
              (*(void (__fastcall **)(_DWORD *, int *, __int64))(*(_QWORD *)v130 + 40LL))(a1: v130, a2: v128, a3: 4);
              if ( (unsigned __int8)sub_1416FD5B0(a1: &v122, a2: &v130) == 0 || v130[4] != 0 )
                goto LABEL_220;
              v30 = v115;
              v31 = *v115;
              v32 = v115[1];
              if ( *v115 == v32 )
              {
                v36 = nullptr;
                v33 = v134;
              }
              else
              {
                v33 = v134;
                while ( *(_DWORD *)v31 != 1952807028 )
                {
                  v31 += 16;
                  if ( v31 == v32 )
                    goto LABEL_76;
                }
                if ( v31 != v32 )
                {
                  v36 = *(__int64 **)(v31 + 8);
                  goto LABEL_77;
                }
LABEL_76:
                v36 = nullptr;
              }
LABEL_77:
              if ( v36 == nullptr )
                v36 = &qword_141B5A4A0;
              (*(void (__fastcall **)(__int64, _DWORD **))(*(_QWORD *)*v36 + 128LL))(a1: *v36, a2: &v133);
              v37 = (__int64)v133;
              if ( v133 != nullptr )
              {
                _InterlockedIncrement(v133 - 1);
                v38 = v125;
                if ( v125 == v37 )
                {
                  if ( _InterlockedDecrement((volatile signed __int32 *)(v37 - 4)) == 0 )
                    sub_1412EC9A0(a1: v37 - 4);
                }
                else
                {
                  if ( v125 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 - 4)) == 0 )
LABEL_83:
                    sub_1412EC9A0(a1: v38 - 4);
LABEL_84:
                  v125 = v37;
                }
                v39 = v133;
                if ( v133 != nullptr && _InterlockedDecrement(v133 - 1) == 0 )
                  sub_1412EC9A0(a1: v39 - 1);
              }
              else
              {
                v38 = v125;
                if ( v125 != 0 )
                {
                  v37 = 0;
                  if ( _InterlockedDecrement((volatile signed __int32 *)(v125 - 4)) == 0 )
                    goto LABEL_83;
                  goto LABEL_84;
                }
              }
              v40 = *v30;
              v41 = v30[1];
              if ( *v30 == v41 )
                goto LABEL_97;
              while ( *(_DWORD *)v40 != 1751740020 )
              {
                v40 += 16;
                if ( v40 == v41 )
                  goto LABEL_97;
              }
              if ( v40 == v41 )
LABEL_97:
                v42 = nullptr;
              else
                v42 = *(__int64 **)(v40 + 8);
              if ( v42 == nullptr )
                v42 = &qword_141B5A4A0;
              (*(void (__fastcall **)(__int64, _DWORD **))(*(_QWORD *)*v42 + 128LL))(a1: *v42, a2: &v133);
              v43 = v127 - 1;
              if ( v127 == nullptr )
                v43 = nullptr;
              v44 = v133 - 1;
              if ( v133 != nullptr )
              {
                if ( v127 != nullptr && _InterlockedDecrement(v43) == 0 )
                  sub_1412EC9A0(a1: v43);
                v127 = nullptr;
                _InterlockedIncrement(v44);
                v45 = v44 + 1;
              }
              else
              {
                if ( v127 != nullptr && _InterlockedDecrement(v43) == 0 )
                  sub_1412EC9A0(a1: v43);
                v45 = nullptr;
              }
              v127 = v45;
              v46 = v133;
              if ( v133 != nullptr && _InterlockedDecrement(v133 - 1) == 0 )
                sub_1412EC9A0(a1: v46 - 1);
              v47 = *v30;
              v48 = v30[1];
              if ( *v30 != v48 )
              {
                v49 = *v30;
                while ( *(_DWORD *)v49 != 1937000772 )
                {
                  v49 += 16;
                  if ( v49 == v48 )
                    goto LABEL_141;
                }
                if ( v49 != v48 && *(_QWORD *)(v49 + 8) != 0 )
                {
                  while ( *(_DWORD *)v47 != 1937000772 )
                  {
                    v47 += 16;
                    if ( v47 == v48 )
                      goto LABEL_128;
                  }
                  if ( v47 != v48 )
                  {
                    v50 = *(__int64 **)(v47 + 8);
                    goto LABEL_129;
                  }
LABEL_128:
                  v50 = nullptr;
LABEL_129:
                  if ( v50 == nullptr )
                    v50 = &qword_141B5A4A0;
                  v128[0] = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v50 + 80LL))(a1: *v50);
                  v51 = *v30;
                  v52 = v30[1];
                  if ( *v30 == v52 )
                    goto LABEL_137;
                  while ( *(_DWORD *)v51 != 1937000772 )
                  {
                    v51 += 16;
                    if ( v51 == v52 )
                      goto LABEL_137;
                  }
                  if ( v51 == v52 )
LABEL_137:
                    v53 = nullptr;
                  else
                    v53 = *(__int64 **)(v51 + 8);
                  if ( v53 == nullptr )
                    v53 = &qword_141B5A4A0;
                  v126 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v53 + 80LL))(a1: *v53);
                }
              }
LABEL_141:
              v54 = v33[8];
              if ( v54 == v33[9] )
              {
                sub_1415E65F0(a1: v117, a2: v54, a3: &v122);
              }
              else
              {
                *(_WORD *)(v54 + 24) = v124;
                *(_QWORD *)(v54 + 16) = v123;
                *(_OWORD *)v54 = v122;
                *(_QWORD *)(v54 + 32) = 0;
                if ( (__int128 *)v54 == &v122 )
                {
                  *(_DWORD *)(v54 + 40) = v126;
                  *(_QWORD *)(v54 + 48) = 0;
                }
                else
                {
                  v55 = v125;
                  if ( v125 != 0 )
                    _InterlockedIncrement((volatile signed __int32 *)(v125 - 4));
                  *(_QWORD *)(v54 + 32) = v55;
                  *(_DWORD *)(v54 + 40) = v126;
                  *(_QWORD *)(v54 + 48) = 0;
                  v56 = v127;
                  if ( v127 != nullptr )
                    _InterlockedIncrement(v127 - 1);
                  *(_QWORD *)(v54 + 48) = v56;
                }
                *(_DWORD *)(v54 + 56) = v128[0];
                v33[8] += 64LL;
              }
              v57 = (char *)v33[11];
              if ( v57 != (char *)v33[12] )
              {
                *(_QWORD *)v57 = 0;
                if ( v57 != (char *)&v131 )
                {
                  v58 = v131;
                  if ( v131 != 0 )
                    _InterlockedIncrement((volatile signed __int32 *)(v131 - 4));
                  *(_QWORD *)v57 = v58;
                }
                v33[11] += 8LL;
                v8 = v120;
                goto LABEL_220;
              }
              v59 = (__int64)&v57[-v33[10]];
              v60 = v59 >> 3;
              v61 = v60 + (v60 >> 1);
              v116 = (v59 >> 3) + 1;
              if ( v61 <= v116 )
                v61 = v60 + 1;
              v118 = v59 >> 3;
              if ( v60 > 0x1FFFFFFFFFFFFFFFLL - (v60 >> 1) )
                v61 = 0x1FFFFFFFFFFFFFFFLL;
              v62 = sub_1407E4490(a1: qword_141ABD470, a2: 8 * v61);
              v63 = v59 & 0xFFFFFFFFFFFFFFF8uLL;
              v64 = (__int64 *)((v59 & 0xFFFFFFFFFFFFFFF8uLL) + v62);
              *v64 = 0;
              if ( v64 != &v131 )
              {
                v65 = v131;
                if ( v131 != 0 )
                  _InterlockedIncrement((volatile signed __int32 *)(v131 - 4));
                *v64 = v65;
              }
              v66 = (char *)v134[10];
              v67 = (char *)v134[11];
              if ( v67 != v57 )
              {
                if ( v66 == v57 )
                  goto LABEL_187;
                v68 = v57 - v66 - 8;
                if ( v68 < 0x88 )
                {
                  v69 = (_QWORD *)v62;
                  do
                  {
LABEL_185:
                    *v69 = *(_QWORD *)v66;
                    *(_QWORD *)v66 = 0;
                    ++v69;
                    v66 += 8;
                  }
                  while ( v66 != v57 );
LABEL_186:
                  v67 = (char *)v134[11];
LABEL_187:
                  if ( v67 != v57 )
                  {
                    v80 = v67 - v57 - 8;
                    if ( v80 < 0xB8
                      || v62 + v63 + 8 < (unsigned __int64)&v57[(v80 & 0xFFFFFFFFFFFFFFF8uLL) + 8]
                      && (unsigned __int64)v57 < v62 + (v80 & 0xFFFFFFFFFFFFFFF8uLL) + v63 + 16 )
                    {
LABEL_198:
                      v90 = v64 + 1;
                      do
                      {
                        *v90 = *(_QWORD *)v57;
                        *(_QWORD *)v57 = 0;
                        v57 += 8;
                        ++v90;
                      }
                      while ( v57 != v67 );
                    }
                    else
                    {
                      v81 = (v80 >> 3) + 1;
                      v82 = v81 & 0x3FFFFFFFFFFFFFFCLL;
                      v83 = (((v81 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
                      if ( (v81 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
                      {
                        v86 = 0;
                        if ( (v83 & 1) != 0 )
                          goto LABEL_195;
                      }
                      else
                      {
                        v84 = v83 & 0xFFFFFFFFFFFFFFFEuLL;
                        v85 = v62 + 8 * v118 + 56;
                        v86 = 0;
                        do
                        {
                          v87 = *(_OWORD *)&v57[8 * v86 + 16];
                          *(_OWORD *)(v85 + 8 * v86 - 48) = *(_OWORD *)&v57[8 * v86];
                          *(_OWORD *)(v85 + 8 * v86 - 32) = v87;
                          *(_OWORD *)&v57[8 * v86] = 0;
                          *(_OWORD *)&v57[8 * v86 + 16] = 0;
                          v88 = *(_OWORD *)&v57[8 * v86 + 48];
                          *(_OWORD *)(v85 + 8 * v86 - 16) = *(_OWORD *)&v57[8 * v86 + 32];
                          *(_OWORD *)(v85 + 8 * v86) = v88;
                          *(_OWORD *)&v57[8 * v86 + 32] = 0;
                          *(_OWORD *)&v57[8 * v86 + 48] = 0;
                          v86 += 8;
                          v84 -= 2LL;
                        }
                        while ( v84 != 0 );
                        if ( (v83 & 1) != 0 )
                        {
LABEL_195:
                          v89 = *(_OWORD *)&v57[8 * v86 + 16];
                          *(_OWORD *)&v64[v86 + 1] = *(_OWORD *)&v57[8 * v86];
                          *(_OWORD *)&v64[v86 + 3] = v89;
                          *(_OWORD *)&v57[8 * v86] = 0;
                          *(_OWORD *)&v57[8 * v86 + 16] = 0;
                        }
                      }
                      if ( v81 != v82 )
                      {
                        v57 += 8 * v82;
                        v64 += v82;
                        goto LABEL_198;
                      }
                    }
                  }
LABEL_209:
                  v57 = (char *)v134[10];
LABEL_210:
                  v99 = v134;
                  if ( v57 != nullptr )
                  {
                    v100 = (char *)v134[11];
                    if ( v57 == v100 )
                    {
                      v99 = v134;
                    }
                    else
                    {
                      do
                      {
                        v101 = *(_QWORD *)v57;
                        if ( *(_QWORD *)v57 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v101 - 4)) == 0 )
                          sub_1412EC9A0(a1: v101 - 4);
                        v57 += 8;
                      }
                      while ( v57 != v100 );
                      v99 = v134;
                    }
                    sub_1407E4890(a1: qword_141ABD470);
                  }
                  v99[10] = v62;
                  v99[11] = v62 + 8 * v116;
                  v99[12] = v62 + 8 * v61;
                  v8 = v120;
LABEL_220:
                  v102 = v127;
                  if ( v127 != nullptr && _InterlockedDecrement(v127 - 1) == 0 )
                    sub_1412EC9A0(a1: v102 - 1);
                  v103 = v125;
                  if ( v125 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v125 - 4)) == 0 )
                    sub_1412EC9A0(a1: v103 - 4);
                  v104 = (void (__fastcall ***)(_QWORD, __int64))v130;
                  if ( v130 != nullptr && _InterlockedDecrement(v130 + 2) == 0 )
                    (**v104)(a1: v104, a2: 1);
                  v105 = v131;
                  if ( v131 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v131 - 4)) == 0 )
                    sub_1412EC9A0(a1: v105 - 4);
                  v35 = 0;
                  if ( _InterlockedDecrement(v18 + 2) != 0 )
                    goto LABEL_71;
                  goto LABEL_70;
                }
                if ( v62 < (unsigned __int64)&v66[(v68 & 0xFFFFFFFFFFFFFFF8uLL) + 8]
                  && (unsigned __int64)v66 < v62 + (v68 & 0xFFFFFFFFFFFFFFF8uLL) + 8 )
                {
                  v69 = (_QWORD *)v62;
                  goto LABEL_185;
                }
                v72 = (v68 >> 3) + 1;
                v73 = v72 & 0x3FFFFFFFFFFFFFFCLL;
                v74 = (((v72 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
                if ( (v72 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
                {
                  v76 = 0;
                  if ( (v74 & 1) != 0 )
                    goto LABEL_182;
                }
                else
                {
                  v75 = v74 & 0xFFFFFFFFFFFFFFFEuLL;
                  v76 = 0;
                  do
                  {
                    v77 = *(_OWORD *)&v66[8 * v76 + 16];
                    *(_OWORD *)(v62 + 8 * v76) = *(_OWORD *)&v66[8 * v76];
                    *(_OWORD *)(v62 + 8 * v76 + 16) = v77;
                    *(_OWORD *)&v66[8 * v76] = 0;
                    *(_OWORD *)&v66[8 * v76 + 16] = 0;
                    v78 = *(_OWORD *)&v66[8 * v76 + 48];
                    *(_OWORD *)(v62 + 8 * v76 + 32) = *(_OWORD *)&v66[8 * v76 + 32];
                    *(_OWORD *)(v62 + 8 * v76 + 48) = v78;
                    *(_OWORD *)&v66[8 * v76 + 32] = 0;
                    *(_OWORD *)&v66[8 * v76 + 48] = 0;
                    v76 += 8;
                    v75 -= 2LL;
                  }
                  while ( v75 != 0 );
                  if ( (v74 & 1) != 0 )
                  {
LABEL_182:
                    v79 = *(_OWORD *)&v66[8 * v76 + 16];
                    *(_OWORD *)(v62 + 8 * v76) = *(_OWORD *)&v66[8 * v76];
                    *(_OWORD *)(v62 + 8 * v76 + 16) = v79;
                    *(_OWORD *)&v66[8 * v76] = 0;
                    *(_OWORD *)&v66[8 * v76 + 16] = 0;
                  }
                }
                if ( v72 != v73 )
                {
                  v66 += 8 * v73;
                  v69 = (_QWORD *)(v62 + 8 * v73);
                  goto LABEL_185;
                }
                goto LABEL_186;
              }
              if ( v66 == v57 )
                goto LABEL_210;
              v70 = v57 - v66 - 8;
              if ( v70 < 0x88 )
              {
                v71 = (_QWORD *)v62;
                goto LABEL_208;
              }
              if ( v62 < (unsigned __int64)&v66[(v70 & 0xFFFFFFFFFFFFFFF8uLL) + 8]
                && (unsigned __int64)v66 < v62 + (v70 & 0xFFFFFFFFFFFFFFF8uLL) + 8 )
              {
                v71 = (_QWORD *)v62;
                do
                {
LABEL_208:
                  *v71 = *(_QWORD *)v66;
                  *(_QWORD *)v66 = 0;
                  ++v71;
                  v66 += 8;
                }
                while ( v66 != v57 );
                goto LABEL_209;
              }
              v91 = (v70 >> 3) + 1;
              v92 = v91 & 0x3FFFFFFFFFFFFFFCLL;
              v93 = (((v91 & 0x3FFFFFFFFFFFFFFCuLL) - 4) >> 2) + 1;
              if ( (v91 & 0x3FFFFFFFFFFFFFFCLL) == 4 )
              {
                v95 = 0;
                if ( (v93 & 1) != 0 )
                  goto LABEL_205;
              }
              else
              {
                v94 = v93 & 0xFFFFFFFFFFFFFFFEuLL;
                v95 = 0;
                do
                {
                  v96 = *(_OWORD *)&v66[8 * v95 + 16];
                  *(_OWORD *)(v62 + 8 * v95) = *(_OWORD *)&v66[8 * v95];
                  *(_OWORD *)(v62 + 8 * v95 + 16) = v96;
                  *(_OWORD *)&v66[8 * v95] = 0;
                  *(_OWORD *)&v66[8 * v95 + 16] = 0;
                  v97 = *(_OWORD *)&v66[8 * v95 + 48];
                  *(_OWORD *)(v62 + 8 * v95 + 32) = *(_OWORD *)&v66[8 * v95 + 32];
                  *(_OWORD *)(v62 + 8 * v95 + 48) = v97;
                  *(_OWORD *)&v66[8 * v95 + 32] = 0;
                  *(_OWORD *)&v66[8 * v95 + 48] = 0;
                  v95 += 8;
                  v94 -= 2LL;
                }
                while ( v94 != 0 );
                if ( (v93 & 1) != 0 )
                {
LABEL_205:
                  v98 = *(_OWORD *)&v66[8 * v95 + 16];
                  *(_OWORD *)(v62 + 8 * v95) = *(_OWORD *)&v66[8 * v95];
                  *(_OWORD *)(v62 + 8 * v95 + 16) = v98;
                  *(_OWORD *)&v66[8 * v95] = 0;
                  *(_OWORD *)&v66[8 * v95 + 16] = 0;
                }
              }
              if ( v91 == v92 )
                goto LABEL_209;
              v66 += 8 * v92;
              v71 = (_QWORD *)(v62 + 8 * v92);
              goto LABEL_208;
            }
          }
          v34 = v131;
          if ( v131 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v131 - 4)) == 0 )
            sub_1412EC9A0(a1: v34 - 4);
          v35 = 1;
          if ( _InterlockedDecrement(v18 + 2) == 0 )
LABEL_70:
            (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v18)(a1: v18, a2: 1);
LABEL_71:
          if ( v35 == 0 )
            goto LABEL_240;
          v15 = v129;
LABEL_30:
          ++v17;
          v16 = *((_QWORD *)v15 + 1);
          if ( v17 >= (*((_QWORD *)v15 + 2) - v16) >> 3 )
            goto LABEL_240;
        }
      }
    }
LABEL_243:
    v107 = v132;
    if ( v132 != nullptr && _InterlockedDecrement(v132 + 2) == 0 )
      result = (**(__int64 (__fastcall ***)(volatile signed __int32 *, __int64))v107)(a1: v107, a2: 1);
  }
  v108 = v129;
  if ( v129 != nullptr && _InterlockedDecrement(v129) == 0 )
  {
    sub_1400532D0(a1: v108);
    result = sub_141750CFC(a1: v108);
  }
  v109 = v119;
  if ( v119 != 0 )
  {
    result = (unsigned int)_InterlockedDecrement((volatile signed __int32 *)(v119 + 8));
    if ( (_DWORD)result == 1 && *(_BYTE *)(v109 + 12) != 0 )
    {
      result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v109 + 16LL))(a1: v109);
      if ( (_BYTE)result != 0 )
      {
        v110 = *(_QWORD *)(v109 + 24);
        if ( v110 == 0
          || (_BYTE)(result = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v110 + 24LL))(a1: v110, a2: v109)) != 0 )
        {
          result = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v109 + 24LL))(a1: v109);
          v111 = *(_QWORD *)(v109 + 24);
          if ( v111 != 0 )
            return (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)v111 + 16LL))(a1: v111, a2: v109);
        }
      }
    }
    else if ( (_DWORD)result == 0 )
    {
      return (**(__int64 (__fastcall ***)(__int64, __int64))v109)(a1: v109, a2: 1);
    }
  }
  return result;
}
