__int64 __fastcall sub_1415398E0(__int64 a1, int a2, __int64 **a3)
{
  unsigned int v5; // edi
  __int64 v6; // rax
  __int64 *v7; // rax
  __int64 *v8; // rcx
  __int64 *v9; // rax
  __int64 *v10; // rcx
  __int64 *v11; // rax
  __int64 *v12; // rcx
  __int64 *v13; // rax
  __int64 *v14; // rcx
  __int64 *v15; // rax
  __int64 *v16; // rcx
  __int64 *v17; // rax
  __int64 *v18; // rcx
  __int64 v19; // rcx
  int v20; // eax
  int v21; // ecx
  __int64 *v22; // rax
  __int64 *v23; // rcx
  __int64 *v24; // rax
  __int64 *v25; // rcx
  __int64 v26; // rcx
  __int64 *v27; // rax
  __int64 *v28; // rcx
  __int64 *v29; // rax
  __int64 *v30; // rcx
  int v31; // eax
  int v32; // ecx
  __int64 *v33; // rax
  __int64 *v34; // rcx
  char v35; // bl
  __int64 *v36; // rax
  __int64 *v37; // rcx
  __int64 *v38; // rcx
  __int64 *v39; // rax
  __int64 *v40; // rcx
  __int64 *v41; // rax
  __int64 *v42; // rcx
  __int64 *v43; // rax
  __int64 *v44; // rcx
  __int64 v45; // rdx
  __int64 *v46; // rax
  __int64 *v47; // rcx
  __int64 *v48; // rax
  __int64 *v49; // rcx
  __int64 *v51; // [rsp+20h] [rbp-10h] BYREF
  __int64 *v52; // [rsp+28h] [rbp-8h]
  __int64 v53; // [rsp+30h] [rbp+0h]

  v53 = -2;
  v5 = 0;
  if ( a2 <= 1399614819 )
  {
    if ( a2 <= 1399022945 )
    {
      if ( a2 > 1399019851 )
      {
        switch ( a2 )
        {
          case 1399019852:
            v5 = *(char *)(a1 + 104);
            if ( v5 != -1 )
            {
              v6 = sub_14083D4F0(a1) + 40;
              LODWORD(v52) = v5;
              v51 = (__int64 *)v6;
              if ( &v51 != a3 )
              {
                (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
                v27 = v51;
                v28 = v52;
                a3[1] = v52;
                *a3 = v27;
                v6 = sub_14083D4F0(v28) + 8;
                v52 = nullptr;
                v51 = (__int64 *)v6;
              }
              goto LABEL_108;
            }
            break;
          case 1399021933:
            v5 = *(_DWORD *)(a1 + 96);
            if ( v5 != -1 )
            {
              v6 = sub_14083D4F0(a1) + 40;
              LODWORD(v52) = v5;
              v51 = (__int64 *)v6;
              if ( &v51 != a3 )
              {
                (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
                v29 = v51;
                v30 = v52;
                a3[1] = v52;
                *a3 = v29;
                v6 = sub_14083D4F0(v30) + 8;
                v52 = nullptr;
                v51 = (__int64 *)v6;
              }
              goto LABEL_108;
            }
            break;
          case 1399021936:
            v5 = *(_DWORD *)(a1 + 60);
            if ( v5 != -1 )
            {
              v6 = sub_14083D4F0(a1) + 40;
              LODWORD(v52) = v5;
              v51 = (__int64 *)v6;
              if ( &v51 != a3 )
              {
                (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
                v9 = v51;
                v10 = v52;
                a3[1] = v52;
                *a3 = v9;
                v6 = sub_14083D4F0(v10) + 8;
                v52 = nullptr;
                v51 = (__int64 *)v6;
              }
              goto LABEL_108;
            }
            break;
          default:
            return v5;
        }
        goto LABEL_109;
      }
      if ( a2 != 1398893684 )
      {
        if ( a2 != 1399018572 )
          return v5;
        v5 = *(char *)(a1 + 103);
        if ( v5 != -1 )
        {
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v52) = v5;
          v51 = (__int64 *)v6;
          if ( &v51 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v17 = v51;
            v18 = v52;
            a3[1] = v52;
            *a3 = v17;
            v6 = sub_14083D4F0(v18) + 8;
            v52 = nullptr;
            v51 = (__int64 *)v6;
          }
          goto LABEL_108;
        }
        goto LABEL_109;
      }
      v26 = *(_QWORD *)(a1 + 72);
      if ( v26 == 0 )
        goto LABEL_99;
      goto LABEL_76;
    }
    if ( a2 <= 1399025772 )
    {
      if ( a2 == 1399022946 )
      {
        v5 = *(_DWORD *)(a1 + 68);
        if ( v5 != -1 )
        {
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v52) = v5;
          v51 = (__int64 *)v6;
          if ( &v51 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v48 = v51;
            v49 = v52;
            a3[1] = v52;
            *a3 = v48;
            v6 = sub_14083D4F0(v49) + 8;
            v52 = nullptr;
            v51 = (__int64 *)v6;
          }
          goto LABEL_108;
        }
      }
      else
      {
        if ( a2 != 1399025267 )
          return v5;
        v5 = *(char *)(a1 + 105);
        if ( v5 != -1 )
        {
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v52) = v5;
          v51 = (__int64 *)v6;
          if ( &v51 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v22 = v51;
            v23 = v52;
            a3[1] = v52;
            *a3 = v22;
            v6 = sub_14083D4F0(v23) + 8;
            v52 = nullptr;
            v51 = (__int64 *)v6;
          }
          goto LABEL_108;
        }
      }
      goto LABEL_109;
    }
    if ( a2 == 1399025773 )
    {
      v35 = *(_BYTE *)(a1 + 101);
      v6 = sub_14083D4F0(a1) + 24;
      LOBYTE(v52) = (v35 & 4) != 0;
      v51 = (__int64 *)v6;
      if ( &v51 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v36 = v51;
        v37 = v52;
        a3[1] = v52;
        *a3 = v36;
        v6 = sub_14083D4F0(v37) + 8;
        v52 = nullptr;
        v51 = (__int64 *)v6;
      }
      goto LABEL_108;
    }
    if ( a2 != 1399612769 )
    {
      if ( a2 != 1399613549 )
        return v5;
      v5 = *(char *)(a1 + 102);
      if ( v5 != -1 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v52) = v5;
        v51 = (__int64 *)v6;
        if ( &v51 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v13 = v51;
          v14 = v52;
          a3[1] = v52;
          *a3 = v13;
          v6 = sub_14083D4F0(v14) + 8;
          v52 = nullptr;
          v51 = (__int64 *)v6;
        }
        goto LABEL_108;
      }
      goto LABEL_109;
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
    LODWORD(v52) = ((*(_WORD *)(a1 + 48) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 48) >> 9)
                 | (*(unsigned __int16 *)(a1 + 50) << 17);
    v38 = &qword_141B5C8A0;
    v51 = &qword_141B5C8A0;
    if ( &v51 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v39 = v51;
      v40 = v52;
      a3[1] = v52;
      *a3 = v39;
      v38 = (__int64 *)(sub_14083D4F0(v40) + 8);
      v52 = nullptr;
      v51 = v38;
    }
    goto LABEL_104;
  }
  if ( a2 <= 1399748704 )
  {
    if ( a2 > 1399743862 )
    {
      if ( a2 != 1399743863 )
      {
        if ( a2 == 1399745902 )
        {
          v5 = *(_DWORD *)(a1 + 84);
          if ( v5 != -1 )
          {
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v52) = v5;
            v51 = (__int64 *)v6;
            if ( &v51 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v33 = v51;
              v34 = v52;
              a3[1] = v52;
              *a3 = v33;
              v6 = sub_14083D4F0(v34) + 8;
              v52 = nullptr;
              v51 = (__int64 *)v6;
            }
            goto LABEL_108;
          }
        }
        else
        {
          if ( a2 != 1399745912 )
            return v5;
          v5 = *(_DWORD *)(a1 + 88);
          if ( v5 != -1 )
          {
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v52) = v5;
            v51 = (__int64 *)v6;
            if ( &v51 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v11 = v51;
              v12 = v52;
              a3[1] = v52;
              *a3 = v11;
              v6 = sub_14083D4F0(v12) + 8;
              v52 = nullptr;
              v51 = (__int64 *)v6;
            }
            goto LABEL_108;
          }
        }
        goto LABEL_109;
      }
      v26 = *(_QWORD *)(a1 + 40);
      if ( v26 == 0 )
        goto LABEL_99;
      goto LABEL_76;
    }
    if ( a2 != 1399614820 )
    {
      if ( a2 != 1399680884 )
        return v5;
      v19 = *(_QWORD *)(a1 + 24);
      if ( v19 != 0 )
      {
        v20 = *(_DWORD *)(v19 + 12);
        v21 = *(_DWORD *)(v19 + 16);
        if ( v21 == 0 )
          v21 = v20;
      }
      else
      {
        v20 = -1;
        v21 = -1;
      }
      v51 = (__int64 *)__PAIR64__(v21, v20);
      v45 = 1416914273;
LABEL_113:
      sub_140FE72B0(&v51, v45, a3);
      goto LABEL_114;
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
    LODWORD(v52) = ((*(_WORD *)(a1 + 56) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 56) >> 9)
                 | (*(unsigned __int16 *)(a1 + 58) << 17);
    v38 = &qword_141B5C8A0;
    v51 = &qword_141B5C8A0;
    if ( &v51 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v46 = v51;
      v47 = v52;
      a3[1] = v52;
      *a3 = v46;
      v38 = (__int64 *)(sub_14083D4F0(v47) + 8);
      v52 = nullptr;
      v51 = v38;
    }
LABEL_104:
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v38 + 16))(v38, &v51);
LABEL_114:
    LOBYTE(v5) = 1;
    return v5;
  }
  if ( a2 > 1400075360 )
  {
    if ( a2 != 1400075361 )
    {
      if ( a2 == 1400138611 )
      {
        v5 = *(_DWORD *)(a1 + 92);
        if ( v5 != -1 )
        {
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v52) = v5;
          v51 = (__int64 *)v6;
          if ( &v51 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v43 = v51;
            v44 = v52;
            a3[1] = v52;
            *a3 = v43;
            v6 = sub_14083D4F0(v44) + 8;
            v52 = nullptr;
            v51 = (__int64 *)v6;
          }
          goto LABEL_108;
        }
      }
      else
      {
        if ( a2 != 1400142192 )
          return v5;
        v5 = *(char *)(a1 + 100);
        if ( v5 != -1 )
        {
          v6 = sub_14083D4F0(a1) + 40;
          LODWORD(v52) = v5;
          v51 = (__int64 *)v6;
          if ( &v51 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v15 = v51;
            v16 = v52;
            a3[1] = v52;
            *a3 = v15;
            v6 = sub_14083D4F0(v16) + 8;
            v52 = nullptr;
            v51 = (__int64 *)v6;
          }
          goto LABEL_108;
        }
      }
      goto LABEL_109;
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
    LODWORD(v52) = ((*(_WORD *)(a1 + 52) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 52) >> 9)
                 | (*(unsigned __int16 *)(a1 + 54) << 17);
    v38 = &qword_141B5C8A0;
    v51 = &qword_141B5C8A0;
    if ( &v51 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v41 = v51;
      v42 = v52;
      a3[1] = v52;
      *a3 = v41;
      v38 = (__int64 *)(sub_14083D4F0(v42) + 8);
      v52 = nullptr;
      v51 = v38;
    }
    goto LABEL_104;
  }
  if ( a2 == 1399748705 )
  {
    v5 = *(_DWORD *)(a1 + 80);
    if ( v5 != -1 )
    {
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v52) = v5;
      v51 = (__int64 *)v6;
      if ( &v51 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v24 = v51;
        v25 = v52;
        a3[1] = v52;
        *a3 = v24;
        v6 = sub_14083D4F0(v25) + 8;
        v52 = nullptr;
        v51 = (__int64 *)v6;
      }
      goto LABEL_108;
    }
    goto LABEL_109;
  }
  if ( a2 == 1399811172 )
  {
    v26 = *(_QWORD *)(a1 + 32);
    if ( v26 == 0 )
    {
LABEL_99:
      v31 = -1;
      v32 = -1;
LABEL_100:
      v51 = (__int64 *)__PAIR64__(v32, v31);
      v45 = 1937006948;
      goto LABEL_113;
    }
LABEL_76:
    v31 = *(_DWORD *)(v26 + 12);
    v32 = *(_DWORD *)(v26 + 16);
    if ( v32 == 0 )
      v32 = v31;
    goto LABEL_100;
  }
  if ( a2 != 1400071024 )
    return v5;
  v5 = *(_DWORD *)(a1 + 64);
  if ( v5 != -1 )
  {
    v6 = sub_14083D4F0(a1) + 40;
    LODWORD(v52) = v5;
    v51 = (__int64 *)v6;
    if ( &v51 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v7 = v51;
      v8 = v52;
      a3[1] = v52;
      *a3 = v7;
      v6 = sub_14083D4F0(v8) + 8;
      v52 = nullptr;
      v51 = (__int64 *)v6;
    }
LABEL_108:
    (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v51);
    goto LABEL_114;
  }
LABEL_109:
  LOBYTE(v5) = 1;
  if ( a3 != (__int64 **)&qword_141B5A4A0 )
  {
    (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
    (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
      qword_141B5A4A0,
      &qword_141B5A4A0,
      a3);
  }
  return v5;
}
