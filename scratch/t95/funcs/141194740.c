__int64 __fastcall sub_141194740(__int64 a1, int a2, unsigned int *a3)
{
  __int64 *v6; // rbx
  unsigned __int64 v7; // rax
  __int64 v8; // rcx
  char v9; // al
  unsigned __int64 v10; // rax
  __int64 v11; // rcx
  __int64 v12; // rax
  unsigned __int64 v13; // rax
  unsigned __int64 v14; // rax
  __int64 v15; // rcx
  unsigned int v16; // eax
  int v17; // ecx
  char v18; // al
  unsigned __int64 v19; // rax
  __int64 v20; // rcx
  unsigned int v21; // eax
  __int64 v22; // rcx
  int v23; // ecx
  __int64 v24; // rax
  __int64 v25; // r15
  unsigned int v26; // ebp
  _QWORD *v27; // r12
  __int64 *v28; // rax
  __int64 *v29; // r13
  __int64 v30; // rbx
  __int64 v31; // rcx
  __int64 v32; // rdx
  __int64 v33; // rdi
  unsigned __int64 v34; // r12
  unsigned __int64 v35; // rdx
  unsigned __int64 v36; // r12
  __int64 v37; // rax
  __int64 v38; // rdx
  __int64 v39; // rbx
  char v40; // al
  unsigned __int64 v41; // rax
  __int64 v42; // rcx
  __int64 v43; // rcx
  int v44; // eax
  int v45; // eax
  _QWORD *v46; // rsi
  _QWORD *v47; // rax
  _QWORD *v48; // rcx
  char v49; // al
  __int64 *v50; // rcx
  __int64 v51; // rbp
  __int64 v52; // rax
  __int64 v53; // rcx
  __int64 v54; // rdx
  _QWORD *v55; // r15
  __int64 v56; // rsi
  __int64 v57; // r8
  __int64 v58; // rax
  __int64 v59; // rbp
  __int64 v60; // r8
  unsigned __int64 v61; // rcx
  __int64 v62; // rdi
  __int64 v63; // rax
  unsigned __int64 v64; // rax
  __int64 v65; // r12
  __int64 v66; // rsi
  __int64 *v67; // rbp
  __int64 v68; // rax
  _QWORD *v69; // rbp
  __int64 v70; // rdi
  __int64 v71; // rdi
  __int64 v72; // r14
  __int64 *v73; // rdx
  int v74; // eax
  __int64 v75; // rcx
  __int64 v76; // rax
  int v77; // eax
  _QWORD *v78; // rcx
  __int64 *v79; // rdx
  unsigned int v80; // eax
  char v81; // al
  __int64 v82; // rcx
  unsigned __int64 v83; // rcx
  char v84; // al
  int v85; // eax
  _QWORD *v86; // rcx
  int v87; // eax
  _QWORD *v88; // rcx
  __int64 *v89; // r14
  __int64 v90; // rax
  __int64 v91; // rcx
  __int64 *v92; // rdx
  __int64 v93; // rcx
  __int64 v94; // rdx
  __int64 *v95; // rax
  _QWORD *v96; // rsi
  __int64 v97; // rdi
  __int64 v98; // r8
  __int64 v99; // rax
  __int64 v100; // rbp
  __int64 v101; // r8
  unsigned __int64 v102; // rcx
  __int64 v103; // rsi
  __int64 v104; // rax
  __int64 v105; // rcx
  int v106; // eax
  __int64 v107; // rdi
  __int64 v108; // rbp
  __int64 v109; // rcx
  __int64 *v110; // rdx
  __int64 v111; // rax
  int v112; // eax
  __int64 v113; // r8
  __int64 *v114; // rdi
  __int64 v115; // rax
  __int64 v116; // rcx
  __int64 v117; // r8
  unsigned __int64 v118; // rdx
  bool v119; // zf
  int v120; // eax
  _QWORD *v121; // rsi
  __int64 v122; // rax
  __int64 v123; // rdi
  __int64 v124; // rbp
  __int64 v125; // rbp
  __int64 v126; // rsi
  __int64 *v127; // r8
  unsigned int v128; // eax
  unsigned __int64 v129; // rcx
  __int64 v130; // rbp
  __int64 v131; // rdi
  bool v132; // al
  __int64 **v134; // [rsp+28h] [rbp-A0h] BYREF
  _QWORD **v135; // [rsp+30h] [rbp-98h] BYREF
  __int64 *v136; // [rsp+38h] [rbp-90h] BYREF
  _QWORD *v137; // [rsp+40h] [rbp-88h] BYREF
  _QWORD *v138; // [rsp+48h] [rbp-80h]
  __int64 v139; // [rsp+50h] [rbp-78h]
  unsigned int v140; // [rsp+60h] [rbp-68h]
  __int64 v141; // [rsp+68h] [rbp-60h]
  _QWORD *v142; // [rsp+70h] [rbp-58h]
  __int64 *v143; // [rsp+78h] [rbp-50h]
  unsigned __int64 v144; // [rsp+80h] [rbp-48h]

  LODWORD(v6) = 0;
  if ( a2 <= 1346792046 )
  {
    if ( a2 > 1346790251 )
    {
      if ( a2 > 1346790978 )
      {
        v13 = (unsigned int)(a2 - 1346790979);
        if ( (unsigned int)v13 <= 0x2F )
        {
          v22 = 0x80060000002BLL;
          if ( _bittest64(&v22, v13) )
            goto LABEL_114;
        }
        v14 = (unsigned int)(a2 - 1346791747);
        if ( (unsigned int)v14 <= 0x2F )
        {
          v15 = 0x840180000001LL;
          if ( _bittest64(&v15, v14) )
            goto LABEL_114;
        }
        v10 = (unsigned int)(a2 - 1346791235);
        if ( (unsigned int)v10 > 0x2B )
          return (unsigned int)v6;
        v11 = 0x80180000001LL;
        goto LABEL_62;
      }
      if ( a2 > 1346790515 )
      {
        if ( a2 == 1346790516 )
        {
          v24 = sub_140DBC940();
          sub_140DBCA60(v24, &v136, a3);
          *(_DWORD *)(a1 + 104) = (_DWORD)v136;
          goto LABEL_497;
        }
        if ( a2 != 1346790755 )
        {
          if ( a2 != 1346790756 )
            return (unsigned int)v6;
          v12 = sub_140DBC940();
          sub_140DBCA60(v12, &v136, a3);
          *(_DWORD *)(a1 + 116) = (_DWORD)v136;
          goto LABEL_497;
        }
        goto LABEL_114;
      }
      if ( a2 != 1346790252 )
      {
        if ( a2 == 1346790259 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            v18 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
          else
            v18 = 6;
          *(_BYTE *)(a1 + 128) = v18;
          goto LABEL_497;
        }
        return (unsigned int)v6;
      }
      v25 = a1 + 80;
    }
    else
    {
      if ( a2 <= 1346786117 )
      {
        if ( a2 > 1346782307 )
        {
          if ( a2 > 1346783331 )
          {
            if ( a2 != 1346783332 && a2 != 1346784327 )
              return (unsigned int)v6;
          }
          else if ( a2 != 1346782308 && a2 != 1346783058 )
          {
            return (unsigned int)v6;
          }
          goto LABEL_114;
        }
        if ( a2 <= 1346782039 )
        {
          if ( a2 == 1179935340 )
          {
            v134 = (__int64 **)(a1 + 48);
            v135 = (_QWORD **)(a1 + 48);
            v136 = (__int64 *)&v134;
            v137 = &v135;
            LODWORD(v6) = sub_141197630(&v136, a3);
            return (unsigned int)v6;
          }
          if ( a2 != 1346777409 && a2 != 1346777424 )
            return (unsigned int)v6;
          goto LABEL_114;
        }
        v16 = a2 - 1346782040;
        if ( (unsigned int)(a2 - 1346782040) > 0x15 )
          return (unsigned int)v6;
        v17 = 2101249;
        goto LABEL_94;
      }
      if ( a2 > 1346787138 )
      {
        if ( a2 > 1346789954 )
        {
          if ( a2 != 1346789955 && a2 != 1346789986 && a2 != 1346790242 )
            return (unsigned int)v6;
        }
        else if ( a2 != 1346787139 && a2 != 1346789730 && a2 != 1346789744 )
        {
          return (unsigned int)v6;
        }
        goto LABEL_114;
      }
      if ( a2 > 1346786159 )
      {
        if ( a2 != 1346786160 && a2 != 1346786375 && a2 != 1346786393 )
          return (unsigned int)v6;
        goto LABEL_114;
      }
      if ( a2 == 1346786118 )
        goto LABEL_114;
      if ( a2 != 1346786156 )
        return (unsigned int)v6;
      v25 = a1 + 88;
    }
    sub_140FE7E20(v25, a3);
    goto LABEL_497;
  }
  if ( a2 > 1346795368 )
  {
    if ( a2 <= 1347905345 )
    {
      if ( a2 <= 1347184962 )
      {
        if ( a2 > 1346795599 )
        {
          if ( a2 != 1346795600 && a2 != 1347176803 )
            return (unsigned int)v6;
        }
        else if ( a2 != 1346795369 )
        {
          if ( a2 != 1346795376 )
            return (unsigned int)v6;
          *(_BYTE *)(a1 + 131) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(
                                   *(_QWORD *)a3,
                                   a3);
          goto LABEL_497;
        }
      }
      else if ( a2 <= 1347637061 )
      {
        if ( a2 != 1347184963 && a2 != 1347185005 )
          return (unsigned int)v6;
      }
      else if ( a2 != 1347637062 && a2 != 1347637315 && a2 != 1347637328 )
      {
        return (unsigned int)v6;
      }
      goto LABEL_114;
    }
    if ( a2 <= 1348036416 )
    {
      if ( (unsigned int)(a2 - 1347905346) <= 5 )
      {
        v23 = 35;
        if ( _bittest(&v23, a2 - 1347905346) )
          goto LABEL_114;
      }
      v10 = (unsigned int)(a2 - 1347905859);
      if ( (unsigned int)v10 > 0x2A )
        return (unsigned int)v6;
      v11 = 0x40100000001LL;
      goto LABEL_62;
    }
    if ( (unsigned int)(a2 - 1348036417) < 3 )
      goto LABEL_114;
    v16 = a2 - 1348101954;
    if ( (unsigned int)(a2 - 1348101954) > 5 )
      return (unsigned int)v6;
    v17 = 35;
LABEL_94:
    if ( !_bittest(&v17, v16) )
      return (unsigned int)v6;
    goto LABEL_114;
  }
  if ( a2 > 1346793538 )
  {
    if ( a2 > 1346794082 )
    {
      if ( a2 > 1346794352 )
      {
        switch ( a2 )
        {
          case 1346794353:
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              v84 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
            else
              v84 = -1;
            *(_BYTE *)(a1 + 130) = v84;
            goto LABEL_497;
          case 1346794598:
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              *(_DWORD *)(a1 + 108) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                        *(_QWORD *)a3,
                                        a3);
            else
              *(_DWORD *)(a1 + 108) = -1;
            break;
          case 1346795361:
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              *(_DWORD *)(a1 + 112) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                        *(_QWORD *)a3,
                                        a3);
            else
              *(_DWORD *)(a1 + 112) = -1;
            break;
          default:
            return (unsigned int)v6;
        }
        goto LABEL_497;
      }
      if ( a2 == 1346794083 )
      {
        v81 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v82 = *(_QWORD *)(a1 + 96);
        if ( v81 != 0 )
          v83 = v82 | 0x8000000;
        else
          v83 = v82 & 0xFFFFFFFFF7FFFFFFuLL;
        *(_QWORD *)(a1 + 96) = v83;
        goto LABEL_497;
      }
      if ( a2 != 1346794084 && a2 != 1346794086 )
        return (unsigned int)v6;
      goto LABEL_114;
    }
    v10 = (unsigned int)(a2 - 1346793539);
    if ( (unsigned int)v10 > 0x2F )
      return (unsigned int)v6;
    v11 = 0x844100000001LL;
LABEL_62:
    if ( !_bittest64(&v11, v10) )
      return (unsigned int)v6;
    goto LABEL_114;
  }
  if ( a2 <= 1346792770 )
  {
    v19 = (unsigned int)(a2 - 1346792515);
    if ( (unsigned int)v19 > 0x2A || (v20 = 0x40100000001LL, !_bittest64(&v20, v19)) )
    {
      if ( a2 != 1346792047 )
        return (unsigned int)v6;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
      {
        v21 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(*(_QWORD *)a3, a3);
        *(_WORD *)(a1 + 124) = v21;
        *(_BYTE *)(a1 + 127) = sub_1415C69A0(v21, 0);
      }
      else
      {
        *(_WORD *)(a1 + 124) = 0;
        *(_BYTE *)(a1 + 127) = 0;
      }
      goto LABEL_497;
    }
  }
  else
  {
    v7 = (unsigned int)(a2 - 1346792771);
    if ( (unsigned int)v7 <= 0x30 )
    {
      v8 = 0x46100000001LL;
      if ( _bittest64(&v8, v7) )
        goto LABEL_114;
      if ( v7 == 48 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          v9 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
        else
          v9 = -1;
        *(_BYTE *)(a1 + 129) = v9;
        goto LABEL_497;
      }
    }
    if ( a2 != 1346793075 )
      return (unsigned int)v6;
  }
LABEL_114:
  v26 = sub_141193FB0((unsigned int)a2);
  v27 = (_QWORD *)(a1 + 24);
  v28 = *(__int64 **)(a1 + 24);
  v29 = *(__int64 **)(a1 + 32);
  v30 = (char *)v29 - (char *)v28;
  if ( v29 == v28 )
  {
LABEL_120:
    v33 = 0;
    if ( a2 <= 1346793538 )
    {
      if ( a2 <= 1346791746 )
      {
        if ( a2 == 1346789955 || a2 == 1346791235 )
          goto LABEL_148;
      }
      else if ( a2 == 1346791747 || a2 == 1346792515 || a2 == 1346792771 )
      {
        goto LABEL_148;
      }
    }
    else if ( a2 > 1347905858 )
    {
      if ( a2 == 1347905859 || a2 == 1348036418 || a2 == 1348101954 )
        goto LABEL_148;
    }
    else if ( a2 == 1346793539 || a2 == 1347184963 || a2 == 1347905346 )
    {
      goto LABEL_148;
    }
    v33 = sub_141750CC0(48);
    *(_QWORD *)v33 = 0;
    *(_DWORD *)(v33 + 8) = v26;
    *(_QWORD *)(v33 + 12) = 0xFFFFFFFF00000000uLL;
    *(_QWORD *)(v33 + 20) = 0;
    *(_DWORD *)(v33 + 28) = -1;
    *(_QWORD *)(v33 + 32) = 0x76C0001076C0001LL;
    *(_WORD *)(v33 + 40) = 511;
    if ( v29 == *(__int64 **)(a1 + 40) )
    {
      v142 = (_QWORD *)(a1 + 24);
      v34 = (unsigned __int64)(v30 >> 3) >> 1;
      v35 = 0x1FFFFFFFFFFFFFFFLL - v34;
      v36 = (v30 >> 3) + v34;
      v144 = (v30 >> 3) + 1;
      if ( v36 <= v144 )
        v36 = (v30 >> 3) + 1;
      if ( v30 >> 3 > v35 )
        v36 = 0x1FFFFFFFFFFFFFFFLL;
      v37 = sub_1407E4490(qword_141ABD470, 8 * v36);
      *(_QWORD *)(v37 + v30) = v33;
      v38 = *(_QWORD *)(a1 + 24);
      v143 = *(__int64 **)(a1 + 32);
      v141 = v37;
      sub_141758A00(v37, v38, (char *)v29 - v38);
      if ( v143 != v29 )
        sub_141758A00(v141 + v30 + 8, v29, *(_QWORD *)(a1 + 32) - (_QWORD)v29);
      v39 = v141;
      if ( *v142 != 0 )
        sub_1407E4890(qword_141ABD470, *v142, *(_QWORD *)(a1 + 40) - *v142);
      *(_QWORD *)(a1 + 24) = v141;
      *(_QWORD *)(a1 + 32) = v39 + 8 * v144;
      *(_QWORD *)(a1 + 40) = v39 + 8 * v36;
      v27 = v142;
    }
    else
    {
      *v29 = v33;
      *(_QWORD *)(a1 + 32) += 8LL;
    }
  }
  else
  {
    v31 = 1;
    if ( (unsigned __int64)(v30 >> 3) >= 2 )
      v31 = v30 >> 3;
    v32 = 0;
    while ( 1 )
    {
      v33 = v28[v32];
      if ( *(_DWORD *)(v33 + 8) == v26 )
        break;
      if ( v31 == ++v32 )
        goto LABEL_120;
    }
  }
LABEL_148:
  LODWORD(v6) = 0;
  if ( a2 > 1346792514 )
  {
    if ( a2 <= 1347176802 )
    {
      if ( a2 <= 1346793538 )
      {
        if ( a2 > 1346792770 )
        {
          switch ( a2 )
          {
            case 1346792771:
              goto LABEL_247;
            case 1346792772:
            case 1346792773:
            case 1346792774:
            case 1346792775:
            case 1346792776:
            case 1346792777:
            case 1346792778:
            case 1346792779:
            case 1346792780:
            case 1346792781:
            case 1346792782:
            case 1346792783:
            case 1346792784:
            case 1346792785:
            case 1346792786:
            case 1346792787:
            case 1346792788:
            case 1346792789:
            case 1346792790:
            case 1346792791:
            case 1346792792:
            case 1346792793:
            case 1346792794:
            case 1346792795:
            case 1346792796:
            case 1346792797:
            case 1346792798:
            case 1346792799:
            case 1346792800:
            case 1346792801:
            case 1346792802:
            case 1346792804:
            case 1346792805:
            case 1346792806:
            case 1346792807:
            case 1346792810:
            case 1346792811:
            case 1346792812:
              return (unsigned int)v6;
            case 1346792803:
              goto LABEL_240;
            case 1346792808:
              goto LABEL_235;
            case 1346792809:
              if ( v33 == 0 )
                goto LABEL_388;
              v40 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
              *(_BYTE *)(v33 + 41) = v40;
              LOBYTE(v6) = 1;
              if ( v40 <= 0 )
                goto LABEL_237;
              return (unsigned int)v6;
            case 1346792813:
              goto LABEL_381;
            default:
              if ( a2 == 1346793075 )
                goto LABEL_362;
              return (unsigned int)v6;
          }
        }
        if ( a2 == 1346792515 )
          goto LABEL_247;
        if ( a2 != 1346792547 )
        {
          if ( a2 != 1346792557 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
        goto LABEL_240;
      }
      if ( a2 <= 1346794083 )
      {
        switch ( a2 )
        {
          case 1346793539:
            goto LABEL_247;
          case 1346793571:
            goto LABEL_240;
          case 1346793577:
            goto LABEL_362;
          case 1346793581:
            goto LABEL_381;
          case 1346793586:
            goto LABEL_228;
          default:
            return (unsigned int)v6;
        }
      }
      if ( a2 > 1346795368 )
      {
        if ( a2 != 1346795369 )
        {
          if ( a2 != 1346795600 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
        goto LABEL_362;
      }
      if ( a2 == 1346794084 )
        goto LABEL_362;
      if ( a2 != 1346794086 )
        return (unsigned int)v6;
      goto LABEL_228;
    }
    if ( a2 > 1347905858 )
    {
      if ( a2 <= 1348036417 )
      {
        if ( a2 > 1347905900 )
        {
          if ( a2 != 1347905901 && a2 != 1348036417 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
        if ( a2 != 1347905859 )
        {
          if ( a2 != 1347905891 )
            return (unsigned int)v6;
          goto LABEL_240;
        }
        goto LABEL_247;
      }
      if ( a2 <= 1348101953 )
      {
        if ( a2 == 1348036418 )
          goto LABEL_247;
        if ( a2 != 1348036419 )
          return (unsigned int)v6;
      }
      else
      {
        if ( a2 == 1348101954 )
          goto LABEL_247;
        if ( a2 != 1348101955 )
        {
          if ( a2 != 1348101959 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
      }
    }
    else
    {
      if ( a2 <= 1347637314 )
      {
        if ( a2 > 1347185004 )
        {
          if ( a2 != 1347185005 && a2 != 1347637062 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
        if ( a2 != 1347176803 )
        {
          if ( a2 != 1347184963 )
            return (unsigned int)v6;
          goto LABEL_247;
        }
        goto LABEL_240;
      }
      if ( a2 <= 1347905345 )
      {
        if ( a2 != 1347637315 )
        {
          if ( a2 != 1347637328 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
LABEL_228:
        if ( v33 == 0 )
          goto LABEL_388;
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
        {
          v44 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
          *(_DWORD *)(v33 + 24) = v44;
          LOBYTE(v6) = 1;
          if ( v44 >= 0 )
            return (unsigned int)v6;
        }
        else
        {
          *(_DWORD *)(v33 + 24) = -1;
        }
        sub_1411946C0(v27, v33);
LABEL_497:
        LOBYTE(v6) = 1;
        return (unsigned int)v6;
      }
      if ( a2 == 1347905346 )
        goto LABEL_247;
      if ( a2 != 1347905347 )
      {
        if ( a2 != 1347905351 )
          return (unsigned int)v6;
        goto LABEL_381;
      }
    }
LABEL_240:
    if ( v33 != 0 )
    {
      v45 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
      *(_DWORD *)(v33 + 24) = v45;
      LOBYTE(v6) = 1;
      if ( v45 > 0 )
        return (unsigned int)v6;
      v46 = *(_QWORD **)(a1 + 32);
      v47 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 24), v46, v33);
      if ( v47 != v46 )
      {
        v48 = v47;
        while ( ++v48 != v46 )
        {
          if ( *v48 != v33 )
            *v47++ = *v48;
        }
      }
      goto LABEL_389;
    }
    goto LABEL_388;
  }
  if ( a2 > 1346790241 )
  {
    if ( a2 <= 1346791234 )
    {
      v41 = (unsigned int)(a2 - 1346790979);
      if ( (unsigned int)v41 <= 0x2F )
      {
        v42 = 0x80000000002BLL;
        if ( _bittest64(&v42, v41) )
          goto LABEL_334;
        v43 = 0x600000000LL;
        if ( _bittest64(&v43, v41) )
          goto LABEL_324;
      }
      if ( a2 == 1346790242 )
      {
LABEL_334:
        if ( v33 != 0 )
        {
          v77 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
          *(_DWORD *)(v33 + 24) = v77;
          LOBYTE(v6) = 1;
          if ( v77 > 0 )
            return (unsigned int)v6;
          v46 = *(_QWORD **)(a1 + 32);
          v47 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 24), v46, v33);
          if ( v47 != v46 )
          {
            v78 = v47;
            while ( ++v78 != v46 )
            {
              if ( *v78 != v33 )
                *v47++ = *v78;
            }
          }
          goto LABEL_389;
        }
        goto LABEL_388;
      }
      if ( a2 != 1346790755 )
        return (unsigned int)v6;
      goto LABEL_235;
    }
    if ( a2 > 1346791277 )
    {
      switch ( a2 )
      {
        case 1346791747:
          goto LABEL_247;
        case 1346791748:
        case 1346791749:
        case 1346791750:
        case 1346791751:
        case 1346791752:
        case 1346791753:
        case 1346791754:
        case 1346791755:
        case 1346791756:
        case 1346791757:
        case 1346791758:
        case 1346791759:
        case 1346791760:
        case 1346791761:
        case 1346791762:
        case 1346791763:
        case 1346791764:
        case 1346791765:
        case 1346791766:
        case 1346791767:
        case 1346791768:
        case 1346791769:
        case 1346791770:
        case 1346791771:
        case 1346791772:
        case 1346791773:
        case 1346791774:
        case 1346791775:
        case 1346791776:
        case 1346791777:
        case 1346791780:
        case 1346791781:
        case 1346791782:
        case 1346791783:
        case 1346791784:
        case 1346791785:
        case 1346791786:
        case 1346791787:
        case 1346791788:
        case 1346791790:
        case 1346791791:
        case 1346791792:
        case 1346791793:
          return (unsigned int)v6;
        case 1346791778:
          goto LABEL_334;
        case 1346791779:
          goto LABEL_240;
        case 1346791789:
          goto LABEL_381;
        case 1346791794:
          goto LABEL_235;
        default:
          if ( a2 == 1346791278 )
            goto LABEL_381;
          return (unsigned int)v6;
      }
    }
    if ( a2 != 1346791235 )
    {
      if ( a2 != 1346791266 )
      {
        if ( a2 != 1346791267 )
          return (unsigned int)v6;
        goto LABEL_240;
      }
      goto LABEL_334;
    }
LABEL_247:
    v136 = (__int64 *)a1;
    sub_141523B90(&v137, a1, v26);
    v140 = v26;
    v134 = &v136;
    v135 = &v137;
    v49 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3);
    v50 = *(__int64 **)a3;
    v51 = **(_QWORD **)a3;
    if ( v49 == 10 )
    {
      v6 = (__int64 *)(*(__int64 (__fastcall **)(__int64 *, unsigned int *, _QWORD))(v51 + 176))(v50, a3, 0);
      v52 = *v6;
      v53 = v6[1];
      if ( *v6 != v53 )
      {
        v54 = *v6;
        while ( *(_DWORD *)v54 != 1819504496 )
        {
          v54 += 16;
          if ( v54 == v53 )
            goto LABEL_487;
        }
        if ( v54 != v53 && *(_QWORD *)(v54 + 8) != 0 )
        {
          v79 = nullptr;
          while ( *(_DWORD *)v52 != 1819504496 )
          {
            v52 += 16;
            if ( v52 == v53 )
              goto LABEL_407;
          }
          if ( v52 == v53 )
            v79 = nullptr;
          else
            v79 = *(__int64 **)(v52 + 8);
LABEL_407:
          v89 = &qword_141B5A4A0;
          if ( v79 == nullptr )
            v79 = &qword_141B5A4A0;
          switch ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)*v79 + 64LL))(*v79) )
          {
            case 0u:
              sub_141524360(&v136);
              goto LABEL_487;
            case 1u:
              v90 = *v6;
              v91 = v6[1];
              v92 = nullptr;
              if ( *v6 != v91 )
              {
                while ( *(_DWORD *)v90 != 1869379180 )
                {
                  v90 += 16;
                  if ( v90 == v91 )
                    goto LABEL_441;
                }
                if ( v90 == v91 )
                  v92 = nullptr;
                else
                  v92 = *(__int64 **)(v90 + 8);
              }
LABEL_441:
              if ( v92 == nullptr )
                v92 = &qword_141B5A4A0;
              v106 = sub_141197370(&v135, v92);
              if ( v106 < 0 )
                goto LABEL_487;
              v96 = v137;
              v107 = v137[v106];
              if ( v107 == 0 )
                goto LABEL_489;
              v108 = *v6;
              v109 = v6[1];
              v110 = nullptr;
              if ( *v6 == v109 )
              {
                v6 = &qword_141B5A4A0;
              }
              else
              {
                v111 = *v6;
                while ( *(_DWORD *)v111 != 1986096245 )
                {
                  v111 += 16;
                  if ( v111 == v109 )
                    goto LABEL_475;
                }
                if ( v111 == v109 )
                  v110 = nullptr;
                else
                  v110 = *(__int64 **)(v111 + 8);
LABEL_475:
                v6 = &qword_141B5A4A0;
                if ( v110 != nullptr )
                  v6 = v110;
                v110 = nullptr;
                while ( *(_DWORD *)v108 != 1768169504 )
                {
                  v108 += 16;
                  if ( v108 == v109 )
                    goto LABEL_484;
                }
                if ( v108 == v109 )
                  v110 = nullptr;
                else
                  v110 = *(__int64 **)(v108 + 8);
              }
LABEL_484:
              if ( v110 != nullptr )
                v89 = v110;
              v128 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v89 + 80LL))(*v89, v89);
              sub_141196420(v107, v128, v6);
              goto LABEL_487;
            case 2u:
              v93 = *v6;
              v94 = v6[1];
              v95 = nullptr;
              if ( *v6 != v94 )
              {
                while ( *(_DWORD *)v93 != 1869379180 )
                {
                  v93 += 16;
                  if ( v93 == v94 )
                    goto LABEL_454;
                }
                if ( v93 == v94 )
                  v95 = nullptr;
                else
                  v95 = *(__int64 **)(v93 + 8);
              }
LABEL_454:
              if ( v95 != nullptr )
                v89 = v95;
              v112 = sub_141197370(&v135, v89);
              if ( v112 < 0 )
                goto LABEL_487;
              v96 = v137;
              v113 = v137[v112];
              if ( v113 == 0 )
                goto LABEL_489;
              v114 = v136;
              v115 = sub_141751B70(v136[3], v136[4], v113);
              v116 = v114[3];
              v117 = v114[4];
              v118 = (unsigned __int64)(v115 - v116) >> 3;
              v119 = v115 == v117;
              v120 = -1;
              if ( !v119 )
                v120 = v118;
              if ( v120 >= 0 )
              {
                v121 = (_QWORD *)(v116 + 8LL * (unsigned int)v120);
                if ( *v121 != 0 )
                {
                  ((void (*)(void))sub_141750CFC)();
                  v117 = v114[4];
                }
                sub_141758A00(v121, v121 + 1, v117 - (_QWORD)(v121 + 1));
                v114[4] -= 8;
              }
              goto LABEL_487;
            case 3u:
              v96 = v138;
              if ( v138 == v137 )
                goto LABEL_488;
              v97 = v138 - v137;
              do
              {
                v98 = v137[--v97];
                if ( v98 != 0 )
                {
                  v6 = v136;
                  v99 = sub_141751B70(v136[3], v136[4], v98);
                  v100 = v6[3];
                  v101 = v6[4];
                  v102 = (unsigned __int64)(v99 - v100) >> 3;
                  if ( v99 == v101 )
                    LODWORD(v102) = -1;
                  if ( (v102 & 0x80000000) == 0LL )
                  {
                    v103 = (unsigned int)v102;
                    if ( *(_QWORD *)(v100 + 8LL * (unsigned int)v102) != 0 )
                    {
                      ((void (*)(void))sub_141750CFC)();
                      v101 = v6[4];
                    }
                    sub_141758A00(v100 + 8 * v103, v100 + 8 * v103 + 8, v101 - (v100 + 8 * v103 + 8));
                    v6[4] -= 8;
                  }
                }
              }
              while ( v97 != 0 );
              goto LABEL_487;
            case 4u:
              v104 = *v6;
              v105 = v6[1];
              v6 = nullptr;
              if ( v104 == v105 )
                goto LABEL_465;
              break;
            case 5u:
              v75 = 0;
              goto LABEL_321;
            default:
              goto LABEL_487;
          }
          while ( *(_DWORD *)v104 != 1869379180 )
          {
            v104 += 16;
            if ( v104 == v105 )
              goto LABEL_465;
          }
          if ( v104 == v105 )
            v6 = nullptr;
          else
            v6 = *(__int64 **)(v104 + 8);
LABEL_465:
          v122 = sub_141524360(&v136);
          if ( v122 != 0 )
          {
            v123 = v122;
            if ( v6 == nullptr )
              v6 = &qword_141B5A4A0;
            v6 = (__int64 *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v6 + 176LL))(*v6, v6, 0);
            v124 = v6[1] - *v6;
            if ( v124 != 0 )
            {
              v125 = v124 >> 4;
              v126 = 8;
              do
              {
                v127 = *(__int64 **)(*v6 + v126);
                if ( v127 == nullptr )
                  v127 = &qword_141B5A4A0;
                sub_141196420(v123, *(unsigned int *)(*v6 + v126 - 8), v127);
                v126 += 16;
                --v125;
              }
              while ( v125 != 0 );
            }
          }
        }
      }
      goto LABEL_487;
    }
    if ( (*(unsigned __int8 (__fastcall **)(__int64 *, unsigned int *))(v51 + 8))(v50, a3) != 11 )
    {
LABEL_487:
      v96 = v137;
LABEL_488:
      if ( v96 != nullptr )
      {
LABEL_489:
        v129 = v139 - (_QWORD)v96;
        if ( v139 - (_QWORD)v96 == -1 )
          v129 = *(unsigned int *)((char *)v96 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v130 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v130) >> 3 > v129)
          && (v131 = *(_QWORD *)(v130 + 8 * v129)) != 0 )
        {
          MEMORY[0x1419475D8](v131 + 32, (char *)v96 - *(unsigned int *)(v131 + 120));
          v132 = *(_BYTE *)(v131 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v131 + 64)) != 0;
          if ( !v132 && *(_BYTE *)(v131 + 97) != 0 )
            sub_1412D33C0(v131);
        }
        else
        {
          MEMORY[0x141948990]((char *)v96 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      goto LABEL_497;
    }
    v55 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD, unsigned int *, _QWORD))(**(_QWORD **)a3 + 184LL))(
                      *(_QWORD *)a3,
                      a3,
                      0);
    if ( v138 != v137 )
    {
      v56 = v138 - v137;
      do
      {
        v57 = v137[--v56];
        if ( v57 != 0 )
        {
          v6 = v136;
          v58 = sub_141751B70(v136[3], v136[4], v57);
          v59 = v6[3];
          v60 = v6[4];
          v61 = (unsigned __int64)(v58 - v59) >> 3;
          if ( v58 == v60 )
            LODWORD(v61) = -1;
          if ( (v61 & 0x80000000) == 0LL )
          {
            v62 = (unsigned int)v61;
            if ( *(_QWORD *)(v59 + 8LL * (unsigned int)v61) != 0 )
            {
              ((void (*)(void))sub_141750CFC)();
              v60 = v6[4];
            }
            sub_141758A00(v59 + 8 * v62, v59 + 8 * v62 + 8, v60 - (v59 + 8 * v62 + 8));
            v6[4] -= 8;
          }
        }
      }
      while ( v56 != 0 );
    }
    v63 = v55[1] - *v55;
    if ( v63 == 0 )
    {
LABEL_317:
      v75 = qword_141B60C38;
      v76 = qword_141B60C30;
      if ( qword_141B60C30 == qword_141B60C38 )
        goto LABEL_320;
      while ( *(_DWORD *)v76 != 1986359923 )
      {
        v76 += 16;
        if ( v76 == qword_141B60C38 )
          goto LABEL_320;
      }
      if ( v76 == qword_141B60C38 || *(_QWORD *)(v76 + 8) == 0 )
      {
LABEL_320:
        LOBYTE(v75) = 1;
LABEL_321:
        sub_140DF3CB0(v75);
      }
      goto LABEL_487;
    }
    v64 = v63 >> 3;
    v65 = 1;
    if ( v64 >= 2 )
      v65 = v64;
    v66 = 0;
    while ( 1 )
    {
      v67 = *(__int64 **)(*v55 + 8 * v66);
      v68 = sub_141524360(&v136);
      if ( v68 != 0 )
      {
        v6 = (__int64 *)v68;
        if ( v67 == nullptr )
          v67 = &qword_141B5A4A0;
        v69 = (_QWORD *)(*(__int64 (__fastcall **)(__int64, __int64 *, _QWORD))(*(_QWORD *)*v67 + 176LL))(*v67, v67, 0);
        v70 = v69[1] - *v69;
        if ( v70 != 0 )
          break;
      }
LABEL_268:
      if ( ++v66 == v65 )
        goto LABEL_317;
    }
    v71 = v70 >> 4;
    v72 = 8;
    while ( 1 )
    {
      v73 = *(__int64 **)(*v69 + v72);
      if ( v73 == nullptr )
        v73 = &qword_141B5A4A0;
      v74 = *(_DWORD *)(*v69 + v72 - 8);
      if ( v74 <= 1346793580 )
        break;
      if ( v74 <= 1347905890 )
      {
        if ( v74 <= 1347185004 )
        {
          if ( v74 == 1346793581 )
            goto LABEL_315;
          if ( v74 != 1347176803 )
            goto LABEL_276;
        }
        else
        {
          if ( v74 == 1347185005 )
            goto LABEL_315;
          if ( v74 != 1347905347 )
          {
            if ( v74 != 1347905351 )
              goto LABEL_276;
            goto LABEL_315;
          }
        }
        goto LABEL_275;
      }
      if ( v74 <= 1348036418 )
      {
        if ( v74 != 1347905891 )
        {
          if ( v74 != 1347905901 && v74 != 1348036417 )
            goto LABEL_276;
LABEL_315:
          *((_DWORD *)v6 + 5) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v73 + 64LL))(*v73);
          goto LABEL_276;
        }
        goto LABEL_275;
      }
      switch ( v74 )
      {
        case 1348036419:
          goto LABEL_275;
        case 1348101959:
          goto LABEL_315;
        case 1348101955:
          goto LABEL_275;
        default:
          break;
      }
LABEL_276:
      v72 += 16;
      if ( --v71 == 0 )
        goto LABEL_268;
    }
    if ( v74 <= 1346792546 )
    {
      if ( v74 <= 1346791277 )
      {
        if ( v74 != 1346789986 && v74 != 1346791267 )
          goto LABEL_276;
      }
      else
      {
        if ( v74 == 1346791278 )
          goto LABEL_315;
        if ( v74 != 1346791779 )
        {
          if ( v74 != 1346791789 )
            goto LABEL_276;
          goto LABEL_315;
        }
      }
    }
    else if ( v74 > 1346792808 )
    {
      if ( v74 == 1346792809 )
      {
        *((_BYTE *)v6 + 41) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v73 + 64LL))(*v73);
        goto LABEL_276;
      }
      if ( v74 == 1346792813 )
        goto LABEL_315;
      if ( v74 != 1346793571 )
        goto LABEL_276;
    }
    else if ( v74 != 1346792547 )
    {
      if ( v74 == 1346792557 )
        goto LABEL_315;
      if ( v74 != 1346792803 )
        goto LABEL_276;
    }
LABEL_275:
    *((_DWORD *)v6 + 6) = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v73 + 64LL))(*v73);
    goto LABEL_276;
  }
  if ( a2 <= 1346786117 )
  {
    if ( a2 > 1346782060 )
    {
      if ( a2 <= 1346783057 )
      {
        if ( a2 != 1346782061 )
        {
          if ( a2 != 1346782308 )
            return (unsigned int)v6;
          goto LABEL_324;
        }
      }
      else if ( a2 != 1346783058 )
      {
        if ( a2 != 1346783332 )
        {
          if ( a2 != 1346784327 )
            return (unsigned int)v6;
          goto LABEL_381;
        }
LABEL_324:
        if ( v33 != 0 )
        {
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
          if ( *(__int64 **)a3 == &qword_141B5C8A0 )
          {
            v80 = a3[2];
            WORD1(v134) = v80 >> 17;
            LOWORD(v134) = (v80 >> 8) & 0x1FF | ((_WORD)v80 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                      *(_QWORD *)a3,
                      a3) == 27 )
          {
            (*(void (__fastcall **)(_QWORD, __int64 **, unsigned int *))(**(_QWORD **)a3 + 160LL))(
              *(_QWORD *)a3,
              &v136,
              a3);
            sub_1413CA830(&v134, &v136);
          }
          else
          {
            LODWORD(v134) = 124518401;
          }
          *(_DWORD *)(v33 + 36) = (_DWORD)v134;
          goto LABEL_497;
        }
        goto LABEL_388;
      }
LABEL_362:
      if ( v33 != 0 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
        {
          v85 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
          *(_DWORD *)(v33 + 12) = v85;
          LOBYTE(v6) = 1;
          if ( v85 > 0 )
            return (unsigned int)v6;
        }
        else
        {
          *(_DWORD *)(v33 + 12) = -1;
        }
        v46 = *(_QWORD **)(a1 + 32);
        v47 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 24), v46, v33);
        if ( v47 != v46 )
        {
          v86 = v47;
          while ( ++v86 != v46 )
          {
            if ( *v86 != v33 )
              *v47++ = *v86;
          }
        }
        LOBYTE(v6) = 1;
        goto LABEL_389;
      }
LABEL_388:
      LODWORD(v6) = 0;
      return (unsigned int)v6;
    }
    if ( a2 > 1346782039 )
    {
      if ( a2 == 1346782040 )
        goto LABEL_381;
      if ( a2 != 1346782052 )
        return (unsigned int)v6;
      goto LABEL_324;
    }
    if ( a2 != 1346777409 && a2 != 1346777424 )
      return (unsigned int)v6;
LABEL_381:
    if ( v33 != 0 )
    {
      v87 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
      *(_DWORD *)(v33 + 20) = v87;
      LOBYTE(v6) = 1;
      if ( v87 > 0 )
        return (unsigned int)v6;
      v46 = *(_QWORD **)(a1 + 32);
      v47 = (_QWORD *)sub_141751B70(*(_QWORD *)(a1 + 24), v46, v33);
      if ( v47 != v46 )
      {
        v88 = v47;
        while ( ++v88 != v46 )
        {
          if ( *v88 != v33 )
            *v47++ = *v88;
        }
      }
LABEL_389:
      if ( v47 != v46 )
      {
        if ( v47 != *(_QWORD **)(a1 + 32) )
          *(_QWORD *)(a1 + 32) = v47;
        sub_141750CFC(v33);
      }
      return (unsigned int)v6;
    }
    goto LABEL_388;
  }
  if ( a2 <= 1346787138 )
  {
    if ( a2 <= 1346786374 )
    {
      if ( a2 != 1346786118 && a2 != 1346786160 )
        return (unsigned int)v6;
      goto LABEL_362;
    }
    if ( a2 != 1346786375 && a2 != 1346786393 )
      return (unsigned int)v6;
    goto LABEL_334;
  }
  if ( a2 > 1346789743 )
  {
    if ( a2 != 1346789744 )
    {
      if ( a2 != 1346789955 )
      {
        if ( a2 != 1346789986 )
          return (unsigned int)v6;
        goto LABEL_240;
      }
      goto LABEL_247;
    }
    goto LABEL_334;
  }
  if ( a2 != 1346787139 )
  {
    if ( a2 != 1346789730 )
      return (unsigned int)v6;
    goto LABEL_334;
  }
LABEL_235:
  if ( v33 == 0 )
    goto LABEL_388;
  LOBYTE(v6) = 1;
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3) == 0 )
LABEL_237:
    sub_1411946C0(v27, v33);
  return (unsigned int)v6;
}
