char __fastcall sub_14437F2A0(__int64 a1, int a2, unsigned int *a3)
{
  char result; // al
  __int64 v6; // rbx
  unsigned int v7; // eax
  unsigned int v8; // eax
  __int64 v9; // rdx
  __int64 v10; // rdx
  __int64 v11; // rdx
  __int64 v12; // rdx
  int v13; // [rsp+28h] [rbp-30h] BYREF
  _BYTE v14[40]; // [rsp+30h] [rbp-28h] BYREF

  result = 0;
  if ( a2 > 1952801132 )
  {
    if ( a2 == 1953132386 )
    {
      *(_WORD *)(a1 + 56) = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 80LL))(
                              *(_QWORD *)a3,
                              a3);
    }
    else
    {
      if ( a2 != 1952801133 )
        return result;
      v6 = qword_141B5FE40;
      sub_140FE7960(v14, a3, 1416914273);
      *(_QWORD *)(a1 + 32) = sub_140FA3700(v6, v14);
    }
  }
  else if ( a2 == 1785686382 )
  {
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        qword_141B5C8A0 = 0x141759DF8LL;
        byte_141B5C8A8 = 32;
        LOBYTE(v11) = 32;
        sub_1412EA280(&qword_141B5C8B0, v11);
        LOBYTE(v12) = 32;
        sub_1412EB230(&qword_141B5C8C0, v12);
        qword_141B5C8A0 = 0x141876208LL;
        qword_141B5C8B0 = 0x1418762E8LL;
        qword_141B5C8C0 = 0x141876308LL;
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    if ( *(__int64 **)a3 == &qword_141B5C8A0 )
    {
      v8 = a3[2];
      HIWORD(v13) = v8 >> 17;
      LOWORD(v13) = (v8 >> 8) & 0x1FF | ((_WORD)v8 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
    {
      (*(void (__fastcall **)(_QWORD, _BYTE *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v14, a3);
      sub_1413CA830(&v13, v14);
    }
    else
    {
      v13 = 124518401;
    }
    *(_DWORD *)(a1 + 40) = v13;
  }
  else
  {
    if ( a2 != 1818584692 )
      return result;
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B5C8D0);
      if ( dword_141B5C8D0 == -1 )
      {
        qword_141B5C8A0 = 0x141759DF8LL;
        byte_141B5C8A8 = 32;
        LOBYTE(v9) = 32;
        sub_1412EA280(&qword_141B5C8B0, v9);
        LOBYTE(v10) = 32;
        sub_1412EB230(&qword_141B5C8C0, v10);
        qword_141B5C8A0 = 0x141876208LL;
        qword_141B5C8B0 = 0x1418762E8LL;
        qword_141B5C8C0 = 0x141876308LL;
        sub_141751048(sub_140DBCA10);
        sub_141750EA0(&dword_141B5C8D0);
      }
    }
    if ( *(__int64 **)a3 == &qword_141B5C8A0 )
    {
      v7 = a3[2];
      HIWORD(v13) = v7 >> 17;
      LOWORD(v13) = (v7 >> 8) & 0x1FF | ((_WORD)v7 << 9);
    }
    else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(*(_QWORD *)a3, a3) == 27 )
    {
      (*(void (__fastcall **)(_QWORD, _BYTE *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v14, a3);
      sub_1413CA830(&v13, v14);
    }
    else
    {
      v13 = 124518401;
    }
    *(_DWORD *)(a1 + 44) = v13;
  }
  return 1;
}
