__int64 __fastcall sub_141439760(__int64 a1, int a2, __int64 **a3)
{
  unsigned int v5; // edi
  __int64 v6; // rax
  __int64 *v7; // rax
  __int64 *v8; // rcx
  __int64 *v9; // rax
  __int64 *v10; // rcx
  __int64 v11; // rax
  int v12; // ecx
  int v13; // eax
  char v14; // bl
  __int64 *v15; // rax
  __int64 *v16; // rcx
  __int64 *v17; // rax
  __int64 *v18; // rcx
  char v19; // bl
  __int64 *v20; // rax
  __int64 *v21; // rcx
  __int64 **v22; // rcx
  __int64 v23; // rdx
  char v24; // bl
  __int64 *v25; // rax
  __int64 *v26; // rcx
  __int64 *v27; // rax
  __int64 *v28; // rcx
  __int64 *v29; // rax
  __int64 *v30; // rcx
  __int64 *v31; // rcx
  __int64 *v32; // rax
  __int64 *v33; // rcx
  __int64 *v34; // rax
  __int64 *v35; // rcx
  __int64 *v36; // rax
  __int64 *v37; // rcx
  __int64 *v38; // rax
  __int64 *v39; // rcx
  __int64 *v41; // [rsp+20h] [rbp-10h] BYREF
  __int64 *v42; // [rsp+28h] [rbp-8h]
  __int64 v43; // [rsp+30h] [rbp+0h]

  v43 = -2;
  v5 = 0;
  if ( a2 > 1785686381 )
  {
    if ( a2 <= 1953655137 )
    {
      switch ( a2 )
      {
        case 1785686382:
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
          LODWORD(v42) = ((*(_WORD *)(a1 + 64) & 0x1FF) << 8)
                       | (*(unsigned __int16 *)(a1 + 64) >> 9)
                       | (*(unsigned __int16 *)(a1 + 66) << 17);
          v31 = &qword_141B5C8A0;
          v41 = &qword_141B5C8A0;
          if ( &v41 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v32 = v41;
            v33 = v42;
            a3[1] = v42;
            *a3 = v32;
            v31 = (__int64 *)(sub_14083D4F0(v33) + 8);
            v42 = nullptr;
            v41 = v31;
          }
          break;
        case 1818583414:
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
          LODWORD(v42) = ((*(_WORD *)(a1 + 68) & 0x1FF) << 8)
                       | (*(unsigned __int16 *)(a1 + 68) >> 9)
                       | (*(unsigned __int16 *)(a1 + 70) << 17);
          v31 = &qword_141B5C8A0;
          v41 = &qword_141B5C8A0;
          if ( &v41 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v34 = v41;
            v35 = v42;
            a3[1] = v42;
            *a3 = v34;
            v31 = (__int64 *)(sub_14083D4F0(v35) + 8);
            v42 = nullptr;
            v41 = v31;
          }
          break;
        case 1869507694:
          v14 = *(_BYTE *)(a1 + 84) & 1;
          v6 = sub_14083D4F0(a1) + 24;
          LOBYTE(v42) = v14;
          v41 = (__int64 *)v6;
          if ( &v41 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v15 = v41;
            v16 = v42;
            a3[1] = v42;
            *a3 = v15;
            v6 = sub_14083D4F0(v16) + 8;
            v42 = nullptr;
            v41 = (__int64 *)v6;
          }
          goto LABEL_69;
        default:
          return v5;
      }
      (*(void (__fastcall **)(__int64 *, __int64 **))(*v31 + 16))(v31, &v41);
LABEL_73:
      LOBYTE(v5) = 1;
      return v5;
    }
    if ( a2 > 2037542769 )
    {
      if ( a2 == 2037542770 )
      {
        v5 = *(char *)(a1 + 87);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v42) = v5;
        v41 = (__int64 *)v6;
        if ( &v41 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v38 = v41;
          v39 = v42;
          a3[1] = v42;
          *a3 = v38;
          v6 = sub_14083D4F0(v39) + 8;
          v42 = nullptr;
          v41 = (__int64 *)v6;
        }
        goto LABEL_69;
      }
      if ( a2 == 2037672052 )
      {
        v19 = *(_BYTE *)(a1 + 84);
        v6 = sub_14083D4F0(a1) + 24;
        LOBYTE(v42) = (v19 & 2) != 0;
        v41 = (__int64 *)v6;
        if ( &v41 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v20 = v41;
          v21 = v42;
          a3[1] = v42;
          *a3 = v20;
          v6 = sub_14083D4F0(v21) + 8;
          v42 = nullptr;
          v41 = (__int64 *)v6;
        }
        goto LABEL_69;
      }
    }
    else
    {
      if ( a2 == 1953655138 )
      {
        v24 = *(_BYTE *)(a1 + 84);
        v6 = sub_14083D4F0(a1) + 24;
        LOBYTE(v42) = (v24 & 0x20) != 0;
        v41 = (__int64 *)v6;
        if ( &v41 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v25 = v41;
          v26 = v42;
          a3[1] = v42;
          *a3 = v25;
          v6 = sub_14083D4F0(v26) + 8;
          v42 = nullptr;
          v41 = (__int64 *)v6;
        }
        goto LABEL_69;
      }
      if ( a2 == 2036687218 )
      {
        v5 = *(__int16 *)(a1 + 80);
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v42) = v5;
        v41 = (__int64 *)v6;
        if ( &v41 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v9 = v41;
          v10 = v42;
          a3[1] = v42;
          *a3 = v9;
          v6 = sub_14083D4F0(v10) + 8;
          v42 = nullptr;
          v41 = (__int64 *)v6;
        }
        goto LABEL_69;
      }
    }
  }
  else
  {
    if ( a2 <= 1684633192 )
    {
      switch ( a2 )
      {
        case 1634758771:
          v5 = *(unsigned __int8 *)(a1 + 85);
          if ( v5 != 255 )
          {
            v6 = sub_14083D4F0(a1) + 56;
            LODWORD(v42) = v5;
            v41 = (__int64 *)v6;
            if ( &v41 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v27 = v41;
              v28 = v42;
              a3[1] = v42;
              *a3 = v27;
              v6 = sub_14083D4F0(v28) + 8;
              v42 = nullptr;
              v41 = (__int64 *)v6;
            }
            goto LABEL_69;
          }
          break;
        case 1667330920:
          v5 = *(_DWORD *)(a1 + 76);
          if ( (v5 & 0x80000000) == 0 )
          {
            v6 = sub_14083D4F0(a1) + 40;
            LODWORD(v42) = v5;
            v41 = (__int64 *)v6;
            if ( &v41 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v29 = v41;
              v30 = v42;
              a3[1] = v42;
              *a3 = v29;
              v6 = sub_14083D4F0(v30) + 8;
              v42 = nullptr;
              v41 = (__int64 *)v6;
            }
            goto LABEL_69;
          }
          break;
        case 1668049252:
          v11 = *(_QWORD *)(a1 + 32);
          if ( v11 != 0 )
          {
            v12 = *(_DWORD *)(v11 + 12);
            LODWORD(v41) = v12;
            v13 = *(_DWORD *)(v11 + 16);
            if ( v13 == 0 )
              v13 = v12;
            HIDWORD(v41) = v13;
          }
          else
          {
            v41 = *(__int64 **)(a1 + 56);
          }
          v22 = &v41;
          v23 = 1416914273;
          goto LABEL_72;
        default:
          return v5;
      }
LABEL_54:
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
    if ( a2 <= 1752393323 )
    {
      if ( a2 != 1684633193 )
      {
        if ( a2 != 1735355507 )
          return v5;
        v5 = *(unsigned __int8 *)(a1 + 86);
        if ( v5 != 255 )
        {
          v6 = sub_14083D4F0(a1) + 56;
          LODWORD(v42) = v5;
          v41 = (__int64 *)v6;
          if ( &v41 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v7 = v41;
            v8 = v42;
            a3[1] = v42;
            *a3 = v7;
            v6 = sub_14083D4F0(v8) + 8;
            v42 = nullptr;
            v41 = (__int64 *)v6;
          }
LABEL_69:
          (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v6 + 16LL))(v6, &v41);
          goto LABEL_73;
        }
        goto LABEL_54;
      }
      v22 = (__int64 **)(a1 + 48);
      v23 = 1668246896;
LABEL_72:
      sub_140FE72B0(v22, v23, a3);
      goto LABEL_73;
    }
    if ( a2 == 1752393324 )
    {
      v5 = *(_BYTE *)(a1 + 84) & 0x1C;
      v6 = sub_14083D4F0(a1) + 40;
      LODWORD(v42) = v5;
      v41 = (__int64 *)v6;
      if ( &v41 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v36 = v41;
        v37 = v42;
        a3[1] = v42;
        *a3 = v36;
        v6 = sub_14083D4F0(v37) + 8;
        v42 = nullptr;
        v41 = (__int64 *)v6;
      }
      goto LABEL_69;
    }
    if ( a2 == 1768842863 )
    {
      v5 = *(_DWORD *)(a1 + 76);
      if ( (int)v5 <= -2 && v5 != -4 )
      {
        v6 = sub_14083D4F0(a1) + 40;
        LODWORD(v42) = v5;
        v41 = (__int64 *)v6;
        if ( &v41 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v17 = v41;
          v18 = v42;
          a3[1] = v42;
          *a3 = v17;
          v6 = sub_14083D4F0(v18) + 8;
          v42 = nullptr;
          v41 = (__int64 *)v6;
        }
        goto LABEL_69;
      }
      goto LABEL_54;
    }
  }
  return v5;
}
