char __fastcall sub_1415698A0(__int64 a1, int a2, unsigned int *a3)
{
  char result; // al
  unsigned int v6; // eax
  __int64 v7; // rbx
  __int64 v8; // rbx
  char v9; // al
  __int16 v10; // cx
  __int64 v11; // rbx
  char v12; // al
  __int16 v13; // cx
  __int64 v14; // rbx
  __int64 v15; // rbx
  char v16; // al
  __int16 v17; // cx
  __int64 v18; // rbx
  __int64 v19; // rbx
  char v20; // al
  __int16 v21; // cx
  __int64 v22; // rbx
  int v23; // eax
  __int16 v24; // cx
  __int16 v25; // dx
  unsigned int v26; // eax
  int v27; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v28[40]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 <= 1752396848 )
  {
    if ( a2 <= 1667789925 )
    {
      if ( a2 > 1667526259 )
      {
        switch ( a2 )
        {
          case 1667526260:
            v16 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
            v17 = *(_WORD *)(a1 + 116);
            if ( v16 != 0 )
              *(_WORD *)(a1 + 116) = v17 | 8;
            else
              *(_WORD *)(a1 + 116) = v17 & 0xFFF7;
            break;
          case 1667786105:
            *(_WORD *)(a1 + 114) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            break;
          case 1667789689:
            *(_WORD *)(a1 + 112) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
            break;
          default:
            return result;
        }
        return 1;
      }
      if ( a2 != 1633907311 )
      {
        if ( a2 != 1667526246 )
          return result;
        v9 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v10 = *(_WORD *)(a1 + 116);
        if ( v9 != 0 )
          *(_WORD *)(a1 + 116) = v10 | 0x100;
        else
          *(_WORD *)(a1 + 116) = v10 & 0xFEFF;
        return 1;
      }
      *(_BYTE *)(a1 + 116) &= 0xC9u;
      v6 = (*(_DWORD *)(a1 + 116) & 0xFFFFFFFB)
         + 4 * (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
      goto LABEL_54;
    }
    if ( a2 <= 1685349474 )
    {
      if ( a2 == 1667789926 )
      {
        v23 = *(unsigned __int16 *)(a1 + 116);
        v24 = *(_WORD *)(a1 + 116) & 0xFFC9;
        v25 = 0;
        if ( v23 != 255 )
          v25 = v24;
        *(_WORD *)(a1 + 116) = v25;
        *(_WORD *)(a1 + 116) |= (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(
                                  *(_QWORD *)a3,
                                  a3);
      }
      else
      {
        if ( a2 != 1668181860 )
          return result;
        v12 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
        v13 = *(_WORD *)(a1 + 116);
        if ( v12 != 0 )
          *(_WORD *)(a1 + 116) = v13 | 0xFF;
        else
          *(_WORD *)(a1 + 116) = v13 & 0xFF00;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1685349475:
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
            HIWORD(v27) = v26 >> 17;
            LOWORD(v27) = (v26 >> 8) & 0x1FF | ((_WORD)v26 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                      *(_QWORD *)a3,
                      a3) == 27 )
          {
            (*(void (__fastcall **)(_QWORD, _BYTE *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v28, a3);
            sub_1413CA830(&v27, v28);
          }
          else
          {
            v27 = 124518401;
          }
          *(_DWORD *)(a1 + 104) = v27;
          break;
        case 1751807095:
          v20 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
          v21 = *(_WORD *)(a1 + 116);
          if ( v20 != 0 )
            *(_WORD *)(a1 + 116) = v21 | 1;
          else
            *(_WORD *)(a1 + 116) = v21 & 0xFFFE;
          break;
        case 1752134516:
          v8 = qword_141B5FE28;
          sub_140FE7960(v28, a3, 1937006948);
          *(_QWORD *)(a1 + 64) = sub_140F7A940(v8, v28);
          break;
        default:
          return result;
      }
    }
  }
  else
  {
    if ( a2 <= 1886150962 )
    {
      if ( a2 <= 1752396850 )
      {
        v11 = qword_141B5FE40;
        if ( a2 == 1752396849 )
        {
          sub_140FE7960(v28, a3, 1416914273);
          *(_QWORD *)(a1 + 72) = sub_140FA3700(v11, v28);
        }
        else
        {
          sub_140FE7960(v28, a3, 1416914273);
          *(_QWORD *)(a1 + 80) = sub_140FA3700(v11, v28);
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1752396851:
            v18 = qword_141B5FE40;
            sub_140FE7960(v28, a3, 1416914273);
            *(_QWORD *)(a1 + 88) = sub_140FA3700(v18, v28);
            break;
          case 1886150961:
            v19 = qword_141B5FE40;
            sub_140FE7960(v28, a3, 1416914273);
            *(_QWORD *)(a1 + 32) = sub_140FA3700(v19, v28);
            break;
          case 1886150962:
            v7 = qword_141B5FE40;
            sub_140FE7960(v28, a3, 1416914273);
            *(_QWORD *)(a1 + 40) = sub_140FA3700(v7, v28);
            break;
          default:
            return result;
        }
      }
      return 1;
    }
    if ( a2 > 1937008493 )
    {
      switch ( a2 )
      {
        case 1937008494:
          v22 = qword_141B5FE38;
          sub_140FE7960(v28, a3, 1937008494);
          *(_QWORD *)(a1 + 96) = sub_140FA3700(v22, v28);
          break;
        case 2037542770:
          *(_BYTE *)(a1 + 118) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
          break;
        case 2036687218:
          *(_WORD *)(a1 + 108) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
          break;
        default:
          return result;
      }
      return 1;
    }
    switch ( a2 )
    {
      case 1886150963:
        v14 = qword_141B5FE40;
        sub_140FE7960(v28, a3, 1416914273);
        *(_QWORD *)(a1 + 48) = sub_140FA3700(v14, v28);
        break;
      case 1886156654:
        v15 = qword_141B5FE40;
        sub_140FE7960(v28, a3, 1416914273);
        *(_QWORD *)(a1 + 56) = sub_140FA3700(v15, v28);
        break;
      case 1936289383:
        *(_BYTE *)(a1 + 116) &= 0xC9u;
        v6 = (*(_DWORD *)(a1 + 116) & 0xFFFFFFFD)
           + 2 * (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(*(_QWORD *)a3, a3);
LABEL_54:
        *(_WORD *)(a1 + 116) = v6;
        return 1;
      default:
        return result;
    }
  }
  return 1;
}
