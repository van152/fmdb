__int64 __fastcall sub_141578930(__int64 a1, int a2, __int64 **a3)
{
  unsigned __int64 v5; // rdi
  __int64 v6; // rax
  __int64 *v7; // rax
  unsigned __int64 v8; // rcx
  char v9; // bl
  __int64 *v10; // rax
  unsigned __int64 v11; // rcx
  __int64 v12; // rcx
  int v13; // eax
  int v14; // ecx
  __int64 *v15; // rax
  unsigned __int64 v16; // rcx
  char v17; // bl
  __int64 *v18; // rax
  unsigned __int64 v19; // rcx
  char v20; // bl
  __int64 *v21; // rax
  unsigned __int64 v22; // rcx
  __int64 *v23; // rax
  unsigned __int64 v24; // rcx
  unsigned __int64 v25; // rdi
  __int64 *v26; // rax
  unsigned __int64 v27; // rcx
  unsigned __int64 v28; // rdi
  __int64 *v29; // rax
  unsigned __int64 v30; // rcx
  unsigned __int64 v31; // rdi
  __int64 *v32; // rax
  unsigned __int64 v33; // rcx
  unsigned __int64 v34; // rcx
  int v35; // eax
  __int64 v36; // rbx
  __int64 *v37; // rcx
  __int64 *v38; // rax
  unsigned __int64 v39; // rcx
  __int64 *v40; // rax
  unsigned __int64 v41; // rcx
  char v42; // bl
  __int64 *v43; // rax
  unsigned __int64 v44; // rcx
  __int64 v45; // rcx
  __int64 *v46; // rcx
  __int64 *v47; // rax
  unsigned __int64 v48; // rcx
  __int64 v49; // rdx
  __int64 *v50; // rax
  unsigned __int64 v51; // rcx
  __int64 *v52; // rax
  unsigned __int64 v53; // rcx
  unsigned __int64 v54; // rdi
  __int64 *v55; // rax
  unsigned __int64 v56; // rcx
  __int64 *v57; // rax
  unsigned __int64 v58; // rcx
  __int64 *v59; // rax
  unsigned __int64 v60; // rcx
  __int64 *v61; // rax
  unsigned __int64 v62; // rcx
  __int64 *v63; // rbx
  __int64 v64; // rdx
  __int64 v65; // rbx
  __int64 v66; // rdx
  int v67; // ecx
  __int64 *v69; // [rsp+20h] [rbp-10h] BYREF
  unsigned __int64 v70; // [rsp+28h] [rbp-8h]
  __int64 v71; // [rsp+30h] [rbp+0h]

  v71 = -2;
  LODWORD(v5) = 0;
  if ( a2 > 1347184235 )
  {
    if ( a2 > 1347186758 )
    {
      if ( a2 > 1347188578 )
      {
        if ( a2 == 1347188579 )
        {
          LODWORD(v5) = *(unsigned __int16 *)(a1 + 100);
          if ( (v5 & 0x8000u) == 0LL )
          {
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v70) = v5;
            v69 = (__int64 *)v6;
            if ( &v69 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v57 = v69;
              v58 = v70;
              a3[1] = (__int64 *)v70;
              *a3 = v57;
              v6 = sub_14083D4F0(v58) + 8;
              v70 = 0;
              v69 = (__int64 *)v6;
            }
            goto LABEL_104;
          }
          goto LABEL_105;
        }
        if ( a2 == 1348887138 )
        {
          LODWORD(v5) = *(_DWORD *)(a1 + 92);
          if ( (_DWORD)v5 != 0 )
          {
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v70) = v5;
            v69 = (__int64 *)v6;
            if ( &v69 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v59 = v69;
              v60 = v70;
              a3[1] = (__int64 *)v70;
              *a3 = v59;
              v6 = sub_14083D4F0(v60) + 8;
              v70 = 0;
              v69 = (__int64 *)v6;
            }
            goto LABEL_104;
          }
          goto LABEL_105;
        }
        if ( a2 != 1886157170 )
          return (unsigned int)v5;
        sub_140FE7F20(*(_QWORD *)(a1 + 24), a3);
      }
      else
      {
        if ( a2 != 1347186759 )
        {
          if ( a2 == 1347187556 )
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
            LODWORD(v70) = ((*(_WORD *)(a1 + 48) & 0x1FF) << 8)
                         | (*(unsigned __int16 *)(a1 + 48) >> 9)
                         | (*(unsigned __int16 *)(a1 + 50) << 17);
            v46 = &qword_141B5C8A0;
            v69 = &qword_141B5C8A0;
            if ( &v69 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v47 = v69;
              v48 = v70;
              a3[1] = (__int64 *)v70;
              *a3 = v47;
              v46 = (__int64 *)(sub_14083D4F0(v48) + 8);
              v70 = 0;
              v69 = v46;
            }
LABEL_82:
            (*(void (__fastcall **)(__int64 *, __int64 **))(*v46 + 16))(v46, &v69);
            goto LABEL_122;
          }
          if ( a2 != 1347187566 )
            return (unsigned int)v5;
          LODWORD(v5) = *(unsigned __int8 *)(a1 + 102);
          if ( (char)v5 > 0 )
          {
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v70) = v5;
            v69 = (__int64 *)v6;
            if ( &v69 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v15 = v69;
              v16 = v70;
              a3[1] = (__int64 *)v70;
              *a3 = v15;
              v6 = sub_14083D4F0(v16) + 8;
              v70 = 0;
              v69 = (__int64 *)v6;
            }
            goto LABEL_104;
          }
          goto LABEL_105;
        }
        if ( (unsigned __int8)sub_1400015B0() == 0 )
        {
          LODWORD(v5) = 0;
          return (unsigned int)v5;
        }
        LODWORD(v5) = *(_DWORD *)(a1 + 96);
        if ( (v5 & 0x80000000) != 0LL )
          goto LABEL_105;
        LODWORD(v70) = *(_DWORD *)(a1 + 96);
        v69 = (__int64 *)(sub_14083D4F0(v45) + 40);
        v5 = (unsigned __int64)&v69;
        sub_14083DFA0(a3, &v69);
        (*(void (__fastcall **)(__int64 *, __int64 **))(*v69 + 16))(v69, &v69);
      }
LABEL_122:
      LOBYTE(v5) = 1;
      return (unsigned int)v5;
    }
    if ( a2 <= 1347186021 )
    {
      switch ( a2 )
      {
        case 1347184236:
          v5 = *(_QWORD *)(a1 + 72) & 0x40000600LL;
          v6 = sub_14083D4F0(a1) + 88;
          v70 = v5;
          v69 = (__int64 *)v6;
          if ( &v69 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v40 = v69;
            v41 = v70;
            a3[1] = (__int64 *)v70;
            *a3 = v40;
            v6 = sub_14083D4F0(v41) + 8;
            v70 = 0;
            v69 = (__int64 *)v6;
          }
          goto LABEL_104;
        case 1347184995:
          v42 = *(_BYTE *)(a1 + 72);
          v6 = sub_14083D4F0(a1) + 24;
          LOBYTE(v70) = (v42 & 2) != 0;
          v69 = (__int64 *)v6;
          if ( &v69 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v43 = v69;
            v44 = v70;
            a3[1] = (__int64 *)v70;
            *a3 = v43;
            v6 = sub_14083D4F0(v44) + 8;
            v70 = 0;
            v69 = (__int64 *)v6;
          }
          goto LABEL_104;
        case 1347186019:
          v9 = *(_BYTE *)(a1 + 74);
          v6 = sub_14083D4F0(a1) + 24;
          LOBYTE(v70) = v9 & 1;
          v69 = (__int64 *)v6;
          if ( &v69 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v10 = v69;
            v11 = v70;
            a3[1] = (__int64 *)v70;
            *a3 = v10;
            v6 = sub_14083D4F0(v11) + 8;
            v70 = 0;
            v69 = (__int64 *)v6;
          }
          goto LABEL_104;
        default:
          break;
      }
      return (unsigned int)v5;
    }
    if ( a2 != 1347186022 )
    {
      if ( a2 == 1347186530 )
      {
        v54 = *(_QWORD *)(a1 + 72);
        v6 = sub_14083D4F0(a1) + 24;
        v5 = v54 >> 15;
        LOBYTE(v70) = v5 & 1;
        v69 = (__int64 *)v6;
        if ( &v69 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v55 = v69;
          v56 = v70;
          a3[1] = (__int64 *)v70;
          *a3 = v55;
          v6 = sub_14083D4F0(v56) + 8;
          v70 = 0;
          v69 = (__int64 *)v6;
        }
        goto LABEL_104;
      }
      if ( a2 == 1347186531 )
      {
        v20 = *(_BYTE *)(a1 + 72);
        v6 = sub_14083D4F0(a1) + 24;
        LOBYTE(v70) = v20 & 1;
        v69 = (__int64 *)v6;
        if ( &v69 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v21 = v69;
          v22 = v70;
          a3[1] = (__int64 *)v70;
          *a3 = v21;
          v6 = sub_14083D4F0(v22) + 8;
          v70 = 0;
          v69 = (__int64 *)v6;
        }
        goto LABEL_104;
      }
      return (unsigned int)v5;
    }
    LODWORD(v5) = *(_DWORD *)(a1 + 84);
    if ( (_DWORD)v5 != 0 )
    {
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v70) = v5;
      v69 = (__int64 *)v6;
      if ( &v69 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v52 = v69;
        v53 = v70;
        a3[1] = (__int64 *)v70;
        *a3 = v52;
        v6 = sub_14083D4F0(v53) + 8;
        v70 = 0;
        v69 = (__int64 *)v6;
      }
      goto LABEL_104;
    }
LABEL_105:
    LOBYTE(v5) = 1;
    if ( a3 != (__int64 **)&qword_141B5A4A0 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
    }
    return (unsigned int)v5;
  }
  if ( a2 > 1347183467 )
  {
    switch ( a2 )
    {
      case 1347183468:
        v12 = *(_QWORD *)(a1 + 32);
        if ( v12 != 0 )
          goto LABEL_20;
        goto LABEL_84;
      case 1347183469:
        v25 = *(_QWORD *)(a1 + 72);
        v6 = sub_14083D4F0(a1) + 24;
        v5 = v25 >> 20;
        LOBYTE(v70) = v5 & 1;
        v69 = (__int64 *)v6;
        if ( &v69 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v26 = v69;
          v27 = v70;
          a3[1] = (__int64 *)v70;
          *a3 = v26;
          v6 = sub_14083D4F0(v27) + 8;
          v70 = 0;
          v69 = (__int64 *)v6;
        }
        goto LABEL_104;
      case 1347183470:
      case 1347183471:
      case 1347183472:
      case 1347183473:
      case 1347183475:
        return (unsigned int)v5;
      case 1347183474:
        v28 = *(_QWORD *)(a1 + 72);
        v6 = sub_14083D4F0(a1) + 24;
        v5 = v28 >> 13;
        LOBYTE(v70) = v5 & 1;
        v69 = (__int64 *)v6;
        if ( &v69 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v29 = v69;
          v30 = v70;
          a3[1] = (__int64 *)v70;
          *a3 = v29;
          v6 = sub_14083D4F0(v30) + 8;
          v70 = 0;
          v69 = (__int64 *)v6;
        }
        goto LABEL_104;
      case 1347183476:
        v31 = *(_QWORD *)(a1 + 72);
        v6 = sub_14083D4F0(a1) + 24;
        v5 = v31 >> 12;
        LOBYTE(v70) = v5 & 1;
        v69 = (__int64 *)v6;
        if ( &v69 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v32 = v69;
          v33 = v70;
          a3[1] = (__int64 *)v70;
          *a3 = v32;
          v6 = sub_14083D4F0(v33) + 8;
          v70 = 0;
          v69 = (__int64 *)v6;
        }
        goto LABEL_104;
      default:
        if ( a2 == 1347183972 )
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
          LODWORD(v70) = ((*(_WORD *)(a1 + 52) & 0x1FF) << 8)
                       | (*(unsigned __int16 *)(a1 + 52) >> 9)
                       | (*(unsigned __int16 *)(a1 + 54) << 17);
          v46 = &qword_141B5C8A0;
          v69 = &qword_141B5C8A0;
          if ( &v69 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v61 = v69;
            v62 = v70;
            a3[1] = (__int64 *)v70;
            *a3 = v61;
            v46 = (__int64 *)(sub_14083D4F0(v62) + 8);
            v70 = 0;
            v69 = v46;
          }
          goto LABEL_82;
        }
        if ( a2 != 1347184226 )
          return (unsigned int)v5;
        LODWORD(v5) = *(_DWORD *)(a1 + 88);
        if ( (_DWORD)v5 != 0 )
        {
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v70) = v5;
          v69 = (__int64 *)v6;
          if ( &v69 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v23 = v69;
            v24 = v70;
            a3[1] = (__int64 *)v70;
            *a3 = v23;
            v6 = sub_14083D4F0(v24) + 8;
            v70 = 0;
            v69 = (__int64 *)v6;
          }
          goto LABEL_104;
        }
        break;
    }
    goto LABEL_105;
  }
  if ( a2 > 1347176043 )
  {
    if ( a2 == 1347176044 )
    {
      v12 = *(_QWORD *)(a1 + 40);
      if ( v12 != 0 )
      {
LABEL_20:
        v13 = *(_DWORD *)(v12 + 12);
        v14 = *(_DWORD *)(v12 + 16);
        if ( v14 == 0 )
          v14 = v13;
      }
      else
      {
LABEL_84:
        v13 = -1;
        v14 = -1;
      }
      v69 = (__int64 *)__PAIR64__(v14, v13);
      v49 = 1416914273;
      goto LABEL_121;
    }
    if ( a2 != 1347178055 )
    {
      if ( a2 == 1347183218 )
      {
        v17 = *(_BYTE *)(a1 + 72);
        v6 = sub_14083D4F0(a1) + 24;
        LOBYTE(v70) = (v17 & 4) != 0;
        v69 = (__int64 *)v6;
        if ( &v69 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v18 = v69;
          v19 = v70;
          a3[1] = (__int64 *)v70;
          *a3 = v18;
          v6 = sub_14083D4F0(v19) + 8;
          v70 = 0;
          v69 = (__int64 *)v6;
        }
        goto LABEL_104;
      }
      return (unsigned int)v5;
    }
    LODWORD(v5) = *(char *)(a1 + 103);
    if ( (_DWORD)v5 != -1 )
    {
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v70) = v5;
      v69 = (__int64 *)v6;
      if ( &v69 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v50 = v69;
        v51 = v70;
        a3[1] = (__int64 *)v70;
        *a3 = v50;
        v6 = sub_14083D4F0(v51) + 8;
        v70 = 0;
        v69 = (__int64 *)v6;
      }
      goto LABEL_104;
    }
    goto LABEL_105;
  }
  switch ( a2 )
  {
    case 1347174723:
      v34 = *(unsigned int *)(a1 + 56);
      v35 = -1;
      if ( (v34 & 0x80000000) == 0LL && qword_141B5FDC0 != 0 )
      {
        if ( (_BYTE)word_141B60320 == 0 )
        {
          v36 = *(_QWORD *)(qword_141B5FDC0 + 96);
          v5 = (*(_QWORD *)(qword_141B5FDC0 + 104) - v36) >> 3;
          if ( v5 > v34 )
          {
            v37 = (__int64 *)(v36 + 8 * v34);
LABEL_115:
            v66 = *v37;
            v67 = -1;
            if ( v66 != 0 )
            {
              v35 = *(_DWORD *)(v66 + 12);
              v67 = *(_DWORD *)(v66 + 16);
              if ( v67 == 0 )
                v67 = *(_DWORD *)(v66 + 12);
            }
            goto LABEL_120;
          }
        }
        v63 = *(__int64 **)(qword_141B5FDC0 + 128);
        v64 = *v63;
        v65 = v63[1] - *v63;
        if ( v65 != 0 && v65 >> 3 > (unsigned __int64)(unsigned int)v34 )
        {
          v37 = (__int64 *)(v64 + 8LL * (unsigned int)v34);
          goto LABEL_115;
        }
      }
      v67 = -1;
LABEL_120:
      v69 = (__int64 *)__PAIR64__(v67, v35);
      v49 = 1668246896;
LABEL_121:
      sub_140FE72B0(&v69, v49, a3);
      goto LABEL_122;
    case 1347174739:
      LODWORD(v5) = *(_DWORD *)(a1 + 60);
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v70) = v5;
      v69 = (__int64 *)v6;
      if ( &v69 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v38 = v69;
        v39 = v70;
        a3[1] = (__int64 *)v70;
        *a3 = v38;
        v6 = sub_14083D4F0(v39) + 8;
        v70 = 0;
        v69 = (__int64 *)v6;
      }
      goto LABEL_104;
    case 1347174740:
      LODWORD(v5) = *(char *)(a1 + 68);
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v70) = v5;
      v69 = (__int64 *)v6;
      if ( &v69 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v7 = v69;
        v8 = v70;
        a3[1] = (__int64 *)v70;
        *a3 = v7;
        v6 = sub_14083D4F0(v8) + 8;
        v70 = 0;
        v69 = (__int64 *)v6;
      }
LABEL_104:
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v69);
      goto LABEL_122;
    default:
      break;
  }
  return (unsigned int)v5;
}
