char __fastcall sub_1415446A0(__int64 a1, int a2, __int64 *a3)
{
  unsigned __int64 v5; // rdi
  __int64 v6; // rax
  __int64 *v7; // rax
  __int64 v8; // rcx
  int v9; // edi
  __int64 *v10; // rax
  __int64 v11; // rcx
  int v12; // ebx
  __int64 v13; // rax
  __int64 *v14; // rax
  __int64 v15; // rcx
  unsigned __int64 v16; // rdi
  __int64 *v17; // rax
  __int64 v18; // rcx
  int v19; // ebx
  __int64 v20; // rax
  __int64 *v21; // rax
  __int64 v22; // rcx
  int v23; // ebx
  __int64 v24; // rax
  __int64 *v25; // rax
  __int64 v26; // rcx
  int v27; // edi
  __int64 *v28; // rax
  __int64 v29; // rcx
  __int64 *v30; // rcx
  __int64 *v31; // rax
  __int64 v32; // rcx
  int v33; // eax
  int v34; // edi
  __int64 *v35; // rax
  __int64 v36; // rcx
  int v37; // edi
  __int64 *v38; // rax
  __int64 v39; // rcx
  char v40; // bl
  __int64 *v41; // rax
  __int64 v42; // rcx
  unsigned __int64 v43; // rdi
  __int64 *v44; // rax
  __int64 v45; // rcx
  int v46; // edi
  __int64 *v47; // rax
  __int64 v48; // rcx
  int v49; // edi
  __int64 *v50; // rax
  __int64 v51; // rcx
  unsigned __int64 v52; // rdi
  __int64 *v53; // rax
  __int64 v54; // rcx
  __int64 *v55; // rdi
  __int64 v56; // rax
  __int64 v57; // rcx
  __int64 *v58; // rax
  __int64 v59; // rcx
  int v60; // edi
  __int64 *v61; // rax
  __int64 v62; // rcx
  __int64 *v63; // rcx
  __int64 *v64; // rax
  __int64 v65; // rcx
  __int64 *v66; // rcx
  __int64 *v67; // rax
  __int64 v68; // rcx
  __int64 *v70; // [rsp+20h] [rbp-10h] BYREF
  _QWORD v71[5]; // [rsp+28h] [rbp-8h] BYREF

  v71[1] = -2;
  if ( a2 > 1768842862 )
  {
    if ( a2 <= 1937007713 )
    {
      if ( a2 > 1869899891 )
      {
        switch ( a2 )
        {
          case 1869899892:
            v43 = ((unsigned __int64)*(unsigned int *)(a1 + 44) << 32) | *(int *)(a1 + 40);
            v6 = sub_14083D4F0(a1) + 72;
            v71[0] = v43;
            v70 = (__int64 *)v6;
            if ( &v70 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v44 = v70;
              v45 = v71[0];
              a3[1] = v71[0];
              *a3 = (__int64)v44;
              v6 = sub_14083D4F0(v45) + 8;
              v71[0] = 0;
              v70 = (__int64 *)v6;
            }
            goto LABEL_88;
          case 1918989417:
            v46 = *(char *)(a1 + 90);
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v71[0]) = v46;
            v70 = (__int64 *)v6;
            if ( &v70 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v47 = v70;
              v48 = v71[0];
              a3[1] = v71[0];
              *a3 = (__int64)v47;
              v6 = sub_14083D4F0(v48) + 8;
              v71[0] = 0;
              v70 = (__int64 *)v6;
            }
            goto LABEL_88;
          case 1920099681:
            v9 = *(char *)(a1 + 92);
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v71[0]) = v9;
            v70 = (__int64 *)v6;
            if ( &v70 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              v10 = v70;
              v11 = v71[0];
              a3[1] = v71[0];
              *a3 = (__int64)v10;
              v6 = sub_14083D4F0(v11) + 8;
              v71[0] = 0;
              v70 = (__int64 *)v6;
            }
            goto LABEL_88;
          default:
            break;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      if ( a2 == 1768842863 )
      {
        v60 = *(char *)(a1 + 91);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v71[0]) = v60;
        v70 = (__int64 *)v6;
        if ( &v70 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v61 = v70;
          v62 = v71[0];
          a3[1] = v71[0];
          *a3 = (__int64)v61;
          v6 = sub_14083D4F0(v62) + 8;
          v71[0] = 0;
          v70 = (__int64 *)v6;
        }
        goto LABEL_88;
      }
      if ( a2 != 1869048947 )
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      v23 = *(__int16 *)(a1 + 88);
      v24 = sub_14083D4F0(a1) + 40;
      LODWORD(v71[0]) = v23;
      v70 = (__int64 *)v24;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v25 = v70;
        v26 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v25;
        v24 = sub_14083D4F0(v26) + 8;
        v71[0] = 0;
        v70 = (__int64 *)v24;
      }
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v24 + 16LL))(v24, &v70);
      if ( a3 == &qword_141B5A4A0 || *(__int16 *)(a1 + 88) >= 0 )
        return 1;
      goto LABEL_99;
    }
    if ( a2 > 1937008995 )
    {
      switch ( a2 )
      {
        case 1952801133:
          v52 = ((unsigned __int64)*(unsigned int *)(a1 + 36) << 32) | *(int *)(a1 + 32);
          v6 = sub_14083D4F0(a1) + 72;
          v71[0] = v52;
          v70 = (__int64 *)v6;
          if ( &v70 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v53 = v70;
            v54 = v71[0];
            a3[1] = v71[0];
            *a3 = (__int64)v53;
            v6 = sub_14083D4F0(v54) + 8;
            v71[0] = 0;
            v70 = (__int64 *)v6;
          }
          goto LABEL_88;
        case 1937010285:
          v55 = (__int64 *)(a1 + 56);
          v56 = sub_14083D4F0(a1);
          v71[0] = 0;
          if ( v71 != v55 )
          {
            v57 = *v55;
            if ( *v55 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v57 - 4));
            v71[0] = v57;
          }
          v6 = v56 + 136;
          v70 = (__int64 *)v6;
          if ( &v70 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v58 = v70;
            v59 = v71[0];
            a3[1] = v71[0];
            *a3 = (__int64)v58;
            v6 = sub_14083D4F0(v59) + 8;
            v71[0] = 0;
            v70 = (__int64 *)v6;
          }
          goto LABEL_88;
        case 1937008996:
          v16 = ((unsigned __int64)*(unsigned int *)(a1 + 28) << 32) | *(int *)(a1 + 24);
          v6 = sub_14083D4F0(a1) + 72;
          v71[0] = v16;
          v70 = (__int64 *)v6;
          if ( &v70 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v17 = v70;
            v18 = v71[0];
            a3[1] = v71[0];
            *a3 = (__int64)v17;
            v6 = sub_14083D4F0(v18) + 8;
            v71[0] = 0;
            v70 = (__int64 *)v6;
          }
          goto LABEL_88;
        default:
          break;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 == 1937007714 )
    {
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
      LODWORD(v71[0]) = ((*(_WORD *)(a1 + 72) & 0x1FF) << 8)
                      | (*(unsigned __int16 *)(a1 + 72) >> 9)
                      | (*(unsigned __int16 *)(a1 + 74) << 17);
      v66 = &qword_141B5C8A0;
      v70 = &qword_141B5C8A0;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v67 = v70;
        v68 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v67;
        v66 = (__int64 *)(sub_14083D4F0(v68) + 8);
        v71[0] = 0;
        v70 = v66;
      }
      (*(void (__fastcall **)(__int64 *, __int64 **))(*v66 + 16))(v66, &v70);
      return 1;
    }
    if ( a2 != 1937007732 )
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
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
    LODWORD(v71[0]) = ((*(_WORD *)(a1 + 64) & 0x1FF) << 8)
                    | (*(unsigned __int16 *)(a1 + 64) >> 9)
                    | (*(unsigned __int16 *)(a1 + 66) << 17);
    v30 = &qword_141B5C8A0;
    v70 = &qword_141B5C8A0;
    if ( &v70 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v31 = v70;
      v32 = v71[0];
      a3[1] = v71[0];
      *a3 = (__int64)v31;
      v30 = (__int64 *)(sub_14083D4F0(v32) + 8);
      v71[0] = 0;
      v70 = v30;
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v30 + 16))(v30, &v70);
    if ( a3 == &qword_141B5A4A0 || (*(_WORD *)(a1 + 64) & 0x1FF) != 1 )
      return 1;
    v33 = *(unsigned __int16 *)(a1 + 66);
LABEL_98:
    if ( v33 != 1900 )
      return 1;
    goto LABEL_99;
  }
  if ( a2 > 1701733491 )
  {
    if ( a2 > 1718839155 )
    {
      if ( a2 == 1718839156 )
      {
        v49 = *(__int16 *)(a1 + 88);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v71[0]) = v49;
        v70 = (__int64 *)v6;
        if ( &v70 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v50 = v70;
          v51 = v71[0];
          a3[1] = v71[0];
          *a3 = (__int64)v50;
          v6 = sub_14083D4F0(v51) + 8;
          v71[0] = 0;
          v70 = (__int64 *)v6;
        }
        goto LABEL_88;
      }
      if ( a2 == 1734438259 )
        goto LABEL_61;
      if ( a2 != 1735355507 )
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      v12 = *(__int16 *)(a1 + 86);
      v13 = sub_14083D4F0(a1) + 40;
      LODWORD(v71[0]) = v12;
      v70 = (__int64 *)v13;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v14 = v70;
        v15 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v14;
        v13 = sub_14083D4F0(v15) + 8;
        v71[0] = 0;
        v70 = (__int64 *)v13;
      }
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v13 + 16LL))(v13, &v70);
      if ( a3 == &qword_141B5A4A0 || *(__int16 *)(a1 + 86) >= 0 )
        return 1;
LABEL_99:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      (*(void (__fastcall **)(__int64, __int64 *, __int64 *))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
        qword_141B5A4A0,
        &qword_141B5A4A0,
        a3);
      return 1;
    }
    if ( a2 != 1701733492 )
    {
      if ( a2 == 1702127982 )
      {
        v27 = *(char *)(a1 + 93);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v71[0]) = v27;
        v70 = (__int64 *)v6;
        if ( &v70 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v28 = v70;
          v29 = v71[0];
          a3[1] = v71[0];
          *a3 = (__int64)v28;
          v6 = sub_14083D4F0(v29) + 8;
          v71[0] = 0;
          v70 = (__int64 *)v6;
        }
        goto LABEL_88;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
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
    LODWORD(v71[0]) = ((*(_WORD *)(a1 + 68) & 0x1FF) << 8)
                    | (*(unsigned __int16 *)(a1 + 68) >> 9)
                    | (*(unsigned __int16 *)(a1 + 70) << 17);
    v63 = &qword_141B5C8A0;
    v70 = &qword_141B5C8A0;
    if ( &v70 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v64 = v70;
      v65 = v71[0];
      a3[1] = v71[0];
      *a3 = (__int64)v64;
      v63 = (__int64 *)(sub_14083D4F0(v65) + 8);
      v71[0] = 0;
      v70 = v63;
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v63 + 16))(v63, &v70);
    if ( a3 == &qword_141B5A4A0 || (*(_WORD *)(a1 + 68) & 0x1FF) != 1 )
      return 1;
    v33 = *(unsigned __int16 *)(a1 + 70);
    goto LABEL_98;
  }
  if ( a2 <= 1667330919 )
  {
    if ( a2 != 1634758771 )
    {
      if ( a2 != 1635021925 )
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      v19 = *(_DWORD *)(a1 + 80);
      v20 = sub_14083D4F0(a1) + 40;
      LODWORD(v71[0]) = v19;
      v70 = (__int64 *)v20;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v21 = v70;
        v22 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v21;
        v20 = sub_14083D4F0(v22) + 8;
        v71[0] = 0;
        v70 = (__int64 *)v20;
      }
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v20 + 16LL))(v20, &v70);
      if ( a3 == &qword_141B5A4A0 || *(_DWORD *)(a1 + 80) != -1 )
        return 1;
      goto LABEL_99;
    }
LABEL_61:
    v34 = *(__int16 *)(a1 + 84);
    v6 = sub_14083D4F0(a1) + 40;
    LODWORD(v71[0]) = v34;
    v70 = (__int64 *)v6;
    if ( &v70 != (__int64 **)a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v35 = v70;
      v36 = v71[0];
      a3[1] = v71[0];
      *a3 = (__int64)v35;
      v6 = sub_14083D4F0(v36) + 8;
      v71[0] = 0;
      v70 = (__int64 *)v6;
    }
    goto LABEL_88;
  }
  switch ( a2 )
  {
    case 1667330920:
      v37 = *(_DWORD *)(a1 + 80);
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v71[0]) = v37;
      v70 = (__int64 *)v6;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v38 = v70;
        v39 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v38;
        v6 = sub_14083D4F0(v39) + 8;
        v71[0] = 0;
        v70 = (__int64 *)v6;
      }
      goto LABEL_88;
    case 1668182900:
      v40 = *(_BYTE *)(a1 + 93);
      v6 = sub_14083D4F0(a1) + 24;
      LOBYTE(v71[0]) = v40 == 1;
      v70 = (__int64 *)v6;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v41 = v70;
        v42 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v41;
        v6 = sub_14083D4F0(v42) + 8;
        v71[0] = 0;
        v70 = (__int64 *)v6;
      }
      goto LABEL_88;
    case 1668246896:
      v5 = ((unsigned __int64)*(unsigned int *)(a1 + 52) << 32) | *(int *)(a1 + 48);
      v6 = sub_14083D4F0(a1) + 72;
      v71[0] = v5;
      v70 = (__int64 *)v6;
      if ( &v70 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v7 = v70;
        v8 = v71[0];
        a3[1] = v71[0];
        *a3 = (__int64)v7;
        v6 = sub_14083D4F0(v8) + 8;
        v71[0] = 0;
        v70 = (__int64 *)v6;
      }
LABEL_88:
      (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v70);
      return 1;
    default:
      break;
  }
  return sub_140FE3F20((_DWORD *)a1, a2, a3);
}
