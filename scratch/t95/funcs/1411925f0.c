__int64 __fastcall sub_1411925F0(__int64 a1, int a2, __int64 *a3)
{
  __int64 v5; // r14
  unsigned int v6; // edi
  unsigned __int64 v7; // rax
  __int64 v8; // rcx
  unsigned __int64 v9; // rax
  __int64 v10; // rcx
  __int64 v11; // rax
  unsigned __int64 v12; // rax
  unsigned __int64 v13; // rax
  __int64 v14; // rcx
  unsigned int v15; // eax
  int v16; // ecx
  char v17; // bl
  __int64 v18; // rax
  unsigned __int64 v19; // rax
  int v20; // esi
  __int64 v21; // rax
  __int64 v22; // rcx
  int v23; // esi
  int v24; // ecx
  __int64 v25; // rax
  __int64 v26; // rcx
  unsigned int v27; // eax
  __int64 v28; // rdx
  __int64 v29; // rcx
  unsigned __int64 v30; // rcx
  __int64 v31; // rdi
  __int64 v32; // rsi
  unsigned __int64 v33; // rax
  __int64 v34; // rdx
  __int64 v35; // rdx
  __int64 v36; // rsi
  __int64 v37; // rax
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 v40; // rdi
  signed __int64 v41; // rdx
  __int64 v42; // rsi
  signed __int64 v43; // rdi
  __int64 v44; // rcx
  __int128 v45; // kr00_16
  __int64 v46; // rdx
  unsigned __int64 v47; // r13
  __int64 v48; // r14
  __int64 v49; // r15
  __int64 v50; // rsi
  unsigned __int64 v51; // rcx
  __int64 v52; // r8
  __int64 v53; // rcx
  __int64 v54; // rbx
  bool v55; // al
  __int64 v56; // rbx
  __int128 *v57; // rdi
  __int64 i; // r14
  __int64 v59; // rsi
  __int64 v60; // rax
  __int64 v61; // rcx
  __int64 v62; // rax
  __int64 v63; // rcx
  unsigned __int64 v64; // rcx
  __int64 v65; // rbx
  __int64 v66; // rsi
  bool v67; // al
  unsigned __int64 v68; // rcx
  __int64 v69; // rbx
  __int64 v70; // rsi
  bool v71; // al
  int v72; // esi
  __int64 v73; // rax
  int v74; // esi
  __int64 v75; // rax
  __int64 v76; // rcx
  int v77; // esi
  __int64 v78; // rcx
  int v79; // esi
  __int64 v80; // rcx
  __int64 v82; // rax
  __int64 *v83; // [rsp+20h] [rbp-60h]
  char *v84; // [rsp+28h] [rbp-58h] BYREF
  char *v85; // [rsp+30h] [rbp-50h]
  __int64 v86; // [rsp+38h] [rbp-48h]
  int v87; // [rsp+40h] [rbp-40h]
  __int128 *v88; // [rsp+48h] [rbp-38h] BYREF
  __int64 v89; // [rsp+50h] [rbp-30h]
  __int64 v90; // [rsp+58h] [rbp-28h] BYREF
  __int64 v91; // [rsp+60h] [rbp-20h]
  unsigned __int64 v92; // [rsp+68h] [rbp-18h]
  __int64 v93; // [rsp+70h] [rbp-10h] BYREF
  __int64 v94; // [rsp+78h] [rbp-8h]
  __int128 v95; // [rsp+80h] [rbp+0h] BYREF
  __int64 v96; // [rsp+90h] [rbp+10h]
  int v97; // [rsp+98h] [rbp+18h]
  __int64 v98; // [rsp+A0h] [rbp+20h]

  v98 = -2;
  v5 = a1;
  v6 = 0;
  if ( a2 <= 1346792046 )
  {
    if ( a2 > 1346790251 )
    {
      if ( a2 > 1346790978 )
      {
        v12 = (unsigned int)(a2 - 1346790979);
        if ( (unsigned int)v12 <= 0x2F )
        {
          v22 = 0x80060000002BLL;
          if ( _bittest64(&v22, v12) )
            goto LABEL_118;
        }
        v13 = (unsigned int)(a2 - 1346791747);
        if ( (unsigned int)v13 <= 0x2F )
        {
          v14 = 0x840180000001LL;
          if ( _bittest64(&v14, v13) )
            goto LABEL_118;
        }
        v9 = (unsigned int)(a2 - 1346791235);
        if ( (unsigned int)v9 > 0x2B )
          return v6;
        v10 = 0x80180000001LL;
        goto LABEL_62;
      }
      if ( a2 > 1346790515 )
      {
        switch ( a2 )
        {
          case 1346790516:
            v25 = sub_140DBC940();
            DWORD2(v95) = ((*(_WORD *)(v5 + 104) & 0x1FF) << 8)
                        | (*(unsigned __int16 *)(v5 + 104) >> 9)
                        | (*(unsigned __int16 *)(v5 + 106) << 17);
            *(_QWORD *)&v95 = v25;
            sub_14083DFA0(a3, &v95);
            (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
            break;
          case 1346790755:
            goto LABEL_118;
          case 1346790756:
            v11 = sub_140DBC940();
            DWORD2(v95) = ((*(_WORD *)(v5 + 116) & 0x1FF) << 8)
                        | (*(unsigned __int16 *)(v5 + 116) >> 9)
                        | (*(unsigned __int16 *)(v5 + 118) << 17);
            *(_QWORD *)&v95 = v11;
            sub_14083DFA0(a3, &v95);
            (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
            break;
          default:
            return v6;
        }
        goto LABEL_295;
      }
      if ( a2 != 1346790252 )
      {
        if ( a2 == 1346790259 )
        {
          if ( *(_BYTE *)(a1 + 128) == 6 )
          {
            (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
              qword_141B5A4A0,
              &qword_141B5A4A0,
              &v95);
          }
          else
          {
            DWORD2(v95) = *(char *)(a1 + 128);
            *(_QWORD *)&v95 = sub_14083D4F0(a1) + 40;
          }
          if ( &v95 != (__int128 *)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v95 + 24LL))(v95, &v95, a3);
          }
          goto LABEL_289;
        }
        return v6;
      }
      v26 = *(_QWORD *)(a1 + 80);
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
              return v6;
          }
          else if ( a2 != 1346782308 && a2 != 1346783058 )
          {
            return v6;
          }
          goto LABEL_118;
        }
        if ( a2 <= 1346782039 )
        {
          if ( a2 == 1179935340 )
          {
            *(_QWORD *)&v95 = a1 + 48;
            v84 = (char *)&v95;
            return (unsigned int)sub_1411968C0(&v84, a3);
          }
          if ( a2 != 1346777409 && a2 != 1346777424 )
            return v6;
          goto LABEL_118;
        }
        v15 = a2 - 1346782040;
        if ( (unsigned int)(a2 - 1346782040) > 0x15 )
          return v6;
        v16 = 2101249;
        goto LABEL_94;
      }
      if ( a2 > 1346787138 )
      {
        if ( a2 > 1346789954 )
        {
          if ( a2 != 1346789955 && a2 != 1346789986 && a2 != 1346790242 )
            return v6;
        }
        else if ( a2 != 1346787139 && a2 != 1346789730 && a2 != 1346789744 )
        {
          return v6;
        }
        goto LABEL_118;
      }
      if ( a2 > 1346786159 )
      {
        if ( a2 != 1346786160 && a2 != 1346786375 && a2 != 1346786393 )
          return v6;
        goto LABEL_118;
      }
      if ( a2 == 1346786118 )
        goto LABEL_118;
      if ( a2 != 1346786156 )
        return v6;
      v26 = *(_QWORD *)(a1 + 88);
    }
    sub_140FCC150(v26, a3);
    LOBYTE(v6) = 1;
    return v6;
  }
  if ( a2 > 1346795368 )
  {
    if ( a2 <= 1347905345 )
    {
      if ( a2 > 1347184962 )
      {
        if ( a2 <= 1347637061 )
        {
          if ( a2 != 1347184963 && a2 != 1347185005 )
            return v6;
        }
        else if ( a2 != 1347637062 && a2 != 1347637315 && a2 != 1347637328 )
        {
          return v6;
        }
        goto LABEL_118;
      }
      if ( a2 > 1346795599 )
      {
        if ( a2 != 1346795600 && a2 != 1347176803 )
          return v6;
        goto LABEL_118;
      }
      if ( a2 == 1346795369 )
        goto LABEL_118;
      if ( a2 != 1346795376 )
        return v6;
      v17 = *(_BYTE *)(a1 + 131);
      v18 = sub_14083D4F0(a1);
      BYTE8(v95) = v17;
      *(_QWORD *)&v95 = v18 + 24;
      sub_14083DFA0(a3, &v95);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
LABEL_295:
      LOBYTE(v6) = 1;
      return v6;
    }
    if ( a2 <= 1348036416 )
    {
      if ( (unsigned int)(a2 - 1347905346) <= 5 )
      {
        v24 = 35;
        if ( _bittest(&v24, a2 - 1347905346) )
          goto LABEL_118;
      }
      v9 = (unsigned int)(a2 - 1347905859);
      if ( (unsigned int)v9 > 0x2A )
        return v6;
      v10 = 0x40100000001LL;
      goto LABEL_62;
    }
    if ( (unsigned int)(a2 - 1348036417) < 3 )
      goto LABEL_118;
    v15 = a2 - 1348101954;
    if ( (unsigned int)(a2 - 1348101954) > 5 )
      return v6;
    v16 = 35;
LABEL_94:
    if ( !_bittest(&v16, v15) )
      return v6;
    goto LABEL_118;
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
            if ( *(char *)(a1 + 130) == -1 )
            {
              (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                qword_141B5A4A0,
                &qword_141B5A4A0,
                &v95);
            }
            else
            {
              DWORD2(v95) = *(char *)(a1 + 130);
              *(_QWORD *)&v95 = sub_14083D4F0(a1) + 40;
            }
            if ( &v95 != (__int128 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v95 + 24LL))(v95, &v95, a3);
            }
            goto LABEL_289;
          case 1346794598:
            v23 = *(_DWORD *)(a1 + 108);
            if ( v23 < 0 )
              goto LABEL_299;
            break;
          case 1346795361:
            v23 = *(_DWORD *)(a1 + 112);
            if ( v23 < 0 )
              goto LABEL_299;
            break;
          default:
            return v6;
        }
        goto LABEL_298;
      }
      if ( a2 != 1346794083 )
      {
        if ( a2 != 1346794084 && a2 != 1346794086 )
          return v6;
        goto LABEL_118;
      }
      v36 = *(_QWORD *)(a1 + 96);
      v37 = sub_14083D4F0(a1);
      BYTE8(v95) = (v36 & 0x8000000) != 0;
      *(_QWORD *)&v95 = v37 + 24;
      sub_14083DFA0(a3, &v95);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
      goto LABEL_295;
    }
    v9 = (unsigned int)(a2 - 1346793539);
    if ( (unsigned int)v9 > 0x2F )
      return v6;
    v10 = 0x844100000001LL;
LABEL_62:
    if ( !_bittest64(&v10, v9) )
      return v6;
    goto LABEL_118;
  }
  if ( a2 <= 1346792770 )
  {
    v19 = (unsigned int)(a2 - 1346792515);
    if ( (unsigned int)v19 <= 0x2A )
    {
      a1 = 0x40100000001LL;
      if ( _bittest64(&a1, v19) )
        goto LABEL_118;
    }
    if ( a2 != 1346792047 )
      return v6;
    v20 = *(unsigned __int16 *)(v5 + 124);
    if ( *(_WORD *)(v5 + 124) == 0 )
      goto LABEL_299;
    v21 = sub_14083D4F0(a1);
    DWORD2(v95) = v20;
    *(_QWORD *)&v95 = v21 + 56;
    sub_14083DFA0(a3, &v95);
    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
    goto LABEL_295;
  }
  v7 = (unsigned int)(a2 - 1346792771);
  if ( (unsigned int)v7 <= 0x30 )
  {
    v8 = 0x46100000001LL;
    if ( _bittest64(&v8, v7) )
      goto LABEL_118;
    if ( v7 == 48 )
    {
      if ( *(char *)(v5 + 129) == -1 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int128 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v95);
      }
      else
      {
        DWORD2(v95) = *(char *)(v5 + 129);
        *(_QWORD *)&v95 = sub_14083D4F0(0x46100000001LL) + 40;
      }
      if ( &v95 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        (*(void (__fastcall **)(_QWORD, __int128 *, __int64 *))(*(_QWORD *)v95 + 24LL))(v95, &v95, a3);
      }
LABEL_289:
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
      goto LABEL_295;
    }
  }
  if ( a2 != 1346793075 )
    return v6;
LABEL_118:
  v27 = sub_141193FB0((unsigned int)a2);
  v28 = *(_QWORD *)(v5 + 24);
  v29 = *(_QWORD *)(v5 + 32) - v28;
  if ( v29 == 0 )
    return 0;
  v30 = v29 >> 3;
  v31 = 1;
  if ( v30 >= 2 )
    v31 = v30;
  v32 = 0;
  while ( 1 )
  {
    a1 = *(_QWORD *)(v28 + 8 * v32);
    if ( *(_DWORD *)(a1 + 8) == v27 )
      break;
    if ( v31 == ++v32 )
      return 0;
  }
  v6 = 0;
  if ( a2 > 1346792514 )
  {
    if ( a2 > 1347176802 )
    {
      if ( a2 > 1347905858 )
      {
        if ( a2 <= 1348036417 )
        {
          if ( a2 > 1347905900 )
          {
            if ( a2 != 1347905901 && a2 != 1348036417 )
              return v6;
            goto LABEL_278;
          }
          if ( a2 != 1347905859 )
          {
            if ( a2 != 1347905891 )
              return v6;
            goto LABEL_269;
          }
        }
        else if ( a2 <= 1348101953 )
        {
          if ( a2 != 1348036418 )
          {
            if ( a2 != 1348036419 )
              return v6;
            goto LABEL_269;
          }
        }
        else if ( a2 != 1348101954 )
        {
          if ( a2 == 1348101959 )
            goto LABEL_278;
          if ( a2 != 1348101955 )
            return v6;
          goto LABEL_269;
        }
        goto LABEL_218;
      }
      if ( a2 <= 1347637314 )
      {
        if ( a2 > 1347185004 )
        {
          if ( a2 != 1347185005 && a2 != 1347637062 )
            return v6;
          goto LABEL_278;
        }
        if ( a2 == 1347176803 )
          goto LABEL_269;
        if ( a2 != 1347184963 )
          return v6;
        goto LABEL_218;
      }
      if ( a2 > 1347905345 )
      {
        if ( a2 != 1347905346 )
        {
          if ( a2 != 1347905347 )
          {
            if ( a2 != 1347905351 )
              return v6;
            goto LABEL_278;
          }
          goto LABEL_269;
        }
        goto LABEL_218;
      }
      if ( a2 != 1347637315 )
      {
        if ( a2 != 1347637328 )
          return v6;
        goto LABEL_278;
      }
      v23 = *(_DWORD *)(a1 + 24);
      if ( v23 <= 0 )
        goto LABEL_299;
    }
    else
    {
      if ( a2 <= 1346793538 )
      {
        if ( a2 <= 1346792770 )
        {
          if ( a2 != 1346792515 )
          {
            if ( a2 != 1346792547 )
            {
              if ( a2 != 1346792557 )
                return v6;
              goto LABEL_278;
            }
            goto LABEL_269;
          }
          goto LABEL_218;
        }
        switch ( a2 )
        {
          case 1346792771:
            goto LABEL_218;
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
            return v6;
          case 1346792803:
            goto LABEL_269;
          case 1346792808:
            goto LABEL_214;
          case 1346792809:
            v23 = *(unsigned __int8 *)(a1 + 41);
            if ( (char)v23 > 0 )
              goto LABEL_298;
            goto LABEL_299;
          case 1346792813:
            goto LABEL_278;
          default:
            if ( a2 == 1346793075 )
              goto LABEL_291;
            break;
        }
        return v6;
      }
      if ( a2 <= 1346794083 )
      {
        switch ( a2 )
        {
          case 1346793539:
            goto LABEL_218;
          case 1346793571:
            goto LABEL_269;
          case 1346793577:
            goto LABEL_291;
          case 1346793581:
            goto LABEL_278;
          case 1346793586:
            goto LABEL_185;
          default:
            return v6;
        }
      }
      if ( a2 > 1346795368 )
      {
        if ( a2 != 1346795369 )
        {
          if ( a2 != 1346795600 )
            return v6;
          goto LABEL_278;
        }
        goto LABEL_291;
      }
      if ( a2 == 1346794084 )
        goto LABEL_291;
      if ( a2 != 1346794086 )
        return v6;
LABEL_185:
      v23 = *(_DWORD *)(a1 + 24);
      if ( v23 < 0 )
        goto LABEL_299;
    }
LABEL_298:
    v82 = sub_14083D4F0(a1);
    DWORD2(v95) = v23;
    *(_QWORD *)&v95 = v82 + 40;
    sub_14083DFA0(a3, &v95);
    (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
    goto LABEL_295;
  }
  if ( a2 <= 1346790241 )
  {
    if ( a2 <= 1346786117 )
    {
      if ( a2 <= 1346782060 )
      {
        if ( a2 <= 1346782039 )
        {
          if ( a2 != 1346777409 && a2 != 1346777424 )
            return v6;
          goto LABEL_278;
        }
        if ( a2 == 1346782040 )
        {
LABEL_278:
          v77 = *(_DWORD *)(a1 + 20);
          if ( v77 > 0 )
          {
            v75 = sub_14083D4F0(a1) + 40;
            DWORD2(v95) = v77;
            *(_QWORD *)&v95 = v75;
            if ( &v95 != (__int128 *)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v78 = *((_QWORD *)&v95 + 1);
              *(_OWORD *)a3 = v95;
              v75 = sub_14083D4F0(v78) + 8;
              v95 = (unsigned __int64)v75;
            }
LABEL_294:
            (*(void (__fastcall **)(__int64, __int128 *))(*(_QWORD *)v75 + 16LL))(v75, &v95);
            goto LABEL_295;
          }
          goto LABEL_299;
        }
        if ( a2 != 1346782052 )
          return v6;
LABEL_262:
        v72 = *(_DWORD *)(a1 + 36);
        if ( (v72 & 0xFFFF01FF) != 0x76C0001 )
        {
          v73 = sub_140DBC940();
          DWORD2(v95) = (v72 << 8) & 0x1FF00 | (((unsigned __int16)v72 >> 9) + 2 * (v72 & 0xFFFF0000));
          *(_QWORD *)&v95 = v73;
          sub_14083DFA0(a3, &v95);
          (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
          goto LABEL_295;
        }
LABEL_299:
        LOBYTE(v6) = 1;
        if ( a3 != &qword_141B5A4A0 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            a3);
        }
        return v6;
      }
      if ( a2 <= 1346783057 )
      {
        if ( a2 != 1346782061 )
        {
          if ( a2 != 1346782308 )
            return v6;
          goto LABEL_262;
        }
      }
      else if ( a2 != 1346783058 )
      {
        if ( a2 != 1346783332 )
        {
          if ( a2 != 1346784327 )
            return v6;
          goto LABEL_278;
        }
        goto LABEL_262;
      }
LABEL_291:
      v79 = *(_DWORD *)(a1 + 12);
      if ( v79 > 0 )
      {
        v75 = sub_14083D4F0(a1) + 40;
        DWORD2(v95) = v79;
        *(_QWORD *)&v95 = v75;
        if ( &v95 != (__int128 *)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v80 = *((_QWORD *)&v95 + 1);
          *(_OWORD *)a3 = v95;
          v75 = sub_14083D4F0(v80) + 8;
          v95 = (unsigned __int64)v75;
        }
        goto LABEL_294;
      }
      goto LABEL_299;
    }
    if ( a2 > 1346787138 )
    {
      if ( a2 > 1346789743 )
      {
        if ( a2 == 1346789744 )
          goto LABEL_269;
        if ( a2 != 1346789955 )
        {
          if ( a2 != 1346789986 )
            return v6;
          goto LABEL_269;
        }
LABEL_218:
        sub_141523B90(&v84, v5, v27);
        v40 = v85 - v84;
        v95 = 0;
        v96 = 0;
        v41 = v85 - v84;
        if ( v85 != v84 )
        {
          if ( v85 - v84 < 0 )
            sub_1400526C0(v39, v41);
          v42 = sub_1407E4490(qword_141ABD470, v41);
          *(_QWORD *)&v95 = v42;
          v96 = v42 + 8 * (v40 >> 3);
          v43 = v85 - v84;
          sub_141758A00(v42, v84, v85 - v84);
          *((_QWORD *)&v95 + 1) = v42 + v43;
        }
        v83 = a3;
        v97 = v87;
        v88 = &v95;
        sub_1407C9510(&v90);
        v45 = v95;
        v46 = *((_QWORD *)&v95 + 1) - v95;
        v47 = (__int64)(*((_QWORD *)&v95 + 1) - v95) >> 3;
        v48 = v90;
        if ( (__int64)(v92 - v90) >> 3 < v47 )
        {
          if ( v46 < 0 )
            sub_1400526C0(v44, v46);
          v49 = v91;
          v50 = sub_1407E4490(qword_141ABD470, v46);
          sub_141758A00(v50, v90, v91 - v90);
          if ( v90 != 0 )
          {
            v51 = v92 - v90;
            if ( v92 - v90 == -1 )
              v51 = *(unsigned int *)(v90 - *(unsigned int *)(qword_141ABD470 + 48));
            if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
              && (v52 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v52) >> 3 > v51)
              && (v53 = *(_QWORD *)(v52 + 8 * v51)) != 0 )
            {
              v54 = v90 - *(unsigned int *)(v53 + 120);
              v89 = v53;
              MEMORY[0x1419475D8](v53 + 32, v54);
              v44 = v89;
              v55 = *(_BYTE *)(v89 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v89 + 64)) != 0;
              if ( !v55 && *(_BYTE *)(v44 + 97) != 0 )
                sub_1412D33C0(v44);
            }
            else
            {
              MEMORY[0x141948990](v90 - *(unsigned int *)(qword_141ABD470 + 48));
            }
          }
          v90 = v50;
          v91 = v50 + v49 - v48;
          v92 = v50 + 8 * v47;
        }
        if ( *((_QWORD *)&v45 + 1) != (_QWORD)v45 )
        {
          v56 = 1;
          if ( v47 >= 2 )
            v56 = v47;
          v57 = v88;
          for ( i = 0; i != v56; ++i )
          {
            v59 = *(_QWORD *)(*(_QWORD *)v57 + 8 * i);
            if ( v59 != 0 )
            {
              v60 = sub_14083D4F0(v44);
              v94 = 0;
              v93 = v60 + 8;
              sub_141196DE0(&v88, v59, &v93);
              sub_14083B5F0(&v90, &v93);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v93 + 16LL))(v93, &v93);
            }
          }
        }
        sub_14083DB80(&v93, &v90);
        v61 = *v83;
        if ( &v93 != v83 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, v83);
          v62 = v93;
          v63 = v94;
          v83[1] = v94;
          *v83 = v62;
          v61 = sub_14083D4F0(v63) + 8;
          v94 = 0;
          v93 = v61;
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v93);
        sub_14083B0A0(&v90);
        if ( (_QWORD)v95 != 0 )
        {
          v64 = v96 - v95;
          if ( v96 - (_QWORD)v95 == -1 )
            v64 = *(unsigned int *)(v95 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v65 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v65) >> 3 > v64)
            && (v66 = *(_QWORD *)(v65 + 8 * v64)) != 0 )
          {
            MEMORY[0x1419475D8](v66 + 32, v95 - *(unsigned int *)(v66 + 120));
            v67 = *(_BYTE *)(v66 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v66 + 64)) != 0;
            if ( !v67 && *(_BYTE *)(v66 + 97) != 0 )
              sub_1412D33C0(v66);
          }
          else
          {
            MEMORY[0x141948990](v95 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v6 = (unsigned int)v84;
        if ( v84 != nullptr )
        {
          v68 = v86 - (_QWORD)v84;
          if ( v86 - (_QWORD)v84 == -1 )
            v68 = *(unsigned int *)&v84[-*(unsigned int *)(qword_141ABD470 + 48)];
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v69 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v69) >> 3 > v68)
            && (v70 = *(_QWORD *)(v69 + 8 * v68)) != 0 )
          {
            v6 = (_DWORD)v84 - *(_DWORD *)(v70 + 120);
            MEMORY[0x1419475D8](v70 + 32, &v84[-*(unsigned int *)(v70 + 120)]);
            v71 = *(_BYTE *)(v70 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v70 + 64)) != 0;
            if ( !v71 && *(_BYTE *)(v70 + 97) != 0 )
            {
              sub_1412D33C0(v70);
              LOBYTE(v6) = 1;
              return v6;
            }
          }
          else
          {
            v6 = (_DWORD)v84 - *(_DWORD *)(qword_141ABD470 + 48);
            MEMORY[0x141948990](&v84[-*(unsigned int *)(qword_141ABD470 + 48)]);
          }
        }
        goto LABEL_295;
      }
      if ( a2 != 1346787139 )
      {
        if ( a2 != 1346789730 )
          return v6;
        goto LABEL_269;
      }
      goto LABEL_214;
    }
    if ( a2 <= 1346786374 )
    {
      if ( a2 != 1346786118 && a2 != 1346786160 )
        return v6;
      goto LABEL_291;
    }
    if ( a2 != 1346786375 && a2 != 1346786393 )
      return v6;
    goto LABEL_269;
  }
  if ( a2 <= 1346791234 )
  {
    v33 = (unsigned int)(a2 - 1346790979);
    if ( (unsigned int)v33 <= 0x2F )
    {
      v34 = 0x80000000002BLL;
      if ( _bittest64(&v34, v33) )
        goto LABEL_269;
      v35 = 0x600000000LL;
      if ( _bittest64(&v35, v33) )
        goto LABEL_262;
    }
    if ( a2 != 1346790242 )
    {
      if ( a2 != 1346790755 )
        return v6;
LABEL_214:
      v38 = sub_14083D4F0(a1);
      BYTE8(v95) = 1;
      *(_QWORD *)&v95 = v38 + 24;
      sub_14083DFA0(a3, &v95);
      (*(void (__fastcall **)(_QWORD, __int128 *))(*(_QWORD *)v95 + 16LL))(v95, &v95);
      goto LABEL_295;
    }
LABEL_269:
    v74 = *(_DWORD *)(a1 + 24);
    if ( v74 > 0 )
    {
      v75 = sub_14083D4F0(a1) + 40;
      DWORD2(v95) = v74;
      *(_QWORD *)&v95 = v75;
      if ( &v95 != (__int128 *)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v76 = *((_QWORD *)&v95 + 1);
        *(_OWORD *)a3 = v95;
        v75 = sub_14083D4F0(v76) + 8;
        v95 = (unsigned __int64)v75;
      }
      goto LABEL_294;
    }
    goto LABEL_299;
  }
  if ( a2 <= 1346791746 )
  {
    if ( (unsigned int)(a2 - 1346791266) < 2 )
      goto LABEL_269;
    if ( a2 != 1346791235 )
    {
      if ( a2 != 1346791278 )
        return v6;
      goto LABEL_278;
    }
    goto LABEL_218;
  }
  switch ( a2 )
  {
    case 1346791747:
      goto LABEL_218;
    case 1346791778:
    case 1346791779:
      goto LABEL_269;
    case 1346791789:
      goto LABEL_278;
    case 1346791794:
      goto LABEL_214;
    default:
      return v6;
  }
}
