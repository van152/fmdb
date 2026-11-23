__int64 __fastcall sub_14143A1A0(__int64 a1, int a2, _QWORD *a3)
{
  _BYTE *v5; // rbx
  __int64 v6; // rax
  int v7; // ecx
  char v8; // al
  char v9; // cl
  char v10; // al
  char v11; // cl
  __int64 v12; // rax
  int v13; // ecx
  char v14; // al
  char v15; // cl
  __int64 v16; // rdx
  unsigned int v17; // eax
  unsigned int v18; // eax
  int v20; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v21[40]; // [rsp+30h] [rbp-28h] BYREF

  LODWORD(v5) = 0;
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
          if ( (__int64 *)*a3 == &qword_141B5C8A0 )
          {
            v17 = *((_DWORD *)a3 + 2);
            HIWORD(v20) = v17 >> 17;
            LOWORD(v20) = (v17 >> 8) & 0x1FF | ((_WORD)v17 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
          {
            v5 = v21;
            (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v21, a3);
            sub_1413CA830(&v20, v21);
          }
          else
          {
            v20 = 124518401;
          }
          *(_DWORD *)(a1 + 64) = v20;
          goto LABEL_67;
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
          if ( (__int64 *)*a3 == &qword_141B5C8A0 )
          {
            v18 = *((_DWORD *)a3 + 2);
            HIWORD(v20) = v18 >> 17;
            LOWORD(v20) = (v18 >> 8) & 0x1FF | ((_WORD)v18 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) == 27 )
          {
            v5 = v21;
            (*(void (__fastcall **)(_QWORD, _BYTE *, _QWORD *))(*(_QWORD *)*a3 + 160LL))(*a3, v21, a3);
            sub_1413CA830(&v20, v21);
          }
          else
          {
            v20 = 124518401;
          }
          *(_DWORD *)(a1 + 68) = v20;
          goto LABEL_67;
        case 1869507694:
          v8 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
          v9 = *(_BYTE *)(a1 + 84);
          if ( v8 != 0 )
            *(_BYTE *)(a1 + 84) = v9 | 1;
          else
            *(_BYTE *)(a1 + 84) = v9 & 0xFE;
          goto LABEL_67;
        default:
          break;
      }
      return (unsigned int)v5;
    }
    if ( a2 > 2037542769 )
    {
      if ( a2 != 2037542770 )
      {
        if ( a2 == 2037672052 )
        {
          v10 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
          v11 = *(_BYTE *)(a1 + 84);
          if ( v10 != 0 )
            *(_BYTE *)(a1 + 84) = v11 | 2;
          else
            *(_BYTE *)(a1 + 84) = v11 & 0xFD;
          goto LABEL_67;
        }
        return (unsigned int)v5;
      }
      *(_BYTE *)(a1 + 87) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
    else
    {
      if ( a2 == 1953655138 )
      {
        v14 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
        v15 = *(_BYTE *)(a1 + 84);
        if ( v14 != 0 )
          *(_BYTE *)(a1 + 84) = v15 | 0x20;
        else
          *(_BYTE *)(a1 + 84) = v15 & 0xDF;
        goto LABEL_67;
      }
      if ( a2 != 2036687218 )
        return (unsigned int)v5;
      *(_WORD *)(a1 + 80) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
    }
LABEL_67:
    LOBYTE(v5) = 1;
    return (unsigned int)v5;
  }
  if ( a2 <= 1684633192 )
  {
    if ( a2 == 1634758771 )
    {
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
        *(_BYTE *)(a1 + 85) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
      else
        *(_BYTE *)(a1 + 85) = -1;
      goto LABEL_67;
    }
    if ( a2 == 1667330920 )
    {
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
      {
        LOBYTE(v5) = 1;
        LOBYTE(v16) = 1;
        *(_DWORD *)(a1 + 76) = sub_140A3C930(a3, v16);
        return (unsigned int)v5;
      }
      goto LABEL_51;
    }
    if ( a2 != 1668049252 )
      return (unsigned int)v5;
    v5 = (_BYTE *)qword_141B5FE40;
    sub_140FE7960(v21, a3, 0);
    v6 = sub_140FA3700(v5, v21);
    *(_QWORD *)(a1 + 32) = v6;
    if ( v6 != 0 )
    {
      *(_DWORD *)(a1 + 56) = *(_DWORD *)(v6 + 12);
      v7 = *(_DWORD *)(v6 + 16);
      if ( v7 == 0 )
      {
        *(_DWORD *)(a1 + 60) = *(_DWORD *)(v6 + 12);
        goto LABEL_67;
      }
    }
    else
    {
      *(_DWORD *)(a1 + 56) = -1;
      v7 = -1;
    }
    *(_DWORD *)(a1 + 60) = v7;
    goto LABEL_67;
  }
  if ( a2 > 1752393323 )
  {
    if ( a2 == 1752393324 )
    {
      *(_BYTE *)(a1 + 84) &= 0xE3u;
      *(_BYTE *)(a1 + 84) |= (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_67;
    }
    if ( a2 != 1768842863 )
      return (unsigned int)v5;
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
    {
      *(_DWORD *)(a1 + 76) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      goto LABEL_67;
    }
LABEL_51:
    *(_DWORD *)(a1 + 76) = -1;
    goto LABEL_67;
  }
  if ( a2 == 1684633193 )
  {
    v5 = (_BYTE *)qword_141B5FDC0;
    sub_140FE7960(v21, a3, 0);
    v12 = sub_140F7A940(v5, v21);
    if ( v12 != 0 )
    {
      *(_DWORD *)(a1 + 48) = *(_DWORD *)(v12 + 12);
      v13 = *(_DWORD *)(v12 + 16);
      if ( v13 == 0 )
      {
        *(_DWORD *)(a1 + 52) = *(_DWORD *)(v12 + 12);
        goto LABEL_67;
      }
    }
    else
    {
      *(_DWORD *)(a1 + 48) = -1;
      v13 = -1;
    }
    *(_DWORD *)(a1 + 52) = v13;
    goto LABEL_67;
  }
  if ( a2 == 1735355507 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
      *(_BYTE *)(a1 + 86) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
    else
      *(_BYTE *)(a1 + 86) = -1;
    goto LABEL_67;
  }
  return (unsigned int)v5;
}
