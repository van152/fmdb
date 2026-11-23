char __fastcall sub_1415799B0(__int64 a1, int a2, unsigned int *a3)
{
  char result; // al
  char v6; // al
  __int64 v7; // rcx
  __int64 v8; // rbx
  char v9; // al
  __int64 v10; // rcx
  char v11; // al
  __int64 v12; // rcx
  char v13; // al
  __int64 v14; // rcx
  char v15; // al
  __int64 v16; // rcx
  char v17; // al
  __int64 v18; // rcx
  __int64 v19; // rbx
  __int64 v20; // rax
  char v21; // al
  __int64 v22; // rcx
  __int64 v23; // rbx
  char v24; // al
  __int64 v25; // rcx
  unsigned int v26; // eax
  unsigned int v27; // eax
  int v28; // [rsp+28h] [rbp-30h] BYREF
  _DWORD v29[10]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 > 1347184235 )
  {
    if ( a2 > 1347186758 )
    {
      if ( a2 > 1347188578 )
      {
        switch ( a2 )
        {
          case 1347188579:
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              *(_WORD *)(a1 + 100) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                       *(_QWORD *)a3,
                                       a3);
            else
              *(_WORD *)(a1 + 100) = -1;
            break;
          case 1348887138:
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              *(_DWORD *)(a1 + 92) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                       *(_QWORD *)a3,
                                       a3);
            else
              *(_DWORD *)(a1 + 92) = 0;
            break;
          case 1886157170:
            sub_140FE8040(a1 + 24, a3);
            break;
          default:
            return result;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1347186759:
            if ( (unsigned __int8)sub_1400015B0() == 0 )
              return 0;
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              *(_DWORD *)(a1 + 96) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                       *(_QWORD *)a3,
                                       a3);
            else
              *(_DWORD *)(a1 + 96) = -1;
            break;
          case 1347187556:
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
              v26 = a3[2];
              HIWORD(v28) = v26 >> 17;
              LOWORD(v28) = (v26 >> 8) & 0x1FF | ((_WORD)v26 << 9);
            }
            else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                        *(_QWORD *)a3,
                        a3) == 27 )
            {
              (*(void (__fastcall **)(_QWORD, _DWORD *, unsigned int *))(**(_QWORD **)a3 + 160LL))(
                *(_QWORD *)a3,
                v29,
                a3);
              sub_1413CA830(&v28, v29);
            }
            else
            {
              v28 = 124518401;
            }
            *(_DWORD *)(a1 + 48) = v28;
            break;
          case 1347187566:
            *(_BYTE *)(a1 + 102) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            break;
          default:
            return result;
        }
      }
    }
    else if ( a2 > 1347186021 )
    {
      switch ( a2 )
      {
        case 1347186022:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 84) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 84) = 0;
          break;
        case 1347186530:
          v24 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v25 = *(_QWORD *)(a1 + 72);
          if ( v24 != 0 )
            *(_QWORD *)(a1 + 72) = v25 | 0x8000;
          else
            *(_QWORD *)(a1 + 72) = v25 & 0xFFFFFFFFFFFF7FFFuLL;
          break;
        case 1347186531:
          v11 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v12 = *(_QWORD *)(a1 + 72);
          if ( v11 != 0 )
            *(_QWORD *)(a1 + 72) = v12 | 1;
          else
            *(_QWORD *)(a1 + 72) = v12 & 0xFFFFFFFFFFFFFFFEuLL;
          break;
        default:
          return result;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1347184236:
          *(_DWORD *)(a1 + 72) &= 0xBFFFF9FF;
          *(_QWORD *)(a1 + 72) |= (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(
                                    *(_QWORD *)a3,
                                    a3);
          break;
        case 1347184995:
          v21 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v22 = *(_QWORD *)(a1 + 72);
          if ( v21 != 0 )
            *(_QWORD *)(a1 + 72) = v22 | 2;
          else
            *(_QWORD *)(a1 + 72) = v22 & 0xFFFFFFFFFFFFFFFDuLL;
          break;
        case 1347186019:
          v6 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v7 = *(_QWORD *)(a1 + 72);
          if ( v6 != 0 )
            *(_QWORD *)(a1 + 72) = v7 | 0x10000;
          else
            *(_QWORD *)(a1 + 72) = v7 & 0xFFFFFFFFFFFEFFFFuLL;
          break;
        default:
          return result;
      }
    }
  }
  else if ( a2 > 1347183467 )
  {
    switch ( a2 )
    {
      case 1347183468:
        v8 = qword_141B5FE40;
        sub_140FE7960(v29, a3, 1416914273);
        *(_QWORD *)(a1 + 32) = sub_140FA3700(v8, v29);
        return 1;
      case 1347183469:
        v13 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v14 = *(_QWORD *)(a1 + 72);
        if ( v13 != 0 )
          *(_QWORD *)(a1 + 72) = v14 | 0x100000;
        else
          *(_QWORD *)(a1 + 72) = v14 & 0xFFFFFFFFFFEFFFFFuLL;
        return 1;
      case 1347183470:
      case 1347183471:
      case 1347183472:
      case 1347183473:
      case 1347183475:
        return result;
      case 1347183474:
        v15 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v16 = *(_QWORD *)(a1 + 72);
        if ( v15 != 0 )
          *(_QWORD *)(a1 + 72) = v16 | 0x2000;
        else
          *(_QWORD *)(a1 + 72) = v16 & 0xFFFFFFFFFFFFDFFFuLL;
        return 1;
      case 1347183476:
        v17 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v18 = *(_QWORD *)(a1 + 72);
        if ( v17 != 0 )
          *(_QWORD *)(a1 + 72) = v18 | 0x1000;
        else
          *(_QWORD *)(a1 + 72) = v18 & 0xFFFFFFFFFFFFEFFFuLL;
        return 1;
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
          if ( *(__int64 **)a3 == &qword_141B5C8A0 )
          {
            v27 = a3[2];
            HIWORD(v28) = v27 >> 17;
            LOWORD(v28) = (v27 >> 8) & 0x1FF | ((_WORD)v27 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                      *(_QWORD *)a3,
                      a3) == 27 )
          {
            (*(void (__fastcall **)(_QWORD, _DWORD *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v29, a3);
            sub_1413CA830(&v28, v29);
          }
          else
          {
            v28 = 124518401;
          }
          *(_DWORD *)(a1 + 52) = v28;
        }
        else
        {
          if ( a2 != 1347184226 )
            return result;
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 88) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 88) = 0;
        }
        break;
    }
  }
  else if ( a2 > 1347176043 )
  {
    switch ( a2 )
    {
      case 1347176044:
        v23 = qword_141B5FE40;
        sub_140FE7960(v29, a3, 1416914273);
        *(_QWORD *)(a1 + 40) = sub_140FA3700(v23, v29);
        break;
      case 1347178055:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_BYTE *)(a1 + 103) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
        else
          *(_BYTE *)(a1 + 103) = -1;
        break;
      case 1347183218:
        v9 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v10 = *(_QWORD *)(a1 + 72);
        if ( v9 != 0 )
          *(_QWORD *)(a1 + 72) = v10 | 4;
        else
          *(_QWORD *)(a1 + 72) = v10 & 0xFFFFFFFFFFFFFFFBuLL;
        break;
      default:
        return result;
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1347174723:
        v19 = qword_141B5FDC0;
        sub_140FE7960(v29, a3, 1668246896);
        v20 = sub_140F7A940(v19, v29);
        if ( v20 != 0 )
          *(_DWORD *)(a1 + 56) = *(_DWORD *)(v20 + 8);
        else
          *(_DWORD *)(a1 + 56) = -1;
        break;
      case 1347174739:
        sub_140FE7960(v29, a3, 0);
        *(_DWORD *)(a1 + 60) = v29[0];
        break;
      case 1347174740:
        *(_BYTE *)(a1 + 68) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                *(_QWORD *)a3,
                                a3);
        break;
      default:
        return result;
    }
  }
  return 1;
}
