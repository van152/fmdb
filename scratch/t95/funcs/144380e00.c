char __fastcall sub_144380E00(__int64 a1, int a2, _QWORD *a3)
{
  char result; // al
  char v6; // cl
  char v7; // cl
  __int64 v8; // rbx
  __int64 v9; // rax
  int v10; // eax
  char v11; // cl
  __int64 v12; // rbx
  __int64 v13; // rax
  int v14; // eax
  char v15; // cl
  _BYTE v16[40]; // [rsp+20h] [rbp-28h] BYREF

  result = 0;
  if ( a2 > 1835820397 )
  {
    if ( a2 <= 1937013105 )
    {
      if ( a2 != 1835820398 )
      {
        if ( a2 != 1851880553 )
          return result;
        v8 = qword_141B5FE08;
        sub_140FE7960(v16, a3, 1315856756);
        v9 = sub_140F7A940(v8, v16);
        if ( v9 != 0 )
          v10 = *(_DWORD *)(v9 + 12);
        else
          v10 = -1;
        *(_DWORD *)(a1 + 44) = v10;
        return 1;
      }
      *(_BYTE *)(a1 + 57) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      v15 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
      result = 1;
      if ( v15 == 0 )
        *(_BYTE *)(a1 + 57) = 0;
    }
    else
    {
      if ( a2 != 1937013106 )
      {
        if ( a2 == 1954115685 )
        {
          *(_BYTE *)(a1 + 54) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
        }
        else
        {
          if ( a2 != 2003985260 )
            return result;
          *(_WORD *)(a1 + 48) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        }
        return 1;
      }
      *(_WORD *)(a1 + 50) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
      v11 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
      result = 1;
      if ( v11 == 0 )
        *(_WORD *)(a1 + 50) = 1900;
    }
  }
  else
  {
    if ( a2 > 1769172838 )
    {
      if ( a2 == 1769172839 )
      {
        *(_BYTE *)(a1 + 58) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 48LL))(*a3, a3);
      }
      else
      {
        if ( a2 != 1818588780 )
        {
          if ( a2 == 1835100005 )
          {
            *(_BYTE *)(a1 + 56) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
            v6 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
            result = 1;
            if ( v6 == 0 )
              *(_BYTE *)(a1 + 56) = 0;
          }
          return result;
        }
        *(_BYTE *)(a1 + 55) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
      return 1;
    }
    if ( a2 == 1668246896 )
    {
      v12 = qword_141B5FDC0;
      sub_140FE7960(v16, a3, 1668246896);
      v13 = sub_140F7A940(v12, v16);
      if ( v13 != 0 )
        v14 = *(_DWORD *)(v13 + 12);
      else
        v14 = -1;
      *(_DWORD *)(a1 + 40) = v14;
      return 1;
    }
    if ( a2 == 1701738866 )
    {
      *(_WORD *)(a1 + 52) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 80LL))(*a3, a3);
      v7 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3);
      result = 1;
      if ( v7 == 0 )
        *(_WORD *)(a1 + 52) = 1900;
    }
  }
  return result;
}
