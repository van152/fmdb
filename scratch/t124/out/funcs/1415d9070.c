__int64 __fastcall sub_1415D9070(char *a1, __int64 a2, __int64 *a3, __int64 a4)
{
  __int64 *v4; // rbx
  int v6; // eax
  char *v7; // rdi
  char v8; // bl
  __int64 v9; // rax
  unsigned __int64 v10; // rax
  __int64 v11; // rcx
  __int64 v12; // rdx
  __int64 v13; // r8
  __int64 v14; // r9
  int v15; // edi
  unsigned __int64 v16; // rax
  __int64 v17; // rcx
  __int64 v18; // rdx
  __int64 v19; // r8
  __int64 v20; // r9
  __int64 v21; // r15
  int v22; // r14d
  __int64 v23; // rbx
  __int64 v24; // rcx
  __int64 v25; // rdx
  __int64 v26; // rcx
  __int64 v27; // r8
  __int64 v28; // r9
  __int64 v29; // rax
  __int64 v30; // rcx
  __int64 v31; // rax
  unsigned __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rdx
  __int64 v35; // r8
  __int64 v36; // r9
  __int64 v37; // rcx
  __int64 v38; // rcx
  void (__fastcall ***v39)(_QWORD, __int64); // rcx
  char v40; // bl
  unsigned __int64 v41; // rax
  __int64 v42; // rcx
  __int64 v43; // rdx
  __int64 v44; // r8
  __int64 v45; // r9
  char v46; // bl
  unsigned __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rdx
  __int64 v50; // r8
  __int64 v51; // r9
  char *v52; // rcx
  __int64 v53; // rax
  __int64 v54; // rdx
  char *v55; // rcx
  __int64 v56; // r8
  __int64 v57; // r9
  __int64 v58; // rbx
  __int64 v59; // rax
  unsigned __int64 v60; // rbx
  int v61; // ebx
  char v62; // di
  int v63; // edi
  unsigned __int64 v64; // rax
  __int64 v65; // rcx
  __int64 v66; // rdx
  __int64 v67; // r8
  __int64 v68; // r9
  char v69; // bl
  unsigned __int64 v70; // rax
  __int64 v71; // rcx
  __int64 v72; // rdx
  __int64 v73; // r8
  __int64 v74; // r9
  __int64 v75; // rcx
  int v76; // eax
  int v77; // ecx
  _DWORD *v78; // rdi
  int v79; // esi
  int v80; // edi
  int v81; // eax
  int v82; // esi
  bool v83; // zf
  int v84; // eax
  __int64 v85; // rax
  int v86; // edi
  unsigned __int64 v87; // rax
  __int64 v88; // rcx
  __int64 v89; // rdx
  __int64 v90; // r8
  __int64 v91; // r9
  __int64 v92; // rdx
  __int64 v93; // rcx
  __int64 v94; // r8
  __int64 v95; // r9
  __int64 v96; // rdx
  __int64 v97; // rcx
  __int64 v98; // r8
  __int64 v99; // r9
  int v100; // esi
  int v101; // edi
  int v102; // eax
  int v103; // esi
  int v104; // eax
  __int64 v105; // rcx
  __int64 v106; // rax
  __int64 v107; // rcx
  __int64 v108; // rdx
  __int64 v109; // r8
  __int64 v110; // r9
  char v111; // bl
  unsigned __int64 v112; // rax
  __int64 v113; // rcx
  __int64 v114; // rdx
  __int64 v115; // r8
  __int64 v116; // r9
  char v117; // bl
  unsigned __int64 v118; // rax
  __int64 v119; // rcx
  __int64 v120; // rdx
  __int64 v121; // r8
  __int64 v122; // r9
  __int64 v123; // rax
  int v124; // esi
  __int64 v125; // rax
  unsigned __int64 v126; // rax
  __int64 v127; // rcx
  __int64 v128; // rdx
  __int64 v129; // r8
  __int64 v130; // r9
  int v131; // edi
  unsigned __int64 v132; // rax
  __int64 v133; // rcx
  __int64 v134; // rdx
  __int64 v135; // r8
  __int64 v136; // r9
  unsigned __int64 v138; // rax
  __int64 v139; // rcx
  __int64 v140; // rdx
  __int64 v141; // r8
  __int64 v142; // r9
  __int64 v143; // rcx
  __int64 v144; // rax
  __int64 v145; // rcx
  __int64 v146; // rdx
  __int64 v147; // r8
  __int64 v148; // r9
  _QWORD v149[2]; // [rsp+30h] [rbp-50h] BYREF
  __int64 v150; // [rsp+40h] [rbp-40h] BYREF
  __int64 v151; // [rsp+48h] [rbp-38h] BYREF
  _QWORD v152[2]; // [rsp+50h] [rbp-30h] BYREF
  unsigned __int64 v153; // [rsp+60h] [rbp-20h] BYREF
  _QWORD v154[9]; // [rsp+68h] [rbp-18h] BYREF

  v154[2] = -2;
  v6 = -*((_DWORD *)a1 - 1);
  v7 = &a1[v6];
  if ( (int)a2 <= 1248029043 )
  {
    if ( (int)a2 <= 1248027501 )
    {
      if ( (int)a2 > 1246589794 )
      {
        if ( (_DWORD)a2 == 1246589795 )
        {
          v123 = *((_QWORD *)v7 - 3);
          LOBYTE(v4) = 1;
          if ( v123 != 0 )
          {
            v124 = *(char *)(v123 + 241);
            v125 = sub_14083D4F0(a1, a2, a3, a4) + 40;
            LODWORD(v154[0]) = v124;
            v153 = v125;
            if ( &v153 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
              v126 = v153;
              v127 = v154[0];
              a3[1] = v154[0];
              *a3 = v126;
              v125 = sub_14083D4F0(a1: v127, a2: v128, a3: v129, a4: v130) + 8;
              v154[0] = 0;
              v153 = v125;
            }
            (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v125 + 16LL))(a1: v125, a2: &v153);
          }
          return (unsigned int)v4;
        }
        if ( (_DWORD)a2 == 1246913900 )
        {
          v53 = sub_140FE35F0();
          if ( v53 != 0 )
          {
            v54 = *((_QWORD *)v7 - 6);
            if ( v54 != 0 )
            {
              v55 = *(char **)v54;
              v58 = *(_QWORD *)(v54 + 8) - *(_QWORD *)v54;
              if ( v58 != 0 )
              {
                v59 = v53 + 1104;
                v60 = v58 >> 4;
                v54 = 1;
                if ( v60 >= 2 )
                  v54 = v60;
                v55 += 12;
                do
                {
                  if ( *(_QWORD *)(v55 - 12) == v59 )
                  {
                    v61 = (unsigned __int8)*(v55 - 1);
                    if ( v61 == 2 )
                    {
                      v62 = -*v55;
                      goto LABEL_110;
                    }
                    if ( v61 == 1 )
                    {
                      v62 = *v55;
                      goto LABEL_110;
                    }
                  }
                  v55 += 16;
                  --v54;
                }
                while ( v54 != 0 );
              }
            }
          }
          v62 = 0;
LABEL_110:
          v9 = sub_14083D4F0(a1: v55, a2: v54, a3: v56, a4: v57) + 40;
          LODWORD(v154[0]) = v62;
          v153 = v9;
          if ( &v153 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v138 = v153;
            v139 = v154[0];
            a3[1] = v154[0];
            *a3 = v138;
            v9 = sub_14083D4F0(a1: v139, a2: v140, a3: v141, a4: v142) + 8;
            v154[0] = 0;
            v153 = v9;
          }
          goto LABEL_112;
        }
      }
      else
      {
        if ( (_DWORD)a2 == 1245931617 )
        {
          sub_1407C9510(a1: &v153);
          LODWORD(v152[0]) = *(v7 - 15);
          v151 = sub_14083D4F0(a1: v93, a2: v92, a3: v94, a4: v95) + 40;
          sub_140833EB0(a1: &v153, a2: 1245931617, a3: &v151);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v151 + 16LL))(a1: v151, a2: &v151);
          v149[1] = 0;
          v149[0] = sub_14083D4F0(a1: v97, a2: v96, a3: v98, a4: v99) + 8;
          v100 = *((_DWORD *)v7 + 2);
          v101 = (*(__int64 (__fastcall **)(char *))(*(_QWORD *)v7 + 56LL))(a1: v7);
          (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)v149[0] + 24LL))(
            a1: v149[0],
            a2: v149,
            a3: v152);
          v102 = v100 & v101;
          v103 = (v101 << 24) | v100 & 0x7FFFFF;
          v83 = v102 == -1;
          v104 = -8388609;
          if ( !v83 )
            v104 = v103;
          LODWORD(v151) = v104;
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v149[0] + 16LL))(a1: v149[0], a2: v149);
          v4 = &v151;
          sub_140FEAD00(a1: &v151, a2: v149);
          sub_140833EB0(a1: &v153, a2: 1248490094, a3: v149);
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v149[0] + 16LL))(a1: v149[0], a2: v149);
          (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v152[0] + 16LL))(a1: v152[0], a2: v152);
          sub_14083DDA0(a1: &v151, a2: &v153);
          v105 = *a3;
          if ( &v151 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v105 + 16LL))(a1: v105, a2: a3);
            v106 = v151;
            v107 = v152[0];
            a3[1] = v152[0];
            *a3 = v106;
            v105 = sub_14083D4F0(a1: v107, a2: v108, a3: v109, a4: v110) + 8;
            v152[0] = 0;
            v151 = v105;
          }
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v105 + 16LL))(a1: v105, a2: &v151);
          sub_140833970(a1: &v153);
          goto LABEL_119;
        }
        if ( (_DWORD)a2 == 1246585197 )
        {
          v21 = *((_QWORD *)v7 - 3);
          if ( v21 != 0 )
          {
            (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v21 + 200LL))(a1: *((_QWORD *)v7 - 3), a2: v149);
            v22 = v149[0];
            v150 = 0;
            v23 = sub_1412EC810(a1: 264, a2: 5);
            *(_QWORD *)v23 = 0x500000000LL;
            *(_BYTE *)(v23 + 12) = MEMORY[0x1418DD4F8];
            *(_DWORD *)(v23 + 8) = MEMORY[0x1418DD4F4];
            *(_BYTE *)(v23 + 13) = 0;
            if ( v150 != 0 )
            {
              v24 = v150 - 4;
              if ( _InterlockedDecrement((volatile signed __int32 *)(v150 - 4)) == 0 )
                sub_1412EC9A0(a1: v24);
            }
            v150 = 0;
            _InterlockedIncrement((volatile signed __int32 *)v23);
            v150 = v23 + 4;
            sub_14081AF20(a1: v22, a2: (unsigned int)&v151, a3: (unsigned int)&v150, a4: 0, a5: 0, a6: 0);
            v29 = sub_14083D4F0(a1: v26, a2: v25, a3: v27, a4: v28);
            v154[0] = 0;
            v30 = v151;
            if ( v151 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v151 - 4));
            v154[0] = v30;
            v31 = v29 + 136;
            v153 = v31;
            if ( &v153 != (unsigned __int64 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
              v32 = v153;
              v33 = v154[0];
              a3[1] = v154[0];
              *a3 = v32;
              v31 = sub_14083D4F0(a1: v33, a2: v34, a3: v35, a4: v36) + 8;
              v154[0] = 0;
              v153 = v31;
            }
            v4 = *(__int64 **)v31;
            (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v31 + 16LL))(a1: v31, a2: &v153);
            v37 = v151;
            if ( v151 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v151 - 4)) == 0 )
              sub_1412EC9A0(a1: v37 - 4);
            v38 = v150;
            if ( v150 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v150 - 4)) == 0 )
              sub_1412EC9A0(a1: v38 - 4);
            v39 = (void (__fastcall ***)(_QWORD, __int64))v149[0];
            if ( v149[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v149[0] + 8LL)) == 0 )
              (**v39)(a1: v39, a2: 1);
          }
          LOBYTE(v4) = v21 != 0;
          return (unsigned int)v4;
        }
      }
    }
    else if ( (int)a2 <= 1248027755 )
    {
      if ( (_DWORD)a2 == 1248027502 )
      {
        v117 = *(v7 - 15);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 24;
        LOBYTE(v154[0]) = (v117 & 4) != 0;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v118 = v153;
          v119 = v154[0];
          a3[1] = v154[0];
          *a3 = v118;
          v9 = sub_14083D4F0(a1: v119, a2: v120, a3: v121, a4: v122) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      }
      if ( (_DWORD)a2 == 1248027752 )
      {
        v46 = *(v7 - 15);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 24;
        LOBYTE(v154[0]) = (v46 & 0x10) != 0;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v47 = v153;
          v48 = v154[0];
          a3[1] = v154[0];
          *a3 = v47;
          v9 = sub_14083D4F0(a1: v48, a2: v49, a3: v50, a4: v51) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      }
    }
    else
    {
      switch ( (_DWORD)a2 )
      {
        case 0x4A63646C:
          v69 = *(v7 - 15);
          v9 = sub_14083D4F0(a1, a2, a3, a4) + 24;
          LOBYTE(v154[0]) = (v69 & 0x40) != 0;
          v153 = v9;
          if ( &v153 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v70 = v153;
            v71 = v154[0];
            a3[1] = v154[0];
            *a3 = v70;
            v9 = sub_14083D4F0(a1: v71, a2: v72, a3: v73, a4: v74) + 8;
            v154[0] = 0;
            v153 = v9;
          }
          goto LABEL_112;
        case 0x4A63656D:
          v75 = *((_QWORD *)v7 - 3);
          if ( v75 != 0 )
          {
            v76 = *(_DWORD *)(v75 + 12);
            v77 = *(_DWORD *)(v75 + 16);
            if ( v77 == 0 )
              v77 = v76;
          }
          else
          {
            v76 = -1;
            v77 = -1;
          }
          v153 = __PAIR64__(v77, v76);
          sub_140FE72B0(a1: &v153, a2: 1298490451, a3);
          goto LABEL_119;
        case 0x4A636578:
          v8 = *(v7 - 15);
          v9 = sub_14083D4F0(a1, a2, a3, a4) + 24;
          LOBYTE(v154[0]) = (v8 & 2) != 0;
          v153 = v9;
          if ( &v153 != (unsigned __int64 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
            v10 = v153;
            v11 = v154[0];
            a3[1] = v154[0];
            *a3 = v10;
            v9 = sub_14083D4F0(a1: v11, a2: v12, a3: v13, a4: v14) + 8;
            v154[0] = 0;
            v153 = v9;
          }
LABEL_112:
          v4 = *(__int64 **)v9;
          (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v9 + 16LL))(a1: v9, a2: &v153);
          goto LABEL_119;
        default:
          break;
      }
    }
    return sub_140DFD340(a1: v7 - 16, a2, a3);
  }
  if ( (int)a2 <= 1248488818 )
  {
    if ( (int)a2 > 1248032113 )
    {
      if ( (_DWORD)a2 == 1248032114 )
      {
        v131 = *(v7 - 13);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 40;
        LODWORD(v154[0]) = v131;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v132 = v153;
          v133 = v154[0];
          a3[1] = v154[0];
          *a3 = v132;
          v9 = sub_14083D4F0(a1: v133, a2: v134, a3: v135, a4: v136) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      }
      if ( (_DWORD)a2 == 1248358254 )
      {
        v63 = *(v7 - 14);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 40;
        LODWORD(v154[0]) = v63;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v64 = v153;
          v65 = v154[0];
          a3[1] = v154[0];
          *a3 = v64;
          v9 = sub_14083D4F0(a1: v65, a2: v66, a3: v67, a4: v68) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      }
    }
    else
    {
      if ( (_DWORD)a2 == 1248029044 )
      {
        v111 = *(v7 - 15);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 24;
        LOBYTE(v154[0]) = (v111 & 0x20) != 0;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v112 = v153;
          v113 = v154[0];
          a3[1] = v154[0];
          *a3 = v112;
          v9 = sub_14083D4F0(a1: v113, a2: v114, a3: v115, a4: v116) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      }
      if ( (_DWORD)a2 == 1248030307 )
      {
        v40 = *(v7 - 15);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 24;
        LOBYTE(v154[0]) = (v40 & 8) != 0;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v41 = v153;
          v42 = v154[0];
          a3[1] = v154[0];
          *a3 = v41;
          v9 = sub_14083D4F0(a1: v42, a2: v43, a3: v44, a4: v45) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      }
    }
    return sub_140DFD340(a1: v7 - 16, a2, a3);
  }
  if ( (int)a2 > 1248686961 )
  {
    switch ( (_DWORD)a2 )
    {
      case 0x4A6D7372:
        v78 = *((_DWORD **)v7 - 3);
        if ( v78 != nullptr )
        {
          v4 = (__int64 *)(sub_14083D4F0(a1, a2, a3, a4) + 8);
          v152[0] = 0;
          v151 = (__int64)v4;
          v79 = v78[2];
          v80 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v78 + 56LL))(a1: v78);
          (*(void (__fastcall **)(__int64 *, __int64 *, _QWORD *))(*v4 + 24))(a1: v4, a2: &v151, a3: v154);
          v81 = v79 & v80;
          v82 = (v80 << 24) | v79 & 0x7FFFFF;
          v83 = v81 == -1;
          v84 = -8388609;
          if ( !v83 )
            v84 = v82;
          LODWORD(v153) = v84;
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v151 + 16LL))(a1: v151, a2: &v151);
        }
        else
        {
          LODWORD(v153) = dword_141B60CC0;
          (*(void (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)qword_141B60CC8 + 24LL))(
            a1: qword_141B60CC8,
            a2: &qword_141B60CC8,
            a3: v154);
        }
        sub_140FEAD00(a1: &v153, a2: &v151);
        v143 = *a3;
        if ( &v151 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v143 + 16LL))(a1: v143, a2: a3);
          v144 = v151;
          v145 = v152[0];
          a3[1] = v152[0];
          *a3 = v144;
          v143 = sub_14083D4F0(a1: v145, a2: v146, a3: v147, a4: v148) + 8;
          v152[0] = 0;
          v151 = v143;
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v143 + 16LL))(a1: v143, a2: &v151);
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v154[0] + 16LL))(a1: v154[0], a2: v154);
        goto LABEL_119;
      case 0x4A6D7374:
        v85 = *((_QWORD *)v7 - 3);
        v86 = 1;
        if ( v85 != 0 )
        {
          a1 = *(char **)(v85 + 48);
          if ( *(char **)(v85 + 56) != a1 )
            v86 = *a1;
        }
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 40;
        LODWORD(v154[0]) = v86;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v87 = v153;
          v88 = v154[0];
          a3[1] = v154[0];
          *a3 = v87;
          v9 = sub_14083D4F0(a1: v88, a2: v89, a3: v90, a4: v91) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      case 0x4A736F77:
        v15 = *(v7 - 16);
        v9 = sub_14083D4F0(a1, a2, a3, a4) + 40;
        LODWORD(v154[0]) = v15;
        v153 = v9;
        if ( &v153 != (unsigned __int64 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(a1: *a3, a2: a3);
          v16 = v153;
          v17 = v154[0];
          a3[1] = v154[0];
          *a3 = v16;
          v9 = sub_14083D4F0(a1: v17, a2: v18, a3: v19, a4: v20) + 8;
          v154[0] = 0;
          v153 = v9;
        }
        goto LABEL_112;
      default:
        break;
    }
    return sub_140DFD340(a1: v7 - 16, a2, a3);
  }
  if ( (_DWORD)a2 == 1248488819 )
  {
    v52 = *((char **)v7 - 3);
  }
  else
  {
    if ( (_DWORD)a2 != 1248490094 )
      return sub_140DFD340(a1: v7 - 16, a2, a3);
    v52 = &a1[v6];
  }
  sub_140F10C50(a1: v52, a2: a3);
LABEL_119:
  LOBYTE(v4) = 1;
  return (unsigned int)v4;
}
