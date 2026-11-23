char __fastcall sub_143FC4210(__int64 a1, int a2, unsigned int *a3)
{
  char result; // al
  __int64 v6; // rbx
  unsigned int v7; // eax
  unsigned int v8; // eax
  int v9; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v10[40]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 > 1886545267 )
  {
    if ( a2 > 1936286820 )
    {
      if ( a2 == 1936286821 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) != 0 )
          *(_BYTE *)(a1 + 51) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                                  *(_QWORD *)a3,
                                  a3);
        else
          *(_BYTE *)(a1 + 51) = 3;
      }
      else
      {
        if ( a2 != 1937007732 )
          return result;
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
          v8 = a3[2];
          HIWORD(v9) = v8 >> 17;
          LOWORD(v9) = (v8 >> 8) & 0x1FF | ((_WORD)v8 << 9);
        }
        else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
        {
          (*(void (__fastcall **)(_QWORD, _BYTE *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v10, a3);
          sub_1413CA830(&v9, v10);
        }
        else
        {
          v9 = 124518401;
        }
        *(_DWORD *)(a1 + 40) = v9;
      }
    }
    else if ( a2 == 1886545268 )
    {
      *(_BYTE *)(a1 + 52) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(
                              *(_QWORD *)a3,
                              a3);
    }
    else
    {
      if ( a2 != 1936029285 )
        return result;
      *(_BYTE *)(a1 + 50) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(
                              *(_QWORD *)a3,
                              a3);
    }
  }
  else if ( a2 > 1768843892 )
  {
    if ( a2 == 1768843893 )
    {
      v6 = qword_141B5FDE8;
      sub_140FE7960(v10, a3, 1768843890);
      *(_QWORD *)(a1 + 32) = sub_140FA3700(v6, v10);
    }
    else
    {
      if ( a2 != 1885696621 )
        return result;
      *(_BYTE *)(a1 + 49) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(
                              *(_QWORD *)a3,
                              a3);
    }
  }
  else if ( a2 == 1701733492 )
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
      v7 = a3[2];
      HIWORD(v9) = v7 >> 17;
      LOWORD(v9) = (v7 >> 8) & 0x1FF | ((_WORD)v7 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
    {
      (*(void (__fastcall **)(_QWORD, _BYTE *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v10, a3);
      sub_1413CA830(&v9, v10);
    }
    else
    {
      v9 = 124518401;
    }
    *(_DWORD *)(a1 + 44) = v9;
  }
  else
  {
    if ( a2 != 1718973557 )
      return result;
    *(_BYTE *)(a1 + 48) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 48LL))(
                            *(_QWORD *)a3,
                            a3);
  }
  return 1;
}
