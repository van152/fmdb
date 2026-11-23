char __fastcall sub_141538FA0(__int64 a1, int a2, unsigned int *a3)
{
  char result; // al
  __int64 v6; // rbx
  __int64 v7; // rcx
  __int64 v8; // rbx
  __int64 v9; // rcx
  __int64 v10; // rbx
  __int64 v11; // rcx
  __int64 v12; // rbx
  __int64 v13; // rdi
  __int64 v14; // rdi
  unsigned int v15; // eax
  unsigned int v16; // eax
  unsigned int v17; // eax
  __int64 v18; // rdi
  __int64 v19; // [rsp+20h] [rbp-20h] BYREF
  int v20; // [rsp+28h] [rbp-18h]
  int v21; // [rsp+30h] [rbp-10h] BYREF
  __int64 v22; // [rsp+38h] [rbp-8h]

  v22 = -2;
  result = 0;
  if ( a2 <= 1399614819 )
  {
    if ( a2 > 1399022945 )
    {
      if ( a2 <= 1399025772 )
      {
        if ( a2 == 1399022946 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 68) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 68) = -1;
        }
        else
        {
          if ( a2 != 1399025267 )
            return result;
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_BYTE *)(a1 + 105) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_BYTE *)(a1 + 105) = -1;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1399025773:
            *(_BYTE *)(a1 + 101) = *(_BYTE *)(a1 + 101) & 0xFB
                                 | (4
                                  * (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(
                                      *(_QWORD *)a3,
                                      a3));
            break;
          case 1399612769:
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
              v15 = a3[2];
              HIWORD(v21) = v15 >> 17;
              LOWORD(v21) = (v15 >> 8) & 0x1FF | ((_WORD)v15 << 9);
            }
            else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                        *(_QWORD *)a3,
                        a3) == 27 )
            {
              (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 160LL))(
                *(_QWORD *)a3,
                &v19,
                a3);
              sub_1413CA830(&v21, &v19);
            }
            else
            {
              v21 = 124518401;
            }
            *(_DWORD *)(a1 + 48) = v21;
            break;
          case 1399613549:
            if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
              *(_BYTE *)(a1 + 102) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                       *(_QWORD *)a3,
                                       a3);
            else
              *(_BYTE *)(a1 + 102) = -1;
            break;
          default:
            return result;
        }
      }
    }
    else if ( a2 <= 1399019851 )
    {
      if ( a2 == 1398893684 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
        {
          v12 = qword_141B5FE28;
          sub_140FE7960(&v19, a3, 1937006948);
          *(_QWORD *)(a1 + 72) = sub_140F7A940(v12, &v19);
        }
        else
        {
          v20 = -1;
          v19 = sub_14083D4F0(v11) + 40;
          v18 = qword_141B5FE28;
          sub_140FE7960(&v21, &v19, 1937006948);
          *(_QWORD *)(a1 + 72) = sub_140F7A940(v18, &v21);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v19);
        }
      }
      else
      {
        if ( a2 != 1399018572 )
          return result;
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_BYTE *)(a1 + 103) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
        else
          *(_BYTE *)(a1 + 103) = -1;
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1399019852:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_BYTE *)(a1 + 104) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_BYTE *)(a1 + 104) = -1;
          break;
        case 1399021933:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 96) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 96) = -1;
          break;
        case 1399021936:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 60) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 60) = -1;
          break;
        default:
          return result;
      }
    }
  }
  else if ( a2 <= 1399748704 )
  {
    if ( a2 <= 1399743862 )
    {
      if ( a2 == 1399614820 )
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
        if ( *(__int64 **)a3 == &qword_141B5C8A0 )
        {
          v17 = a3[2];
          HIWORD(v21) = v17 >> 17;
          LOWORD(v21) = (v17 >> 8) & 0x1FF | ((_WORD)v17 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
        {
          (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, &v19, a3);
          sub_1413CA830(&v21, &v19);
        }
        else
        {
          v21 = 124518401;
        }
        *(_DWORD *)(a1 + 56) = v21;
      }
      else
      {
        if ( a2 != 1399680884 )
          return result;
        v6 = qword_141B5FE40;
        sub_140FE7960(&v19, a3, 1416914273);
        *(_QWORD *)(a1 + 24) = sub_140FA3700(v6, &v19);
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1399743863:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          {
            v10 = qword_141B5FE28;
            sub_140FE7960(&v19, a3, 1937006948);
            *(_QWORD *)(a1 + 40) = sub_140F7A940(v10, &v19);
          }
          else
          {
            v20 = -1;
            v19 = sub_14083D4F0(v9) + 40;
            v14 = qword_141B5FE28;
            sub_140FE7960(&v21, &v19, 1937006948);
            *(_QWORD *)(a1 + 40) = sub_140F7A940(v14, &v21);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v19);
          }
          break;
        case 1399745902:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 84) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 84) = -1;
          break;
        case 1399745912:
          if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
            *(_DWORD *)(a1 + 88) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                     *(_QWORD *)a3,
                                     a3);
          else
            *(_DWORD *)(a1 + 88) = -1;
          break;
        default:
          return result;
      }
    }
  }
  else if ( a2 > 1400075360 )
  {
    switch ( a2 )
    {
      case 1400075361:
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
        if ( *(__int64 **)a3 == &qword_141B5C8A0 )
        {
          v16 = a3[2];
          HIWORD(v21) = v16 >> 17;
          LOWORD(v21) = (v16 >> 8) & 0x1FF | ((_WORD)v16 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
        {
          (*(void (__fastcall **)(_QWORD, __int64 *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, &v19, a3);
          sub_1413CA830(&v21, &v19);
        }
        else
        {
          v21 = 124518401;
        }
        *(_DWORD *)(a1 + 52) = v21;
        break;
      case 1400138611:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_DWORD *)(a1 + 92) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
        else
          *(_DWORD *)(a1 + 92) = -1;
        break;
      case 1400142192:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_BYTE *)(a1 + 100) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
        else
          *(_BYTE *)(a1 + 100) = -1;
        break;
      default:
        return result;
    }
  }
  else
  {
    switch ( a2 )
    {
      case 1399748705:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_DWORD *)(a1 + 80) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
        else
          *(_DWORD *)(a1 + 80) = -1;
        break;
      case 1399811172:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
        {
          v8 = qword_141B5FE28;
          sub_140FE7960(&v19, a3, 1937006948);
          *(_QWORD *)(a1 + 32) = sub_140F7A940(v8, &v19);
        }
        else
        {
          v20 = -1;
          v19 = sub_14083D4F0(v7) + 40;
          v13 = qword_141B5FE28;
          sub_140FE7960(&v21, &v19, 1937006948);
          *(_QWORD *)(a1 + 32) = sub_140F7A940(v13, &v21);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v19);
        }
        break;
      case 1400071024:
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_DWORD *)(a1 + 64) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                   *(_QWORD *)a3,
                                   a3);
        else
          *(_DWORD *)(a1 + 64) = -1;
        break;
      default:
        return result;
    }
  }
  return 1;
}
