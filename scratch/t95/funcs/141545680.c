char __fastcall sub_141545680(__int64 a1, int a2, __int64 **a3)
{
  char result; // al
  __int64 v7; // rdx
  __int64 v8; // rcx
  unsigned int v9; // eax
  unsigned int v10; // eax
  unsigned int v11; // eax
  __int16 v12; // ax
  __int16 v13; // cx
  __int16 v14; // bx
  __int16 v15; // ax
  __int16 v16; // cx
  __int16 v17; // bx
  int v18; // [rsp+20h] [rbp-28h] BYREF
  _QWORD v19[4]; // [rsp+28h] [rbp-20h] BYREF

  if ( (unsigned __int8)sub_140FE2700((_DWORD *)a1, a2, a3) != 0 )
    return 1;
  result = 0;
  if ( a2 <= 1768842862 )
  {
    if ( a2 > 1701733491 )
    {
      if ( a2 <= 1718839155 )
      {
        if ( a2 == 1701733492 )
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
          if ( *a3 == &qword_141B5C8A0 )
          {
            v9 = *((_DWORD *)a3 + 2);
            HIWORD(v18) = v9 >> 17;
            LOWORD(v18) = (v9 >> 8) & 0x1FF | ((_WORD)v9 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 27 )
          {
            (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 160))(*a3, v19, a3);
            sub_1413CA830(&v18, v19);
          }
          else
          {
            v18 = 124518401;
          }
          *(_DWORD *)(a1 + 68) = v18;
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          {
            v15 = *(_WORD *)(a1 + 68);
            if ( (v15 & 0x1FF) == 1 && *(_WORD *)(a1 + 70) == 1900 )
            {
              v16 = word_141AB0260;
              if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
              {
                word_141AB0260 = 2023;
                v16 = 2023;
              }
              v17 = 3;
              if ( (unsigned __int16)(23593 * v16) < 0xA3Eu )
                v17 = 15;
              *(_WORD *)(a1 + 70) = v16;
              *(_WORD *)(a1 + 68) = ((unsigned __int16)(v16 & v17) == 0) + (v15 & 0xFE00) + 182;
            }
          }
          return 1;
        }
        if ( a2 == 1702127982 )
        {
          *(_BYTE *)(a1 + 93) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          return 1;
        }
        return result;
      }
      if ( a2 == 1718839156 )
      {
        *(_WORD *)(a1 + 88) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      }
      if ( a2 != 1734438259 )
      {
        if ( a2 == 1735355507 )
        {
          *(_WORD *)(a1 + 86) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 0 )
            *(_WORD *)(a1 + 86) = -1;
          return 1;
        }
        return result;
      }
    }
    else
    {
      if ( a2 > 1667330919 )
      {
        switch ( a2 )
        {
          case 1667330920:
            *(_DWORD *)(a1 + 80) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
            return 1;
          case 1668182900:
            *(_BYTE *)(a1 + 93) = (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3) != 0;
            return 1;
          case 1668246896:
            sub_140FE7960(v19, a3, 0);
            *(_QWORD *)(a1 + 48) = v19[0];
            return 1;
          default:
            break;
        }
        return result;
      }
      if ( a2 != 1634758771 )
      {
        if ( a2 == 1635021925 )
        {
          *(_DWORD *)(a1 + 80) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 0 )
            *(_DWORD *)(a1 + 80) = -1;
          return 1;
        }
        return result;
      }
    }
    *(_WORD *)(a1 + 84) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    return 1;
  }
  if ( a2 > 1937007713 )
  {
    if ( a2 <= 1937008995 )
    {
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
        if ( *a3 == &qword_141B5C8A0 )
        {
          v10 = *((_DWORD *)a3 + 2);
          HIWORD(v18) = v10 >> 17;
          LOWORD(v18) = (v10 >> 8) & 0x1FF | ((_WORD)v10 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 27 )
        {
          (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 160))(*a3, v19, a3);
          sub_1413CA830(&v18, v19);
        }
        else
        {
          v18 = 124518401;
        }
        *(_DWORD *)(a1 + 72) = v18;
        return 1;
      }
      if ( a2 == 1937007732 )
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
        if ( *a3 == &qword_141B5C8A0 )
        {
          v11 = *((_DWORD *)a3 + 2);
          HIWORD(v18) = v11 >> 17;
          LOWORD(v18) = (v11 >> 8) & 0x1FF | ((_WORD)v11 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 27 )
        {
          (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 160))(*a3, v19, a3);
          sub_1413CA830(&v18, v19);
        }
        else
        {
          v18 = 124518401;
        }
        *(_DWORD *)(a1 + 64) = v18;
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
        {
          v12 = *(_WORD *)(a1 + 64);
          if ( (v12 & 0x1FF) == 1 && *(_WORD *)(a1 + 66) == 1900 )
          {
            v13 = word_141AB0260;
            if ( (unsigned __int16)word_141AB0260 >= 0x7E8u )
            {
              word_141AB0260 = 2023;
              v13 = 2023;
            }
            v14 = 3;
            if ( (unsigned __int16)(23593 * v13) < 0xA3Eu )
              v14 = 15;
            *(_WORD *)(a1 + 66) = v13;
            *(_WORD *)(a1 + 64) = ((unsigned __int16)(v13 & v14) == 0) + (v12 & 0xFE00) + 182;
          }
        }
        return 1;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1952801133:
          sub_140FE7960(v19, a3, 0);
          *(_QWORD *)(a1 + 32) = v19[0];
          return 1;
        case 1937010285:
          (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v19, a3);
          v8 = *(_QWORD *)(a1 + 56);
          if ( v8 == v19[0] )
          {
            if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 - 4)) == 0 )
              sub_1412EC9A0(v8 - 4, v7);
          }
          else
          {
            if ( v8 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8 - 4)) == 0 )
              sub_1412EC9A0(v8 - 4, v7);
            *(_QWORD *)(a1 + 56) = v19[0];
          }
          return 1;
        case 1937008996:
          sub_140FE7960(v19, a3, 0);
          *(_QWORD *)(a1 + 24) = v19[0];
          return 1;
        default:
          break;
      }
    }
  }
  else if ( a2 <= 1869899891 )
  {
    if ( a2 == 1768842863 )
    {
      *(_BYTE *)(a1 + 91) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      return 1;
    }
    if ( a2 == 1869048947 )
    {
      *(_WORD *)(a1 + 88) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 0 )
        *(_WORD *)(a1 + 88) = -1;
      return 1;
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1869899892:
        sub_140FE7960(v19, a3, 0);
        *(_QWORD *)(a1 + 40) = v19[0];
        return 1;
      case 1918989417:
        *(_BYTE *)(a1 + 90) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      case 1920099681:
        *(_BYTE *)(a1 + 92) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        return 1;
      default:
        break;
    }
  }
  return result;
}
